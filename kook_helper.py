from typing import Union, List

from khl import Bot, Guild, User, Requestable, PublicVoiceChannel
from khl.util import unpack_id


class Region:

    id: str
    name: str
    crowding: int

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.crowding = kwargs.get('crowding')


class FriendRequest(Requestable):

    id: int
    user: User

    def __init__(self, **kwargs):
        self.gate = kwargs.get('_gate_')
        self.id = kwargs.get('id')
        self.user = kwargs.get('user')

    async def accept(self):
        await self.gate.request('POST', 'friend/handle-request', id=self.id, accept=True)

    async def deny(self):
        await self.gate.request('POST', 'friend/handle-request', id=self.id, accept=False)


async def list_regions(bot: Bot) -> List[Region]:
    region_datas = (await bot.client.gate.request('GET', 'guild/regions')).get('items', list())
    return [Region(**data) for data in region_datas]


async def create_guild(bot: Bot, name: str, icon: str = '', region: Union[str, Region] = 'beijing', template_id: int = 0) -> Guild:
    region = unpack_id(region)
    guild_data = await bot.client.gate.request('POST', 'guild/create', name=name, icon=icon, region=region,
                                               template_id=template_id)
    guild = Guild(_gate_=bot.client.gate, **guild_data)
    await guild.load()
    return guild


async def delete_guild(bot: Bot, guild: Union[Guild, str]):
    guild = unpack_id(guild)
    await bot.client.gate.request('POST', 'guild/delete', guild_id=guild)


async def add_friend(bot: Bot, user: Union[User, str], user_code: str = None, guild: Union[Guild, str] = None):
    params = {}
    if user_code is not None:
        params['user_code'] = user_code
    elif not isinstance(user, User):
        user = await bot.client.fetch_user(user)
        params['user_code'] = f'{user.username}#{user.identify_num}'
    if guild is not None:
        params['from'] = 2
        params['guild_id'] = unpack_id(guild)
    else:
        params['from'] = 0
    await bot.client.gate.request('POST', 'friend/request', data=params)


async def delete_friend(bot: Bot, user: Union[User, id]):
    await bot.client.gate.request('POST', 'friend/request', user_id=unpack_id(user))


async def list_friends(bot: Bot) -> List[User]:
    user_datas = (await bot.client.gate.request('GET', 'friend')).get('friend', list())
    return [User(_gate_=bot.client.gate, **data.get('friend_info')) for data in user_datas]


async def list_friend_requests(bot: Bot) -> List[FriendRequest]:
    user_datas = (await bot.client.gate.request('GET', 'friend')).get('request', list())
    return [FriendRequest(_gate_=bot.client.gate, id=data.get('id'), user=User(_gate_=bot.client.gate, **data.get('friend_info')))
            for data in user_datas]


async def accept_request(bot: Bot, request: Union[FriendRequest, str]):
    if isinstance(request, str):
        request = FriendRequest(_gate_=bot.client.gate, id=request)
    await request.accept()


async def deny_request(bot: Bot, request: Union[FriendRequest, str]):
    if isinstance(request, str):
        request = FriendRequest(_gate_=bot.client.gate, id=request)
    await request.deny()


async def set_password(bot: Bot, channel: Union[PublicVoiceChannel, str], password: str = None):
    params = {'channel_id': unpack_id(channel)}
    if password is None:
        params['has_password'] = False
    else:
        params['has_password'] = True
        params['password'] = password
    await bot.client.gate.request('POST', 'channel/update', **params)


async def kickout(bot: Bot, channel: Union[PublicVoiceChannel, str], user: Union[User, str]):
    params = {'channel_id': unpack_id(channel), 'user_id': unpack_id(user)}
    await bot.client.gate.request('POST', 'channel/kickout', **params)


async def use_boost(bot: Bot, guild: Union[Guild, str], count: int):
    await bot.client.gate.request('POST', 'boost/use', guild_id=unpack_id(guild), count=count)


async def exchange(bot: Bot, code: str):
    await bot.client.gate.request('POST', 'coupon/exchange', code=code)
