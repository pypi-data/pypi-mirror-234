from .context import Context
from .match import Match

class Filter:

    def from_users(self, users: list):
        """
        from_users event filter

        filter params:
        ----------------
        users: list[str] - list of user_id, who is accepted to send event

        func params:
        --------------
        room: MatrixRoom,
        event: Event

        or 

        ctx: Context
        """
        def wrapper(func):
            async def command_func(*args) -> None:
                if len(args) == 1 and type(args[0]) == Context:
                    ctx = args[0]
                    if Match.is_from_users(ctx.sender, users):
                        await func(ctx)
                else:
                    room, message = args[0:2]
                    if Match.is_from_users(message.sender, users):
                        await func(room, message)
            return command_func
        return wrapper


