"""Check public lesson outputs across capture reuse and site finalization."""
import json
from pathlib import Path
import tempfile
import unittest

import nbformat as nbf

from check_site import Links, check_notebooks
from navigation import finalize_navigation
from public_outputs import output_records
from publish import sha256
from site_shell import finalize_site
import test_publication as publication_fixtures
import test_site_shell as shell_fixtures


NATIVE_HTML = b'''<!doctype html><html lang="en"><head>
<meta http-equiv="Content-Security-Policy" content="default-src 'none'">
<title>A prepared answer</title></head><body>
<h1>Selected map</h1><p>Keep this native document byte for byte.</p>
<script type="application/json" id="values">{"matrix":[[1]]}</script>
</body></html>\n'''


def declare_view(nb):
    nb.metadata['tamerop'] = {'public_outputs': [
        {'path': 'views/view.html', 'label': 'Explore the map', 'embed': True}]}
    nb.cells[0].metadata['tamerop'] = {'show_outputs': ['views/view.html']}


class OutputEntranceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.docs = Path(temporary.name)
        self.root = self.docs / 'build'
        source = self.docs / 'tutorials/example.ipynb'
        source.parent.mkdir()
        download = self.root / 'downloads/example.ipynb'
        download.parent.mkdir(parents=True)
        nb = publication_fixtures.PublicationTests().fixture()
        declare_view(nb)
        nbf.write(nb, source)
        nbf.write(nb, download)
        outputs = self.root / 'downloads/figures/example'
        self.view = outputs / 'views/view.html'
        self.view.parent.mkdir(parents=True)
        self.view.write_bytes(NATIVE_HTML)
        record = {'notebooks': [{'source': 'tutorials/example.ipynb',
            'sha256': sha256(source), 'download_sha256': sha256(download),
            'code_cells': 1, 'figures': 1, 'public_outputs': output_records(nb, outputs)}]}
        (self.root / 'downloads/publication.json').write_text(json.dumps(record))
        self.manifest = {'notebooks': [{'source': 'tutorials/example.ipynb',
                                       'page': 'guides/example.md'}]}
        self.page = self.root / 'guides/example.html'
        self.page.parent.mkdir()
        self.base = ('<a href="../downloads/example.ipynb">Notebook</a>'
                     '<img src="data:image/png;base64,AA==" alt="A saved figure">')
        self.href = '../downloads/figures/example/views/view.html'
        self.anchors = (f'<a href="{self.href}" target="_blank">Open the viewer</a>'
                        f'<a href="{self.href}" download>Download HTML</a>')
        self.frame = f'<iframe src="{self.href}" title="Explore the map"></iframe>'

    def check_page(self, content):
        self.page.write_text(content)
        parsed = Links()
        parsed.feed(content)
        check_notebooks(self.manifest, {self.page.resolve(): parsed}, self.root, self.docs)

    def test_embed_does_not_substitute_for_a_separate_open_or_download_link(self):
        self.check_page(self.base + self.anchors + self.frame)
        with self.assertRaisesRegex(ValueError, 'Missing public-output link'):
            self.check_page(self.base + self.frame)

    def test_download_link_does_not_substitute_for_the_declared_embed(self):
        self.check_page(self.base + self.anchors + self.frame)
        with self.assertRaisesRegex(ValueError, 'Missing prepared-example embed'):
            self.check_page(self.base + self.anchors)


class NativeOutputFinalizationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.docs = Path(temporary.name)
        self.build = self.docs / 'build'
        self.page = self.build / 'guides/current.html'
        self.page.parent.mkdir(parents=True)
        self.page.write_text(shell_fixtures.HTML)
        stage = self.docs / '.build/src'
        stage.mkdir(parents=True)
        (stage / 'catalog.json').write_text(json.dumps(shell_fixtures.catalog()))
        assets = self.docs / 'src/assets'
        assets.mkdir(parents=True)
        for name in ('site_navigation.css', 'site_navigation.js'):
            (assets / name).write_text('/* fixture asset */')
        self.native = self.build / 'downloads/figures/example/views/view.html'
        self.native.parent.mkdir(parents=True)
        self.native.write_bytes(NATIVE_HTML)
        record = {'notebooks': [{'source': 'tutorials/example.ipynb',
                                'public_outputs': [{'path': 'views/view.html'}]}]}
        (self.build / 'downloads/publication.json').write_text(json.dumps(record))
        (self.docs / 'publication.toml').write_text(
            '[guides]\n"current.md" = "guides/current.md"\n'
            '[reading_map]\nsource = "reading_map.toml"\npage = "reading_map.md"\n')
        (self.docs / 'reading_map.toml').write_text('nodes = []\ngroups = []\n')
        # The footer pass expects a notebook list, even for this article-only fixture.
        config = (self.docs / 'publication.toml').read_text()
        (self.docs / 'publication.toml').write_text('notebooks = []\n' + config)

    def test_native_html_survives_navigation_and_site_chrome_byte_for_byte(self):
        finalize_navigation(self.docs)
        finalize_site(self.docs)
        self.assertEqual(self.native.read_bytes(), NATIVE_HTML)
        transformed = self.page.read_text()
        self.assertIn('id="site-navigation"', transformed)
        self.assertIn('class="reading-map-return"', transformed)

    def test_unrecorded_html_in_downloads_is_not_exempted(self):
        unknown = self.native.with_name('unrecorded.html')
        unknown.write_bytes(NATIVE_HTML)
        with self.assertRaises(ValueError):
            finalize_site(self.docs)
        self.assertEqual(self.native.read_bytes(), NATIVE_HTML)
        self.assertEqual(unknown.read_bytes(), NATIVE_HTML)
        self.assertEqual(self.page.read_text(), shell_fixtures.HTML)


class OutputReuseIntegrationTests(unittest.TestCase):
    def setUp(self):
        # Reuse the isolated publisher fixture, including its simulated Julia
        # client. These tests invoke the actual publication reuse workflow.
        self.fixture = publication_fixtures.UnchangedPublicationTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        evidence = self.fixture.record['notebooks'][0]
        source = self.fixture.docs / evidence['source']
        saved = self.fixture.previous / source.name
        for path in (source, saved):
            nb = nbf.read(path, as_version=4)
            declare_view(nb)
            nbf.write(nb, path)
        exports = self.fixture.previous / 'figures/one'
        self.view = exports / 'views/view.html'
        self.view.parent.mkdir()
        self.view.write_bytes(NATIVE_HTML)
        evidence.update(sha256=sha256(source), download_sha256=sha256(saved),
                        public_outputs=output_records(nb, exports))
        self.fixture.save_record()

    def test_reused_capture_retains_native_output_and_its_page_entrance(self):
        previous = self.fixture.record['notebooks'][0]['public_outputs']
        record = self.fixture.build(reuse_unchanged=True)
        self.assertEqual(self.fixture.executed, [])
        self.assertEqual(record['notebooks'][0]['public_outputs'], previous)
        self.assertEqual(self.view.read_bytes(), NATIVE_HTML)
        page = self.fixture.docs / '.build/src/tutorials/one.md'
        text = page.read_text()
        self.assertIn('src="../downloads/figures/one/views/view.html"', text)
        self.assertIn('download>Download HTML', text)

    def test_missing_or_tampered_output_rejects_both_reuse_modes_before_execution(self):
        publication = self.fixture.previous / 'publication.json'
        original_record = publication.read_bytes()
        for mode in ('reuse_executed', 'reuse_unchanged'):
            for mutation in ('missing', 'tampered'):
                with self.subTest(mode=mode, mutation=mutation):
                    if mutation == 'missing':
                        self.view.unlink()
                    else:
                        self.view.write_bytes(b'<p>A different mathematical answer</p>')
                    message = 'Missing' if mutation == 'missing' else 'differ'
                    with self.assertRaisesRegex(ValueError, message):
                        self.fixture.build(**{mode: True})
                    self.assertEqual(self.fixture.executed, [])
                    self.assertEqual(publication.read_bytes(), original_record)
                    self.view.write_bytes(NATIVE_HTML)


if __name__ == '__main__':
    unittest.main()
