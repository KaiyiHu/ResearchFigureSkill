import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "research-figure" / "scripts" / "quick_qa.py"


def write_png_header(path: Path, width: int = 1200, height: int = 800) -> None:
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + b"\x00\x00\x00\rIHDR"
        + struct.pack(">II", width, height)
    )


class QuickQaTests(unittest.TestCase):
    def run_qa(self, svg_text: str, *extra: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            svg = root / "figure.svg"
            png = root / "figure.png"
            svg.write_text(svg_text, encoding="utf-8")
            write_png_header(png)
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(svg), str(png), *extra],
                text=True,
                capture_output=True,
                check=False,
            )

    def test_valid_editable_svg_passes(self) -> None:
        result = self.run_qa(
            """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800">
            <text id="label" x="20" y="40">Exact label</text>
            <rect id="box" x="10" y="60" width="100" height="50"/>
            <circle id="node" cx="180" cy="85" r="20"/>
            <path id="edge" d="M110 85 H160"/>
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
            viewBox="0 0 1200 800">
            <image x="0" y="0" width="1200" height="800" href="figure.png"/>
            <text id="label" x="20" y="40">Editable title</text>
            <rect id="panel" x="10" y="60" width="100" height="50"/>
            <circle id="node" cx="180" cy="85" r="20"/>
            <path id="edge" d="M110 85 H160"/>
            </svg>"""
        rejected = self.run_qa(svg)
        self.assertNotEqual(rejected.returncode, 0)
        accepted = self.run_qa(svg, "--allow-hybrid")
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
        self.assertIn("explicitly allowed for disclosed hybrid", accepted.stdout)


if __name__ == "__main__":
    unittest.main()
