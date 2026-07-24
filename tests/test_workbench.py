from __future__ import annotations

import copy
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

PROMPT_FIXTURES = [
    (
        REPO_ROOT / "examples" / "claimcrawl" / "motivation-spec.json",
        REPO_ROOT / "examples" / "claimcrawl" / "motivation-spec-prompt.md",
    ),
    (
        REPO_ROOT / "examples" / "claimcrawl" / "method-spec.json",
        REPO_ROOT / "examples" / "claimcrawl" / "method-spec-prompt.md",
    ),
    (
        REPO_ROOT / "examples" / "method-pipeline" / "figure-spec.json",
        REPO_ROOT / "examples" / "method-pipeline" / "figure-spec-prompt.md",
    ),
    (
        REPO_ROOT / "examples" / "quantitative-result" / "figure-spec.json",
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


class FigureWorkbenchTests(unittest.TestCase):
    def test_schema_and_template_are_valid_json(self) -> None:
        schema = load(SKILL_ROOT / "assets" / "figure-spec.schema.json")
        template = load(SKILL_ROOT / "assets" / "figure-spec.template.json")
        self.assertEqual(schema["title"], "Research FigureSpec")
        self.assertEqual(template["schema_version"], "1.0")
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
        first = workbench.compile_prompt(spec)
        second = workbench.compile_prompt(copy.deepcopy(spec))
        self.assertEqual(first, second)
        self.assertIn(
            "Panel A: crawler | kind: process | exact label: Crawler", first
        )
        self.assertIn("Known source limitations:", first)

    def test_checked_in_prompts_match_compiler(self) -> None:
        for spec_path, prompt_path in PROMPT_FIXTURES:
            with self.subTest(spec=spec_path):
                expected = prompt_path.read_text(encoding="utf-8")
                self.assertEqual(workbench.compile_prompt(load(spec_path)), expected)

    def test_compile_preserves_exact_quantitative_values_and_constraints(self) -> None:
        spec = load(REPO_ROOT / "examples" / "quantitative-result" / "figure-spec.json")
        prompt = workbench.compile_prompt(spec)
        self.assertIn("74.8, 72.1, and 75.4", prompt)
        self.assertIn("Mean ± 1 SD", prompt)
        self.assertIn("Do not infer significance.", prompt)
        self.assertIn("Mode: plot-code", prompt)
        self.assertNotIn("Mode: image-generation", prompt)

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

    def test_evidence_ledger_passes_and_supported_claims_need_anchors(self) -> None:
        path = REPO_ROOT / "examples" / "claimcrawl" / "evidence-ledger.json"
        ledger = load(path)
        self.assertEqual(workbench.validate_evidence_ledger(ledger), [])
        ledger["claims"][0]["source_anchor"] = ""
        codes = {
            item.code for item in workbench.validate_evidence_ledger(ledger)
        }
        self.assertIn("evidence.anchor.missing", codes)

    def test_new_quantitative_spec_routes_to_plot_code(self) -> None:
        spec = workbench.build_new_spec("experiment")
        self.assertEqual(spec["render"]["mode"], "plot-code")
        self.assertTrue(spec["render"]["deterministic_numbers"])

    def test_unicode_labels_survive_compilation(self) -> None:
        spec = load(EXAMPLE_SPECS[2])
        spec["content"]["required_text"].append("覆盖率 Δ")
        prompt = workbench.compile_prompt(spec)
        self.assertIn("覆盖率 Δ", prompt)

    def test_compile_blocks_invalid_spec(self) -> None:
        spec = load(EXAMPLE_SPECS[1])
        spec["panels"][0]["relations"][0]["from"] = "missing"
        with self.assertRaisesRegex(ValueError, "validation errors"):
            workbench.compile_prompt(spec)

    def test_compile_blocks_provisional_warnings_by_default(self) -> None:
        spec = workbench.build_new_spec("method")
        with self.assertRaisesRegex(ValueError, "validation warnings"):
            workbench.compile_prompt(spec)
        prompt = workbench.compile_prompt(spec, allow_warnings=True)
        self.assertIn("KNOWN VALIDATION WARNINGS", prompt)

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
