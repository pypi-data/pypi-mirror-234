#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Jira integration for RegScale CLI """

# Standard python imports
import os
import tempfile
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from typing import Tuple, Optional

import click
from jira import JIRA, Issue as jiraIssue, JIRAError

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    check_file_path,
    check_license,
    convert_datetime_to_regscale_string,
    compute_hashes_in_directory,
    create_progress_object,
    error_and_exit,
    get_current_datetime,
    save_data_to,
)
from regscale.core.app.utils.regscale_utils import verify_provided_module
from regscale.core.app.utils.threadhandler import create_threads, thread_assignment
from regscale.models import regscale_id, regscale_module
from regscale.models.regscale_models.issue import Issue
from regscale.models.regscale_models.files import File

# global variables
job_progress = create_progress_object()
logger = create_logger()
update_issues = []
new_regscale_issues = []
updated_regscale_issues = []
update_counter = []
JIRA_FIELDS = ["key", "summary", "description", "status", "duedate", "priority"]


####################################################################################################
#
# PROCESS ISSUES TO JIRA
# JIRA CLI Python Docs: https://jira.readthedocs.io/examples.html#issues
# JIRA API Docs: https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/
#
####################################################################################################


# Create group to handle Jira integration
@click.group()
def jira():
    """Sync issues between Jira and RegScale."""


@jira.command()
@regscale_id()
@regscale_module()
@click.option(
    "--jira_project",
    type=click.STRING,
    help="RegScale will sync the issues for the record to the Jira project.",
    prompt="Enter the name of the project in Jira",
    required=True,
)
@click.option(
    "--jira_issue_type",
    type=click.STRING,
    help="Enter the Jira issue type to use when creating new issues from RegScale. (CASE SENSITIVE)",
    prompt="Enter the Jira issue type",
    required=True,
)
@click.option(
    "--sync_attachments",
    type=click.BOOL,
    help=(
        "Whether RegScale will sync the attachments for the issue "
        "in the provided Jira project and vice versa. Defaults to True."
    ),
    required=False,
    default=True,
)
def issues(
    regscale_id: int,
    regscale_module: str,
    jira_project: str,
    jira_issue_type: str,
    sync_attachments: bool = True,
):
    """Sync issues from Jira into RegScale."""
    sync_regscale_and_jira(
        parent_id=regscale_id,
        parent_module=regscale_module,
        jira_project=jira_project,
        jira_issue_type=jira_issue_type,
        sync_attachments=sync_attachments,
    )


def sync_regscale_and_jira(
    parent_id: int,
    parent_module: str,
    jira_project: str,
    jira_issue_type: str,
    sync_attachments: bool = True,
) -> None:
    """
    Sync issues from Jira into RegScale as issues
    :param int parent_id: ID # from RegScale to associate issues with
    :param str parent_module: RegScale module to associate issues with
    :param str jira_project: Name of the project in Jira
    :param str jira_issue_type: Type of issues to sync from Jira
    :param bool sync_attachments: Whether to sync attachments in RegScale & Jira, defaults to True
    :return: None
    """
    app = check_license()
    api = Api(app)
    config = app.config

    # see if provided RegScale Module is an accepted option
    verify_provided_module(parent_module)

    jira_client = create_jira_client(config)

    (
        regscale_issues,
        regscale_attachments,
    ) = Issue.fetch_issues_and_attachments_by_parent(
        app=app,
        parent_id=parent_id,
        parent_module=parent_module,
        fetch_attachments=sync_attachments,
    )
    jira_issues = fetch_jira_issues(
        jira_client=jira_client,
        jira_project=jira_project,
        fetch_attachments=sync_attachments,
    )

    if regscale_issues:
        # sync RegScale issues to Jira
        if issues_to_update := sync_regscale_to_jira(
            regscale_issues=regscale_issues,
            jira_client=jira_client,
            jira_project=jira_project,
            jira_issue_type=jira_issue_type,
            sync_attachments=sync_attachments,
            attachments=regscale_attachments,
        ):
            with job_progress:
                # create task to update RegScale issues
                updating_issues = job_progress.add_task(
                    f"[#f8b737]Updating {len(issues_to_update)} RegScale issue(s) from Jira...",
                    total=len(issues_to_update),
                )
                # create threads to analyze Jira issues and RegScale issues
                create_threads(
                    process=update_regscale_issues,
                    args=(
                        issues_to_update,
                        api,
                        updating_issues,
                    ),
                    thread_count=len(issues_to_update),
                )
                # output the final result
                logger.info(
                    "%i/%i issue(s) updated in RegScale.",
                    len(issues_to_update),
                    len(update_counter),
                )
    else:
        logger.info("No issues need to be updated in RegScale.")

    if jira_issues:
        # sync Jira issues to RegScale
        with job_progress:
            # create task to create RegScale issues
            creating_issues = job_progress.add_task(
                f"[#f8b737]Analyzing {len(jira_issues)} Jira issue(s)"
                f" and {len(regscale_issues)} RegScale issue(s)...",
                total=len(jira_issues),
            )
            # create threads to analyze Jira issues and RegScale issues
            create_threads(
                process=create_and_update_regscale_issues,
                args=(
                    jira_issues,
                    regscale_issues,
                    sync_attachments,
                    config,
                    app,
                    parent_id,
                    parent_module,
                    creating_issues,
                ),
                thread_count=len(jira_issues),
            )
            # output the final result
            logger.info(
                "Analyzed %i Jira issue(s), created %i issue(s) and updated %i issue(s) in RegScale.",
                len(jira_issues),
                len(new_regscale_issues),
                len(updated_regscale_issues),
            )
    else:
        logger.info("No issues need to be analyzed from Jira.")


