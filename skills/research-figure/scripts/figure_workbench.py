#!/usr/bin/env python3
"""Deterministic FigureSpec scaffolding, validation, prompt compilation, and QA.

This module intentionally has no third-party dependencies. The bundled JSON
Schema supports editor integration; this script adds scientific semantic checks
that generic schema validators cannot express.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_ROOT / "assets"
TEMPLATE_PATH = ASSETS_DIR / "figure-spec.template.json"
SCHEMA_PATH = ASSETS_DIR / "figure-spec.schema.json"
ARTIFACT_SCHEMAS = {
    "evidence-ledger": ASSETS_DIR / "evidence-ledger.schema.json",
    "figure-audit": ASSETS_DIR / "figure-audit.schema.json",
}

ROLES = {
    "motivation",
    "method",
    "mechanism",
    "experiment",
    "ablation",
    "comparison",
    "taxonomy",
    "graphical-abstract",
    "mixed",
}
CLAIM_STATUSES = {"supported", "inferred", "hypothesis", "missing"}
CLAIM_SCOPES = {
    "descriptive",
    "associational",
    "causal",
    "procedural",
    "normative",
}
RELATION_TYPES = {
    "data-flow",
    "control-flow",
    "causal",
    "causal-hypothesis",
    "temporal",
    "association",
    "comparison",
    "feedback",
    "inhibition",
    "containment",
    "correspondence",
}
RENDER_MODES = {"vector-code", "plot-code", "image-generation", "hybrid"}
QUANTITATIVE_ROLES = {"experiment", "ablation"}

ROLE_DEFAULTS = {
    "motivation": {
        "question": "Why is a new solution needed?",
        "message": "A source-grounded failure exposes a bounded research gap.",
        "boundary": "Do not imply universal failure or reveal the full method.",
        "adapter": (
            "Make the gap visually dominant. Encode status quo, observed "
            "failure, and bounded research need as distinct regions. Do not "
            "turn independent problems into method stages or reveal the full "
            "proposed architecture."
        ),
    },
    "method": {
        "question": "How does the proposed system transform input into output?",
        "message": "Typed operations and interfaces define the method's main flow.",
        "boundary": "Do not imply empirical superiority or guaranteed correctness.",
        "adapter": (
            "Treat the diagram as a typed transformation, not a box inventory. "
            "For every arrow preserve source, target, direction, semantic type, "
            "and payload label. Make the novel operation dominant."
        ),
    },
    "mechanism": {
        "question": "Why should the intervention change the outcome?",
        "message": "A supported intermediate transformation links intervention to outcome.",
        "boundary": "Do not promote association or hypothesis to proven causality.",
        "adapter": (
            "Expose the intermediate transformation connecting intervention to "
            "outcome. Use causal encoding only for supported causal claims and "
            "explicit hypothesis encoding otherwise."
        ),
    },
    "experiment": {
        "question": "Does the evidence support the main empirical claim?",
        "message": "The primary comparison, uncertainty, and boundary determine support.",
        "boundary": "Do not invent values, significance, or causal explanations.",
        "adapter": (
            "Render values and geometry deterministically from supplied data. "
            "Make the primary comparison obvious, show uncertainty and scope, "
            "and retain negative or tied evidence."
        ),
    },
    "ablation": {
        "question": "Which controlled component or choice contributes?",
        "message": "A controlled change produces a bounded observed delta.",
        "boundary": "Do not imply independent additive or universal importance.",
        "adapter": (
            "Center the controlled contrast. Label the changed factor precisely, "
            "show the full system as reference, and limit interpretation to the "
            "tested setting."
        ),
    },
    "comparison": {
        "question": "How do alternatives differ on shared dimensions?",
        "message": "Consistent criteria reveal meaningful trade-offs.",
        "boundary": "Do not convert unknown or unreported evidence into absence.",
        "adapter": (
            "Apply identical criteria and scale to every alternative. Encode "
            "unknown separately from absent and show trade-offs rather than a "
            "decorative winner."
        ),
    },
    "taxonomy": {
        "question": "How is the space organized?",
        "message": "Explicit dimensions define groups, boundaries, and exceptions.",
        "boundary": "Do not imply exclusivity or completeness without support.",
        "adapter": (
            "State the classification dimensions and whether membership is "
            "exclusive. Preserve overlap and exceptions; do not imply complete "
            "coverage unless established."
        ),
    },
    "graphical-abstract": {
        "question": "What compact end-to-end story should a broad reader remember?",
        "message": "Context, intervention, principal result, and bounded implication form one story.",
        "boundary": "Do not add secondary results or an unverified mechanism.",
        "adapter": (
            "Compress the paper into context, intervention, principal result, "
            "and bounded implication. Use one dominant path and preserve "
            "scientific qualifiers."
        ),
    },
    "mixed": {
        "question": "How do distinct panels support one figure-level message?",
        "message": "Panels with unique roles form one traceable evidence chain.",
        "boundary": "Do not use mixed as a label for an overloaded figure.",
        "adapter": (
            "Give every panel a distinct local role and unique evidence while "
            "preserving one figure-level message. Route conceptual and "
            "quantitative panels independently."
        ),
    },
}

RENDERER_ADAPTERS = {
    "vector-code": (
        "Generate editable vector geometry or native diagram objects. Keep final "
        "labels as live text nodes, not outlined glyphs or a raster layer. "
        "Preserve stable IDs, endpoints, arrowheads, grouping, and alignment "
        "deterministically. Return editable source plus SVG/PDF and a crisp "
        "raster preview."
    ),
    "plot-code": (
        "Generate geometry from the supplied machine-readable data. Preserve "
        "values, units, signs, category order, uncertainty, and missing values. "
        "Do not infer significance. Keep labels as live text where the export "
        "format permits it. Return plotting source, editable SVG/PDF, and a "
        "crisp preview."
    ),
    "image-generation": (
        "Generate only the inventoried, preferably text-free conceptual base "
        "illustration. Do not render exact values, axes, tables, equations, "
        "citations, or final labels. Reserve negative space for a deterministic "
        "live-text and vector-arrow overlay. Reject blurred, fuzzy, melted, "
        "ghosted, or visibly upscaled local regions before compositing."
    ),
    "hybrid": (
        "Render plots, equations, labels, arrows, and core geometry "
        "deterministically. Use image generation only for named illustration "
        "assets, preferably without text. Assemble layers in an editable "
        "composition, preserve a source manifest, and reject any generated asset "
        "with pseudo-text, soft edges, local melting, ghosting, or visible "
        "upscaling."
    ),
}

PROMPT_SECTION_HEADINGS = (
    "# 1. JOB, TARGET, AND CANVAS",
    "# 2. REFERENCE-FIGURE CONTRACT",
    "# 3. SCIENTIFIC TOPIC AND PURPOSE",
    "# 4. SCIENTIFIC NARRATIVE",
    "# 5. CONTENT AND EXACT-TEXT INVENTORY",
    "# 6. RELATION AND ARROW CONTRACT",
    "# 7. GLOBAL LAYOUT AND REGION GEOMETRY",
    "# 8. PER-PANEL COMPOSITION",
    "# 9. VISUAL LANGUAGE",
    "# 10. EDITABLE CONSTRUCTION CONTRACT",
    "# 11. NEGATIVE PROMPT",
    "# 12. OUTPUT CONTRACT",
    "# 13. PREFLIGHT BEFORE DELIVERY",
)

OPTICAL_NEGATIVE_RULES = (
    "wrong, pseudo-, warped, duplicated, or misspelled text",
    "font substitution, missing glyphs, or corrupted symbols",
    "rasterized final labels or unreadable microtext",
    "blurred, fuzzy, melted, ghosted, or partially erased shapes",
    "soft edges caused by low-resolution upscaling",
    "overlapping, clipped, truncated, duplicated, or off-canvas labels",
)

SUMMARY_REQUIRED_HEADINGS = (
    "# Paper summary",
    "## 0. Source contract",
    "## 1. Executive summary",
    "## 2. Problem and research gap",
    "## 3. Key observations and thesis",
    "## 4. Contributions",
    "## 5. Method",
    "## 6. Experimental design",
    "## 7. Results and negative evidence",
    "## 8. Limitations, ethics, and scope",
    "## 9. Terminology and exact-text register",
    "## 10. Section coverage",
    "## 11. Figure portfolio signals",
    "## 12. Unresolved questions",
)

SUMMARY_SECTION_SENTINELS = {
    "## 0. Source contract": (
        "Title:",
        "Source files:",
        "Allowed scope:",
        "Explicit exclusions:",
    ),
    "## 2. Problem and research gap": (
        "Why the problem is difficult",
        "Evidence anchor:",
        "Existing approaches and limitations",
    ),
    "## 3. Key observations and thesis": (
        "Bounded paper thesis:",
        "Stronger interpretation not supported:",
    ),
    "## 5. Method": (
        "Input–process–output",
        "Intermediate states:",
        "Explicitly absent paths:",
    ),
    "## 6. Experimental design": (
        "Datasets/corpora:",
        "Baselines:",
        "Metrics and what each metric measures:",
        "Statistical tests:",
    ),
    "## 7. Results and negative evidence": (
        "Main result:",
        "Negative, tied, or contradictory result:",
        "Unreported evidence that must not be invented:",
    ),
    "## 8. Limitations, ethics, and scope": (
        "Generalization limitation:",
        "Legal/clinical/safety boundary:",
    ),
    "## 9. Terminology and exact-text register": (
        "Term/symbol",
        "Exact spelling",
        "Must remain exact in figure?",
    ),
    "## 10. Section coverage": (
        "Section or source region",
        "Inspected?",
        "Exclusion reason if not used",
    ),
    "## 11. Figure portfolio signals": (
        "Candidate figure",
        "Reader question",
        "Unique evidence",
    ),
    "## 12. Unresolved questions": (
        "Missing evidence:",
        "Conflicting sources:",
        "Assumptions requiring author confirmation:",
    ),
}

UNSAFE_REFERENCE_PATTERNS = (
    r"\bcopy\b",
    r"\bclone\b",
    r"\bexact(?:ly)?\b",
    r"\bidentical\b",
    r"\bimitat(?:e|ion|ing)\b",
    r"\breplicat(?:e|ion|ing)\b",
    r"\breproduc(?:e|tion|ing)\b",
    r"\brecreat(?:e|ion|ing)\b",
    r"\bmirror(?:ed|ing)?\b",
    r"\bone[- ]to[- ]one\b",
    r"\b1\s*[:：]\s*1\b",
    r"\btrac(?:e|ing)\b",
    r"\bpixel[- ]for[- ]pixel\b",
    r"\b(?:all|every) (?:word|label|object|detail|element)\b",
    r"\bsame (?:artist|design system|composition|layout|style)\b",
    r"\bas if (?:made|drawn|designed) by\b",
    r"(?:完全|精确|原样|逐像素)(?:复制|复刻|模仿)",
    r"(?:照搬|临摹|复刻|像素级复刻|逐字复制)",
    r"(?:一模一样|原封不动|完全相同|一比一|照着.+?(?:做|画|重建))",
    r"(?:保持|做成|画成).+?(?:一样|相同|同样)",
)

UNSAFE_REFERENCE_CONTENT_PATTERNS = (
    r"\bscientific content\b",
    r"\b(?:exact |source )?(?:text|labels?|values?|equations?)\b",
    r"\b(?:logos?|branding)\b",
    r"\b(?:wording|artwork)\b",
    r"\b(?:unique|distinctive|signature) (?:icons?|motifs?|objects?|expression)\b",
    r"(?:原图|参考图)的?(?:文字|标签|数值|公式|标志|品牌|独特图标|独特表达)",
)

REFERENCE_ABSTRACT_ATTRIBUTE_PATTERNS = (
    r"\baspect ratio\b",
    r"\b(?:region|panel) (?:proportion|ratio|arrangement|geometry|layout)\b",
    r"\b(?:layout|reading) (?:topology|rhythm|order|direction|pattern)\b",
    r"\b(?:alignment|whitespace|density|spacing|margin)\b",
    r"\b(?:borders?|corner|line|stroke) (?:treatment|style|rhythm|weight|pattern)\b",
    r"\b(?:dashed|rounded|solid|soft).*?\bborders?\b",
    r"\b(?:palette|color) (?:relationship|contrast|hierarchy|temperature|semantics)\b",
    r"\bicon (?:scale|density|spacing|treatment)\b",
    r"\barrow (?:rhythm|scale|density|treatment|style)\b",
    r"\btypograph(?:y|ic) (?:hierarchy|scale|rhythm|treatment)\b",
    r"\bvisual (?:hierarchy|density|rhythm|language)\b",
    r"\b(?:hand[- ]drawn|flat|monochrome|muted) (?:treatment|visual language|texture)\b",
    r"\bbackground (?:tone|treatment|texture)\b",
    r"\b(?:one|two|three|\d+) .*?\bregion(?:s)?\b",
    r"\bfunctional composition (?:class|pattern)\b",
    r"(?:纵横比|宽高比|区域比例|面板比例|布局拓扑|阅读顺序)",
    r"(?:对齐|留白|密度|间距|边距|边框处理|线条处理)",
    r"(?:配色关系|色彩层级|图标尺度|箭头节奏|字体层级|排版层级|视觉层级)",
    r"(?:手绘质感|背景色调|背景纹理)",
)


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "level": self.level,
            "code": self.code,
            "path": self.path,
            "message": self.message,
        }


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def write_text(path: Path, text: str, force: bool = False) -> None:
    if path.exists() and not force:
        raise ValueError(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def string_ok(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def add(
    findings: list[Finding],
    level: str,
    code: str,
    path: str,
    message: str,
) -> None:
    findings.append(Finding(level, code, path, message))


def duplicate_values(items: Iterable[Any]) -> set[Any]:
    seen: set[Any] = set()
    duplicates: set[Any] = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return duplicates


def _json_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def _resolve_schema_ref(root_schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"Unsupported schema reference: {ref}")
    node: Any = root_schema
    for token in ref[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        node = node[token]
    if not isinstance(node, dict):
        raise ValueError(f"Schema reference does not resolve to an object: {ref}")
    return node


def validate_schema_shape(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any] | None = None,
    path: str = "$",
) -> list[Finding]:
    """Validate the JSON-Schema subset used by FigureSpec without dependencies."""

    root = root_schema or schema
    if "$ref" in schema:
        findings = validate_schema_shape(
            value, _resolve_schema_ref(root, schema["$ref"]), root, path
        )
        sibling_schema = {
            key: item for key, item in schema.items() if key != "$ref"
        }
        if sibling_schema:
            findings.extend(
                validate_schema_shape(value, sibling_schema, root, path)
            )
        return findings

    findings: list[Finding] = []
    expected_type = schema.get("type")
    type_matches = True
    if isinstance(expected_type, str):
        type_matches = _json_type_matches(value, expected_type)
    elif isinstance(expected_type, list):
        type_matches = any(
            isinstance(item, str) and _json_type_matches(value, item)
            for item in expected_type
        )
    if expected_type is not None and not type_matches:
        add(
            findings,
            "error",
            "schema.type",
            path,
            f"Expected {expected_type}, got {type(value).__name__}.",
        )
        return findings

    if "const" in schema and value != schema["const"]:
        add(
            findings,
            "error",
            "schema.const",
            path,
            f"Expected constant value {schema['const']!r}.",
        )
    if "enum" in schema and value not in schema["enum"]:
        add(
            findings,
            "error",
            "schema.enum",
            path,
            f"Value {value!r} is not one of {schema['enum']!r}.",
        )

    if isinstance(value, str):
        minimum = schema.get("minLength")
        if isinstance(minimum, int) and len(value) < minimum:
            add(
                findings,
                "error",
                "schema.minLength",
                path,
                f"String must contain at least {minimum} character(s).",
            )
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.search(pattern, value) is None:
            add(
                findings,
                "error",
                "schema.pattern",
                path,
                f"String does not match pattern {pattern!r}.",
            )

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        exclusive_minimum = schema.get("exclusiveMinimum")
        exclusive_maximum = schema.get("exclusiveMaximum")
        if minimum is not None and value < minimum:
            add(
                findings,
                "error",
                "schema.minimum",
                path,
                f"Value must be >= {minimum}.",
            )
        if maximum is not None and value > maximum:
            add(
                findings,
                "error",
                "schema.maximum",
                path,
                f"Value must be <= {maximum}.",
            )
        if exclusive_minimum is not None and value <= exclusive_minimum:
            add(
                findings,
                "error",
                "schema.exclusiveMinimum",
                path,
                f"Value must be > {exclusive_minimum}.",
            )
        if exclusive_maximum is not None and value >= exclusive_maximum:
            add(
                findings,
                "error",
                "schema.exclusiveMaximum",
                path,
                f"Value must be < {exclusive_maximum}.",
            )

    if isinstance(value, list):
        minimum_items = schema.get("minItems")
        maximum_items = schema.get("maxItems")
        if isinstance(minimum_items, int) and len(value) < minimum_items:
            add(
                findings,
                "error",
                "schema.minItems",
                path,
                f"Array must contain at least {minimum_items} item(s).",
            )
        if isinstance(maximum_items, int) and len(value) > maximum_items:
            add(
                findings,
                "error",
                "schema.maxItems",
                path,
                f"Array must contain at most {maximum_items} item(s).",
            )
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True) for item in value]
            if len(serialized) != len(set(serialized)):
                add(
                    findings,
                    "error",
                    "schema.uniqueItems",
                    path,
                    "Array items must be unique.",
                )
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                findings.extend(
                    validate_schema_shape(
                        item, item_schema, root, f"{path}[{index}]"
                    )
                )

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                add(
                    findings,
                    "error",
                    "schema.required",
                    path,
                    f"Missing required property {key!r}.",
                )
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, item in value.items():
            child_path = f"{path}.{key}"
            if key in properties:
                findings.extend(
                    validate_schema_shape(item, properties[key], root, child_path)
                )
            elif additional is False:
                add(
                    findings,
                    "error",
                    "schema.additionalProperties",
                    child_path,
                    f"Unexpected property {key!r}.",
                )
            elif isinstance(additional, dict):
                findings.extend(
                    validate_schema_shape(item, additional, root, child_path)
                )
    return findings


def validate_evidence_ledger(ledger: Any) -> list[Finding]:
    schema = load_json(ARTIFACT_SCHEMAS["evidence-ledger"])
    findings = validate_schema_shape(ledger, schema)
    if findings or not isinstance(ledger, dict):
        return findings
    claim_ids = [claim["id"] for claim in ledger["claims"]]
    for duplicate in sorted(duplicate_values(claim_ids)):
        add(
            findings,
            "error",
            "evidence.claim-id.duplicate",
            "$.claims",
            f"Duplicate claim ID: {duplicate}",
        )
    for index, claim in enumerate(ledger["claims"]):
        path = f"$.claims[{index}]"
        if claim["status"] == "supported":
            if not string_ok(claim["source_anchor"]):
                add(
                    findings,
                    "error",
                    "evidence.anchor.missing",
                    f"{path}.source_anchor",
                    "A supported claim requires a source anchor.",
                )
            if not string_ok(claim["evidence"]):
                add(
                    findings,
                    "error",
                    "evidence.support.missing",
                    f"{path}.evidence",
                    "A supported claim requires an evidence statement.",
                )
        if claim["status"] == "missing" and string_ok(claim["evidence"]):
            add(
                findings,
                "warning",
                "evidence.missing-has-support",
                f"{path}.evidence",
                "A missing claim should not contain purported supporting evidence.",
            )
    return findings


def summary_sha256(summary_text: str) -> str:
    return hashlib.sha256(summary_text.encode("utf-8")).hexdigest()


def artifact_signature_error(path: Path, artifact_format: str) -> str | None:
    """Return a concrete signature/container error for supported deliverables."""

    normalized = artifact_format.strip().lower().lstrip(".")
    try:
        data = path.read_bytes()
    except OSError as exc:
        return f"Could not read artifact bytes: {exc}"
    if normalized == "svg":
        try:
            root = ET.fromstring(data)
        except ET.ParseError as exc:
            return f"Invalid SVG/XML: {exc}"
        if root.tag.rsplit("}", 1)[-1] != "svg":
            return "SVG artifact does not have an <svg> root."
    elif normalized == "pdf":
        if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-4096:]:
            return "PDF signature or end-of-file marker is missing."
        if re.search(rb"(?m)^\d+\s+\d+\s+obj\b", data) is None:
            return "PDF contains no indirect object graph."
        startxref_matches = list(
            re.finditer(rb"startxref\s+(\d+)\s*(?:%%EOF)?", data)
        )
        if not startxref_matches:
            return "PDF startxref pointer is missing."
        xref_offset = int(startxref_matches[-1].group(1))
        if xref_offset < 0 or xref_offset >= len(data):
            return "PDF startxref pointer is outside the file."
        xref_head = data[xref_offset : xref_offset + 512].lstrip()
        classic_xref = xref_head.startswith(b"xref")
        xref_stream = (
            re.match(rb"\d+\s+\d+\s+obj\b", xref_head) is not None
            and b"/Type" in xref_head
            and b"/XRef" in xref_head
        )
        if not classic_xref and not xref_stream:
            return "PDF startxref does not point to an xref table or xref stream."
        if b"/Root" not in data:
            return "PDF trailer/xref stream has no document Root reference."
    elif normalized == "png":
        if (
            not data.startswith(b"\x89PNG\r\n\x1a\n")
            or len(data) < 24
            or struct.unpack(">II", data[16:24])[0] <= 0
            or struct.unpack(">II", data[16:24])[1] <= 0
        ):
            return "PNG signature or positive IHDR dimensions are missing."
    elif normalized in {"jpg", "jpeg"}:
        if not data.startswith(b"\xff\xd8") or not data.rstrip().endswith(
            b"\xff\xd9"
        ):
            return "JPEG start/end markers are missing."
    elif normalized == "webp":
        if (
            len(data) < 12
            or data[:4] != b"RIFF"
            or data[8:12] != b"WEBP"
        ):
            return "WebP RIFF signature is missing."
    elif normalized == "pptx":
        try:
            with zipfile.ZipFile(path) as archive:
                names = set(archive.namelist())
        except (OSError, zipfile.BadZipFile) as exc:
            return f"PPTX is not a readable OOXML ZIP container: {exc}"
        required = {"[Content_Types].xml", "ppt/presentation.xml"}
        if not required.issubset(names):
            return "PPTX container is missing required OOXML presentation parts."
    elif normalized == "drawio":
        try:
            root = ET.fromstring(data)
        except ET.ParseError as exc:
            return f"Invalid draw.io XML: {exc}"
        if root.tag.rsplit("}", 1)[-1] not in {"mxfile", "mxGraphModel"}:
            return "draw.io artifact must have an <mxfile> or <mxGraphModel> root."
    return None


def validate_paper_summary(
    summary_text: str, spec: dict[str, Any] | None = None
) -> list[Finding]:
    """Validate that prompt compilation is preceded by a filled summary artifact."""

    findings: list[Finding] = []
    if not string_ok(summary_text):
        return [
            Finding(
                "error",
                "summary.empty",
                "$",
                "A non-empty detailed paper summary is required before compilation.",
            )
        ]
    prior_index = -1
    section_matches: list[tuple[str, re.Match[str]]] = []
    for heading in SUMMARY_REQUIRED_HEADINGS:
        matches = list(
            re.finditer(rf"(?m)^{re.escape(heading)}[ \t]*$", summary_text)
        )
        if not matches:
            add(
                findings,
                "error",
                "summary.section.missing",
                "$",
                f"Missing required summary section: {heading}",
            )
            continue
        if len(matches) > 1:
            add(
                findings,
                "error",
                "summary.section.duplicate",
                "$",
                f"Summary section appears {len(matches)} times: {heading}",
            )
        match = matches[0]
        if match.start() <= prior_index:
            add(
                findings,
                "error",
                "summary.section.order",
                "$",
                f"Summary section is out of order: {heading}",
            )
        else:
            prior_index = match.start()
            section_matches.append((heading, match))

    summary_tokens = re.findall(
        r"[A-Za-z0-9_±Δ]+|[\u3400-\u9fff]", summary_text
    )
    token_count = len(summary_tokens)
    minimum_tokens = (
        600
        if spec is not None and spec.get("source", {}).get("type") == "paper"
        else 250
    )
    if token_count < minimum_tokens:
        add(
            findings,
            "error",
            "summary.detail.insufficient",
            "$",
            f"Detailed summary contains only {token_count} word/CJK tokens; at least {minimum_tokens} are required.",
        )
    normalized_tokens = [
        token.lower()
        for token in summary_tokens
        if len(token) > 1 or re.fullmatch(r"[\u3400-\u9fff]", token)
    ]
    if normalized_tokens:
        lexical_diversity = len(set(normalized_tokens)) / len(normalized_tokens)
        if lexical_diversity < 0.12:
            add(
                findings,
                "error",
                "summary.detail.repetitive",
                "$",
                (
                    "Summary content is too repetitive to demonstrate a "
                    f"detailed source analysis (lexical diversity {lexical_diversity:.3f})."
                ),
            )
    if len(section_matches) == len(SUMMARY_REQUIRED_HEADINGS):
        for index, (heading, match) in enumerate(section_matches[1:], start=1):
            end = (
                section_matches[index + 1][1].start()
                if index + 1 < len(section_matches)
                else len(summary_text)
            )
            section_text = summary_text[match.end() : end]
            raw_section_tokens = re.findall(
                r"[A-Za-z0-9_±Δ]+|[\u3400-\u9fff]",
                section_text,
            )
            section_tokens = len(raw_section_tokens)
            minimum_section_tokens = (
                80 if heading == "## 1. Executive summary" else 15
            )
            if section_tokens < minimum_section_tokens:
                add(
                    findings,
                    "error",
                    "summary.section.thin",
                    heading,
                    (
                        f"Section has only {section_tokens} word/CJK tokens; "
                        f"at least {minimum_section_tokens} are required."
                    ),
                )
            normalized_section_tokens = {
                token.lower()
                for token in raw_section_tokens
                if len(token) > 1 or re.fullmatch(r"[\u3400-\u9fff]", token)
            }
            if len(normalized_section_tokens) < 8:
                add(
                    findings,
                    "error",
                    "summary.section.repetitive",
                    heading,
                    "Section lacks enough distinct content to count as a detailed analysis.",
                )
            for sentinel in SUMMARY_SECTION_SENTINELS.get(heading, ()):
                if sentinel not in section_text:
                    add(
                        findings,
                        "error",
                        "summary.section.contract-missing",
                        heading,
                        f"Section is missing required structured field: {sentinel!r}",
                    )
    unresolved_bullets = re.findall(
        r"(?m)^-\s+[^:\n]+:\s*$",
        summary_text,
    )
    if unresolved_bullets:
        add(
            findings,
            "error",
            "summary.placeholder.empty-field",
            "$",
            f"Summary contains {len(unresolved_bullets)} empty template field(s).",
        )
    if re.search(r"(?m)^\|\s*(?:\|\s*){3,}$", summary_text):
        add(
            findings,
            "error",
            "summary.placeholder.empty-row",
            "$",
            "Summary contains an unresolved blank table row.",
        )
    if "Write a faithful 150–250 word account" in summary_text:
        add(
            findings,
            "error",
            "summary.placeholder.instructions",
            "$",
            "Summary still contains template-writing instructions.",
        )

    if spec is not None:
        if spec["source"]["title"] not in summary_text:
            add(
                findings,
                "error",
                "summary.source-title.missing",
                "$.source.title",
                "FigureSpec source title is absent from the detailed summary.",
            )
        anchors = {
            claim["source_anchor"]
            for claim in spec["claims"]
            if claim["status"] == "supported"
            and string_ok(claim.get("source_anchor"))
        }
        for anchor in sorted(anchors):
            if anchor not in summary_text:
                add(
                    findings,
                    "error",
                    "summary.anchor.missing",
                    "$.claims",
                    f"Supported-claim anchor is absent from the summary: {anchor!r}",
                )
    return findings


def expected_inventory_from_spec(spec: dict[str, Any]) -> dict[str, list[str]]:
    return {
        "panels": [panel["id"] for panel in spec["panels"]],
        "claims": [claim["id"] for claim in spec["claims"]],
        "components": [
            f"Panel {panel['id']}: {entity['id']} | label: {entity['label']}"
            for panel in spec["panels"]
            for entity in panel["entities"]
        ],
        "relations": [
            (
                f"Panel {panel['id']}: {relation['id']} | "
                f"{relation['from']} → {relation['to']} | "
                f"type: {relation['type']} | payload/label: "
                f"{relation['label'] or '(none)'}"
            )
            for panel in spec["panels"]
            for relation in panel["relations"]
        ],
        "must_show": list(spec["content"]["must_show"]),
        "required_text": list(spec["content"]["required_text"]),
        "critical_checks": list(spec["acceptance"]["critical_checks"]),
    }


def validate_audit(
    audit: Any, spec: dict[str, Any] | None = None
) -> list[Finding]:
    schema = load_json(ARTIFACT_SCHEMAS["figure-audit"])
    findings = validate_schema_shape(audit, schema)
    if findings or not isinstance(audit, dict):
        return findings
    if spec is not None:
        spec_findings = validate_spec(spec)
        spec_errors = [item for item in spec_findings if item.level == "error"]
        if spec_errors:
            add(
                findings,
                "error",
                "audit.spec.invalid",
                "$",
                "The comparison FigureSpec is invalid.",
            )
            return findings
        if audit["figure_id"] != spec["figure_id"]:
            add(
                findings,
                "error",
                "audit.figure-id",
                "$.figure_id",
                "Audit figure_id does not match FigureSpec.",
            )
        expected_from_spec = expected_inventory_from_spec(spec)
        for field, expected_items in expected_from_spec.items():
            if audit["expected_inventory"].get(field) != expected_items:
                add(
                    findings,
                    "error",
                    "audit.expected-inventory.mismatch",
                    f"$.expected_inventory.{field}",
                    "Expected inventory does not match the supplied FigureSpec.",
                )

    if audit["verdict"] == "pending":
        add(
            findings,
            "warning",
            "audit.pending",
            "$.verdict",
            "The audit has not been completed.",
        )
    if audit["verdict"] == "pass":
        if spec is None:
            add(
                findings,
                "error",
                "audit.pass.spec-required",
                "$.verdict",
                "A passing audit must be validated against its FigureSpec.",
            )
        if audit["critical_failures"]:
            add(
                findings,
                "error",
                "audit.pass.critical",
                "$.critical_failures",
                "A passing audit cannot contain critical failures.",
            )
        if audit["major_issues"]:
            add(
                findings,
                "error",
                "audit.pass.major",
                "$.major_issues",
                "A passing audit cannot contain major issues.",
            )
        technical = audit["technical_quality"]
        required_strings = {
            "artifact_path": "the rendered artifact path",
            "artifact_format": "the rendered artifact format",
            "artifact_sha256": "the rendered artifact SHA-256",
            "declared_final_dimensions": "declared final dimensions",
            "inspection_notes": "observable inspection notes",
        }
        if spec is not None and spec["target"]["editable"]:
            required_strings.update(
                {
                    "editable_source_path": "the editable source path",
                    "editable_source_sha256": "the editable source SHA-256",
                }
            )
        for field, label in required_strings.items():
            if not string_ok(technical[field]):
                add(
                    findings,
                    "error",
                    "audit.pass.technical-evidence",
                    f"$.technical_quality.{field}",
                    f"A passing audit must record {label}.",
                )
        if string_ok(technical["inspection_notes"]) and len(
            technical["inspection_notes"].strip()
        ) < 20:
            add(
                findings,
                "error",
                "audit.pass.inspection-notes",
                "$.technical_quality.inspection_notes",
                "Inspection notes must record observable results, not a bare assertion.",
            )

        artifact_fields = [
            ("artifact_path", "artifact_sha256"),
        ]
        if spec is not None and spec["target"]["editable"]:
            artifact_fields.append(
                ("editable_source_path", "editable_source_sha256")
            )
        for path_field, hash_field in artifact_fields:
            raw_path = technical[path_field]
            expected_hash = technical[hash_field].lower()
            if string_ok(expected_hash) and re.fullmatch(
                r"[0-9a-f]{64}", expected_hash
            ) is None:
                add(
                    findings,
                    "error",
                    "audit.pass.sha256-format",
                    f"$.technical_quality.{hash_field}",
                    "SHA-256 must contain exactly 64 hexadecimal characters.",
                )
            if string_ok(raw_path):
                artifact_path = Path(raw_path).expanduser()
                if not artifact_path.is_file():
                    add(
                        findings,
                        "error",
                        "audit.pass.artifact-missing",
                        f"$.technical_quality.{path_field}",
                        f"Recorded file does not exist: {raw_path}",
                    )
                elif re.fullmatch(r"[0-9a-f]{64}", expected_hash):
                    actual_hash = hashlib.sha256(
                        artifact_path.read_bytes()
                    ).hexdigest()
                    if actual_hash != expected_hash:
                        add(
                            findings,
                            "error",
                            "audit.pass.sha256-mismatch",
                            f"$.technical_quality.{hash_field}",
                            f"Recorded SHA-256 does not match {raw_path}.",
                        )
        artifact_format = technical["artifact_format"].strip().lower().lstrip(".")
        artifact_path = Path(technical["artifact_path"]).expanduser()
        format_suffixes = {
            "svg": {".svg"},
            "pdf": {".pdf"},
            "png": {".png"},
            "jpg": {".jpg", ".jpeg"},
            "jpeg": {".jpg", ".jpeg"},
            "webp": {".webp"},
            "pptx": {".pptx"},
            "drawio": {".drawio", ".xml"},
        }
        if artifact_format not in format_suffixes:
            add(
                findings,
                "error",
                "audit.pass.artifact-format",
                "$.technical_quality.artifact_format",
                "Artifact format must name the actual SVG, PDF, PNG, JPEG, WebP, PPTX, or draw.io export.",
            )
        elif artifact_path.suffix.lower() not in format_suffixes[artifact_format]:
            add(
                findings,
                "error",
                "audit.pass.artifact-extension",
                "$.technical_quality.artifact_path",
                "Artifact filename extension does not match artifact_format.",
            )
        elif artifact_path.is_file():
            signature_error = artifact_signature_error(
                artifact_path, artifact_format
            )
            if signature_error:
                add(
                    findings,
                    "error",
                    "audit.pass.artifact-signature",
                    "$.technical_quality.artifact_path",
                    signature_error,
                )
            elif artifact_format == "svg" and spec is not None:
                for svg_finding in inspect_svg(artifact_path, spec):
                    if svg_finding.level in {"error", "warning"}:
                        add(
                            findings,
                            "error",
                            "audit.pass.svg-structure",
                            svg_finding.path,
                            f"SVG structural precheck failed [{svg_finding.code}]: {svg_finding.message}",
                        )
        if spec is not None and spec["target"]["editable"]:
            editable_path = Path(
                technical["editable_source_path"]
            ).expanduser()
            editable_formats = {
                ".svg": "svg",
                ".pptx": "pptx",
                ".drawio": "drawio",
                ".xml": "drawio",
                ".pdf": "pdf",
            }
            editable_format = editable_formats.get(
                editable_path.suffix.lower()
            )
            if editable_path.is_file() and editable_format is not None:
                signature_error = artifact_signature_error(
                    editable_path, editable_format
                )
                if signature_error:
                    add(
                        findings,
                        "error",
                        "audit.pass.editable-signature",
                        "$.technical_quality.editable_source_path",
                        signature_error,
                    )
                elif (
                    editable_format == "svg"
                    and spec is not None
                    and editable_path != artifact_path
                ):
                    for svg_finding in inspect_svg(editable_path, spec):
                        if svg_finding.level in {"error", "warning"}:
                            add(
                                findings,
                                "error",
                                "audit.pass.editable-svg-structure",
                                svg_finding.path,
                                f"Editable SVG precheck failed [{svg_finding.code}]: {svg_finding.message}",
                            )
        required_inspections = {
            "artifact_inspected": "the rendered artifact",
            "final_size_checked": "the final publication size",
            "zoom_100_checked": "the 100% view",
            "zoom_200_checked": "the 200% view",
        }
        if spec is not None and spec["target"]["editable"]:
            required_inspections.update(
                {
                    "editable_source_checked": "the editable master",
                    "live_text_verified": "live editable text",
                }
            )
        for field, label in required_inspections.items():
            if technical[field] is not True:
                add(
                    findings,
                    "error",
                    "audit.pass.technical-check",
                    f"$.technical_quality.{field}",
                    f"A passing audit must verify {label}.",
                )
        technical_defects = {
            "blurred_or_soft_regions": "blurred, fuzzy, melted, or ghosted regions",
            "font_or_glyph_errors": "font, glyph, spelling, or pseudo-text errors",
            "overlap_or_clipping": "overlap, clipping, or off-canvas defects",
            "rasterization_or_resolution_issues": (
                "unintended rasterization, low resolution, or visible upscaling"
            ),
        }
        for field, description in technical_defects.items():
            if technical[field]:
                add(
                    findings,
                    "error",
                    "audit.pass.technical-defect",
                    f"$.technical_quality.{field}",
                    f"A passing audit cannot retain {description}.",
                )
        expected_inventory = audit["expected_inventory"]
        visible_inventory = audit["visible_inventory"]
        for field in (
            "panels",
            "components",
            "relations",
            "must_show",
            "required_text",
        ):
            missing = [
                item
                for item in expected_inventory[field]
                if item not in visible_inventory[field]
            ]
            for item in missing:
                add(
                    findings,
                    "error",
                    "audit.pass.inventory-missing",
                    f"$.visible_inventory.{field}",
                    f"Expected visible item was not inventoried: {item}",
                )
            unexpected = [
                item
                for item in visible_inventory[field]
                if item not in expected_inventory[field]
            ]
            for item in unexpected:
                add(
                    findings,
                    "error",
                    "audit.pass.inventory-extra",
                    f"$.visible_inventory.{field}",
                    f"Unspecified visible item was inventoried: {item}",
                )
        if spec is not None and spec["claims"] and not audit["reader_inferences"]:
            add(
                findings,
                "error",
                "audit.pass.inferences-empty",
                "$.reader_inferences",
                "A passing audit must record the scientific inference(s) made by a reader.",
            )
        for index, inference in enumerate(audit["reader_inferences"]):
            if inference["status"] != "supported":
                add(
                    findings,
                    "error",
                    "audit.pass.inference",
                    f"$.reader_inferences[{index}].status",
                    "A passing audit cannot retain a non-supported reader inference.",
                )
            if inference["status"] == "supported" and not string_ok(
                inference["source_anchor"]
            ):
                add(
                    findings,
                    "error",
                    "audit.pass.inference-anchor",
                    f"$.reader_inferences[{index}].source_anchor",
                    "A supported reader inference requires a source anchor.",
                )
        if spec is not None:
            supported_anchors = {
                claim["source_anchor"]
                for claim in spec["claims"]
                if claim["status"] == "supported"
            }
            visible_anchors = {
                inference["source_anchor"]
                for inference in audit["reader_inferences"]
                if inference["status"] == "supported"
                and string_ok(inference["source_anchor"])
            }
            for index, inference in enumerate(audit["reader_inferences"]):
                if (
                    inference["status"] == "supported"
                    and inference["source_anchor"] not in supported_anchors
                ):
                    add(
                        findings,
                        "error",
                        "audit.pass.inference-anchor-unknown",
                        f"$.reader_inferences[{index}].source_anchor",
                        "Supported reader inference anchor does not belong to a supported FigureSpec claim.",
                    )
            for claim in spec["claims"]:
                if (
                    claim["status"] == "supported"
                    and claim["source_anchor"] not in visible_anchors
                ):
                    add(
                        findings,
                        "error",
                        "audit.pass.claim-not-reviewed",
                        "$.reader_inferences",
                        f"Supported claim anchor was not covered by a reader inference: {claim['source_anchor']}",
                    )
        thresholds = (
            spec["acceptance"]["minimum_scores"]
            if spec is not None
            else {
                "scientific_fidelity": 5,
                "structural_correctness": 5,
                "role_purity": 4,
                "message_clarity": 4,
                "readability": 4,
                "accessibility": 4,
                "editability_reproducibility": 4,
            }
        )
        for dimension, threshold in thresholds.items():
            value = audit["scores"].get(dimension)
            if value is None or value < threshold:
                add(
                    findings,
                    "error",
                    "audit.pass.score",
                    f"$.scores.{dimension}",
                    f"Passing audit requires score >= {threshold}.",
                )
    return findings


def validate_spec(spec: Any) -> list[Finding]:
    try:
        root_schema = load_json(SCHEMA_PATH)
        shape_findings = validate_schema_shape(spec, root_schema)
    except ValueError as exc:
        return [Finding("error", "schema.load", str(SCHEMA_PATH), str(exc))]
    if shape_findings:
        return shape_findings

    findings: list[Finding] = []
    if not isinstance(spec, dict):
        return [
            Finding("error", "root.type", "$", "FigureSpec root must be an object.")
        ]

    required_top = {
        "schema_version",
        "figure_id",
        "source",
        "target",
        "intent",
        "claims",
        "content",
        "panels",
        "layout",
        "render",
        "style",
        "acceptance",
    }
    for key in sorted(required_top - set(spec)):
        add(findings, "error", "field.required", "$", f"Missing top-level field: {key}")

    if spec.get("schema_version") != "2.0":
        add(
            findings,
            "error",
            "schema.version",
            "$.schema_version",
            "Only FigureSpec schema_version 2.0 is supported.",
        )
    if not string_ok(spec.get("figure_id")):
        add(
            findings,
            "error",
            "figure_id.invalid",
            "$.figure_id",
            "figure_id must be a non-empty string.",
        )

    source = as_dict(spec.get("source"))
    for key in ("title", "type", "scope", "limitations"):
        if key not in source:
            add(
                findings,
                "error",
                "field.required",
                "$.source",
                f"Missing source.{key}.",
            )
    if source.get("type") not in {
        "paper",
        "proposal",
        "brief",
        "data",
        "existing-figure",
    }:
        add(
            findings,
            "error",
            "source.type",
            "$.source.type",
            "Unknown source type.",
        )
    if not as_list(source.get("scope")):
        add(
            findings,
            "warning",
            "source.scope.empty",
            "$.source.scope",
            "Record the exact source sections, tables, files, or user statements inspected.",
        )

    target = as_dict(spec.get("target"))
    for key in ("medium", "venue", "audience", "language", "size", "editable"):
        if key not in target:
            add(
                findings,
                "error",
                "field.required",
                "$.target",
                f"Missing target.{key}.",
            )

    intent = as_dict(spec.get("intent"))
    role = intent.get("role")
    if role not in ROLES:
        add(
            findings,
            "error",
            "intent.role",
            "$.intent.role",
            f"Unknown role {role!r}.",
        )
    for key in ("reader_question", "five_second_message", "claim_boundary"):
        if not string_ok(intent.get(key)):
            add(
                findings,
                "error",
                f"intent.{key}",
                f"$.intent.{key}",
                f"intent.{key} must be a non-empty string.",
            )

    claims = as_list(spec.get("claims"))
    claim_ids = [c.get("id") for c in claims if isinstance(c, dict)]
    for duplicate in sorted(str(x) for x in duplicate_values(claim_ids)):
        add(
            findings,
            "error",
            "claim.id.duplicate",
            "$.claims",
            f"Duplicate claim ID: {duplicate}",
        )
    claim_map = {
        c.get("id"): c
        for c in claims
        if isinstance(c, dict) and string_ok(c.get("id"))
    }
    for index, raw_claim in enumerate(claims):
        path = f"$.claims[{index}]"
        claim = as_dict(raw_claim)
        for key in ("id", "text", "status", "scope", "source_anchor", "evidence"):
            if key not in claim:
                add(
                    findings,
                    "error",
                    "field.required",
                    path,
                    f"Missing claim.{key}.",
                )
        if claim.get("status") not in CLAIM_STATUSES:
            add(
                findings,
                "error",
                "claim.status",
                f"{path}.status",
                f"Unknown claim status {claim.get('status')!r}.",
            )
        if claim.get("scope") not in CLAIM_SCOPES:
            add(
                findings,
                "error",
                "claim.scope",
                f"{path}.scope",
                f"Unknown claim scope {claim.get('scope')!r}.",
            )
        if claim.get("status") == "supported":
            if not string_ok(claim.get("source_anchor")):
                add(
                    findings,
                    "error",
                    "claim.anchor.missing",
                    f"{path}.source_anchor",
                    "A supported claim requires a source anchor.",
                )
            if not string_ok(claim.get("evidence")):
                add(
                    findings,
                    "error",
                    "claim.evidence.missing",
                    f"{path}.evidence",
                    "A supported claim requires an evidence statement.",
                )

    content = as_dict(spec.get("content"))
    for key in ("must_show", "nice_to_show", "must_not_show", "required_text"):
        if not isinstance(content.get(key), list):
            add(
                findings,
                "error",
                "content.type",
                f"$.content.{key}",
                f"content.{key} must be an array.",
            )
    if not as_list(content.get("must_not_show")):
        add(
            findings,
            "warning",
            "content.negatives.empty",
            "$.content.must_not_show",
            "Add explicit forbidden content and stronger readings.",
        )

    panels = as_list(spec.get("panels"))
    panel_ids = [p.get("id") for p in panels if isinstance(p, dict)]
    for duplicate in sorted(str(x) for x in duplicate_values(panel_ids)):
        add(
            findings,
            "error",
            "panel.id.duplicate",
            "$.panels",
            f"Duplicate panel ID: {duplicate}",
        )
    used_claims: set[str] = set()
    relation_ids: list[str] = []
    for p_index, raw_panel in enumerate(panels):
        panel_path = f"$.panels[{p_index}]"
        panel = as_dict(raw_panel)
        for key in (
            "id",
            "title",
            "question",
            "claim_ids",
            "dominance",
            "visual_form",
            "entities",
            "relations",
        ):
            if key not in panel:
                add(
                    findings,
                    "error",
                    "field.required",
                    panel_path,
                    f"Missing panel.{key}.",
                )
        if role == "mixed" and panel.get("role") not in ROLES - {"mixed"}:
            add(
                findings,
                "error",
                "panel.role.required",
                f"{panel_path}.role",
                "A mixed figure requires a non-mixed role for every panel.",
            )
        for claim_id in as_list(panel.get("claim_ids")):
            if claim_id not in claim_map:
                add(
                    findings,
                    "error",
                    "panel.claim.unknown",
                    f"{panel_path}.claim_ids",
                    f"Unknown claim ID: {claim_id}",
                )
                continue
            used_claims.add(claim_id)
            claim = claim_map[claim_id]
            if claim.get("status") == "missing":
                add(
                    findings,
                    "error",
                    "panel.claim.missing",
                    f"{panel_path}.claim_ids",
                    f"Missing claim {claim_id} cannot be assigned to a renderable panel.",
                )
            if claim.get("status") in {"inferred", "hypothesis"} and not string_ok(
                claim.get("visual_label")
            ):
                add(
                    findings,
                    "error",
                    "panel.claim.epistemic-label",
                    f"{panel_path}.claim_ids",
                    f"{claim_id} must define visual_label to expose its epistemic status.",
                )

        entities = as_list(panel.get("entities"))
        entity_ids = [
            e.get("id") for e in entities if isinstance(e, dict) and e.get("id")
        ]
        for duplicate in sorted(str(x) for x in duplicate_values(entity_ids)):
            add(
                findings,
                "error",
                "entity.id.duplicate",
                f"{panel_path}.entities",
                f"Duplicate entity ID in panel: {duplicate}",
            )
        entity_set = set(entity_ids)
        for r_index, raw_relation in enumerate(as_list(panel.get("relations"))):
            relation_path = f"{panel_path}.relations[{r_index}]"
            relation = as_dict(raw_relation)
            for key in ("id", "from", "to", "type", "label"):
                if key not in relation:
                    add(
                        findings,
                        "error",
                        "field.required",
                        relation_path,
                        f"Missing relation.{key}.",
                    )
            if string_ok(relation.get("id")):
                relation_ids.append(relation["id"])
            for endpoint in ("from", "to"):
                if relation.get(endpoint) not in entity_set:
                    add(
                        findings,
                        "error",
                        "relation.endpoint.unknown",
                        f"{relation_path}.{endpoint}",
                        f"Unknown entity endpoint: {relation.get(endpoint)!r}",
                    )
            rel_type = relation.get("type")
            if rel_type not in RELATION_TYPES:
                add(
                    findings,
                    "error",
                    "relation.type",
                    f"{relation_path}.type",
                    f"Unknown relation type {rel_type!r}.",
                )
            claim_id = relation.get("claim_id")
            if claim_id and claim_id not in claim_map:
                add(
                    findings,
                    "error",
                    "relation.claim.unknown",
                    f"{relation_path}.claim_id",
                    f"Unknown relation claim ID: {claim_id}",
                )
            if rel_type == "causal":
                causal_claim = claim_map.get(claim_id)
                if not causal_claim:
                    add(
                        findings,
                        "error",
                        "relation.causal.no-claim",
                        relation_path,
                        "A causal relation requires claim_id.",
                    )
                elif not (
                    causal_claim.get("status") == "supported"
                    and causal_claim.get("scope") == "causal"
                ):
                    add(
                        findings,
                        "error",
                        "relation.causal.unsupported",
                        relation_path,
                        "A causal relation requires a supported claim with causal scope.",
                    )
            if rel_type == "causal-hypothesis":
                hypothesis_claim = claim_map.get(claim_id)
                if not hypothesis_claim:
                    add(
                        findings,
                        "error",
                        "relation.causal-hypothesis.no-claim",
                        relation_path,
                        "A causal-hypothesis relation requires claim_id.",
                    )
                elif not (
                    hypothesis_claim.get("status") in {"inferred", "hypothesis"}
                    and hypothesis_claim.get("scope") == "causal"
                    and string_ok(hypothesis_claim.get("visual_label"))
                ):
                    add(
                        findings,
                        "error",
                        "relation.causal-hypothesis.invalid",
                        relation_path,
                        "A causal-hypothesis relation requires an inferred/hypothesis causal claim with visual_label.",
                    )

    for duplicate in sorted(duplicate_values(relation_ids)):
        add(
            findings,
            "error",
            "relation.id.duplicate",
            "$.panels",
            f"Duplicate relation ID: {duplicate}",
        )

    if claims and not panels:
        add(
            findings,
            "warning",
            "panels.empty",
            "$.panels",
            "No renderable panels are defined.",
        )
    for claim_id, claim in claim_map.items():
        if claim.get("status") == "supported" and claim_id not in used_claims:
            add(
                findings,
                "note",
                "claim.unused",
                "$.claims",
                f"Supported claim {claim_id} is not assigned to a panel.",
            )

    layout = as_dict(spec.get("layout"))
    reading_order = as_list(layout.get("reading_order"))
    known_panels = set(panel_ids)
    for panel_id in reading_order:
        if panel_id not in known_panels:
            add(
                findings,
                "error",
                "layout.panel.unknown",
                "$.layout.reading_order",
                f"Unknown panel in reading order: {panel_id}",
            )
    if panels and set(reading_order) != known_panels:
        add(
            findings,
            "warning",
            "layout.reading-order.incomplete",
            "$.layout.reading_order",
            "Reading order should contain every panel exactly once.",
        )
    regions = as_list(layout.get("regions"))
    region_ids = [
        as_dict(region).get("id")
        for region in regions
        if string_ok(as_dict(region).get("id"))
    ]
    for duplicate in sorted(str(x) for x in duplicate_values(region_ids)):
        add(
            findings,
            "error",
            "layout.region-id.duplicate",
            "$.layout.regions",
            f"Duplicate normalized region ID: {duplicate}",
        )
    for index, raw_region in enumerate(regions):
        region = as_dict(raw_region)
        path = f"$.layout.regions[{index}]"
        width = region.get("w_pct")
        height = region.get("h_pct")
        if isinstance(width, (int, float)) and width <= 0:
            add(
                findings,
                "error",
                "layout.region.width",
                f"{path}.w_pct",
                "Normalized region width must be greater than zero.",
            )
        if isinstance(height, (int, float)) and height <= 0:
            add(
                findings,
                "error",
                "layout.region.height",
                f"{path}.h_pct",
                "Normalized region height must be greater than zero.",
            )
        x = region.get("x_pct")
        y = region.get("y_pct")
        if (
            isinstance(x, (int, float))
            and isinstance(width, (int, float))
            and x + width > 100
        ):
            add(
                findings,
                "error",
                "layout.region.horizontal-bounds",
                path,
                "Normalized region extends beyond the right canvas edge.",
            )
        if (
            isinstance(y, (int, float))
            and isinstance(height, (int, float))
            and y + height > 100
        ):
            add(
                findings,
                "error",
                "layout.region.vertical-bounds",
                path,
                "Normalized region extends beyond the bottom canvas edge.",
            )
    max_words = layout.get("max_label_words")
    if isinstance(max_words, int) and max_words > 0:
        for text in as_list(content.get("required_text")):
            if isinstance(text, str) and len(text.split()) > max_words:
                add(
                    findings,
                    "warning",
                    "text.long",
                    "$.content.required_text",
                    f"Required label exceeds max_label_words={max_words}: {text!r}",
                )

    render = as_dict(spec.get("render"))
    mode = render.get("mode")
    if mode not in RENDER_MODES:
        add(
            findings,
            "error",
            "render.mode",
            "$.render.mode",
            f"Unknown render mode {mode!r}.",
        )
    if render.get("deterministic_numbers") and mode == "image-generation":
        add(
            findings,
            "error",
            "render.numeric-imagegen",
            "$.render",
            "Deterministic numeric content cannot use pure image generation.",
        )
    if mode == "image-generation" and (
        render.get("deterministic_text") or as_list(content.get("required_text"))
    ):
        add(
            findings,
            "error",
            "render.text-imagegen",
            "$.render",
            "Exact or required text needs vector/hybrid composition, not pure image generation.",
        )
    if as_list(content.get("required_text")) and render.get(
        "deterministic_text"
    ) is not True:
        add(
            findings,
            "error",
            "render.text-determinism",
            "$.render.deterministic_text",
            "Required exact text requires deterministic_text=true.",
        )
    if role in QUANTITATIVE_ROLES:
        if mode == "image-generation":
            add(
                findings,
                "error",
                "render.quantitative-imagegen",
                "$.render.mode",
                f"{role} figures cannot use pure image generation.",
            )
        if render.get("deterministic_numbers") is not True:
            add(
                findings,
                "error",
                "render.quantitative-determinism",
                "$.render.deterministic_numbers",
                f"{role} figures require deterministic_numbers=true.",
            )
        if not string_ok(render.get("data_source")):
            add(
                findings,
                "error",
                "render.data-source",
                "$.render.data_source",
                f"{role} figures require a machine-readable data_source.",
            )
    if target.get("editable") and str(render.get("preferred_format", "")).lower() in {
        "png",
        "jpg",
        "jpeg",
        "webp",
    }:
        add(
            findings,
            "warning",
            "render.editability",
            "$.render.preferred_format",
            "Editable target should prefer a vector or native source format.",
        )

    visual_reference = as_dict(spec.get("visual_reference"))
    if visual_reference:
        reference_available = visual_reference.get("available")
        reference_mode = visual_reference.get("mode")
        if reference_available:
            if not string_ok(visual_reference.get("source")):
                add(
                    findings,
                    "error",
                    "reference.source.missing",
                    "$.visual_reference.source",
                    "An available reference requires a source path or identifier.",
                )
            if reference_mode == "none":
                add(
                    findings,
                    "error",
                    "reference.mode.none",
                    "$.visual_reference.mode",
                    "An available reference must use layout-only or abstract-attributes mode.",
                )
            if not as_list(visual_reference.get("use_for")):
                add(
                    findings,
                    "error",
                    "reference.attributes.empty",
                    "$.visual_reference.use_for",
                    "Record the inspected abstract attributes to use.",
                )
        elif reference_mode not in {None, "none"}:
            add(
                findings,
                "warning",
                "reference.unavailable.mode",
                "$.visual_reference.mode",
                "Reference mode should be none when no reference is available.",
            )
        if not as_list(visual_reference.get("do_not_copy")):
            add(
                findings,
                "error",
                "reference.copy-boundary.empty",
                "$.visual_reference.do_not_copy",
                "Reference contract requires explicit do-not-copy boundaries.",
            )
        for index, instruction in enumerate(
            as_list(visual_reference.get("use_for"))
        ):
            text = str(instruction)
            matched = [
                pattern
                for pattern in (
                    *UNSAFE_REFERENCE_PATTERNS,
                    *UNSAFE_REFERENCE_CONTENT_PATTERNS,
                )
                if re.search(pattern, text, flags=re.IGNORECASE)
            ]
            if matched:
                add(
                    findings,
                    "error",
                    "reference.use-for.unsafe",
                    f"$.visual_reference.use_for[{index}]",
                    "Reference use_for may contain only abstract, non-exclusive visual attributes; exact copying and source content are forbidden.",
                )
            if not any(
                re.search(pattern, text, flags=re.IGNORECASE)
                for pattern in REFERENCE_ABSTRACT_ATTRIBUTE_PATTERNS
            ):
                add(
                    findings,
                    "error",
                    "reference.use-for.not-abstract",
                    f"$.visual_reference.use_for[{index}]",
                    (
                        "Reference use_for must name a recognized abstract "
                        "attribute such as aspect ratio, region proportions, "
                        "alignment, whitespace, density, border treatment, "
                        "palette relationship, icon scale, arrow rhythm, or "
                        "typography hierarchy."
                    ),
                )
        copy_boundary = " ".join(
            str(item) for item in as_list(visual_reference.get("do_not_copy"))
        ).lower()
        boundary_requirements = {
            "scientific content/text/value boundary": (
                "scientific",
                "text",
                "label",
                "value",
                "equation",
            ),
            "logo/branding boundary": ("logo", "brand"),
            "distinctive-expression boundary": (
                "distinctive",
                "unique",
                "signature",
                "composition",
                "icon",
                "motif",
                "expression",
            ),
        }
        for label, tokens in boundary_requirements.items():
            if not any(token in copy_boundary for token in tokens):
                add(
                    findings,
                    "error",
                    "reference.copy-boundary.incomplete",
                    "$.visual_reference.do_not_copy",
                    f"Reference do_not_copy is missing the {label}.",
                )

    if role == "motivation":
        for p_index, panel in enumerate(panels):
            for r_index, relation in enumerate(as_list(as_dict(panel).get("relations"))):
                if as_dict(relation).get("type") in {"data-flow", "control-flow"}:
                    add(
                        findings,
                        "warning",
                        "role.motivation.workflow",
                        f"$.panels[{p_index}].relations[{r_index}]",
                        "A motivation figure may be turning independent problems into a workflow.",
                    )

    acceptance = as_dict(spec.get("acceptance"))
    scores = as_dict(acceptance.get("minimum_scores"))
    for dimension in (
        "scientific_fidelity",
        "structural_correctness",
        "role_purity",
        "message_clarity",
        "readability",
        "accessibility",
        "editability_reproducibility",
    ):
        value = scores.get(dimension)
        if not isinstance(value, int) or not 1 <= value <= 5:
            add(
                findings,
                "error",
                "acceptance.score",
                f"$.acceptance.minimum_scores.{dimension}",
                "Minimum score must be an integer from 1 to 5.",
            )
    if scores.get("scientific_fidelity", 0) < 5:
        add(
            findings,
            "warning",
            "acceptance.fidelity-low",
            "$.acceptance.minimum_scores.scientific_fidelity",
            "Scientific fidelity should normally be a hard 5/5 gate.",
        )
    if scores.get("structural_correctness", 0) < 5:
        add(
            findings,
            "warning",
            "acceptance.structure-low",
            "$.acceptance.minimum_scores.structural_correctness",
            "Structural correctness should normally be a hard 5/5 gate.",
        )

    return findings


def build_new_spec(role: str) -> dict[str, Any]:
    if role not in ROLES:
        raise ValueError(f"Unknown role {role!r}; choose from {sorted(ROLES)}")
    spec = load_json(TEMPLATE_PATH)
    defaults = ROLE_DEFAULTS[role]
    spec["intent"].update(
        {
            "role": role,
            "reader_question": defaults["question"],
            "five_second_message": defaults["message"],
            "claim_boundary": defaults["boundary"],
        }
    )
    if role in QUANTITATIVE_ROLES:
        spec["render"].update(
            {
                "mode": "plot-code",
                "deterministic_numbers": True,
                "preferred_format": "svg",
                "fallback_format": "pdf",
            }
        )
    elif role == "graphical-abstract":
        spec["render"]["mode"] = "hybrid"
    return spec


def format_bullets(items: Iterable[Any], empty: str = "- None specified") -> str:
    material = [str(item) for item in items if str(item).strip()]
    return "\n".join(f"- {item}" for item in material) if material else empty


def compile_prompt(
    spec: dict[str, Any],
    summary_text: str,
    allow_warnings: bool = False,
    _skip_self_lint: bool = False,
) -> str:
    findings = validate_spec(spec)
    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]
    blocking = errors + ([] if allow_warnings else warnings)
    if blocking:
        details = "\n".join(
            f"- [{finding.code}] {finding.path}: {finding.message}"
            for finding in blocking
        )
        label = "errors" if errors else "warnings"
        raise ValueError(f"FigureSpec has validation {label}:\n{details}")
    if (
        not spec["claims"]
        or not spec["panels"]
        or not spec["content"]["must_show"]
    ):
        raise ValueError(
            "Production prompt compilation requires at least one claim, one panel, and one must_show item."
        )
    summary_findings = validate_paper_summary(summary_text, spec)
    summary_errors = [
        finding for finding in summary_findings if finding.level == "error"
    ]
    if summary_errors:
        details = "\n".join(
            f"- [{finding.code}] {finding.path}: {finding.message}"
            for finding in summary_errors
        )
        raise ValueError(f"Detailed paper summary failed validation:\n{details}")

    intent = spec["intent"]
    role = intent["role"]
    render = spec["render"]
    claims = spec["claims"]
    content = spec["content"]
    layout = spec["layout"]
    target = spec["target"]
    style = spec["style"]
    reference = as_dict(spec.get("visual_reference"))

    claim_lines = []
    narrative_lines = []
    for index, claim in enumerate(claims, start=1):
        suffix = (
            f" | visible epistemic label: {claim['visual_label']}"
            if claim.get("visual_label")
            else ""
        )
        claim_lines.append(
            f"{claim['id']} [{claim['status']}/{claim['scope']}] "
            f"{claim['text']} | source: {claim['source_anchor'] or 'MISSING'}"
            f" | evidence: {claim['evidence'] or 'MISSING'}"
            f"{suffix}"
        )
        narrative_lines.append(
            f"{index}. {claim['id']} [{claim['status']}]: {claim['text']}"
        )

    panel_lines = []
    entity_lines = []
    relation_lines = []
    for panel in spec["panels"]:
        panel_role = f" | role: {panel['role']}" if panel.get("role") else ""
        panel_lines.append(
            f"Panel {panel['id']} — {panel['title']}{panel_role} | "
            f"question: {panel['question']} | claims: "
            f"{', '.join(panel['claim_ids']) or 'none'} | "
            f"dominance: {panel['dominance']} | form: {panel['visual_form']}"
        )
        for entity in panel["entities"]:
            entity_lines.append(
                f"Panel {panel['id']}: {entity['id']} | kind: {entity['kind']} "
                f"| exact label: {entity['label']}"
            )
        for relation in panel["relations"]:
            claim_suffix = (
                f" | claim: {relation['claim_id']}"
                if relation.get("claim_id")
                else ""
            )
            relation_lines.append(
                f"Panel {panel['id']}: {relation['id']} | "
                f"{relation['from']} → {relation['to']} "
                f"| type: {relation['type']} | payload/label: "
                f"{relation['label'] or '(none)'}{claim_suffix}"
            )

    region_lines = []
    for region in as_list(layout.get("regions")):
        item = as_dict(region)
        width = item.get("w_pct", item.get("width_pct"))
        height = item.get("h_pct", item.get("height_pct"))
        region_lines.append(
            f"Region {item.get('id', 'unnamed')}: "
            f"purpose={item.get('purpose', 'not specified')} | "
            f"x={item.get('x_pct', 'unspecified')}%, "
            f"y={item.get('y_pct', 'unspecified')}%, "
            f"width={width if width is not None else 'unspecified'}%, "
            f"height={height if height is not None else 'unspecified'}%"
        )

    reference_available = bool(reference.get("available"))
    reference_use = as_list(reference.get("use_for"))
    reference_do_not_copy = as_list(reference.get("do_not_copy"))
    reference_source = reference.get("source") or "none supplied"
    reference_mode = reference.get("mode") or "none"
    color_semantics = "; ".join(
        f"{color}={meaning}" for color, meaning in style["color_semantics"].items()
    )
    main_title = content.get("title") or "not specified; do not invent one"
    risk_section = (
        "\n## Known validation warnings\n"
        + "\n".join(f"- [{f.code}] {f.message}" for f in warnings)
        + "\n"
        if warnings
        else ""
    )
    role_negatives = [
        f"Anything that violates this claim boundary: {intent['claim_boundary']}",
        f"Content that changes the dominant {role} role into another figure role",
    ]
    negative_items = [
        *content["must_not_show"],
        *style["avoid"],
        *reference_do_not_copy,
        *role_negatives,
        "invented components, values, equations, citations, claims, or causal links",
        "unlabeled or scientifically ambiguous arrows",
        "decorative entities that resemble additional scientific components",
        "fake numbers, pseudo-equations, watermarks, venue logos, or celebratory badges",
        *OPTICAL_NEGATIVE_RULES,
    ]
    output_items = [
        f"editable master: {render['preferred_format']}",
        f"paper/vector fallback: {render['fallback_format']}",
        "crisp high-resolution preview at the requested final aspect and size",
        "font and external-asset manifest when non-system assets are used",
        "provenance record and completed RF-CRITIQUE-2.0 audit",
    ]

    summary_hash = summary_sha256(summary_text)
    prompt = f"""[COMPILED_FROM: RF-COMPILE-2.0 | FIGURESPEC: {spec['schema_version']} | FIGURE: {spec['figure_id']} | SUMMARY_SHA256: {summary_hash}]

