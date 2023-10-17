from nio import MatrixRoom, Event, RoomMessageText
from dataclasses import dataclass, field
from typing import List

from .types.file import File, FileType
from .api import Api

@dataclass
class Context:
    """
    Event context class
    """
    api: Api
    room: MatrixRoom
    room_id: str
    event: Event
    sender: str
    event_id: str
    body: str=str()
    command: str=str()
    args: List[str]=field(
        default_factory=lambda: list()
    )

    async def __send(self, body: str | File, use_html: bool, reply: bool, edit: bool) -> None:
        if isinstance(body, str):
            if use_html: 
                await self.send_markdown(body, reply, edit)
            else: 
                await self.send_text(body, reply, edit)
        elif isinstance(body, File):
            if body.filetype == FileType.Image:
                await self.send_image(body.path, reply, edit)
            elif body.filetype == FileType.Video:
                await self.send_video(body.path, reply, edit)

    async def send(self, body: str | File, use_html: bool=False) -> None:
        """
        Send text or file to context room

        Parameters:
        -------------
        body: str | mxbt.types.File
            Text of message or File object to send
        use_html: bool, optional
            Use html formatting or not
        """
        await self.__send(body, use_html, False, False)

    async def reply(self, body: str | File, use_html: bool=False) -> None:
        """
        Reply context message with text or file

        Parameters:
        -------------
        body: str | mxbt.types.File
            Text of message or File object to send
        use_html: bool, optional
            Use html formatting or not
        """
        await self.__send(body, use_html, True, False)

    async def edit(self, body: str | File, use_html: bool=False) -> None:
        """
        Edit context message with text or file

        Parameters:
        -------------
        body: str | mxbt.types.File
            Text of message or File object to send
        use_html: bool, optional
            Use html formatting or not
        """
        await self.__send(body, use_html, False, True)
 
    async def delete(self, reason: str | None=None) -> None:
        """
        Delete context event

        Parameters:
        -------------
        reason: str | None - optional
            Reason, why message is deleted
        """
        await self.api.delete(
            self.room.room_id,
            self.event.event_id,
            reason
        )

    async def send_text(self, 
                        body: str, 
                        reply: bool=False,
                        edit: bool=False) -> None:
        """
        Send text to context room.

        Parameters:
        --------------
        body : str
            Text of message.

        reply : bool, optional
            Is your message need to reply event.

        edit : bool, optional
            Is your message need to edit event (your messages only).
        """
        await self.api.send_text(
            self.room.room_id,
            body,
            reply_to=self.event.event_id if reply else "",
            edit_id=self.event.event_id if edit else ""
        )

    async def send_markdown(self, 
                            body: str, 
                            reply: bool=False, 
                            edit: bool=False) -> None:
        """
        Send markdown to context room.

        Parameters:
        --------------
        body : str
            Text of message.

        reply : bool, optional
            Is your message need to reply event.

        edit : bool, optional
            Is your message need to edit event (your messages only).
        """
        await self.api.send_markdown(
            self.room.room_id,
            body,
            reply_to=self.event.event_id if reply else "",
            edit_id=self.event.event_id if edit else ""
        )

    async def send_image(self, 
                         filepath: str, 
                         reply: bool=False, 
                         edit: bool=False) -> None:
        """
        Send image to context room.

        Parameters:
        --------------
        filepath : str
            Path to image.

        reply : bool, optional
            Is your message need to reply event.

        edit : bool, optional
            Is your message need to edit event (your messages only).
        """
        await self.api.send_image(
            self.room.room_id,
            filepath,
            self.event.event_id if reply else "",
            self.event.event_id if edit else ""
        )

    async def send_video(self, 
                         filepath: str, 
                         reply: bool=False, 
                         edit: bool=False) -> None:
        """
        Send video to context room.

        Parameters:
        --------------
        filepath : str
            Path to video.

        reply : bool, optional
            Is your message need to reply event.

        edit : bool, optional
            Is your message need to edit event (your messages only).
        """
        await self.api.send_video(
            self.room.room_id,
            filepath,
            self.event.event_id if reply else "",
            self.event.event_id if edit else ""
        )

    async def send_reaction(self, body: str) -> None:
        """
        Send reaction to context message.

        Parameters:
        --------------
        body : str
            Reaction emoji.
        """
        await self.api.send_reaction(
            self.room.room_id,
            self.event.event_id,
            body
        )

    @staticmethod
    def __parse_command(message: RoomMessageText) -> tuple:
        args = message.body.split(" ")
        command = args[0]
        if len(args) > 1:
            args = args[1:]
        return command, args

    @staticmethod
    def from_command(api: Api, room: MatrixRoom, message: RoomMessageText):
        command, args = Context.__parse_command(message)
        return Context(
            api=api,
            room=room, 
            room_id=room.room_id,
            event=message,
            sender=message.sender,
            event_id=message.event_id,
            body=message.body,
            command=command,
            args=args
        )

    @staticmethod
    def from_text(api: Api, room: MatrixRoom, message: RoomMessageText):
        return Context(
            api=api,
            room=room,
            room_id=room.room_id,
            event=message,
            sender=message.sender,
            event_id=message.event_id,
            body=message.body
        )

