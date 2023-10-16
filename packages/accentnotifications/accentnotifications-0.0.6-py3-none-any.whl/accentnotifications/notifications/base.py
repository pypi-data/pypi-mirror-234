from typing import Optional, Type

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class BaseResponse(BaseModel):
    success: bool


class BaseNotification(BaseSettings):
    response: Optional[BaseResponse] = None

    @property
    def backend(self) -> Type["BaseBackend"]:
        raise NotImplementedError()


class BaseBackend:
    options: BaseNotification

    def __init__(self, options: BaseNotification) -> None:
        self.options = options

    async def __aenter__(self):
        try:
            await self.open()
        except Exception:
            await self.close()
            raise
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def open(self):
        pass

    async def close(self):
        pass

    async def send(self) -> bool:
        raise NotImplementedError()
