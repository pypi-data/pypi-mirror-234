from pathlib import Path

from skpy import Skype

from bsc_utils.config import config


class Messenger:

    def __init__(self):
        self.skype = Skype(user=config.skype.account, pwd=config.skype.password)
        self.contacts = self.skype.chats

    def send_message(self, msg: str, target_id: str):
        target = self.contacts[target_id]
        if target:
            target.sendMsg(msg, rich=True)

    def send_messages(self, msg: str, target_id_list: list[str]):
        [send_message(msg, target_id) for target_id in target_id_list]

    def send_attachment(self, image_path: Path | str, target_id: str):
        target = self.contacts[target_id]
        with open(Path(image_path), 'rb') as img:
            target.sendFile(img, name='', image=True)
