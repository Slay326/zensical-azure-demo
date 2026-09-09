"""Regression checks for the published private-asset boundary."""

from pathlib import Path
import tempfile
import unittest

from verify_assets import verify


class PublishedAssetBoundary(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        self.private = self.site / "death-star"
        self.private.mkdir()
        (self.private / "index.html").write_text("<h1>Private documentation</h1>")
        self.asset = self.private / "assets/blueprints/plate.svg"
        self.asset.parent.mkdir(parents=True)
        self.asset.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.page = self.private / "systems/example/index.html"
        self.page.parent.mkdir(parents=True)

    def test_nested_page_resolves_inside_private_prefix(self):
        self.page.write_text('<img src="../../assets/blueprints/plate.svg" alt="Plate">')
        verify(self.site)

    def test_public_root_asset_is_rejected_even_if_it_exists(self):
        public_asset = self.site / "assets/plate.svg"
        public_asset.parent.mkdir()
        public_asset.write_text("<svg/>")
        self.page.write_text('<img src="/assets/plate.svg">')
        with self.assertRaisesRegex(ValueError, "escapes authorization boundary"):
            verify(self.site)

    def test_encoded_parent_traversal_is_rejected(self):
        self.page.write_text('<img src="%2e%2e/%2e%2e/%2e%2e/assets/plate.svg">')
        with self.assertRaisesRegex(ValueError, "escapes authorization boundary"):
            verify(self.site)

    def test_missing_image_is_rejected(self):
        self.page.write_text('<img src="../../assets/absent.svg">')
        with self.assertRaisesRegex(ValueError, "Missing or escaped asset"):
            verify(self.site)

    def test_unlinked_blueprint_is_rejected(self):
        self.page.write_text("<p>No figure</p>")
        with self.assertRaisesRegex(ValueError, "not referenced"):
            verify(self.site)

    def test_srcset_cannot_bypass_check(self):
        self.page.write_text('<img srcset="/assets/plate.svg 2x">')
        with self.assertRaisesRegex(ValueError, "escapes authorization boundary"):
            verify(self.site)

    def test_runtime_search_cannot_escape_prefix(self):
        self.page.write_text(
            '<script id="__config" type="application/json">'
            '{"base":"/","search":"/assets/search.js"}</script>'
        )
        with self.assertRaisesRegex(ValueError, "escapes authorization boundary"):
            verify(self.site)

    def test_nested_runtime_base_preserves_parent_segments(self):
        (self.private / "search.json").write_text("{}")
        worker = self.private / "assets/search.js"
        worker.write_text("// Search worker")
        self.page.write_text(
            '<img src="../../assets/blueprints/plate.svg">'
            '<script id="__config" type="application/json">'
            '{"base":"../..","search":"../../assets/search.js"}</script>'
        )
        verify(self.site)


if __name__ == "__main__":
    unittest.main()
