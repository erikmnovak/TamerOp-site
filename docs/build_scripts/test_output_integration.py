"""Check public lesson outputs across capture reuse and site finalization."""
import base64
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import nbformat as nbf

from check_site import Links, check_notebooks
from navigation import finalize_navigation
from public_outputs import output_records, present_outputs, verify_outputs
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


def session_html():
    image = 'data:image/svg+xml;base64,' + base64.b64encode(
        b'<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0h5v5z"/></svg>').decode()
    payload = {'initial': 'selected', 'states': [{
        'id': 'selected', 'label': 'A selected map', 'image': image,
        'selection': 'NamedTuple()', 'context': 'Source identity: nothing',
        'plotted_json': '{"matrix":[[1]]}'}], 'session_json': '{"source":"full record"}'}
    return ('<!doctype html><html><body><header><h1>A selected map</h1>'
            '<p>Follow the retained drawing.</p></header>'
            '<script id="portable-visual-data" type="application/json">'
            + json.dumps(payload) + '</script></body></html>').encode()


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
        self.anchors = f'<a href="{self.href}" target="_blank">Explore the map</a>'
        self.frame = f'<iframe src="{self.href}" title="Explore the map"></iframe>'

    def check_page(self, content):
        self.page.write_text(content)
        parsed = Links()
        parsed.feed(content)
        check_notebooks(self.manifest, {self.page.resolve(): parsed}, self.root, self.docs)

    def test_embed_is_the_entrance_without_an_extra_link(self):
        self.check_page(self.base + self.frame)

    def test_opening_link_does_not_substitute_for_the_declared_embed(self):
        with self.assertRaisesRegex(ValueError, 'Missing prepared-example embed'):
            self.check_page(self.base + self.anchors)

    def test_standalone_view_requires_its_one_opening_link(self):
        source = self.docs / 'tutorials/example.ipynb'
        download = self.root / 'downloads/example.ipynb'
        for path in (source, download):
            nb = nbf.read(path, as_version=4)
            nb.metadata.tamerop.public_outputs[0].embed = False
            nbf.write(nb, path)
        record_path = self.root / 'downloads/publication.json'
        record = json.loads(record_path.read_text())
        record['notebooks'][0].update(sha256=sha256(source), download_sha256=sha256(download))
        record_path.write_text(json.dumps(record))
        self.check_page(self.base + self.anchors)
        with self.assertRaisesRegex(ValueError, 'Missing public-output link'):
            self.check_page(self.base + self.frame)


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


class LessonPresentationIntegrationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.docs = Path(temporary.name)
        self.capture = self.docs / '.build/src'
        self.build = self.docs / 'build'
        self.outputs = self.capture / 'downloads/figures/example'
        self.view = self.outputs / 'views/view.html'
        self.view.parent.mkdir(parents=True)
        self.view.write_bytes(session_html())
        self.fixed = self.outputs / 'views/composition.html'
        self.fixed.write_bytes(NATIVE_HTML)
        self.notebook = publication_fixtures.PublicationTests().fixture()
        declare_view(self.notebook)
        self.notebook.metadata.tamerop.public_outputs.append({
            'path': 'views/composition.html', 'label': 'View the composition'})
        self.notebook.cells[0].metadata.tamerop.show_outputs.append('views/composition.html')
        self.record = {'notebooks': [{'source': 'tutorials/example.ipynb',
            'public_outputs': output_records(self.notebook, self.outputs)}]}
        self.record_path = self.capture / 'downloads/publication.json'
        self.record_path.write_text(json.dumps(self.record))
        self.published_outputs = self.build / 'downloads/figures/example'
        self.published_record = self.build / 'downloads/publication.json'
        self.copy_capture()

    def copy_capture(self):
        if self.build.exists():
            shutil.rmtree(self.build)
        shutil.copytree(self.capture, self.build)

    def test_only_website_copy_changes_and_both_hash_contracts_remain_verifiable(self):
        original_view = self.view.read_bytes()
        original_record = self.record_path.read_bytes()
        self.assertEqual(present_outputs(self.build), 1)
        self.assertEqual(self.view.read_bytes(), original_view)
        self.assertEqual(self.record_path.read_bytes(), original_record)
        verify_outputs(self.notebook, self.outputs, self.record['notebooks'][0])
        published = json.loads(self.published_record.read_text())['notebooks'][0]
        public_view = self.published_outputs / 'views/view.html'
        self.assertNotEqual(public_view.read_bytes(), original_view)
        self.assertEqual((self.published_outputs / 'views/composition.html').read_bytes(), NATIVE_HTML)
        expected = output_records(self.notebook, self.published_outputs)
        self.assertEqual(verify_outputs(self.notebook, self.published_outputs, published, published=True), expected)
        raw_record = self.record['notebooks'][0]['public_outputs'][0]
        item = published['public_outputs'][0]
        self.assertEqual({key: item[key] for key in ('path', 'sha256', 'bytes')}, raw_record)
        self.assertEqual(item['presentation'], {'kind': 'lesson-viewer',
            'sha256': sha256(public_view), 'bytes': public_view.stat().st_size})
        self.assertNotIn('presentation', published['public_outputs'][1])
        with self.assertRaisesRegex(ValueError, 'differ'):
            verify_outputs(self.notebook, self.published_outputs, self.record['notebooks'][0])

    def test_missing_or_changed_presentation_file_fails_published_verification(self):
        present_outputs(self.build)
        published = json.loads(self.published_record.read_text())['notebooks'][0]
        view = self.published_outputs / 'views/view.html'
        good = view.read_bytes()
        for changed, message in ((None, 'Missing'), (good + b'<!-- changed -->', 'differ'),
                                 (session_html(), 'differ')):
            with self.subTest(mutation=message):
                if changed is None:
                    view.unlink()
                else:
                    view.write_bytes(changed)
                with self.assertRaisesRegex(ValueError, message):
                    verify_outputs(self.notebook, self.published_outputs, published, published=True)
                view.write_bytes(good)

    def test_missing_or_unknown_presentation_record_fails_verification(self):
        present_outputs(self.build)
        published = json.loads(self.published_record.read_text())['notebooks'][0]
        for replacement in (None, {'kind': 'unknown', 'sha256': '0' * 64, 'bytes': 1}):
            broken = copy.deepcopy(published)
            item = broken['public_outputs'][0]
            if replacement is None:
                del item['presentation']
            else:
                item['presentation'] = replacement
            with self.subTest(record=replacement), self.assertRaises(ValueError):
                verify_outputs(self.notebook, self.published_outputs, broken, published=True)

    def test_published_verification_rejects_an_unpresented_native_session(self):
        # A valid raw capture is not yet the lesson's reader-facing presentation.
        verify_outputs(self.notebook, self.outputs, self.record['notebooks'][0])
        with self.assertRaisesRegex(ValueError, 'Unprepared native viewer'):
            verify_outputs(self.notebook, self.published_outputs,
                           self.record['notebooks'][0], published=True)

    def test_invalid_later_session_leaves_every_file_and_manifest_untouched(self):
        # This is a captured, hash-consistent file whose bundle cannot be shown.
        self.fixed.write_bytes(b'<header><h1>Broken view</h1><p>Explanation</p></header>'
                               b'<script id="portable-visual-data" type="application/json">'
                               b'{"initial":"absent","states":[]}</script>')
        self.record['notebooks'][0]['public_outputs'] = output_records(self.notebook, self.outputs)
        self.record_path.write_text(json.dumps(self.record))
        self.copy_capture()
        before = {path: path.read_bytes() for path in self.build.rglob('*') if path.is_file()}
        with self.assertRaisesRegex(ValueError, 'prepared states'):
            present_outputs(self.build)
        self.assertEqual({path: path.read_bytes() for path in before}, before)

    def test_repeated_presentation_requires_a_fresh_copy_of_the_capture(self):
        present_outputs(self.build)
        before = {path: path.read_bytes() for path in self.build.rglob('*') if path.is_file()}
        with self.assertRaisesRegex(ValueError, 'original execution capture'):
            present_outputs(self.build)
        self.assertEqual({path: path.read_bytes() for path in before}, before)

    def test_tampered_capture_is_rejected_before_any_presentation_is_written(self):
        view = self.published_outputs / 'views/view.html'
        view.write_bytes(view.read_bytes() + b'changed')
        before = {path: path.read_bytes() for path in self.build.rglob('*') if path.is_file()}
        with self.assertRaisesRegex(ValueError, 'differs from the execution record'):
            present_outputs(self.build)
        self.assertEqual({path: path.read_bytes() for path in before}, before)


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
        self.raw_view = session_html()
        self.view.write_bytes(self.raw_view)
        evidence.update(sha256=sha256(source), download_sha256=sha256(saved),
                        public_outputs=output_records(nb, exports))
        self.fixture.save_record()

    def test_reused_capture_retains_native_output_and_its_page_entrance(self):
        previous = self.fixture.record['notebooks'][0]['public_outputs']
        record = self.fixture.build(reuse_unchanged=True)
        self.assertEqual(self.fixture.executed, [])
        self.assertEqual(record['notebooks'][0]['public_outputs'], previous)
        self.assertEqual(self.view.read_bytes(), self.raw_view)
        published_record = json.loads((self.fixture.docs / 'build/downloads/publication.json').read_text())
        published_outputs = self.fixture.docs / 'build/downloads/figures/one'
        self.assertNotEqual((published_outputs / 'views/view.html').read_bytes(), self.raw_view)
        notebook = nbf.read(self.fixture.previous / 'one.ipynb', as_version=4)
        verify_outputs(notebook, published_outputs, published_record['notebooks'][0], published=True)
        page = self.fixture.docs / '.build/src/tutorials/one.md'
        text = page.read_text()
        self.assertIn('src="../downloads/figures/one/views/view.html"', text)
        self.assertIn('sandbox="allow-scripts"', text)
        self.assertNotIn('Download HTML', text)

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
                    self.view.write_bytes(self.raw_view)


if __name__ == '__main__':
    unittest.main()
