#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RegScale Email Reminders"""

# standard python imports
import re
import sys
from datetime import datetime, timedelta
from typing import Tuple

import click
import pandas as pd
from requests import JSONDecodeError
from rich.console import Console

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    check_license,
    create_progress_object,
    error_and_exit,
    flatten_dict,
    get_css,
    reformat_str_date,
    uncamel_case,
)
from regscale.core.app.utils.regscale_utils import (
    get_user,
    send_email,
    verify_provided_module,
)
from regscale.core.app.utils.threadhandler import create_threads, thread_assignment
from regscale.models.app_models.click import regscale_id, regscale_module
from regscale.models.app_models.pipeline import Pipeline

job_progress = create_progress_object()
logger = create_logger()

# empty global lists to be used for threads
tenant_pipeline = []
final_pipeline = []
emails = []
workflows = {}


@click.group(name="admin_actions")
def actions():
    """Performs administrative actions on the RegScale platform."""


@actions.command(name="update_compliance_history")
@regscale_id()
@regscale_module()
def update_compliance_history(regscale_id: int, regscale_module: str):
    """
    Update the daily compliance score for a given RegScale System Security Plan.
    """
    verify_provided_module(regscale_module)
    update_compliance(regscale_id, regscale_module)


@actions.command(name="send_reminders")
@click.option(
    "--days",
    type=click.INT,
    help="RegScale will look for Assessments, Tasks, Issues, Security Plans, "
    + "Data Calls, and Workflows using today + # of days entered. Default is 30 days.",
    default=30,
    show_default=True,
    required=True,
)
def send_reminders(days: int):
    """
    Get Assessments, Issues, Tasks, Data Calls, Security Plans, and Workflows
    for the users that have email notifications enabled, email comes
    from support@regscale.com.
    """
    get_and_send_reminders(days)


def get_and_send_reminders(days: int = 30) -> None:
    """
    Function to get and send reminders for users in RegScale that have email notifications
    enabled and have upcoming or outstanding Tasks, Assessments, Data Calls, Issues, Security Plans,
    and Workflows
    :param int days: # of days to look for upcoming and/or outstanding items, default is 30 days
    :return: None
    """
    app = check_license()
    api = Api(app)
    config = {}
    try:
        # load the config from YAML
        config = app.load_config()
    except FileNotFoundError:
        error_and_exit("No init.yaml file or permission error when opening file.")
    # make sure config is set before processing
    if "domain" not in config:
        error_and_exit("No domain set in the initialization file.")
    if config["domain"] == "":
        error_and_exit("The domain is blank in the initialization file.")
    if ("token" not in config) or (config["token"] == ""):
        error_and_exit("The token has not been set in the initialization file.")

    # set base url, used for other api paths
    base_url = config["domain"] + "/api/"

    # get the user's tenant id, used to get all active
    # users for that instance of the application
    res = api.get(url=f'{base_url}accounts/find/{config["userId"]}').json()
    ten_id = res["tenantId"]

    # Use the api to get a list of all active users
    # with emailNotifications set to True for
    # the tenant id of the current user
    response = api.get(url=f"{base_url}accounts/{str(ten_id)}/True")
    activated_users_response = api.get(url=f"{base_url}accounts")
    # try to convert the response to a json file, exit if it errors
    try:
        users = response.json()
        activated_users = activated_users_response.json()
    # if error encountered, exit the application
    except JSONDecodeError as ex:
        error_and_exit(f"Unable to retrieve active users from RegScale.\n{ex}")

    # start a console progress bar and threads for the given task
    # create the threads with the given function, arguments and thread count
    with job_progress:
        logger.info("Fetching pipeline for %s user(s).", len(users))
        getting_items = job_progress.add_task(
            f"[#f8b737]Fetching pipeline for {len(users)} user(s)...", total=len(users)
        )

        create_threads(
            process=get_upcoming_or_expired_items,
            args=(api, users, base_url, days, config, getting_items),
            thread_count=len(users),
        )

        if len(tenant_pipeline) > 0:
            logger.info("Analyzing pipeline for %s user(s).", len(tenant_pipeline))
            # start a console progress bar and threads for the given task
            analyze_items = job_progress.add_task(
                f"[#ef5d23]Analyzing pipeline for {len(tenant_pipeline)} user(s)...",
                total=len(tenant_pipeline),
            )
            # convert user list into a dictionary using ID as the key for each user dictionary
            dict_users = {
                activated_users[i]["id"]: activated_users[i]
                for i in range(len(activated_users))
            }
            create_threads(
                process=analyze_pipeline,
                args=(config, analyze_items, dict_users, api),
                thread_count=len(tenant_pipeline),
            )
            logger.info("Sending an email to %s user(s).", len(final_pipeline))
            # start a console progress bar and threads for the given task
            emailing_users = job_progress.add_task(
                f"[#21a5bb]Sending an email to {len(final_pipeline)} user(s)...",
                total=len(final_pipeline),
            )
            create_threads(
                process=format_and_email,
                args=(api, config, emailing_users),
                thread_count=len(final_pipeline),
            )
        else:
            logger.info("No outstanding or upcoming items!")
            sys.exit()

    # create one data table from all pandas data tables in emails
    email_data = pd.concat(emails)

    # create console variable and print # of emails sent successfully
    logger.info("Successfully sent an email to %s user(s)...", email_data.Emailed.sum())
    console = Console()
    console.print(
        f"[green]Successfully sent an email to {email_data.Emailed.sum()} user(s)..."
    )

    # format email to notify person that called the command of the outcome
    email_payload = {
        "id": 0,
        "from": "Support@RegScale.com",
        "emailSenderId": config["userId"],
        "to": res["email"],
        "cc": "",
        "dateSent": "",
        "subject": f"RegScale Reminders Sent to {email_data.Emailed.sum()} User(s)",
        "body": get_css(".\\models\\email_style.css")
        + email_data.to_html(justify="left", index=False)
        .replace('border="1"', 'border="0"')
        .replace("&amp;", "&")
        .replace("&gt;", ">")
        .replace("&lt;", "<")
        .replace("’", "'"),
    }

    # send the email to the user
    send_email(api=api, domain=config["domain"], payload=email_payload)


