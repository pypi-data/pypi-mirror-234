from nio import SyncResponse, AsyncClient
from inspect import isclass
import cryptography
import importlib
import asyncio
import os

from nio.crypto import ENCRYPTION_ENABLED

from .callbacks import Callbacks
from .listener import Listener
from .module import Module
from .api import Api

from .utils import info

class Bot:

    def __init__(self, creds, prefix: str="!", selfbot: bool=False, config: dict=dict()) -> None:
        self.prefix = prefix
        self.selfbot = selfbot
        self.creds = creds 
        self.config = config

        self.api = Api(self.creds)
        self.listener = Listener(self)
        self.async_client: AsyncClient | None = None
        self.callbacks: Callbacks | None = None

    def mount_module(self, module: str) -> None:
        mod_file = importlib.import_module(module)
        for it in dir(mod_file):
            obj = getattr(mod_file, it)
            if isclass(obj) and issubclass(obj, Module) and obj != Module:
                info(f"Setup {obj.__name__} module")
                obj(self)

    def on_custom_event(self, event):
        def wrapper(func) -> None:
            @self.listener.on_custom_event(event)
            async def on_custom_event(*args) -> None:
                await func(*args)
            return on_custom_event
        return wrapper

    def on_member_join(self):
        """
        on_member_join event listener

        func params:
        --------------
        room: MatrixRoom
        event: InviteMemberEvent
        """
        def wrapper(func) -> None:
            self.listener.on_member_join(func)
        return wrapper

    def on_member_leave(self):
        """
        on_member_leave event listener

        func params:
        --------------
        room: MatrixRoom
        event: InviteMemberEvent
        """
        def wrapper(func) -> None:
            self.listener.on_member_leave(func)
        return wrapper

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
            @self.listener.on_command(**kwargs)
            async def command_func(*args) -> None:
                await func(*args)
            return command_func
        return wrapper

    def on_message(self):
        """
        on_message event listener

        func params:
        --------------
        room: MatrixRoom
        event: RoomMessageText
        """
        def wrapper(func) -> None:
            self.listener.on_message(func)
        return wrapper

    def on_reaction(self):
        def wrapper(func) -> None:
           self.listener.on_reaction(func) 
        return wrapper

    async def main(self) -> None:
        """
        Implementation from:
        https://codeberg.org/imbev/simplematrixbotlib/src/branch/master/simplematrixbotlib/bot.py
        """
        try:
            self.creds.session_read_file()
        except cryptography.fernet.InvalidToken:
            print("Invalid Stored Token")
            print("Regenerating token from provided credentials")
            os.remove(self.creds._session_stored_file)
            self.creds.session_read_file()

        await self.api.login()

        self.async_client = self.api.async_client

        resp = await self.async_client.sync(full_state=False)  #Ignore prior messages

        if isinstance(resp, SyncResponse):
            info(
                f"Connected to {self.async_client.homeserver} as {self.async_client.user_id} ({self.async_client.device_id})"
            )
            if ENCRYPTION_ENABLED:
                key = self.async_client.olm.account.identity_keys['ed25519']
                info(
                    f"This bot's public fingerprint (\"Session key\") for one-sided verification is: "
                    f"{' '.join([key[i:i+4] for i in range(0, len(key), 4)])}")

        self.creds.session_write_file()

        self.callbacks = Callbacks(self.async_client, self)
        await self.callbacks.setup()

        for action in self.listener._startup_registry:
            for room_id in self.async_client.rooms:
                await action(room_id)

        await self.async_client.sync_forever(timeout=3000, full_state=True)

    def run(self) -> None:
        asyncio.run(self.main())

