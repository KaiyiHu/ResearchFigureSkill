from __future__ import annotations

import copy
import hashlib
import html
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "research-figure"
MODULE_PATH = SKILL_ROOT / "scripts" / "figure_workbench.py"
SPEC = importlib.util.spec_from_file_location("figure_workbench", MODULE_PATH)
assert SPEC and SPEC.loader
workbench = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = workbench
SPEC.loader.exec_module(workbench)


EXAMPLE_SPECS = [
    REPO_ROOT / "examples" / "claimcrawl" / "motivation-spec.json",
    REPO_ROOT / "examples" / "claimcrawl" / "method-spec.json",
    REPO_ROOT / "examples" / "method-pipeline" / "figure-spec.json",
    REPO_ROOT / "examples" / "quantitative-result" / "figure-spec.json",
]

EXAMPLE_SUMMARIES = [
    REPO_ROOT / "examples" / "claimcrawl" / "paper-summary.md",
    REPO_ROOT / "examples" / "claimcrawl" / "paper-summary.md",
    REPO_ROOT / "examples" / "method-pipeline" / "paper-summary.md",
    REPO_ROOT / "examples" / "quantitative-result" / "paper-summary.md",
]

PROMPT_FIXTURES = [
    (
        REPO_ROOT / "examples" / "claimcrawl" / "motivation-spec.json",
        REPO_ROOT / "examples" / "claimcrawl" / "paper-summary.md",
        REPO_ROOT / "examples" / "claimcrawl" / "motivation-spec-prompt.md",
    ),
    (
        REPO_ROOT / "examples" / "claimcrawl" / "method-spec.json",
        REPO_ROOT / "examples" / "claimcrawl" / "paper-summary.md",
        REPO_ROOT / "examples" / "claimcrawl" / "method-spec-prompt.md",
    ),
    (
        REPO_ROOT / "examples" / "method-pipeline" / "figure-spec.json",
        REPO_ROOT / "examples" / "method-pipeline" / "paper-summary.md",
        REPO_ROOT / "examples" / "method-pipeline" / "figure-spec-prompt.md",
    ),
    (
        REPO_ROOT / "examples" / "quantitative-result" / "figure-spec.json",
        REPO_ROOT / "examples" / "quantitative-result" / "paper-summary.md",
        REPO_ROOT / "examples" / "quantitative-result" / "figure-spec-prompt.md",
    ),
]

AUDIT_FIXTURES = [
    (
        REPO_ROOT / "examples" / "claimcrawl" / "motivation-spec.json",
        REPO_ROOT / "examples" / "claimcrawl" / "motivation-audit.template.json",
    ),
    (
        REPO_ROOT / "examples" / "claimcrawl" / "method-spec.json",
        REPO_ROOT / "examples" / "claimcrawl" / "method-audit.template.json",
    ),
    (
        REPO_ROOT / "examples" / "method-pipeline" / "figure-spec.json",
        REPO_ROOT / "examples" / "method-pipeline" / "figure-audit.template.json",
    ),
    (
        REPO_ROOT / "examples" / "quantitative-result" / "figure-spec.json",
        REPO_ROOT
        / "examples"
        / "quantitative-result"
        / "figure-audit.template.json",
    ),
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def summary(index: int) -> str:
    return EXAMPLE_SUMMARIES[index].read_text(encoding="utf-8")


def build_valid_svg(
    spec: dict,
    text_modes: dict[int, str] | None = None,
) -> str:
    text_modes = text_modes or {}
    entity_elements = []
    relation_elements = []
    for panel in spec["panels"]:
        for entity in panel["entities"]:
            entity_elements.append(
                f'<g id="{html.escape(entity["id"], quote=True)}">'
                '<rect x="1" y="1" width="8" height="8"/></g>'
            )
        for relation in panel["relations"]:
            relation_elements.append(
                f'<path id="{html.escape(relation["id"], quote=True)}" '
                'd="M 10 10 L 20 20"/>'
            )

    label_elements = []
    for index, label in enumerate(spec["content"]["required_text"]):
        mode = text_modes.get(index)
        x = "9999" if mode == "offcanvas" else "10"
        extra = {
            "hidden": ' display="none"',
            "dx-offcanvas": ' dx="9999"',
        }.get(mode, "")
        label_elements.append(
            f'<text id="label-{index}" x="{x}" y="{20 + index * 20}" '
            f'font-family="Arial" font-size="12"{extra}>'
            f"{html.escape(label)}</text>"
        )

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240">'
        '<g id="panel-A">'
        + "".join(entity_elements)
        + "".join(relation_elements)
        + "".join(label_elements)
        + "</g></svg>"
    )