def get_upcoming_or_expired_items(args: Tuple, thread: int) -> None:
    """
    Function used by threads to send emails to users with upcoming and/or outstanding
    Tasks, Assessments, Data Calls, Issues, Security Plans, and Workflows
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :return: None:
    """
    # set up my args from the args tuple
    api, all_users, base_url, days, config, task = args

    # get the thread assignment for the current thread
    threads = thread_assignment(thread=thread, total_items=len(all_users))

    # update api pool limits to max_thread count from init.yaml
    api.pool_connections = config["maxThreads"]
    api.pool_maxsize = config["maxThreads"]

    # check the Assessments, Issues, Tasks, Data Calls, Security Plans and Workflows
    # for each user in all users dictionary and store them in the list
    for i in range(len(threads)):
        user = all_users[threads[i]]

        # calculate date with the # of days provided
        before_date = datetime.now() + timedelta(days=days)
        after_date = datetime.now() - timedelta(days=days)

        # format the date to a string the server will recognize
        before_date = before_date.strftime("%Y-%m-%dT%H:%M:%S")
        after_date = after_date.strftime("%Y-%m-%dT%H:%M:%S")

        # get all the assessments, issues, tasks, data calls, security plans and workflows
        # for the user we can email, using the # of days entered by the user using graphql,
        # if no days were entered, the default is 30 days
        query = f"""
            query {{
              assessments(
                take: 50
                skip: 0
                order: {{ plannedFinish: DESC }}
                where: {{
                  leadAssessorId: {{ eq: "{user["id"]}" }}
              plannedFinish: {{ lte: "{before_date}" }}
              status: {{ nin: ["Complete", "Cancelled"] }}
            }}
          ) {{
            items {{
              uuid
              id
              title
              leadAssessorId
              assessmentType
              plannedFinish
              createdById
              dateCreated
              status
              assessmentResult
              actualFinish
            }}
            totalCount
            pageInfo {{
              hasNextPage
            }}
          }}
          dataCalls(
            take: 50
            skip: 0
            order: {{ dateDue: DESC }}
            where: {{
              createdById: {{ eq: "{user["id"]}" }}
              dateDue: {{ lte: "{before_date}" }}
              status: {{ nin: ["Completed", "Cancelled"] }}
            }}
          ) {{
            items {{
              uuid
              id
              title
              dataCallLeadId
              dateDue
              createdById
              dateCreated
              status
            }}
            totalCount
            pageInfo {{
              hasNextPage
            }}
          }}
          securityPlans(
            take: 50
            skip: 0
            order: {{ expirationDate: DESC }}
            where: {{
              systemOwnerId: {{ eq: "{user["id"]}" }}
              expirationDate: {{ lte: "{before_date}" }}
            }}
          ) {{
            items {{
              uuid
              id
              systemName
              systemOwnerId
              status
              systemType
              expirationDate
              overallCategorization
              createdById
              dateCreated
            }}
            totalCount
            pageInfo {{
              hasNextPage
            }}
          }}
          workflowInstances(
            take: 50
            skip: 0
            order: {{ startDate: DESC }}
            where: {{
              ownerId: {{ eq: "{user["id"]}" }}
              status: {{ neq: "Complete" }}
              startDate: {{ gte: "{after_date}" }}
              endDate: {{ eq: null }}
            }}
          ) {{
            items {{
              id
              name
              status
              startDate
              endDate
              comments
              currentStep
              createdById
              dateCreated
              lastUpdatedById
              ownerId
              atlasModule
              parentId
            }}
            totalCount
            pageInfo {{
              hasNextPage
            }}
          }}
          tasks(
            take: 50
            skip: 0
            order: {{ dueDate: DESC }}
            where: {{
              assignedToId: {{ eq: "{user["id"]}" }}
              dueDate: {{ lte: "{before_date}" }}
              status: {{ nin: ["Closed", "Cancelled"] }}
            }}
          ) {{
            items {{
              uuid
              id
              title
              assignedToId
              dueDate
              createdById
              status
              percentComplete
            }}
            totalCount
            pageInfo {{
              hasNextPage
            }}
          }}
          issues(
            take: 50
            skip: 0
            order: {{ dueDate: DESC }}
            where: {{
              issueOwnerId: {{ eq: "{user["id"]}" }}
              dueDate: {{ lte: "{before_date}" }}
              status: {{ nin: ["Closed", "Cancelled"] }}
            }}
          ) {{
            items {{
              uuid
              id
              title
              issueOwnerId
              severityLevel
              createdById
              dateCreated
              status
              dueDate
            }}
            totalCount
            pageInfo {{
              hasNextPage
            }}
          }}
        }}
        """
        # get the data from GraphQL
        res_data = api.graph(query=query)

        # create list that has dictionaries of the user's pipeline and categories
        pipelines = {
            "Assessments": {"Pipeline": res_data["assessments"]["items"]},
            "Issues": {"Pipeline": res_data["issues"]["items"]},
            "Tasks": {"Pipeline": res_data["tasks"]["items"]},
            "Data Calls": {"Pipeline": res_data["dataCalls"]["items"]},
            "Security Plans": {"Pipeline": res_data["securityPlans"]["items"]},
            "Workflow": {"Pipeline": res_data["workflowInstances"]["items"]},
        }
        # iterate through the user's pipeline tallying their items
        # create variable to see how many total objects are in the user's pipeline
        total_tasks = sum(len(pipeline["Pipeline"]) for pipeline in pipelines.values())
        # check the total # of items in their pipeline
        if total_tasks > 0:
            # map and add the data to a global variable
            tenant_pipeline.append(
                Pipeline(
                    email=user["email"],
                    fullName=f'{user["firstName"]} {user["lastName"]}',
                    pipelines=pipelines,
                    totalTasks=total_tasks,
                )
            )
        job_progress.update(task, advance=1)


