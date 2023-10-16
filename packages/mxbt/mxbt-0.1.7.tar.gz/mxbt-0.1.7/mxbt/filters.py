from nio import MatrixRoom

from .context import Context
from .match import Match

class Filter:

    @staticmethod
    def __find_context(args) -> Context | None:
        for arg in args:
            if type(arg) == Context:
                return arg
    
    @staticmethod
    def __find_context_body(args) -> tuple | None:
        for index, arg in enumerate(args):
            if type(arg) == MatrixRoom:
                return args[index:index+1]
    
    @staticmethod
    def from_rooms(rooms: list):
        """
        from_rooms event filter

        filter params:
        ----------------
        rooms: list[str] 
            list of user_id, who is accepted to send event

        func params:
        --------------
        room: MatrixRoom,
        event: Event

        or 

        ctx: Context
        """
        def wrapper(func):
            async def command_func(*args) -> None:
                ctx = Filter.__find_context(args)
                if not ctx is None:
                    if Match.is_from_rooms(ctx.room.room_id, rooms):
                        await func(*args)
                else:
                    body = Filter.__find_context_body(args)
                    if body is None: return
                    room, _ = body
                    if Match.is_from_rooms(room.room_id, rooms):
                        await func(*args)
            return command_func
        return wrapper

    @staticmethod
    def from_users(users: list):
        """
        from_users event filter

        filter params:
        ----------------
        users: list[str]
            list of user_id, who is accepted to send event

        func params:
        --------------
        room: MatrixRoom,
        event: Event

        or 

        ctx: Context
        """
        def wrapper(func):
            async def command_func(*args) -> None:
                ctx = Filter.__find_context(args)
                if not ctx is None:
                    if Match.is_from_users(ctx.sender, users):
                        await func(*args)
                else:
                    body = Filter.__find_context_body(args)
                    if body is None: return
                    _, message = body
                    if Match.is_from_users(message.sender, users):
                        await func(*args)
            return command_func
        return wrapper


