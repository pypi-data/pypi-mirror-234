# mxbt 

Yet another Matrix bot library.

## Installation

```sh
$ pip install mxbt
```

## Getting started

More examples [here](examples/).

**credits.json:**
```json
{
    "homeserver" : "https://matrix.org",
    "user_id" : "user",
    "password" : "password"
}
```

```python
from mxbt import Bot, Context, Creds

bot = Bot(
    prefix="!",          # Standart command prefix, commands can setup it own prefix
    creds=Creds.from_json_file("credits.json")
)

@bot.listener.on_command(prefix="?", alliases=["test", "t"])
@bot.filter.from_users(['@username:homeserver']) # Event works only with this senders
async def ctx_echo(ctx: Context) -> None: # Context object contains main info about event
    await ctx.send_text(ctx.body, reply=True) # Reply message to event room

@bot.listener.on_message
async def echo(room, message) -> None:
    await bot.api.send_text(
        room.room_id, message.body,
        reply_to=message.event_id
    )

bot.run()
```

## Special thanks

* [simplematrixbotlib](https://codeberg.org/imbev/simplematrixbotlib) for base parts of API, Listener and Callbacks code ideas.
* [matrix-nio](https://github.com/poljar/matrix-nio) for cool client library.

## Contacts

| Contact                                               | Description       |
| :---:                                                 | :---              |
| [`Matrix`](https://matrix.to/#/#librehub:matrix.org)  | Matrix server     |

## Donates
**Monero/XMR:** `47KkgEb3agJJjSpeW1LpVi1M8fsCfREhnBCb1yib5KQgCxwb6j47XBQAamueByrLUceRinJqveZ82UCbrGqrsY9oNuZ97xN`