# flake8: noqa: C901
def analyze_pipeline(args: Tuple, thread: int):
    """
    Function to set up data tables from the user's pipeline while using threading
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :return: None
    """
    config, task, users, api = args

    id_fields = ["leadassessorid", "assignedtoid", "datacallleadid"]

    # get the assigned threads
    threads = thread_assignment(
        thread=thread,
        total_items=len(tenant_pipeline),
    )
    for i in range(len(threads)):
        # get the pipeline from the global tenant_pipeline
        pipelines = tenant_pipeline[threads[i]].pipelines

        # set up local variable for user pipeline
        user_pipeline = []

        # check if the user has already been analyzed
        if not tenant_pipeline[threads[i]].analyzed:
            # change the user's status to analyzed
            tenant_pipeline[threads[i]].analyzed = True

            # start out in the beginning of the pipelines
            # and iterate through all of their items
            for pipe in pipelines:
                # creating variable to store html table for the user's email
                prelim_pipeline = []

                # iterate through the items in the pipeline category while
                # creating legible table headers
                for item in pipelines[pipe]["Pipeline"]:
                    # flatten the dict to remove nested dictionaries
                    item = flatten_dict(item)

                    # create list variable to store the renamed column names
                    headers = []
                    # iterate through all columns for the item and see if the header
                    # has to be changed to Title Case and if the data has to revalued
                    for key in item.keys():
                        # change the camelcase header to a Title Case Header
                        fixed_key = uncamel_case(key)

                        # check the keys to revalue the data accordingly
                        if key.lower() == "uuid" or (
                            pipe.lower() == "workflow" and key.lower() == "id"
                        ):
                            # create html url using data for the html table
                            href = f'{config["domain"]}/{pipe.lower().replace(" ", "")}'
                            href += f'/form/{item["id"]}'
                            # have to add an if clause for mso to display the view button correctly
                            url = (
                                '<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml"'
                                f'xmlns:w="urn:schemas-microsoft-com:office:word" href="{href}" '
                                'style="height:40px;v-text-anchor:middle;width:60px;" arcsize="5%" '
                                'strokecolor="#22C2DC" fillcolor="#1DC3EB"><w:anchorlock/><center'
                                ' style="color:#ffffff;font-family:Roboto, Arial, sans-serif;font'
                                '-size:14px;">View</center></v:roundrect><![endif]-->'
                            )
                            url += f'<a href="{href}" style="mso-hide:all;">View</a>'

                            headers.append("Action")
                            if pipe.lower() == "workflow":
                                update_dict = {"UUID": url}
                                item = {**update_dict, **item}
                                headers.append("ID")
                            else:
                                # replace the UUID with the HTML url
                                item[key] = url
                        elif (
                            "ById" in key
                            or "ownerid" in key.lower()
                            or key.lower() in id_fields
                        ) and item[key]:
                            # remove ById from the key
                            new_key = key.replace("Id", "")

                            # uncamel_case() the key
                            new_key = uncamel_case(new_key)

                            # replace the user id string with a user's name
                            user_id = item[key]
                            try:
                                # try to replace the ID with a user from all active users
                                item[
                                    key
                                ] = f'{users[user_id]["firstName"]} {users[user_id]["lastName"]}'
                            except KeyError:
                                # means the user is not activated, fetch them via API
                                user = get_user(api, user_id)
                                item[key] = f'{user["firstName"]} {user["lastName"]}'
                            # add the updated key to the table headers
                            headers.append(new_key)
                        elif key.lower() == "atlasmodule":
                            headers.append("Parent Module")
                        elif (
                            "date" in key.lower() or "finish" in key.lower()
                        ) and item[key]:
                            try:
                                # convert string to a date & reformat the date to a legible string
                                item[key] = reformat_str_date(item[key], "%b %d, %Y")
                            except ValueError:
                                headers.append(fixed_key)
                                continue
                            # append the Title Case header to the headers list
                            headers.append(fixed_key)
                        elif key == "id":
                            # change the key to all uppercase
                            headers.append(key.upper())
                        elif isinstance(item[key], str) and "<" in item[key]:
                            # replace </br> with \n
                            text = item[key].replace("</br>", "\n")

                            # strip other html codes from string values
                            item[key] = re.sub("<[^<]+?>", "", text)

                            # append the Title Case header to headers
                            headers.append(fixed_key)
                        elif key.lower() == "currentstep":
                            item[key] += 1
                            headers.append(fixed_key)
                        elif key.lower() == "workflowinstancesteps":
                            del item[key]
                        else:
                            headers.append(fixed_key)
                    # add it to the final pipeline for the user
                    prelim_pipeline.append(item)
                # check to see if there is an item for the bucket before
                # appending it to the final_pipeline for the email
                if len(prelim_pipeline) > 0:
                    # convert the item to a pandas data table
                    data = pd.DataFrame(prelim_pipeline)

                    # replace the columns with our legible data headers
                    data.columns = headers

                    # append the data item and bucket to our local user_pipeline list
                    user_pipeline.append({"bucket": pipe, "items": data})
            # add the user's pipeline data to the global pipeline for the emails
            final_pipeline.append(
                Pipeline(
                    email=tenant_pipeline[threads[i]].email,
                    fullName=tenant_pipeline[threads[i]].fullName,
                    pipelines=user_pipeline,
                    totalTasks=tenant_pipeline[threads[i]].totalTasks,
                    analyzed=True,
                )
            )
        job_progress.update(task, advance=1)


