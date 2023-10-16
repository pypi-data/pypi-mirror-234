from typing import Optional, Type

from pydantic_settings import SettingsConfigDict

try:
    from aiosmtplib import SMTP
except ImportError:  # pragma: no cover
    SMTP = None

from pydantic import SecretStr

from accentnotifications.types import Email

from .base import BaseBackend, BaseNotification, BaseResponse


class SmtpResponse(BaseResponse):
    success: bool


class SmtpNotification(BaseNotification):
    model_config = SettingsConfigDict(
        arbitrary_types_allowed=True,
        env_prefix="notifications_smtp_",
        # json_encoders={Message: lambda v: v.as_string()}
    )

    host: str
    port: int
    username: Optional[SecretStr] = None
    password: Optional[SecretStr] = None
    use_tls: bool = False
    starttls: bool = False
    timeout: Optional[int] = None
    fail_silently: bool = False
    email: Email
    response: Optional[SmtpResponse] = None

    @property
    def backend(self) -> Type["SmtpBackend"]:
        return SmtpBackend


class SmtpBackend(BaseBackend):
    options: SmtpNotification
    connection = None

    def __init__(self, options: BaseNotification) -> None:
        super().__init__(options)

        if not SMTP:  # pragma: no cover
            raise ModuleNotFoundError("python library aiosmtplib required")

    async def open(self):
        params = {
            "hostname": self.options.host,
            "port": self.options.port,
            "use_tls": self.options.use_tls and not self.options.starttls,
        }
        if self.options.timeout is not None:
            params["timeout"] = self.options.timeout

        try:
            self.connection = SMTP(**params)

            await self.connection.connect()

            if self.options.starttls:
                await self.connection.starttls()

            if self.options.username and self.options.password:
                await self.connection.login(
                    self.options.username.get_secret_value(),
                    self.options.password.get_secret_value(),
                )

            return True
        except OSError:
            if not self.options.fail_silently:
                raise

    async def close(self):
        if self.connection is None:  # pragma: no cover
            return

        try:
            await self.connection.quit()
        except Exception:
            if self.options.fail_silently:
                return
            raise
        finally:
            self.connection = None

    async def send(self) -> bool:
        try:
            await self.connection.send_message(self.options.email)
        except Exception:
            self.options.response = SmtpResponse(success=False)
            if self.options.fail_silently:
                return False
            raise

        self.options.response = SmtpResponse(success=True)
        return True
