import os

STATES =  ['start', 'options', 'fast_avatar', 'train_avatar', 'result']

class User:
    def __init__(self, id, msg_id, date, type, text, group_media_id):
        self.id = id
        self.msg_id = [msg_id]
        self.date = date
        self.type = type
        self.text = text
        self.state = STATES[0]
        self.theme = 'other' # business, sport, casual, other
        self.group_media_id = group_media_id
        self.num = 0
        self.free = True
        self.payment = 0
        
        if not os.path.exists(f"photos/{self.id}"):
            os.mkdir(f"photos/{self.id}")

    def update_msg(self, msg_id, date, type, text, group_media_id):
        self.msg_id.append(msg_id)
        self.date = date
        self.type = type
        self.text = text
        self.group_media_id = group_media_id

    def update_flow(self, state):
        self.state = state

    def update_num(self):
        self.num += 1

    def update_payment(self, payment):
        self.payment = payment