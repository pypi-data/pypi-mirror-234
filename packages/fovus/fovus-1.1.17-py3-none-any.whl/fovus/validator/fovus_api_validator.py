import datetime
import json
import os
from http import HTTPStatus

import jsonschema

from fovus.constants.cli_constants import (
    JOB_MAX_CLUSTER_SIZE_VCPU,
    MAX_GPU,
    MAX_VCPU,
    MIN_GPU,
    MIN_VCPU,
    PARALLELISM_OPTIMIZATION,
    SCALABLE_PARALLELISM,
    SCHEDULED_AT,
)
from fovus.constants.fovus_api_constants import (
    PAYLOAD_CONSTRAINTS,
    PAYLOAD_JOB_CONSTRAINTS,
    PAYLOAD_TASK_CONSTRAINTS,
    PAYLOAD_TIME_COST_PRIORITY_RATIO,
    ApiMethod,
)
from fovus.exception.user_exception import UserException
from fovus.root_config import ROOT_DIR
from fovus.util.file_util import FileUtil

SCHEMA_PATH_PREFIX = "schema/"
SCHEMA_PATH_SUFFIX = "_schema.json"


class FovusApiValidator:  # pylint: disable=too-few-public-methods
    def __init__(self, payload, api_method: ApiMethod):
        self.payload = payload
        self.api_method = api_method.value.replace("-", "_")

    def validate(self):
        self._validate_schema()
        self._validate_time_cost_to_priority_ratio()
        self._validate_parallelism_optimization_allowed_value()
        self._validate_job_max_cluster_size()
        self._validate_min_max_vcpu()
        self._validate_min_max_gpu()
        self._validate_scheduled_at()

    def _validate_schema(self):
        schema_path = os.path.abspath(
            os.path.join(ROOT_DIR, SCHEMA_PATH_PREFIX, "".join((self.api_method.lower(), SCHEMA_PATH_SUFFIX)))
        )
        with FileUtil.open(schema_path) as schema_file:
            schema = json.load(schema_file)
            try:
                jsonschema.validate(self.payload, schema)
            except jsonschema.exceptions.ValidationError as exception:
                raise UserException(
                    HTTPStatus.BAD_REQUEST.value, FovusApiValidator.__name__, exception.message
                ) from exception

    def _validate_time_cost_to_priority_ratio(self):
        time_cost_to_priority_ratio_exception = UserException(
            HTTPStatus.BAD_REQUEST,
            FovusApiValidator.__name__,
            'timeToCostPriorityRatio must be of the form "time/cost" where 0 <= time <= 1, '
            + "0 <= cost <= 1, and time + cost = 1",
        )

        time, cost = self.payload[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS][PAYLOAD_TIME_COST_PRIORITY_RATIO].split(
            "/"
        )
        time, cost = float(time), float(cost)
        for value in (time, cost):
            if value < 0 or value > 1:
                raise time_cost_to_priority_ratio_exception
        if time + cost != 1:
            raise time_cost_to_priority_ratio_exception

    def _validate_parallelism_optimization_allowed_value(self):
        if (
            self.payload[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][PARALLELISM_OPTIMIZATION]
            and not self.payload[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][SCALABLE_PARALLELISM]
        ):
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                FovusApiValidator.__name__,
                "parallelismOptimization is only allowed to be set to true when scalableParallelism is set to true",
            )

    def _validate_job_max_cluster_size(self):
        job_constraints = self.payload[PAYLOAD_CONSTRAINTS][PAYLOAD_JOB_CONSTRAINTS]
        if hasattr(job_constraints, JOB_MAX_CLUSTER_SIZE_VCPU) and job_constraints[JOB_MAX_CLUSTER_SIZE_VCPU] < 0:
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                FovusApiValidator.__name__,
                "jobMaxClusterSizevCpu must be >= 0",
            )

    def _validate_min_max_vcpu(self):
        if (
            self.payload[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][MIN_VCPU]
            > self.payload[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][MAX_VCPU]
        ):
            raise UserException(
                HTTPStatus.BAD_REQUEST, FovusApiValidator.__name__, "minvCpu must be less than or equal to maxvCpu"
            )

    def _validate_min_max_gpu(self):
        if (
            self.payload[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][MIN_GPU]
            > self.payload[PAYLOAD_CONSTRAINTS][PAYLOAD_TASK_CONSTRAINTS][MAX_GPU]
        ):
            raise UserException(
                HTTPStatus.BAD_REQUEST, FovusApiValidator.__name__, "minGpu must be less than or equal to maxGpu"
            )

    def _validate_scheduled_at(self):
        if "SCHEDULED_AT" in self.payload and self.payload[SCHEDULED_AT] < datetime.datetime.now().isoformat():
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                self.__class__.__name__,
                f"Invalid ISO 8601-formatted value of {self.payload[SCHEDULED_AT]} for '{SCHEDULED_AT}'. "
                "Scheduled job must be in the future.",
            )
