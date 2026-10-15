"""Verify prepared arithmetic states, including exact membership and endpoints."""
from fractions import Fraction
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

DOCS = Path(__file__).resolve().parents[1]


def choices():
    script = (DOCS / 'assets/arithmetic/choices.js').read_text()
    return json.loads(re.search(r'const examples = (\{.*?\n  \});', script, re.S)[1])


class ArithmeticChoicesTests(unittest.TestCase):
    def test_exact_mathematical_values_of_every_selection(self):
        data = choices()
        for state in data['cutoff']:
            cutoff = Fraction(str(state['atol']))
            rank = sum(value > cutoff for value in (Fraction(1), Fraction(1, 10**14)))
            self.assertEqual(state['rank'], rank)
            self.assertEqual(state['nullity'], 2-rank)
        for state in data['certificate']:
            self.assertEqual(state['residual'], 2-state['y2'])
            self.assertEqual(state['accepted'], state['y2'] == 2)
        for state in data['boundary']:
            x, y = state['x'], state['y']
            self.assertEqual(state['signature'], [int(x >= 0 and y >= 0), int(x > 0 or y > 2)])
            self.assertEqual(state['dimension'], int(x == 0 and 0 <= y <= 2))
        first, second = Fraction(1), 1+Fraction(1, 2**71)
        for state in data['grades']:
            radius = 1+Fraction(state['offset'], 2**state['power'])
            self.assertEqual(float(radius), 0.5 if state['id'] == 'before' else 1.0)
            self.assertEqual(state['components'], 3-int(radius >= first)-int(radius >= second))

    def test_prepared_choices_agree_with_the_selected_library(self):
        julia = os.environ.get('TAMEROP_DOCS_TEST_JULIA') or shutil.which('julia')
        environment = DOCS / '.build/environment'
        if not julia or not (environment / 'Manifest.toml').is_file():
            self.skipTest('Julia documentation environment is not available')
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'choices.json'
            source.write_text(json.dumps(choices()))
            command = [julia, '--startup-file=no', '--threads=1', f'--project={environment}',
                       str(DOCS / 'build_scripts/check_arithmetic_choices.jl'), str(source)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=420)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
