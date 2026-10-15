"""Verify Documenter integration and catalog navigation independently of Julia."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from site_shell import Structure, finalize_site, relative_url, transform


ARTICLE = r'''<article class="content" id="documenter-page"><h1 id="title">Title</h1>
<p>\(M \\cong \\pi^* N\) &amp; <code>x &lt; y</code></p>
<h2 id="first"><a class="docs-heading-anchor" href="#first">A space &amp; map</a><a id="first-1"></a><a class="docs-heading-anchor-permalink" href="#first"></a></h2>
<pre><code class="language-julia">x &lt; y\n"$literal"</code></pre>
<details><summary>Optional</summary><h3 id="detail">Matrix coordinates</h3><p>Read me.</p></details>
<h2 id="empty"><a href="#empty"></a></h2>
<img src="plot.svg" alt="An exact diagram"/>
</article>'''
FOOTER = '<nav class="docs-footer"><div class="lesson-continuation"><a href="../tameness.html">Next</a></div></nav>'
HTML = ('''<!doctype html><html><head><meta charset="UTF-8"/><script src="../assets/documenter.js"></script></head>
<body><div id="documenter"><nav class="docs-sidebar"><div class="docs-package-name"><span class="docs-autofit"><a href="../index.html">TamerOp.jl</a></span></div>
<button class="docs-search-query" id="documenter-search-query">Search docs</button><ul class="docs-menu"><li><a href="old.html">Old menu</a></li></ul>
<div class="docs-version-selector"><select id="documenter-version-selector"></select></div></nav>
<div class="docs-main"><header class="docs-navbar"><a id="documenter-sidebar-button" class="docs-sidebar-button" href="#"></a><a id="documenter-settings-button" href="#">Settings</a></header>'''
        + ARTICLE + FOOTER + '</div></div></body></html>')


def catalog():
    record = dict(title="Selected article", type="library_guide", type_label="Library guide",
                  topics=["encodings"], question="What can I inspect?", collection="using")
    return {
        "pages": {"guides/current.html": record},
        "anchors": dict(home="index.html", install="start/install.html", learning="reading_map.html",
                        topics="topics/index.html", contributing="contributing/index.html"),
        "collections": [dict(id="using", title="Using TamerOp", page="collections/using.html",
                             grouped_sidebar=False,
                             items=[dict(page="guides/current.html", **record)]),
                        dict(id="implementation", title="Implementation", page="implementation/index.html",
                             grouped_sidebar=False, items=[]),
                        dict(id="contributing", title="Contributing", page="contributing/index.html",
                             grouped_sidebar=False, items=[])],
        "topics": [dict(id="encodings", title="Finite encodings", page="topics/encodings.html", articles=[])]}


class ShellTests(unittest.TestCase):
    def test_preserves_article_footer_and_documenter_controls_exactly(self):
        output = transform(HTML, "guides/current.html", catalog())
        self.assertIn(ARTICLE, output)
        self.assertIn(FOOTER, output)
        self.assertIn('<a id="documenter-settings-button" href="#">Settings</a>', output)
        self.assertIn('<button class="docs-search-query" id="documenter-search-query">Search docs</button>', output)
        self.assertNotIn("Old menu", output)
        structure = Structure(output)
        self.assertEqual(structure.one(id="documenter-sidebar-button").tag, "button")
        self.assertEqual(structure.one(id="documenter-sidebar-button").attrs["aria-controls"], "site-navigation")
        self.assertEqual(len([n for n in structure.elements if n.attrs.get("id") == "first"]), 1)
        self.assertIn('src="../assets/site_navigation.js"', output)
        self.assertIn('href="../assets/site_navigation.css"', output)

    def test_fixed_entry_links_active_collection_and_contributor_footer(self):
        output = transform(HTML, "guides/current.html", catalog())
        structure = Structure(output)
        current = [n for n in structure.elements if n.attrs.get("aria-current") == "page"]
        self.assertEqual(len(current), 1)
        self.assertEqual(current[0].attrs["href"], "current.html")
        self.assertNotIn("is-active", current[0].attrs.get("class", "").split())
        groups = [n for n in structure.elements if n.tag == "details" and "data-collection" in n.attrs]
        self.assertEqual([n.attrs["data-collection"] for n in groups], ["using", "implementation"])
        self.assertIn("open", groups[0].attrs)
        self.assertNotIn("open", groups[1].attrs)
        self.assertIn("Learning map", output)
        self.assertIn("Contributors &amp; contributing", output)
        self.assertLess(output.index('class="site-entry-links"'), output.index('class="docs-menu site-collections"'))
        self.assertLess(output.index('class="docs-menu site-collections"'), output.index('class="site-nav-bottom"'))

    def test_one_local_outline_with_heading_depth_and_no_empty_or_copied_ids(self):
        output = transform(HTML, "guides/current.html", catalog())
        structure = Structure(output)
        outline = structure.one(class_name="site-outline")
        contents = output[outline.start:outline.end]
        self.assertIn("site-outline-h2", contents)
        self.assertIn("site-outline-h3", contents)
        self.assertIn('href="#first">A space &amp; map', contents)
        self.assertNotIn('href="#empty"', contents)
        self.assertNotIn('id="first"', contents)
        self.assertLess(outline.end, structure.one(id="documenter-page").start + 1)
        no_headings = HTML.replace(ARTICLE, '<article class="content" id="documenter-page"><h1>Only a title</h1></article>')
        self.assertNotIn('class="site-outline"', transform(no_headings, "guides/current.html", catalog()))

    def test_grouped_catalog_exposes_articles_and_opens_only_the_current_topic(self):
        config = catalog()
        group = config["collections"][0]
        group["grouped_sidebar"] = True
        group["items"].extend(dict(page=f"guides/extra{i}.html", title=f"Other article {i}", topics=["encodings"])
                              for i in range(70))
        group["topic_groups"] = [dict(id="encodings", title="Finite encodings",
                                      page="collections/using/topics/encodings.html", overview_title="Choosing a guide", items=group["items"]),
                                 dict(id="algebra", title="Modules & maps",
                                      page=None,
                                      items=[dict(page="guides/maps.html", title="Inspecting maps")])]
        output = transform(HTML, "guides/current.html", config)
        parsed = Structure(output)
        menu = parsed.one(class_name="site-collections")
        contents = output[menu.start:menu.end]
        self.assertIn('href="../collections/using/topics/encodings.html"', contents)
        self.assertIn('aria-current="page"', contents)
        self.assertNotIn("Current page", contents)
        self.assertIn("Other article 69", contents)
        topics = [n for n in parsed.elements if "data-topic" in n.attrs]
        self.assertEqual(len(topics), 2)
        self.assertIn("open", topics[0].attrs)
        self.assertNotIn("open", topics[1].attrs)
        for topic in topics:
            summary = next(n for n in parsed.elements if n.parent is topic and n.tag == "summary")
            self.assertNotIn("<a", output[summary.inner:summary.stop])
            self.assertNotIn("Topic overview", output[topic.inner:topic.stop])
            entry = topic.parent
            heading = next(n for n in parsed.elements if n.parent is entry
                           and 'site-topic-heading' in n.attrs.get('class', '').split())
            button = next(n for n in parsed.elements if n.parent is heading and n.tag == 'button')
            self.assertIn('hidden', button.attrs, 'Native disclosure is the no-JS fallback')
            self.assertEqual(button.attrs['aria-expanded'], str('open' in topic.attrs).lower())
            self.assertIs(parsed.one(id=button.attrs['aria-controls']).parent, topic)
        title_link = next(n for n in parsed.elements if 'site-topic-link' in n.attrs.get('class', '').split())
        self.assertEqual(output[title_link.inner:title_link.stop], 'Finite encodings')
        self.assertFalse(topics[0].start < title_link.start < topics[0].end,
                         'The overview link stays outside the collapsible content')
        self.assertNotIn('Choosing a guide', contents)
        self.assertEqual(contents.count('href="../collections/using/topics/encodings.html"'), 1)
        current = [n for n in parsed.elements if n.attrs.get("aria-current") == "page"]
        self.assertEqual(len(current), 1)
        self.assertTrue(topics[0].start < current[0].start < topics[0].end)
        group_page = group["topic_groups"][0]["page"]
        config["pages"][group_page] = dict(title="Finite encodings", collection="using", type="resource")
        topic_output = transform(HTML, group_page, config)
        topic_structure = Structure(topic_output)
        self.assertEqual(len([n for n in topic_structure.elements if n.attrs.get("aria-current") == "page"]), 1)
        self.assertEqual(next(n for n in topic_structure.elements if n.attrs.get("aria-current") == "page").tag, "a")
        self.assertIn("open", next(n for n in topic_structure.elements if n.attrs.get("data-topic") == "encodings").attrs)
        active_title = next(n for n in topic_structure.elements if n.attrs.get('aria-current') == 'page')
        self.assertIn('site-topic-link', active_title.attrs.get('class', '').split())

    def test_grouped_catalog_keeps_articles_without_a_topic_and_related_links(self):
        config = catalog()
        group = config["collections"][0]
        group["grouped_sidebar"] = True
        external = dict(page="implementation/method.html", title="How it works", type_label="Implementation account")
        group["topic_groups"] = [dict(id="related", title="Related methods",
                                      page=None, items=[external])]
        config["collections"][1]["items"] = [external]
        config["pages"][external["page"]] = dict(title=external["title"], collection="implementation")
        output = transform(HTML, "guides/current.html", config)
        self.assertIn('href="current.html"', output)
        external_output = transform(HTML, external["page"], config)
        parsed = Structure(external_output)
        active = [n for n in parsed.elements if n.attrs.get("aria-current") == "page"]
        self.assertEqual(len(active), 1)
        self.assertIn("Implementation account", external_output)
        self.assertNotIn("open", next(n for n in parsed.elements if n.attrs.get("data-topic") == "related").attrs)

    def test_topic_without_child_guides_has_a_link_without_empty_controls(self):
        config = catalog()
        group = config["collections"][0]
        group["grouped_sidebar"] = True
        route = "collections/using/topics/data_io.html"
        group["topic_groups"] = [dict(id="data_io", title="Data and saving", page=route,
                                      overview_title="Data and saving", items=[])]
        config["pages"][route] = dict(title="Data and saving", collection="using", type="resource")
        output = transform(HTML, route, config)
        parsed = Structure(output)
        entry = parsed.one(class_name="site-topic-leaf")
        contents = output[entry.start:entry.end]
        self.assertIn('href="data_io.html"', contents)
        self.assertIn('aria-current="page"', contents)
        self.assertNotIn('<button', contents)
        self.assertNotIn('<details', contents)
        self.assertNotIn('Current page', contents)

    def test_retained_subject_pages_do_not_force_a_small_collection_into_groups(self):
        config = catalog()
        group = config["collections"][0]
        subject_page = "collections/using/topics/encodings.html"
        group["topic_groups"] = [dict(id="encodings", title="Finite encodings",
                                      page=subject_page, items=group["items"])]
        config["pages"][subject_page] = dict(title="Finite encodings", collection="using", type="resource")
        output = transform(HTML, "guides/current.html", config)
        menu = Structure(output).one(class_name="site-collections")
        contents = output[menu.start:menu.end]
        active = [n for n in Structure(output).elements if n.attrs.get("aria-current") == "page"]
        self.assertEqual([n.attrs["href"] for n in active], ["current.html"])
        self.assertNotIn('href="../collections/using/topics/encodings.html"', contents)
        self.assertNotIn('Current page', contents)

        subject_output = transform(HTML, subject_page, config)
        parsed = Structure(subject_output)
        active = [n for n in parsed.elements if n.attrs.get("aria-current") == "page"]
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].attrs["href"], "encodings.html")
        self.assertIn('data-collection="using" open', subject_output)

    def test_supporting_resource_retains_current_collection_context(self):
        config = catalog()
        config["pages"]["implementation/references.html"] = dict(
            title="Bibliography", type="resource", collection="implementation", topics=[])
        output = transform(HTML, "implementation/references.html", config)
        parsed = Structure(output)
        active = [n for n in parsed.elements if n.attrs.get("aria-current") == "page"]
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].attrs['href'], 'references.html')
        self.assertIn('data-collection="implementation" open', output)

    def test_metadata_is_safe_and_identifies_real_search_destinations(self):
        config = catalog()
        config["pages"]["guides/current.html"]["title"] = "</script><p>Bad & title"
        output = transform(HTML, "guides/current.html", config)
        parsed = Structure(output)
        script = parsed.one(id="site-catalog")
        payload = output[script.inner:script.stop]
        self.assertNotIn("</script>", payload)
        data = json.loads(payload)
        self.assertEqual(data["root"], "../")
        self.assertEqual(data["pages"]["guides/current.html"]["type_label"], "Library guide")
        self.assertEqual(data["topics"]["encodings"], "Finite encodings")

    def test_fail_fast_for_changed_upstream_dom_and_double_finalization(self):
        for broken in [HTML.replace('class="docs-sidebar"', 'class="moved-sidebar"'),
                       HTML.replace('id="documenter-search-query"', 'id="new-search"'),
                       HTML.replace('id="documenter-page"', 'id="new-article"')]:
            with self.assertRaisesRegex(ValueError, "Expected one HTML element"):
                transform(broken, "guides/current.html", catalog())
        once = transform(HTML, "guides/current.html", catalog())
        with self.assertRaisesRegex(ValueError, "already present"):
            transform(once, "guides/current.html", catalog())

    def test_urls_are_portable_and_cannot_escape_site(self):
        self.assertEqual(relative_url("topics/finite/index.html", "start/install.html"), "../../start/install.html")
        self.assertEqual(relative_url("index.html", "a space.html#some heading"), "a%20space.html#some%20heading")
        for target in ["/tmp/a.html", "../a.html", "#heading"]:
            with self.assertRaises(ValueError):
                relative_url("index.html", target)

    def test_finalize_checks_all_pages_before_replacing_any(self):
        with tempfile.TemporaryDirectory() as name:
            docs = Path(name)
            (docs / '.build/src').mkdir(parents=True)
            (docs / '.build/src/catalog.json').write_text(json.dumps(catalog()))
            (docs / 'build/guides').mkdir(parents=True)
            good = docs / 'build/guides/current.html'
            good.write_text(HTML)
            bad = docs / 'build/z.html'
            bad.write_text(HTML.replace('class="docs-sidebar"', 'class="unsupported"'))
            assets = docs / 'src/assets'
            assets.mkdir(parents=True)
            for filename in ['site_navigation.css', 'site_navigation.js']:
                (assets / filename).write_text('/* asset */')
            with self.assertRaises(ValueError):
                finalize_site(docs)
            self.assertEqual(good.read_text(), HTML)


if __name__ == '__main__':
    unittest.main()
