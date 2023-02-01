from telethon.sync import TelegramClient

class Session:
    def __init__(self, phone, id, hash):
        self.client = TelegramClient(phone, id, hash)
        self.client.connect()
        if not self.client.is_user_authorized():
            self.client.send_code_request(phone)
            self.client.sign_in(phone, input('Verification code: '))

        self.dialogs = self.client.get_dialogs()

    async def get_messages(self, group_title, limit=None):
        group_entity = await self.client.get_entity(group_title)
        messages = await self.client.get_messages(group_entity, limit=limit)
        data = {}
        for message in messages:
            if message.sender_id not in data:
                if not message.sender_id:
                    continue
                data[message.sender_id] = {'username': message.sender.username, 'content': {}}
            data[message.sender_id]['content'][message.id] = message.message
        return data

    def get_groups(self):
        groups = []
        for dialog in self.dialogs:
            if dialog.is_group:
                groups.append(dialog)
        return groups
    
    async def get_participants(self, group_title):
        group_entity = await self.client.get_entity(group_title)
        participants = await self.client.get_participants(group_entity)
        users = {}
        for user in participants:
            users[user.id] = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone
            }

        return users