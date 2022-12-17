import asyncio
import io
import json
import logging
import os
import random
import subprocess
import time
from typing import Union, List, IO

import ffmpeg
from aiohttp import ClientWebSocketResponse, ClientSession, WSMsgType
from goto import with_goto
from khl import Bot, Guild, User, Requestable, PublicVoiceChannel, Gateway
from khl.util import unpack_id


class VoiceChannelConnection(Requestable):
    me: User

    _gateway_url: str
    session: ClientSession
    client: ClientWebSocketResponse

    rtp_ip: str
    rtp_port: int
    rtcp_port: int

    _get_router_rtp_capabilities: bool = False
    _join: bool = False
    _create_plain_transport: bool = False
    _produce: bool = False

    _process = None
    _stdin = None

    streaming: bool = False

    next: bytes = None

    def __init__(self, bot: Bot, gateway_url: str):
        self._bot = bot
        self.gate = bot.client.gate
        self._gateway_url = gateway_url
        self.session = ClientSession()

    async def connect(self):
        self.me = await self._bot.client.fetch_me()
        self.client = await self.session.ws_connect(self._gateway_url)
        await self.client.send_json(
            {'request': True, 'id': random_id(), 'method': 'getRouterRtpCapabilities', 'data': dict()})
        await asyncio.gather(self._heartbeat(), self._receive_pkg(), self._prepare_stream(), self._play())

    async def _heartbeat(self):
        last_heartbeat = 0.0
        while True:
            await asyncio.sleep(0.1)
            now = time.time()
            if now - last_heartbeat >= 30:
                await self.client.ping()
                last_heartbeat = now

    async def _receive_pkg(self):
        async for msg in self.client:
            if msg.type == WSMsgType.TEXT:
                await self._consume_pkg(json.loads(msg.data))
            elif msg.type == WSMsgType.ERROR:
                logging.error('Error occurred')
                break
            else:
                return

    async def _consume_pkg(self, data):
        logging.debug(f'receiving data: {data}')
        if not self._get_router_rtp_capabilities:
            await self._consume_get_router_rtp_capabilities(data)
        elif not self._join:
            await self._consume_join(data)
        elif not self._create_plain_transport:
            await self._consume_create_plain_transport(data)
        elif not self._produce:
            await self._consume_produce(data)
        else:
            await self._consume(data)

    async def _consume_get_router_rtp_capabilities(self, data):
        await self.client.send_json({'data': {'displayName': ''}, 'id': random_id(), 'method': 'join', 'request': True})
        self._get_router_rtp_capabilities = True

    async def _consume_join(self, data):
        await self.client.send_json({'data': {'comedia': True, 'rtcpMux': False, 'type': 'plain'},
                                     'id': random_id(),
                                     'method': 'createPlainTransport',
                                     'request': True})
        self._join = True

    async def _consume_create_plain_transport(self, data):
        data = data['data']
        self.rtp_ip = data['ip']
        self.rtp_port = data['port']
        self.rtcp_port = data['rtcpPort']
        await self.client.send_json({
            'data': {
                'appData': dict(),
                'kind': 'audio',
                'peerId': '',
                'rtpParameters': {
                    'codecs': [
                        {
                            'channels': 2,
                            'clockRate': 48000,
                            'mimeType': 'audio/opus',
                            'parameters': {
                                'sprop-stereo': 1
                            },
                            'payloadType': 100
                        },
                    ],
                    'encodings': [
                        {
                            'ssrc': 1357
                        }
                    ]
                },
                'transportId': data['id']
            },
            'id': random_id(),
            'method': 'produce',
            'request': True
        })
        self._create_plain_transport = True

    async def _prepare_stream(self):
        while True:
            await asyncio.sleep(0.1)
            if self._produce:
                break
        self._process = ffmpeg.input('pipe:', re=None, loglevel='level+info', nostats=None).output(
            f'[select=a:f=rtp:ssrc=1357:payload_type=100]rtp://{self.rtp_ip}:{self.rtp_port}?rtcpport={self.rtcp_port}',
            map='0:a:0', acodec='libopus', ab='128k', **{'filter:a': 'volume=0.5'}, ac=2, ar=48000, f='tee') \
            .overwrite_output() \
            .run_async(pipe_stdin=True)

    async def _play(self):
        empty_bytes = bytes(256)
        while True:
            fk = False
            while True:
                if self.next is not None:
                    file_size = len(self.next)
                    music = self.next
                    self.next = None
                    for i in range(file_size // 256 if file_size % 256 == 0 else (file_size // 256) + 1):
                        self._process.stdin.write(music[i * 256:min((i + 1) * 256, file_size)])
                        if self.next is not None:
                            fk = True
                            break
                        elif not self.streaming:
                            break
                        await asyncio.sleep(0.0019)
                    if fk:
                        break
                else:
                    if self._process is not None:
                        self._process.stdin.write(empty_bytes)
                    await asyncio.sleep(0.002)

    async def _consume_produce(self, data):
        logging.info(f'ssrc=1357 ffmpeg rtp url: rtp://{self.rtp_ip}:{self.rtp_port}?rtcpport={self.rtcp_port}')
        self._produce = True

    async def _consume(self, data):
        if 'notification' in data and 'method' in data and data['method'] == 'disconnect':
            logging.debug('The connection had been disconnected', data)
            await self.client.close()
        elif 'notification' in data and 'method' in data and data['method'] == 'networkStat' and self.me.id in \
                data['data'][
                    'stat']:
            pass
        else:
            logging.debug(data)

    async def stream(self, file: Union[str, bytes, IO]):
        self.streaming = True
        if isinstance(file, str):
            with open(file, 'rb') as audio:
                self.next = audio.read()
        elif isinstance(file, bytes):
            self.next = file
        elif isinstance(file, IO):
            self.next = file.read()

        # self._stdin.write(f'-i {file}')
        ...

    async def stop_stream(self):
        # TODO
        # if self.streaming:
        #     self._process.communicate('q')
        self.streaming = False
        ...

    async def _create_popon(self,
                            output,
                            cmd='ffmpeg',
                            pipe_stdin=False,
                            pipe_stdout=False,
                            pipe_stderr=False,
                            quiet=False,
                            overwrite_output=False) -> subprocess.Popen:
        args = output.compile(cmd, overwrite_output=overwrite_output)
        stdin_stream = subprocess.PIPE if pipe_stdin else None
        stdout_stream = subprocess.PIPE if pipe_stdout or quiet else None
        stderr_stream = subprocess.PIPE if pipe_stderr or quiet else None
        return subprocess.Popen(
            args, stdin=stdin_stream, stdout=stdout_stream, stderr=stderr_stream, encoding='utf-8'
        )


async def fetch_voice_gateway(bot: Bot, channel: Union[PublicVoiceChannel, str]) -> str:
    return (await bot.client.gate.request('GET', 'gateway/voice', data={'channel_id': unpack_id(channel)}))[
        'gateway_url']


async def connect(bot: Bot, channel: Union[PublicVoiceChannel, str]) -> VoiceChannelConnection:
    gateway_url = await fetch_voice_gateway(bot, channel)
    connection = VoiceChannelConnection(bot=bot, gateway_url=gateway_url)
    return connection


def random_id() -> int:
    return random.randint(1000000, 9999999)