# 1. JOB, TARGET, AND CANVAS

Create a publication-quality scientific figure for {target['venue']}.

- Figure ID and role: {spec['figure_id']} / {role}
- Medium: {target['medium']}
- Audience and language: {target['audience']} / {target['language']}
- Final canvas or column class: {target['size']}
- Editable source required: {str(target['editable']).lower()}

# 2. REFERENCE-FIGURE CONTRACT

- Reference available: {str(reference_available).lower()}
- Source: {reference_source}
- Use mode: {reference_mode}
- Use only these abstract attributes:
{format_bullets(reference_use)}
- Do not copy:
{format_bullets(reference_do_not_copy)}
- Replace all reference-specific scientific content. The validated inventory below overrides the reference whenever they conflict.

# 3. SCIENTIFIC TOPIC AND PURPOSE

- Source topic: {spec['source']['title']}
- Figure role: {role}
- Reader question: {intent['reader_question']}
- Five-second message: {intent['five_second_message']}
- Claim boundary: {intent['claim_boundary']}
- Source scope: {', '.join(spec['source']['scope']) or 'not specified'}
- Known source limitations: {', '.join(spec['source']['limitations']) or 'none recorded'}

Render only the supplied scientific inventory. Preserve epistemic qualifiers
and source-bounded scope. Never fill missing evidence with plausible content.

