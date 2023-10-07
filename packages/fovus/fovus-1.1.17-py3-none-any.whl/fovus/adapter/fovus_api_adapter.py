import copy
import json
import os
from enum import Enum
from functools import lru_cache
from http import HTTPStatus
from operator import itemgetter

import dateparser
import requests
from typing_extensions import TypedDict, Union

from fovus.adapter.fovus_cognito_adapter import FovusCognitoAdapter
from fovus.constants.benchmark_constants import (
    BENCHMARK_NAME,
    BOUNDS,
    COMPARISONS,
    COMPREHENSIONS,
    INCORRECTABLE_ERROR_MESSAGE_FROM_BOUNDS,
    IS_INVALID_CORRECTABLE,
)
from fovus.constants.cli_constants import (
    BENCHMARKING_PROFILE_NAME,
    COMPUTING_DEVICE,
    CPU,
    DEBUG_MODE,
    ENABLE_HYPERTHREADING,
    FOVUS_PROVIDED_CONFIGS,
    GPU,
    IS_SINGLE_THREADED_TASK,
    JOB_CONFIG_CONTAINERIZED_TEMPLATE,
    JOB_CONFIG_FILE_PATH,
    JOB_NAME,
    MAX_GPU,
    MAX_VCPU,
    MIN_GPU,
    MIN_GPU_MEM_GIB,
    MIN_VCPU,
    MONOLITHIC_OVERRIDE,
    PATH_TO_CONFIG_FILE_IN_REPO,
    SCALABLE_PARALLELISM,
    SCHEDULED_AT,
    SUPPORTED_CPU_ARCHITECTURES,
    TIMESTAMP,
)
from fovus.constants.fovus_api_constants import (
    BOUND_VALUE_CORRECTION_PRINT_ORDER,
    CONTAINERIZED,
    DEFAULT_TIMEZONE,
    ENVIRONMENT,
    IS_LICENSE_REQUIRED,
    JOB_STATUS,
    LICENSE_ADDRESS,
    LICENSE_COUNT_PER_TASK,
    LICENSE_CONSUMPTION_PROFILE_NAME,
    LICENSE_FEATURE,
    MONOLITHIC_LIST,
    PAYLOAD_CONSTRAINTS,
    PAYLOAD_DEBUG_MODE,
    PAYLOAD_JOB_CONSTRAINTS,
    PAYLOAD_JOB_NAME,
    PAYLOAD_TASK_CONSTRAINTS,
    PAYLOAD_TIMESTAMP,
    PAYLOAD_WORKSPACE_ID,
    SOFTWARE_NAME,
    SOFTWARE_VERSION,
    SOFTWARE_VERSIONS,
    TIMEOUT_SECONDS,
    VENDOR_NAME,
    Api,
    ApiMethod,
)
from fovus.exception.user_exception import UserException
from fovus.root_config import ROOT_DIR
from fovus.util.file_util import FileUtil
from fovus.util.fovus_api_util import FovusApiUtil
from fovus.util.util import Util


class AwsCognitoAuthType(Enum):
    USER_SRP_AUTH = "USER_SRP_AUTH"  # nosec


class UserAttribute(Enum):
    USER_ID = "custom:userId"


class UserInfo(TypedDict):
    email: str
    user_id: str
    workspace_name: str
    workspace_id: str


