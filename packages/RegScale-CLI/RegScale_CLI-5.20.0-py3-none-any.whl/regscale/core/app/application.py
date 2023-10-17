#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Application Configuration """

# standard python imports
import hashlib
import os
import platform
import sys
import uuid
from collections.abc import MutableMapping
from subprocess import PIPE, STDOUT, Popen

import requests
import yaml
from requests import Response
from yaml.scanner import ScannerError

from regscale.core.app.internal.encrypt import IOA21H98
from regscale.core.app.logz import create_logger


def verify_config(template: dict, config: dict) -> dict:
    """
    Verify keys and value types in init.yaml
    :param dict template: Default template configuration
    :param dict config: Dictionary to compare against template
    :return: validated and/or updated config
    :rtype: dict
    """
    # iterate through passed template dictionary
    for item in template:
        # see if item exists in the config dictionary
        if item in config:
            # check if value types are the same, update to template value if not
            if not isinstance(config[item], type(template[item])):
                config[item] = template[item]
            # check if the value is null
            elif (
                config[item] is None
                or str(config[item]).lower() == "null"
                or config[item] == ""
            ):
                config[item] = template[item]
            # check if value is a dict, then compare the dicts
            elif isinstance(template[item], dict):
                # iterate through dict and compare it to the template
                for key in template[item].keys():
                    if key in config[item].keys():
                        updated = verify_config(
                            template=template[item][key], config=config[item][key]
                        )
                        # update the config item
                        config[item][key] = updated
                    else:
                        # item isn't in the config sub dictionary, so add it
                        config[item][key] = template[item][key]
        else:
            # update the config with the template item
            config[item] = template[item]
    # return the updated/validated config file
    return config


