import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "research-figure" / "scripts" / "quick_qa.py"
SKILL = ROOT / "skills" / "research-figure" / "SKILL.md"
PROMPTS = (
    ROOT
    / "skills"
    / "research-figure"
    / "references"
    / "prompt-templates.md"
)
CHANGELOG = ROOT / "CHANGELOG.md"
README_EN = ROOT / "README.md"
README_ZH = ROOT / "README.zh-CN.md"


def independent_renderer_available() -> bool:
    runtime = (
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
    )
    return (
        (runtime / "node" / "bin" / "node").is_file()
        and (runtime / "node" / "node_modules" / "sharp").is_dir()
    )


def write_png_header(path: Path, width: int = 1200, height: int = 800) -> None:
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + b"\x00\x00\x00\rIHDR"
        + struct.pack(">II", width, height)
    )


class QuickQaTests(unittest.TestCase):
    def run_qa(
        self,
        svg_text: str,
        *extra: str,
        render_qa: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            svg = root / "figure.svg"
            png = root / "figure.png"
            svg.write_text(svg_text, encoding="utf-8")
            write_png_header(png)
            args = [sys.executable, str(SCRIPT), str(svg), str(png), *extra]
            if not render_qa:
                args.append("--metadata-only")
            return subprocess.run(
                args,
                text=True,
                capture_output=True,
                check=False,
            )

    def test_valid_editable_svg_passes(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"
              data-safe-box="48 32 1104 736"
              data-bbox-audit="getBBox+getCTM+stroke">
            <text id="label" data-bbox="60 40 120 30"
              x="60" y="65">Exact label</text>
            <rect id="box" data-bbox="60 80 100 50"
              x="60" y="80" width="100" height="50"/>
            <circle id="node" data-bbox="180 85 40 40"
              cx="200" cy="105" r="20"/>
            <path id="edge" data-bbox="160 100 20 10" d="M160 105 H180"/>
            </svg>""",
            "--required-text",
            "Exact label",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS:", result.stdout)

    def test_blur_filter_fails(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800">
            <filter id="blur"><feGaussianBlur stdDeviation="2"/></filter>
            <text x="20" y="40">Exact label</text>
            <rect x="10" y="60" width="100" height="50"/>
            <circle cx="180" cy="85" r="20"/>
            <path d="M110 85 H160"/>
            </svg>"""
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("blur/filter effect", result.stdout)

    def test_disclosed_hybrid_passes_only_with_flag(self) -> None:
        svg = """<svg xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            viewBox="0 0 1200 800" data-safe-box="48 32 1104 736"
            data-bbox-audit="getBBox+getCTM+stroke">
            <image data-role="background" data-allow-outside-safe="true"
              data-bbox="0 0 1200 800" x="0" y="0" width="1200" height="800"
              href="figure.png"/>
            <text id="label" data-bbox="60 40 160 30"
              x="60" y="65">Editable title</text>
            <rect id="panel" data-bbox="60 80 100 50"
              x="60" y="80" width="100" height="50"/>
            <circle id="node" data-bbox="180 85 40 40"
              cx="200" cy="105" r="20"/>
            <path id="edge" data-bbox="160 100 20 10" d="M160 105 H180"/>
            </svg>"""
        rejected = self.run_qa(svg)
        self.assertNotEqual(rejected.returncode, 0)
        accepted = self.run_qa(svg, "--allow-hybrid")
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        self.assertIn("explicitly allowed for disclosed hybrid", accepted.stdout)

    def test_structural_symbol_requires_anchor_metadata(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800">
            <text id="label" x="100" y="100">Grouped stages</text>
            <rect id="box-a" x="100" y="150" width="180" height="100"/>
            <rect id="box-b" x="100" y="280" width="180" height="100"/>
            <path id="bad-bracket" data-role="bracket" d="M300 150 H320 V380 H300"/>
            </svg>"""
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("lacks structural anchor metadata", result.stdout)

    def test_structural_symbol_with_anchor_metadata_passes(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"
              data-safe-box="48 32 1104 736"
              data-bbox-audit="getBBox+getCTM+stroke">
            <text id="label" data-bbox="100 70 180 35"
              x="100" y="100">Grouped stages</text>
            <rect id="box-a" data-bbox="100 150 180 100"
              x="100" y="150" width="180" height="100"/>
            <rect id="box-b" data-bbox="100 280 180 100"
              x="100" y="280" width="180" height="100"/>
            <path id="good-bracket" data-role="bracket"
              data-bbox="300 150 20 230"
              data-target-group="stages" data-target-bbox="100 150 180 230"
              data-side="right" data-span="150 380" data-clearance="20"
              d="M300 150 H320 V380 H300"/>
            </svg>"""
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unprotected_title_fails(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800">
            <path id="arc" d="M250 120 Q600 20 950 120"/>
            <rect id="panel" x="220" y="140" width="760" height="300"/>
            <circle id="node" cx="600" cy="300" r="40"/>
            <g data-role="title-layer" data-clear-zone="360 30 480 100">
              <text id="main-title" data-role="title"
                data-bbox="400 55 400 40" x="400" y="90">Count-aware probe</text>
            </g>
            </svg>"""
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("lacks a matching title-mask", result.stdout)

    def test_last_title_layer_with_full_mask_passes(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"
              data-safe-box="48 32 1104 736"
              data-bbox-audit="getBBox+getCTM+stroke">
            <path id="arc" data-bbox="250 80 700 70"
              d="M250 150 Q600 80 950 150"/>
            <rect id="panel" data-bbox="220 170 760 300"
              x="220" y="170" width="760" height="300"/>
            <circle id="node" data-bbox="560 260 80 80"
              cx="600" cy="300" r="40"/>
            <g data-role="title-layer" data-clear-zone="366 35 468 80">
              <rect data-role="title-mask" data-target="main-title"
                data-bbox="366 35 468 80" x="366" y="35" width="468"
                height="80" fill="#fffdf7"/>
              <text id="main-title" data-role="title"
                data-bbox="400 55 400 40" x="400" y="90">Count-aware probe</text>
            </g>
            </svg>"""
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_text_outside_safe_box_fails(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"
              data-safe-box="48 32 1104 736">
            <text id="overflow" data-bbox="20 740 300 40"
              x="20" y="775">Footer outside the safe area</text>
            <rect data-bbox="60 80 100 50" x="60" y="80"
              width="100" height="50"/>
            <circle data-bbox="180 85 40 40" cx="200" cy="105" r="20"/>
            <path data-bbox="160 100 20 10" d="M160 105 H180"/>
            </svg>"""
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("overflows data-safe-box", result.stdout)

    def test_missing_renderer_bbox_audit_fails(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"
              data-safe-box="48 32 1104 736">
            <text id="label" data-bbox="60 40 120 30"
              x="60" y="65">Exact label</text>
            <rect data-bbox="60 80 100 50" x="60" y="80"
              width="100" height="50"/>
            <circle data-bbox="180 85 40 40" cx="200" cy="105" r="20"/>
            <path data-bbox="160 100 20 10" d="M160 105 H180"/>
            </svg>"""
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("lacks data-bbox-audit", result.stdout)

    def test_text_outside_panel_content_box_fails(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"
              data-safe-box="48 32 1104 736">
            <g id="footer" data-role="footer" data-bbox="60 500 1080 220"
              data-content-box="90 530 1020 140">
              <rect x="60" y="500" width="1080" height="220"/>
              <text id="footer-note" data-bbox="100 650 900 40"
                x="100" y="685">Text crosses the footer border</text>
              <circle cx="100" cy="560" r="10"/>
              <path d="M120 560 H180"/>
            </g>
            </svg>"""
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("overflows footer footer content box", result.stdout)

    def test_connector_label_without_bridge_fails(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"
              data-safe-box="48 32 1104 736"
              data-bbox-audit="getBBox+getCTM+stroke">
            <text id="same-x" data-role="connector-label"
              data-bbox="500 300 100 30" x="500" y="325">same x</text>
            <rect data-bbox="60 80 100 50" x="60" y="80"
              width="100" height="50"/>
            <circle data-bbox="180 85 40 40" cx="200" cy="105" r="20"/>
            <path data-bbox="160 100 20 10" d="M160 105 H180"/>
            </svg>"""
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("is not inside a declared bridge", result.stdout)

    def test_connector_label_inside_bridge_corridor_passes(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"
              data-safe-box="48 32 1104 736"
              data-bbox-audit="getBBox+getCTM+stroke">
            <g id="bridge-a-b" data-role="bridge"
              data-bridge-from="panel-a" data-bridge-to="panel-b"
              data-corridor-box="500 260 160 100" data-bbox="500 260 160 100">
              <text id="same-x" data-role="connector-label"
                data-bbox="530 290 100 30" x="530" y="315">same x</text>
              <rect x="520" y="280" width="120" height="50"/>
              <circle cx="510" cy="330" r="10"/>
              <path d="M500 330 H520"/>
            </g>
            </svg>"""
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    @unittest.skipUnless(
        independent_renderer_available(),
        "independent SVG renderer not available",
    )
    def test_renderer_rejects_false_declared_text_bbox(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"
              data-safe-box="48 32 1104 736"
              data-bbox-audit="getBBox+getCTM+stroke">
            <g id="panel-a" data-role="panel" data-bbox="80 80 250 140"
              data-content-box="100 100 200 80">
              <rect x="80" y="80" width="250" height="140"/>
              <text id="false-safe" data-bbox="100 110 80 30"
                x="100" y="140" font-size="30">This rendered label is much too wide</text>
              <circle cx="120" cy="180" r="10"/>
              <path d="M140 180 H180"/>
            </g>
            </svg>""",
            render_qa=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sharp: false-safe overflows panel panel-a", result.stdout)
        self.assertIn(
            "declared bbox does not contain independently rendered pixels",
            result.stdout,
        )

    @unittest.skipUnless(
        independent_renderer_available(),
        "independent SVG renderer not available",
    )
    def test_independent_renderer_accepts_contained_pixels(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"
              data-safe-box="48 32 1104 736"
              data-bbox-audit="getBBox+getCTM+stroke">
            <g id="panel-ok" data-role="panel" data-bbox="80 80 300 160"
              data-content-box="95 95 270 120">
              <rect x="80" y="80" width="300" height="160"/>
              <text id="label-ok" data-bbox="100 100 100 50"
                x="105" y="135" font-size="24">OK</text>
              <circle cx="120" cy="190" r="10"/>
              <path d="M140 190 H180"/>
            </g>
            </svg>""",
            render_qa=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("independent pixel QA: sharp", result.stdout)

    def test_skill_requires_safe_area_balance_and_existing_figure_choice(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        agent_prompt = (
            ROOT / "skills" / "research-figure" / "agents" / "openai.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("leading AI-conference figures", skill)
        self.assertIn("Figure type: Motivation, Pipeline, or both?", skill)
        self.assertIn("completely replace it", skill)
        self.assertIn("use it as a reference and improve it", skill)
        self.assertIn("strict isolation", skill)
        self.assertIn("without image inputs or recent-image carryover", skill)
        self.assertIn("native editable PowerPoint objects", skill)
        self.assertIn("at least 36 pt for the slide title", skill)
        self.assertIn("20 pt", skill)
        self.assertIn("18 pt for connector labels", skill)
        self.assertIn("reject all figure footnotes", skill)
        self.assertIn("normally 3–5", skill)
        self.assertIn("Preserve the original visual system", skill)
        self.assertIn("rounded dashed semantic regions", skill)
        self.assertIn("Do not let overflow safeguards redefine the style", skill)
        self.assertIn("semantic overflow", skill)
        self.assertIn("ARROW_STYLE_TOKENS", skill)
        self.assertIn("one native connected object for the shaft and head", skill)
        self.assertIn("never assemble a separate triangle and line", skill)
        self.assertIn("attach endpoints to named shape ports", skill)
        self.assertIn("create connectors before nodes", skill)
        self.assertIn("render_slides.py", skill)
        self.assertIn("slides_test.py", skill)
        self.assertIn("image-viewing tool", skill)
        self.assertIn("visible defect fails", skill)
        self.assertIn("4–6% outer safe area", skill)
        self.assertIn("regenerate independently and ignore it", skill)
        self.assertIn("original Research Figure Prompt Template", agent_prompt)
        self.assertIn("style-faithful primary", agent_prompt)
        self.assertIn("faithful editable PPTX companion", agent_prompt)
        self.assertIn("$research-figure", agent_prompt)
        self.assertIn("Default deliverables are", skill)
        self.assertIn("SVG is not a default deliverable", skill)

    def test_original_prompt_template_is_the_immutable_core(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        prompts = PROMPTS.read_text(encoding="utf-8")
        changelog = CHANGELOG.read_text(encoding="utf-8")
        self.assertIn("Original Research Figure Prompt Template", prompts)
        self.assertIn("Do **not**", prompts)
        self.assertIn(
            "Use the supplied reference figure as the PRIMARY visual and compositional",
            prompts,
        )
        self.assertIn("closely preserve the reference image's distinctive", prompts)
        self.assertIn("hand-drawn academic", prompts)
        self.assertIn("Do not redesign it as a modern corporate diagram", prompts)
        self.assertIn("immediately look like another figure produced", prompts)
        self.assertIn("SCIENTIFIC TOPIC", prompts)
        self.assertIn("Main centered title:", prompts)
        self.assertIn("The overall scientific narrative is:", prompts)
        self.assertIn("REFERENCE-ALIGNED GLOBAL LAYOUT", prompts)
        self.assertIn("Maintain almost exactly the same high-level composition", prompts)
        self.assertIn("large black hand-lettered text", prompts)
        self.assertIn("white-background rounded", prompts)
        self.assertIn("Negative Prompt: Sleek corporate infographic", prompts)
        self.assertIn("Nature-style polished vector", prompts)
        self.assertIn("ultra-clean geometric sans-serif", prompts)
        self.assertIn("Hierarchical Skill Mining Pipeline", prompts)
        self.assertIn("49–51%", prompts)
        self.assertNotIn("STRICT REVIEWER PREFLIGHT", prompts)
        self.assertNotIn("EDITABLE COMPANION", prompts)
        self.assertNotIn("PowerPoint reconstruction and visual QA happen afterward", prompts.split("## Renderer-facing master template", 1)[1].split("## Fill card", 1)[0])
        self.assertIn("PowerPoint SmartArt", skill)
        self.assertIn("Original Research Figure Prompt Template", skill)
        self.assertIn("without paraphrasing", skill)
        self.assertIn("must end after", skill)
        self.assertIn("Never append PowerPoint", skill)
        self.assertIn("primary PNG as a complete scientific figure", skill)
        self.assertIn("with the declared title", skill)
        self.assertIn("faithful editable companion", skill)
        self.assertIn("approved primary PNG is the aesthetic reference", skill)
        self.assertIn("all six gates pass", skill)
        self.assertIn("## 1.0", changelog)
        self.assertNotIn("## 2.", changelog)

    def test_usage_notice_documents_scope_and_current_limits(self) -> None:
        english = README_EN.read_text(encoding="utf-8")
        chinese = README_ZH.read_text(encoding="utf-8")
        for text in (english, chinese):
            self.assertIn("Codex", text)
            self.assertIn("Claude Code", text)
            self.assertIn("Motivation", text)
            self.assertIn("Pipeline", text)
            self.assertIn("SVG", text)
            self.assertIn("PPTX", text)
            self.assertIn("PNG", text)
        self.assertIn("latest capable GPT model", english)
        self.assertIn("input → core processing → output", english)
        self.assertIn("will not perfectly reproduce", english)
        self.assertIn("最新 GPT", chinese)
        self.assertIn("输入 → 核心处理 → 输出", chinese)
        self.assertIn("无法完全复现", chinese)


if __name__ == "__main__":
    unittest.main()
