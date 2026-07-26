#!/usr/bin/env python3
"""Fast structural QA for the simplified research-figure workflow."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def number(value: str | None) -> float | None:
    if value is None:
        return None
    match = re.match(r"^\s*(-?(?:\d+(?:\.\d*)?|\.\d+))", value)
    return float(match.group(1)) if match else None


def box4(value: str | None) -> tuple[float, float, float, float] | None:
    if value is None:
        return None
    parts = value.replace(",", " ").split()
    if len(parts) != 4:
        return None
    try:
        box = tuple(float(item) for item in parts)
    except ValueError:
        return None
    if box[2] <= 0 or box[3] <= 0:
        return None
    return box  # type: ignore[return-value]


def contains(
    outer: tuple[float, float, float, float],
    inner: tuple[float, float, float, float],
    tolerance: float = 1e-6,
) -> bool:
    ox, oy, ow, oh = outer
    ix, iy, iw, ih = inner
    return (
        ix >= ox - tolerance
        and iy >= oy - tolerance
        and ix + iw <= ox + ow + tolerance
        and iy + ih <= oy + oh + tolerance
    )


def normalized_text(element: ET.Element) -> str:
    return " ".join("".join(element.itertext()).split())


def png_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()[:24]
    except OSError:
        return None
    if len(data) < 24 or not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return None
    return struct.unpack(">II", data[16:24])


def find_chromium() -> str | None:
    candidates = [
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        shutil.which("microsoft-edge"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    return None


def find_sharp_runtime() -> tuple[str, str] | None:
    runtime_root = (
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
    )
    node_candidates = [
        runtime_root / "node" / "bin" / "node",
        Path(shutil.which("node") or ""),
    ]
    sharp_candidates = [
        runtime_root / "node" / "node_modules" / "sharp",
    ]
    for node in node_candidates:
        if not node.is_file():
            continue
        for sharp in sharp_candidates:
            if sharp.is_dir():
                return str(node), str(sharp)
    return None


def sharp_visual_boxes(
    svg_path: Path,
    target_ids: list[str],
    canvas: tuple[float, float, float, float],
    runtime: tuple[str, str],
) -> tuple[dict[str, tuple[float, float, float, float]], list[str], str]:
    node, sharp_module = runtime
    runner = r"""
