#!/usr/bin/env python3
"""Deterministic FigureSpec scaffolding, validation, prompt compilation, and QA.

This module intentionally has no third-party dependencies. The bundled JSON
Schema supports editor integration; this script adds scientific semantic checks
that generic schema validators cannot express.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
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
        "Generate editable vector geometry or native diagram objects. Keep text "
        "as text nodes. Preserve stable IDs, endpoints, arrowheads, grouping, "
        "and alignment deterministically. Return editable source plus SVG/PDF "
        "preview."
    ),
    "plot-code": (
        "Generate geometry from the supplied machine-readable data. Preserve "
        "values, units, signs, category order, uncertainty, and missing values. "
        "Do not infer significance. Return plotting source, editable SVG/PDF, "
        "and a preview."
    ),
    "image-generation": (
        "Generate only the inventoried conceptual base illustration. Do not "
        "render exact values, axes, tables, equations, citations, or long "
        "required labels. Reserve negative space for deterministic text overlay "
        "and return a draft for compositing and audit."
    ),
    "hybrid": (
        "Render plots, equations, labels, arrows, and core geometry "
        "deterministically. Use image generation only for named illustration "
        "assets. Assemble layers in an editable composition and preserve a "
        "source manifest."
    ),
}


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
        return validate_schema_shape(
            value, _resolve_schema_ref(root, schema["$ref"]), root, path
        )

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

    if isinstance(value, list):
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

    if audit["verdict"] == "pending":
        add(
            findings,
            "warning",
            "audit.pending",
            "$.verdict",
            "The audit has not been completed.",
        )
    if audit["verdict"] == "pass":
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
        for index, inference in enumerate(audit["reader_inferences"]):
            if inference["status"] != "supported":
                add(
                    findings,
                    "error",
                    "audit.pass.inference",
                    f"$.reader_inferences[{index}].status",
                    "A passing audit cannot retain a non-supported reader inference.",
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

    if spec.get("schema_version") != "1.0":
        add(
            findings,
            "error",
            "schema.version",
            "$.schema_version",
            "Only FigureSpec schema_version 1.0 is supported.",
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
            for key in ("from", "to", "type", "label"):
                if key not in relation:
                    add(
                        findings,
                        "error",
                        "field.required",
                        relation_path,
                        f"Missing relation.{key}.",
                    )
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
    spec: dict[str, Any], allow_warnings: bool = False
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

    intent = spec["intent"]
    role = intent["role"]
    render = spec["render"]
    claims = spec["claims"]
    content = spec["content"]
    layout = spec["layout"]
    target = spec["target"]
    style = spec["style"]

    claim_lines = []
    for claim in claims:
        suffix = (
            f" | visual label: {claim['visual_label']}"
            if claim.get("visual_label")
            else ""
        )
        claim_lines.append(
            f"{claim['id']} [{claim['status']}/{claim['scope']}] "
            f"{claim['text']} | source: {claim['source_anchor'] or 'MISSING'}"
            f" | evidence: {claim['evidence'] or 'MISSING'}"
            f"{suffix}"
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
                f"Panel {panel['id']}: {relation['from']} → {relation['to']} "
                f"| type: {relation['type']} | label: "
                f"{relation['label'] or '(none)'}{claim_suffix}"
            )

    color_semantics = "; ".join(
        f"{color}={meaning}" for color, meaning in style["color_semantics"].items()
    )
    risk_section = (
        "\nKNOWN VALIDATION WARNINGS\n"
        + "\n".join(f"- [{f.code}] {f.message}" for f in warnings)
        + "\n"
        if warnings
        else ""
    )

    return f"""[COMPILED_FROM: RF-COMPILE-1.0 | FIGURESPEC: {spec['schema_version']} | FIGURE: {spec['figure_id']}]

SCIENTIFIC OBJECTIVE
Role: {role}
Reader question: {intent['reader_question']}
Five-second message: {intent['five_second_message']}
Claim boundary: {intent['claim_boundary']}

TRUTH AND PROVENANCE CONTRACT
- Render only the supplied scientific inventory.
- Do not invent or strengthen claims, values, equations, labels, or relations.
- Preserve epistemic qualifiers and source-bounded scope.
- If an instruction cannot be rendered faithfully, omit decoration and report the unresolved item; never substitute plausible content.
- Source scope: {', '.join(spec['source']['scope']) or 'not specified'}
- Known source limitations: {', '.join(spec['source']['limitations']) or 'none recorded'}

