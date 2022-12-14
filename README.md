# Kook unofficial apis

**Attention**: v2 api auth requires cookies not headers, so it is not available for bot

## Guild

### Create guild

**URL**: https://www.kookapp.cn/api/v3/guild/create

**Method**: POST

**Params**:

| Name        | Type | Is Required | Description                                                  |
| ----------- | ---- | ----------- | ------------------------------------------------------------ |
| icon        | str  | unknown     | the icon of the guild, maybe it is a url of image            |
| name        | str  | yes         | the name of the server                                       |
| region      | str  | unknown     | the region of the server, it is an enum, but I only know there is value named "chengdu" |
| template_id | int  | unknown     | the id of the template which you want to use                 |

**Response**:

| Name                       | Type           | Description                                                  |
| -------------------------- | -------------- | ------------------------------------------------------------ |
| id                         | str            | the id of the guild                                          |
| name                       | str            | the name of the guild                                        |
| topic                      | str            | the topic of the guild                                       |
| user_id                    | str            | who create the guild                                         |
| is_master                  | boolean        | should always be true                                        |
| icon                       | str            | the icon of the guild                                        |
| invite_enabled             | int            | i dont know                                                  |
| notify_type                | int            | the type of notification, 0 means using guild defaults settings, 1 means accepting all, 2 means only accepting when mentioned, 3 means not accepting |
| region                     | str            | where the voice chat server of the guild is                  |
| enable_open                | int            | if the guild is public                                       |
| open_id                    | str            | public server id                                             |
| default_channel_id         | str            | the id of the default channel                                |
| default_channel_id_setting | str            | i dont know                                                  |
| welcome_channel_id         | str            | the id of the welcome channel                                |
| ws_type                    | int            | i dont know                                                  |
| features                   | array          | i dont know                                                  |
| banner                     | str            | the banner of the guild                                      |
| banner_status              | int            | i dont know                                                  |
| custom_id                  | str            | i dont know                                                  |
| boost_num                  | int            | the amount of boosts has used                                |
| level                      | int            | the level of the guild                                       |
| status                     | int            | i dont know                                                  |
| live_count                 | int            | i dont know                                                  |
| channels                   | array<Channel> | the channels in the guild                                    |
| emojis                     | array<Emoji>   | the emojis in the guild                                      |

### Delete the guild  v2

you should be the master of the guild

**URL**: https://www.kookapp.cn/api/v2/guilds/{guild_id}

**Method**: DELETE

### Delete the guild v3

**URL**: https://www.kookapp.cn/api/v3/guild/delete

**Method**: POST

**Params**:

| Name     | Type | Is Required | Description         |
| -------- | ---- | ----------- | ------------------- |
| guild_id | str  | yes         | the id of the guild |

### Get available regions

the response of v2 apis is different from v3, it is not formated as {"code": x, "message": "xxx", "data": data}
it responds a array of regions directly

**URL**: https://www.kookapp.cn/api/v2/guilds/regions

**Method**: GET

**Region**:

| Name     | Type | Description            |
| -------- | ---- | ---------------------- |
| id       | str  | the id of the region   |
| name     | str  | the name of the region |
| crowding | int  | percentage of using    |

## Channel

### Update channel

this is an existed interface, but missing two params

**URL**: https://www.kookapp.cn/api/v3/channel/update

**Method**: POST

**Missing params**:

| Name         | Type    | Is Required                 | Description                       |
| ------------ | ------- | --------------------------- | --------------------------------- |
| has_password | unknown | no                          | if the voice channel has password |
| password     | str     | yes if has password is true | the password of the voice channel |

**Response**: [See official docs](https://developer.kookapp.cn/doc/http/channel#%E7%BC%96%E8%BE%91%E9%A2%91%E9%81%93)

### Kickout from voice channel

**URL**: https://www.kookapp.cn/api/v3/channel/kickout

**Method**: POST

**Params**:

| Name       | Type | Is Required | Description                                            |
| ---------- | ---- | ----------- | ------------------------------------------------------ |
| channel_id | str  | yes         | the id of the voice channel                            |
| user_id    | str  | yes         | which user you want to kick out from the voice channel |

## Gateway

### Voice channel

**URL**: https://www.kaiheila.cn/api/v3/gateway/voice

**Method**: GET

**Params**:

| Name       | Type | Is Required | Description                       |
| ---------- | ---- | ----------- | --------------------------------- |
| channel_id | str  | yes         | must be the id of a voice channel |

**Response**:

| Name          | Type | Description       |
| ------------- | ---- | ----------------- |
| gateway_url   | str  | the websocket url |
| ios_voice_sdk | int  | i dont know       |
| pc_voice_sdk  | int  | i dont know       |

## Friend

### Add friend v2

**URL**: https://www.kookapp.cn/api/v2/friends/request

**Method**: POST

**Params**:

| Name     | Type | Is Required | Description                                                  |
| -------- | ---- | ----------- | ------------------------------------------------------------ |
| from     | int  | unknown     | i dont know, official value is 0                             |
| guild_id | str  | no          | where you send the request                                   |
| user_id  | str  | yes         | the identify, format: XXX#0000, it's not the number id of user |

### Add friend v3

**URL**: https://www.kookapp.cn/api/v3/friend/request

**Method**: POST

**Params**:

| Name      | Type | Is Required             | Description                                                  |
| --------- | ---- | ----------------------- | ------------------------------------------------------------ |
| from      | int  | unknown                 | 0, 1: just add, 2: add from guild                            |
| guild_id  | str  | required when from is 2 | where you send the request                                   |
| user_code | str  | yes                     | the identify, format: XXX#0000, it's not the number id of user |

### List friend v2

**URL**: https://www.kookapp.cn/api/v2/friend/request

**Method**: GET

**Params**:

| Name | Type | Is Required | Description                          |
| ---- | ---- | ----------- | ------------------------------------ |
| type | str  | no          | i dont know, but default is "friend" |

### List friends v3

**URL**: https://www.kookapp.cn/api/v2/friends

**Method**: GET

**Response**:

| Name    | Type                 | Description     |
| ------- | -------------------- | --------------- |
| request | array<FriendRequest> | friend requests |
| friend  | array<User>          | friends         |
| blocked | array<User>          | blocked users   |

### Delete friend

**URL**: https://www.kookapp.cn/api/v3/friend/delete

**Method**: POST

**Params**:

| Name    | Type | Is Required | Description        |
| ------- | ---- | ----------- | ------------------ |
| user_id | str  | yes         | the id of the user |

### Accept/Deny friend request

**URL**: https://www.kookapp.cn/api/v3/friend/handle-request

**Method**: POST

**Params**:

| Name   | Type    | Is Required | Description                                                  |
| ------ | ------- | ----------- | ------------------------------------------------------------ |
| id     | str     | yes         | the id of the friend request which you can get from List friends v3 api |
| accept | boolean | yes         | True: accept, False: deny                                    |
