# mxbt 

Yet another Matrix bot library.

## Installation

```sh
$ pip install mxbt
```

## Getting started

More examples [here](examples/).

```python
from mxbt import Bot, Context, Creds, Filter

bot = Bot(
    prefix="!",          # Standart command prefix, commands can setup it own prefix
    creds=Creds.from_json_file("credits.json")
)

@bot.on_command(prefix="?", aliases=["test", "t"])
@Filter.from_users(['@username:homeserver'])    # Event works only with this senders
async def ctx_echo(ctx: Context) -> None:       # Context object contains main info about event
    await ctx.send_text(ctx.body, reply=True)   # Reply message to event room

bot.run()
```

**credits.json** structure
```json
{
    "homeserver" : "https://matrix.org",
    "user_id" : "user",
    "password" : "password"
}
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