def create_jira_client(
    config: dict,
) -> JIRA:
    """
    Create a Jira client to use for interacting with Jira
    :param dict config: RegScale CLI application config
    :return: JIRA Client
    :rtype: JIRA
    """
    url = config["jiraUrl"]
    token = config["jiraApiToken"]
    jira_user = config["jiraUserName"]

    # set the JIRA Url
    return JIRA(basic_auth=(jira_user, token), options={"server": url})


def update_regscale_issues(args: Tuple, thread: int) -> None:
    """
    Function to compare Jira issues and RegScale issues
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :raises: RequestException if unable to update RegScale issue
    :return: None
    """
    # set up local variables from the passed args
    (
        regscale_issues,
        app,
        task,
    ) = args
    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(regscale_issues))
    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the issue for the thread for later use in the function
        issue = regscale_issues[threads[i]]
        # update the issue in RegScale
        Issue.update_issue(app=app, issue=issue)
        logger.info(
            "RegScale Issue %i was updated with the Jira link.",
            issue.id,
        )
        update_counter.append(issue)
        # update progress bar
        job_progress.update(task, advance=1)


def create_and_update_regscale_issues(args: Tuple, thread: int) -> None:
    """
    Function to create or update issues in RegScale from Jira
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :raises: RequestException if unable to update RegScale issue
    :return: None
    """
    # set up local variables from the passed args
    (
        jira_issues,
        regscale_issues,
        add_attachments,
        config,
        app,
        parent_id,
        parent_module,
        task,
    ) = args
    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(jira_issues))

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        jira_issue: jiraIssue = jira_issues[threads[i]]
        regscale_issue: Optional[Issue] = next(
            (issue for issue in regscale_issues if issue.jiraId == jira_issue.key), None
        )
        # see if the Jira issue needs to be created in RegScale
        if jira_issue.fields.status.name.lower() == "done" and regscale_issue:
            # update the status and date completed of the RegScale issue
            regscale_issue.status = "Closed"
            regscale_issue.dateCompleted = get_current_datetime()
            # update the issue in RegScale
            updated_regscale_issues.append(
                Issue.update_issue(app=app, issue=regscale_issue)
            )
        elif regscale_issue:
            # update the issue in RegScale
            updated_regscale_issues.append(
                Issue.update_issue(app=app, issue=regscale_issue)
            )
        else:
            # map the jira issue to a RegScale issue object
            issue = map_jira_to_regscale_issue(
                jira_issue=jira_issue,
                config=config,
                parent_id=parent_id,
                parent_module=parent_module,
            )
            # create the issue in RegScale
            if regscale_issue := Issue.insert_issue(
                app=app,
                issue=issue,
            ):
                if regscale_issue.id:
                    logger.debug(
                        "Created issue #%i-%s in RegScale.",
                        regscale_issue.id,
                        regscale_issue.title,
                    )
                else:
                    logger.warning(
                        "Unable to create issue in RegScale.\nIssue: %s", issue.dict()
                    )
                new_regscale_issues.append(regscale_issue)
        if add_attachments and regscale_issue:
            # determine which attachments need to be uploaded to prevent duplicates by
            # getting the hashes of all Jira & RegScale attachments
            compare_files_for_dupes_and_upload(
                jira_issue=jira_issue,
                regscale_issue=regscale_issue,
                jira_client=create_jira_client(config),
                api=Api(app),
            )
        # update progress bar
        job_progress.update(task, advance=1)


