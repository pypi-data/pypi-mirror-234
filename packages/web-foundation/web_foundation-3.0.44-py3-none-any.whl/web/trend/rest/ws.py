from dataclasses import dataclass, field
from typing import Iterable

from sanic.server.websockets.impl import WebsocketImplProtocol
from websockets.typing import Data

from web.kernel.types import RtMessage, RtWriter, RtReadCallback


@dataclass
class WsRtMessage(RtMessage):
    msg: Data | Iterable[Data] = field(default="")

    def prepare(self, *args, **kwargs) -> str | bytes:
        return self.msg

    @classmethod
    def ping_message(cls):
        return ""


class WsWriter(RtWriter[WsRtMessage]):
    """
    Resolve WebSocket communication
    """
    read_callback: RtReadCallback
    obj: WebsocketImplProtocol

    def __init__(self, obj: WebsocketImplProtocol,
                 read_callback: RtReadCallback = None):
        super().__init__(obj)
        self.read_callback = read_callback

    async def write(self, message: Data | Iterable[Data]) -> None:
        await self.obj.send(message)

    async def freeze(self, ping_enable: bool = False, ping_timeout: int = 5):
        self.obj.connection_lost_waiter.add_done_callback(lambda s: self.on_close())
        if self.read_callback:
            async for msg in self.obj:
                await self.read_callback(self, msg)
        else:
            await self.obj.wait_for_connection_lost()

    async def close(self, code: int = 1000, reason: str = ""):
        await self.obj.close(code=code, reason=reason)
