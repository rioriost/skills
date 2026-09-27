"""Offline regressions use invented prose, not copies of Apple documentation."""

import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import fetch_apple_hig as reader


def paragraph(text):
    return {"type": "paragraph", "inlineContent": [{"type": "text", "text": text}]}


def document(*blocks):
    return {
        "metadata": {"title": "Synthetic topic"},
        "primaryContentSections": [{"kind": "content", "content": list(blocks)}],
    }


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.data = document(paragraph("Consider a contextual alternative."))

    def test_accepts_slug_and_canonical_url(self):
        for value in ("accessibility", "/Accessibility/", reader.HIG_PREFIX + "accessibility#scope"):
            self.assertEqual(reader.parse_slug(value), "accessibility")

    def test_rejects_non_apple_and_non_topic_inputs(self):
        for value in ("", "../buttons", "buttons/subtopic", "buttons?x=1", "file:///tmp/test",
                      "http://developer.apple.com/design/human-interface-guidelines/buttons",
                      "https://developer.apple.com.evil.test/design/human-interface-guidelines/buttons",
                      "https://evil.test@developer.apple.com/design/human-interface-guidelines/buttons",
                      "https://developer.apple.com/documentation/buttons"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                reader.parse_slug(value)

    def test_preserves_modal_scope_and_reference_text(self):
        self.data["references"] = {"ref": {"title": "Related topic"}}
        self.data["primaryContentSections"][0]["content"] += [
            {"type": "paragraph", "inlineContent": [
                {"type": "strong", "inlineContent": [{"type": "text", "text": "Only if applicable: "}]},
                {"type": "reference", "identifier": "ref"},
            ]}
        ]
        result = reader.build_result("buttons", self.data)
        self.assertIn("Consider a contextual alternative.", result["content"])
        self.assertIn("Only if applicable: Related topic", result["content"])
        self.assertEqual(result["extraction_warnings"], [])
        self.assertIsNone(result["alert_date"])
        self.assertIsNone(result["supported_platforms"])

    def test_tabs_keep_titles_and_conditions(self):
        result = reader.build_result("buttons", document({"type": "tabNavigator", "tabs": [
            {"title": "Platform A", "content": [paragraph("Prefer A only in this context.")]},
            {"title": "Platform B", "content": [paragraph("Consider B for this input.")]},
        ]}))
        self.assertIn("### Platform A\n\nPrefer A only in this context.", result["content"])
        self.assertIn("### Platform B\n\nConsider B for this input.", result["content"])

    def test_tables_and_lists_keep_boundaries(self):
        data = document(
            {"type": "table", "rows": [
                [[paragraph("Scope")], [paragraph("Default"), paragraph("Minimum")]],
                [[paragraph("Synthetic platform")], [paragraph("Contextual value")]],
            ]},
            {"type": "orderedList", "items": [{"content": [paragraph("First condition."),
                paragraph("Separate exception."), {"type": "unorderedList", "items": [
                    {"content": [paragraph("Nested qualification.")]}
                ]}]}]},
        )
        result = reader.build_result("buttons", data)
        self.assertIn("Scope | Default / Minimum", result["content"])
        self.assertIn("Synthetic platform | Contextual value", result["content"])
        self.assertIn("1. First condition.\n   \n   Separate exception.", result["content"])
        self.assertIn("   - Nested qualification.", result["content"])
        self.assertTrue(any("Table" in item for item in result["extraction_warnings"]))

    def test_unknown_blocks_warn_and_retain_reachable_text(self):
        result = reader.build_result("buttons", document(
            {"type": "futureContainer", "content": [paragraph("Conditional detail.")]},
            {"type": "video", "identifier": "demo"},
            {"type": "paragraph", "inlineContent": [{"type": "reference", "identifier": "missing"}]},
        ))
        self.assertIn("Conditional detail.", result["content"])
        self.assertEqual(len(result["extraction_warnings"]), 3)

    def test_small_print_and_malformed_neighbors_are_not_silent(self):
        note = paragraph("Exception applies only to this configuration.")
        note["type"] = "small"
        result = reader.build_result("buttons", document(note, 42, {
            "type": "futureContainer", "content": [paragraph("Retained qualification.")]
        }))
        self.assertIn("Exception applies only to this configuration.", result["content"])
        self.assertIn("Retained qualification.", result["content"])
        self.assertTrue(any("Malformed block" in item for item in result["extraction_warnings"]))

    def test_rejects_invalid_and_empty_payloads(self):
        for value in ([], {}, {"metadata": {"title": "Missing content"}},
                      document(), document({"type": "futureContainer", "unknownChildren": []})):
            with self.subTest(value=value), self.assertRaises(ValueError):
                reader.build_result("buttons", value)

    def test_digest_is_order_independent_but_detects_source_drift(self):
        original = reader.build_result("buttons", self.data)
        reordered = dict(reversed(list(self.data.items())))
        self.assertEqual(original["source_sha256"], reader.build_result("buttons", reordered)["source_sha256"])
        for changed in (document(paragraph("A changed recommendation.")), copy.deepcopy(self.data)):
            changed["metadata"]["customMetadata"] = {"alert-date": "2000-01-01"}
            current = reader.build_result("buttons", changed)
            self.assertEqual(reader.compare_metadata(current, original)["status"], "changed")
        self.assertEqual(reader.compare_metadata(original, original)["status"], "unchanged")

    def test_legacy_metadata_unknown_and_bad_baselines_rejected(self):
        result = reader.build_result("buttons", self.data)
        legacy = {"source_url": result["source_url"], "retrieved_at_utc": "old task"}
        self.assertEqual(reader.compare_metadata(result, legacy)["status"], "unknown")
        for baseline in ([], {}, {"source_url": reader.HIG_PREFIX + "typography"},
                         {**legacy, "source_sha256": "invalid"}):
            with self.subTest(baseline=baseline), self.assertRaises(ValueError):
                reader.compare_metadata(result, baseline)

    def test_timeout_must_be_finite_and_positive(self):
        for timeout in (0, -1, float("nan"), float("inf")):
            with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                reader.fetch_json(reader.DOCC_PREFIX + "buttons.json", timeout)

    def test_official_origin_redirect_boundary(self):
        handler = reader.AppleOnlyRedirect()
        request = urllib.request.Request(reader.DOCC_PREFIX + "buttons.json")
        for url in ("http://developer.apple.com/topic", "https://example.com/topic",
                    "https://developer.apple.com.evil.test/topic"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                handler.redirect_request(request, None, 302, "Found", {}, url)
        official = reader.DOCC_PREFIX + "accessibility.json"
        redirected = handler.redirect_request(request, None, 302, "Found", {}, official)
        self.assertEqual(redirected.full_url, official)

    def test_fetch_handles_success_http_failure_and_bad_json(self):
        for status, body, expected in ((200, json.dumps(self.data), None),
                                       (503, "{}", RuntimeError),
                                       (200, "not JSON", ValueError),
                                       (200, "[]", ValueError)):
            response = io.StringIO(body)
            response.status = status
            with self.subTest(status=status, body=body), patch.object(reader.urllib.request, "build_opener") as factory:
                factory.return_value.open.return_value = response
                if expected:
                    with self.assertRaises(expected):
                        reader.fetch_json(reader.DOCC_PREFIX + "buttons.json", 3)
                else:
                    self.assertEqual(reader.fetch_json(reader.DOCC_PREFIX + "buttons.json", 3), self.data)
                self.assertEqual(factory.return_value.open.call_args.kwargs["timeout"], 3)

    def run_cli(self, args, side_effect=None):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(sys, "argv", ["reader", *args]), \
             patch.object(reader, "fetch_json", return_value=self.data, side_effect=side_effect), \
             contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            status = reader.main()
        return status, stdout.getvalue(), stderr.getvalue()

    def test_cli_metadata_comparison_does_not_write_baseline(self):
        result = reader.build_result("buttons", self.data)
        with tempfile.TemporaryDirectory() as directory:
            baseline = Path(directory) / "baseline.json"
            text = json.dumps(result)
            baseline.write_text(text)
            status, stdout, stderr = self.run_cli(["buttons", "--metadata-only", "--compare-metadata", str(baseline)])
            output = json.loads(stdout)
            self.assertEqual((status, stderr), (0, ""))
            self.assertEqual(output["comparison"]["status"], "unchanged")
            self.assertNotIn("content", output)
            self.assertEqual(baseline.read_text(), text)

    def test_cli_failure_has_no_success_output(self):
        errors = (urllib.error.URLError("offline"), TimeoutError("timeout"),
                  ValueError("Malformed DocC"), TypeError("Unexpected content"))
        for error in errors:
            with self.subTest(error=error):
                status, stdout, stderr = self.run_cli(["buttons"], error)
                self.assertEqual((status, stdout), (1, ""))
                self.assertIn("error:", stderr)

    def test_cli_missing_and_malformed_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "baseline.json"
            for text in (None, "invalid JSON", "[]"):
                if text is not None:
                    path.write_text(text)
                status, stdout, stderr = self.run_cli(["buttons", "--compare-metadata", str(path)])
                self.assertEqual((status, stdout), (1, ""))
                self.assertIn("error:", stderr)

    def test_cli_markdown_and_json_include_evidence(self):
        for options in ([], ["--format", "json"]):
            status, stdout, stderr = self.run_cli(["buttons", *options])
            self.assertEqual((status, stderr), (0, ""))
            self.assertIn("Consider a contextual alternative.", stdout)
            self.assertIn(reader.HIG_PREFIX + "buttons", stdout)
            self.assertIn("Retrieval time is not", stdout)


if __name__ == "__main__":
    unittest.main()
