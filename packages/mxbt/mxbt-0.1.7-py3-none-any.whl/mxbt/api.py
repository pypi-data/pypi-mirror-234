from nio import AsyncClient, LoginResponse, OlmUnverifiedDeviceError, UploadResponse, AsyncClientConfig
from nio.crypto import ENCRYPTION_ENABLED
from typing import List, Union, Tuple 
from PIL import Image
import aiofiles.os
import mimetypes
import markdown
import aiohttp
import json
import nio
import os
import re

from .utils import info, error

def split_mxid(mxid: str) -> Union[Tuple[str, str], Tuple[None, None]]:
    # s = mxid.split(':')
    # if len(s) != 2 or s[0][0] != '@':
    #     return None, None
    # s[0] = s[0][1:]
    match = re.match(
        r'@(?P<localpart>[^:]*):(?P<hostname>(?P<ipv4>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|(?P<ipv6>\[[\da-fA-F:.]{2,45}\])|(?P<dns>[a-zA-Z\d\-.]{1,255}))(?P<port>:\d{1,5})?',
        mxid)
    if match is None:
        return None, None
    return match.group('localpart'), match.group('hostname')


class Api:

    def __init__(self, creds) -> None:
        self.creds = creds
        self.async_client: AsyncClient = None

    async def login(self):
        """
        Login the client to the homeserver

        Implementation from:
        https://codeberg.org/imbev/simplematrixbotlib/src/branch/master/simplematrixbotlib/api.py

        """

        if not self.creds.homeserver:
            raise ValueError("Missing homeserver")
        if not self.creds.username:
            raise ValueError("Missing Username")
        if not (self.creds.password or self.creds.login_token
                or self.creds.access_token):
            raise ValueError(
                "Missing password, login token, access token. "
                "Either password, login token or access token must be provided"
            )

        client_config = AsyncClientConfig(
            max_limit_exceeded=0,
            max_timeouts=0,
            store_sync_tokens=True,
            encryption_enabled=ENCRYPTION_ENABLED)
        store_path = "./store"
        os.makedirs(store_path, mode=0o750, exist_ok=True)
        self.async_client = AsyncClient(homeserver=self.creds.homeserver,
                                        user=self.creds.username,
                                        device_id=self.creds.device_id,
                                        store_path=store_path,
                                        config=client_config)

        if self.creds.access_token:
            self.async_client.access_token = self.creds.access_token

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.creds.homeserver}/_matrix/client/r0/account/whoami?access_token={self.creds.access_token}'
                ) as response:
                    if isinstance(response, nio.responses.LoginError):
                        raise Exception(response)

                    r = json.loads(
                        (await
                         response.text()).replace(":false,", ":\"false\","))
                    # This assumes there was an error that needs to be communicated to the user. A key error happens in
                    # the absence of an error code -> everything fine, we pass
                    try:
                        raise ConnectionError(f"{r['errcode']}: {r['error']}")
                    except KeyError:
                        pass
                    device_id = r['device_id']
                    self.async_client.user_id, user_id = (r['user_id'],
                                                          r['user_id'])
            if self.creds.username == split_mxid(user_id)[0]:
                # save full MXID
                self.creds.username = user_id
            elif user_id != self.creds.username:
                raise ValueError(
                    f"Given Matrix ID (username) '{user_id}' does not match the access token. "
                    "This error prevents you from accidentally using the wrong account. "
                    "Resolve this by providing the correct username with your credentials, "
                    f"or reset your session by deleting {self.creds._session_stored_file}"
                    #f"{' and ' + self.config.store_path if self.config.encryption_enabled else ''}."
                )
            if device_id != self.creds.device_id:
                if client_config.encryption_enabled:
                    if self.creds.device_id is not None:
                        raise ValueError(
                            f"Given device ID (session ID) '{device_id}' does not match the access token. "
                            "This is critical, because it may break your verification status unintentionally. "
                            "Fix this by providing the correct credentials matching the stored session "
                            f"{self.creds._session_stored_file}.")
                    else:
                        info(
                            "First run with access token. "
                            "Saving device ID (session ID)...")
                        self.creds.device_id, self.async_client.device_id = (device_id, device_id)
                        self.creds.session_write_file()
                else:
                    info(
                        "Loaded device ID (session ID) does not match the access token. "
                        "Recovering automatically...")
                    self.creds.device_id, self.async_client.device_id = (device_id, device_id)
                    self.creds.session_write_file()

            if client_config.encryption_enabled:
                self.async_client.load_store()

        else:
            if self.creds.password:
                resp = await self.async_client.login(
                    password=self.creds.password,
                    device_name=self.creds.device_name)

            elif self.creds.login_token:
                resp = await self.async_client.login(
                    token=self.creds.login_token,
                    device_name=self.creds.device_name)

            else:
                raise ValueError(
                    "Can't log in: Missing access token, password, or login token"
                )

            if isinstance(resp, nio.responses.LoginError):
                raise Exception(resp)

            self.creds.device_id = resp.device_id
            self.creds.access_token = resp.access_token

        if self.async_client.should_upload_keys:
            await self.async_client.keys_upload()

        return self.async_client

    async def _send_room(self,
                         room_id: str,
                         content: dict,
                         message_type: str = "m.room.message",
                         ignore_unverified_devices: bool = None) -> None:
        """
        Send a custom event in a Matrix room.

        Parameters
        -----------
        room_id : str
            The room id of the destination of the message.

        content : dict
            The content block of the event to be sent.

        message_type : str, optional
            The type of event to send, default m.room.message.

        ignore_unverified_devices : bool, optional
            Whether to ignore that devices are not verified and send the
            message to them regardless on a per-message basis.
        """

        try:
            await self.async_client.room_send(
                room_id=room_id,
                message_type=message_type,
                content=content,
                ignore_unverified_devices=ignore_unverified_devices)
        except OlmUnverifiedDeviceError as e:
            # print(str(e))
            error(
                "Message could not be sent. "
                "Set ignore_unverified_devices = True to allow sending to unverified devices."
            )
            error("Automatically blacklisting the following devices:")
            for user in self.async_client.rooms[room_id].users:
                if self.async_client.olm is None: break
                unverified: List[str] = list()
                for device_id, device in self.async_client.olm.device_store[
                    user].items():
                    if not (self.async_client.olm.is_device_verified(device) or
                            self.async_client.olm.is_device_blacklisted(device)
                    ):
                        self.async_client.olm.blacklist_device(device)
                        unverified.append(device_id)
                if len(unverified) > 0:
                    info(f"\tUser {user}: {', '.join(unverified)}")

            await self.async_client.room_send(
                room_id=room_id,
                message_type=message_type,
                content=content,
                ignore_unverified_devices=ignore_unverified_devices)

    async def delete(self, room_id: str, event_id: str, reason: str | None=None) -> None:
        await self.async_client.room_redact(room_id, event_id, reason)

    async def send_text(self, room_id: str, body: str,
                        msgtype: str="m.text",
                        reply_to: str="", edit_id: str="") -> None:
        content: dict[str, str | dict] = {
            "msgtype" : msgtype,
            "body" : body,
        }

        if edit_id != "":
            content['m.new_content'] = content.copy()
            content['m.relates_to'] = {
                "rel_type" : "m.replace",
                "event_id" : edit_id
            }
        elif reply_to != "":
            content['m.relates_to'] = {
                "m.in_reply_to" : {
                    "event_id" : reply_to
                }
            }
            
        await self._send_room(room_id=room_id, content=content)

    async def send_markdown(self, room_id: str, body: str,
                        msgtype: str="m.text",
                        reply_to: str="", edit_id: str="") -> None:
        content: dict[str, str | dict] = {
            "msgtype" : msgtype,
            "body" : body,
            "format" : "org.matrix.custom.html",
            "formatted_body" : markdown.markdown(body, extensions=['fenced_code', 'nl2br'])
        }

        if edit_id != "":
            content['m.new_content'] = content.copy()
            content['m.relates_to'] = {
                "rel_type" : "m.replace",
                "event_id" : edit_id
            }
        elif reply_to != "":
            content['m.relates_to'] = {
                "m.in_reply_to" : {
                    "event_id" : reply_to
                }
            }
            
        await self._send_room(room_id=room_id, content=content)

    async def send_reaction(self, room_id: str, event_id: str, key: str) -> None:
        await self._send_room(
            room_id=room_id,
            content={
                "m.relates_to": {
                    "event_id": event_id,
                    "key": key,
                    "rel_type": "m.annotation"
                }
            },
            message_type="m.reaction"
        )

    async def send_image(self, room_id: str, 
                         image_filepath: str, 
                         reply_to: str="", edit_id: str="") -> None:
        mime_type = mimetypes.guess_type(image_filepath)[0]
        if mime_type is None: return

        image = Image.open(image_filepath)
        (width, height) = image.size

        file_stat = await aiofiles.os.stat(image_filepath)
        async with aiofiles.open(image_filepath, "r+b") as file:
            resp, maybe_keys = await self.async_client.upload(
                file,
                content_type=mime_type,
                filename=os.path.basename(image_filepath),
                filesize=file_stat.st_size)
        if isinstance(resp, UploadResponse):
            pass  # Successful upload
        else:
            info(f"Failed Upload Response: {resp}")
            return

        content = {
            "body": os.path.basename(image_filepath),
            "info": {
                "size": file_stat.st_size,
                "mimetype": mime_type,
                "thumbnail_info": None,
                "w": width,
                "h": height,
                "thumbnail_url": None
            },
            "msgtype": "m.image",
            "url": resp.content_uri
        }

        if edit_id != "":
            content['m.new_content'] = content.copy()
            content['m.relates_to'] = {
                "rel_type" : "m.replace",
                "event_id" : edit_id
            }
        elif reply_to != "":
            content['m.relates_to'] = {
                "m.in_reply_to" : {
                    "event_id" : reply_to
                }
            }

        try:
            await self._send_room(room_id=room_id, content=content)
        except:
            error(f"Failed to send image file {image_filepath}")

    async def send_video(self, room_id: str,
                         video_filepath: str,
                         reply_to: str="", edit_id: str="") -> None:
        """
        Send a video message in a Matrix room.

        Parameters
        ----------
        room_id : str
            The room id of the destination of the message.

        video_filepath : str
            The path to the video on your machine.
        """

        mime_type = mimetypes.guess_type(video_filepath)[0]

        file_stat = await aiofiles.os.stat(video_filepath)
        async with aiofiles.open(video_filepath, "r+b") as file:
            resp, maybe_keys = await self.async_client.upload(
                file,
                content_type=mime_type,
                filename=os.path.basename(video_filepath),
                filesize=file_stat.st_size)

        if isinstance(resp, UploadResponse):
            pass  # Successful upload
        else:
            error(f"Failed Upload Response: {resp}")
            return

        content = {
            "body": os.path.basename(video_filepath),
            "info": {
                "size": file_stat.st_size,
                "mimetype": mime_type,
                "thumbnail_info": None
            },
            "msgtype": "m.video",
            "url": resp.content_uri
        }

        if edit_id != "":
            content['m.new_content'] = content.copy()
            content['m.relates_to'] = {
                "rel_type" : "m.replace",
                "event_id" : edit_id
            }
        elif reply_to != "":
            content['m.relates_to'] = {
                "m.in_reply_to" : {
                    "event_id" : reply_to
                }
            }

        try:
            await self._send_room(room_id=room_id, content=content)
        except:
            error(f"Failed to send video file {video_filepath}")

