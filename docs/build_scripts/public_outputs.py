"""Declare, retain and verify files offered alongside an executed lesson."""
from __future__ import annotations

import hashlib
import html
import json
import os
from pathlib import Path, PurePosixPath
from urllib.parse import quote

from lesson_viewer import render_lesson_viewer


def output_path(value):
    if (not isinstance(value, str) or not value or '\\' in value
            or any(c in value for c in ('?', '#', ':', '\x00'))):
        raise ValueError('Public output path must be a relative file path')
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in ('.', '..', '') for p in value.split('/')):
        raise ValueError('Public output path must stay within tamerop_outputs')
    return path


def declarations(nb):
    items = nb.metadata.get('tamerop', {}).get('public_outputs', [])
    if not isinstance(items, list):
        raise ValueError('public_outputs must be a list')
    result = {}
    for item in items:
        if not isinstance(item, dict) or set(item) - {'path', 'label', 'embed', 'height'}:
            raise ValueError('Invalid public output declaration')
        path = str(output_path(item.get('path')))
        if path in result:
            raise ValueError(f'Duplicate public output: {path}')
        if not isinstance(item.get('label'), str) or not item['label'].strip():
            raise ValueError(f'Public output needs a label: {path}')
        if type(item.get('embed', False)) is not bool:
            raise ValueError(f'embed must be boolean: {path}')
        if item.get('embed') and Path(path).suffix != '.html':
            raise ValueError(f'Only HTML outputs can be embedded: {path}')
        height = item.get('height', 720)
        if type(height) is not int or not 280 <= height <= 1600:
            raise ValueError(f'Invalid public output height: {path}')
        result[path] = dict(item)
    shown = set()
    for cell in nb.cells:
        paths = cell.metadata.get('tamerop', {}).get('show_outputs', [])
        if not isinstance(paths, list) or any(not isinstance(p, str) for p in paths):
            raise ValueError('show_outputs must be a list of declared paths')
        for path in paths:
            if path not in result:
                raise ValueError(f'Undeclared public output: {path}')
            shown.add(path)
    if shown != set(result):
        raise ValueError('Declared public outputs need a page entrance: ' + ', '.join(sorted(set(result)-shown)))
    return result


def output_records(nb, directory):
    directory = Path(directory).resolve()
    records = []
    for name in declarations(nb):
        path = directory / name
        if not path.is_file() or not path.resolve().is_relative_to(directory):
            raise ValueError(f'Missing or escaping public output: {name}')
        data = path.read_bytes()
        if not data or len(data) > 20 * 1024 * 1024:
            raise ValueError(f'Public output is empty or exceeds 20 MiB: {name}')
        records.append({'path': name, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
    return records


def verify_outputs(nb, directory, record, *, published=False):
    actual = output_records(nb, directory)
    expected = record.get('public_outputs', [])
    if published:
        expected = [published_record(item) for item in expected]
    if actual != expected:
        raise ValueError('Public output files differ from the execution record; execute a fresh publication')
    if published:
        for item in actual:
            path = Path(directory) / item['path']
            if path.suffix == '.html' and render_lesson_viewer(path.read_text(encoding='utf-8')) is not None:
                raise ValueError(f'Unprepared native viewer remains in the website: {item["path"]}')
    return actual


def published_record(item):
    """Use presentation hashes only when checking the delivered website copy."""
    presentation = item.get('presentation')
    if presentation is None:
        return item
    if (set(presentation) != {'kind', 'sha256', 'bytes'}
            or presentation['kind'] != 'lesson-viewer'):
        raise ValueError('Unknown public output presentation')
    return {'path': item['path'], 'sha256': presentation['sha256'],
            'bytes': presentation['bytes']}


def present_outputs(root):
    """Simplify website viewers after copying verified execution artifacts.

    The capture and its record remain unchanged. The built record distinguishes
    their original hashes from the delivered presentation. Validate all inputs
    before replacing any file, so malformed exports fail publication together.
    """
    root = Path(root).resolve()
    record_path = root / 'downloads/publication.json'
    record = json.loads(record_path.read_text(encoding='utf-8'))
    replacements = []
    for lesson in record['notebooks']:
        directory = root / 'downloads/figures' / Path(lesson['source']).stem
        for item in lesson.get('public_outputs', []):
            if 'presentation' in item:
                raise ValueError('Prepare website views from the original execution capture')
            path = directory / output_path(item['path'])
            if not path.is_file() or not path.resolve().is_relative_to(directory.resolve()):
                raise ValueError(f'Missing or escaping public output: {item["path"]}')
            data = path.read_bytes()
            if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise ValueError(f'Public output differs from the execution record: {item["path"]}')
            if path.suffix != '.html':
                continue
            rendered = render_lesson_viewer(data.decode('utf-8'))
            if rendered is None:
                continue
            delivered = rendered.encode('utf-8')
            item['presentation'] = {'kind': 'lesson-viewer',
                'sha256': hashlib.sha256(delivered).hexdigest(), 'bytes': len(delivered)}
            replacements.append((path, delivered))
    for path, data in replacements:
        path.write_bytes(data)
    record_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    return len(replacements)


def output_routes(record):
    """Only explicitly recorded files may be standalone pages outside the catalog."""
    routes = set()
    for lesson in record.get('notebooks', []):
        stem = Path(lesson['source']).stem
        for item in lesson.get('public_outputs', []):
            name = output_path(item['path'])
            routes.add(f'downloads/figures/{stem}/{name}')
    return routes


def render_outputs(paths, declared, source, page, stage):
    blocks = []
    for name in paths:
        item = declared[name]
        target = stage / 'downloads' / 'figures' / source.stem / name
        relative = Path(os.path.relpath(target, page.parent)).as_posix()
        url = html.escape(quote(relative), quote=True)
        label = html.escape(item['label'], quote=True)
        if item.get('embed'):
            blocks.append(
                '<div class="prepared-example">'
                f'<iframe src="{url}" title="{label}" loading="lazy"'
                ' sandbox="allow-scripts"'
                f' height="{item.get("height", 720)}"></iframe></div>')
        elif Path(name).suffix == '.html':
            blocks.append(f'<p class="prepared-download"><a href="{url}" target="_blank" rel="noopener">{label}</a></p>')
        else:
            blocks.append(f'<p class="prepared-download"><a href="{url}" download>{label}</a></p>')
    return '\n'.join(blocks)
