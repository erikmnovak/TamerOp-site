"""Regression checks for outputs that formerly disappeared after execution."""
from pathlib import Path
import tempfile
import unittest

import nbformat as nbf

from public_outputs import declarations, output_records, output_routes, render_outputs, verify_outputs
from publish import DOCS, export_lesson
from check_site import Links


class PublicOutputTests(unittest.TestCase):
    def notebook(self):
        return nbf.v4.new_notebook(
            metadata={'tamerop': {'public_outputs': [
                {'path': 'views/square.html', 'label': 'Select a map', 'embed': True}]}},
            cells=[nbf.v4.new_markdown_cell('# Square\n\nCompare the prepared maps.',
                metadata={'tamerop': {'show_outputs': ['views/square.html']}})])

    def test_published_files_survive_reuse_and_changes_are_rejected(self):
        nb = self.notebook()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaisesRegex(ValueError, 'Missing'):
                output_records(nb, root)
            target = root / 'views/square.html'
            target.parent.mkdir()
            target.write_text('<p>Prepared maps</p>')
            evidence = {'source': 'tutorials/square.ipynb', 'public_outputs': output_records(nb, root)}
            verify_outputs(nb, root, evidence)
            self.assertEqual(output_routes({'notebooks': [evidence]}),
                {'downloads/figures/square/views/square.html'})
            target.write_text('<p>A changed answer</p>')
            with self.assertRaisesRegex(ValueError, 'differ'):
                verify_outputs(nb, root, evidence)
            target.unlink()
            with self.assertRaisesRegex(ValueError, 'Missing'):
                verify_outputs(nb, root, evidence)

    def test_output_has_page_entrance_and_does_not_leave_export_directory(self):
        for path in ['../escape.html', '/tmp/escape.html', 'views/../escape.html',
                     'views//square.html', 'https://example.com/a.html', 'view.html#x']:
            nb = self.notebook()
            nb.metadata.tamerop.public_outputs[0].path = path
            with self.subTest(path=path), self.assertRaises(ValueError):
                declarations(nb)
        nb = self.notebook()
        nb.cells[0].metadata.tamerop.show_outputs = []
        with self.assertRaisesRegex(ValueError, 'entrance'):
            declarations(nb)
        nb.cells[0].metadata.tamerop.show_outputs = ['absent.html']
        with self.assertRaisesRegex(ValueError, 'Undeclared'):
            declarations(nb)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'exports/views').mkdir(parents=True)
            (root / 'external.html').write_text('outside')
            (root / 'exports/views/square.html').symlink_to(root / 'external.html')
            with self.assertRaisesRegex(ValueError, 'escaping'):
                output_records(self.notebook(), root / 'exports')

    def test_converter_places_accessible_embed_without_redundant_links(self):
        nb = self.notebook()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / 'guides/square.md'
            export_lesson(nb, DOCS / 'tutorials/square.ipynb', page, {}, root)
            result = page.read_text()
            self.assertIn('src="../downloads/figures/square/views/square.html"', result)
            self.assertIn('sandbox="allow-scripts"', result)
            self.assertIn('title="Select a map"', result)
            self.assertNotIn('Download HTML', result)
            self.assertNotIn('open separately', result)
            self.assertLess(result.index('Compare the prepared maps.'), result.index('<iframe'))
            parsed = Links()
            parsed.feed(result)
            self.assertEqual(len(parsed.frames), 1)
            self.assertNotIn('../downloads/figures/square/views/square.html', parsed.anchor_links)

    def test_standalone_html_has_one_escaped_entrance_and_no_download_twin(self):
        nb = self.notebook()
        item = nb.metadata.tamerop.public_outputs[0]
        item.label = 'A < B & "C"'
        item.embed = False
        result = render_outputs(['views/square.html'], declarations(nb), Path('square.ipynb'),
                                Path('/stage/guides/square.md'), Path('/stage'))
        self.assertNotIn('<iframe', result)
        self.assertIn('A &lt; B &amp; &quot;C&quot;', result)
        self.assertNotIn(' download', result)
        parsed = Links()
        parsed.feed(result)
        self.assertEqual(parsed.anchor_links, ['../downloads/figures/square/views/square.html'])

    def test_static_figure_keeps_its_requested_download_link(self):
        nb = self.notebook()
        item = nb.metadata.tamerop.public_outputs[0]
        item.path, item.label, item.embed = 'views/square.svg', 'Save the drawing', False
        nb.cells[0].metadata.tamerop.show_outputs = ['views/square.svg']
        result = render_outputs(['views/square.svg'], declarations(nb), Path('square.ipynb'),
                                Path('/stage/guides/square.md'), Path('/stage'))
        self.assertIn('download>Save the drawing</a>', result)
        self.assertNotIn('<iframe', result)


if __name__ == '__main__':
    unittest.main()
