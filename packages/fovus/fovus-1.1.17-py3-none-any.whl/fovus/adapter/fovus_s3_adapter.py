import concurrent.futures
import json
import logging
import os
import random
import time
from enum import Enum
from http import HTTPStatus
from io import BufferedReader, BufferedWriter
from threading import Lock

from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import ObjectTypeDef
from tqdm import tqdm
from typing_extensions import Any, Callable, Optional, Type, TypedDict, TypeVar, Union

from fovus.adapter.fovus_api_adapter import FovusApiAdapter
from fovus.config.config import Config
from fovus.constants.cli_constants import (
    CLI_ARGUMENTS,
    DOMAIN_NAME,
    EXCLUDE_INPUT,
    EXCLUDE_OUTPUT,
    FOVUS_PATH,
    INCLUDE_INPUT,
    INCLUDE_OUTPUT,
    JOB_ID,
    SKIP_CREATE_JOB_INFO_FOLDER,
)
from fovus.exception.user_exception import UserException
from fovus.util.aws_util import AwsUtil
from fovus.util.file_util import FOVUS_JOB_INFO_FOLDER, FileUtil
from fovus.util.fovus_api_util import FovusApiUtil
from fovus.util.fovus_s3_adapter_util import FovusS3AdapterUtil
from fovus.util.util import Util

DOWNLOAD = "Download"
LOCAL_FILEPATH = "local_filepath"
SUCCESS = "success"
UPLOAD = "Upload"

JOB_DATA_FILENAME = "job_data.json"

SECONDS_PER_MINUTE = 60
S3_TIMEOUT_MINUTES = 55

DOWNLOAD_FILE_EXTENSION = ".fovusdownload"


class S3Info(TypedDict):
    s3_client: S3Client
    s3_bucket: str
    s3_prefix: str
    expires_at: float


class CachedFileData(TypedDict):
    last_modified: float
    s3_hash: str


CachedFileDataMapping = dict[str, CachedFileData]


class UploadType(Enum):
    UPLOAD = "upload"
    UPLOAD_TO_STORAGE = "upload_to_storage"