const fs = require("fs");
const sharp = require(process.argv[2]);
const payload = JSON.parse(fs.readFileSync(process.argv[3], "utf8"));
const result = {boxes: {}, errors: []};
function cssEscape(value) {
  return value.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
}
(async () => {
  for (const id of payload.ids) {
    const selector = `[id="${cssEscape(id)}"]`;
    const style = `<style>svg *{visibility:hidden!important}`
      + `${selector},${selector} *{visibility:visible!important}</style>`;
    const isolated = payload.svg.replace(/<\/svg>\s*$/i, `${style}</svg>`);
    if (isolated === payload.svg) {
      result.errors.push(`sharp: cannot instrument SVG for ${id}`);
      continue;
    }
    try {
      const rendered = await sharp(Buffer.from(isolated), {density: 72})
        .resize(payload.width, payload.height, {fit: "fill"})
        .ensureAlpha()
        .raw()
        .toBuffer({resolveWithObject: true});
      const data = rendered.data;
      const info = rendered.info;
      let minX = info.width, minY = info.height, maxX = -1, maxY = -1;
      for (let y = 0; y < info.height; y++) {
        for (let x = 0; x < info.width; x++) {
          if (data[(y * info.width + x) * info.channels + 3] > 8) {
            minX = Math.min(minX, x); minY = Math.min(minY, y);
            maxX = Math.max(maxX, x); maxY = Math.max(maxY, y);
          }
        }
      }
      if (maxX < minX || maxY < minY) {
        result.errors.push(`sharp: ${id} rendered no visible pixels`);
        continue;
      }
      result.boxes[id] = [minX, minY, maxX - minX + 1, maxY - minY + 1];
    } catch (error) {
      result.errors.push(`sharp: ${id} render failed: ${error.message}`);
    }
  }
  process.stdout.write(JSON.stringify(result));
})().catch(error => {
  process.stdout.write(JSON.stringify({boxes: {}, errors: [String(error)]}));
  process.exit(1);
});
"""
    payload = {
        "svg": svg_path.read_text(encoding="utf-8"),
        "ids": target_ids,
        "width": max(1, round(canvas[2])),
        "height": max(1, round(canvas[3])),
    }
    with tempfile.TemporaryDirectory(prefix="research-figure-sharp-qa-") as temp:
        temp_root = Path(temp)
        runner_path = temp_root / "measure.js"
        input_path = temp_root / "input.json"
        runner_path.write_text(runner, encoding="utf-8")
        input_path.write_text(json.dumps(payload), encoding="utf-8")
        result = subprocess.run(
            [node, str(runner_path), sharp_module, str(input_path)],
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
    if not result.stdout.strip():
        detail = result.stderr.strip().splitlines()
        return {}, [
            "sharp render QA failed"
            + (f": {detail[-1]}" if detail else "")
        ], "sharp"
    try:
        decoded = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}, ["sharp render QA returned invalid data"], "sharp"
    vx, vy, vw, vh = canvas
    width = payload["width"]
    height = payload["height"]
    boxes = {
        element_id: (
            vx + values[0] * vw / width,
            vy + values[1] * vh / height,
            values[2] * vw / width,
            values[3] * vh / height,
        )
        for element_id, values in decoded.get("boxes", {}).items()
    }
    return boxes, [str(item) for item in decoded.get("errors", [])], "sharp"


def browser_layout_errors(svg_path: Path, browser: str) -> tuple[list[str], str]:
    svg_text = svg_path.read_text(encoding="utf-8")
    if re.search(r"<\s*script\b", svg_text, re.IGNORECASE):
        return ["browser QA refuses SVG containing executable script"], browser
    svg_text = re.sub(r"^\s*<\?xml[^>]*\?>", "", svg_text, count=1)
    svg_text = re.sub(r"<!DOCTYPE[^>]*>", "", svg_text, count=1, flags=re.IGNORECASE)
    base_url = svg_path.parent.resolve().as_uri() + "/"
    audit_script = r"""