# 4. SCIENTIFIC NARRATIVE

Communicate the following evidence-bounded propositions in order:
{format_bullets(narrative_lines)}

Role-specific narrative directive:
{ROLE_DEFAULTS[role]['adapter']}

Claim inventory with provenance:
{format_bullets(claim_lines)}

# 5. CONTENT AND EXACT-TEXT INVENTORY

- Main title: {main_title}

Must show:
{format_bullets(content['must_show'])}

Semantic entities with stable IDs:
{format_bullets(entity_lines)}

Required exact text:
{format_bullets(content['required_text'])}

Optional; remove before compressing required content:
{format_bullets(content['nice_to_show'])}

# 6. RELATION AND ARROW CONTRACT

{format_bullets(relation_lines)}

Every connector must preserve its listed source, target, direction, type, and
payload. Never add an unlabeled or scientifically ambiguous arrow.

# 7. GLOBAL LAYOUT AND REGION GEOMETRY

- Topology: {layout['topology']}
- Reading order: {', '.join(layout['reading_order']) or 'not specified'}
- Hierarchy: {' > '.join(layout['hierarchy'])}
- Panel grid: {layout['panel_grid']}
- Whitespace: {layout['whitespace']}
- Maximum label words: {layout['max_label_words']}

Normalized regions:
{format_bullets(region_lines, empty='- No normalized region geometry specified; do not infer percentages from an uninspected reference.')}

