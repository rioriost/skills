"""Exercise cross-reference validation with isolated synthetic repositories."""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_repository import validate_links


class LinkTests(unittest.TestCase):
    def test_nested_links_resolve_from_containing_document(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "references").mkdir()
            target = root / "SKILL.md"
            target.touch()
            source = root / "references" / "guide.md"
            validate_links("[entry](../SKILL.md#workflow) [web](https://example.com) [here](#section)", source, root)

    def test_missing_or_escaping_links_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "SKILL.md"
            for link in ("missing.md", "../outside.md"):
                with self.subTest(link=link), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    validate_links(f"[broken]({link})", source, root)

    def test_fenced_example_is_not_a_repository_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            validate_links("```markdown\n[example](nonexistent.md)\n```\n", root / "SKILL.md", root)


if __name__ == "__main__":
    unittest.main()
