"""The lesson presentation preserves drawings while omitting record controls."""
import base64
import copy
import hashlib
import html
from html.parser import HTMLParser
import json
import unittest

from lesson_viewer import render_lesson_viewer


def image_svg(contents):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="720">' + contents + '</svg>'
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.scripts = []
        self.styles = []
        self.active = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.elements.append((tag, attrs))
        if tag in ('script', 'style'):
            self.active = {'attrs': attrs, 'text': ''}
            (self.scripts if tag == 'script' else self.styles).append(self.active)

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.active = None

    def handle_data(self, text):
        if self.active is not None:
            self.active['text'] += text

    def by_id(self, identity):
        return next(attrs for _, attrs in self.elements if attrs.get('id') == identity)

    def bundle(self):
        return json.loads(next(script['text'] for script in self.scripts
                               if script['attrs'].get('id') == 'lesson-viewer-data'))


class LessonViewerTests(unittest.TestCase):
    def setUp(self):
        self.bundle = {
            'initial': 'filled',
            'states': [
                {'id': 'ring', 'label': 'Threshold zero', 'image': image_svg('<path d="M0 0h8v8z"/>'),
                 'selection': 'NamedTuple()', 'context': 'Runtime metadata omitted: internal',
                 'plotted_json': '{"private_record":42}'},
                {'id': 'filled', 'label': 'Threshold five', 'image': image_svg('<rect width="8" height="8"/>'),
                 'selection': 'NamedTuple()', 'context': 'Source identity: nothing',
                 'plotted_json': '{"private_record":43}'}],
            'session_json': '{"full_source":"not needed for selecting figures"}'}

    def source(self, bundle=None, title='A hole fills', caption='Compare the threshold and its barcode.'):
        payload = json.dumps(self.bundle if bundle is None else bundle).replace('<', '\\u003c')
        return ('<!doctype html><html><body><header><h1>' + html.escape(title)
                + '</h1><p>' + html.escape(caption) + '</p></header>'
                '<button id="download-session">Download session JSON</button>'
                '<details><summary>Raw selection</summary><pre>NamedTuple()</pre></details>'
                '<script id="portable-visual-data" type="application/json">' + payload
                + '</script><script>oldViewer();</script></body></html>')

    def test_every_prepared_drawing_and_state_identity_is_preserved(self):
        result = Document(render_lesson_viewer(self.source())).bundle()
        self.assertEqual(result, {
            'initial': self.bundle['initial'],
            'states': [{key: state[key] for key in ('id', 'label', 'image')}
                       for state in self.bundle['states']]})
        for original, presented in zip(self.bundle['states'], result['states']):
            self.assertEqual(hashlib.sha256(original['image'].encode()).digest(),
                             hashlib.sha256(presented['image'].encode()).digest())

    def test_initial_figure_and_disabled_controls_work_without_script(self):
        document = Document(render_lesson_viewer(self.source()))
        image = document.by_id('saved-figure')
        self.assertEqual(image['src'], self.bundle['states'][1]['image'])
        self.assertEqual(image['alt'], 'Threshold five')
        options = [attrs for tag, attrs in document.elements if tag == 'option']
        self.assertEqual([item['value'] for item in options], ['ring', 'filled'])
        self.assertEqual([item['value'] for item in options if 'selected' in item], ['filled'])
        for identity in ('saved-state', 'previous-state', 'next-state'):
            self.assertIn('disabled', document.by_id(identity))
        self.assertEqual(document.by_id('view-status')['aria-live'], 'polite')

    def test_record_controls_and_payloads_are_absent(self):
        rendered = render_lesson_viewer(self.source())
        document = Document(rendered)
        self.assertFalse(any(tag in ('a', 'details', 'pre') for tag, _ in document.elements))
        for removed in ('session_json', 'plotted_json', 'NamedTuple()', 'Runtime metadata omitted',
                        'download-session', 'download-values', 'download-figure', 'state-link',
                        'full_source', 'private_record', 'oldViewer'):
            self.assertNotIn(removed, rendered)
        self.assertEqual(len(document.scripts), 2)

    def test_explanatory_text_and_state_names_cannot_inject_markup(self):
        bundle = copy.deepcopy(self.bundle)
        dangerous = '</script><script>unexpected()</script> & "name"\u2028\u2029'
        bundle['states'][0]['id'] = dangerous
        bundle['states'][0]['label'] = dangerous
        bundle['initial'] = dangerous
        rendered = render_lesson_viewer(self.source(bundle, title=dangerous, caption=dangerous))
        document = Document(rendered)
        self.assertEqual(len(document.scripts), 2)
        self.assertEqual(document.bundle()['initial'], dangerous)
        self.assertEqual(document.by_id('saved-figure')['alt'], dangerous)
        self.assertNotIn('<script>unexpected()', rendered)
        self.assertIn('&lt;/script&gt;', rendered)
        self.assertIn('\\u003c/script>', rendered)
        self.assertIn('\\u2028', rendered)
        self.assertIn('\\u2029', rendered)

    def test_policy_hashes_identify_actual_script_and_style(self):
        document = Document(render_lesson_viewer(self.source()))
        policy = next(attrs['content'] for tag, attrs in document.elements
                      if tag == 'meta' and attrs.get('http-equiv') == 'Content-Security-Policy')
        executable = [item for item in document.scripts if item['attrs'].get('type') != 'application/json']
        self.assertEqual(len(executable), 1)
        for text in (executable[0]['text'], document.styles[0]['text']):
            digest = base64.b64encode(hashlib.sha256(text.encode()).digest()).decode()
            self.assertIn("'sha256-" + digest + "'", policy)
        for rule in ("default-src 'none'", "connect-src 'none'", 'img-src data:',
                     "object-src 'none'", "frame-src 'none'"):
            self.assertIn(rule, policy)
        self.assertNotIn('unsafe-inline', policy)
        self.assertFalse(any('src' in script['attrs'] for script in document.scripts))

    def test_ordinary_html_is_left_for_its_existing_publication_path(self):
        self.assertIsNone(render_lesson_viewer('<h1>A static composition</h1><img src="figure.svg">'))
        self.assertIsNone(render_lesson_viewer('<script type="application/json">{"states":[]}</script>'))

    def test_rejects_ambiguous_or_unclosed_recognized_bundles(self):
        source = self.source()
        script = source[source.index('<script id="portable-visual-data"'):source.index('<script>oldViewer')]
        for malformed in (source.replace('</body>', script + '</body>'),
                          source.replace('type="application/json"', 'type="text/javascript"'),
                          source[:source.index('</script>')],
                          source.replace('<header>', '<header><h1>Second title</h1>'),
                          source.replace('</header>', ''),
                          source.replace('<h1>A hole fills</h1>', '<h1> </h1>')):
            with self.subTest(source=malformed[:80]), self.assertRaises(ValueError):
                render_lesson_viewer(malformed)

    def test_rejects_invalid_json_and_duplicate_keys(self):
        for payload in ('{broken', '{"initial":"ring","initial":"filled","states":[]}'):
            source = self.source().replace(json.dumps(self.bundle), payload)
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                render_lesson_viewer(source)

    def test_rejects_missing_or_ambiguous_states(self):
        cases = [[], None, {}, [None], self.bundle['states'] * 2]
        for states in cases:
            bundle = {**self.bundle, 'states': states}
            with self.subTest(states=states), self.assertRaises(ValueError):
                render_lesson_viewer(self.source(bundle))
        for field, value in (('initial', 'absent'), ('initial', [])):
            with self.subTest(value=value), self.assertRaises(ValueError):
                render_lesson_viewer(self.source({**self.bundle, field: value}))
        for field in ('id', 'label'):
            for value in ('', ' ', None, 1):
                bundle = copy.deepcopy(self.bundle)
                bundle['states'][0][field] = value
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    render_lesson_viewer(self.source(bundle))

    def test_rejects_external_or_invalid_images(self):
        for image in ('https://example.org/figure.svg', 'data:image/png;base64,AA==',
                      'data:image/svg+xml;base64,***',
                      'data:image/svg+xml;base64,' + base64.b64encode(b'<html/>').decode(),
                      'data:image/svg+xml;base64,' + base64.b64encode(b'<svg>').decode(), None):
            bundle = copy.deepcopy(self.bundle)
            bundle['states'][0]['image'] = image
            with self.subTest(image=image), self.assertRaises(ValueError):
                render_lesson_viewer(self.source(bundle))

    def test_one_state_and_library_state_limit(self):
        one = {'initial': 'ring', 'states': self.bundle['states'][:1]}
        self.assertEqual(Document(render_lesson_viewer(self.source(one))).bundle(), {
            'initial': 'ring', 'states': [{key: one['states'][0][key]
                                        for key in ('id', 'label', 'image')}]})
        many = [{'id': str(i), 'label': str(i), 'image': self.bundle['states'][0]['image']}
                for i in range(129)]
        self.assertEqual(len(Document(render_lesson_viewer(self.source({
            'initial': '0', 'states': many[:128]}))).bundle()['states']), 128)
        with self.assertRaises(ValueError):
            render_lesson_viewer(self.source({'initial': '0', 'states': many}))


if __name__ == '__main__':
    unittest.main()