# 8. PER-PANEL COMPOSITION

{format_bullets(panel_lines)}

# 9. VISUAL LANGUAGE

- Background: {style['background']}
- Palette: {', '.join(style['palette'])}
- Color semantics: {color_semantics or 'none specified'}
- Typography: {style['font']}; preserve exact glyphs and a clear title/label hierarchy.
- Borders and lines: {style['line_style']}
- Density and whitespace: {layout['whitespace']}
- Accessibility: pair color with shape, text, or line style; never rely on color alone.

# 10. EDITABLE CONSTRUCTION CONTRACT

- Renderer mode: {render['mode']}
- {RENDERER_ADAPTERS[render['mode']]}
- Keep final labels as live editable text.
- Keep core shapes and arrows as vector or native objects with stable IDs.
- Do not flatten the complete figure into one bitmap.
- Deterministic text/numbers: {str(render['deterministic_text']).lower()} / {str(render['deterministic_numbers']).lower()}
- Data source: {render['data_source'] or 'none'}
- External provider allowed: {str(render['external_provider_allowed']).lower()}
- If AI image generation is used, generate only the approved illustration layer; add exact text, arrows, equations, plots, and values deterministically.

# 11. NEGATIVE PROMPT

Do not include:
{format_bullets(negative_items)}

# 12. OUTPUT CONTRACT

