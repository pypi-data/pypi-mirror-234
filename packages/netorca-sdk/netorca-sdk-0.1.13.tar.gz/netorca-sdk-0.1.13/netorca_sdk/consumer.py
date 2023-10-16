import json
import os
from typing import Tuple

import git
import yaml
from beautifultable import BeautifulTable

from netorca_sdk.auth import AbstractNetorcaAuth, NetorcaAuth
from netorca_sdk.config import SUBMIT_CONSUMER_SUBMISSION_ENDPOINT, VALIDATE_CONSUMER_SUBMISSION_ENDPOINT
from netorca_sdk.exceptions import NetorcaException


class ConsumerSubmission:
    def __init__(self, netorca_api_key: str):
        self.netorca_api_key = netorca_api_key

        self.config = None
        self.consumer_submission = None
        self.auth = None

    def load_from_repository(
        self, repository_path: str, netorca_directory: str = ".netorca", repository_config: dict = None
    ) -> None:
        """
        Check if valid and load request and config from consumer's repository.

        Note: Only one allowed extensions in netorca_directory directory is `*.yaml/*.yml`

        Args:
            repository_path: str    path to consumer repository

        Returns: None
        :param repository_path:     path to consumer repository
        :param netorca_directory:   netorca directory name, defaults to ".netorca"
        :param repository_config:      optional: you can specify config from dictionary instead of config.y(a)ml
        """

        repository_exists = os.path.isdir(repository_path)
        if not repository_exists:
            raise NetorcaException(f"`{repository_path}` directory does not exist.")

        netorca_exists = os.path.isdir(f"{repository_path}/{netorca_directory}")
        if not netorca_exists:
            raise NetorcaException(f"`{netorca_directory}` directory does not exist.")

        dotnetorca_path = f"{repository_path}/{netorca_directory}"
        if repository_config:
            netorca_global = repository_config.get("netorca_global", {})
            if not (netorca_global and netorca_global.get("base_url")):
                raise NetorcaException("No `netorca_global.base_url` provided.")

            # Check for empty base_url
            base_url = netorca_global.get("base_url", "") or ""
            base_url = base_url.strip()
            if not base_url:
                raise NetorcaException("`netorca_global.base_url` is empty.")

            self.config = repository_config
            self.auth = self.get_auth()
        else:
            # check and load config from file if it exists
            config_path_yaml = f"{repository_path}/{netorca_directory}/config.yaml"
            config_path_yml = f"{repository_path}/{netorca_directory}/config.yml"

            if os.path.exists(config_path_yml):
                config_path = config_path_yml
            elif os.path.exists(config_path_yaml):
                config_path = config_path_yaml
            else:
                raise NetorcaException("No config file in the repository.")

            with open(config_path, "r") as stream:
                try:
                    config = yaml.safe_load(stream)
                    netorca_global = config.get("netorca_global", {})
                    if not (netorca_global and netorca_global.get("base_url")):
                        raise NetorcaException("No `netorca_global.base_url` provided.")

                    # Check for empty base_url
                    base_url = netorca_global.get("base_url", "") or ""
                    base_url = base_url.strip()

                    if not base_url:
                        raise NetorcaException("`netorca_global.base_url` is empty.")
                    config["netorca_global"]["commit_id"] = self.get_commit_id(repository_path)
                    self.config = config
                    self.auth = self.get_auth()
                except yaml.YAMLError as exc:
                    raise NetorcaException(f"Error while parsing file: `config.yaml`. Exception: {exc.problem}")

        _tmp_consumer_submission = {}
        # check and load consumer request
        for filename in os.listdir(dotnetorca_path):
            if filename == "config.yaml" or filename == "config.yml":
                continue

            f = os.path.join(dotnetorca_path, filename)
            # checking if it is a file and is `*.yaml/*.yml`
            if not (os.path.isfile(f) and (f.endswith(".yaml") or f.endswith(".yml"))):
                continue

            with open(f, "r") as stream:
                try:
                    app = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    raise NetorcaException(f"Error while parsing file: `{filename}`. Exception: {exc.problem}")

            if not isinstance(app, dict) or not app:
                raise NetorcaException(
                    f"Invalid format in file: `{filename}`. The file should contain a dictionary with at least one key-value pair."
                )

            for key in app.keys():
                if key in _tmp_consumer_submission:
                    raise NetorcaException(
                        f"Application with name `{key}` already exists in different yaml declaration."
                    )

                _tmp_consumer_submission.update(app)
        self.consumer_submission = _tmp_consumer_submission

    @staticmethod
    def get_commit_id(repo_path) -> str:
        try:
            repo = git.Repo(repo_path, search_parent_directories=True)
            latest_commit = repo.head.commit
            latest_commit_id = latest_commit.hexsha
            return latest_commit_id
        except git.exc.InvalidGitRepositoryError:
            return ""

    def get_auth(self) -> AbstractNetorcaAuth:
        if not self.config:
            raise NetorcaException("Cannot authenticate before loading repository config.")

        netorca_fqdn = self.config.get("netorca_global", {}).get("base_url")
        self.auth = NetorcaAuth(fqdn=netorca_fqdn, api_key=self.netorca_api_key)
        return self.auth

    def get_team(self) -> dict:
        teams = self.auth.get_teams_info()
        if teams:
            return teams[0]
        return {}

    def prepare_request(self) -> dict:
        team = self.get_team()
        metadata = self.config.get("netorca_global", {}).get("metadata", {})
        if not (team and self.config and self.consumer_submission and self.auth):
            raise NetorcaException("Team, config and consumer request should be fetched at this stage.")

        full_request = {team["name"]: self.consumer_submission}

        if metadata is not None:
            full_request[team["name"]]["metadata"] = metadata

        return full_request

    def validate(self, pretty_print=False, partial=False) -> Tuple[bool, dict]:
        """
        Validate consume request.
        NOTE: Data must be first imported with `load_from_repository` method
        Parameters:
            pretty_print:   (optional) pretty print errors, default: False
            partial:        (optional) partial validation, default: False
        Returns:
            Tuple[bool, str]    ->  is_valid, validation_errors
        """
        if not self.consumer_submission:
            print("No application detected. Validation skipped.")
            return False, {}
        if not (self.config and self.auth):
            raise NetorcaException("Use `load_from_repository(repository_path)` method to load configuration.")
        VALIDATE_REQUEST_PATH = f"{self.auth.fqdn}{VALIDATE_CONSUMER_SUBMISSION_ENDPOINT}"
        full_request = self.prepare_request()

        if partial:
            response = self.auth.patch(
                url=VALIDATE_REQUEST_PATH, data=json.dumps(full_request), authentication_required=True
            )
        else:
            response = self.auth.post(
                url=VALIDATE_REQUEST_PATH, data=json.dumps(full_request), authentication_required=True
            )

        response = response.json()
        if response.get("is_valid"):
            return True, {}
        errors = response.get("errors")

        if pretty_print:
            ConsumerSubmission.pretty_print_errors(errors)
        return False, errors

    def submit(self, partial=False) -> Tuple[bool, str]:
        """
        Validate and submit consumer request.
        NOTE: Data must be first imported with `load_from_repository` method

        Parameters:
            partial:        (optional) partial submission, default: False
        Returns:
            bool, str    ->  submission successful, submission messages
        """
        if not self.consumer_submission:
            print("No application detected. Submission skipped.")
            return False, "No application detected. Submission skipped."
        is_valid = self.validate(pretty_print=True, partial=partial)
        if not is_valid[0]:
            return False, "Consumer request is invalid and cannot be submitted."

        SUBMIT_REQUEST_PATH = f"{self.auth.fqdn}{SUBMIT_CONSUMER_SUBMISSION_ENDPOINT}?commit_id={self.config.get('netorca_global', {}).get('commit_id')}"
        full_request = self.prepare_request()
        if partial:
            response = self.auth.patch(
                url=SUBMIT_REQUEST_PATH, data=json.dumps(full_request), authentication_required=True
            )
        else:
            response = self.auth.post(
                url=SUBMIT_REQUEST_PATH, data=json.dumps(full_request), authentication_required=True
            )

        if response.status_code == 201:
            return True, "Submitted successfully."
        if response.status_code == 200:
            return True, "Submitted successfully, no changes detected"
        return False, response.text

    @staticmethod
    def pretty_print_errors(errors: dict) -> None:
        """
        Pretty print errors
        #TODO: this should be refactored to cleaner code (probably recursive)
        """

        table = BeautifulTable(maxwidth=100)
        table.set_style(BeautifulTable.STYLE_SEPARATED)
        table.columns.header = ["Team", "Field", "Reason"]
        for item1, value1 in errors.items():
            if isinstance(value1, str) or isinstance(value1, list):
                table.rows.append([item1, "", value1])
            elif isinstance(value1, dict):
                for item2, value2 in value1.items():
                    if isinstance(value2, str) or isinstance(value2, list):
                        table.rows.append([item1, item2, value2])

                        if table.rows:
                            print("-" * 100)
                            print(f"Team: {item1} validation errors")
                            print("-" * 100)
                            print(table)
                            print()
                        break

        for item1, value1 in errors.items():
            if isinstance(value1, dict):
                for item2, value2 in value1.items():
                    table = BeautifulTable(maxwidth=100)
                    table.set_style(BeautifulTable.STYLE_SEPARATED)
                    table.columns.header = ["Application", "Service", "ServiceItem", "Field", "Reason"]

                    if isinstance(value2, dict):
                        for item3, value3 in value2.items():
                            if isinstance(value3, str):
                                table.rows.append([item2, "", "", item3, value3])
                            elif isinstance(value3, list):
                                for err in value3:
                                    table.rows.append([item2, "", "", item3, err])
                            elif isinstance(value3, dict):
                                for item4, value4 in value3.items():
                                    if isinstance(value4, str) or isinstance(value4, list):
                                        table.rows.append([item2, item3, "", item4, value4])
                                    elif isinstance(value4, dict):
                                        for item5, value5 in value4.items():
                                            if isinstance(value5, str) or isinstance(value5, list):
                                                table.rows.append([item2, item3, item4, item5, value5])

                        if table.rows:
                            print("-" * 100)
                            print(f"Application: `{item2}` validation errors")
                            print("-" * 100)
                            print(table)
                            print()