def build_passing_audit(spec: dict, artifact_path: Path) -> dict:
    audit = workbench.build_audit_template(spec)
    digest = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
    audit["verdict"] = "pass"
    audit["visible_inventory"].update(
        {
            field: copy.deepcopy(audit["expected_inventory"][field])
            for field in (
                "panels",
                "components",
                "relations",
                "must_show",
                "required_text",
            )
        }
    )
    audit["reader_inferences"] = [
        {
            "text": claim["text"],
            "status": "supported",
            "visual_cue": f"Visible evidence for {claim['id']}",
            "source_anchor": claim["source_anchor"],
        }
        for claim in spec["claims"]
        if claim["status"] == "supported"
    ]
    for dimension, threshold in spec["acceptance"]["minimum_scores"].items():
        audit["scores"][dimension] = threshold
    audit["technical_quality"].update(
        {
            "artifact_inspected": True,
            "artifact_path": str(artifact_path),
            "artifact_format": "svg",
            "artifact_sha256": digest,
            "declared_final_dimensions": "400 × 240 px at final publication size",
            "inspection_notes": (
                "Inspected the complete export at final size, 100%, and 200%; "
                "all required labels, paths, and edges were crisp and visible."
            ),
            "final_size_checked": True,
            "zoom_100_checked": True,
            "zoom_200_checked": True,
            "editable_source_checked": True,
            "editable_source_path": str(artifact_path),
            "editable_source_sha256": digest,
            "live_text_verified": True,
        }
    )
    return audit


