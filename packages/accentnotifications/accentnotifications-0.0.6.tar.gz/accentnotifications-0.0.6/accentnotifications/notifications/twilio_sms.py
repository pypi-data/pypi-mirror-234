from pydantic_settings import SettingsConfigDict

try:
    from aiohttp import BasicAuth, ClientSession
except ImportError:  # pragma: no cover
    BasicAuth = None
    ClientSession = None

from typing import Optional, Type

from pydantic import SecretStr, constr

from .base import BaseBackend, BaseNotification, BaseResponse

KeyTypeStr = constr(pattern=r"^\+?[1-9]\d{1,14}$")


class TwilioSMSResponse(BaseResponse):
    success: bool
    status_code: int = None
    request_id: str = None
    message: str = None


class TwilioSMSNotification(BaseNotification):
    model_config = SettingsConfigDict(
        arbitrary_types_allowed=True,
        env_prefix="notifications_twilio_sms_",
    )

    from_number: str
    to_number: KeyTypeStr
    body: str
    base_url: str
    account_sid: SecretStr
    auth_token: SecretStr
    fail_silently: bool = False
    response: Optional[TwilioSMSResponse] = None

    @property
    def backend(self) -> Type["TwilioSMSBackend"]:
        return TwilioSMSBackend


class TwilioSMSBackend(BaseBackend):
    options: TwilioSMSNotification
    connection = None

    def __init__(self, options: TwilioSMSNotification) -> None:
        super().__init__(options)

        if not ClientSession:  # pragma: no cover
            raise ModuleNotFoundError("python library aiohttp required")

    async def send(self) -> bool:
        auth = BasicAuth(
            login=self.options.account_sid.get_secret_value(),
            password=self.options.auth_token.get_secret_value(),
        )
        async with ClientSession(auth=auth) as connection:
            try:
                data = {
                    "From": self.options.from_number,
                    "To": self.options.to_number,
                    "Body": self.options.body,
                }
                post_data = await connection.post(
                    f"{self.options.base_url}/2010-04-01/Accounts/{self.options.account_sid}/Messages.json",
                    data=data,
                )
                body = await post_data.json()
                # Twilio uses 201 for success
                if post_data.status != 201:
                    self.options.response = TwilioSMSResponse(
                        status_code=post_data.status,
                        success=False,
                        request_id=post_data.headers["Twilio-Request-Id"],
                        message=body["message"],
                    )
                    return False
                else:
                    self.options.response = TwilioSMSResponse(
                        status_code=post_data.status,
                        success=True,
                        request_id=post_data.headers["Twilio-Request-Id"],
                        message=body["message"],
                    )
                    return True
            except Exception:
                self.options.response = TwilioSMSResponse(success=False)
                if self.options.fail_silently:
                    return False
                raise
