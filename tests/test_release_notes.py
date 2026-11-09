"""Offline tests with fake Jira and fake LLM; no real credentials required."""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from tools.story_details import story_details_extractor
from tools.output_formatter import output_formatter


class FakeLLM:
    """Test object with an invoke() method, not a real LLM."""
    def invoke(self, messages):
        return SimpleNamespace(content="Draft based on provided test facts.")


class ReleaseNotesTests(unittest.TestCase):

    def test_story_details_extractor(self):
        issues = [{
            "key": "DEMO-11",
            "fields": {
                "summary": "Improve search",
                "description": {"type": "doc", "content": [
                    {"type": "paragraph", "content": [
                        {"type": "text", "text": "More accurate matching"}
                    ]}
                ]},
                "issuetype": {"name": "Story"},
                "status": {"name": "Done"},
            },
        }]
        records = story_details_extractor.invoke({"issues": issues})
        self.assertEqual(records[0]["key"], "DEMO-11")
        self.assertEqual(records[0]["description"], "More accurate matching")

    def test_output_formatter(self):
        text = output_formatter.invoke({"title": "Release Notes", "body": "Test"})
        self.assertEqual(text, "Release Notes\n\nTest\n")

    def test_maintenance_skips_jira(self):
        import backend
        user_input = {
            "project_key": "DEMO", "fix_version": "v1.0",
            "output_type": "maintenance", "impact": "Read-only mode",
        }
        with patch.object(backend, "get_llm", return_value=FakeLLM()), \
             patch.object(backend.jira_version_lookup, "invoke") as lookup, \
             patch.object(backend.jira_story_fetcher, "invoke") as fetch:
            draft = backend.run_release_workflow(user_input)
        self.assertIn("Maintenance Notice", draft)
        lookup.assert_not_called()
        fetch.assert_not_called()

    def test_release_notes_reads_jira(self):
        import backend
        user_input = {
            "project_key": "DEMO", "fix_version": "v1.0",
            "output_type": "release_notes",
        }
        with patch.object(backend, "get_llm", return_value=FakeLLM()), \
             patch.object(backend.jira_version_lookup, "invoke", return_value={"id": "123", "name": "v1.0"}) as lookup, \
             patch.object(backend.jira_story_fetcher, "invoke", return_value=[{"key": "DEMO-11", "fields": {}}]) as fetch:
            draft = backend.run_release_workflow(user_input)
        self.assertIn("Release Notes", draft)
        lookup.assert_called_once()
        fetch.assert_called_once()


if __name__ == "__main__":
    unittest.main()
