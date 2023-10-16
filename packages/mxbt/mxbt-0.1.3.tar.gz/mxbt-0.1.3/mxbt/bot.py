from nio import SyncResponse, AsyncClient
from inspect import isclass
import cryptography
import importlib
import asyncio
import os

from nio.crypto import ENCRYPTION_ENABLED

from .callbacks import Callbacks
from .listener import Listener
from .filters import Filter
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
        self.filter = Filter()
        self.async_client: AsyncClient = None
        self.callbacks: Callbacks = None

    def mount_module(self, module: str) -> None:
        mod_file = importlib.import_module(module)
        for it in dir(mod_file):
            obj = getattr(mod_file, it)
            if isclass(obj) and issubclass(obj, Module) and obj != Module:
                info(f"Setup {obj.__name__} module")
                obj(self)

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

