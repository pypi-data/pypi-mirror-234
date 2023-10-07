import json
import logging
import os
import shutil
from http import HTTPStatus

import pkg_resources  # type: ignore
import requests
from packaging import version

from fovus.adapter.fovus_api_adapter import FovusApiAdapter
from fovus.adapter.fovus_cognito_adapter import FovusCognitoAdapter
from fovus.adapter.fovus_s3_adapter import JOB_DATA_FILENAME, FovusS3Adapter
from fovus.adapter.fovus_sign_in_adapter import FovusSignInAdapter
from fovus.constants.cli_action_runner_constants import GENERIC_SUCCESS, OUTPUTS
from fovus.constants.cli_constants import (
    CONFLICTING_CLI_ARGUMENT_SETS,
    CREATE_JOB_WITH_UPLOAD,
    DEBUG_MODE,
    DOWNLOAD_JOB_FILES,
    FOVUS_PROVIDED_CONFIGS,
    GET_JOB_CURRENT_STATUS,
    JOB_CONFIG_FILE_PATH,
    JOB_FILE_ROOT_DIRECTORY,
    JOB_ID,
    LOCAL_PATH,
    LOGIN,
    LOGOUT,
    OPEN_CONFIG_FOLDER,
    PATH_TO_CONFIG_FILE_IN_REPO,
    PATH_TO_CONFIG_FILE_LOCAL,
    PATH_TO_CONFIG_ROOT,
    PATH_TO_JOB_CONFIGS,
    PATH_TO_JOB_LOGS,
    PATH_TO_USER_CONFIGS,
    UNIX_OPEN,
    UPLOAD_FILES,
    USER,
    WINDOWS_EXPLORER,
)
from fovus.constants.fovus_api_constants import ApiMethod
from fovus.exception.status_code_exception import StatusException
from fovus.exception.user_exception import UserException
from fovus.root_config import ROOT_DIR
from fovus.util.cli_action_runner_util import CliActionRunnerUtil
from fovus.util.file_util import FOVUS_JOB_INFO_FOLDER, FileUtil
from fovus.util.fovus_api_util import FovusApiUtil
from fovus.util.util import Util
from fovus.validator.fovus_api_validator import FovusApiValidator