# pylint: disable=R0902
class FovusS3Adapter:
    download_s3_info: Union[S3Info, None]
    upload_s3_info: Union[S3Info, None]
    cached_file_data: CachedFileDataMapping
    upload_type: Union[UploadType, None]
    fovus_path: Union[str, None]

    def __init__(self, fovus_api_adapter: FovusApiAdapter, cli_dict, root_directory_path: str):
        self.fovus_api_adapter: FovusApiAdapter = fovus_api_adapter
        self.cli_dict = cli_dict
        self.local_root_directory_path = root_directory_path

        user_id = fovus_api_adapter.get_user_id()

        self.job_id = FovusApiUtil.get_job_id(self.cli_dict, user_id)
        self.cached_file_data = self._load_cached_file_data()

        # Assigned if upload function is called.
        self.local_filepath_list = None
        self.task_count = None
        self.total_file_size_bytes = None
        self.download_s3_info = None
        self.upload_s3_info = None
        self.upload_type = None

        # Assigned if upload_to_storage function is called.
        self.fovus_path = None

    def get_job_id(self):
        return self.job_id

    def upload_files(self):
        self._validate_root_directory()
        self._instantiate_upload_instance_variables()
        FovusS3AdapterUtil.print_pre_operation_information(
            UPLOAD, len(self.local_filepath_list), self.total_file_size_bytes, self.task_count
        )
        self._operate_on_s3_in_parallel(self.local_filepath_list, self._upload_file)
        self._create_job_data_file()
        FovusS3AdapterUtil.print_post_operation_success(UPLOAD, is_success=True)

    def _print_uploaded_file_info(self):
        print(
            "\n".join(
                [
                    "-------------------------",
                    "Fovus Storage Information",
                    "-------------------------",
                    "URL: " + self._get_upload_to_storage_url(),
                    "Full Path: " + self._get_upload_to_storage_path(full_path=True),
                    "Relative Path: " + self._get_upload_to_storage_path(),
                ]
            )
        )

    def _get_upload_to_storage_url(self):
        url = "https://www." + Config.get(DOMAIN_NAME)

        if isinstance(self.local_root_directory_path, str) and os.path.isdir(self.local_root_directory_path):
            url += "/folders?path="
        else:
            url += "/files?path="

        if isinstance(self.fovus_path, str):
            url += self.fovus_path.strip("/").strip("\\") + "/"

        if isinstance(self.local_root_directory_path, str):
            basename = os.path.basename(self.local_root_directory_path.strip("/").strip("\\"))
            url += basename

        return url

    def _get_upload_to_storage_path(self, full_path: bool = False):
        path = "/files/" if full_path else ""

        if isinstance(self.fovus_path, str):
            path += self.fovus_path.strip("/").strip("\\") + "/"

        if isinstance(self.local_root_directory_path, str):
            basename = os.path.basename(self.local_root_directory_path.strip("/").strip("\\"))
            path += basename

        return path

    def upload_to_storage(self):
        self._instantiate_upload_to_storage_instance_variables()
        FovusS3AdapterUtil.print_pre_operation_information(
            UPLOAD, len(self.local_filepath_list), self.total_file_size_bytes
        )
        self._operate_on_s3_in_parallel(self.local_filepath_list, self._upload_file)
        FovusS3AdapterUtil.print_post_operation_success(UPLOAD, is_success=True)
        self._print_uploaded_file_info()

    def _validate_root_directory(self):
        if FileUtil.directory_contains_directory(self.local_root_directory_path, FOVUS_JOB_INFO_FOLDER):
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                self.__class__.__name__,
                "Root directory cannot contain a .fovus folder. Please remove it and try again. "
                + "\nNote: The .fovus folder is hidden, so you may need to adjust your file explorer's settings "
                + "to show hidden folders.",
            )

    def _create_job_data_file(self):
        if self.cli_dict.get(SKIP_CREATE_JOB_INFO_FOLDER):
            print(
                f"The {SKIP_CREATE_JOB_INFO_FOLDER} flag is set, so the {FOVUS_JOB_INFO_FOLDER} folder will not be "
                "created. Future operations on this job will require manual job ID specification using one of the "
                f"following CLI arguments: {CLI_ARGUMENTS[JOB_ID]}."
            )
            return

        job_data = {
            "job_id": self.job_id,
        }
        fovus_job_info_directory_path = os.path.join(self.local_root_directory_path, FOVUS_JOB_INFO_FOLDER)
        os.makedirs(fovus_job_info_directory_path, exist_ok=True)
        job_data_filepath = os.path.join(fovus_job_info_directory_path, JOB_DATA_FILENAME)
        with FileUtil.open(job_data_filepath, "w") as job_data_file:
            json.dump(job_data, job_data_file)

    def download_files(self):
        print("Retrieving file list from server...")
        s3_object_list = self._get_s3_object_list()

        if len(s3_object_list) == 0:
            raise UserException(
                HTTPStatus.NOT_FOUND,
                self.__class__.__name__,
                "Unable to retrieve file list from server. Please check your job ID and try again.",
            )

        s3_info = self._get_download_s3_info()
        s3_prefix = s3_info["s3_prefix"]

        objects_to_download, self.total_file_size_bytes, self.task_count = AwsUtil.get_s3_object_list_info(
            s3_object_list, s3_prefix, self.cli_dict[INCLUDE_OUTPUT], self.cli_dict[EXCLUDE_OUTPUT]
        )
        FovusS3AdapterUtil.print_pre_operation_information(
            DOWNLOAD, len(objects_to_download), self.total_file_size_bytes, self.task_count
        )
        FileUtil.create_missing_directories(
            self.local_root_directory_path,
            AwsUtil.get_all_directories(
                objects_to_download,
                s3_prefix,
                self.cli_dict[INCLUDE_OUTPUT],
                self.cli_dict[EXCLUDE_OUTPUT],
            ),
        )
        self._operate_on_s3_in_parallel(objects_to_download, self._download_file)
        FovusS3AdapterUtil.print_post_operation_success(DOWNLOAD, is_success=True)

    def _operate_on_s3_in_parallel(self, remaining_items: list, file_operation: Callable[[Any, tqdm], Any]):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            progress_bar = tqdm(
                total=self.total_file_size_bytes, unit="B", desc="Progress", unit_scale=True, unit_divisor=1024
            )
            self._try_operate_on_file_list(file_operation, executor, remaining_items, progress_bar)
            progress_bar.close()

    Out = TypeVar("Out")

    def exponential_backoff_retry(
        self,
        function: Callable[..., Out],
        max_retries=5,
        exceptions_to_raise: Union[list[Type[BaseException]], None] = None,
        base=2,
        multiplier=1,
        randomize_sleep=True,
    ) -> Callable[..., Out]:
        def wrapper(*args, **kwargs):
            retry_count = 0
            while True:
                try:
                    return function(*args, **kwargs)
                except BaseException as exc:  # pylint: disable=broad-except
                    logging.error("Exception caught by exponential_backoff_retry.")
                    logging.exception(exc)

                    if retry_count >= max_retries - 1 or (
                        isinstance(exceptions_to_raise, list)
                        and any(isinstance(exc, exception) for exception in exceptions_to_raise)
                    ):
                        raise exc

                    time.sleep(
                        (base**retry_count) * multiplier * (random.random() if randomize_sleep else 1)  # nosec B311
                    )
                    retry_count += 1

                    logging.info("Retrying function.")

        return wrapper

    def _try_operate_on_file_list(
        self,
        file_operation: Callable[[Any, tqdm], Any],
        executor: concurrent.futures.ThreadPoolExecutor,
        remaining_objects: Union[list[str], list[ObjectTypeDef]],
        progress_bar: tqdm,
    ):
        futures_to_obj = {executor.submit(file_operation, obj, progress_bar): obj for obj in remaining_objects}

        for future in concurrent.futures.as_completed(futures_to_obj):
            obj = futures_to_obj[future]
            key = obj if isinstance(obj, str) else obj["Key"]

            try:
                future.result()
            except BaseException as exc:  # pylint: disable=broad-except
                logging.error("Exception caught in _try_operate_on_file_list for %s.", key)
                logging.exception(exc)

    def _instantiate_upload_instance_variables(self):
        print("Preparing to upload files.")
        self.upload_type = UploadType.UPLOAD
        self.local_filepath_list, self.task_count, self.total_file_size_bytes = FileUtil.get_files_in_job_directory(
            self.local_root_directory_path, self.cli_dict[INCLUDE_INPUT], self.cli_dict[EXCLUDE_INPUT]
        )
        self._validate_upload_job()

    def _instantiate_upload_to_storage_instance_variables(self) -> None:
        print("Preparing to upload files.")
        self.upload_type = UploadType.UPLOAD_TO_STORAGE

        if isinstance(self.cli_dict[FOVUS_PATH], str):
            self.fovus_path = self.cli_dict[FOVUS_PATH]

        if isinstance(self.fovus_path, str) and not self.fovus_path.endswith("/"):
            self.fovus_path += "/"

        self.local_filepath_list, self.total_file_size_bytes = FileUtil.get_files_in_storage_directory(
            self.local_root_directory_path, self.cli_dict[INCLUDE_INPUT], self.cli_dict[EXCLUDE_INPUT]
        )
        self._validate_upload_to_storage()

    def _validate_upload_job(self):
        errors = []
        if self.task_count == 0:
            errors.append("tasks")
        if len(self.local_filepath_list) == 0:
            errors.append("files")
        if errors:
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                self.__class__.__name__,
                f"No {' or '.join(errors)} found to upload. Please check your include/exclude filters.",
            )

    def _validate_upload_to_storage(self):
        if len(self.local_filepath_list) == 0:
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                self.__class__.__name__,
                "No files found to upload. Please check your include/exclude filters.",
            )

    def _s3_initiate_multipart_upload(self, bucket_name: str, key: str) -> str:
        def file_operation() -> str:
            s3_info = self._get_upload_s3_info()
            response = s3_info["s3_client"].create_multipart_upload(Bucket=bucket_name, Key=key)
            return response["UploadId"]

        s3_info = self._get_upload_s3_info()
        s3_exceptions = s3_info["s3_client"].exceptions

        wrapped_file_operation = self.exponential_backoff_retry(
            file_operation,
            exceptions_to_raise=[s3_exceptions.NoSuchBucket],
        )

        return wrapped_file_operation()

    def _s3_upload_multipart_part(
        self,
        data: bytes,
        upload_id: str,
        bucket_name: str,
        key: str,
        part_number: int,
        callback: Optional[Callable[[int], Any]],
    ) -> Any:
        def file_operation() -> Any:
            s3_info = self._get_upload_s3_info()

            response = s3_info["s3_client"].upload_part(
                Bucket=bucket_name, Key=key, PartNumber=part_number, UploadId=upload_id, Body=data
            )
            part = {"PartNumber": part_number, "ETag": response["ETag"]}

            if callback:
                callback(len(data))

            return part

        s3_info = self._get_upload_s3_info()
        s3_exceptions = s3_info["s3_client"].exceptions

        wrapped_file_operation = self.exponential_backoff_retry(
            file_operation,
            exceptions_to_raise=[s3_exceptions.NoSuchBucket],
        )

        return wrapped_file_operation()

    def _s3_complete_multipart_upload(self, upload_id: str, bucket_name: str, key: str, parts: list) -> None:
        def file_operation() -> None:
            s3_info = self._get_upload_s3_info()
            s3_info["s3_client"].complete_multipart_upload(
                Bucket=bucket_name, Key=key, UploadId=upload_id, MultipartUpload={"Parts": parts}
            )

        s3_info = self._get_upload_s3_info()
        s3_exceptions = s3_info["s3_client"].exceptions

        wrapped_file_operation = self.exponential_backoff_retry(
            file_operation,
            exceptions_to_raise=[s3_exceptions.NoSuchBucket],
        )

        wrapped_file_operation()

    def _s3_multipart_upload(
        self,
        bucket_name: str,
        file_path: str,
        key: str,
        callback: Optional[Callable[[int], None]],
        chunk_size: int,
    ) -> None:
        upload_id = self._s3_initiate_multipart_upload(bucket_name, key)

        file_size = os.path.getsize(file_path)
        num_parts = (file_size + chunk_size - 1) // chunk_size

        parts = []
        file_lock = Lock()

        file: BufferedReader
        with open(file_path, "rb") as file:

            def upload_part_operation(part_number: int):
                with file_lock:
                    file.seek(chunk_size * part_number)
                    data = file.read(chunk_size)

                part = self._s3_upload_multipart_part(data, upload_id, bucket_name, key, part_number + 1, callback)

                return part

            executor: concurrent.futures.ThreadPoolExecutor
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                for part in executor.map(upload_part_operation, range(num_parts)):
                    parts.append(part)

        parts = sorted(parts, key=lambda k: k["PartNumber"])

        self._s3_complete_multipart_upload(upload_id, bucket_name, key, parts)

    def _s3_put_object(
        self, bucket_name: str, file_path: str, key: str, callback: Optional[Callable[[int], None]]
    ) -> None:
        with open(file_path, "rb") as file:

            def file_operation() -> None:
                s3_info = self._get_upload_s3_info()
                s3_info["s3_client"].put_object(Bucket=bucket_name, Key=key, Body=file)

            s3_info = self._get_upload_s3_info()
            s3_exceptions = s3_info["s3_client"].exceptions

            wrapped_file_operation = self.exponential_backoff_retry(
                file_operation,
                exceptions_to_raise=[s3_exceptions.NoSuchBucket],
            )

            wrapped_file_operation()

            if callback:
                callback(os.path.getsize(file_path))

    def _s3_upload_file(
        self,
        bucket_name: str,
        file_path: str,
        key: str,
        callback: Optional[Callable[[int], None]] = None,
        multipart_threshold=5 * 1024 * 1024,
    ) -> None:
        file_size = os.path.getsize(file_path)

        if file_size > multipart_threshold:
            self._s3_multipart_upload(bucket_name, file_path, key, callback, chunk_size=multipart_threshold)
        else:
            self._s3_put_object(bucket_name, file_path, key, callback)

    def _upload_file(self, local_filepath: str, progress_bar: tqdm):
        try:
            local_relative_filepath = (
                os.path.relpath(local_filepath, self.local_root_directory_path)
                if local_filepath != self.local_root_directory_path
                else os.path.basename(local_filepath)
            )
            s3_info = self._get_upload_s3_info()
            s3_path = s3_info["s3_prefix"] + "/" + local_relative_filepath
            if Util.is_windows():
                s3_path = FileUtil.windows_to_unix_path(s3_path)

            self._s3_upload_file(
                bucket_name=s3_info["s3_bucket"], file_path=local_filepath, key=s3_path, callback=progress_bar.update
            )
        except BaseException as exc:  # pylint: disable=broad-except
            progress_bar.write(f"Failed to upload {local_filepath}.")
            logging.error("Failed to upload %s.", local_filepath)
            logging.exception(exc)

    def _get_s3_object_list(self) -> list[ObjectTypeDef]:
        s3_info = self._get_download_s3_info()
        response = s3_info["s3_client"].list_objects_v2(Bucket=s3_info["s3_bucket"], Prefix=s3_info["s3_prefix"])

        if "Contents" not in response:
            return []

        s3_objects_list: list[ObjectTypeDef] = response["Contents"]

        while "NextContinuationToken" in response:
            response = s3_info["s3_client"].list_objects_v2(
                Bucket=s3_info["s3_bucket"],
                Prefix=s3_info["s3_prefix"],
                ContinuationToken=response["NextContinuationToken"],
            )
            s3_objects_list.extend(response["Contents"])

        return s3_objects_list

    def _get_download_s3_info(self) -> S3Info:
        if self.download_s3_info and self.download_s3_info["expires_at"] > time.time():
            return self.download_s3_info

        expires_at = time.time() + SECONDS_PER_MINUTE * S3_TIMEOUT_MINUTES
        s3_client, s3_bucket, s3_prefix = self.fovus_api_adapter.get_temporary_s3_download_credentials()
        s3_prefix += self.job_id

        self.download_s3_info = {
            "s3_client": s3_client,
            "s3_bucket": s3_bucket,
            "s3_prefix": s3_prefix,
            "expires_at": expires_at,
        }
        return self.download_s3_info

    def _get_upload_s3_info(self) -> S3Info:
        if self.upload_s3_info and self.upload_s3_info["expires_at"] > time.time():
            return self.upload_s3_info

        expires_at = time.time() + SECONDS_PER_MINUTE * S3_TIMEOUT_MINUTES
        s3_client, s3_bucket, s3_prefix = self.fovus_api_adapter.get_temporary_s3_upload_credentials()

        if self.upload_type == UploadType.UPLOAD:
            s3_prefix += self.job_id
        elif self.upload_type == UploadType.UPLOAD_TO_STORAGE:
            s3_prefix = "files"

            if isinstance(self.fovus_path, str):
                s3_prefix += "/" + self.fovus_path.strip("/").strip("\\")

            if isinstance(self.local_root_directory_path, str) and os.path.isdir(self.local_root_directory_path):
                basename = os.path.basename(self.local_root_directory_path.strip("/").strip("\\"))
                s3_prefix += "/" + basename

        self.upload_s3_info = {
            "s3_client": s3_client,
            "s3_bucket": s3_bucket,
            "s3_prefix": s3_prefix,
            "expires_at": expires_at,
        }
        return self.upload_s3_info

    def _s3_download_multipart_part(self, bucket_name: str, key: str, start_byte: int, end_byte: int) -> bytes:
        def file_operation() -> bytes:
            range_header = f"bytes={start_byte}-{end_byte}"

            s3_info = self._get_download_s3_info()
            response = s3_info["s3_client"].get_object(Bucket=bucket_name, Key=key, Range=range_header)
            part_data = response["Body"].read()

            return part_data

        s3_info = self._get_download_s3_info()
        s3_exceptions = s3_info["s3_client"].exceptions

        wrapped_file_operation = self.exponential_backoff_retry(
            file_operation,
            exceptions_to_raise=[s3_exceptions.NoSuchKey, s3_exceptions.NoSuchBucket],
        )

        return wrapped_file_operation()

    def _s3_download_file(
        self,
        bucket_name: str,
        key: str,
        local_path: str,
        file_size: int,
        part_size: int = 1024 * 512,
        callback: Optional[Callable[[int], None]] = None,
    ) -> None:
        total_parts = (file_size + part_size - 1) // part_size

        download_path = local_path + DOWNLOAD_FILE_EXTENSION

        file_lock = Lock()

        file: BufferedWriter
        with open(download_path, "wb") as file:

            def download_part_operation(part_number: int) -> tuple[int, bytes]:
                start_byte = part_number * part_size
                end_byte = min((part_number + 1) * part_size - 1, file_size)

                part_data = self._s3_download_multipart_part(bucket_name, key, start_byte, end_byte)

                if callback:
                    callback(len(part_data))

                return start_byte, part_data

            executor: concurrent.futures.ThreadPoolExecutor
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                for start_byte, part_data in executor.map(download_part_operation, range(total_parts)):
                    with file_lock:
                        file.seek(start_byte)
                        file.write(part_data)

        os.rename(download_path, local_path)

    def _download_file(self, s3_object: ObjectTypeDef, progress_bar: tqdm):
        try:
            if not AwsUtil.s3_object_is_directory(s3_object):
                s3_info = self._get_download_s3_info()
                local_filepath = self._get_local_filepath(s3_object, s3_info["s3_prefix"])

                if FileUtil.include_exclude_allows_path(
                    os.path.relpath(local_filepath, self.local_root_directory_path),
                    self.cli_dict[INCLUDE_OUTPUT],
                    self.cli_dict[EXCLUDE_OUTPUT],
                ) and self._should_download_file(local_filepath, s3_object):
                    os.makedirs(os.path.dirname(local_filepath), exist_ok=True)

                    s3_info = self._get_download_s3_info()
                    refreshed_s3_object = s3_info["s3_client"].get_object(
                        Bucket=s3_info["s3_bucket"], Key=s3_object["Key"]
                    )
                    s3_object["ETag"] = refreshed_s3_object["ETag"]

                    self._s3_download_file(
                        bucket_name=s3_info["s3_bucket"],
                        key=s3_object["Key"],
                        local_path=local_filepath,
                        file_size=s3_object["Size"],
                        callback=progress_bar.update,
                    )

                    self._cache_file_data(local_filepath, s3_object)
                else:
                    progress_bar.update(s3_object["Size"])
        except BaseException as exc:  # pylint: disable=broad-except
            progress_bar.write(f"Failed to download {s3_object['Key']}.")
            logging.error("Failed to download %s.", s3_object["Key"])
            logging.exception(exc)

    def _load_cached_file_data(self):
        cached_file_data_filepath = os.path.join(
            self.local_root_directory_path, FOVUS_JOB_INFO_FOLDER, "cached_file_data.json"
        )
        if not os.path.isfile(cached_file_data_filepath):
            return {}

        try:
            with FileUtil.open(cached_file_data_filepath, "r") as cached_file_data_file:
                return json.load(cached_file_data_file)
        except Exception as exc:  # pylint: disable=broad-except
            logging.error("Failed to load cached file data.")
            logging.exception(exc)
            return {}

    def _cache_file_data(self, local_filepath: str, s3_object: ObjectTypeDef):
        self.cached_file_data[s3_object["Key"]] = self._retrieve_file_data(local_filepath, s3_object)
        self._save_cached_file_data()

    def _save_cached_file_data(self):
        cached_file_data_filepath = os.path.join(
            self.local_root_directory_path, FOVUS_JOB_INFO_FOLDER, "cached_file_data.json"
        )
        os.makedirs(os.path.dirname(cached_file_data_filepath), exist_ok=True)

        with FileUtil.open(cached_file_data_filepath, "w") as cached_file_data_file:
            json.dump(self.cached_file_data.copy(), cached_file_data_file)

    def _retrieve_file_data(self, local_file_path: str, s3_object: ObjectTypeDef) -> CachedFileData:
        last_modified = os.path.getmtime(local_file_path)

        return {
            "last_modified": last_modified,
            "s3_hash": s3_object["ETag"],
        }

    def _should_download_file(self, local_file_path: str, s3_object: ObjectTypeDef) -> bool:
        if not FileUtil.file_exists(local_file_path):
            return True

        cached_file_data = self.cached_file_data.get(s3_object["Key"])

        if not cached_file_data or cached_file_data["last_modified"] != os.path.getmtime(local_file_path):
            return not FileUtil.compare_s3_hash(local_file_path, s3_object, self._cache_file_data)

        return cached_file_data["s3_hash"] != s3_object["ETag"]

    def _get_local_filepath(self, s3_object, s3_prefix):
        return os.path.join(
            self.local_root_directory_path, AwsUtil.get_s3_object_key_without_prefix(s3_object, s3_prefix)
        )