def sync_regscale_to_jira(
    regscale_issues: list[Issue],
    jira_client: JIRA,
    jira_project: str,
    jira_issue_type: str,
    sync_attachments: bool = True,
    attachments: Optional[dict] = None,
) -> list[Issue]:
    """
    Sync issues from RegScale to Jira
    :param list regscale_issues: list of RegScale issues to sync to Jira
    :param JIRA jira_client: Jira client to use for issue creation in Jira
    :param str jira_project: Jira Project to create the issues in
    :param str jira_issue_type: Type of issue to create in Jira
    :param bool sync_attachments: Sync attachments from RegScale to Jira, defaults to True
    :param dict attachments: Dict of attachments to sync from RegScale to Jira, defaults to None
    :return: list of RegScale issues that need to be updated
    :rtype: list[Issue]
    """
    new_issue_counter = 0
    issuess_to_update = []
    for issue in regscale_issues:
        # see if Jira issue already exists
        if not issue.jiraId or issue.jiraId == "":
            new_issue = create_issue_in_jira(
                issue=issue,
                jira_client=jira_client,
                jira_project=jira_project,
                issue_type=jira_issue_type,
                add_attachments=sync_attachments,
                attachments=attachments,
            )
            # log progress
            new_issue_counter += 1
            # get the Jira ID
            jira_id = new_issue.key
            # update the RegScale issue for the Jira link
            issue.jiraId = jira_id
            # add the issue to the update_issues global list
            issuess_to_update.append(issue)
    # output the final result
    logger.info("%i new issue(s) opened in Jira.", new_issue_counter)
    return issuess_to_update


def fetch_jira_issues(
    jira_client: JIRA,
    jira_project: str,
    fetch_attachments: bool = True,
) -> list[jiraIssue]:
    """
    Fetch all issues from Jira for the provided project
    :param JIRA jira_client: Jira client to use for the request
    :param str jira_project: Name of the project in Jira
    :param bool fetch_attachments: Whether to fetch attachments from Jira, defaults to True
    :return: List of Jira issues
    :rtype: list[jiraIssue]
    """
    start_pointer = 0
    page_size = 100
    jira_issues = []
    fields = (
        ",".join(JIRA_FIELDS) + ",attachment"
        if fetch_attachments
        else ",".join(JIRA_FIELDS)
    )

    # get all issues for the Jira project
    while True:
        start = start_pointer * page_size
        jira_issues_response = jira_client.search_issues(
            f"project={jira_project}",
            fields=fields,
            startAt=start,
            maxResults=page_size,
        )
        if len(jira_issues) == jira_issues_response.total:
            break
        start_pointer += 1
        # append new records to jira_issues
        jira_issues.extend(jira_issues_response)
        logger.info(
            "%i/%i Jira issue(s) retrieved.",
            jira_issues_response.total,
            len(jira_issues),
        )
    if jira_issues:
        check_file_path("artifacts")
        save_data_to(
            file=Path(f"./artifacts/{jira_project}_existingJiraIssues.json"),
            data=[issue.raw for issue in jira_issues],
            output_log=False,
        )
        logger.info(
            "Saved %i Jira issue(s), see /artifacts/%s_existingJiraIssues.json",
            len(jira_issues),
            jira_project,
        )
    logger.info("%i issue(s) retrieved from Jira.", len(jira_issues))
    return jira_issues


