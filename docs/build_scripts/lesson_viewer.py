"""Present captured session figures with only the controls used by a lesson.

The library export remains the execution artifact. This presentation copies its
SVG images and explanatory text without interpreting or recomputing the data.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import html
from html.parser import HTMLParser
import json
import xml.etree.ElementTree as ET


_STYLE = """
:root{color-scheme:light;font-family:system-ui,sans-serif;color:#172b38;background:white}
*{box-sizing:border-box}body{margin:1rem auto;padding:0 1rem;max-width:1600px;line-height:1.5;overflow-wrap:anywhere}
h1{font-size:1.5rem;line-height:1.25;margin:.5rem 0}header p{max-width:85ch;margin:.75rem 0}
button,select{font:inherit;padding:.45rem .7rem;border:1px solid #78909c;border-radius:.25rem;background:white;color:inherit}
button:not(:disabled),select:not(:disabled){cursor:pointer}button:disabled,select:disabled{color:#65747d;background:#f2f5f6}
button:focus-visible,select:focus-visible,.figure-scroll:focus-visible{outline:3px solid #0072b2;outline-offset:3px}
nav{display:flex;gap:.6rem;align-items:center;flex-wrap:wrap;padding:.75rem 0;border-block:1px solid #d8e0e4}
label{font-weight:600}select{max-width:100%;min-width:0;flex:1 1 16rem}nav .step{display:flex;gap:.5rem}
#view-status{min-height:1.5em;margin:.5rem 0;color:#405965}.error{color:#a51b16}
figure{margin:.75rem 0}.figure-scroll{max-width:100%;overflow:auto;border:1px solid #d8e0e4;background:white}
.figure-scroll img{display:block;width:auto;max-width:none;height:auto}
@media(max-width:600px){body{margin:.75rem auto;padding:0 .65rem}h1{font-size:1.3rem}nav{gap:.5rem}select{flex-basis:100%}}
@media print{nav,#view-status,noscript{display:none}figure{break-inside:avoid}.figure-scroll{overflow:visible}.figure-scroll img{max-width:100%}}
"""

_SCRIPT = """
(() => {
  'use strict';
  const bundle = JSON.parse(document.getElementById('lesson-viewer-data').textContent);
  const byId = new Map(bundle.states.map((state, index) => [state.id, index]));
  const chooser = document.getElementById('saved-state');
  const image = document.getElementById('saved-figure');
  const status = document.getElementById('view-status');
  const previous = document.getElementById('previous-state');
  const next = document.getElementById('next-state');
  let current = byId.get(bundle.initial);
  function requestedState() {
    return location.hash ? new URLSearchParams(location.hash.slice(1)).get('state') : bundle.initial;
  }
  function display(id, updateHash = false) {
    const found = byId.has(id);
    current = found ? byId.get(id) : byId.get(bundle.initial);
    const state = bundle.states[current];
    chooser.value = state.id;
    image.src = state.image;
    image.alt = state.label;
    image.dataset.stateId = state.id;
    previous.disabled = current === 0;
    next.disabled = current === bundle.states.length - 1;
    status.textContent = (found ? '' : 'Unknown view; showing the initial selection. ') +
      'View ' + (current + 1) + ' of ' + bundle.states.length + ': ' + state.label;
    status.classList.toggle('error', !found);
    const hash = '#state=' + encodeURIComponent(state.id);
    if (updateHash && location.hash !== hash) location.hash = hash;
    document.documentElement.dataset.selectedState = state.id;
  }
  chooser.addEventListener('change', () => display(chooser.value, true));
  previous.addEventListener('click', () => {
    if (current > 0) display(bundle.states[current - 1].id, true);
  });
  next.addEventListener('click', () => {
    if (current + 1 < bundle.states.length) display(bundle.states[current + 1].id, true);
  });
  window.addEventListener('hashchange', () => display(requestedState()));
  display(requestedState());
  chooser.disabled = bundle.states.length === 1;
  document.documentElement.dataset.ready = 'true';
})();
"""


class _Export(HTMLParser):
    """Read only the native bundle and the visible explanatory header."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bundles = []
        self.titles = []
        self.captions = []
        self.header_depth = 0
        self.header_count = 0
        self.script = None
        self.heading = None
        self.paragraph = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script' and attrs.get('id') == 'portable-visual-data':
            self.script = {'type': attrs.get('type'), 'text': [], 'closed': False}
            self.bundles.append(self.script)
        if tag == 'header':
            self.header_depth += 1
            self.header_count += 1
        if self.header_depth and tag == 'h1':
            self.heading = []
            self.titles.append(self.heading)
        if self.header_depth and tag == 'p':
            self.paragraph = []
            self.captions.append(self.paragraph)

    def handle_endtag(self, tag):
        if tag == 'script' and self.script is not None:
            self.script['closed'] = True
            self.script = None
        if tag == 'h1':
            self.heading = None
        if tag == 'p':
            self.paragraph = None
        if tag == 'header':
            self.header_depth = max(0, self.header_depth - 1)

    def handle_data(self, data):
        if self.script is not None:
            self.script['text'].append(data)
        elif self.heading is not None:
            self.heading.append(data)
        elif self.paragraph is not None:
            self.paragraph.append(data)


def _unique_object(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f'Duplicate lesson-viewer data key: {key}')
        result[key] = value
    return result


def _read_states(bundle):
    if not isinstance(bundle, dict):
        raise ValueError('Lesson-viewer bundle must be an object')
    states = bundle.get('states')
    if not isinstance(states, list) or not 1 <= len(states) <= 128:
        raise ValueError('Lesson viewer needs between 1 and 128 prepared states')
    result, identities = [], set()
    for state in states:
        if not isinstance(state, dict):
            raise ValueError('Lesson-viewer state must be an object')
        for field in ('id', 'label'):
            if not isinstance(state.get(field), str) or not state[field].strip():
                raise ValueError(f'Lesson-viewer state needs a nonempty {field}')
        if state['id'] in identities:
            raise ValueError('Lesson-viewer state identities must be unique')
        identities.add(state['id'])
        image = state.get('image')
        prefix = 'data:image/svg+xml;base64,'
        if not isinstance(image, str) or not image.startswith(prefix):
            raise ValueError('Lesson-viewer figures must be embedded SVG images')
        try:
            drawing = base64.b64decode(image[len(prefix):], validate=True)
            root = ET.fromstring(drawing)
        except (ValueError, binascii.Error, ET.ParseError) as error:
            raise ValueError('Invalid embedded lesson-viewer SVG') from error
        if root.tag not in ('svg', '{http://www.w3.org/2000/svg}svg'):
            raise ValueError('Lesson-viewer image must have an SVG root')
        result.append({field: state[field] for field in ('id', 'label', 'image')})
    initial = bundle.get('initial')
    if not isinstance(initial, str) or initial not in identities:
        raise ValueError('Lesson-viewer initial state must name a prepared state')
    return {'initial': initial, 'states': result}


def _csp_hash(text):
    return base64.b64encode(hashlib.sha256(text.encode('utf-8')).digest()).decode('ascii')


def render_lesson_viewer(source: str) -> str | None:
    """Return a lesson presentation, or ``None`` for an unrelated HTML export.

    A recognized but malformed session export fails publication rather than
    silently reverting to its raw record interface.
    """
    document = _Export()
    document.feed(source)
    document.close()
    if not document.bundles:
        return None
    if len(document.bundles) != 1:
        raise ValueError('Expected exactly one portable-visual-data bundle')
    record = document.bundles[0]
    if record['type'] != 'application/json' or not record['closed']:
        raise ValueError('Lesson-viewer bundle must be a closed JSON script')
    if (document.header_count != 1 or len(document.titles) != 1
            or len(document.captions) != 1 or document.header_depth):
        raise ValueError('Lesson-viewer export needs one explanatory header')
    title = ''.join(document.titles[0])
    caption = ''.join(document.captions[0])
    if not title.strip():
        raise ValueError('Lesson viewer needs a title')
    try:
        bundle = json.loads(''.join(record['text']), object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError('Invalid lesson-viewer JSON bundle') from error
    data = _read_states(bundle)
    initial = next(state for state in data['states'] if state['id'] == data['initial'])
    initial_index = data['states'].index(initial)
    escaped = lambda value: html.escape(value, quote=True)
    options = ''.join(
        '<option value="' + escaped(state['id']) + '"'
        + (' selected' if state['id'] == data['initial'] else '')
        + '>' + escaped(state['label']) + '</option>' for state in data['states'])
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace(
        '<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    policy = ("default-src 'none'; script-src 'sha256-" + _csp_hash(_SCRIPT)
              + "'; style-src 'sha256-" + _csp_hash(_STYLE)
              + "'; img-src data:; connect-src 'none'; object-src 'none'; "
                "frame-src 'none'; base-uri 'none'; form-action 'none'")
    status = f"View {initial_index + 1} of {len(data['states'])}: {initial['label']}"
    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta http-equiv="Content-Security-Policy" content="' + escaped(policy) + '">'
        '<title>' + escaped(title) + '</title><style>' + _STYLE + '</style></head><body>'
        '<header><h1>' + escaped(title) + '</h1><p>' + escaped(caption) + '</p></header>'
        '<nav aria-label="Prepared views"><label for="saved-state">View</label>'
        '<select id="saved-state" aria-describedby="view-status" disabled>' + options + '</select>'
        '<span class="step"><button id="previous-state" type="button" disabled>Previous</button>'
        '<button id="next-state" type="button" disabled>Next</button></span></nav>'
        '<p id="view-status" role="status" aria-live="polite">' + escaped(status) + '</p>'
        '<figure><div class="figure-scroll" tabindex="0" role="region" aria-label="Figure">'
        '<img id="saved-figure" src="' + escaped(initial['image']) + '" alt="'
        + escaped(initial['label']) + '"></div></figure>'
        '<noscript><p>The initial figure is shown above. Enable JavaScript to change the selection.</p></noscript>'
        '<script id="lesson-viewer-data" type="application/json">' + payload + '</script>'
        '<script>' + _SCRIPT + '</script></body></html>\n')
