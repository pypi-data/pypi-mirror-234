from collections import namedtuple
import logging
from typing import Any, Dict, Generator
from jira import JIRA

# jira renamed this between api versions for some reason
try:
    from jira.resources import AgileResource as AGILE_BASE_REST_PATH
except ImportError:
    from jira.resources import GreenHopperResource as AGILE_BASE_REST_PATH

logger = logging.getLogger(__name__)


def get_jira_connection(config, creds, max_retries=3) -> JIRA:
    kwargs = {
        "server": config.jira_url,
        "max_retries": max_retries,
        "options": {
            "agile_rest_path": AGILE_BASE_REST_PATH,
            "verify": not config.skip_ssl_verification,
        },
    }

    if creds.jira_username and creds.jira_password:
        kwargs["basic_auth"] = (creds.jira_username, creds.jira_password)
    elif creds.jira_bearer_token:
        kwargs["options"]["headers"] = {
            "Authorization": f"Bearer {creds.jira_bearer_token}",
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Atlassian-Token": "no-check",
        }
    else:
        raise RuntimeError(
            "No valid Jira credentials found! Check your JIRA_USERNAME, JIRA_PASSWORD, or JIRA_BEARER_TOKEN environment variables."
        )

    jira_connection = JIRA(**kwargs)

    jira_connection._session.headers[
        "User-Agent"
    ] = f'jellyfish/1.0 ({jira_connection._session.headers["User-Agent"]})'

    return jira_connection


def download_fields(
    jira_connection: JIRA, include_fields=[], exclude_fields=[]
) -> list[dict]:
    logger.info("downloading jira fields... ")

    filters = []
    if include_fields:
        filters.append(lambda field: field["id"] in include_fields)
    if exclude_fields:
        filters.append(lambda field: field["id"] not in exclude_fields)

    fields = [
        field
        for field in jira_connection.fields()
        if all(filter(field) for filter in filters)
    ]

    logger.info("✓")
    return fields


def download_projects_and_versions(
    jira_connection: JIRA,
    include_projects,
    exclude_projects,
    include_categories,
    exclude_categories,
) -> list[dict]:
    return []


def download_users(
    jira_connection,
    gdpr_active,
    quiet=False,
    required_email_domains=None,
    is_email_required=False,
) -> list[dict]:
    return []


def download_resolutions(jira_connection) -> list[dict]:
    return []


def download_issuetypes(jira_connection, project_ids) -> list[dict]:
    return []


def download_issuelinktypes(jira_connection) -> list[dict]:
    return []


def download_priorities(jira_connection) -> list[dict]:
    return []


def download_projects_and_versions(
    jira_connection,
    include_projects,
    exclude_projects,
    include_categories,
    exclude_categories,
) -> list[dict]:
    return []


def download_boards_and_sprints(
    jira_connection: JIRA, project_ids, download_sprints
) -> list[dict]:
    return []


def get_issues(jira_connection, issue_jql, start_at, batch_size) -> list[dict]:
    return []


# TODO: Make this a dataclass. Not a fan of namedtuple
IssueMetadata = namedtuple("IssueMetadata", ("key", "updated"))


def download_all_issue_metadata(
    jira_connection,
    all_project_ids,
    earliest_issue_dt,
    num_parallel_threads,
    issue_filter,
) -> Dict[int, IssueMetadata]:
    return []


def detect_issues_needing_sync(
    issue_metadata_from_jira: Dict[int, IssueMetadata],
    issue_metadata_from_jellyfish: Dict[int, IssueMetadata],
) -> list[dict]:
    return []


def download_worklogs(jira_connection, issue_ids, work_logs_pull_from) -> list[dict]:
    return []


# Returns an array of CustomFieldOption items
def download_customfieldoptions(jira_connection, project_ids) -> list[dict]:
    return []


def download_statuses(jira_connection) -> list[dict]:
    return []


def detect_issues_needing_re_download(
    downloaded_issue_id_and_key_tuples: set[tuple[str, str]],
    issue_metadata_from_jellyfish,
    issue_metadata_addl_from_jellyfish,
) -> list[dict]:
    return []


def download_necessary_issues(
    jira_connection,
    issue_ids_to_download,
    include_fields,
    exclude_fields,
    num_parallel_threads,
    suggested_batch_size: int = 2000,
) -> Generator[Any, None, None]:
    return []
