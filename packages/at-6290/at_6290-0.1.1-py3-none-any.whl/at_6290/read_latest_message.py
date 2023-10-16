import configparser
# from configs.cmd_line_flags import CmdLineFlags

import asyncio
import time
from at_8257.at_datetime_utils import get_ist_timestamp, get_current_time_millis, to_ist
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, TimedOutError, RPCError, InvalidBufferError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)


# from log_stuff import dated_log_it


class LatestMessageReader:
    # config = None
    api_id = None
    api_hash = None
    channel_url = None
    callback = None
    phone = None
    username = None
    client = None
    me = None
    builder = None

    def __init__(self, api_id, api_hash, phone, username, channel_url, callback):
        self.api_id = int(api_id)
        self.api_hash = str(api_hash)
        self.phone = str(phone)
        self.username = str(username)
        self.channel_url = str(channel_url)
        self.callback = callback
        asyncio.run(self.init())

    # def build(self):
    #     if self.builder is None:
    #         raise Exception("LatestMessageReader Builder is None")
    #     return

    async def init(self):
        session_name = str(self.username) + "_" + str(get_current_time_millis())
        # Create the client and connect
        self.client = TelegramClient(session_name, int(self.api_id), self.api_hash)
        # dated_log_it("Awaiting for Client Start")
        await self.client.start()
        # dated_log_it("Client Created")
        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            try:
                await self.client.sign_in(self.phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await self.client.sign_in(password=input('Password: '))

        self.me = await self.client.get_me()
        if self.channel_url.isdigit():
            entity = PeerChannel(int(self.channel_url))
        else:
            entity = self.channel_url

        registration_timestamp = get_ist_timestamp()
        last_timestamp = registration_timestamp
        my_channel = await self.client.get_entity(entity)

        while True:
            valid_msgs = await self.get_all_messages_after_timestamp(my_channel, last_timestamp)
            if len(valid_msgs) > 0:
                last_timestamp = to_ist(valid_msgs[0].date)
            for msg in valid_msgs:
                self.callback(msg.message)
            time.sleep(2)
        return

    async def get_all_messages_after_timestamp(self, my_channel, given_timestamp):
        valid_msgs = []
        last_offset_id = 0
        while True:
            history = None
            try:
                history = await self.client(GetHistoryRequest(
                    peer=my_channel,
                    offset_id=last_offset_id,
                    offset_date=None,
                    add_offset=0,
                    limit=1,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))
            except TimedOutError as e:
                # dated_log_it("Exception TimedOutError in telegram get message: ", e)
                a = 1
            except RPCError as e:
                # dated_log_it("Exception RPCError in telegram get message: ", e)
                a = 1
            except InvalidBufferError as e:
                # dated_log_it("Exception InvalidBufferError in telegram get message: ", e)
                a = 1
            except Exception as e:
                # dated_log_it("Exception in telegram get message: ", e)
                a = 1
            except:
                # dated_log_it("Exception UNKNOWN in telegram get message: ", e)
                a = 1

            if history is not None and history.messages and len(history.messages) > 0:
                message = history.messages[0]
                if to_ist(message.date) > given_timestamp:
                    valid_msgs.append(message)
                    last_offset_id = message.id
                else:
                    break
            else:
                break
        return valid_msgs
