import os

import requests_mock
from unittest import TestCase

from jf_ingest.jf_jira.downloaders import get_jira_connection, download_fields

MOCK_SERVER_INFO_RESP = (
    '{"baseUrl":"https://test-co.atlassian.net","version":"1001.0.0-SNAPSHOT",'
    '"versionNumbers":[1001,0,0],"deploymentType":"Cloud","buildNumber":100218,'
    '"buildDate":"2023-03-16T08:21:48.000-0400","serverTime":"2023-03-17T16:32:45.255-0400",'
    '"scmInfo":"9999999999999999999999999999999999999999","serverTitle":"JIRA",'
    '"defaultLocale":{"locale":"en_US"}} '
)


def get_connection(mocker: requests_mock.Mocker):
    class PartialConfig:
        jira_url = "https://test-co.atlassian.net/"
        skip_ssl_verification = False

    class PartialCreds:
        jira_password = None
        jira_username = None
        jira_bearer_token = "asdf"

    config = PartialConfig()
    creds = PartialCreds()
    # you can test behavior against a live jira instance by setting an email as `jira_username`
    # and storing a generated token in env and retrieving like so:
    # creds.jira_bearer_token = os.environ.get('JIRA_TOKEN')

    # https://test-co.atlassian.net/rest/api/2/serverInfo
    mocker.register_uri(
        "GET",
        "https://test-co.atlassian.net/rest/api/2/serverInfo",
        text=f"{MOCK_SERVER_INFO_RESP}",
    )
    jira_conn = get_jira_connection(config, creds, max_retries=1)

    return jira_conn


class TestJiraDownload(TestCase):
    URL_BASE = "https://test-co.atlassian.net/rest/api/2/search"

    start_at = 0
    max_results = 100

    jira_connection = None
    mock_field_response = None

    @classmethod
    def setUpClass(cls):
        with open(
            f"{os.path.dirname(__file__)}/fixtures/jira_fields_response.json", "r"
        ) as file:
            cls.mock_field_response = file.read()
        with requests_mock.Mocker() as m:
            m.register_uri(
                "GET",
                "https://test-co.atlassian.net/rest/api/2/field",
                text=f"{cls.mock_field_response}",
            )
            cls.jira_connection = get_connection(m)

    def test_get_fields_once(self):
        expected_field = {
            "id": "statuscategorychangedate",
            "key": "statuscategorychangedate",
            "name": "Status Category Changed",
            "custom": False,
            "orderable": False,
            "navigable": True,
            "searchable": True,
            "clauseNames": ["statusCategoryChangedDate"],
            "schema": {"type": "datetime", "system": "statuscategorychangedate"},
        }

        with requests_mock.Mocker() as m:
            m.register_uri(
                "GET",
                "https://test-co.atlassian.net/rest/api/2/field",
                text=self.mock_field_response,
            )
            fields = download_fields(
                jira_connection=self.jira_connection,
                include_fields=[],
                exclude_fields=[],
            )

        self.assertEqual(4, len(fields))
        self.assertEqual(expected_field, fields[0])
        for field in fields:
            self.assertIn("id", field.keys())
            self.assertIn("key", field.keys())
            self.assertIn("name", field.keys())

    def test_get_fields_exclude_list(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                "GET",
                "https://test-co.atlassian.net/rest/api/2/field",
                text=self.mock_field_response,
            )
            fields = download_fields(
                jira_connection=self.jira_connection,
                include_fields=[],
                exclude_fields=["customfield_10070"],
            )

        self.assertEqual(3, len(fields))

    def test_get_fields_include_list(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                "GET",
                "https://test-co.atlassian.net/rest/api/2/field",
                text=self.mock_field_response,
            )
            fields = download_fields(
                jira_connection=self.jira_connection,
                include_fields=["customfield_10070"],
                exclude_fields=[],
            )

        self.assertEqual(1, len(fields))
