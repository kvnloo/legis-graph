"""Integration checks for the script's YAML loader and CSV contract."""

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class LegislatorParsingTest(unittest.TestCase):
    def run_parser(self, current, historical):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data_dir = root / "data" / "congress-legislators"
            data_dir.mkdir(parents=True)
            (root / "outputs").mkdir()
            (data_dir / "legislators-current.yaml").write_text(
                current, encoding="utf8"
            )
            (data_dir / "legislators-historical.yaml").write_text(
                historical, encoding="utf8"
            )
            result = subprocess.run(
                [sys.executable, str(REPO_ROOT / "parse_legislators.py")],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            rows = {}
            for kind in ("current", "historical"):
                output = root / "outputs" / f"legislators-{kind}.csv"
                if output.exists():
                    with output.open(newline="", encoding="utf8") as source:
                        rows[kind] = list(csv.DictReader(source))
            return result, rows

    def test_current_and_historical_rows(self):
        current = """
- id: {bioguide: T000001}
  name: {first: Ada, last: Example}
  terms:
    - {state: IL, district: 1, party: Democrat, type: rep}
"""
        historical = """
- id: {bioguide: T000002}
  name: {first: Pat, last: Sample}
  terms:
    - {state: IL, party: Republican, type: sen}
"""
        result, rows = self.run_parser(current, historical)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(rows["current"][0]["bioguideID"], "T000001")
        self.assertEqual(rows["current"][0]["type"], "House")
        self.assertEqual(rows["current"][0]["party"], "democrat")
        self.assertEqual(rows["historical"][0]["type"], "Senate")
        self.assertEqual(rows["historical"][0]["party"], "republican")

    def test_python_specific_yaml_tag_is_not_accepted(self):
        current = "!!python/tuple [a, b]\n"
        result, _ = self.run_parser(current, "[]\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("constructor", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
