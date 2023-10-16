import abc
import asyncio
import websockets

from typing import Any, List, Union, Callable, Coroutine, Optional
from contextlib import asynccontextmanager
from amiyabot.typeIndexes import T_BotHandlerFactory
from amiyabot.builtin.message import Event, EventList, Message, MessageCallback
from amiyabot.builtin.messageChain import Chain
from amiyabot.log import LoggerManager

HANDLER_TYPE = Callable[[str, dict], Coroutine[Any, Any, None]]
PACKAGE_RESULT = Union[Message, Event, EventList]


class BotAdapterProtocol:
    def __init__(self, appid: str, token: str):
        self.appid = appid
        self.token = token
        self.alive = False
        self.keep_run = True

        # 适配器实例连接信息
        self.host: Optional[str] = None
        self.ws_port: Optional[int] = None
        self.http_port: Optional[int] = None
        self.session: Optional[str] = None

        self.log = LoggerManager(self.__str__())
        self.bot: Optional[T_BotHandlerFactory] = None

    def __str__(self):
        return 'Adapter'

    def set_alive(self, status: bool):
        self.alive = status

    async def send_message(
        self,
        chain: Chain,
        user_id: str = '',
        channel_id: str = '',
        direct_src_guild_id: str = '',
    ):
        chain = await self.build_active_message_chain(chain, user_id, channel_id, direct_src_guild_id)

        async with self.bot.processing_context(chain):
            callback = await self.send_chain_message(chain, is_sync=True)

        return callback

    @asynccontextmanager
    async def get_websocket_connection(self, mark: str, url: str):
        async with self.log.catch(
            f'websocket connection({mark}) error:',
            ignore=[
                asyncio.CancelledError,
                websockets.ConnectionClosedError,
                websockets.ConnectionClosedOK,
                ManualCloseException,
            ],
        ):
            self.set_alive(True)
            async with websockets.connect(url) as websocket:
                yield websocket

        self.set_alive(False)
        self.log.info(f'websocket connection({mark}) closed.')

    @abc.abstractmethod
    async def close(self):
        """
        关闭此实例
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def connect(self, private: bool, handler: HANDLER_TYPE):
        """
        连接至服务并启动实例

        :param private: 是否私域
        :param handler: 消息处理方法
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def send_chain_message(self, chain: Chain, is_sync: bool = False) -> List[MessageCallback]:
        """
        使用 Chain 对象发送消息

        :param chain:   Chain 对象
        :param is_sync: 是否同步发送消息
        :return:        如果是同步发送，则返回 MessageCallback 列表
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def build_active_message_chain(
        self, chain: Chain, user_id: str, channel_id: str, direct_src_guild_id: str
    ) -> Chain:
        """
        构建主动消息的 Chain 对象

        :param chain:               消息 Chain 对象
        :param user_id:             用户 ID
        :param channel_id:          子频道 ID
        :param direct_src_guild_id: 来源的频道 ID（私信时需要）
        :return:                    Chain 对象
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def package_message(self, event: str, message: dict) -> PACKAGE_RESULT:
        """
        预处理并封装消息对象

        :param event:   事件名
        :param message: 消息对象
        :return:        封装结果：Message、Event、EventList
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def recall_message(self, message_id: Union[str, int], target_id: Optional[Union[str, int]] = None):
        """
        撤回消息

        :param message_id: 消息 ID
        :param target_id:  目标 ID
        """
        raise NotImplementedError


class ManualCloseException(Exception):
    ...
