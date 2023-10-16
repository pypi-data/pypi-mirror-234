from nio import MatrixRoom, RoomMessageText, UnknownEvent, InviteMemberEvent
from .match import Match
from .context import Context

class Listener:

    def __init__(self, bot) -> None:
        self._bot = bot
        self._registry = []
        self._startup_registry = []

    def _reg_event(self, func, event) -> None:
        self._registry.append([func, event])

    def on_custom_event(self, event):

        def wrapper(func) -> None:
            if [func, event] in self._registry:
                func()
            else:
                self._reg_event(func, event)

        return wrapper

    def on_message(self, func) -> None:
        """
        on_message event listener

        func params:
        --------------
        room: MatrixRoom
        event: RoomMessageText
        """
        if [func, RoomMessageText] in self._registry:
            func()
        else:
            self._reg_event(func, RoomMessageText)

    def on_member_join(self, func) -> None:
        """
        on_member_join event listener

        func params:
        --------------
        room: MatrixRoom
        event: InviteMemberEvent
        """
        async def wrapper(room: MatrixRoom, event: InviteMemberEvent) -> None:
            if event.membership == 'join':
                await func(room, event)
        self._reg_event(wrapper, InviteMemberEvent)

    def on_member_leave(self, func) -> None:
        """
        on_member_leave event listener

        func params:
        --------------
        room: MatrixRoom
        event: InviteMemberEvent
        """
        async def wrapper(room: MatrixRoom, event: InviteMemberEvent) -> None:
            if event.membership == 'leave':
                await func(room, event)
        self._reg_event(wrapper, InviteMemberEvent)

    def on_command(self, **kwargs):
        """
        Custom on_command event listener

        listener params:
        ------------------
        aliases: list[str] - list of command aliases
        prefix: str, optional - custom command prefix (empty - use standart bot prefix)

        func params:
        ------------------
        ctx: mxbt.Context
        """
        def wrapper(func):
            async def command_func(room, event: RoomMessageText) -> None:
                prefix = ""
                if not 'prefix' in kwargs.keys():
                    prefix = self._bot.prefix
                else:
                    prefix = kwargs['prefix']

                if not event.body.startswith(prefix):
                    return

                match = Match(room, event, self._bot)
                body_command = event.body.split(" ")[0].replace(prefix, "")
                if body_command in kwargs['aliases']:
                    if self._bot.selfbot:
                        if not match.is_from_self():
                            return
                    else:
                        if match.is_from_self():
                            return
                    await func(Context.from_command(self._bot.api, room, event))
            self._reg_event(command_func, RoomMessageText)
            return command_func
        return wrapper

    def on_reaction(self, func) -> None:
        async def new_func(room, event) -> None:
            if event.type == "m.reaction":
                await func(room, event,
                           event.source['content']['m.relates_to']['key'])

        self._reg_event(new_func, UnknownEvent)

    def on_startup(self, func) -> None:
        if func in self._startup_registry:
            func()
        else:
            self._startup_registry.append(func)


