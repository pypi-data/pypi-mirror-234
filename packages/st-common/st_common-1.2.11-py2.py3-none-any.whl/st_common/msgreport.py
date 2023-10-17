import requests

class ISZMsgReport():
    def __init__(self,webhook) -> None:
        self.webhook = webhook
        pass
    def chatbot_text(self, touser:list = ["011222671211-1181533439"], title:str = None, content:str = None):
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "code": "ipd",
            "userIds": 
                touser
            ,
            "content": content,
            "title": title
        }
        result = requests.post(self.webhook, json=data, headers=headers)
        return result