class CliActionRunner:  # pylint: disable=too-few-public-methods
    def __init__(self, args_dict):
        self.args_dict = args_dict

    def run_actions(self):
        try:
            logging.info("CLI Arguments: %s", self.args_dict)
            self._confirm_latest_version()
            self._run_actions()
        except StatusException as exception:
            print(exception)

    def _run_actions(self):
        self._confirm_nonconflicting_argument_sets(CONFLICTING_CLI_ARGUMENT_SETS)

        if self.args_dict[OPEN_CONFIG_FOLDER]:
            self._confirm_required_arguments_present([])
            self._open_config_folder()

        if self.args_dict[LOGIN]:
            self._login()

        if self.args_dict[LOGOUT]:
            self._logout()

        if self.args_dict[USER]:
            self._user()

        if self.args_dict[CREATE_JOB_WITH_UPLOAD]:
            self._confirm_required_arguments_present([JOB_CONFIG_FILE_PATH, JOB_FILE_ROOT_DIRECTORY])
            self._confirm_forbidden_arguments_not_present([JOB_ID])
            self._create_job()

        if self.args_dict[DOWNLOAD_JOB_FILES]:
            self._try_set_job_id()
            self._confirm_required_arguments_present([JOB_FILE_ROOT_DIRECTORY, JOB_ID])
            self._download_job_files()

        if self.args_dict[GET_JOB_CURRENT_STATUS]:
            self._try_set_job_id()
            self._confirm_required_arguments_present([JOB_ID])
            self._get_job_current_status()

        if self.args_dict[UPLOAD_FILES]:
            self._confirm_required_arguments_present([LOCAL_PATH])
            self._upload_file()

    def _confirm_latest_version(self):
        try:
            response = requests.get("https://pypi.org/pypi/fovus/json", timeout=5)
            data = response.json()
            latest_version = data["info"]["version"]
        except (requests.RequestException, KeyError):
            print("Unable to check for latest version.")
            return

        try:
            current_version = pkg_resources.get_distribution("fovus").version
        except pkg_resources.DistributionNotFound:
            print("Unable to check for latest version.")
            return

        if version.parse(current_version) < version.parse(latest_version):
            print(
                "===================================================\n"
                + f"  A new version of Fovus CLI ({latest_version}) is available.\n"
                + f"  Your current version is {current_version}\n"
                + "  Update using: pip install --upgrade fovus\n"
                + "==================================================="
            )

    def _confirm_nonconflicting_argument_sets(self, conflicting_argument_sets):
        print("Confirming no conflicting arguments are present...")
        for conflicting_argument_set in conflicting_argument_sets:
            self._confirm_nonconflicting_arguments(conflicting_argument_set)
        print(GENERIC_SUCCESS)

    def _confirm_nonconflicting_arguments(self, conflicting_arguments):
        conflicting_arguments_count = 0
        for argument in self.args_dict.keys():
            if self.args_dict.get(argument) and argument in conflicting_arguments:
                conflicting_arguments_count += 1
        if conflicting_arguments_count > 1:
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                self.__class__.__name__,
                "Only one of the following arguments can be used at a time: "
                + ", ".join(CliActionRunnerUtil.get_argument_string_list_from_keys(conflicting_arguments)),
            )

    def _confirm_required_arguments_present(self, argument_list):
        print("Confirming required arguments are present...")
        missing_arguments = []
        for argument in argument_list:
            if not self.args_dict.get(argument):
                missing_arguments.append(argument)
        if missing_arguments:
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                self.__class__.__name__,
                "Missing required arguments: "
                + ", ".join(CliActionRunnerUtil.get_argument_string_list_from_keys(missing_arguments))
                + ".",
            )
        print(GENERIC_SUCCESS)

    def _confirm_forbidden_arguments_not_present(self, argument_list):
        print("Confirming forbidden arguments are not present...")
        forbidden_arguments = []
        for argument in argument_list:
            if self.args_dict.get(argument):
                forbidden_arguments.append(argument)
        if forbidden_arguments:
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                self.__class__.__name__,
                "Forbidden arguments: "
                + ", ".join(CliActionRunnerUtil.get_argument_string_list_from_keys(forbidden_arguments))
                + ".",
            )
        print(GENERIC_SUCCESS)

    def _try_set_job_id(self):
        if self.args_dict.get(JOB_ID):
            return

        if self.args_dict.get(JOB_FILE_ROOT_DIRECTORY):
            print(
                "Job ID not specified. Attempting to find job ID in "
                + os.path.join(self.args_dict[JOB_FILE_ROOT_DIRECTORY], FOVUS_JOB_INFO_FOLDER, JOB_DATA_FILENAME)
                + "..."
            )
            job_data_file_path = os.path.join(
                self.args_dict[JOB_FILE_ROOT_DIRECTORY], FOVUS_JOB_INFO_FOLDER, JOB_DATA_FILENAME
            )
            if os.path.exists(job_data_file_path):
                with FileUtil.open(job_data_file_path) as file:
                    job_data = json.load(file)
                    self.args_dict[JOB_ID] = job_data.get(JOB_ID)
                    print("Job ID found: " + self.args_dict[JOB_ID])
                    return

        raise UserException(
            HTTPStatus.BAD_REQUEST,
            self.__class__.__name__,
            (
                "Missing job ID. This can be provided as an argument (via --job-id) or through the job data "
                "file (via --job-file-root-directory), which is automatically generated in the "
                "'job_root_folder/.fovus' directory when a job is created from the CLI."
            ),
        )

    def _open_config_folder(self):
        self._create_missing_directories()
        print(GENERIC_SUCCESS)
        self._create_missing_empty_config_files()
        print(GENERIC_SUCCESS)

        print("Opening config folder...")
        # Subprocess imported locally to discourage use throughout module. All subprocess calls are hardcoded and safe.
        import subprocess  # pylint: disable=import-outside-toplevel  # nosec

        if Util.is_windows():
            subprocess.run(  # nosec - This subprocess call is fully hardcoded.
                [WINDOWS_EXPLORER, os.path.expanduser(PATH_TO_CONFIG_ROOT)], shell=False, check=False
            )
        elif Util.is_unix():
            subprocess.run(  # nosec - This subprocess call is fully hardcoded.
                [UNIX_OPEN, os.path.expanduser(PATH_TO_CONFIG_ROOT)], shell=False, check=False
            )
        else:
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                self.__class__.__name__,
                "Unsupported operating system. Only Windows and Unix are supported.",
            )
        print(GENERIC_SUCCESS)

    def _create_job(self):
        self._confirm_enable_debug_mode()
        print("Creating Fovus API adapter and Fovus S3 adapter and authenticating...")
        fovus_api_adapter = FovusApiAdapter()
        fovus_s3_adapter = FovusS3Adapter(fovus_api_adapter, self.args_dict, self.args_dict[JOB_FILE_ROOT_DIRECTORY])
        print(GENERIC_SUCCESS)

        user_id = fovus_api_adapter.get_user_id()
        workspace_id = fovus_api_adapter.get_workspace_id()

        print("Creating and validating create job request...")
        create_job_request = FovusApiAdapter.get_create_job_request(self.args_dict, user_id, workspace_id)
        fovus_api_adapter.make_dynamic_changes_to_create_job_request(create_job_request)
        validator = FovusApiValidator(create_job_request, ApiMethod.CREATE_JOB)
        validator.validate()
        print(GENERIC_SUCCESS)

        fovus_s3_adapter.upload_files()

        print("Creating job...")
        fovus_api_adapter.create_job(create_job_request)
        print(GENERIC_SUCCESS)
        print(OUTPUTS)
        print(
            "\n".join(
                (
                    "Job name:",
                    create_job_request["jobName"],
                    "Job ID:",
                    FovusApiUtil.get_job_id(self.args_dict, user_id),
                )
            )
        )

    def _confirm_enable_debug_mode(self):
        if self.args_dict.get(DEBUG_MODE):
            print(
                "In debug mode, compute nodes will stay alive after each task execution until the task walltime is "
                + "reached to allow addtional time for debugging via SSH. Make sure to terminate your task or job "
                + "manually after debugging to avoid unnecessary charges for the additional time."
            )
            print("Are you sure you want to enable debug mode? (y/n):")
            if input() == "y":
                self.args_dict[DEBUG_MODE] = True
                print("Debug mode enabled")
            else:
                self.args_dict[DEBUG_MODE] = False
                print("Debug mode disabled")

    def _download_job_files(self):
        print("Authenticating...")
        fovus_api_adapter = FovusApiAdapter()
        fovus_s3_adapter = FovusS3Adapter(fovus_api_adapter, self.args_dict, self.args_dict[JOB_FILE_ROOT_DIRECTORY])
        fovus_s3_adapter.download_files()

    def _create_missing_directories(self):
        print("Creating missing config directories (if any)")
        for directory in (PATH_TO_CONFIG_ROOT, PATH_TO_JOB_CONFIGS, PATH_TO_USER_CONFIGS, PATH_TO_JOB_LOGS):
            if not os.path.exists(os.path.expanduser(directory)):
                os.makedirs(os.path.expanduser(directory), exist_ok=True)

    def _create_missing_empty_config_files(self):
        print("Creating missing empty config files (if any)")
        for config in FOVUS_PROVIDED_CONFIGS.values():
            empty_config_json_file_path = os.path.abspath(os.path.join(ROOT_DIR, config[PATH_TO_CONFIG_FILE_IN_REPO]))
            shutil.copy(empty_config_json_file_path, config[PATH_TO_CONFIG_FILE_LOCAL])

    def _get_job_current_status(self):
        print("Getting job current status...")
        fovus_api_adapter = FovusApiAdapter()
        job_current_status = fovus_api_adapter.get_job_current_status(self.args_dict[JOB_ID])
        print(GENERIC_SUCCESS)
        print(OUTPUTS)
        print("\n".join(("Job ID", self.args_dict[JOB_ID], "Job current status:", job_current_status)))

    def _upload_file(self):
        print("Authenticating...")
        fovus_api_adapter = FovusApiAdapter()
        fovus_s3_adapter = FovusS3Adapter(fovus_api_adapter, self.args_dict, self.args_dict[LOCAL_PATH])
        fovus_s3_adapter.upload_to_storage()

    def _login(self) -> None:
        fovus_sign_in_adapter = FovusSignInAdapter()
        fovus_sign_in_adapter.sign_in_concurrent()

    def _logout(self):
        print("Logging out...")

        fovus_cognito_adapter = FovusCognitoAdapter()
        fovus_cognito_adapter.sign_out()
        print(GENERIC_SUCCESS)

    def _user(self):
        fovus_api_adapter = FovusApiAdapter()
        fovus_api_adapter.print_user_info()
