"""Check the authored encoding explorer against its mathematical definitions."""
from fractions import Fraction
from html.parser import HTMLParser
from itertools import product
import os
from pathlib import Path
import re
import shutil
import subprocess
import unittest


DOCS = Path(__file__).resolve().parents[1]


class EncodingExplorerData(HTMLParser):
    """Read the actual choices and labelled regions from the chapter's HTML."""
    def __init__(self, source):
        super().__init__()
        self.active = False
        self.in_selector = False
        self.groups = []
        self.options, self.regions, self.bands, self.signatures = [], [], [], []
        self.option = self.text = None
        for block in re.findall(r'```@raw html\n(.*?)\n```', source, flags=re.S):
            self.feed(block)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'figure' and attrs.get('id') == 'encoding-label-explorer':
            self.active = True
        if not self.active:
            return
        classes = attrs.get('class', '').split()
        if tag == 'select':
            self.in_selector = attrs.get('id') == 'encoding-parameter'
        elif tag == 'option' and self.in_selector:
            self.option = {**attrs, 'text': ''}
            self.options.append(self.option)
        elif tag == 'rect' and 'encoding-region' in classes:
            self.regions.append(attrs)
        elif tag == 'g':
            self.groups.append('encoding-signature-label' in classes)
        elif tag == 'text':
            self.text = {**attrs, 'text': ''}
            if 'encoding-band' in classes:
                self.bands.append(self.text)
            elif any(self.groups):
                self.signatures.append(self.text)

    def handle_endtag(self, tag):
        if not self.active:
            return
        if tag == 'figure':
            self.active = False
        elif tag == 'select':
            self.in_selector = False
        elif tag == 'option':
            self.option = None
        elif tag == 'text':
            self.text = None
        elif tag == 'g':
            self.groups.pop()

    def handle_data(self, data):
        if self.active:
            if self.option is not None:
                self.option['text'] += data
            if self.text is not None:
                self.text['text'] += data


def band(coordinate):
    if coordinate < 0:
        return 'L'
    if coordinate <= 2:
        return 'C'
    return 'H'


def signature(x, y):
    # These are the chapter's two inequalities, evaluated with exact rationals.
    return f'{int(x >= 0 and y >= 0)}{int(x > 2 or y > 2)}'


def contains_label(region, label):
    x, y = Fraction(label['x']), Fraction(label['y'])
    left, top = Fraction(region['x']), Fraction(region['y'])
    return (left < x < left + Fraction(region['width'])
            and top < y < top + Fraction(region['height']))


class PreparedEncodingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = DOCS / 'finite_encodings.md'
        cls.data = EncodingExplorerData(source.read_text())

    def test_prepared_points_follow_both_exact_classifiers(self):
        self.assertTrue(self.data.options, 'The parameter selector has no prepared points')
        for option in self.data.options:
            with self.subTest(point=option['value']):
                x, y = Fraction(option['data-x']), Fraction(option['data-y'])
                self.assertEqual(option['data-band'], band(x) + band(y))
                self.assertEqual(option['data-signature'], signature(x, y))
                # A correct hidden record must agree with the coordinates readers choose.
                label = re.match(r'^\(([^,]+),\s*([^\)]+)\):', option['text'].strip())
                self.assertIsNotNone(label, 'Each choice must name its parameter')
                self.assertEqual((Fraction(label[1]), Fraction(label[2])), (x, y))

    def test_choices_cover_all_nine_bands_and_all_closed_corners(self):
        options = self.data.options
        points = [(Fraction(o['data-x']), Fraction(o['data-y'])) for o in options]
        self.assertEqual(len({o['value'] for o in options}), len(options))
        self.assertEqual(len(set(points)), len(options), 'Prepared choices must be distinct')
        self.assertEqual({o['data-band'] for o in options},
                         {''.join(pair) for pair in product('LCH', repeat=2)})
        corners = set(product((Fraction(0), Fraction(2)), repeat=2))
        self.assertTrue(corners <= set(points), 'Each included corner needs a prepared choice')
        marked = {point for point, option in zip(points, options)
                  if option.get('data-boundary') == 'true'}
        self.assertEqual(marked, corners)
        for point, option in zip(points, options):
            if point in corners:
                self.assertEqual(option['data-band'], 'CC')
                self.assertEqual(option['data-signature'], '10')

    def test_drawn_regions_have_their_mathematical_signatures(self):
        self.assertEqual(len(self.data.regions), 9)
        self.assertEqual(len(self.data.bands), 9)
        self.assertEqual(len(self.data.signatures), 9)
        self.assertEqual({label['data-band'] for label in self.data.bands},
                         {''.join(pair) for pair in product('LCH', repeat=2)})
        representatives = {'L': Fraction(-1), 'C': Fraction(1), 'H': Fraction(3)}
        columns = sorted({Fraction(region['x']) for region in self.data.regions})
        rows = sorted({Fraction(region['y']) for region in self.data.regions})
        self.assertEqual(len(columns), 3)
        self.assertEqual(len(rows), 3)
        for region in self.data.regions:
            names = [label for label in self.data.bands if contains_label(region, label)]
            printed = [label for label in self.data.signatures if contains_label(region, label)]
            self.assertEqual(len(names), 1, 'A region needs exactly one band label')
            self.assertEqual(len(printed), 1, 'A region needs exactly one signature label')
            pair = names[0]['data-band']
            expected = signature(*(representatives[letter] for letter in pair))
            with self.subTest(region=pair):
                # x increases rightward, while SVG row positions increase downward.
                self.assertEqual(pair, 'LCH'[columns.index(Fraction(region['x']))]
                                 + 'HCL'[rows.index(Fraction(region['y']))])
                self.assertEqual(names[0]['text'].replace(' ', ''), f'({pair[0]},{pair[1]})')
                self.assertEqual(region['data-signature'], expected)
                self.assertEqual(printed[0]['text'].replace(' ', ''),
                                 f'({expected[0]},{expected[1]})')


class PreparedRelativeTests(unittest.TestCase):
    def test_authored_states_agree_with_the_relative_pair_calculation(self):
        julia = os.environ.get('TAMEROP_DOCS_TEST_JULIA') or shutil.which('julia')
        if not julia:
            self.skipTest('Relative schematic regression requires Julia and the instantiated docs environment')
        project = Path(os.environ.get('TAMEROP_DOCS_TEST_PROJECT', DOCS / '.build/environment'))
        result = subprocess.run(
            [julia, '--startup-file=no', '--threads=1', f'--project={project}',
             str(DOCS / 'build_scripts/check_relative_pair.jl')],
            cwd=DOCS.parent, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=300)
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == '__main__':
    unittest.main()
