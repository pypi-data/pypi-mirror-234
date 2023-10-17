import json
import unittest

from click.testing import CliRunner

from src.lrn_cli import cli


class TestCli(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_annotations(self):
        request = {"group_id": "a91faa6e-8bd2-4365-872d-f644f1f41853"}
        request_json = json.dumps(request)
        result = self.runner.invoke(cli, ["-R", request_json, "annotations", "annotations"])
        self.assertIsNone(result.exception, "Unexpected exception")
        self.assertEqual(result.exit_code, 0, "Non-zero exit code")

    def test_author(self):
        result = self.runner.invoke(cli, ["author", "itembank/itemlist"])
        self.assertIsNone(result.exception, "Unexpected exception")
        self.assertEqual(result.exit_code, 0, "Non-zero exit code")

    def test_data(self):
        result = self.runner.invoke(cli, ["data", "itembank/items"])
        self.assertIsNone(result.exception, "Unexpected exception")
        self.assertEqual(result.exit_code, 0, "Non-zero exit code")

    def test_events(self):
        result = self.runner.invoke(cli, ["-R", "{}", "events", "authenticate", "-u", "test"])
        self.assertIsNone(result.exception, "Unexpected exception")
        self.assertEqual(result.exit_code, 0, "Non-zero exit code")

    def test_items(self):
        request = {
            "user_id": "lrn-cli",
            "activity_id": "lrn-cli_test",
            "session_id": "e0fa16e3-e763-4125-8708-60c04251de47",
            "rendering_type": "assess",
            "items": ["item_1"],
            "name": "lrn-cli test",
        }
        request_json = json.dumps(request)
        result = self.runner.invoke(cli, ["-R", request_json, "items", "activity"])
        self.assertIsNone(result.exception, "Unexpected exception")
        self.assertEqual(result.exit_code, 0, "Non-zero exit code")

    def test_questions(self):
        usrequest = {
            "questionResponseIds": [
                "0034_demo-user_04c389f8-a306-4f11-b259-105dc4c6932d_f167c24c98ea6415d9a7b227714f491d"
            ],
        }
        usrequest_json = json.dumps(usrequest)
        result = self.runner.invoke(
            cli, ["-R", "{}", "-U", usrequest_json, "questions", "questionresponses", "-u", "test"]
        )
        self.assertIsNone(result.exception, "Unexpected exception")
        self.assertEqual(result.exit_code, 0, "Non-zero exit code")

    def test_reports(self):
        request = {
            "reports": [
                {
                    "user_id": "test_student",
                    "session_id": "6e15d841-e6f0-419f-9fa5-eac62b7b102b",
                    "id": "session-detail-by-item",
                    "type": "session-detail-by-item",
                }
            ]
        }

        request_json = json.dumps(request)
        result = self.runner.invoke(cli, ["-R", request_json, "reports", "init"])
        self.assertIsNone(result.exception, "Unexpected exception")
        self.assertEqual(result.exit_code, 0, "Non-zero exit code")