Return:
{format_bullets(output_items)}

Report every instruction that could not be rendered faithfully. Do not silently
drop required content or replace missing evidence with plausible content.
{risk_section}
# 13. PREFLIGHT BEFORE DELIVERY

- [ ] One dominant reader question is answered and the five-second message is visually dominant.
- [ ] Every required component appears exactly once unless repetition is specified.
- [ ] Every forbidden component is absent.
- [ ] Every arrow has the correct endpoints, direction, semantic type, and payload.
- [ ] Every required label matches the exact-text register and is readable at final size.
- [ ] No text is pseudo-text, misspelled, warped, substituted, clipped, or unintentionally rasterized.
- [ ] No local shape is blurred, fuzzy, melted, ghosted, partially erased, or visibly upscaled.
- [ ] The real export is inspected at final publication size, 100%, and 200% zoom.
- [ ] No label or object overlaps, clips, truncates, or falls off canvas.
- [ ] The editable master retains live text, semantic groups, stable IDs, and editable relations.
- [ ] The claim boundary cannot be misread from arrows, scale, color, or visual emphasis.
"""
    if not _skip_self_lint:
        prompt_findings = validate_compiled_prompt(
            prompt,
            spec,
            summary_text,
            require_canonical=False,
        )
        prompt_errors = [item for item in prompt_findings if item.level == "error"]
        if prompt_errors:
            details = "\n".join(
                f"- [{item.code}] {item.path}: {item.message}"
                for item in prompt_errors
            )
            raise ValueError(f"Compiled prompt failed self-lint:\n{details}")
    return prompt


def validate_compiled_prompt(
    prompt: str,
    spec: dict[str, Any] | None = None,
    summary_text: str | None = None,
    require_canonical: bool = True,
) -> list[Finding]:
    """Lint the observable contract of a compiled RF-COMPILE-2.0 prompt."""

    findings: list[Finding] = []
    if not string_ok(prompt):
        return [
            Finding(
                "error",
                "prompt.empty",
                "$",
                "Compiled prompt must be a non-empty string.",
            )
        ]
    if prompt.count("[COMPILED_FROM: RF-COMPILE-2.0") != 1:
        add(
            findings,
            "error",
            "prompt.version",
            "$",
            "Prompt must declare RF-COMPILE-2.0 exactly once.",
        )
    marker_match = re.search(
        r"\[COMPILED_FROM: RF-COMPILE-2\.0 \| FIGURESPEC: [^|\]]+ "
        r"\| FIGURE: [^|\]]+ \| SUMMARY_SHA256: ([0-9a-f]{64})\]",
        prompt,
    )
    if marker_match is None:
        add(
            findings,
            "error",
            "prompt.summary-marker",
            "$",
            "Prompt marker must contain a 64-character SUMMARY_SHA256.",
        )

    prior_index = -1
    section_indices: dict[str, int] = {}
    for heading in PROMPT_SECTION_HEADINGS:
        count = prompt.count(heading)
        if count > 1:
            add(
                findings,
                "error",
                "prompt.section.duplicate",
                "$",
                f"Section heading appears {count} times: {heading}",
            )
        index = prompt.find(heading)
        if index < 0:
            add(
                findings,
                "error",
                "prompt.section.missing",
                "$",
                f"Missing required section heading: {heading}",
            )
        elif index <= prior_index:
            add(
                findings,
                "error",
                "prompt.section.order",
                "$",
                f"Section is out of order: {heading}",
            )
        else:
            prior_index = index
            section_indices[heading] = index

    sections: dict[str, str] = {}
    if len(section_indices) == len(PROMPT_SECTION_HEADINGS):
        for index, heading in enumerate(PROMPT_SECTION_HEADINGS):
            start = section_indices[heading] + len(heading)
            end = (
                section_indices[PROMPT_SECTION_HEADINGS[index + 1]]
                if index + 1 < len(PROMPT_SECTION_HEADINGS)
                else len(prompt)
            )
            sections[heading] = prompt[start:end]
            if len(sections[heading].strip()) < 20:
                add(
                    findings,
                    "error",
                    "prompt.section.empty",
                    heading,
                    "Prompt section is empty or only a token stub.",
                )

    placeholders = sorted(set(re.findall(r"\{\{[^{}\n]+\}\}", prompt)))
    for placeholder in placeholders:
        add(
            findings,
            "error",
            "prompt.placeholder.unresolved",
            "$",
            f"Unresolved template placeholder: {placeholder}",
        )

    def require_in(
        section_heading: str,
        phrase: str,
        code: str,
        path: str = "$",
    ) -> None:
        section = sections.get(section_heading, "")
        if phrase.lower() not in section.lower():
            add(
                findings,
                "error",
                code,
                path,
                f"{section_heading} is missing: {phrase!r}",
            )

    construction_heading = PROMPT_SECTION_HEADINGS[9]
    negative_heading = PROMPT_SECTION_HEADINGS[10]
    output_heading = PROMPT_SECTION_HEADINGS[11]
    preflight_heading = PROMPT_SECTION_HEADINGS[12]
    for phrase in ("live editable text", "stable IDs", "Do not flatten"):
        require_in(
            construction_heading,
            phrase,
            "prompt.construction.missing",
        )
    for phrase in (
        "pseudo-",
        "font substitution",
        "missing glyphs",
        "blurred",
        "fuzzy",
        "melted",
        "ghosted",
        "low-resolution upscaling",
        "clipped",
    ):
        require_in(negative_heading, phrase, "prompt.negative.optical-missing")
    for phrase in (
        "final publication size",
        "100%",
        "200%",
        "live text",
    ):
        require_in(preflight_heading, phrase, "prompt.qa.missing")
    for phrase in ("editable master", "preview", "provenance", "audit"):
        require_in(output_heading, phrase, "prompt.output.missing")

    if summary_text is None:
        add(
            findings,
            "error",
            "prompt.summary.required",
            "$",
            "Prompt lint requires the detailed summary artifact.",
        )
    else:
        summary_findings = validate_paper_summary(summary_text, spec)
        findings.extend(summary_findings)
        expected_hash = summary_sha256(summary_text)
        if marker_match is None or marker_match.group(1) != expected_hash:
            add(
                findings,
                "error",
                "prompt.summary-hash.mismatch",
                "$",
                "Prompt SUMMARY_SHA256 does not match the supplied summary.",
            )

    if spec is None:
        return findings
    spec_errors = [item for item in validate_spec(spec) if item.level == "error"]
    if spec_errors:
        add(
            findings,
            "error",
            "prompt.spec.invalid",
            "$",
            "Cannot lint content coverage against an invalid FigureSpec.",
        )
        return findings

    purpose_heading = PROMPT_SECTION_HEADINGS[2]
    narrative_heading = PROMPT_SECTION_HEADINGS[3]
    content_heading = PROMPT_SECTION_HEADINGS[4]
    relation_heading = PROMPT_SECTION_HEADINGS[5]
    layout_heading = PROMPT_SECTION_HEADINGS[6]
    panel_heading = PROMPT_SECTION_HEADINGS[7]
    visual_heading = PROMPT_SECTION_HEADINGS[8]
    reference_heading = PROMPT_SECTION_HEADINGS[1]

    for value, path in (
        (spec["source"]["title"], "$.source.title"),
        (spec["intent"]["role"], "$.intent.role"),
        (spec["intent"]["reader_question"], "$.intent.reader_question"),
        (spec["intent"]["five_second_message"], "$.intent.five_second_message"),
        (spec["intent"]["claim_boundary"], "$.intent.claim_boundary"),
    ):
        require_in(
            purpose_heading,
            str(value),
            "prompt.purpose.missing",
            path,
        )
    for index, claim in enumerate(spec["claims"]):
        for value in (
            claim["id"],
            claim["status"],
            claim["scope"],
            claim["text"],
            claim["source_anchor"] or "MISSING",
            claim["evidence"] or "MISSING",
        ):
            require_in(
                narrative_heading,
                str(value),
                "prompt.claim.missing",
                f"$.claims[{index}]",
            )
    for index, must_show in enumerate(spec["content"]["must_show"]):
        require_in(
            content_heading,
            must_show,
            "prompt.must-show.missing",
            f"$.content.must_show[{index}]",
        )
    for index, exact_text in enumerate(spec["content"]["required_text"]):
        require_in(
            content_heading,
            exact_text,
            "prompt.required-text.missing",
            f"$.content.required_text[{index}]",
        )
    for index, forbidden in enumerate(spec["content"]["must_not_show"]):
        require_in(
            negative_heading,
            forbidden,
            "prompt.negative.missing",
            f"$.content.must_not_show[{index}]",
        )
    for p_index, panel in enumerate(spec["panels"]):
        for value in (
            f"Panel {panel['id']}",
            panel["title"],
            panel["question"],
            panel["visual_form"],
        ):
            require_in(
                panel_heading,
                str(value),
                "prompt.panel.missing",
                f"$.panels[{p_index}]",
            )
        for e_index, entity in enumerate(panel["entities"]):
            for value in (entity["id"], entity["kind"], entity["label"]):
                require_in(
                    content_heading,
                    str(value),
                    "prompt.entity.missing",
                    f"$.panels[{p_index}].entities[{e_index}]",
                )
        for r_index, relation in enumerate(panel["relations"]):
            expected = (
                f"{relation['id']} | {relation['from']} → {relation['to']} "
                f"| type: {relation['type']} | payload/label: "
                f"{relation['label'] or '(none)'}"
            )
            require_in(
                relation_heading,
                expected,
                "prompt.relation.missing",
                f"$.panels[{p_index}].relations[{r_index}]",
            )
    for value in (
        spec["layout"]["topology"],
        spec["layout"]["panel_grid"],
        spec["layout"]["whitespace"],
    ):
        require_in(layout_heading, str(value), "prompt.layout.missing")
    for value in (
        spec["style"]["background"],
        spec["style"]["font"],
        spec["style"]["line_style"],
    ):
        require_in(visual_heading, str(value), "prompt.visual.missing")
    require_in(
        construction_heading,
        spec["render"]["mode"],
        "prompt.renderer.missing",
        "$.render.mode",
    )
    reference = as_dict(spec.get("visual_reference"))
    if reference.get("available"):
        for field in ("use_for", "do_not_copy"):
            for index, item in enumerate(as_list(reference.get(field))):
                target_heading = (
                    reference_heading if field == "use_for" else negative_heading
                )
                require_in(
                    target_heading,
                    str(item),
                    "prompt.reference.missing",
                    f"$.visual_reference.{field}[{index}]",
                )
    if spec["target"]["editable"]:
        require_in(
            output_heading,
            "editable master",
            "prompt.editable.missing",
            "$.target.editable",
        )
    if (
        require_canonical
        and summary_text is not None
        and not any(
            item.level == "error" and item.code.startswith("summary.")
            for item in findings
        )
    ):
        try:
            canonical_prompt = compile_prompt(
                spec,
                summary_text,
                allow_warnings=True,
                _skip_self_lint=True,
            )
        except ValueError as exc:
            add(
                findings,
                "error",
                "prompt.canonical.unavailable",
                "$",
                f"Canonical compiler could not reproduce this contract: {exc}",
            )
        else:
            if prompt != canonical_prompt:
                add(
                    findings,
                    "error",
                    "prompt.noncanonical",
                    "$",
                    (
                        "Prompt differs from the deterministic RF-COMPILE-2.0 "
                        "output for the supplied summary and FigureSpec."
                    ),
                )
    return findings


def inspect_svg(
    svg_path: Path, spec: dict[str, Any] | None = None
) -> list[Finding]:
    """Run structural checks before the mandatory rendered-artifact audit."""

    findings: list[Finding] = []
    try:
        tree = ET.parse(svg_path)
    except FileNotFoundError:
        return [
            Finding("error", "svg.missing", str(svg_path), "SVG file not found.")
        ]
    except ET.ParseError as exc:
        return [
            Finding(
                "error",
                "svg.xml.invalid",
                str(svg_path),
                f"Invalid SVG/XML: {exc}",
            )
        ]
    root = tree.getroot()

    def local_name(tag: str) -> str:
        return tag.rsplit("}", 1)[-1]

    def parse_number(value: str | None) -> float | None:
        if value is None:
            return None
        match = re.match(
            r"^\s*(-?(?:\d+(?:\.\d*)?|\.\d+))(?:px)?\s*$",
            value,
        )
        return float(match.group(1)) if match else None

    def style_map(element: ET.Element) -> dict[str, str]:
        parsed: dict[str, str] = {}
        for declaration in element.get("style", "").split(";"):
            if ":" in declaration:
                key, value = declaration.split(":", 1)
                parsed[key.strip().lower()] = value.strip().lower()
        return parsed

    def attribute_value(element: ET.Element, key: str) -> str | None:
        direct = element.get(key)
        if direct is not None:
            return direct.strip().lower()
        return style_map(element).get(key.lower())

    def raster_dimensions(data: bytes) -> tuple[int, int] | None:
        if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
            return struct.unpack(">II", data[16:24])
        if data.startswith(b"\xff\xd8"):
            offset = 2
            sof_markers = {
                0xC0,
                0xC1,
                0xC2,
                0xC3,
                0xC5,
                0xC6,
                0xC7,
                0xC9,
                0xCA,
                0xCB,
                0xCD,
                0xCE,
                0xCF,
            }
            while offset + 9 < len(data):
                if data[offset] != 0xFF:
                    offset += 1
                    continue
                marker = data[offset + 1]
                offset += 2
                if marker in {0xD8, 0xD9}:
                    continue
                if offset + 2 > len(data):
                    break
                length = int.from_bytes(data[offset : offset + 2], "big")
                if length < 2 or offset + length > len(data):
                    break
                if marker in sof_markers and length >= 7:
                    height = int.from_bytes(data[offset + 3 : offset + 5], "big")
                    width = int.from_bytes(data[offset + 5 : offset + 7], "big")
                    return width, height
                offset += length
        return None

    def image_bytes(href: str) -> bytes | None:
        if href.startswith("data:"):
            header, separator, payload = href.partition(",")
            if not separator or ";base64" not in header.lower():
                return None
            try:
                return base64.b64decode(payload, validate=True)
            except (ValueError, TypeError):
                return None
        if "://" in href:
            return None
        candidate = (svg_path.parent / href).resolve()
        try:
            return candidate.read_bytes()
        except OSError:
            return None

    if local_name(root.tag) != "svg":
        add(
            findings,
            "error",
            "svg.root.invalid",
            "$",
            "Root element must be <svg>.",
        )
        return findings

    view_box: tuple[float, float, float, float] | None = None
    raw_view_box = root.get("viewBox")
    if raw_view_box:
        try:
            values = [float(value) for value in re.split(r"[,\s]+", raw_view_box.strip())]
            if len(values) == 4 and values[2] > 0 and values[3] > 0:
                view_box = (values[0], values[1], values[2], values[3])
            else:
                raise ValueError
        except ValueError:
            add(
                findings,
                "error",
                "svg.viewbox.invalid",
                "$.svg",
                "SVG viewBox must contain four numbers with positive width and height.",
            )
    else:
        add(
            findings,
            "warning",
            "svg.viewbox.missing",
            "$.svg",
            "SVG has no viewBox; scaling and off-canvas checks are unreliable.",
        )

    elements = list(root.iter())
    parent_map = {
        child: parent for parent in elements for child in list(parent)
    }
    ids = [
        element.get("id")
        for element in elements
        if string_ok(element.get("id"))
    ]
    for duplicate in sorted(duplicate_values(ids)):
        add(
            findings,
            "error",
            "svg.id.duplicate",
            "$.svg",
            f"Duplicate editable object ID: {duplicate}",
        )

    blur_elements = [
        element
        for element in elements
        if local_name(element.tag)
        in {"feGaussianBlur", "feConvolveMatrix", "feDisplacementMap"}
    ]
    filtered_elements = [
        element
        for element in elements
        if attribute_value(element, "filter") not in {None, "none"}
    ]
    if blur_elements or filtered_elements:
        add(
            findings,
            "warning",
            "svg.blur-filter",
            "$.svg",
            "SVG contains a blur, convolution, displacement, or filter effect; inspect every affected region at 200%.",
        )

    css_rules: list[tuple[str, dict[str, str]]] = []
    for style_element in (
        element for element in elements if local_name(element.tag) == "style"
    ):
        raw_css = "".join(style_element.itertext())
        for selectors, declarations in re.findall(
            r"([^{}]+)\{([^{}]+)\}", raw_css
        ):
            parsed_declarations: dict[str, str] = {}
            for declaration in declarations.split(";"):
                if ":" in declaration:
                    key, value = declaration.split(":", 1)
                    parsed_declarations[key.strip().lower()] = (
                        value.replace("!important", "").strip().lower()
                    )
            for selector in selectors.split(","):
                if selector.strip():
                    css_rules.append((selector.strip(), parsed_declarations))
    text_elements = [
        element for element in elements if local_name(element.tag) == "text"
    ]

    def ancestry(element: ET.Element) -> list[ET.Element]:
        chain = [element]
        while element in parent_map:
            element = parent_map[element]
            chain.append(element)
        return chain

    def selector_matches(element: ET.Element, selector: str) -> bool:
        """Match the final simple selector in common embedded SVG CSS."""

        simple = re.split(r"[\s>+~]+", selector.strip())[-1]
        simple = re.sub(r":[\w-]+(?:\([^)]*\))?", "", simple)
        if not simple or any(character in simple for character in "[]*"):
            return False
        match = re.fullmatch(
            r"(?P<tag>[A-Za-z_][\w-]*)?"
            r"(?P<id>#[A-Za-z_][\w.-]*)?"
            r"(?P<classes>(?:\.[A-Za-z_][\w-]*)*)",
            simple,
        )
        if match is None:
            return False
        tag = match.group("tag")
        element_id = (match.group("id") or "").lstrip("#")
        classes = {
            item for item in (match.group("classes") or "").split(".") if item
        }
        element_classes = set(element.get("class", "").split())
        return (
            (not tag or local_name(element.tag).lower() == tag.lower())
            and (not element_id or element.get("id") == element_id)
            and classes.issubset(element_classes)
        )

    def effective_value(element: ET.Element, key: str) -> str | None:
        direct = attribute_value(element, key)
        if direct is not None:
            return direct
        value: str | None = None
        for selector, declarations in css_rules:
            if key in declarations and selector_matches(element, selector):
                value = declarations[key]
        return value

    def transform_operations(
        transform: str,
    ) -> list[tuple[str, list[float]]]:
        operations: list[tuple[str, list[float]]] = []
        for name, payload in re.findall(
            r"([A-Za-z]+)\s*\(([^)]*)\)", transform
        ):
            try:
                numbers = [
                    float(value)
                    for value in re.findall(
                        r"-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?",
                        payload,
                    )
                ]
            except ValueError:
                continue
            operations.append((name.lower(), numbers))
        return operations

    def translated_position(element: ET.Element) -> tuple[float | None, float | None]:
        x = parse_number(element.get("x"))
        y = parse_number(element.get("y"))
        dx = parse_number(element.get("dx")) or 0.0
        dy = parse_number(element.get("dy")) or 0.0
        if x is None or y is None:
            for child in element.iter():
                if local_name(child.tag) == "tspan":
                    x = x if x is not None else parse_number(child.get("x"))
                    y = y if y is not None else parse_number(child.get("y"))
                    dx += parse_number(child.get("dx")) or 0.0
                    dy += parse_number(child.get("dy")) or 0.0
                    if x is not None and y is not None:
                        break
        x = (x if x is not None else 0.0) + dx
        y = (y if y is not None else 0.0) + dy
        for node in ancestry(element):
            for name, values in transform_operations(
                node.get("transform", "")
            ):
                if name == "translate" and values:
                    x += values[0]
                    y += values[1] if len(values) > 1 else 0.0
                elif name == "scale" and values:
                    x *= values[0]
                    y *= values[1] if len(values) > 1 else values[0]
                elif name == "matrix" and len(values) >= 6:
                    a, b, c, d, e, f = values[:6]
                    x, y = a * x + c * y + e, b * x + d * y + f
        return x, y

    def transformed_scale(element: ET.Element) -> tuple[float, float]:
        scale_x = 1.0
        scale_y = 1.0
        for node in ancestry(element):
            for name, values in transform_operations(
                node.get("transform", "")
            ):
                if name == "scale" and values:
                    scale_x *= abs(values[0])
                    scale_y *= abs(
                        values[1] if len(values) > 1 else values[0]
                    )
                elif name == "matrix" and len(values) >= 4:
                    a, b, c, d = values[:4]
                    scale_x *= (a * a + b * b) ** 0.5
                    scale_y *= (c * c + d * d) ** 0.5
        return scale_x, scale_y

    def hidden_reason(element: ET.Element) -> str | None:
        chain = ancestry(element)
        for node in chain:
            if local_name(node.tag) in {
                "defs",
                "clipPath",
                "mask",
                "marker",
                "pattern",
                "symbol",
            }:
                return f"inside non-rendered <{local_name(node.tag)}> definition"
            display = effective_value(node, "display")
            visibility = effective_value(node, "visibility")
            opacity = parse_number(effective_value(node, "opacity"))
            fill_opacity = parse_number(effective_value(node, "fill-opacity"))
            font_size = parse_number(effective_value(node, "font-size"))
            if display == "none":
                return "display:none"
            if visibility in {"hidden", "collapse"}:
                return f"visibility:{visibility}"
            if opacity is not None and opacity <= 0:
                return "opacity:0"
            if fill_opacity is not None and fill_opacity <= 0:
                return "fill-opacity:0"
            if font_size is not None and font_size <= 0:
                return "font-size:0"
            if node.get("aria-hidden", "").lower() == "true":
                return "aria-hidden:true"
            transform = node.get("transform", "")
            if re.search(
                r"scale\(\s*0(?:[,\s]+0)?\s*\)",
                transform,
            ):
                return "scale(0)"
        fill = effective_value(element, "fill")
        stroke = effective_value(element, "stroke")
        if fill in {"none", "transparent"} and stroke in {
            None,
            "none",
            "transparent",
        }:
            return f"fill:{fill} with no visible stroke"
        if view_box is not None:
            x, y = translated_position(element)
            min_x, min_y, width, height = view_box
            margin_x = width * 0.05
            margin_y = height * 0.05
            if x is not None and not (
                min_x - margin_x <= x <= min_x + width + margin_x
            ):
                return f"x={x:g} is outside the viewBox"
            if y is not None and not (
                min_y - margin_y <= y <= min_y + height + margin_y
            ):
                return f"y={y:g} is outside the viewBox"
        return None

    visible_fragments: list[str] = []
    missing_font_family = False
    missing_font_size = False
    for element in text_elements:
        fragment = " ".join("".join(element.itertext()).split())
        if not fragment:
            continue
        reason = hidden_reason(element)
        if reason:
            add(
                findings,
                "warning",
                "svg.text.hidden",
                f"$.svg.text[{element.get('id') or fragment[:30]}]",
                f"Live text is not visibly inspectable: {reason}.",
            )
            continue
        visible_fragments.append(fragment)
        chain = ancestry(element)
        has_font_family = any(
            string_ok(effective_value(node, "font-family")) for node in chain
        )
        has_font_size = any(
            (
                parse_number(effective_value(node, "font-size")) is not None
                and parse_number(effective_value(node, "font-size")) > 0
            )
            for node in chain
        )
        missing_font_family = missing_font_family or not has_font_family
        missing_font_size = missing_font_size or not has_font_size
        if any(
            effective_value(node, "clip-path") not in {None, "none"}
            or effective_value(node, "mask") not in {None, "none"}
            for node in chain
        ):
            add(
                findings,
                "warning",
                "svg.text.clip-or-mask",
                f"$.svg.text[{element.get('id') or fragment[:30]}]",
                "Visible text uses a clip path or mask; verify the rendered glyphs are not clipped at 100% and 200%.",
            )

    if missing_font_family:
        add(
            findings,
            "warning",
            "svg.font-family.unspecified",
            "$.svg.text",
            "At least one visible label has no inspectable font-family declaration.",
        )
    if missing_font_size:
        add(
            findings,
            "warning",
            "svg.font-size.unspecified",
            "$.svg.text",
            "At least one visible label has no inspectable positive font-size declaration.",
        )

    visible_text = " ".join(visible_fragments)
    if "\ufffd" in visible_text:
        add(
            findings,
            "error",
            "svg.glyph.replacement",
            "$.svg.text",
            "SVG contains the Unicode replacement character.",
        )
    if any(character in visible_text for character in ("\u25a1", "\u25af")):
        add(
            findings,
            "warning",
            "svg.glyph.tofu",
            "$.svg.text",
            "SVG contains square placeholder glyphs; verify intended symbols and font coverage.",
        )

    image_elements = [
        element for element in elements if local_name(element.tag) == "image"
    ]
    for index, image in enumerate(image_elements):
        href = image.get("href") or image.get(
            "{http://www.w3.org/1999/xlink}href"
        )
        native = raster_dimensions(image_bytes(href) or b"") if href else None
        placed_width = parse_number(image.get("width"))
        placed_height = parse_number(image.get("height"))
        if native is None or placed_width is None or placed_height is None:
            add(
                findings,
                "warning",
                "svg.raster-resolution-unverified",
                f"$.svg.image[{index}]",
                "Raster native or placed dimensions could not be verified; record effective resolution before pass.",
            )
            continue
        transform_scale_x, transform_scale_y = transformed_scale(image)
        effective_width = placed_width * transform_scale_x
        effective_height = placed_height * transform_scale_y
        if effective_width <= 0 or effective_height <= 0:
            add(
                findings,
                "error",
                "svg.raster-hidden",
                f"$.svg.image[{index}]",
                "Raster has zero effective width or height after transforms.",
            )
            continue
        scale_x = effective_width / native[0]
        scale_y = effective_height / native[1]
        if scale_x > 1.01 or scale_y > 1.01:
            add(
                findings,
                "error",
                "svg.raster-upscaled",
                f"$.svg.image[{index}]",
                (
                    f"Raster {native[0]}×{native[1]} is effectively placed at "
                    f"{effective_width:g}×{effective_height:g} SVG units after transforms."
                ),
            )
        else:
            add(
                findings,
                "note",
                "svg.raster-layer",
                f"$.svg.image[{index}]",
                f"Raster layer native dimensions verified as {native[0]}×{native[1]}; effective PPI still requires final-size review.",
            )
        if (
            image.get("preserveAspectRatio") == "none"
            and abs(
                (native[0] / native[1])
                - (effective_width / effective_height)
            )
            > 0.05
        ):
            add(
                findings,
                "warning",
                "svg.raster-distorted",
                f"$.svg.image[{index}]",
                "Raster aspect ratio is distorted by preserveAspectRatio='none'.",
            )

    if spec is not None:
        spec_errors = [
            item for item in validate_spec(spec) if item.level == "error"
        ]
        if spec_errors:
            add(
                findings,
                "error",
                "svg.spec.invalid",
                "$",
                "Cannot inspect SVG against an invalid FigureSpec.",
            )
            return findings
        required_text = spec["content"]["required_text"]
        if required_text and not text_elements:
            add(
                findings,
                "error",
                "svg.live-text.missing",
                "$.svg.text",
                "Required labels exist in FigureSpec but SVG has no live <text> nodes.",
            )
        for index, exact_text in enumerate(required_text):
            normalized = " ".join(exact_text.split())
            if normalized not in visible_text:
                add(
                    findings,
                    "error",
                    "svg.required-text.missing",
                    f"$.content.required_text[{index}]",
                    f"Required visible live text is absent from the SVG: {exact_text!r}",
                )
        if spec["render"]["mode"] == "vector-code" and image_elements:
            add(
                findings,
                "warning",
                "svg.vector-mode.raster",
                "$.svg",
                "vector-code output contains raster layers.",
            )
        if spec["target"]["editable"]:
            entity_ids = {
                entity["id"]
                for panel in spec["panels"]
                for entity in panel["entities"]
            }
            relation_types = {
                relation["id"]: relation["type"]
                for panel in spec["panels"]
                for relation in panel["relations"]
            }
            relation_ids = set(relation_types)
            expected_ids = entity_ids | relation_ids
            missing_ids = sorted(expected_ids - set(ids))
            for stable_id in missing_ids:
                add(
                    findings,
                    "error",
                    "svg.editable.id-missing",
                    "$.svg",
                    f"Required editable entity/relation ID is absent: {stable_id}",
                )
            id_elements = {
                element.get("id"): element
                for element in elements
                if string_ok(element.get("id"))
            }

            def has_visible_geometry(
                root_element: ET.Element, relation_only: bool
            ) -> bool:
                allowed = (
                    {"path", "line", "polyline", "polygon"}
                    if relation_only
                    else {
                        "path",
                        "line",
                        "polyline",
                        "polygon",
                        "rect",
                        "circle",
                        "ellipse",
                        "image",
                        "use",
                        "text",
                    }
                )
                for candidate in root_element.iter():
                    tag = local_name(candidate.tag)
                    if tag not in allowed or hidden_reason(candidate):
                        continue
                    if tag in {"line", "polyline"} and effective_value(
                        candidate, "stroke"
                    ) in {None, "none", "transparent"}:
                        continue
                    if tag == "text" and " ".join(
                        "".join(candidate.itertext()).split()
                    ):
                        return True
                    if tag == "path" and string_ok(candidate.get("d")):
                        return True
                    if tag in {"polyline", "polygon"} and string_ok(
                        candidate.get("points")
                    ):
                        return True
                    if tag == "line" and all(
                        parse_number(candidate.get(key)) is not None
                        for key in ("x1", "y1", "x2", "y2")
                    ):
                        return True
                    if tag == "rect" and (
                        (parse_number(candidate.get("width")) or 0) > 0
                        and (parse_number(candidate.get("height")) or 0) > 0
                    ):
                        return True
                    if tag == "circle" and (
                        parse_number(candidate.get("r")) or 0
                    ) > 0:
                        return True
                    if tag == "ellipse" and (
                        (parse_number(candidate.get("rx")) or 0) > 0
                        and (parse_number(candidate.get("ry")) or 0) > 0
                    ):
                        return True
                    if tag in {"image", "use"} and string_ok(
                        candidate.get("href")
                        or candidate.get(
                            "{http://www.w3.org/1999/xlink}href"
                        )
                    ):
                        return True
                return False

            for stable_id in sorted(expected_ids & set(id_elements)):
                if not has_visible_geometry(
                    id_elements[stable_id],
                    relation_only=(
                        stable_id in relation_ids
                        and relation_types[stable_id] != "containment"
                    ),
                ):
                    add(
                        findings,
                        "error",
                        "svg.editable.id-empty",
                        f"$.svg#{stable_id}",
                        "Required stable ID does not own visible editable geometry.",
                    )
    return findings


def build_audit_template(spec: dict[str, Any]) -> dict[str, Any]:
    findings = validate_spec(spec)
    errors = [finding for finding in findings if finding.level == "error"]
    if errors:
        details = "; ".join(f"{f.code}: {f.message}" for f in errors)
        raise ValueError(f"Cannot create audit template: {details}")
    expected_inventory = expected_inventory_from_spec(spec)
    return {
        "prompt_id": "RF-CRITIQUE-2.0",
        "figure_id": spec["figure_id"],
        "verdict": "pending",
        "reader_inferences": [],
        "visible_inventory": {
            "panels": [],
            "components": [],
            "relations": [],
            "must_show": [],
            "required_text": [],
            "numeric_marks": [],
        },
        "technical_quality": {
            "artifact_inspected": False,
            "artifact_path": "",
            "artifact_format": "",
            "artifact_sha256": "",
            "declared_final_dimensions": "",
            "inspection_notes": "",
            "final_size_checked": False,
            "zoom_100_checked": False,
            "zoom_200_checked": False,
            "editable_source_checked": False,
            "editable_source_path": "",
            "editable_source_sha256": "",
            "live_text_verified": False,
            "blurred_or_soft_regions": [],
            "font_or_glyph_errors": [],
            "overlap_or_clipping": [],
            "rasterization_or_resolution_issues": [],
        },
        "expected_inventory": expected_inventory,
        "scores": {
            "scientific_fidelity": None,
            "structural_correctness": None,
            "role_purity": None,
            "message_clarity": None,
            "readability": None,
            "accessibility": None,
            "editability_reproducibility": None,
        },
        "critical_failures": [],
        "major_issues": [],
        "minor_issues": [],
        "revision_deltas": [],
        "unresolved_evidence": [],
        "new_issues_vs_prior": [],
    }


MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def check_skill_links(skill_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    skill_file = skill_root / "SKILL.md"
    if not skill_file.exists():
        return [
            Finding("error", "skill.missing", str(skill_file), "SKILL.md not found.")
        ]
    skill_text = skill_file.read_text(encoding="utf-8")
    if "TODO" in skill_text:
        add(
            findings,
            "error",
            "skill.todo",
            str(skill_file),
            "SKILL.md contains TODO.",
        )
    if len(skill_text.splitlines()) >= 500:
        add(
            findings,
            "error",
            "skill.length",
            str(skill_file),
            "SKILL.md must stay under 500 lines.",
        )
    if (skill_root / "README.md").exists():
        add(
            findings,
            "error",
            "skill.readme",
            str(skill_root / "README.md"),
            "Keep repository documentation outside the installable skill.",
        )

    linked_paths: set[Path] = set()
    markdown_files = [skill_file, *sorted((skill_root / "references").glob("*.md"))]
    for markdown_file in markdown_files:
        text = markdown_file.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (markdown_file.parent / target).resolve()
            if not resolved.exists():
                add(
                    findings,
                    "error",
                    "link.missing",
                    str(markdown_file),
                    f"Missing linked file: {target}",
                )
            if resolved.parent == (skill_root / "references").resolve():
                linked_paths.add(resolved)

    reference_files = {
        path.resolve() for path in (skill_root / "references").glob("*.md")
    }
    for unlinked in sorted(reference_files - linked_paths):
        add(
            findings,
            "warning",
            "reference.unlinked",
            str(unlinked),
            "Reference is not linked from SKILL.md or another checked reference.",
        )

    required_files = [
        skill_root / "agents" / "openai.yaml",
        skill_root / "assets" / "evidence-ledger.schema.json",
        skill_root / "assets" / "figure-audit.schema.json",
        skill_root / "assets" / "figure-spec.schema.json",
        skill_root / "assets" / "figure-spec.template.json",
        skill_root / "assets" / "paper-summary.template.md",
        skill_root / "assets" / "final-prompt.template.md",
        skill_root / "scripts" / "figure_workbench.py",
    ]
    for required in required_files:
        if not required.exists():
            add(
                findings,
                "error",
                "resource.missing",
                str(required),
                "Required skill resource is missing.",
            )
    return findings


def findings_payload(findings: list[Finding], strict: bool) -> dict[str, Any]:
    errors = sum(f.level == "error" for f in findings)
    warnings = sum(f.level == "warning" for f in findings)
    notes = sum(f.level == "note" for f in findings)
    ok = errors == 0 and (not strict or warnings == 0)
    return {
        "ok": ok,
        "strict": strict,
        "summary": {"errors": errors, "warnings": warnings, "notes": notes},
        "findings": [finding.as_dict() for finding in findings],
    }


def print_findings(findings: list[Finding], strict: bool, as_json: bool) -> bool:
    payload = findings_payload(findings, strict)
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for finding in findings:
            print(
                f"{finding.level.upper():7} {finding.code:32} "
                f"{finding.path}: {finding.message}"
            )
        summary = payload["summary"]
        print(
            f"{'PASS' if payload['ok'] else 'FAIL'}: "
            f"{summary['errors']} error(s), {summary['warnings']} warning(s), "
            f"{summary['notes']} note(s)"
        )
    return bool(payload["ok"])


def cmd_new(args: argparse.Namespace) -> int:
    spec = build_new_spec(args.role)
    text = json.dumps(spec, ensure_ascii=False, indent=2)
    write_text(Path(args.out), text, force=args.force)
    print(f"Created {args.out}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        spec = load_json(Path(args.spec))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    ok = print_findings(validate_spec(spec), args.strict, args.json)
    return 0 if ok else 1


def cmd_validate_artifact(args: argparse.Namespace) -> int:
    try:
        artifact = load_json(Path(args.artifact))
        if args.kind == "evidence-ledger":
            findings = validate_evidence_ledger(artifact)
        elif args.kind == "figure-audit":
            spec = load_json(Path(args.spec)) if args.spec else None
            findings = validate_audit(artifact, spec)
        else:
            raise ValueError(f"Unsupported artifact kind: {args.kind}")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    ok = print_findings(findings, args.strict, args.json)
    return 0 if ok else 1


def cmd_compile(args: argparse.Namespace) -> int:
    try:
        spec = load_json(Path(args.spec))
        summary_text = Path(args.summary).read_text(encoding="utf-8")
        prompt = compile_prompt(
            spec,
            summary_text,
            allow_warnings=args.allow_warnings,
        )
        if args.out:
            write_text(Path(args.out), prompt, force=args.force)
            print(f"Created {args.out}")
        else:
            print(prompt.rstrip())
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


def cmd_lint_prompt(args: argparse.Namespace) -> int:
    try:
        prompt_path = Path(args.prompt)
        prompt = prompt_path.read_text(encoding="utf-8")
        summary_text = Path(args.summary).read_text(encoding="utf-8")
        spec = load_json(Path(args.spec)) if args.spec else None
    except (OSError, UnicodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    ok = print_findings(
        validate_compiled_prompt(prompt, spec, summary_text),
        args.strict,
        args.json,
    )
    return 0 if ok else 1


def cmd_inspect_svg(args: argparse.Namespace) -> int:
    try:
        spec = load_json(Path(args.spec)) if args.spec else None
        findings = inspect_svg(Path(args.svg), spec)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    ok = print_findings(findings, args.strict, args.json)
    return 0 if ok else 1


def cmd_audit_template(args: argparse.Namespace) -> int:
    try:
        spec = load_json(Path(args.spec))
        audit = build_audit_template(spec)
        write_text(
            Path(args.out),
            json.dumps(audit, ensure_ascii=False, indent=2),
            force=args.force,
        )
        print(f"Created {args.out}")
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


def cmd_check_links(args: argparse.Namespace) -> int:
    root = Path(args.skill_root).resolve() if args.skill_root else SKILL_ROOT
    ok = print_findings(check_skill_links(root), args.strict, args.json)
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Work with Research FigureSpec artifacts."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new", help="Create a FigureSpec template.")
    new_parser.add_argument("--role", choices=sorted(ROLES), required=True)
    new_parser.add_argument("--out", required=True)
    new_parser.add_argument("--force", action="store_true")
    new_parser.set_defaults(func=cmd_new)

    validate_parser = subparsers.add_parser(
        "validate", help="Validate schema shape and scientific semantics."
    )
    validate_parser.add_argument("spec")
    validate_parser.add_argument("--strict", action="store_true")
    validate_parser.add_argument("--json", action="store_true")
    validate_parser.set_defaults(func=cmd_validate)

    artifact_parser = subparsers.add_parser(
        "validate-artifact",
        help="Validate an evidence ledger or figure audit artifact.",
    )
    artifact_parser.add_argument(
        "--kind", choices=sorted(ARTIFACT_SCHEMAS), required=True
    )
    artifact_parser.add_argument("artifact")
    artifact_parser.add_argument(
        "--spec", help="FigureSpec used to check figure-audit acceptance thresholds."
    )
    artifact_parser.add_argument("--strict", action="store_true")
    artifact_parser.add_argument("--json", action="store_true")
    artifact_parser.set_defaults(func=cmd_validate_artifact)

    compile_parser = subparsers.add_parser(
        "compile", help="Compile a validated FigureSpec into a production prompt."
    )
    compile_parser.add_argument("spec")
    compile_parser.add_argument(
        "--summary",
        required=True,
        help="Completed paper-summary.md required before prompt compilation.",
    )
    compile_parser.add_argument("--out")
    compile_parser.add_argument("--force", action="store_true")
    compile_parser.add_argument(
        "--allow-warnings",
        action="store_true",
        help="Compile a partial/provisional spec while surfacing validation warnings.",
    )
    compile_parser.set_defaults(func=cmd_compile)

    lint_parser = subparsers.add_parser(
        "lint-prompt",
        help="Lint an RF-COMPILE-2.0 prompt against its summary and FigureSpec.",
    )
    lint_parser.add_argument("prompt")
    lint_parser.add_argument(
        "--spec",
        required=True,
        help="FigureSpec used to check exact text, relations, negatives, and editability.",
    )
    lint_parser.add_argument(
        "--summary",
        required=True,
        help="Detailed summary used to verify the compiled summary hash and anchors.",
    )
    lint_parser.add_argument("--strict", action="store_true")
    lint_parser.add_argument("--json", action="store_true")
    lint_parser.set_defaults(func=cmd_lint_prompt)

    svg_parser = subparsers.add_parser(
        "inspect-svg",
        help="Check SVG editability, exact live text, filters, raster layers, and glyph hazards.",
    )
    svg_parser.add_argument("svg")
    svg_parser.add_argument(
        "--spec",
        required=True,
        help="FigureSpec used to check exact labels, renderer mode, and editability.",
    )
    svg_parser.add_argument("--strict", action="store_true")
    svg_parser.add_argument("--json", action="store_true")
    svg_parser.set_defaults(func=cmd_inspect_svg)

    audit_parser = subparsers.add_parser(
        "audit-template", help="Create an artifact-audit record from FigureSpec."
    )
    audit_parser.add_argument("spec")
    audit_parser.add_argument("--out", required=True)
    audit_parser.add_argument("--force", action="store_true")
    audit_parser.set_defaults(func=cmd_audit_template)

    check_parser = subparsers.add_parser(
        "check-links", help="Check skill resources and relative Markdown links."
    )
    check_parser.add_argument("--skill-root")
    check_parser.add_argument("--strict", action="store_true")
    check_parser.add_argument("--json", action="store_true")
    check_parser.set_defaults(func=cmd_check_links)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
