# Kook unofficial apis

**Attention**: v2 api auth requires cookies not headers, so it is not available for bot

## Guild

### Create guild

**URL**: https://www.kookapp.cn/api/v3/guild/create

**Method**: POST

**Params**:

| Name        | Type | Is Required | Description                                                  |
| ----------- | ---- | ----------- | ------------------------------------------------------------ |
| icon        | str  | yes         | the icon of the guild, maybe it is a url of image            |
| name        | str  | yes         | the name of the server                                       |
| region      | str  | no          | the region of the server, it is an enum, but I only know there is value named "chengdu", default as "beijing" |
| template_id | int  | no          | the id of the template which you want to use, default as 0   |

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

### Update guild

**URL**: https://www.kookapp.cn/api/v3/guild/update

**Method**: POST

**Params**:

| Name                                        | Type | Is Required | Description                      |
| ------------------------------------------- | ---- | ----------- | -------------------------------- |
| guild_id                                    | str  | yes         | the id of the guild              |
| name                                        | str  | no          | the new name of the guild        |
| region                                      | str  | no          | the new region of the guild      |
| default_channel_id_setting (haven't proved) | str  | no          | the default channel of the guild |
| welcome_channel_id (haven't proved)         | str  | no          | the welcome channel of the guild |
| notify_type (haven't proved)                | int  | no          | notification type                |
| enable_open (haven't proved)                | int  | no          | open: 1, close: 0                |
| enable_widget (haven't proved)              | int  | no          | enable: 1, disable: 0            |
| widget_invite_channel_id (haven't proved)   | str  | no          | the invite channel id of widget  |

### Get available regions v2

the response of v2 apis is different from v3, it is not formated as {"code": x, "message": "xxx", "data": data}
it responds a array of regions directly

**URL**: https://www.kookapp.cn/api/v2/guilds/regions

**Method**: GET

### Get available regions v3 (pageable api)

**URL**: https://www.kookapp.cn/api/v3/guild/regions

**Method**: GET

**Response**:

| Name         | Type          | Description                  |
| ------------ | ------------- | ---------------------------- |
| items        | array<Region> | regions                      |
| sort         | array         | i dont know                  |
| meta         | object        | page meta                    |
| » page       | int           | the page                     |
| » page_total | int           | total pages                  |
| » page_size  | int           | how many regions in one page |
| » total      | int           | total regions                |



**Region**:

| Name     | Type | Description            |
| -------- | ---- | ---------------------- |
| id       | str  | the id of the region   |
| name     | str  | the name of the region |
| crowding | int  | percentage of using    |

### Join Guild

**URL**: https://www.kookapp.cn/api/v3/guild/join

**Method**: GET (WTF, kook should fix this)

**Params**:

| Name | Type | Is Required | Description                  |
| ---- | ---- | ----------- | ---------------------------- |
| code | str  | no          | the invite code of the guild |
| id   | str  | no          | the id of the guild          |

You must fill one of code or id

**Response**:

If joined, will cause HTTP 500 (Kook should fix this bug)

| Name   | Type         | Description |
| ------ | ------------ | ----------- |
| joined | boolean      | as its name |
| guild  | guild object | guild info  |

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

## Guild Security

### Update

**URL**: https://www.kookapp.cn/api/v3/guild-security/update

**Method**: POST

**Params**:

| Name     | Type    | Is Required | Description                 |
| -------- | ------- | ----------- | --------------------------- |
| guild_id | str     | yes         | the id of the guild         |
| id       | str     | yes         | the id of the security rule |
| switch   | boolean | yes         | on or off                   |

## Coupon

### Exchange

**URL**: https://www.kookapp.cn/api/v3/coupon/exchange

**Method**: POST

**Params**:

| Name | Type | Is Required | Description      |
| ---- | ---- | ----------- | ---------------- |
| code | str  | yes         | the code of item |

## Guild Boost

### Get unused boost number

**URL**: https://www.kookapp.cn/api/v3/guild-boost/get-unused-boost-num

**Method**: GET

**Response**:

| Name             | Type  | Description         |
| ---------------- | ----- | ------------------- |
| unused_boost_num | int、 | unused boost number |

## Boost

### Use boost

**URL**: https://www.kookapp.cn/api/v3/boost/use

**Method**: POST	

**Response**:

| Name     | Type | Description            |
| -------- | ---- | ---------------------- |
| guild_id | str  | the id of guild        |
| count    | int  | how many boosts to use |

## Message

### Check Card

**URL**: https://www.kookapp.cn/api/v3/message/check-card

**Method**: POST

**Params**:

| Name    | Type | Is Required | Description                    |
| ------- | ---- | ----------- | ------------------------------ |
| content | str  | yes         | the string of the card message |

**Response**:

The card message is good

| Name           | Type               | Description                                |
| -------------- | ------------------ | ------------------------------------------ |
| mention        | object             | all the mentioned objects                  |
| » mentions     | array<int>         | all mentioned user ids                     |
| » mentionRoles | array<?>           | all mentioned role ids                     |
| » mentionAll   | boolean            | is mentioning all                          |
| » mentionHere  | boolean            | is mentioning here                         |
| » mentionPart  | array<UserInfo>    | contains username, id, fullname and avatar |
| » mentionPart  | array<RoleInfo>    | i dont know                                |
| » navChannels  | array<?>           | i dont know                                |
| » channelPart  | array<ChannelInfo> | i dont know                                |
| » guildEmojis  | array<?>           | i dont know                                |
| content        | str                | the string of the card message you send    |

The card message is bad, the data will be a json array, which contains all the error messages
Example:

```json
{
    "code": 40000,
    "message": "卡片消息json没有通过验证或者不存在",
    "data": [
        "[action-group]:Elements过多"
    ]
}
```

## Item

### Use item

**URL**: https://www.kookapp.cn/api/v3/item/using

**Method**: POST

**Params**:

| Name         | Type | Is Required | Description |
| ------------ | ---- | ----------- | ----------- |
| user_item_id | int  | yes         | the item id |

### Cancel use

**URL**: https://www.kookapp.cn/api/v3/item/cancel-use

**Method**: POST

**Params**:

| Name         | Type | Is Required | Description |
| ------------ | ---- | ----------- | ----------- |
| user_item_id | int  | yes         | the item id |

### Delete items

**URL**: https://www.kookapp.cn/api/v3/item/delete

**Method**: POST

**Params**:

| Name          | Type       | Is Required | Description                    |
| ------------- | ---------- | ----------- | ------------------------------ |
| user_item_ids | array<int> | yes         | ids of the items to be deleted |

### List items

**URL**: https://www.kookapp.cn/api/v3/item/list

**Method**: GET

**Params**:

| Name     | Type | Is Required | Description                         |
| -------- | ---- | ----------- | ----------------------------------- |
| category | str  | i dont know | all, time_limit, decoration, action |

## Bag

**URL**: https://www.kookapp.cn/api/v3/item/bag

**Method**: GET

**Response**:

| Name           | Type | Description              |
| -------------- | ---- | ------------------------ |
| id             | str  | the id of the item       |
| status         | int  | i dont know              |
| type           | int  | i dont know              |
| name           | str  | the name of the item     |
| price          | int  | should be divided by 100 |
| origin_price   | int  | should be divided by 100 |
| service_time   | int  | i dont know              |
| discount_label | str  | discount string          |
| iap_code       | str  | i dont know              |

## Order

### Create orders

**URL**: https://www.kookapp.cn/api/v3/order/create

**Method**: POST

**Params**:

| Name        | Type               | Is Required | Description               |
| ----------- | ------------------ | ----------- | ------------------------- |
| products    | array<ProductInfo> | yes         | the products to buy       |
| » id        | int                | yes         | the id of the product     |
| » count     | int                | yes         | how many to buy           |
| platform    | ?                  | ?           | i dont know, default is 1 |
| request_pay | boolean            | ?           | true to pay               |

**Response**:

| Name               | Type           | Description                                                  |
| ------------------ | -------------- | ------------------------------------------------------------ |
| id                 | str            | the id of the order                                          |
| status             | int            | i dont know                                                  |
| user_id            | str            | the user who is ordering                                     |
| total_fee          | int            | the total price need be paid, divided by 100 to convert to CNY |
| pay_fee            | int            | maybe same as total_fee, i dont know                         |
| paid               | boolean        | is this order paid                                           |
| pay_time           | int            | when you create the payment                                  |
| create_time        | int            | when you create this order                                   |
| products           | array<Product> | all products will be paid                                    |
| usage_info         | str            | i dont know                                                  |
| item_entities_desc | str            | the description of the items being paid?                     |
| paydata            | object         | payment data                                                 |
| » id               | str            | the id of the payment                                        |
| » pay_fee          | str            | how many CNY you need pay, should be divided by 100          |
| » qr_code          | str            | weixin qr code link, using wechat payment                    |
| » qr_code_url      | str            | qr code link with kook server                                |
| » expired_time     | int            | when the payment will expire                                 |
| » mobile_pay       | str            | i dont know                                                  |

Product

| Name                | Type       | Description                      |
| ------------------- | ---------- | -------------------------------- |
| id                  | int        | i dont know                      |
| item_id             | int        | i dont know                      |
| item                | object     | i dont know                      |
| » id                | int        | i dont know, same as item_id     |
| » name              | str        | the name of the item             |
| » desc              | str        | the description of the item      |
| » cd                | int        | i dont know                      |
| » categories        | array<str> | all the categories it belongs to |
| » label             | int        | i dont know                      |
| » label_name        | str        | i dont know                      |
| » quality           | int        | i dont know                      |
| » icon              | str        | the icon url                     |
| » icon_thumb        | str        | i dont know                      |
| » icon_expired      | str        | i dont know                      |
| » quality_resource  | object     | i dont know                      |
| » » color           | str        | i dont know                      |
| » » small           | str        | image url                        |
| » » big             | str        | image url                        |
| » resources         | object     | i dont know                      |
| » » gif             | str        | git image url                    |
| » » height          | int        | height                           |
| » » pag             | str        | image url                        |
| » » percent         | int        | i dont know                      |
| » » preview         | str        | image url                        |
| » » preview_expired | str        | i dont know                      |
| » » time            | int        | i dont know                      |
| » » type            | str        | i dont know                      |
| » » webp            | str        | i dont know                      |
| » » width           | int        | width                            |
| » position          | str        | i dont know                      |
| total               | int        | amount of items to buy           |
| expire_time         | int        | when the order expires           |

## User

### Update self info

**URL**: https://www.kookapp.cn/api/v3/user/update

**Method**: POST

**Params**:

| Name          | Type | Is Required | Description                                                  |
| ------------- | ---- | ----------- | ------------------------------------------------------------ |
| username      | str  | no          | new username, length must be larger than 2                   |
| identify_num  | str  | no          | new identify number                                          |
| avatar        | str  | no          | the base64 of the image (data:image/png;base64,{base64 value}) |
| banner        | str  | no          | the link of the image                                        |
| mobile        | str  | no          | new mobile phone number                                      |
| mobile_prefix | str  | no          | new mobile phone prefix                                      |
| password      | str  | no          | new password                                                 |
| verify_code   | str  | no          | verify code                                                  |
