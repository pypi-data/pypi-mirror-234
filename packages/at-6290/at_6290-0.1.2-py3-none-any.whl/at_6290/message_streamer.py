import threading
from . import read_latest_message


class MessageStreamer:
    api_id = None
    api_hash = None
    channel_url = None
    callback = None
    phone = None
    username = None

    def __init__(self, api_id, api_hash, phone, username, channel_url, callback):
        self.api_id = int(api_id)
        self.api_hash = str(api_hash)
        self.phone = str(phone)
        self.username = str(username)
        self.channel_url = str(channel_url)
        self.callback = callback

    def subscribe(self):
        c_thread = threading.Thread(target=lambda: read_latest_message.LatestMessageReader(
            self.api_id, self.api_hash, self.phone, self.username, self.channel_url, self.callback))
        c_thread.start()