def map_jira_to_regscale_issue(
    jira_issue: jiraIssue, config: dict, parent_id: int, parent_module: str
) -> Issue:
    """
    Map Jira issues to RegScale issues
    :param jiraIssue jira_issue: Jira issue to map to issue in RegScale
    :param dict config: Application config
    :param int parent_id: Parent record ID in RegScale
    :param str parent_module: Parent record module in RegScale
    :return: Issue object of the newly created issue in RegScale
    :rtype: Issue
    """
    due_date = map_jira_due_date(jira_issue, config)
    issue = Issue(
        title=jira_issue.fields.summary,
        severityLevel=Issue.assign_severity(jira_issue.fields.priority.name),
        issueOwnerId=config["userId"],
        dueDate=due_date,
        description=(
            f"Description {jira_issue.fields.description}"
            f"\nStatus: {jira_issue.fields.status.name}"
            f"\nDue Date: {due_date}"
        ),
        status="Closed"
        if jira_issue.fields.status.name.lower() == "done"
        else config["issues"]["jira"]["status"],
        jiraId=jira_issue.key,
        parentId=parent_id,
        parentModule=parent_module,
        dateCreated=get_current_datetime(),
        dateCompleted=get_current_datetime()
        if jira_issue.fields.status.name.lower() == "done"
        else None,
    )
    return issue


def map_jira_due_date(jira_issue: Optional[jiraIssue], config: dict) -> str:
    """
    Parses the provided jira_issue for a due date and returns it as a string
    :param jiraIssue jira_issue: Jira issue to parse for a due date
    :param dict config: Application config
    :return: due date as a string
    :rtype: str
    """
    if jira_issue.fields.duedate:
        due_date = jira_issue.fields.duedate
    elif jira_issue.fields.priority:
        due_date = datetime.now() + timedelta(
            days=config["issues"]["jira"][jira_issue.fields.priority.name.lower()]
        )
        due_date = convert_datetime_to_regscale_string(due_date)
    else:
        due_date = datetime.now() + timedelta(days=config["issues"]["jira"]["medium"])
        due_date = convert_datetime_to_regscale_string(due_date)
    return due_date


def create_issue_in_jira(
    issue: Issue,
    jira_client: JIRA,
    jira_project: str,
    issue_type: str,
    add_attachments: Optional[bool] = True,
    attachments: Optional[dict] = None,
    api: Optional[Api] = None,
) -> jiraIssue:
    """
    Create a new issue in Jira
    :param Issue issue: RegScale issue object
    :param JIRA jira_client: Jira client to use for issue creation in Jira
    :param str jira_project: Project name in Jira to create the issue in
    :param str issue_type: The type of issue to create in Jira
    :param bool add_attachments: Whether to add attachments to new issue, defaults to true
    :param dict attachments: Dictionary containing attachments, defaults to None
    :param Api api: API object to download attachments, defaults to None
    :raises: JIRAError if unable to create the issue in Jira
    :raises: JIRAError if unable to upload attachment to Jira issue
    :return: Newly created issue in Jira
    :rtype: jiraIssue
    """
    try:
        new_issue = jira_client.create_issue(
            project=jira_project,
            summary=issue.title,
            description=issue.description,
            issuetype={"name": issue_type},
        )
    except JIRAError as ex:
        error_and_exit(f"Unable to create Jira issue.\nError: {ex}")
    # add the attachments to the new Jira issue
    if add_attachments and attachments:
        if not api:
            app = Application()
            api = Api(app)
        compare_files_for_dupes_and_upload(
            jira_issue=new_issue,
            regscale_issue=issue,
            jira_client=jira_client,
            api=api,
        )
    return new_issue