CLAIM INVENTORY
{format_bullets(claim_lines)}

COMPONENT AND REQUIRED-TEXT INVENTORY
Must show:
{format_bullets(content['must_show'])}

Semantic entities:
{format_bullets(entity_lines)}

Required exact text:
{format_bullets(content['required_text'])}

Optional; remove before compressing required content:
{format_bullets(content['nice_to_show'])}

RELATION INVENTORY
{format_bullets(relation_lines)}

PANEL AND LAYOUT PLAN
{format_bullets(panel_lines)}
- Topology: {layout['topology']}
- Reading order: {', '.join(layout['reading_order']) or 'not specified'}
- Hierarchy: {' > '.join(layout['hierarchy'])}
- Panel grid: {layout['panel_grid']}
- Whitespace: {layout['whitespace']}
- Maximum label words: {layout['max_label_words']}

ROLE-SPECIFIC DIRECTIVE
{ROLE_DEFAULTS[role]['adapter']}

RENDERER-SPECIFIC DIRECTIVE
Mode: {render['mode']}
{RENDERER_ADAPTERS[render['mode']]}

STYLE BOUNDS
- Background: {style['background']}
- Palette: {', '.join(style['palette'])}
- Color semantics: {color_semantics or 'none specified'}
- Font: {style['font']}
- Line style: {style['line_style']}
- Avoid: {', '.join(style['avoid']) or 'none specified'}
- Do not rely on color alone for any scientific distinction.

FORBIDDEN CONTENT
{format_bullets(content['must_not_show'])}
- No decorative entity may resemble an additional scientific component.
- No unlabeled arrow, pseudo-equation, fake number, fake citation, watermark, venue logo, or celebratory badge.

OUTPUT CONTRACT
- Medium/venue: {target['medium']} / {target['venue']}
- Audience/language: {target['audience']} / {target['language']}
- Final size: {target['size']}
- Preferred/fallback format: {render['preferred_format']} / {render['fallback_format']}
- Editable required: {str(target['editable']).lower()}
- Deterministic text/numbers: {str(render['deterministic_text']).lower()} / {str(render['deterministic_numbers']).lower()}
- Data source: {render['data_source'] or 'none'}
- External provider allowed: {str(render['external_provider_allowed']).lower()}
{risk_section}
PREFLIGHT CHECKLIST
[ ] Every required component appears exactly once unless repetition is specified.
[ ] Every relation has correct endpoints, direction, type, and label.
[ ] Every required label is exact and legible at final size.
[ ] No extra scientific entity, value, or claim appears.
[ ] Visual hierarchy makes the five-second message dominant.
[ ] The claim boundary cannot be misread from arrows, scale, or color.
"""


def build_audit_template(spec: dict[str, Any]) -> dict[str, Any]:
    findings = validate_spec(spec)
    errors = [finding for finding in findings if finding.level == "error"]
    if errors:
        details = "; ".join(f"{f.code}: {f.message}" for f in errors)
        raise ValueError(f"Cannot create audit template: {details}")
    critical_checks = as_list(as_dict(spec.get("acceptance")).get("critical_checks"))
    return {
        "prompt_id": "RF-CRITIQUE-1.0",
        "figure_id": spec["figure_id"],
        "verdict": "pending",
        "reader_inferences": [],
        "visible_inventory": {
            "panels": [],
            "components": [],
            "relations": [],
            "required_text": [],
            "numeric_marks": [],
        },
        "expected_inventory": {
            "panels": [panel["id"] for panel in spec["panels"]],
            "claims": [claim["id"] for claim in spec["claims"]],
            "required_text": spec["content"]["required_text"],
            "critical_checks": critical_checks,
        },
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
        prompt = compile_prompt(spec, allow_warnings=args.allow_warnings)
        if args.out:
            write_text(Path(args.out), prompt, force=args.force)
            print(f"Created {args.out}")
        else:
            print(prompt.rstrip())
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


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
    compile_parser.add_argument("--out")
    compile_parser.add_argument("--force", action="store_true")
    compile_parser.add_argument(
        "--allow-warnings",
        action="store_true",
        help="Compile a partial/provisional spec while surfacing validation warnings.",
    )
    compile_parser.set_defaults(func=cmd_compile)

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
