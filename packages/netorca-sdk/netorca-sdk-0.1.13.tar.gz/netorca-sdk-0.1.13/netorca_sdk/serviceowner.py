import json
import os
from collections import defaultdict
from string import Template
from typing import Tuple

import requests
from beautifultable import BeautifulTable

from netorca_sdk.auth import AbstractNetorcaAuth, NetorcaAuth
from netorca_sdk.config import (
    SUBMIT_SERVICEOWNER_SUBMISSION_DOCS_ENDPOINT,
    SUBMIT_SERVICEOWNER_SUBMISSION_ENDPOINT,
    VALIDATE_SERVICEOWNER_SUBMISSION_ENDPOINT,
)
from netorca_sdk.exceptions import NetorcaException


class ServiceOwnerSubmission:
    def __init__(self, netorca_api_key: str):
        self.netorca_api_key = netorca_api_key

        self.config = None
        self.serviceowner_submission = None
        self.auth = None

    def load_from_repository(
        self, repository_path: str, netorca_directory: str = ".netorca", repository_config: dict = None
    ) -> None:
        """
        Check if valid and load submission and config from service owner's repository.
        Repository must contain `.netorca` directory and `config.json` file.
        Note: Two allowed extensions in `.netorca` directory are: `*.yaml` and `*.md`.

        Args:
            repository_path: str    path to service owner repository

        Returns: None
        :param repository_path:     path to service owner repository
        :param netorca_directory:   netorca directory name, defaults to ".netorca"
        :param repository_config:      optional: you can specify config from dictionary instead of config.json
        """

        repository_exists = os.path.isdir(repository_path)
        if not repository_exists:
            raise NetorcaException(f"`{repository_path}` directory does not exist.")

        netorca_path = os.path.join(repository_path, netorca_directory)
        netorca_exists = os.path.isdir(netorca_path)
        if not netorca_exists:
            raise NetorcaException(f"`{netorca_directory}` directory does not exist.")

        if repository_config:
            netorca_global = repository_config.get("netorca_global", {})
            if not (netorca_global and netorca_global.get("base_url")):
                raise NetorcaException("No `netorca_global.base_url` provided.")
            self.config = repository_config
            self.auth = self.get_auth()
        else:
            config_path = os.path.join(netorca_path, "config.json")
            self.config = self.read_json_file(config_path)
            netorca_global = self.config.get("netorca_global", {})
            if not (netorca_global and netorca_global.get("base_url")):
                raise NetorcaException("No `netorca_global.base_url` provided.")
            self.auth = self.get_auth()

        _tmp_serviceowner_submission = defaultdict()
        for filename in os.listdir(netorca_path):
            if filename == "config.json":
                continue

            file_path = os.path.join(netorca_path, filename)
            if not os.path.isfile(file_path) and not (file_path.endswith(".json") or file_path.endswith(".md")):
                raise NetorcaException(
                    f"ServiceOwner submission file: `{file_path}` does not exist or must be `.json` or `.md` extension"
                )

            if filename.endswith(".json"):
                json_file = self.read_json_file(file_path)
                filename_without_ext = os.path.splitext(filename)[0]
                _tmp_serviceowner_submission.setdefault(filename_without_ext, {})
                _tmp_serviceowner_submission[filename_without_ext]["service"] = json_file

        for filename in os.listdir(netorca_path):
            if filename == "config.json" or not filename.endswith(".md"):
                continue

            file_path = os.path.join(netorca_path, filename)
            filename_without_ext = os.path.splitext(filename)[0]

            if not _tmp_serviceowner_submission.get(filename_without_ext):
                raise NetorcaException(
                    f"'\nYou are trying to add README file: `{filename}` for non existing service.\n"
                    f"Readme file (.md) must have the same name as service definition file (.json)."
                )

            _tmp_serviceowner_submission[filename_without_ext]["readme"] = file_path

        self.serviceowner_submission = _tmp_serviceowner_submission

    def read_json_file(self, file_path: str):
        try:
            with open(file_path, "r") as stream:
                return json.load(stream)
        except FileNotFoundError as exc:
            raise NetorcaException(f"File not found: `{file_path}`. Exception: {exc}")
        except PermissionError as exc:
            raise NetorcaException(f"Permission error while reading file: `{file_path}`. Exception: {exc}")
        except json.JSONDecodeError as exc:
            raise NetorcaException(f"Error while parsing file: `{file_path}`. Exception: {exc.msg}")

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

    def validate(self, pretty_print=False) -> Tuple[bool, str]:
        """
        Validate service owner submission.
        NOTE: Data must be first imported with `load_from_repository` method

        Returns:
            bool    ->  validation successful
        """
        if self.auth is None:
            raise NetorcaException("Use `load_from_repository(repository_path)` method to load configuration.")
        VALIDATE_SERVICEOWNER_PATH = f"{self.auth.fqdn}{VALIDATE_SERVICEOWNER_SUBMISSION_ENDPOINT}"
        invalid_services = []

        if not (self.config and self.serviceowner_submission and self.auth):
            raise NetorcaException("Use `load_from_repository(repository_path)` method to load configuration.")

        for service, service_submission in self.serviceowner_submission.items():
            response = self.auth.post(
                url=VALIDATE_SERVICEOWNER_PATH,
                data=json.dumps(service_submission["service"]),
                authentication_required=True,
            )
            response = response.json()
            if response.get("is_valid"):
                print(f"VALIDATION SUCCESSFUL for service: `{service}`.")
            else:
                invalid_services.append(service)
                errors = response.get("errors")
                if pretty_print and errors:
                    ServiceOwnerSubmission.pretty_print_errors(service, errors)

        if invalid_services:
            print("INVALID SERVICES: " + ", ".join(invalid_services))
            return False, "Invalid services: " + ", ".join(invalid_services)
        return True, "Services validated successfully."

    def submit(self) -> Tuple[bool, str]:
        """
        Validate and submit consumer submission.
        NOTE: Data must be first imported with `load_from_repository` method

        Returns:
            bool, str    ->  is submission successful, submission messages
        """
        SUBMIT_SERVICEOWNER_REQUEST_PATH = f"{self.auth.fqdn}{SUBMIT_SERVICEOWNER_SUBMISSION_ENDPOINT}"
        submitted_services = []
        is_valid = self.validate(pretty_print=True)

        if not is_valid[0]:
            return False, "Some of your submissions are invalid and were not submitted."

        print()
        for service, service_submission in self.serviceowner_submission.items():
            response = self.auth.post(
                url=SUBMIT_SERVICEOWNER_REQUEST_PATH,
                data=json.dumps(service_submission["service"]),
                authentication_required=True,
            )

            if response.status_code == 201:
                print(f"SUBMITTED service to NetOrca. Service: `{service}` is now available for consumers.")
                submitted_services.append(service)
                if service_submission.get("readme"):
                    service_id = response.json()["id"]
                    docs_path = Template(SUBMIT_SERVICEOWNER_SUBMISSION_DOCS_ENDPOINT).substitute(id=service_id)
                    SUBMIT_SERVICEOWNER_DOCS_PATH = f"{self.auth.fqdn}{docs_path}"
                    files = {"md_file": ("VM.md", open(service_submission.get("readme"), "rb"))}
                    auth = self.auth.headers["Authorization"]
                    response = requests.post(
                        SUBMIT_SERVICEOWNER_DOCS_PATH, files=files, headers={"Authorization": auth}, verify=False
                    )
                    if response.status_code == 200:
                        print(f"SUBMITTED README file for service: `{service}`.")
                    else:
                        print(f"FAILED to submit README file for service: `{service}`. Reason: `{response.json()}.`")
                else:
                    print(f"NOTE: Service `{service}` does not have a README file. Skipped.")
            else:
                print(f"FAILED to submit service: `{service}`. Reason: {response.json()}")
                print("\nMoving to next service...")
            print()

        if submitted_services:
            return True, "Submitted services: " + ", ".join(submitted_services)
        return False, "No services were submitted."

    @staticmethod
    def pretty_print_errors(service_name: str, errors: dict) -> None:
        def append_to_table(service_name: str, item: str, value: str, table: BeautifulTable) -> None:
            if isinstance(value, str) or isinstance(value, list):
                table.rows.append([service_name, item, value])
            elif isinstance(value, dict):
                for key, val in value.items():
                    append_to_table(service_name, key, val, table)

        table = BeautifulTable(maxwidth=100)
        table.set_style(BeautifulTable.STYLE_SEPARATED)
        table.columns.header = ["Schema", "Property", "Reason"]

        for item, value in errors.items():
            append_to_table(service_name, item, value, table)

        if table.rows:
            print("-" * 100)
            print(f"Schema: `{service_name}` validation errors")
            print("-" * 100)
            print(table)
            print()