class Application(MutableMapping):
    """
    RegScale CLI configuration class
    """

    def __init__(self):
        """
        Initialize application
        """
        # FIXME - move this to a template or config file
        template = {
            "stigBatchSize": 100,
            "adAccessToken": "<createdProgrammatically>",
            "adAuthUrl": "https://login.microsoftonline.com/",
            "adClientId": "<myClientIdGoesHere>",
            "adClientSecret": "<mySecretGoesHere>",
            "adGraphUrl": "https://graph.microsoft.com/.default",
            "adTenantId": "<myTenantIdGoesHere>",
            "assessmentDays": 10,
            "azure365AccessToken": "<createdProgrammatically>",
            "azure365ClientId": "<myClientIdGoesHere>",
            "azure365Secret": "<mySecretGoesHere>",
            "azure365TenantId": "<myTenantIdGoesHere>",
            "azureCloudAccessToken": "<createdProgrammatically>",
            "azureCloudClientId": "<myClientIdGoesHere>",
            "azureCloudSecret": "<mySecretGoesHere>",
            "azureCloudTenantId": "<myTenantIdGoesHere>",
            "azureCloudSubscriptionId": "<mySubscriptionIdGoesHere>",
            "cisaKev": "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
            "crowdstrikeClientId": "<myClientIdGoesHere>",
            "crowdstrikeClientSecret": "<mySecretGoesHere>",
            "dependabotId": "<myGithubUserIdGoesHere>",
            "dependabotOwner": "<myGithubRepoOwnerGoesHere>",
            "dependabotRepo": "<myGithubRepoNameGoesHere>",
            "dependabotToken": "<myGithubPersonalAccessTokenGoesHere>",
            "domain": "https://regscale.yourcompany.com/",
            "evidenceFolder": "./evidence",
            "passScore": 80,
            "failScore": 30,
            "githubDomain": "api.github.com",
            "issues": {
                "aws": {
                    "high": 30,
                    "low": 365,
                    "moderate": 90,
                    "status": "Open",
                },
                "defender365": {
                    "high": 30,
                    "low": 365,
                    "moderate": 90,
                    "status": "Open",
                },
                "defenderCloud": {
                    "high": 30,
                    "low": 365,
                    "moderate": 90,
                    "status": "Open",
                },
                "jira": {
                    "highest": 7,
                    "high": 30,
                    "medium": 90,
                    "low": 180,
                    "lowest": 365,
                    "status": "Open",
                },
                "qualys": {
                    "high": 30,
                    "moderate": 90,
                    "low": 365,
                    "status": "Open",
                },
                "salesforce": {
                    "critical": 7,
                    "high": 30,
                    "medium": 90,
                    "low": 365,
                    "status": "Open",
                },
                "tenable": {
                    "critical": 3,
                    "high": 5,
                    "moderate": 30,
                    "status": "Draft",
                },
                "wiz": {
                    "critical": 30,
                    "high": 90,
                    "low": 365,
                    "medium": 90,
                    "status": "Open",
                },
            },
            "jiraApiToken": "<jiraAPIToken>",
            "jiraUrl": "<myJiraUrl>",
            "jiraUserName": "<jiraUserName>",
            "maxThreads": 1000,
            "oktaApiToken": "Can be a SSWS token from Okta or created programmatically",
            "oktaClientId": "<oktaClientIdGoesHere>",
            "oktaUrl": "<oktaUrlGoesHere>",
            "oscalLocation": "/opt/OSCAL",
            "pwshPath": "/opt/microsoft/powershell/7/pwsh",
            "qualysUrl": "",
            "qualysUserName": "<qualysUserName>",
            "qualysPassword": "<qualysPassword>",
            "salesforceUserName": "<salesforceUserName>",
            "salesforcePassword": "<salesforcePassword>",
            "salesforceToken": "<salesforceSecurityToken>",
            "snowPassword": "<snowPassword>",
            "snowUrl": "<mySnowUrl>",
            "snowUserName": "<snowUserName>",
            "sonarToken": "<mySonarToken>",
            "tenableAccessKey": "<tenableAccessKeyGoesHere>",
            "tenableSecretKey": "<tenableSecretKeyGoesHere>",
            "tenableUrl": "https://sc.tenalab.online",
            "token": "<createdProgrammatically>",
            "userId": "enter user id here",
            "otx": "enter AlienVault API key here",
            "wizAccessToken": "<createdProgrammatically>",
            "wizAuthUrl": "https://auth.wiz.io/oauth/token",
            "wizExcludes": "My things to exclude here",
            "wizScope": "<filled out programmatically after authenticating to Wiz>",
            "wizUrl": "<my Wiz URL goes here>",
            "wizReportAge": 15,
        }

        logger = create_logger()
        self.template = template
        self.templated = False
        self.logger = logger
        config = self._gen_config()
        self.config = config
        self.os = platform.system()
        self.input_host = ""

    def __getitem__(self, key: any) -> any:
        """
        Get an item
        :param any key: key to retrieve
        :return: value of provided key
        :rtype: any
        """
        return self.config.__getitem__(self, key)

    def __setitem__(self, key: any, value: any) -> None:
        """
        Set an item
        :param any key: Key to set the provided value
        :param any value: Value to set the provided key
        :return: None
        """
        self.config.__setitem__(self, key, value)

    def __delitem__(self, key: any) -> None:
        """
        Delete an item
        :param any key: Key desired to delete
        :return: None
        """
        self.config.__delitem__(self, key)

    def __iter__(self):
        """
        Return iterator
        :return: Iterator
        """
        return self.config.__iter__(self)

    def __len__(self) -> int:
        """
        Get the length of the config
        :return: # of items in config
        :rtype: int
        """
        return len(self.config)

    def __contains__(self, x: str) -> bool:
        """
        Check config if it contains string
        :param x:
        :return: Whether the provided string exists in the config
        :rtype: bool
        """
        return self.config.__contains__(self, x)

    def _gen_config(self) -> dict:
        """
        Generate the Application config from file or environment
        :return: configuration
        :raises: TypeError if unable to generate config file
        :rtype: dict
        """
        config = None
        try:
            env = self._get_env()
            file_config = self._get_conf() or {}
            self.logger.debug("file_config: %s", file_config)
            # Merge
            if self.templated is False:
                config = {**file_config, **env}
            else:
                config = {**env, **file_config}
        except ScannerError:
            self.save_config(self.template)
        except TypeError:
            self.logger.error(
                "ERROR: init.yaml has been encrypted! Please decrypt it before proceeding.\n"
            )
            IOA21H98("init.yaml")
            sys.exit()
        if config is not None:
            # verify keys aren't null and the values are the expected data type
            config = verify_config(template=self.template, config=config)
            self.save_config(config)

        # Return config
        return config

    def _get_env(self) -> dict:
        """
        return dict of RegScale keys from system
        :raises: KeyError if unable to verify config keys
        :return: Application config
        :rtype: dict
        """
        all_keys = self.template.keys()
        sys_keys = [key for key in os.environ if key in all_keys]
        #  Update Template
        dat = None
        try:
            dat = self.template.copy()
            for k in sys_keys:
                dat[k] = os.environ[k]
        except KeyError as ex:
            self.logger.error("Key Error!!: %s", ex)
        self.logger.debug("dat: %s", dat)
        if dat == self.template:
            # Is the generated data the same as the template?
            self.templated = True
        return dat

    def _get_conf(self) -> dict:
        """
        Get configuration from init.yaml if exists
        :raises: FileNotFoundError when unable to load init.yaml
        :return: Application config
        :rtype: dict
        """
        config = None
        fname = "init.yaml"
        # load the config from YAML
        try:
            with open(fname, encoding="utf-8") as stream:
                config = yaml.safe_load(stream)
        except FileNotFoundError as ex:
            self.logger.debug(
                "%s!\n This RegScale CLI application will create the file in the current working directory.",
                ex,
            )
        self.logger.debug("_get_conf: %s, %s", config, type(config))
        return config

    @classmethod
    def save_config(cls, conf: dict) -> None:
        """
        Save Configuration to init.yaml
        :param dict conf: Application configuration
        :raises: OSError if unable to save init.yaml file
        :return: None
        """
        try:
            with open("init.yaml", "w", encoding="utf-8") as file:
                yaml.dump(conf, file)
        except OSError:
            logger = create_logger()
            logger.error("Could not dump config to init.yaml.")

    @staticmethod
    def get_regscale_license(appl, api) -> Response:
        """
        Get RegScale license of provided application via provided API object
        :param appl: Application object
        :param api: API object
        :raises: requests.RequestException if unable to get data from API call
        :return: API response
        :rtype: Response
        """
        config = appl.config
        data = {}
        domain = config["domain"]
        if domain.endswith("/"):
            domain = domain[:-1]
        try:
            data = api.get(f"{domain}/api/config/getLicense")
        except requests.RequestException:
            pass
        return data

    @staticmethod
    def load_config() -> dict:
        """
        Load Configuration file: init.yaml
        :return: Dict of config
        :rtype: dict
        """
        with open("init.yaml", "r", encoding="utf-8") as stream:
            return yaml.safe_load(stream)

    @staticmethod
    def get_java() -> str:
        """
        Get Java Version from system
        :return: Java Version
        :rtype: str
        """
        command = "java --version"
        java8_command = "java -version"
        with Popen(command, shell=True, stdout=PIPE, stderr=STDOUT) as p_cmd, Popen(
            java8_command, shell=True, stdout=PIPE, stderr=STDOUT
        ) as alt_cmd:
            out = iter(p_cmd.stdout.readline, b"")
            result = list(out)[0].decode("utf-8").rstrip("\n")
            if result == "Unrecognized option: --version":
                out = iter(alt_cmd.stdout.readline, b"")
                result = list(out)[0].decode("utf-8").rstrip("\n")
            return result

    @staticmethod
    def get_pwsh() -> str:
        """
        Get PowerShell version from the system
        :return: PowerShell version as a string
        :rtype: str
        """
        command = "pwsh --version"
        with Popen(command, shell=True, stdout=PIPE, stderr=STDOUT) as p_cmd:
            out = iter(p_cmd.stdout.readline, b"")
            result = list(out)[0].decode("utf-8").rstrip("\n")
            return result

    @staticmethod
    def gen_uuid(seed: str) -> uuid.UUID:
        """
        Generate UUID
        :param str seed: String to produce a reproducible UUID
        :return: Unique ID
        :rtype: uuid.UUID
        """
        m = hashlib.md5()
        m.update(seed.encode("utf-8"))
        new_uuid = uuid.UUID(m.hexdigest())
        return new_uuid
