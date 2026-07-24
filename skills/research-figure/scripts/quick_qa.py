#!/usr/bin/env python3
"""Fast structural QA for the simplified research-figure workflow."""

from __future__ import annotations

import argparse
import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def number(value: str | None) -> float | None:
    if value is None:
        return None
    match = re.match(r"^\s*(-?(?:\d+(?:\.\d*)?|\.\d+))", value)
    return float(match.group(1)) if match else None


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


def inspect(svg_path: Path, png_path: Path | None, required: list[str]) -> int:
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

    view_box = root.get("viewBox", "").replace(",", " ").split()
    canvas: tuple[float, float] | None = None
    if len(view_box) == 4:
        try:
            canvas = (float(view_box[2]), float(view_box[3]))
        except ValueError:
            errors.append("invalid viewBox")
    else:
        errors.append("missing four-number viewBox")

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
                and width >= 0.9 * canvas[0]
                and height >= 0.9 * canvas[1]
            ):
                errors.append("near-full-canvas raster image suggests flattened output")
                break

    vector_count = sum(
        local_name(element.tag)
        in {"path", "rect", "circle", "ellipse", "line", "polyline", "polygon"}
        for element in elements
    )
    if vector_count < 3:
        errors.append("too little editable vector geometry")

    if png_path is not None:
        dims = png_dimensions(png_path)
        if dims is None:
            errors.append(f"missing or invalid PNG preview: {png_path}")
        else:
            notes.append(f"PNG {dims[0]}×{dims[1]}")
            if dims[0] < 1000 or dims[1] < 600:
                errors.append("PNG preview is below the default review size")

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
    args = parser.parse_args()
    return inspect(args.svg, args.png, args.required_text)


if __name__ == "__main__":
    sys.exit(main())