def update_compliance(regscale_parent_id: int, regscale_parent_module: str) -> None:
    """
    Update RegScale compliance history with a System Security Plan ID
    :param int regscale_parent_id: RegScale parent ID
    :param str regscale_parent_module: RegScale parent module
    :return: None
    """
    app = Application()
    api = Api(app)
    headers = {
        "accept": "*/*",
        "Authorization": app.config["token"],
    }

    response = api.post(
        headers=headers,
        url=app.config["domain"]
        + f"/api/controlImplementation/SaveComplianceHistoryByPlan?intParent={regscale_parent_id}&strModule={regscale_parent_module}",
        data="",
    )
    if not response.raise_for_status():
        if response.status_code == 201:
            if (
                "application/json" in response.headers.get("content-type")
                and "message" in response.json()
            ):
                logger.warning(response.json()["message"])
            else:
                logger.warning("Resource not created.")
        if response.status_code == 200:
            logger.info(
                "Updated Compliance Score for RegScale Parent ID: %i.\nParent module: %s.",
                regscale_parent_id,
                regscale_parent_module,
            )


def format_and_email(args: Tuple, thread: int):
    """
    Function to email all users with an HTML formatted email
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :return: None
    """
    # set up my args from the args tuple
    api, config, task = args

    threads = thread_assignment(
        thread=thread,
        total_items=len(final_pipeline),
    )

    # update api pool limits to max_thread count from init.yaml
    api.pool_connections = config["maxThreads"]
    api.pool_maxsize = config["maxThreads"]

    # get assigned threads
    for i in range(len(threads)):
        # get the user's pipeline details
        email = final_pipeline[threads[i]].email
        total_tasks = final_pipeline[threads[i]].totalTasks

        # create list to store the html tables
        tables = []

        # see if the user has been emailed already
        if not final_pipeline[threads[i]].emailed:
            # set the emailed flag to true
            final_pipeline[threads[i]].emailed = True

            # iterate through all items in final_pipeline to
            # set up data tables as a html tables using pandas
            for item in final_pipeline[threads[i]].pipelines:
                tables.extend(
                    (
                        f'<h1>{item["bucket"]}</h1>',
                        item["items"]
                        .to_html(justify="left", index=False)
                        .replace('border="1"', 'border="0"'),
                    )
                )
            # join all the items in tables and separate them all with a </br> tag
            tables = "</br>".join(tables)

            # fix any broken html tags
            tables = (
                tables.replace("&amp;", "&")
                .replace("&gt;", ">")
                .replace("&lt;", "<")
                .replace("’", "'")
            )

            # create email payload
            email_payload = {
                "id": 0,
                "from": "Support@RegScale.com",
                "emailSenderId": config["userId"],
                "to": email,
                "cc": "",
                "dateSent": "",
                "subject": f"RegScale Reminder: {total_tasks} Upcoming Items",
                "body": get_css(".\\models\\email_style.css") + tables,
            }

            # send the email and get the response
            emailed = send_email(
                api=api, domain=config["domain"], payload=email_payload
            )

            # set up dict to use for pandas data
            data = {
                "Email Address": '<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml"'
                'xmlns:w="urn:schemas-microsoft-com:office:word" href="mailto:'
                f'{email}"style="height:auto;v-text-anchor:middle;mso-width-'
                'percent:150;" arcsize="5%" strokecolor="#22C2DC" fillcolor='
                '"#1DC3EB"><w:anchorlock/><center style="color:#ffffff;font-'
                f'family:Roboto, Arial, sans-serif;font-size:14px;">{email}'
                '</center></v:roundrect><![endif]--><a href="mailto:'
                f'{email}" style="mso-hide:all;">{email}</a>',
                "User Name": final_pipeline[threads[i]].fullName,
                "Total Tasks": total_tasks,
                "Emailed": emailed,
            }
            table = pd.DataFrame([data])
            emails.append(table)
        job_progress.update(task, advance=1)
