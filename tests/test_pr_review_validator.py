#!/usr/bin/env python3
"""Tests for skills/pr-review/scripts/validate_pr_review.py and the pr-review/v1 schema. Stdlib only."""
import copy
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PR = ROOT / "skills" / "pr-review"
SCRIPT = PR / "scripts" / "validate_pr_review.py"
SAMPLE = PR / "references" / "sample-reply.md"

spec = importlib.util.spec_from_file_location("validate_pr_review", SCRIPT)
val = importlib.util.module_from_spec(spec)
spec.loader.exec_module(val)


def sample_doc():
    block = val.FENCE.findall(SAMPLE.read_text(encoding="utf-8"))[-1]
    return json.loads(block)


def reply(doc, prose="Thank you.\n\n"):
    return prose + "```json pr-review/v1\n" + json.dumps(doc, indent=1) + "\n```\n"


class TestValidator(unittest.TestCase):
    def errs(self, mutate):
        doc = copy.deepcopy(sample_doc())
        mutate(doc)
        return val.validate_text(reply(doc))

    def test_sample_reply_is_valid(self):
        self.assertEqual(val.validate_text(SAMPLE.read_text(encoding="utf-8")), [])

    def test_cli_exit_codes(self):
        ok = subprocess.run([sys.executable, str(SCRIPT), str(SAMPLE)], capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stdout)
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad-reply.md"
            bad.write_text("no block here", encoding="utf-8")
            r = subprocess.run([sys.executable, str(SCRIPT), str(bad)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertIn("no fenced block", r.stdout)

    def test_template_has_labelled_block(self):
        tpl = (PR / "templates" / "CONTRIBUTOR_REPLY_TEMPLATE.md").read_text(encoding="utf-8")
        self.assertTrue(val.FENCE.search(tpl))

    def test_last_block_wins(self):
        text = reply({"schema": "nope"}) + reply(sample_doc(), prose="")
        self.assertEqual(val.validate_text(text), [])

    def test_missing_required_field(self):
        self.assertTrue(any("missing required 'head_sha'" in e for e in self.errs(lambda d: d.pop("head_sha"))))

    def test_bad_verdict_and_severity(self):
        def m(d):
            d["verdict"] = "lgtm"
            d["findings"][0]["severity"] = "huge"
        e = self.errs(m)
        self.assertTrue(any("verdict" in x for x in e) and any("severity" in x for x in e))

    def test_unknown_property_rejected(self):
        self.assertTrue(any("unknown property" in e for e in self.errs(lambda d: d.update(extra=1))))

    def test_bad_finding_id_pattern(self):
        self.assertTrue(any("findings[0].id" in e for e in self.errs(lambda d: d["findings"][0].update(id="bug1"))))

    def test_line_must_be_positive_int_or_null(self):
        self.assertTrue(self.errs(lambda d: d["findings"][0].update(line=0)))
        self.assertTrue(self.errs(lambda d: d["findings"][0].update(line="12")))
        self.assertEqual(self.errs(lambda d: d["findings"][0].update(line=None)), [])

    def test_bool_is_not_integer(self):
        self.assertTrue(self.errs(lambda d: d["pr"].update(number=True)))

    def test_duplicate_ids(self):
        self.assertTrue(any("duplicate id" in e for e in self.errs(lambda d: d["findings"].append(copy.deepcopy(d["findings"][0])))))

    def test_approve_with_blocking_is_inconsistent(self):
        self.assertTrue(any("approve but blocking" in e for e in self.errs(lambda d: d.update(verdict="approve"))))

    def test_changes_requested_needs_blocking(self):
        def m(d):
            for f in d["findings"]:
                f["blocking"] = False
                f["severity"] = "low"
        self.assertTrue(any("needs at least one blocking" in e for e in self.errs(m)))

    def test_needs_info_needs_question(self):
        def m(d):
            d["verdict"] = "needs_info"
            d["findings"] = []
            d["questions"] = []
        self.assertTrue(any("needs_info" in e for e in self.errs(m)))

    def test_high_severity_must_block(self):
        self.assertTrue(any("must be blocking" in e for e in self.errs(lambda d: d["findings"][0].update(blocking=False))))

    def test_invalid_json_reported(self):
        self.assertTrue(any("not valid JSON" in e for e in val.validate_text("```json pr-review/v1\n{oops\n```\n")))

    def test_schema_ids_match_documented_pattern(self):
        schema = json.loads((PR / "references" / "pr-review-v1.schema.json").read_text(encoding="utf-8"))
        pat = schema["properties"]["findings"]["items"]["properties"]["id"]["pattern"]
        self.assertTrue(re.match(pat, "EGR-preview-csp-open-connect"))
        self.assertFalse(re.match(pat, "EGR-1"))


if __name__ == "__main__":
    unittest.main()
