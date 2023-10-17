import requests
from pathlib import Path

class teleknock():
    def __init__(self):
        try:
            with open(Path().home() / "credentials.txt", "r") as f:
                text = f.read().split('\n')
        except FileNotFoundError:
            raise(FileNotFoundError("Can not find credential file"))
        if len(text) != 2:
            raise(FileNotFoundError('Wrong credentials file'))
        self.token = text[0]
        self.chat_id = text[1]
    def sendMsg(self, obj):
        sendMessage = str(obj)
        response = requests.get(
            "https://api.telegram.org/"
            + self.token
            + "/sendMessage?chat_id="
            + self.chat_id
            +"&text="
            + sendMessage
        )
        return response.ok