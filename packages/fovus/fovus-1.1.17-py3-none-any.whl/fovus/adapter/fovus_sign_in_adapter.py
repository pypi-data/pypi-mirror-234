import asyncio
import json
import logging
import platform
import webbrowser
from http import HTTPStatus

import boto3
import pkg_resources  # type: ignore
from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from typing_extensions import Union
from websockets.client import WebSocketClientProtocol, connect

from fovus.adapter.fovus_api_adapter import FovusApiAdapter
from fovus.adapter.fovus_cognito_adapter import (
    CognitoTokens,
    DeviceInformation,
    FovusCognitoAdapter,
)
from fovus.config.config import Config
from fovus.constants.cli_constants import AUTH_WS_API_URL, CLIENT_ID, USER_POOL_ID
from fovus.exception.user_exception import UserException


class FovusSignInAdapter:
    user_pool_id: str
    client_id: str
    user_pool_region: str
    cognito_client: CognitoIdentityProviderClient
    device_information: Union[DeviceInformation, None] = None

    def __init__(self) -> None:
        self.user_pool_id = Config.get(USER_POOL_ID)
        self.client_id = Config.get(CLIENT_ID)
        self.user_pool_region = self.user_pool_id.split("_", maxsplit=1)[0]

        self.cognito_client: CognitoIdentityProviderClient = boto3.client(
            "cognito-idp", region_name=self.user_pool_region
        )

    def sign_in_concurrent(self) -> None:
        asyncio.run(self.sign_in())

    async def sign_in(self) -> None:
        url = Config.get(AUTH_WS_API_URL)

        websocket: WebSocketClientProtocol
        async with connect(url) as websocket:
            await websocket.send(json.dumps({"action": "GET_SIGN_IN_URL"}))
            cognito_challenge: asyncio.Future = asyncio.Future()
            connection_id: Union[str, None] = None
            username: Union[str, None] = None

            async for message in websocket:
                res = json.loads(message)
                action = res["action"]

                if action == "GET_SIGN_IN_URL_RESPONSE":
                    connection_id = self._get_sign_in_url_response(res)

                elif action == "IS_VALID":
                    username = self._is_valid(res, connection_id, cognito_challenge)

                elif action == "CHALLENGE_ANSWER":
                    await self._challenge_answer(res, cognito_challenge, username)

    def _get_sign_in_url_response(self, res: dict) -> str:
        connection_id = res["connectionId"]
        sign_in_url = res["signInUrl"]

        print(
            "----------------------------------------------------------",
            "  Open the sign in URL to authenticate with Fovus",
            "",
            "  Sign in URL:",
            f"  {sign_in_url}",
            "----------------------------------------------------------",
            sep="\n",
        )

        try:
            webbrowser.open(sign_in_url)
        except webbrowser.Error:
            logging.warning("Unable to open sign in URL in browser.")

        return connection_id

    def _is_valid(self, res: dict, connection_id: Union[str, None], cognito_challenge: asyncio.Future) -> str:
        if not res["isValid"] or connection_id is None:
            raise UserException(HTTPStatus.BAD_REQUEST, self.__class__.__name__, "Login failed")

        print("Logging in...")

        try:
            fovus_cognito_adapter = FovusCognitoAdapter()
            fovus_cognito_adapter.sign_out()
        except UserException:
            pass

        username = res["username"]

        try:
            self.device_information = FovusCognitoAdapter.load_device_information()
        except UserException:
            pass

        initiate_auth_response = self.cognito_client.initiate_auth(
            AuthFlow="CUSTOM_AUTH",
            AuthParameters=self._add_device_key({"USERNAME": username}),
            ClientId=self.client_id,
        )

        respond_to_auth_challenge_response = self.cognito_client.respond_to_auth_challenge(
            ChallengeName="CUSTOM_CHALLENGE",
            ChallengeResponses=self._add_device_key({"USERNAME": username, "ANSWER": "none"}),
            ClientId=self.client_id,
            Session=initiate_auth_response["Session"],
            ClientMetadata={
                "connectionId": connection_id,
            },
        )

        cognito_challenge.set_result(respond_to_auth_challenge_response)

        return username

    # pylint: disable=too-many-locals
    async def _challenge_answer(self, res: dict, cognito_challenge: asyncio.Future, username: Union[str, None]) -> None:
        if username is None:
            raise UserException(HTTPStatus.BAD_REQUEST, self.__class__.__name__, "Login failed")

        challenge_answer = res["challengeAnswer"]

        cognito_challenge_response = await cognito_challenge

        if cognito_challenge_response["ChallengeName"] == "CUSTOM_CHALLENGE":
            response = self.cognito_client.respond_to_auth_challenge(
                ChallengeName="CUSTOM_CHALLENGE",
                ChallengeResponses=self._add_device_key({"ANSWER": challenge_answer, "USERNAME": username}),
                ClientId=self.client_id,
                Session=cognito_challenge_response["Session"],
            )

            if "ChallengeName" in response and response["ChallengeName"] == "DEVICE_SRP_AUTH":
                if self.device_information is None:
                    raise UserException(
                        HTTPStatus.BAD_REQUEST,
                        self.__class__.__name__,
                        "Device information is not found.",
                    )

                response = FovusCognitoAdapter.respond_to_device_srp_challenge(
                    response,
                    self.device_information,
                    self.cognito_client,
                    self.client_id,
                    username,
                    self.user_pool_region,
                    self.user_pool_region,
                )

            id_token = response["AuthenticationResult"]["IdToken"]
            access_token = response["AuthenticationResult"]["AccessToken"]
            refresh_token = response["AuthenticationResult"]["RefreshToken"]

            if "NewDeviceMetadata" in response["AuthenticationResult"]:
                device_key: str = response["AuthenticationResult"]["NewDeviceMetadata"]["DeviceKey"]
                device_group_key: str = response["AuthenticationResult"]["NewDeviceMetadata"]["DeviceGroupKey"]

                salt, verifier, device_password = FovusCognitoAdapter.generate_device_secrets(
                    device_key, device_group_key
                )

                current_fovus_version = pkg_resources.get_distribution("fovus").version
                device_name = f"Fovus CLI@{current_fovus_version}-{platform.platform()}"

                self.cognito_client.confirm_device(
                    AccessToken=access_token,
                    DeviceKey=device_key,
                    DeviceName=device_name,
                    DeviceSecretVerifierConfig={"PasswordVerifier": verifier, "Salt": salt},
                )

                self.device_information = {
                    "device_name": device_name,
                    "device_key": device_key,
                    "device_group_key": device_group_key,
                    "device_password": device_password,
                    "verifier": verifier,
                    "salt": salt,
                }

                FovusCognitoAdapter.save_device_information(self.device_information)

            cognito_tokens: CognitoTokens = {
                "id_token": id_token,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

            FovusCognitoAdapter.save_credentials(cognito_tokens)

            fovus_cognito_adapter = FovusCognitoAdapter(
                cognito_tokens=cognito_tokens,
                device_information=self.device_information,
            )

            fovus_api_adapter = FovusApiAdapter(fovus_cognito_adapter)
            fovus_api_adapter.print_user_info(title="Login successful")

    def _add_device_key(self, params: dict) -> dict:
        if self.device_information is not None:
            params["DEVICE_KEY"] = self.device_information["device_key"]

        return params
