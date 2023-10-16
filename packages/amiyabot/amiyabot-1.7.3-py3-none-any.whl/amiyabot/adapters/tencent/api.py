import abc
import json
import asyncio

from typing import Optional
from amiyabot.network.httpRequests import http_requests, ResponseException
from amiyabot.adapters import BotAdapterProtocol, HANDLER_TYPE
from amiyabot.log import LoggerManager

from .url import APIConstant, get_url
from .model import GateWay, ConnectionHandler
from .builder import MessageSendRequest

log = LoggerManager('Tencent')


class TencentAPI(BotAdapterProtocol):
    def __init__(self, appid: str, token: str):
        super().__init__(appid, token)

        self.appid = appid
        self.token = token

        self.headers = {'Authorization': f'Bot {appid}.{token}'}

    async def connect(self, private: bool, handler: HANDLER_TYPE):
        log.info(f'requesting appid {self.appid} gateway')

        resp = await self.get_request(APIConstant.gatewayBotURI)

        if not resp:
            if self.keep_run:
                await asyncio.sleep(10)
                asyncio.create_task(self.connect(private, handler))
            return False

        gateway = GateWay(**resp)

        log.info(
            f'appid {self.appid} gateway resp: shards {gateway.shards}, remaining %d/%d'
            % (
                gateway.session_start_limit['remaining'],
                gateway.session_start_limit['total'],
            )
        )

        await self.create_connection(ConnectionHandler(private=private, gateway=gateway, message_handler=handler))

    async def get_request(self, url: str):
        return self.__check_response(await http_requests.get(get_url(url), headers=self.headers))

    async def post_request(self, url: str, payload: Optional[dict] = None, is_form_data: bool = False):
        if is_form_data:
            return self.__check_response(await http_requests.post_form(get_url(url), payload, headers=self.headers))
        return self.__check_response(await http_requests.post(get_url(url), payload, headers=self.headers))

    async def get_me(self):
        return await self.get_request(APIConstant.userMeURI)

    async def get_channel(self, channel_id: str):
        return await self.get_request(APIConstant.channelURI.format(channel_id=channel_id))

    async def get_channel_permissions(self, channel_id: str, user_id: str):
        return await self.get_request(APIConstant.channelPermissionsURI.format(channel_id=channel_id, user_id=user_id))

    async def get_message(self, channel_id: str, message_id: str):
        return await self.get_request(APIConstant.messageURI.format(channel_id=channel_id, message_id=message_id))

    async def post_message(self, guild_id: str, src_guild_id: str, channel_id: str, req: MessageSendRequest):
        if req.direct:
            if not guild_id or not req.data['msg_id']:
                create_direct = await self.post_request(
                    APIConstant.userMeDMURI,
                    {'recipient_id': req.user_id, 'source_guild_id': src_guild_id},
                )
                guild_id = create_direct['guild_id']

            api = APIConstant.dmsURI.format(guild_id=guild_id)
        else:
            api = APIConstant.messagesURI.format(channel_id=channel_id)

        complete = None
        retry_times = 0

        while complete is None and retry_times < 3:
            retry_times += 1
            try:
                complete = await self.post_request(api, req.data, req.upload_image)
            except ResponseException:
                complete = {}

            await asyncio.sleep(0)

        return complete

    async def recall_message(self, message_id: str, target_id: Optional[str] = None):
        await http_requests.request(
            get_url(f'/channels/{target_id}/messages/{message_id}?hidetip=false'),
            method='delete',
            headers=self.headers,
        )

    @abc.abstractmethod
    async def create_connection(self, handler: ConnectionHandler, shards_index: int = 0):
        raise NotImplementedError

    @staticmethod
    def __check_response(response_text: Optional[str]) -> Optional[dict]:
        if response_text is None:
            return None

        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as e:
            raise ResponseException(-1, repr(e)) from e

        if 'code' in data and data['code'] != 200:
            raise ResponseException(**data)

        return data