class FovusApiAdapter:
    user_id: str
    workspace_id: str
    fovus_cognito_adapter: FovusCognitoAdapter

    def __init__(self, fovus_cognito_adapter: Union[FovusCognitoAdapter, None] = None):
        if fovus_cognito_adapter is None:
            self.fovus_cognito_adapter = FovusCognitoAdapter()
        else:
            self.fovus_cognito_adapter = fovus_cognito_adapter

        self.user_id = self._get_user_id()
        self.workspace_id = self._get_workspace_id()

    def create_job(self, request):
        headers = self.fovus_cognito_adapter.get_authorization_header()
        response = requests.post(
            FovusApiUtil.get_api_address(Api.JOB, ApiMethod.CREATE_JOB),
            json=request,
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        return FovusApiUtil.confirm_successful_response(response.json(), response.status_code, self.__class__.__name__)

    def get_user_info(self) -> UserInfo:
        workspace = self.get_workspace()
        claims = self.fovus_cognito_adapter.get_claims()

        return {
            "email": claims["email"],
            "user_id": self.user_id,
            "workspace_name": workspace["workspaceName"],
            "workspace_id": self.workspace_id,
        }

    def print_user_info(self, title: Union[str, None] = None) -> UserInfo:
        user_info = self.get_user_info()
        print("------------------------------------------------")

        if title is not None:
            print(f"  {title}", "", sep="\n")

        print(
            "  User information:",
            "",
            f"  Email: {user_info['email']}",
            f"  User ID: {user_info['user_id']}",
            f"  Workspace Name: {user_info['workspace_name']}",
            f"  Workspace ID: {user_info['workspace_id']}",
            "------------------------------------------------",
            sep="\n",
        )
        return user_info

    def make_dynamic_changes_to_create_job_request(self, request):
        self._make_dynamic_changes_to_software(request)
        self._validate_benchmarking_profile(request)
        self._convert_scheduled_at_format(request)
        self._validate_scalable_parallelism(request)

    def _validate_scalable_parallelism(self, request):
        scalable_parallelism = request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][SCALABLE_PARALLELISM]
        min_vcpu = request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][MIN_VCPU]
        max_vcpu = request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][MAX_VCPU]
        min_gpu = request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][MIN_GPU]
        max_gpu = request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][MAX_GPU]
        benchmark_profile_name = request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][BENCHMARKING_PROFILE_NAME]
        computing_device = request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][COMPUTING_DEVICE]

        if computing_device == CPU and not scalable_parallelism and min_vcpu != max_vcpu:
            print(
                f"Scalable parallelism is false for Benchmarking profile '{benchmark_profile_name}'. The value of "
                + "maxvCpu must be equal to that of minvCpu to define a user-specified parallelism. Overriding "
                + f"maxvCpu ({max_vcpu}) with minvCpu ({min_vcpu})."
            )
            request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][MAX_VCPU] = min_vcpu

        if computing_device == GPU and not scalable_parallelism and min_gpu != max_gpu:
            print(
                f"Scalable parallelism is false for Benchmarking profile '{benchmark_profile_name}'. The value of "
                + "maxGpu must be equal to that of minGpu to define a user-specified parallelism. Overriding maxGpu "
                + f"({max_gpu}) with minGpu ({min_gpu})."
            )
            request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][MAX_GPU] = min_gpu

    def _ensure_is_single_threaded_task_filled(self, request):
        if (
            request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][COMPUTING_DEVICE] == CPU
            and IS_SINGLE_THREADED_TASK not in request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS]
        ):
            print(
                f"Field '{IS_SINGLE_THREADED_TASK}' is now required in '{PAYLOAD_TASK_CONSTRAINTS}' for create job "
                f"requests where '{COMPUTING_DEVICE}' is '{CPU}' and one of the following is true:"
                f"\n\t- Job environment is '{CONTAINERIZED}'"
                f"\n\t- Job environment is monolithic and any software in '{MONOLITHIC_LIST}' "
                "does not require a license."
                f"\nAutofilling '{IS_SINGLE_THREADED_TASK}' with default value of False."
            )
            request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][IS_SINGLE_THREADED_TASK] = False

    def _make_dynamic_changes_to_software(self, request):
        print("Validating software...")
        if MONOLITHIC_LIST not in request[ENVIRONMENT]:
            print("Request is for a containerized job. Filling missing/empty vendorName fields is not required.")
            self._ensure_is_single_threaded_task_filled(request)
            return
        
        license_consumption_profiles = self.get_license_consumption_profiles(request[PAYLOAD_WORKSPACE_ID])
        list_software_response = self.list_software()
        for i, monolithic_list_item in enumerate(copy.deepcopy(request[ENVIRONMENT][MONOLITHIC_LIST])):
            software_name = monolithic_list_item[SOFTWARE_NAME]
            software_version = monolithic_list_item[SOFTWARE_VERSION]
            software_vendor = monolithic_list_item[VENDOR_NAME]

            valid_software_names = []
            is_valid_software_name = False
            for valid_software_vendor in list_software_response:
                if software_name in list_software_response[valid_software_vendor]:
                    is_valid_software_name = True
                    if (
                        software_version
                        in list_software_response[valid_software_vendor][software_name][SOFTWARE_VERSIONS]
                    ):
                        software_supported_architectures = list_software_response[valid_software_vendor][software_name][SOFTWARE_VERSIONS][software_version]
                        for architecture in request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][SUPPORTED_CPU_ARCHITECTURES]:
                            if architecture not in software_supported_architectures:
                                raise UserException(
                                    HTTPStatus.BAD_REQUEST,
                                    self.__class__.__name__,
                                    f"Supported Cpu architectures '{request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][SUPPORTED_CPU_ARCHITECTURES]}' "
                                    + f"for software name '{software_name}' and version '{software_version}' is not valid."
                                    + f" Valid Supported Cpu architectures for version '{software_version}' : "
                                    + str(software_supported_architectures),
                                )

                        if valid_software_vendor != software_vendor:
                            print(
                                f"Replacing vendor name '{software_vendor}' with "
                                f"'{valid_software_vendor}' for monolithic list item {monolithic_list_item}."
                            )
                            request[ENVIRONMENT][MONOLITHIC_LIST][i][VENDOR_NAME] = valid_software_vendor
                        if list_software_response[valid_software_vendor][software_name][IS_LICENSE_REQUIRED]:
                            self._ensure_is_single_threaded_task_filled(request)
                            self._confirm_required_fields_for_licensed_software(monolithic_list_item, license_consumption_profiles)
                        break  # Successful validation of current list item.
                    raise UserException(
                        HTTPStatus.BAD_REQUEST,
                        self.__class__.__name__,
                        f"Software version '{software_version}' for software name '{software_name}' is not valid. "
                        + "Valid software versions: "
                        + str(list_software_response[valid_software_vendor][software_name][SOFTWARE_VERSIONS]),
                    )
                valid_software_names.append(
                    {valid_software_vendor: list(list_software_response[valid_software_vendor].keys())}
                )
            if not is_valid_software_name:
                raise UserException(
                    HTTPStatus.BAD_REQUEST,
                    self.__class__.__name__,
                    f"Software name '{software_name}' is not valid. "
                    + "Valid software vendors and names (format: [{vendor: [name, ...]}, ...]): "
                    + str(valid_software_names),
                )

    def _confirm_required_fields_for_licensed_software(self, monolithic_list_item, license_consumption_profiles):
        error_messages = []
        if not monolithic_list_item.get(LICENSE_ADDRESS):
            error_messages.append(f"Non-empty '{LICENSE_ADDRESS}'")
        if not monolithic_list_item.get(LICENSE_FEATURE):
            error_messages.append(f"Non-empty '{LICENSE_FEATURE}'")

        if not monolithic_list_item.get(LICENSE_COUNT_PER_TASK) and not monolithic_list_item.get(LICENSE_CONSUMPTION_PROFILE_NAME):
            error_messages.append(f"Must required '{LICENSE_COUNT_PER_TASK}' or '{LICENSE_CONSUMPTION_PROFILE_NAME}'.")

        if monolithic_list_item.get(LICENSE_CONSUMPTION_PROFILE_NAME):
            software_key = f"{monolithic_list_item[SOFTWARE_NAME]}#{monolithic_list_item[VENDOR_NAME]}"
            profile_list = FovusApiUtil.get_license_consuption_profile_list(license_consumption_profiles)
            if software_key not in license_consumption_profiles:
                error_messages.append(f"Invalid license consumption profile: '{LICENSE_CONSUMPTION_PROFILE_NAME}' for software `{monolithic_list_item[SOFTWARE_NAME]}'.")
            elif monolithic_list_item.get(LICENSE_CONSUMPTION_PROFILE_NAME) not in profile_list:
                error_messages.append(f"Invalid license consumption profile: '{monolithic_list_item.get(LICENSE_CONSUMPTION_PROFILE_NAME)}'. " + f"Valid license consumption profiles: {profile_list}")
            elif monolithic_list_item.get(LICENSE_FEATURE) and monolithic_list_item.get(LICENSE_FEATURE) not in license_consumption_profiles[software_key]:
                feature_list = []
                for featureMap in license_consumption_profiles.values():
                    for feature, profiles in featureMap.items():
                        if monolithic_list_item.get(LICENSE_CONSUMPTION_PROFILE_NAME) in profiles:
                            feature_list.append(feature)
                error_messages.append(f"Invalid license feature '{monolithic_list_item.get(LICENSE_FEATURE)}'. '{monolithic_list_item.get(LICENSE_CONSUMPTION_PROFILE_NAME)}' profile only supports these features: {feature_list}")
        elif (
            not isinstance(monolithic_list_item.get(LICENSE_COUNT_PER_TASK), int)
            or monolithic_list_item.get(LICENSE_COUNT_PER_TASK) < 0
        ):
            error_messages.append(f"Non-negative integer '{LICENSE_COUNT_PER_TASK}'")
        if error_messages:
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                self.__class__.__name__,
                f"The following are required for {MONOLITHIC_LIST} item {monolithic_list_item} "
                f"in order for license queue and auto-scaling to take effect:"
                + "\n\t- "
                + "\n\t- ".join(error_messages),
            )

    def _validate_benchmarking_profile(self, request):  # pylint: disable=too-many-locals
        benchmarking_profile_name = request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][BENCHMARKING_PROFILE_NAME]
        hyperthreading_enabled = request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][ENABLE_HYPERTHREADING]
        print(
            f"Validating the benchmarking profile '{benchmarking_profile_name}' and "
            "updating values if necessary and possible..."
        )
        list_benchmark_profile_response = self.list_benchmarking_profile(request[PAYLOAD_WORKSPACE_ID])
        valid_benchmarking_profile_names = []
        for current_benchmarking_profile in list_benchmark_profile_response:  # pylint: disable=too-many-nested-blocks
            current_benchmarking_profile_name = current_benchmarking_profile[BENCHMARK_NAME]
            valid_benchmarking_profile_names.append(current_benchmarking_profile_name)
            if benchmarking_profile_name == current_benchmarking_profile_name:
                validations_config = FovusApiUtil.get_benchmark_validations_config(request)
                FovusApiUtil.print_benchmark_hyperthreading_info(hyperthreading_enabled)
                FovusApiUtil.validate_computing_device(
                    request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][COMPUTING_DEVICE],
                    current_benchmarking_profile,
                )
                FovusApiUtil.validate_cpu_architectures(
                    request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][SUPPORTED_CPU_ARCHITECTURES],
                    current_benchmarking_profile,
                )
                corrected_value_messages = {}
                for validation_type in validations_config:  # pylint: disable=consider-using-dict-items
                    for bound_to_validate in validations_config[validation_type][BOUNDS]:
                        current_value = itemgetter(*bound_to_validate)(  # Multiple values may be retrieved.
                            request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS]
                        )
                        benchmarking_profile_bounds = FovusApiUtil.get_benchmark_profile_bounds(
                            current_benchmarking_profile,
                            bound_to_validate,
                            request,
                            source=self.__class__.__name__,
                        )
                        for is_invalid, comprehension in zip(COMPARISONS, COMPREHENSIONS):
                            if is_invalid in validations_config[validation_type]:
                                benchmarking_profile_item_bound = validations_config[validation_type][comprehension](
                                    benchmarking_profile_bounds
                                )
                                if validations_config[validation_type][is_invalid](
                                    current_value, benchmarking_profile_item_bound
                                ):
                                    if is_invalid == IS_INVALID_CORRECTABLE:
                                        bound_to_validate = bound_to_validate[
                                            0  # Correctable bounds are single values stored in tuples.
                                        ]
                                        corrected_value_messages[
                                            bound_to_validate
                                        ] = FovusApiUtil.get_corrected_value_message(
                                            validation_type,
                                            benchmarking_profile_name,
                                            bound_to_validate,
                                            benchmarking_profile_item_bound,
                                            hyperthreading_enabled,
                                            current_value,
                                        )
                                        request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][
                                            bound_to_validate
                                        ] = benchmarking_profile_item_bound
                                    else:
                                        raise UserException(
                                            HTTPStatus.BAD_REQUEST,
                                            self.__class__.__name__,
                                            f"Invalid value of {current_value} for "
                                            f"{Util.get_message_from_list(bound_to_validate)} with "
                                            f"benchmarking profile '{benchmarking_profile_name}'. "
                                            + validations_config[validation_type][
                                                INCORRECTABLE_ERROR_MESSAGE_FROM_BOUNDS
                                            ](bound_to_validate, benchmarking_profile_bounds, hyperthreading_enabled),
                                        )
                for bound_value_correction in BOUND_VALUE_CORRECTION_PRINT_ORDER:
                    if bound_value_correction in corrected_value_messages:
                        print(corrected_value_messages[bound_value_correction])
                return  # Successful validation.

        raise UserException(
            HTTPStatus.BAD_REQUEST,
            self.__class__.__name__,
            f"Invalid benchmarking profile: '{benchmarking_profile_name}'. "
            + f"Valid benchmarking profiles: {valid_benchmarking_profile_names}",
        )

    def _convert_scheduled_at_format(self, request):
        job_scheduled_at = request.get(SCHEDULED_AT)
        if job_scheduled_at:
            print("Converting value for scheduledAt to ISO 8601 (if needed)...")
            scheduled_at_iso = dateparser.parse(
                job_scheduled_at,
                settings={
                    "RETURN_AS_TIMEZONE_AWARE": True,
                    "TO_TIMEZONE": DEFAULT_TIMEZONE,
                    "PREFER_DATES_FROM": "future",
                },
            )
            if not scheduled_at_iso:
                raise UserException(
                    HTTPStatus.BAD_REQUEST,
                    self.__class__.__name__,
                    f"Invalid value of '{job_scheduled_at}' for '{SCHEDULED_AT}'. See --help for recommended "
                    "formats.",
                )
            print(f"Create job scheduled at: {scheduled_at_iso.isoformat()}")
            request[SCHEDULED_AT] = scheduled_at_iso.isoformat()

    def get_file_download_token(self, request):
        headers = self.fovus_cognito_adapter.get_authorization_header()
        response = requests.post(
            FovusApiUtil.get_api_address(Api.FILE, ApiMethod.GET_FILE_DOWNLOAD_TOKEN),
            json=request,
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        return FovusApiUtil.confirm_successful_response(response.json(), response.status_code, self.__class__.__name__)

    def get_file_upload_token(self, request):
        headers = self.fovus_cognito_adapter.get_authorization_header()
        response = requests.post(
            FovusApiUtil.get_api_address(Api.FILE, ApiMethod.GET_FILE_UPLOAD_TOKEN),
            json=request,
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        return FovusApiUtil.confirm_successful_response(response.json(), response.status_code, self.__class__.__name__)

    def get_temporary_s3_upload_credentials(self):
        upload_credentials = self.get_file_upload_token(
            FovusApiAdapter.get_file_upload_download_token_request(self.workspace_id)
        )
        return FovusApiUtil.get_s3_info(upload_credentials)

    def get_temporary_s3_download_credentials(self):
        download_credentials = self.get_file_download_token(
            FovusApiAdapter.get_file_upload_download_token_request(self.workspace_id)
        )
        return FovusApiUtil.get_s3_info(download_credentials)

    def get_job_current_status(self, job_id):
        job_info = self.get_job_info(FovusApiAdapter.get_job_info_request(self.workspace_id, job_id))
        return job_info[JOB_STATUS]

    def get_job_info(self, request):
        headers = self.fovus_cognito_adapter.get_authorization_header()
        response = requests.post(
            FovusApiUtil.get_api_address(Api.JOB, ApiMethod.GET_JOB_INFO),
            json=request,
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        return FovusApiUtil.confirm_successful_response(response.json(), response.status_code, self.__class__.__name__)

    def list_software(self):
        headers = self.fovus_cognito_adapter.get_authorization_header()
        response = requests.get(
            FovusApiUtil.get_api_address(Api.SOFTWARE, ApiMethod.LIST_SOFTWARE),
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        return FovusApiUtil.confirm_successful_response(response.json(), response.status_code, self.__class__.__name__)
    
    def get_license_consumption_profiles(self, workspace_id):
        headers = self.fovus_cognito_adapter.get_authorization_header()
        response = requests.get(
            FovusApiUtil.get_api_address(Api.LICENSE, ApiMethod.GET_LICENSE_CONSUMPTION_PROFILE),
            params={"workspaceId": workspace_id},
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        return FovusApiUtil.confirm_successful_response(response.json(), response.status_code, self.__class__.__name__)

    def list_benchmarking_profile(self, workspace_id):
        headers = self.fovus_cognito_adapter.get_authorization_header()
        response = requests.get(
            FovusApiUtil.get_api_address(Api.BENCHMARK, ApiMethod.LIST_BENCHMARK_PROFILE),
            params={"workspaceId": workspace_id},
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        return FovusApiUtil.confirm_successful_response(response.json(), response.status_code, self.__class__.__name__)

    def _get_user_id(self) -> str:
        claims = self.fovus_cognito_adapter.get_claims()
        return claims[UserAttribute.USER_ID.value]

    def get_user_id(self) -> str:
        return self.user_id

    @lru_cache
    def get_workspace(self) -> dict:
        headers = self.fovus_cognito_adapter.get_authorization_header()
        response = requests.get(
            FovusApiUtil.get_api_address(
                Api.WORKSPACE,
                ApiMethod.LIST_WORKSPACES,
            ),
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        res = FovusApiUtil.confirm_successful_response(response.json(), response.status_code, self.__class__.__name__)

        try:
            return res[0]
        except Exception as exc:
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                self.__class__.__name__,
                "Unable to retrieve workspace. Please check that you have a workspace.",
            ) from exc

    def _get_workspace_id(self) -> str:
        workspace = self.get_workspace()
        return workspace["workspaceId"]

    def get_workspace_id(self) -> str:
        return self.workspace_id

    @staticmethod
    def get_create_job_request(cli_dict, user_id: str, workspace_id: str):
        with FileUtil.open(os.path.expanduser(cli_dict[JOB_CONFIG_FILE_PATH])) as job_config_file:
            create_job_request = json.load(job_config_file)
            FovusApiAdapter._add_create_job_request_remaining_fields(
                create_job_request, cli_dict, user_id, workspace_id
            )
            FovusApiAdapter._apply_cli_overrides_to_request(create_job_request, cli_dict)
            FovusApiAdapter._apply_computing_device_overrides(create_job_request)
            return create_job_request

    @staticmethod
    def _add_create_job_request_remaining_fields(create_job_request, cli_dict, user_id: str, workspace_id: str):
        create_job_request[PAYLOAD_DEBUG_MODE] = cli_dict[DEBUG_MODE]
        create_job_request[PAYLOAD_TIMESTAMP] = cli_dict[TIMESTAMP]
        create_job_request[PAYLOAD_WORKSPACE_ID] = workspace_id
        if cli_dict.get(JOB_NAME):
            create_job_request[PAYLOAD_JOB_NAME] = cli_dict[JOB_NAME]
        else:
            timestamp = create_job_request[PAYLOAD_TIMESTAMP]
            create_job_request[PAYLOAD_JOB_NAME] = FovusApiUtil.get_job_id_with_timestamp(timestamp, user_id)

    @staticmethod
    def _apply_cli_overrides_to_request(create_job_request, cli_dict):
        print("Applying CLI overrides to create job request...")
        FovusApiAdapter._apply_single_field_overrides(create_job_request, cli_dict)
        FovusApiAdapter._apply_monolithic_list_overrides(create_job_request, cli_dict)

    @staticmethod
    def _apply_single_field_overrides(create_job_request, cli_dict):
        # The empty create job request is used to reference keys in the event that the provided config is not complete
        # and CLI arguments are being used to replace the remaining values.
        with FileUtil.open(
            os.path.join(
                ROOT_DIR, FOVUS_PROVIDED_CONFIGS[JOB_CONFIG_CONTAINERIZED_TEMPLATE][PATH_TO_CONFIG_FILE_IN_REPO]
            ),
        ) as empty_job_config_file:
            empty_create_job_request = json.load(empty_job_config_file)
            del empty_create_job_request[ENVIRONMENT]

            FovusApiAdapter._apply_overrides_to_root_keys(create_job_request, empty_create_job_request, cli_dict)
            for empty_sub_dict, create_job_request_sub_dict in FovusApiAdapter._get_deepest_sub_dict_pairs(
                empty_create_job_request, create_job_request
            ):
                FovusApiAdapter._apply_cli_overrides_to_sub_dict(create_job_request_sub_dict, empty_sub_dict, cli_dict)

    @staticmethod
    def _apply_monolithic_list_overrides(create_job_request, cli_dict):
        environment = create_job_request[ENVIRONMENT]
        if MONOLITHIC_LIST in environment:
            for monolithic in environment[MONOLITHIC_LIST]:
                for vendor_name, software_name, license_feature, new_license_count_per_task in cli_dict[
                    MONOLITHIC_OVERRIDE
                ]:
                    if (
                        monolithic[VENDOR_NAME] == vendor_name
                        and monolithic[SOFTWARE_NAME] == software_name
                        and monolithic[LICENSE_FEATURE] == license_feature
                    ):
                        print(
                            f"CLI override found for monolithic item with keys: {vendor_name}, {software_name}, and "
                            f"{license_feature}. Overriding default license count per task of "
                            f"{monolithic[LICENSE_COUNT_PER_TASK]} with {new_license_count_per_task}."
                        )
                        monolithic[LICENSE_COUNT_PER_TASK] = int(new_license_count_per_task)

    @staticmethod
    def _apply_overrides_to_root_keys(create_job_request, empty_create_job_request, cli_dict):
        for key in empty_create_job_request:
            if not isinstance(key, dict):
                new_value = cli_dict.get(key)
                if new_value:
                    print(
                        f"CLI override found for key: {key}. Overriding default value of "
                        f"'{create_job_request.get(key)}' "
                        f"with '{new_value}'."
                    )
                    create_job_request[key] = new_value

    @staticmethod
    def _get_deepest_sub_dict_pairs(empty_create_job_request, create_job_request):
        sub_dict_pairs = []
        for key in empty_create_job_request.keys():
            if isinstance(empty_create_job_request[key], dict):
                if key not in create_job_request:
                    create_job_request[key] = {}
                sub_sub_dict_pairs = FovusApiAdapter._get_deepest_sub_dict_pairs(
                    empty_create_job_request[key], create_job_request[key]
                )
                if sub_sub_dict_pairs:
                    sub_dict_pairs.extend(sub_sub_dict_pairs)
                else:
                    sub_dict_pairs.append((empty_create_job_request[key], create_job_request[key]))
        return sub_dict_pairs

    @staticmethod
    def _apply_cli_overrides_to_sub_dict(sub_dict, empty_sub_dict, cli_dict):
        for sub_dict_parameter_key in empty_sub_dict.keys():
            cli_dict_value = cli_dict.get(sub_dict_parameter_key)
            if cli_dict[sub_dict_parameter_key] is not None:
                print(
                    f"CLI override found for key: {sub_dict_parameter_key}. Overriding default job config value of "
                    f"{sub_dict.get(sub_dict_parameter_key)} with {cli_dict[sub_dict_parameter_key]}."
                )
                if isinstance(cli_dict_value, str) and cli_dict_value.isdigit():
                    cli_dict_value = int(cli_dict_value)
                sub_dict[sub_dict_parameter_key] = cli_dict_value

    @staticmethod
    def _apply_computing_device_overrides(create_job_request):
        value_was_overridden = False
        computing_device = create_job_request[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][COMPUTING_DEVICE]
        print(f"Computing device is {computing_device}. Overriding related constraints if needed...")
        if computing_device == CPU:
            for field in [MIN_GPU, MAX_GPU, MIN_GPU_MEM_GIB]:
                current_field_value = create_job_request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][field]
                if current_field_value != 0:
                    print(f"Overriding current {field} value of {current_field_value} with 0.")
                    value_was_overridden = True
                    create_job_request[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][field] = 0
        if not value_was_overridden:
            print("No overrides necessary.")

    @staticmethod
    def get_file_upload_download_token_request(workspace_id: str, duration_seconds=3600):
        return {"workspaceId": workspace_id, "durationSeconds": duration_seconds}

    @staticmethod
    def get_job_info_request(workspace_id: str, job_id):
        return {"workspaceId": workspace_id, "jobId": job_id}
