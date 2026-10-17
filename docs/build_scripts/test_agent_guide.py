"""Check canonical source publication without Julia or private reference files."""
import copy
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import agent_guide
from publish import documenter_markdown, rewrite_links


class AgentGuideTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.package = self.root / "library"
        self.package.mkdir()
        self.stage = self.root / "site"
        self.stage.mkdir()
        self.guides = {"library:agent/README.md": "agents/index.md",
                       "library:agent/workflows/example.md": "agents/workflows/example.md"}
        self.files = {"README.md": "# Agent guide\n\n[Compute](workflows/example.md)\n",
                      "install_skill.jl": "# Install the skill\n",
                      "check_skill.jl": "# Check the skill\n",
                      "workflows/example.md": "# Example\n\n[Run](../examples/example.jl)\n",
                      "examples/example.jl": "@assert 1 + 1 == 2\n",
                      "skills/tamerop/SKILL.md": "---\nname: tamerop\n---\n# TamerOp\n",
                      "skills/tamerop/agents/openai.yaml": "interface:\n  display_name: TamerOp\n"}
        for name, text in self.files.items():
            path = self.package / "agent" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        (self.package / "Project.toml").write_text('name = "TamerOp"\nversion = "0.2.0"\n')
        subprocess.run(["git", "init", "-q", str(self.package)], check=True)
        subprocess.run(["git", "add", "."], cwd=self.package, check=True)
        subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.org",
                        "commit", "-qm", "Fixture"], cwd=self.package, check=True)

    def publish(self):
        record, files = agent_guide.snapshot(self.package, self.guides)
        agent_guide.stage_downloads(self.stage, record, files)
        # Markdown is installed after Documenter to keep it as Markdown, without
        # creating unlisted HTML copies in the download directory.
        self.assertFalse((self.stage / "downloads/agent/README.md").exists())
        agent_guide.install_downloads(self.stage, files)
        for name, route in record["routes"].items():
            page = self.stage / route
            page.parent.mkdir(parents=True, exist_ok=True)
            note = agent_guide.page_note(record, self.package / "agent" / name,
                                         self.package, page, self.stage)
            page.with_suffix(".html").write_text(note)
        publication = {"agent_guide": record,
                       "package_checkout": {"git_commit": record["library_revision"]}}
        return record, files, publication

    def test_exact_public_sources_are_downloadable_and_versioned(self):
        record, files, publication = self.publish()
        self.assertEqual(record["library_version"], "0.2.0")
        self.assertFalse(record["working_tree_dirty"])
        self.assertEqual(set(files), set(self.files))
        agent_guide.check_downloads(self.stage, publication, self.guides)
        for name, data in files.items():
            self.assertEqual((self.stage / "downloads/agent" / name).read_bytes(), data)
        with zipfile.ZipFile(self.stage / agent_guide.ARCHIVE_PATH) as archive:
            self.assertEqual(archive.read("agent/README.md"), files["README.md"])

    def test_missing_workflow_script_or_skill_fails_before_publication(self):
        for name in ("workflows/example.md", "examples/example.jl", "skills/tamerop/SKILL.md"):
            path = self.package / "agent" / name
            data = path.read_bytes()
            path.unlink()
            with self.assertRaisesRegex(ValueError, "Missing agent guide input"):
                agent_guide.snapshot(self.package, self.guides)
            path.write_bytes(data)

    def test_source_changes_and_dirty_checkout_are_recorded(self):
        initial, _ = agent_guide.snapshot(self.package, self.guides)
        (self.package / "agent/README.md").write_text("# Revised guide\n")
        changed, _ = agent_guide.snapshot(self.package, self.guides)
        self.assertTrue(changed["working_tree_dirty"])
        self.assertNotEqual(initial["files_sha256"], changed["files_sha256"])

    def test_symlinks_cannot_publish_files_outside_the_guide(self):
        (self.package / "agent/private.md").symlink_to(self.package / "Project.toml")
        with self.assertRaisesRegex(ValueError, "symlinks"):
            agent_guide.snapshot(self.package, self.guides)

    def test_guide_root_cannot_redirect_to_another_tree(self):
        directory = self.package / "agent"
        external = self.root / "other-guide"
        directory.rename(external)
        directory.symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            agent_guide.snapshot(self.package, self.guides)

    def test_changed_downloads_archives_or_provenance_fail(self):
        record, files, publication = self.publish()
        path = self.stage / "downloads/agent/examples/example.jl"
        path.write_text("broken\n")
        with self.assertRaisesRegex(ValueError, "download changed"):
            agent_guide.check_downloads(self.stage, publication, self.guides)
        path.write_bytes(files["examples/example.jl"])
        stale = copy.deepcopy(publication)
        stale["package_checkout"]["git_commit"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "selected library revision"):
            agent_guide.check_downloads(self.stage, stale, self.guides)
        with zipfile.ZipFile(self.stage / agent_guide.ARCHIVE_PATH, "w") as archive:
            archive.writestr("agent/README.md", files["README.md"])
        with self.assertRaisesRegex(ValueError, "different source set"):
            agent_guide.check_downloads(self.stage, publication, self.guides)

    def test_stale_routes_and_missing_download_entrances_fail(self):
        record, files, publication = self.publish()
        changed = {**self.guides, "library:agent/other.md": "agents/other.md"}
        with self.assertRaisesRegex(ValueError, "routes changed"):
            agent_guide.check_downloads(self.stage, publication, changed)
        (self.stage / "agents/index.html").write_text("<h1>Guide</h1>")
        with self.assertRaisesRegex(ValueError, "missing its source download"):
            agent_guide.check_downloads(self.stage, publication, self.guides)

    def test_guide_links_become_local_pages_and_exact_script_downloads(self):
        page = self.stage / "agents/index.md"
        source = self.package / "agent/README.md"
        workflow = self.package / "agent/workflows/example.md"
        example = self.package / "agent/examples/example.jl"
        pages = {source: page, workflow: self.stage / "agents/workflows/example.md",
                 example: self.stage / "downloads/agent/examples/example.jl"}
        with patch.dict(os.environ, {"TAMEROP_SOURCE": str(self.package)}):
            self.assertIn("](workflows/example.md)", rewrite_links(source.read_text(), source,
                          page, pages, self.stage))
            self.assertIn("](../../downloads/agent/examples/example.jl)", rewrite_links(
                workflow.read_text(), workflow, pages[workflow], pages, self.stage))
        record, _ = agent_guide.snapshot(self.package, self.guides)
        note = agent_guide.page_note(record, source, self.package, page, self.stage)
        self.assertIn('href="../downloads/agent/README.md"', documenter_markdown(note))


if __name__ == "__main__":
    unittest.main()
