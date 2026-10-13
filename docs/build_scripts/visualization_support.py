"""Render the library-owned acceptance data for the website."""
from pathlib import Path
import re
import tomllib
from source_paths import package_root

def render(data):
    lines = ['# Visualization support and acceptance', '',
        'Use this matrix to choose a display and to review a visualization change. '
        'Support is a declared behavior; verification is evidence for a specified path. '
        'A native figure or serialized HTML is not evidence that a browser or notebook executed it.', '',
        'The maintained source is [visualization_support.toml](https://github.com/erikmnovak/TamerOp.jl/blob/main/test/visualization_support.toml). '
        'The website renders this page from the selected library checkout; '
        'Library CI rejects unassigned source files and unassigned native/browser tests. '
        'Reviewers must also identify new recipes within existing source files.', '',
        '## Reading the matrix', '',
        '- **N**: family-specific native mathematical/renderer checks; no browser execution implied.',
        '- **B**: maintained Chromium scenario exercises this family through real browser events.',
        '- **S**: supported through shared rendering/export code, covered by shared checks; '
        'not a separate browser acceptance claim for every recipe.',
        '- **U**: integration exists but that named frontend has not been qualified.',
        '- **—**: no such callback/widget is offered. Static selection remains a Julia argument.', '',
        'Cairo means static PNG/SVG/PDF figures. WGL native means native scene construction; '
        'HTML means exported scenes or fixed SVG compositions. Live Chromium means a standalone '
        'Bonito application with Julia running. Saved-view HTML instead selects among explicitly '
        'precomputed states after Julia has exited.', '',
        'The notebook column applies to each of IJulia/Jupyter, Pluto and VS Code: none inherits '
        'standalone-browser acceptance. Static notebook publication and executed Julia cells '
        'also do not certify a live notebook frontend. Firefox and WebKit have no declared '
        'acceptance baseline yet.', '',
        'The maintained standalone-browser environment requires Bonito 5.2 within major '
        'version 5. Browser evidence applies to the resolved harness stack; it does not '
        'qualify older nested-application integrations.', '',
        '## Families and display paths', '',
        '| Family | Cairo | WGL native | Exported HTML | Standalone Chromium | Live notebooks |',
        '| --- | --- | --- | --- | --- | --- |']
    for row in data['family']:
        symbols = {'native':'N','shared':'S','browser':'B','unsupported':'—','unverified':'U'}
        live = 'B (precomputed)' if row['live']=='precomputed' else 'B' if row['live']=='supported' else '—'
        slug = re.sub(r'[^\w\- ]', '', row['title'].lower()).replace(' ', '-')
        lines.append(f"| [{row['title']}](#{slug}) | {symbols[row['cairo']]} | {symbols[row['wgl']]} | {symbols[row['html']]} | {live} | U |")
    lines += ['', 'These entries identify maintained checks, not a claim that a test file proves '
        'its latest execution passed. CI supplies a run result and retained artifacts; '
        'local acceptance records preserve their environment, failures, reruns and scope. '
        'A green shared check does not qualify every possible input, recipe or frontend.', '']
    if snapshot := data.get('verification'):
        lines += ['## Recorded verification', '', f"Acceptance recorded on {snapshot['date']}. {snapshot['environment']}", '',
            f"- Native: {snapshot['native']}", f"- Live browser: {snapshot['live']}",
            f"- Offline exports: {snapshot['offline']}", '',
            'This dated record describes the tested revision and environment; current CI results '
            'remain the evidence for subsequent changes. The matrix validator checks the record\'s '
            'format, not the truth of an execution claim.', '']
    lines += [
        '## Standing A36 and A37 contracts', '',
        '**A36 — mathematical coordinates.** Use asymmetric and nonuniform fixtures wherever '
        'a transpose or midpoint convention could look plausible. Assert actual plotted cell '
        'boundaries and values in both backends, selected axis order, fixed coordinates, masks, '
        'orientation and exact-query behavior. Exact classification precedes floating drawing '
        'conversion. Native slider callbacks and real browser slider transport are separate checks.', '',
        '**A37 — advertised interaction.** Controls need accessible names and keyboard operation '
        'without requiring a canvas click. Tab and Shift+Tab must leave plots and reach later '
        'controls, including after a figure rebuild. Test pointer events when picking is advertised, '
        'read-only hover, invalid-input rollback, shared selection across clients, '
        'disconnection and close/disposal. Verify visible updates and mathematical readouts. '
        'Declare live Julia, static scene navigation and precomputed offline selection distinctly. '
        'At narrow widths, preserve readable scientific labels and keyboard/pointer access to wide '
        'charts; fitting the surrounding page alone does not establish readability.', '',
        '## Required checks for a change', '',
        '1. Update the family entry when adding a recipe, a backend or a new interaction. '
        'Provide an independent mathematical oracle and real backend assertions appropriate to it.',
        '2. For an advertised live control, add a browser scenario with real user input, '
        'readout/drawing assertions and lifecycle coverage. Preserve narrow-layout and keyboard access.',
        '3. Run the matrix validator and affected native/browser owners locally. The '
        '[Visualization CI workflow](https://github.com/erikmnovak/TamerOp.jl/blob/main/.github/workflows/Visualization.yml) requires both '
        'rendering extensions and runs all registered visualization owners, live Chromium, '
        'then no-server exported-HTML scenarios. Missing offline fixtures fail rather than skip.',
        '4. Review representative figures. Tests of coordinates, transport or DOM layout '
        'do not establish readability or a clear mathematical explanation.', '',
        'Commands and environment setup are in [testing](testing.md) and the '
        '[browser harness](https://github.com/erikmnovak/TamerOp.jl/blob/main/test/browser/README.md). These are contributor acceptance '
        'requirements; development status and test counts do not belong in mathematical lessons.', '',
        '## Evidence by family', '']
    for row in data['family']:
        links=lambda paths: ', '.join(f'[{Path(p).name}](https://github.com/erikmnovak/TamerOp.jl/blob/main/{p})' for p in paths)
        lines += [f'### {row["title"]}', '',row['scope'],'',
                  'Native owners: '+links(['test/'+p for p in row['native_tests']])+'.', '']
        if row['browser_tests']:
            lines += ['Browser scenarios: '+links(['test/browser/'+p for p in row['browser_tests']])+'.', '']
    return '\n'.join(lines)



def render_selected():
    data = tomllib.loads((package_root() / "test/visualization_support.toml").read_text())
    return render(data)
