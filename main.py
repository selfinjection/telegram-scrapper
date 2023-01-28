import json
from telethon.sync import TelegramClient

class Session:
    def __init__(self, phone, id, hash):
        self.client = TelegramClient(phone, id, hash)
        self.client.connect()
        if not self.client.is_user_authorized():
            self.client.send_code_request(phone)
            self.client.sign_in(phone, input('[+] Enter the verification code: '))

        self.dialogs = self.client.get_dialogs()

    def find_user_message(self, msg, username):
        for _, v in msg.items():
            if username == v['username']:
                return v['content']
        return None

    def get_messages(self, group_title, limit=None):
        group_entity = self.client.get_entity(group_title)
        messages = self.client.get_messages(group_entity, limit=limit)

        data = {}
        for message in messages:
            if message.sender_id not in data:
                data[message.sender_id] = {'username': message.sender.username, 'content': {}}
            data[message.sender_id]['content'][message.id] = message.message
        return data

    def get_groups(self):
        groups = []
        for dialog in self.dialogs:
            if dialog.is_group:
                groups.append(dialog)
        return groups
    
    def get_participants(self, group_title):
        participants = self.client.get_participants(group_title)

        users = {}
        for user in participants:
            users[user.id] = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone
            }

        return users


def main():
    #with open('config/config.json', 'r') as file:
    #    data = json.load(file)

    id, hash, phone = 123, 123, 123

    session = Session(phone, id, hash)

    # groups = session.get_groups()
    group_title = '123'
    user_to_find = 'Fiery0304'

    msgs = session.get_messages(group_title, limit=1000)
    participants = session.get_participants(group_title)
    user_messages = session.find_user_message(msgs, user_to_find)

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(user_messages, file, indent=4, ensure_ascii=False)

    with open('participants.json', 'w', encoding='utf-8') as file:
        json.dump(participants, file, indent=4, ensure_ascii=False)

    with open('messages.json', 'w', encoding='utf-8') as file:
        json.dump(msgs, file, indent=4, ensure_ascii=False)

main()