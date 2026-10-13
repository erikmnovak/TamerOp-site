"""The website must neither select a registry release nor confuse the repositories."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import publish
import source_paths
from check_update import matches


class ProjectBoundaryTests(unittest.TestCase):
    def test_library_and_site_links_have_distinct_owners(self):
        with tempfile.TemporaryDirectory() as folder:
            site, library = Path(folder) / "site", Path(folder) / "library"
            with patch.object(source_paths, "SITE", site), patch.object(source_paths, "package_root", return_value=library):
                self.assertEqual(source_paths.source_path(site / "docs", "library:CONTRIBUTING.md"), library / "CONTRIBUTING.md")
                self.assertEqual(source_paths.source_name(library / "src/TamerOp.jl"), "library:src/TamerOp.jl")
                self.assertIn("TamerOp.jl/blob/main/src/TamerOp.jl", source_paths.source_url(library / "src/TamerOp.jl"))
                self.assertIn("TamerOp-site/blob/main/docs/a.md", source_paths.source_url(site / "docs/a.md"))
                with self.assertRaises(ValueError):
                    source_paths.source_path(site, "library:../outside")

    def test_environment_rejects_registry_or_wrong_checkout(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); docs = root / "docs"; env = docs / ".build/environment"
            env.mkdir(parents=True); library = root / "library"
            project = '[deps]\nTamerOp = "40830518-3340-46e0-bdcb-56edef4036ff"\n'
            (docs / "Project.toml").write_text(project)
            (env / "Project.toml").write_text(project)
            with patch.multiple(publish, DOCS=docs, ENVIRONMENT=env, PACKAGE_ROOT=library):
                for entry in ('git-tree-sha1 = "registry"', 'path = "wrong"'):
                    (env / "Manifest.toml").write_text('[[deps.TamerOp]]\n' + entry + '\n')
                    with self.assertRaises(ValueError):
                        publish.validate_environment()
                (env / "Manifest.toml").write_text(f'[[deps.TamerOp]]\npath = "{library}"\n')
                publish.validate_environment()
                (docs / "Project.toml").write_text(project + '[compat]\njulia = "1.12"\n')
                with self.assertRaisesRegex(ValueError, "dependencies changed"):
                    publish.validate_environment()

    def test_schedule_only_skips_exact_clean_revisions(self):
        record = {"site": {"repository": "https://github.com/erikmnovak/TamerOp-site",
                            "git_commit": "site-sha", "working_tree_dirty": False},
                  "package_repository": "https://github.com/erikmnovak/TamerOp.jl",
                  "git_commit": "library-sha", "working_tree_dirty": False}
        self.assertTrue(matches(record, "site-sha", "library-sha"))
        self.assertFalse(matches(record, "site-sha", "new-library"))
        self.assertFalse(matches(record, "new-site", "library-sha"))
        self.assertFalse(matches({}, "site-sha", "library-sha"))
        dirty = copy.deepcopy(record); dirty['site']['working_tree_dirty'] = True
        self.assertFalse(matches(dirty, "site-sha", "library-sha"))


if __name__ == "__main__":
    unittest.main()