def compare_files_for_dupes_and_upload(
    jira_issue: jiraIssue, regscale_issue: Issue, jira_client: JIRA, api: Api
) -> None:
    """
    Compare attachments for provided Jira and RegScale issues via hash to prevent duplicates
    :param jiraIssue jira_issue: Jira issue object to compare attachments from
    :param Issue regscale_issue: RegScale issue object to compare attachments from
    :param JIRA jira_client: Jira client to use for interacting with Jira
    :param Api api: RegScale API object to use for interacting with RegScale
    :return: None
    """
    jira_uploaded_attachments = []
    regscale_uploaded_attachments = []
    # create a temporary directory to store the downloaded attachments from Jira and RegScale
    with tempfile.TemporaryDirectory() as temp_dir:
        # write attachments to the temporary directory
        jira_dir, regscale_dir = download_issue_attachments_to_directory(
            directory=temp_dir,
            jira_issue=jira_issue,
            regscale_issue=regscale_issue,
            api=api,
        )
        # get the hashes for the attachments in the regscale and jira directories
        # iterate all files in the jira directory and compute their hashes
        jira_attachment_hashes = compute_hashes_in_directory(jira_dir)
        regscale_attachment_hashes = compute_hashes_in_directory(regscale_dir)

        # check where the files need to be uploaded to before uploading
        for file_hash, file in regscale_attachment_hashes.items():
            if file_hash not in jira_attachment_hashes:
                try:
                    with open(file, "rb") as in_file:
                        jira_client.add_attachment(
                            issue=jira_issue.id,
                            attachment=BytesIO(in_file.read()),  # type: ignore
                            filename=f"RegScale_Issue_{regscale_issue.id}_{Path(file).name}",
                        )
                        jira_uploaded_attachments.append(file)
                except JIRAError as ex:
                    logger.error(
                        "Unable to upload %s to Jira issue %s.\nError: %s",
                        Path(file).name,
                        jira_issue.key,
                        ex,
                    )
                except TypeError as ex:
                    logger.error(
                        "Unable to upload %s to Jira issue %s.\nError: %s",
                        Path(file).name,
                        jira_issue.key,
                        ex,
                    )
        for file_hash, file in jira_attachment_hashes.items():
            if file_hash not in regscale_attachment_hashes:
                with open(file, "rb") as in_file:
                    if File.upload_file_to_regscale(
                        file_name=f"Jira_attachment_{Path(file).name}",
                        parent_id=regscale_issue.id,
                        parent_module="issues",
                        api=api,
                        file_data=in_file.read(),
                    ):
                        regscale_uploaded_attachments.append(file)
                        logger.debug(
                            "Uploaded %s to RegScale issue #%i.",
                            Path(file).name,
                            regscale_issue.id,
                        )
                    else:
                        logger.warning(
                            "Unable to upload %s to RegScale issue #%i.",
                            Path(file).name,
                            regscale_issue.id,
                        )
    if regscale_uploaded_attachments and jira_uploaded_attachments:
        logger.info(
            "%i file(s) uploaded to RegScale issue #%i and %i file(s) uploaded to Jira issue %s.",
            len(regscale_uploaded_attachments),
            regscale_issue.id,
            len(jira_uploaded_attachments),
            jira_issue.key,
        )
    elif jira_uploaded_attachments:
        logger.info(
            "%i file(s) uploaded to Jira issue %s.",
            len(jira_uploaded_attachments),
            jira_issue.key,
        )
    elif regscale_uploaded_attachments:
        logger.info(
            "%i file(s) uploaded to RegScale issue #%i.",
            len(regscale_uploaded_attachments),
            regscale_issue.id,
        )


def download_issue_attachments_to_directory(
    directory: str,
    jira_issue: jiraIssue,
    regscale_issue: Issue,
    api: Api,
) -> tuple[str, str]:
    """
    Function to download attachments from Jira and RegScale issues to a directory
    :param str directory: Directory to store the files in
    :param jiraIssue jira_issue: Jira issue to download the attachments for
    :param regscale_issue: RegScale issue to download the attachments for
    :param api: Api object to use for interacting with RegScale
    :return: Tuple of strings containing the Jira and RegScale directories
    :rtype: tuple[str, str]
    """
    # determine which attachments need to be uploaded to prevent duplicates by checking hashes
    jira_dir = os.path.join(directory, "jira")
    check_file_path(jira_dir, False)
    # download all attachments from Jira to the jira directory in temp_dir
    for attachment in jira_issue.fields.attachment:
        with open(os.path.join(jira_dir, attachment.filename), "wb") as file:
            file.write(attachment.get())
    # get the regscale issue attachments
    regscale_issue_attachments = File.get_files_for_parent_from_regscale(
        api=api,
        parent_id=regscale_issue.id,
        parent_module="issues",
    )
    # create a directory for the regscale attachments
    regscale_dir = os.path.join(directory, "regscale")
    check_file_path(regscale_dir, False)
    # download regscale attachments to the directory
    for attachment in regscale_issue_attachments:
        with open(
            os.path.join(regscale_dir, attachment.trustedDisplayName), "wb"
        ) as file:
            file.write(
                File.download_file_from_regscale_to_memory(
                    api=api,
                    record_id=regscale_issue.id,
                    module="issues",
                    stored_name=attachment.trustedStorageName,
                    file_hash=attachment.shaHash
                    if attachment.shaHash
                    else attachment.fileHash,
                )
            )
    return jira_dir, regscale_dir