class FigureWorkbenchTests(unittest.TestCase):
    def test_schema_and_template_are_valid_json(self) -> None:
        schema = load(SKILL_ROOT / "assets" / "figure-spec.schema.json")
        template = load(SKILL_ROOT / "assets" / "figure-spec.template.json")
        self.assertEqual(schema["title"], "Research FigureSpec")
        self.assertEqual(template["schema_version"], "2.0")
        self.assertIn("title", template["content"])
        self.assertIn("visual_reference", template)
        self.assertEqual(workbench.validate_schema_shape(template, schema), [])
        for name in ("evidence-ledger.schema.json", "figure-audit.schema.json"):
            self.assertIsInstance(load(SKILL_ROOT / "assets" / name), dict)

    def test_schema_rejects_unknown_fields(self) -> None:
        spec = load(EXAMPLE_SPECS[1])
        spec["render"]["imaginary_provider_setting"] = True
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertIn("schema.additionalProperties", codes)

    def test_all_examples_pass_strict_semantic_validation(self) -> None:
        for path in EXAMPLE_SPECS:
            with self.subTest(path=path):
                findings = workbench.validate_spec(load(path))
                blocking = [
                    finding
                    for finding in findings
                    if finding.level in {"error", "warning"}
                ]
                self.assertEqual(blocking, [])

    def test_compile_is_deterministic(self) -> None:
        spec = load(EXAMPLE_SPECS[1])
        summary_text = summary(1)
        first = workbench.compile_prompt(spec, summary_text)
        second = workbench.compile_prompt(copy.deepcopy(spec), summary_text)
        self.assertEqual(first, second)
        self.assertIn("[COMPILED_FROM: RF-COMPILE-2.0", first)
        self.assertIn(
            f"SUMMARY_SHA256: {workbench.summary_sha256(summary_text)}", first
        )
        self.assertIn(
            "Panel A: crawler | kind: process | exact label: Crawler", first
        )
        self.assertIn("Panel A: R1 | crawler → selector", first)
        self.assertIn("Known source limitations:", first)
        expected_headings = (
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
        self.assertEqual(workbench.PROMPT_SECTION_HEADINGS, expected_headings)
        positions = [
            first.index(heading) for heading in expected_headings
        ]
        self.assertEqual(positions, sorted(positions))

    def test_checked_in_prompts_match_compiler(self) -> None:
        for spec_path, summary_path, prompt_path in PROMPT_FIXTURES:
            with self.subTest(spec=spec_path):
                expected = prompt_path.read_text(encoding="utf-8")
                self.assertEqual(
                    workbench.compile_prompt(
                        load(spec_path),
                        summary_path.read_text(encoding="utf-8"),
                    ),
                    expected,
                )

    def test_compile_preserves_exact_quantitative_values_and_constraints(self) -> None:
        spec = load(REPO_ROOT / "examples" / "quantitative-result" / "figure-spec.json")
        prompt = workbench.compile_prompt(spec, summary(3))
        self.assertIn("74.8, 72.1, and 75.4", prompt)
        self.assertIn("Mean ± 1 SD", prompt)
        self.assertIn("Do not infer significance.", prompt)
        self.assertIn("Renderer mode: plot-code", prompt)
        self.assertNotIn("Renderer mode: image-generation", prompt)
        self.assertIn("blurred, fuzzy, melted, ghosted", prompt)
        self.assertIn("font substitution, missing glyphs", prompt)

    def test_supported_claim_requires_anchor(self) -> None:
        spec = load(EXAMPLE_SPECS[1])
        spec["claims"][0]["source_anchor"] = ""
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertIn("claim.anchor.missing", codes)

    def test_missing_claim_cannot_enter_panel(self) -> None:
        spec = load(EXAMPLE_SPECS[1])
        spec["claims"][0]["status"] = "missing"
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertIn("panel.claim.missing", codes)

    def test_hypothesis_requires_visible_epistemic_label(self) -> None:
        spec = load(EXAMPLE_SPECS[1])
        spec["claims"][0]["status"] = "hypothesis"
        spec["claims"][0]["scope"] = "causal"
        spec["panels"][0]["relations"][0]["type"] = "causal-hypothesis"
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertIn("panel.claim.epistemic-label", codes)
        self.assertIn("relation.causal-hypothesis.invalid", codes)
        spec["claims"][0]["visual_label"] = "Hypothesized relation"
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertNotIn("panel.claim.epistemic-label", codes)
        self.assertNotIn("relation.causal-hypothesis.invalid", codes)

    def test_causal_edge_requires_supported_causal_claim(self) -> None:
        spec = load(EXAMPLE_SPECS[1])
        relation = spec["panels"][0]["relations"][0]
        relation["type"] = "causal"
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertIn("relation.causal.unsupported", codes)

        spec["claims"][0]["scope"] = "causal"
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertNotIn("relation.causal.unsupported", codes)

    def test_relation_endpoint_must_exist(self) -> None:
        spec = load(EXAMPLE_SPECS[1])
        spec["panels"][0]["relations"][0]["to"] = "invented-module"
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertIn("relation.endpoint.unknown", codes)

    def test_relation_ids_are_required_and_unique(self) -> None:
        spec = load(EXAMPLE_SPECS[2])
        del spec["panels"][0]["relations"][0]["id"]
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertIn("schema.required", codes)

        spec = load(EXAMPLE_SPECS[2])
        spec["panels"][0]["relations"][1]["id"] = spec["panels"][0]["relations"][0][
            "id"
        ]
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertIn("relation.id.duplicate", codes)

    def test_quantitative_role_rejects_image_generation(self) -> None:
        spec = load(REPO_ROOT / "examples" / "quantitative-result" / "figure-spec.json")
        spec["render"]["mode"] = "image-generation"
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertIn("render.numeric-imagegen", codes)
        self.assertIn("render.quantitative-imagegen", codes)

    def test_required_text_rejects_pure_image_generation(self) -> None:
        spec = load(EXAMPLE_SPECS[1])
        spec["render"]["mode"] = "image-generation"
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertIn("render.text-imagegen", codes)

    def test_audit_template_maps_expected_inventory(self) -> None:
        spec = load(EXAMPLE_SPECS[2])
        audit = workbench.build_audit_template(spec)
        self.assertEqual(audit["figure_id"], spec["figure_id"])
        self.assertEqual(audit["expected_inventory"]["panels"], ["A"])
        self.assertIn("C1", audit["expected_inventory"]["claims"])
        self.assertEqual(audit["reader_inferences"], [])
        self.assertFalse(audit["technical_quality"]["artifact_inspected"])
        self.assertEqual(audit["technical_quality"]["font_or_glyph_errors"], [])
        self.assertIsNone(audit["scores"]["scientific_fidelity"])
        errors = [
            item
            for item in workbench.validate_audit(audit, spec)
            if item.level == "error"
        ]
        self.assertEqual(errors, [])

    def test_checked_in_audit_templates_match_builder(self) -> None:
        for spec_path, audit_path in AUDIT_FIXTURES:
            with self.subTest(spec=spec_path):
                self.assertEqual(
                    workbench.build_audit_template(load(spec_path)),
                    load(audit_path),
                )

    def test_passing_audit_cannot_have_empty_scores(self) -> None:
        spec = load(EXAMPLE_SPECS[2])
        audit = workbench.build_audit_template(spec)
        audit["verdict"] = "pass"
        codes = {item.code for item in workbench.validate_audit(audit, spec)}
        self.assertIn("audit.pass.score", codes)
        self.assertIn("audit.pass.technical-check", codes)

    def test_passing_audit_requires_completed_optical_checks_and_no_defects(
        self,
    ) -> None:
        spec = load(EXAMPLE_SPECS[2])
        with tempfile.TemporaryDirectory() as directory:
            artifact_path = Path(directory) / "figure.svg"
            artifact_path.write_text(build_valid_svg(spec), encoding="utf-8")
            audit = build_passing_audit(spec, artifact_path)
            self.assertEqual(
                audit["visible_inventory"]["relations"],
                audit["expected_inventory"]["relations"],
            )
            self.assertEqual(
                {
                    item["source_anchor"] for item in audit["reader_inferences"]
                },
                {
                    claim["source_anchor"]
                    for claim in spec["claims"]
                    if claim["status"] == "supported"
                },
            )
            errors = [
                item
                for item in workbench.validate_audit(audit, spec)
                if item.level == "error"
            ]
            self.assertEqual(errors, [])

            defect_fields = {
                "blurred_or_soft_regions": "Panel A is fuzzy at 200%.",
                "font_or_glyph_errors": "A label contains pseudo-text.",
                "overlap_or_clipping": "The right label is clipped.",
                "rasterization_or_resolution_issues": "A raster is visibly upscaled.",
            }
            for field, defect in defect_fields.items():
                with self.subTest(field=field):
                    defective = copy.deepcopy(audit)
                    defective["technical_quality"][field].append(defect)
                    codes = {
                        item.code
                        for item in workbench.validate_audit(defective, spec)
                    }
                    self.assertIn("audit.pass.technical-defect", codes)

    def test_passing_audit_rejects_fabrication_no_spec_and_artifact_mismatch(
        self,
    ) -> None:
        spec = load(EXAMPLE_SPECS[2])
        fabricated = workbench.build_audit_template(spec)
        fabricated["verdict"] = "pass"
        for dimension in fabricated["scores"]:
            fabricated["scores"][dimension] = 5
        codes = {
            item.code for item in workbench.validate_audit(fabricated, spec)
        }
        self.assertIn("audit.pass.technical-evidence", codes)
        self.assertIn("audit.pass.inventory-missing", codes)
        self.assertIn("audit.pass.inferences-empty", codes)

        with tempfile.TemporaryDirectory() as directory:
            artifact_path = Path(directory) / "figure.svg"
            artifact_path.write_text(build_valid_svg(spec), encoding="utf-8")
            audit = build_passing_audit(spec, artifact_path)

            codes = {item.code for item in workbench.validate_audit(audit)}
            self.assertIn("audit.pass.spec-required", codes)

            mismatched = copy.deepcopy(audit)
            mismatched["technical_quality"]["artifact_sha256"] = "0" * 64
            codes = {
                item.code for item in workbench.validate_audit(mismatched, spec)
            }
            self.assertIn("audit.pass.sha256-mismatch", codes)

            wrong_inventory = copy.deepcopy(audit)
            wrong_inventory["expected_inventory"]["relations"] = []
            codes = {
                item.code
                for item in workbench.validate_audit(wrong_inventory, spec)
            }
            self.assertIn("audit.expected-inventory.mismatch", codes)

    def test_passing_audit_rejects_non_pdf_bytes_named_pdf(self) -> None:
        spec = load(EXAMPLE_SPECS[2])
        with tempfile.TemporaryDirectory() as directory:
            editable_path = Path(directory) / "figure.svg"
            editable_path.write_text(build_valid_svg(spec), encoding="utf-8")
            fake_pdf_path = Path(directory) / "figure.pdf"
            fake_variants = (
                b"plain text wearing a PDF filename",
                b"%PDF-1.7\nthis is not a PDF object graph\n%%EOF\n",
            )
            for fake_pdf_bytes in fake_variants:
                with self.subTest(fake_pdf_bytes=fake_pdf_bytes):
                    fake_pdf_path.write_bytes(fake_pdf_bytes)
                    audit = build_passing_audit(spec, editable_path)
                    audit["technical_quality"].update(
                        {
                            "artifact_path": str(fake_pdf_path),
                            "artifact_format": "pdf",
                            "artifact_sha256": hashlib.sha256(
                                fake_pdf_bytes
                            ).hexdigest(),
                        }
                    )
                    codes = {
                        item.code
                        for item in workbench.validate_audit(audit, spec)
                    }
                    self.assertIn(
                        "audit.pass.artifact-signature",
                        codes,
                    )

            pdf = bytearray(b"%PDF-1.4\n")
            offsets = [0]
            for object_bytes in (
                b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
                b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
                b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 10 10] >>\nendobj\n",
            ):
                offsets.append(len(pdf))
                pdf.extend(object_bytes)
            xref_offset = len(pdf)
            pdf.extend(b"xref\n0 4\n0000000000 65535 f \n")
            for offset in offsets[1:]:
                pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
            pdf.extend(
                (
                    "trailer\n<< /Size 4 /Root 1 0 R >>\n"
                    f"startxref\n{xref_offset}\n%%EOF\n"
                ).encode("ascii")
            )
            valid_pdf_path = Path(directory) / "valid.pdf"
            valid_pdf_path.write_bytes(pdf)
            self.assertIsNone(
                workbench.artifact_signature_error(valid_pdf_path, "pdf")
            )

    def test_evidence_ledger_passes_and_supported_claims_need_anchors(self) -> None:
        path = REPO_ROOT / "examples" / "claimcrawl" / "evidence-ledger.json"
        ledger = load(path)
        self.assertEqual(workbench.validate_evidence_ledger(ledger), [])
        ledger["claims"][0]["source_anchor"] = ""
        codes = {
            item.code for item in workbench.validate_evidence_ledger(ledger)
        }
        self.assertIn("evidence.anchor.missing", codes)

    def test_empty_production_ledger_and_spec_are_rejected(self) -> None:
        ledger = load(
            REPO_ROOT / "examples" / "claimcrawl" / "evidence-ledger.json"
        )
        ledger["source_map"] = []
        ledger["claims"] = []
        ledger["paper_thesis"] = ""
        codes = {
            item.code for item in workbench.validate_evidence_ledger(ledger)
        }
        self.assertIn("schema.minItems", codes)
        self.assertIn("schema.minLength", codes)

        spec = workbench.build_new_spec("method")
        with self.assertRaisesRegex(
            ValueError,
            "requires at least one claim, one panel, and one must_show item",
        ):
            workbench.compile_prompt(spec, summary(1), allow_warnings=True)

    def test_new_quantitative_spec_routes_to_plot_code(self) -> None:
        spec = workbench.build_new_spec("experiment")
        self.assertEqual(spec["render"]["mode"], "plot-code")
        self.assertTrue(spec["render"]["deterministic_numbers"])

    def test_unicode_labels_survive_compilation(self) -> None:
        spec = load(EXAMPLE_SPECS[2])
        spec["content"]["required_text"].append("覆盖率 Δ")
        prompt = workbench.compile_prompt(spec, summary(2))
        self.assertIn("覆盖率 Δ", prompt)

    def test_compile_blocks_invalid_spec(self) -> None:
        spec = load(EXAMPLE_SPECS[1])
        spec["panels"][0]["relations"][0]["from"] = "missing"
        with self.assertRaisesRegex(ValueError, "validation errors"):
            workbench.compile_prompt(spec, summary(1))

    def test_compile_blocks_provisional_warnings_by_default(self) -> None:
        spec = load(EXAMPLE_SPECS[1])
        spec["source"]["scope"] = []
        with self.assertRaisesRegex(ValueError, "validation warnings"):
            workbench.compile_prompt(spec, summary(1))
        prompt = workbench.compile_prompt(
            spec,
            summary(1),
            allow_warnings=True,
        )
        self.assertIn("Known validation warnings", prompt)

    def test_reference_contract_and_region_percentages_survive_compilation(
        self,
    ) -> None:
        spec = load(EXAMPLE_SPECS[2])
        spec["visual_reference"] = {
            "available": True,
            "source": "reference.png",
            "mode": "abstract-attributes",
            "use_for": [
                "one wide left region and two stacked right regions",
                "dashed rounded region borders",
            ],
            "do_not_copy": [
                "reference scientific labels",
                "reference logos and branding",
                "distinctive icon drawings",
            ],
        }
        spec["layout"]["regions"] = [
            {
                "id": "left",
                "purpose": "main transformation",
                "x_pct": 3,
                "y_pct": 14,
                "w_pct": 48,
                "h_pct": 76,
            }
        ]
        prompt = workbench.compile_prompt(spec, summary(2))
        self.assertIn("Reference available: true", prompt)
        self.assertIn("dashed rounded region borders", prompt)
        self.assertIn(
            "Region left: purpose=main transformation | x=3%, y=14%, width=48%, height=76%",
            prompt,
        )

    def test_reference_and_region_contract_rejects_empty_or_zero_values(
        self,
    ) -> None:
        spec = load(EXAMPLE_SPECS[2])
        spec["visual_reference"] = {
            "available": True,
            "source": "reference.png",
            "mode": "abstract-attributes",
            "use_for": ["layout rhythm"],
            "do_not_copy": [],
        }
        spec["layout"]["regions"] = [
            {
                "id": "left",
                "purpose": "main transformation",
                "x_pct": 3,
                "y_pct": 14,
                "w_pct": 0,
                "h_pct": 76,
            }
        ]
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertIn("schema.minItems", codes)
        self.assertIn("schema.exclusiveMinimum", codes)

    def test_reference_contract_rejects_unsafe_use_and_incomplete_boundaries(
        self,
    ) -> None:
        spec = load(EXAMPLE_SPECS[2])
        unsafe_instructions = [
            (
                "clone the reference pixel-for-pixel, including its "
                "wording and artwork"
            ),
            "recreate the layout topology one-to-one",
            "一模一样地复刻参考图的布局拓扑",
            "与参考图保持一模一样的布局拓扑",
            "照着参考图原封不动地做同样的布局拓扑",
        ]
        for instruction in unsafe_instructions:
            with self.subTest(instruction=instruction):
                candidate = copy.deepcopy(spec)
                candidate["visual_reference"] = {
                    "available": True,
                    "source": "reference.png",
                    "mode": "abstract-attributes",
                    "use_for": [instruction],
                    "do_not_copy": [
                        "reference scientific labels and values",
                        "reference logos and branding",
                        "distinctive icon drawings and expression",
                    ],
                }
                codes = {
                    finding.code
                    for finding in workbench.validate_spec(candidate)
                }
                self.assertIn("reference.use-for.unsafe", codes)

        spec["visual_reference"] = {
            "available": True,
            "source": "reference.png",
            "mode": "abstract-attributes",
            "use_for": ["layout rhythm"],
            "do_not_copy": ["reference labels"],
        }
        codes = {finding.code for finding in workbench.validate_spec(spec)}
        self.assertIn("reference.copy-boundary.incomplete", codes)

    def test_prompt_linter_rejects_placeholders_and_missing_inventory(self) -> None:
        spec = load(EXAMPLE_SPECS[2])
        summary_text = summary(2)
        prompt = (
            workbench.compile_prompt(spec, summary_text)
            + "\n{{UNRESOLVED}}\n"
        )
        codes = {
            finding.code
            for finding in workbench.validate_compiled_prompt(
                prompt,
                spec,
                summary_text,
            )
        }
        self.assertIn("prompt.placeholder.unresolved", codes)

        exact_text = spec["content"]["required_text"][-1]
        prompt = workbench.compile_prompt(spec, summary_text).replace(
            exact_text, "REMOVED"
        )
        codes = {
            finding.code
            for finding in workbench.validate_compiled_prompt(
                prompt,
                spec,
                summary_text,
            )
        }
        self.assertIn("prompt.required-text.missing", codes)

    def test_prompt_linter_rejects_noncanonical_section_local_bag(self) -> None:
        spec = load(EXAMPLE_SPECS[2])
        summary_text = summary(2)
        canonical = workbench.compile_prompt(spec, summary_text)
        content_heading = workbench.PROMPT_SECTION_HEADINGS[4]
        local_tokens = [
            *spec["content"]["must_show"],
            *spec["content"]["required_text"],
            *(
                value
                for panel in spec["panels"]
                for entity in panel["entities"]
                for value in (
                    entity["id"],
                    entity["kind"],
                    entity["label"],
                )
            ),
        ]
        section_local_bag = (
            "\n\nSection-local inventory bag: "
            + " | ".join(local_tokens)
        )
        noncanonical = canonical.replace(
            content_heading,
            content_heading + section_local_bag,
            1,
        )
        error_codes = {
            finding.code
            for finding in workbench.validate_compiled_prompt(
                noncanonical,
                spec,
                summary_text,
            )
            if finding.level == "error"
        }
        self.assertEqual(error_codes, {"prompt.noncanonical"})

    def test_prompt_linter_rejects_duplicate_headings_and_token_dump_omissions(
        self,
    ) -> None:
        spec = load(EXAMPLE_SPECS[2])
        summary_text = summary(2)
        prompt = workbench.compile_prompt(spec, summary_text)

        duplicated = prompt + "\n" + workbench.PROMPT_SECTION_HEADINGS[0] + "\n"
        codes = {
            finding.code
            for finding in workbench.validate_compiled_prompt(
                duplicated,
                spec,
                summary_text,
            )
        }
        self.assertIn("prompt.section.duplicate", codes)

        exact_text = spec["content"]["required_text"][-1]
        content_heading = workbench.PROMPT_SECTION_HEADINGS[4]
        relation_heading = workbench.PROMPT_SECTION_HEADINGS[5]
        start = prompt.index(content_heading)
        end = prompt.index(relation_heading)
        content_section = prompt[start:end].replace(exact_text, "REMOVED")
        token_dump = prompt[:start] + content_section + prompt[end:]
        token_dump += f"\nDetached token dump: {exact_text}\n"
        codes = {
            finding.code
            for finding in workbench.validate_compiled_prompt(
                token_dump,
                spec,
                summary_text,
            )
        }
        self.assertIn("prompt.required-text.missing", codes)

    def test_summary_template_requires_full_paper_coverage(self) -> None:
        text = (
            SKILL_ROOT / "assets" / "paper-summary.template.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "Executive summary",
            "Method",
            "Experimental design",
            "Negative",
            "Limitations",
            "Section coverage",
            "Figure portfolio",
        ):
            self.assertIn(phrase, text)

    def test_completed_summaries_pass_and_missing_or_broken_summaries_fail(
        self,
    ) -> None:
        for index, spec_path in enumerate(EXAMPLE_SPECS):
            with self.subTest(spec=spec_path):
                spec = load(spec_path)
                self.assertEqual(
                    workbench.validate_paper_summary(summary(index), spec),
                    [],
                )

        spec = load(EXAMPLE_SPECS[2])
        summary_text = summary(2)
        with self.assertRaisesRegex(ValueError, "Detailed paper summary"):
            workbench.compile_prompt(spec, "")

        missing_section = summary_text.replace("## 5. Method", "## 5. Removed", 1)
        codes = {
            finding.code
            for finding in workbench.validate_paper_summary(
                missing_section,
                spec,
            )
        }
        self.assertIn("summary.section.missing", codes)

        missing_anchor = summary_text.replace(
            spec["claims"][0]["source_anchor"],
            "removed source anchor",
        )
        codes = {
            finding.code
            for finding in workbench.validate_paper_summary(
                missing_anchor,
                spec,
            )
        }
        self.assertIn("summary.anchor.missing", codes)

        prompt = workbench.compile_prompt(spec, summary_text)
        changed_summary = summary_text + "\nAdditional validated context.\n"
        codes = {
            finding.code
            for finding in workbench.validate_compiled_prompt(
                prompt,
                spec,
                changed_summary,
            )
        }
        self.assertIn("prompt.summary-hash.mismatch", codes)
        codes = {
            finding.code
            for finding in workbench.validate_compiled_prompt(prompt, spec)
        }
        self.assertIn("prompt.summary.required", codes)

    def test_repetitive_boilerplate_summary_is_rejected(self) -> None:
        boilerplate = (
            "method evidence analysis result source scope "
            "method evidence analysis result source scope "
        )
        sections = []
        for heading in workbench.SUMMARY_REQUIRED_HEADINGS:
            sections.append(heading)
            for sentinel in workbench.SUMMARY_SECTION_SENTINELS.get(
                heading, ()
            ):
                sections.append(f"{sentinel} {boilerplate}")
            sections.append(boilerplate * 30)
        codes = {
            finding.code
            for finding in workbench.validate_paper_summary(
                "\n\n".join(sections)
            )
        }
        self.assertIn("summary.detail.repetitive", codes)
        self.assertIn("summary.section.repetitive", codes)

    def test_svg_inspector_checks_live_text_and_blur_filters(self) -> None:
        spec = load(EXAMPLE_SPECS[2])
        clean_svg = build_valid_svg(spec)
        blurred_svg = clean_svg.replace(
            '<g id="panel-A">',
            (
                '<defs><filter id="soft">'
                '<feGaussianBlur stdDeviation="2"/></filter></defs>'
                '<g id="panel-A" filter="url(#soft)">'
            ),
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            clean_path = Path(directory) / "clean.svg"
            blur_path = Path(directory) / "blur.svg"
            clean_path.write_text(clean_svg, encoding="utf-8")
            blur_path.write_text(blurred_svg, encoding="utf-8")
            blocking = [
                item
                for item in workbench.inspect_svg(clean_path, spec)
                if item.level in {"error", "warning"}
            ]
            self.assertEqual(blocking, [])
            codes = {
                item.code for item in workbench.inspect_svg(blur_path, spec)
            }
            self.assertIn("svg.blur-filter", codes)

    def test_svg_inspector_rejects_hidden_offcanvas_and_upscaled_raster_content(
        self,
    ) -> None:
        spec = load(EXAMPLE_SPECS[2])
        one_pixel_png = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8"
            "/x8AAusB9Y9Zl1EAAAAASUVORK5CYII="
        )
        stretched_raster = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            f'<image href="data:image/png;base64,{one_pixel_png}" '
            'width="100" height="100"/></svg>'
        )
        transformed_raster = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            f'<image href="data:image/png;base64,{one_pixel_png}" '
            'width="1" height="1" transform="scale(100)"/></svg>'
        )
        with tempfile.TemporaryDirectory() as directory:
            for mode in ("hidden", "offcanvas", "dx-offcanvas"):
                with self.subTest(mode=mode):
                    path = Path(directory) / f"{mode}.svg"
                    path.write_text(
                        build_valid_svg(spec, {0: mode}),
                        encoding="utf-8",
                    )
                    codes = {
                        item.code for item in workbench.inspect_svg(path, spec)
                    }
                    self.assertIn("svg.text.hidden", codes)
                    self.assertIn("svg.required-text.missing", codes)

            raster_path = Path(directory) / "stretched.svg"
            raster_path.write_text(stretched_raster, encoding="utf-8")
            codes = {
                item.code for item in workbench.inspect_svg(raster_path)
            }
            self.assertIn("svg.raster-upscaled", codes)

            transformed_path = Path(directory) / "transformed.svg"
            transformed_path.write_text(
                transformed_raster,
                encoding="utf-8",
            )
            codes = {
                item.code for item in workbench.inspect_svg(transformed_path)
            }
            self.assertIn("svg.raster-upscaled", codes)

    def test_svg_inspector_requires_stable_relation_ids(self) -> None:
        spec = load(EXAMPLE_SPECS[2])
        svg = build_valid_svg(spec)
        missing_relation = spec["panels"][0]["relations"][0]["id"]
        svg = svg.replace(f'id="{missing_relation}"', 'id="removed-relation"', 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing-relation.svg"
            path.write_text(svg, encoding="utf-8")
            findings = workbench.inspect_svg(path, spec)
        self.assertTrue(
            any(
                item.code == "svg.editable.id-missing"
                and missing_relation in item.message
                for item in findings
            )
        )

    def test_svg_inspector_rejects_empty_entity_and_relation_groups(
        self,
    ) -> None:
        spec = load(EXAMPLE_SPECS[2])
        entity_id = spec["panels"][0]["entities"][0]["id"]
        relation_id = spec["panels"][0]["relations"][0]["id"]
        valid_svg = build_valid_svg(spec)
        cases = {
            entity_id: valid_svg.replace(
                (
                    f'<g id="{html.escape(entity_id, quote=True)}">'
                    '<rect x="1" y="1" width="8" height="8"/></g>'
                ),
                f'<g id="{html.escape(entity_id, quote=True)}"></g>',
                1,
            ),
            relation_id: valid_svg.replace(
                (
                    f'<path id="{html.escape(relation_id, quote=True)}" '
                    'd="M 10 10 L 20 20"/>'
                ),
                f'<g id="{html.escape(relation_id, quote=True)}"></g>',
                1,
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            for stable_id, svg in cases.items():
                with self.subTest(stable_id=stable_id):
                    path = Path(directory) / f"empty-{stable_id}.svg"
                    path.write_text(svg, encoding="utf-8")
                    findings = workbench.inspect_svg(path, spec)
                    self.assertTrue(
                        any(
                            item.code == "svg.editable.id-empty"
                            and item.path == f"$.svg#{stable_id}"
                            for item in findings
                        )
                    )

    def test_cli_refuses_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "spec.json"
            workbench.write_text(path, "first")
            with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
                workbench.write_text(path, "second")

    def test_skill_links_and_resources_are_complete(self) -> None:
        findings = workbench.check_skill_links(SKILL_ROOT)
        blocking = [
            finding
            for finding in findings
            if finding.level in {"error", "warning"}
        ]
        self.assertEqual(blocking, [])

    def test_repository_markdown_links_resolve(self) -> None:
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        failures = []
        for markdown in REPO_ROOT.rglob("*.md"):
            for raw_target in link_pattern.findall(
                markdown.read_text(encoding="utf-8")
            ):
                target = raw_target.split("#", 1)[0].strip()
                if (
                    not target
                    or "://" in target
                    or target.startswith("mailto:")
                    or target.startswith("<")
                ):
                    continue
                resolved = (markdown.parent / target).resolve()
                if not resolved.exists():
                    failures.append(f"{markdown.relative_to(REPO_ROOT)} -> {target}")
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