const out = document.getElementById("qa-output");
const svg = document.querySelector("svg");
const errors = [];
function parseBox(value) {
  if (!value) return null;
  const p = value.trim().replaceAll(",", " ").split(/\s+/).map(Number);
  return p.length === 4 && p.every(Number.isFinite) && p[2] > 0 && p[3] > 0
    ? p : null;
}
function contains(outer, inner, tolerance = 1.5) {
  return inner[0] >= outer[0] - tolerance
    && inner[1] >= outer[1] - tolerance
    && inner[0] + inner[2] <= outer[0] + outer[2] + tolerance
    && inner[1] + inner[3] <= outer[1] + outer[3] + tolerance;
}
function closeEnough(a, b) {
  const tolerance = Math.max(2, 0.015 * Math.max(a[2], a[3], b[2], b[3]));
  return a.every((value, index) => Math.abs(value - b[index]) <= tolerance);
}
function label(element) {
  return element.id || element.textContent.trim().replace(/\s+/g, " ").slice(0, 60)
    || element.tagName;
}
function actualBox(element) {
  const rect = element.getBoundingClientRect();
  const rootRect = svg.getBoundingClientRect();
  const view = svg.viewBox.baseVal;
  const scaleX = view.width / rootRect.width;
  const scaleY = view.height / rootRect.height;
  return [
    view.x + (rect.left - rootRect.left) * scaleX,
    view.y + (rect.top - rootRect.top) * scaleY,
    rect.width * scaleX,
    rect.height * scaleY,
  ];
}
function role(element) {
  return (element.getAttribute("data-role") || "").trim().toLowerCase();
}
function owningPanel(element) {
  let node = element.parentElement;
  while (node && node !== svg) {
    if (["panel", "footer", "legend", "callout"].includes(role(node))) return node;
    node = node.parentElement;
  }
  return null;
}
function isMeaningful(element) {
  return element.tagName.toLowerCase() === "text"
    || element.getAttribute("data-critical") === "true"
    || ["title", "bracket", "brace", "merge", "fusion", "junction",
        "connector", "arrow", "arrowhead", "equation", "icon"]
       .includes(role(element));
}
function hasHiddenOverflow(element) {
  let node = element;
  while (node && node !== svg) {
    const style = getComputedStyle(node);
    if (style.overflow === "hidden" || style.clipPath !== "none"
        || style.maskImage !== "none") return true;
    node = node.parentElement;
  }
  return false;
}
async function audit() {
  if (!svg || !svg.viewBox || svg.viewBox.baseVal.width <= 0) {
    errors.push("browser: SVG or viewBox unavailable");
    out.textContent = JSON.stringify(errors);
    return;
  }
  const view = svg.viewBox.baseVal;
  svg.setAttribute("width", String(view.width));
  svg.setAttribute("height", String(view.height));
  svg.style.width = `${view.width}px`;
  svg.style.height = `${view.height}px`;
  await document.fonts.ready;
  const safe = parseBox(svg.getAttribute("data-safe-box"));
  if (!safe) errors.push("browser: valid root data-safe-box required");

  const panels = [...svg.querySelectorAll(
    '[data-role="panel"],[data-role="footer"],[data-role="legend"],[data-role="callout"]'
  )];
  for (const panel of panels) {
    const panelActual = actualBox(panel);
    const panelDeclared = parseBox(panel.getAttribute("data-bbox"));
    const content = parseBox(panel.getAttribute("data-content-box"));
    if (safe && !contains(safe, panelActual)) {
      errors.push(`browser: ${role(panel)} ${label(panel)} overflows canvas safe box`);
    }
    if (!panelDeclared || !closeEnough(panelActual, panelDeclared)) {
      errors.push(`browser: ${role(panel)} ${label(panel)} declared bbox differs from rendered bbox`);
    }
    if (!content) continue;
    for (const child of panel.querySelectorAll("text,[data-critical='true']")) {
      const measured = actualBox(child);
      if (!contains(content, measured)) {
        errors.push(`browser: ${label(child)} overflows ${role(panel)} ${label(panel)} content box`);
      }
      if (hasHiddenOverflow(child)) {
        errors.push(`browser: ${label(child)} uses clipping/masking to hide overflow`);
      }
    }
  }

  for (const element of svg.querySelectorAll("text,[data-critical='true'],[data-role]")) {
    if (!isMeaningful(element)) continue;
    const measured = actualBox(element);
    const declared = parseBox(element.getAttribute("data-bbox"));
    if (!declared || !closeEnough(measured, declared)) {
      errors.push(`browser: ${label(element)} declared bbox differs from rendered bbox`);
    }
    if (safe && !owningPanel(element) && !contains(safe, measured)) {
      errors.push(`browser: ${label(element)} overflows canvas safe box`);
    }
    if (hasHiddenOverflow(element)) {
      errors.push(`browser: ${label(element)} uses clipping/masking to hide overflow`);
    }
  }
  out.textContent = JSON.stringify([...new Set(errors)]);
}
audit();
"""
    document = (
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        f"<base href=\"{base_url}\"></head><body>{svg_text}"
        "<pre id=\"qa-output\"></pre><script>"
        f"{audit_script}</script></body></html>"
    )
    with tempfile.TemporaryDirectory(prefix="research-figure-dom-qa-") as temp:
        temp_root = Path(temp)
        html_path = temp_root / "audit.html"
        profile = temp_root / "chrome-profile"
        html_path.write_text(document, encoding="utf-8")
        result = subprocess.run(
            [
                browser,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--allow-file-access-from-files",
                "--virtual-time-budget=2500",
                f"--user-data-dir={profile}",
                "--dump-dom",
                html_path.as_uri(),
            ],
            text=True,
            capture_output=True,
            check=False,
            timeout=20,
        )
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()
        return [
            "browser DOM QA failed to run"
            + (f": {detail[-1]}" if detail else "")
        ], browser
    match = re.search(
        r'<pre id="qa-output">(.*?)</pre>',
        result.stdout,
        flags=re.DOTALL,
    )
    if not match:
        return ["browser DOM QA returned no audit result"], browser
    try:
        errors = json.loads(html.unescape(match.group(1)))
    except json.JSONDecodeError:
        return ["browser DOM QA returned invalid audit data"], browser
    return [str(item) for item in errors], browser


def inspect(
    svg_path: Path,
    png_path: Path | None,
    required: list[str],
    allow_hybrid: bool = False,
    metadata_only: bool = False,
) -> int:
    errors: list[str] = []
    notes: list[str] = []

    try:
        root = ET.parse(svg_path).getroot()
    except FileNotFoundError:
        print(f"FAIL: SVG not found: {svg_path}")
        return 1
    except ET.ParseError as exc:
        print(f"FAIL: invalid SVG/XML: {exc}")
        return 1

    if local_name(root.tag) != "svg":
        errors.append("root element is not <svg>")

    elements = list(root.iter())
    text_nodes = [
        element
        for element in elements
        if local_name(element.tag) == "text" and normalized_text(element)
    ]
    visible_text = " ".join(normalized_text(element) for element in text_nodes)
    if not text_nodes:
        errors.append("no live <text> nodes")

    ids = [element.get("id") for element in elements if element.get("id")]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append("duplicate editable IDs: " + ", ".join(duplicates))

    if any(
        local_name(element.tag)
        in {"filter", "feGaussianBlur", "feConvolveMatrix", "feDisplacementMap"}
        for element in elements
    ):
        errors.append("blur/filter effect found")
    if any(
        element.get("filter") not in {None, "", "none"}
        for element in elements
    ):
        errors.append("element uses a filter attribute")

    for exact in required:
        if " ".join(exact.split()) not in visible_text:
            errors.append(f"missing required live text: {exact!r}")

    parent = {
        child: container
        for container in root.iter()
        for child in list(container)
    }

    view_box = root.get("viewBox", "").replace(",", " ").split()
    canvas: tuple[float, float, float, float] | None = None
    if len(view_box) == 4:
        try:
            canvas = tuple(float(item) for item in view_box)  # type: ignore[assignment]
            if canvas[2] <= 0 or canvas[3] <= 0:
                errors.append("viewBox width and height must be positive")
                canvas = None
        except ValueError:
            errors.append("invalid viewBox")
    else:
        errors.append("missing four-number viewBox")

    safe_box = box4(root.get("data-safe-box"))
    bbox_audit = (root.get("data-bbox-audit") or "").strip()
    if safe_box is None:
        errors.append("root SVG lacks a valid data-safe-box")
    elif canvas is not None:
        if not contains(canvas, safe_box):
            errors.append("data-safe-box lies outside the SVG viewBox")
        else:
            vx, vy, vw, vh = canvas
            sx, sy, sw, sh = safe_box
            margins = (
                (sx - vx) / vw,
                ((vx + vw) - (sx + sw)) / vw,
                (sy - vy) / vh,
                ((vy + vh) - (sy + sh)) / vh,
            )
            if any(margin < 0.04 - 1e-6 or margin > 0.06 + 1e-6 for margin in margins):
                errors.append(
                    "data-safe-box must preserve 4–6% on every canvas edge"
                )
    if bbox_audit != "getBBox+getCTM+stroke":
        errors.append(
            "root SVG lacks data-bbox-audit='getBBox+getCTM+stroke'"
        )

    allowed_outside_roles = {"background", "texture"}
    drawable_tags = {
        "text",
        "image",
        "path",
        "rect",
        "circle",
        "ellipse",
        "line",
        "polyline",
        "polygon",
    }
    ignored_ancestors = {"defs", "clipPath", "mask", "marker", "pattern", "symbol"}

    def has_ignored_ancestor(element: ET.Element) -> bool:
        container = parent.get(element)
        while container is not None:
            if local_name(container.tag) in ignored_ancestors:
                return True
            container = parent.get(container)
        return False

    def bounded_ancestor(element: ET.Element) -> ET.Element | None:
        container = parent.get(element)
        while container is not None and container is not root:
            if box4(container.get("data-bbox")) is not None:
                return container
            container = parent.get(container)
        return None

    for element in elements:
        if element is root:
            continue
        role = (element.get("data-role") or "").strip().lower()
        element_box = box4(element.get("data-bbox"))
        outside_allowed = (
            role in allowed_outside_roles
            and (element.get("data-allow-outside-safe") or "").strip().lower()
            == "true"
        )
        if (
            element_box is not None
            and safe_box is not None
            and not outside_allowed
            and not contains(safe_box, element_box)
        ):
            errors.append(
                f"{role or local_name(element.tag)} "
                f"{element.get('id') or '<unnamed>'} overflows data-safe-box"
            )

        tag = local_name(element.tag)
        if tag == "text" and normalized_text(element) and element_box is None:
            errors.append(
                f"live text {element.get('id') or normalized_text(element)!r} "
                "lacks a valid visual data-bbox"
            )
        elif (
            tag in drawable_tags
            and not has_ignored_ancestor(element)
            and element_box is None
            and bounded_ancestor(element) is None
            and not outside_allowed
        ):
            errors.append(
                f"drawable {element.get('id') or '<unnamed>'} lacks a visual "
                "data-bbox or bounded ancestor"
            )

    panel_roles = {"panel", "footer", "legend", "callout"}
    for panel in elements:
        role = (panel.get("data-role") or "").strip().lower()
        if role not in panel_roles:
            continue
        panel_box = box4(panel.get("data-bbox"))
        content_box = box4(panel.get("data-content-box"))
        panel_id = panel.get("id") or "<unnamed>"
        if panel_box is None:
            errors.append(f"{role} {panel_id} lacks a valid data-bbox")
        if content_box is None:
            errors.append(f"{role} {panel_id} lacks a valid data-content-box")
        elif panel_box is not None and not contains(panel_box, content_box):
            errors.append(f"{role} {panel_id} content box exceeds its panel")
        if content_box is not None:
            for descendant in panel.iter():
                if (
                    descendant is not panel
                    and local_name(descendant.tag) == "text"
                    and normalized_text(descendant)
                ):
                    descendant_box = box4(descendant.get("data-bbox"))
                    if descendant_box is not None and not contains(
                        content_box, descendant_box
                    ):
                        errors.append(
                            f"text {descendant.get('id') or normalized_text(descendant)!r} "
                            f"overflows {role} {panel_id} content box"
                        )

    bridge_roles = {"bridge"}
    for bridge in elements:
        if (bridge.get("data-role") or "").strip().lower() not in bridge_roles:
            continue
        bridge_id = bridge.get("id") or "<unnamed>"
        missing = [
            attribute
            for attribute in (
                "data-bridge-from",
                "data-bridge-to",
                "data-corridor-box",
                "data-bbox",
            )
            if not (bridge.get(attribute) or "").strip()
        ]
        if missing:
            errors.append(
                f"bridge {bridge_id} lacks routing metadata: {', '.join(missing)}"
            )
        corridor_box = box4(bridge.get("data-corridor-box"))
        if corridor_box is None:
            errors.append(f"bridge {bridge_id} lacks a valid data-corridor-box")
            continue
        for descendant in bridge.iter():
            if (
                descendant is not bridge
                and (descendant.get("data-role") or "").strip().lower()
                == "connector-label"
            ):
                label_box = box4(descendant.get("data-bbox"))
                if label_box is not None and not contains(corridor_box, label_box):
                    errors.append(
                        f"connector label {descendant.get('id') or '<unnamed>'} "
                        f"overflows bridge {bridge_id} corridor"
                    )

    meaningful_roles = panel_roles | {
        "bridge",
        "connector-label",
        "title",
        "bracket",
        "brace",
        "merge",
        "fusion",
        "junction",
        "connector",
        "arrow",
        "arrowhead",
        "equation",
        "icon",
    }
    measured_targets: list[ET.Element] = []
    for element in elements:
        role = (element.get("data-role") or "").strip().lower()
        if (
            (local_name(element.tag) == "text" and normalized_text(element))
            or (element.get("data-critical") or "").strip().lower() == "true"
            or role in meaningful_roles
        ):
            if not element.get("id"):
                errors.append(
                    f"meaningful {role or local_name(element.tag)} "
                    f"{normalized_text(element) or '<unnamed>'!r} lacks an id "
                    "for independent render QA"
                )
            else:
                measured_targets.append(element)

    def owning_panel(element: ET.Element) -> ET.Element | None:
        container = parent.get(element)
        while container is not None and container is not root:
            if (container.get("data-role") or "").strip().lower() in panel_roles:
                return container
            container = parent.get(container)
        return None

    def owning_bridge(element: ET.Element) -> ET.Element | None:
        container = parent.get(element)
        while container is not None and container is not root:
            if (container.get("data-role") or "").strip().lower() == "bridge":
                return container
            container = parent.get(container)
        return None

    def uses_overflow_hiding(element: ET.Element) -> bool:
        node: ET.Element | None = element
        while node is not None and node is not root:
            style = (node.get("style") or "").replace(" ", "").lower()
            if (
                node.get("clip-path")
                or node.get("mask")
                or "overflow:hidden" in style
                or "clip-path:" in style
                or "mask:" in style
            ):
                return True
            node = parent.get(node)
        return False

    for element in measured_targets:
        if (
            (element.get("data-role") or "").strip().lower()
            == "connector-label"
            and owning_bridge(element) is None
        ):
            errors.append(
                f"connector label {element.get('id')} is not inside a "
                "declared bridge"
            )
        if uses_overflow_hiding(element):
            errors.append(
                f"{element.get('id')} uses clipping or masking to hide overflow"
            )

    image_nodes = [e for e in elements if local_name(e.tag) == "image"]
    if image_nodes:
        notes.append(f"{len(image_nodes)} raster layer(s); inspect sharpness manually")
    if canvas:
        for image in image_nodes:
            width = number(image.get("width"))
            height = number(image.get("height"))
            if (
                width is not None
                and height is not None
                and width >= 0.9 * canvas[2]
                and height >= 0.9 * canvas[3]
            ):
                if allow_hybrid:
                    notes.append(
                        "near-full-canvas raster explicitly allowed for disclosed hybrid"
                    )
                else:
                    errors.append(
                        "near-full-canvas raster image suggests flattened output"
                    )
                break

    vector_count = sum(
        local_name(element.tag)
        in {"path", "rect", "circle", "ellipse", "line", "polyline", "polygon"}
        for element in elements
    )
    if vector_count < 3:
        errors.append("too little editable vector geometry")

    grouping_roles = {"bracket", "brace"}
    junction_roles = {"merge", "fusion", "junction"}
    for element in elements:
        role = (element.get("data-role") or "").strip().lower()
        if role in grouping_roles:
            missing = [
                attr
                for attr in (
                    "data-target-group",
                    "data-target-bbox",
                    "data-side",
                    "data-span",
                    "data-clearance",
                )
                if not (element.get(attr) or "").strip()
            ]
            if missing:
                errors.append(
                    f"{role} {element.get('id') or '<unnamed>'} lacks structural "
                    f"anchor metadata: {', '.join(missing)}"
                )
        if role in junction_roles:
            missing = [
                attr
                for attr in ("data-incoming", "data-outgoing", "data-junction")
                if not (element.get(attr) or "").strip()
            ]
            if missing:
                errors.append(
                    f"{role} {element.get('id') or '<unnamed>'} lacks structural "
                    f"anchor metadata: {', '.join(missing)}"
                )

    title_nodes = [
        element
        for element in elements
        if (element.get("data-role") or "").strip().lower() == "title"
    ]
    ignored_top_level = {"defs", "metadata", "title", "desc", "style"}
    drawable_top_level = [
        element
        for element in list(root)
        if local_name(element.tag) not in ignored_top_level
    ]

    for title in title_nodes:
        title_id = (title.get("id") or "").strip()
        title_box = box4(title.get("data-bbox"))
        if not title_id:
            errors.append("title lacks an editable id")
        if title_box is None:
            errors.append(
                f"title {title_id or '<unnamed>'} lacks a valid data-bbox"
            )

        layer = parent.get(title)
        while layer is not None and (
            (layer.get("data-role") or "").strip().lower() != "title-layer"
        ):
            layer = parent.get(layer)
        if layer is None:
            errors.append(
                f"title {title_id or '<unnamed>'} is not inside a title-layer"
            )
            continue

        clear_zone = box4(layer.get("data-clear-zone"))
        if clear_zone is None:
            errors.append(
                f"title-layer for {title_id or '<unnamed>'} lacks a valid "
                "data-clear-zone"
            )
        elif title_box is not None:
            tx, ty, tw, th = title_box
            cx, cy, cw, ch = clear_zone
            left = tx - cx
            right = (cx + cw) - (tx + tw)
            top = ty - cy
            bottom = (cy + ch) - (ty + th)
            if (
                left < 0.35 * th
                or right < 0.35 * th
                or top < 0.5 * th
                or bottom < 0.5 * th
            ):
                errors.append(
                    f"title-layer for {title_id or '<unnamed>'} has "
                    "insufficient clear-zone padding"
                )

        masks = [
            element
            for element in layer.iter()
            if (element.get("data-role") or "").strip().lower() == "title-mask"
            and (element.get("data-target") or "").strip() == title_id
        ]
        if not masks:
            errors.append(
                f"title {title_id or '<unnamed>'} lacks a matching title-mask"
            )
        elif clear_zone is not None:
            mask = masks[0]
            mask_box = box4(mask.get("data-bbox"))
            if mask_box is None:
                errors.append(
                    f"title-mask for {title_id or '<unnamed>'} lacks a valid "
                    "data-bbox"
                )
            else:
                mx, my, mw, mh = mask_box
                cx, cy, cw, ch = clear_zone
                if (
                    mx > cx
                    or my > cy
                    or mx + mw < cx + cw
                    or my + mh < cy + ch
                ):
                    errors.append(
                        f"title-mask for {title_id or '<unnamed>'} does not "
                        "cover the complete clear zone"
                    )
            if (mask.get("fill") or "").strip().lower() in {"", "none", "transparent"}:
                errors.append(
                    f"title-mask for {title_id or '<unnamed>'} is not opaque"
                )
            if number(mask.get("fill-opacity")) == 0:
                errors.append(
                    f"title-mask for {title_id or '<unnamed>'} is not opaque"
                )

        if drawable_top_level and drawable_top_level[-1] is not layer:
            errors.append(
                f"title-layer for {title_id or '<unnamed>'} is not the last "
                "root-level drawable object"
            )

    if png_path is not None:
        dims = png_dimensions(png_path)
        if dims is None:
            errors.append(f"missing or invalid PNG preview: {png_path}")
        else:
            notes.append(f"PNG {dims[0]}×{dims[1]}")
            if dims[0] < 1000 or dims[1] < 600:
                errors.append("PNG preview is below the default review size")
            if canvas is not None:
                svg_ratio = canvas[2] / canvas[3]
                png_ratio = dims[0] / dims[1]
                if abs(svg_ratio - png_ratio) / svg_ratio > 0.01:
                    errors.append(
                        "PNG aspect ratio differs from SVG viewBox; possible "
                        "crop or stretch"
                    )

    if metadata_only:
        notes.append("independent render measurement skipped explicitly")
    else:
        sharp_runtime = find_sharp_runtime()
        if sharp_runtime is not None and canvas is not None:
            measured_boxes, render_errors, renderer = sharp_visual_boxes(
                svg_path,
                [element.get("id") or "" for element in measured_targets],
                canvas,
                sharp_runtime,
            )
            errors.extend(render_errors)
            for element in measured_targets:
                element_id = element.get("id") or ""
                measured = measured_boxes.get(element_id)
                if measured is None:
                    continue
                declared = box4(element.get("data-bbox"))
                if declared is None or not contains(
                    declared,
                    measured,
                    tolerance=2.0,
                ):
                    errors.append(
                        f"{renderer}: {element_id} declared bbox does not "
                        "contain independently rendered pixels"
                    )
                panel = owning_panel(element)
                if panel is not None:
                    content_box = box4(panel.get("data-content-box"))
                    if content_box is not None and not contains(
                        content_box, measured, tolerance=1.5
                    ):
                        errors.append(
                            f"{renderer}: {element_id} overflows "
                            f"{(panel.get('data-role') or '').strip().lower()} "
                            f"{panel.get('id') or '<unnamed>'} content box"
                        )
                else:
                    bridge = owning_bridge(element)
                    if bridge is not None:
                        corridor_box = box4(bridge.get("data-corridor-box"))
                        if corridor_box is not None and not contains(
                            corridor_box, measured, tolerance=1.5
                        ):
                            errors.append(
                                f"{renderer}: {element_id} overflows bridge "
                                f"{bridge.get('id') or '<unnamed>'} corridor"
                            )
                    elif (
                        (element.get("data-role") or "").strip().lower()
                        == "connector-label"
                    ):
                        errors.append(
                            f"{renderer}: connector label {element_id} is not "
                            "inside a declared bridge"
                        )
                if (
                    panel is None
                    and owning_bridge(element) is None
                    and safe_box is not None
                    and not contains(
                        safe_box,
                        measured,
                        tolerance=1.5,
                    )
                ):
                    errors.append(
                        f"{renderer}: {element_id} overflows canvas safe box"
                    )
            notes.append(f"independent pixel QA: {renderer}")
        else:
            browser = find_chromium()
            if browser is None:
                errors.append(
                    "no independent SVG renderer available; use "
                    "--metadata-only only in isolated automated tests"
                )
            else:
                browser_errors, browser_name = browser_layout_errors(
                    svg_path, browser
                )
                errors.extend(browser_errors)
                notes.append(f"browser DOM QA: {Path(browser_name).name}")

    if errors:
        print(f"FAIL: {len(errors)} critical structural issue(s)")
        for item in errors:
            print(f"- {item}")
        for item in notes:
            print(f"NOTE: {item}")
        return 1

    suffix = f"; {'; '.join(notes)}" if notes else ""
    print(
        f"PASS: live text={len(text_nodes)}, vector objects={vector_count}, "
        f"duplicate IDs=0, blur filters=0{suffix}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run fast structural QA on an editable SVG and PNG preview."
    )
    parser.add_argument("svg", type=Path)
    parser.add_argument("png", nargs="?", type=Path)
    parser.add_argument(
        "--required-text",
        action="append",
        default=[],
        help="Exact visible text required in the SVG; may be repeated.",
    )
    parser.add_argument(
        "--allow-hybrid",
        action="store_true",
        help=(
            "Allow a disclosed near-full-canvas raster illustration layer when "
            "the SVG also contains useful live text and vector objects."
        ),
    )
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help=(
            "Skip independent render measurement. Intended only for "
            "isolated automated tests, not final figure approval."
        ),
    )
    args = parser.parse_args()
    return inspect(
        args.svg,
        args.png,
        args.required_text,
        args.allow_hybrid,
        args.metadata_only,
    )


if __name__ == "__main__":
    sys.exit(main())
