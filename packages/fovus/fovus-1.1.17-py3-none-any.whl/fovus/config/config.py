# Prod
import copy
from http import HTTPStatus

from fovus.constants.cli_constants import (
    API_DOMAIN_NAME,
    AUTH_WS_API_URL,
    CLIENT_ID,
    DOMAIN_NAME,
    USER_POOL_ID,
)
from fovus.exception.user_exception import UserException


class Config:
    __conf = {
        CLIENT_ID: "353su1970rpnfcigu09j9078c0",
        API_DOMAIN_NAME: "https://api.fovus.co",
        USER_POOL_ID: "us-east-1_fVH5TjPp5",
        DOMAIN_NAME: "fovus.co",
        AUTH_WS_API_URL: "wss://websocket.fovus.co/cli-auth/",
    }
    __setters = [API_DOMAIN_NAME, DOMAIN_NAME, CLIENT_ID, USER_POOL_ID]

    @staticmethod
    def get(key):
        return Config.__conf[key]

    @staticmethod
    def set(key, value):
        if key in Config.__setters:
            Config.__conf[key] = value
        else:
            raise UserException(HTTPStatus.INTERNAL_SERVER_ERROR, Config.__name__, f"Key '{key}' is not in Config.")

    @staticmethod
    def editable_configs():
        return copy.copy(Config.__setters)
