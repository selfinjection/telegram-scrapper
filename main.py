import json
from telethon.sync import TelegramClient

def find_user_message(msg, username):
    for _, v in msg.items():
        if username == v['username']:
            return v['content']
    return None

def get_messages(cl, group_title, limit=None):
    group_entity = cl.get_entity(group_title)
    messages = cl.get_messages(group_entity, limit=limit)

    data = {}
    for message in messages:
        if message.sender_id not in data:
            data[message.sender_id] = {'username': message.sender.username, 'content': {}}
        data[message.sender_id]['content'][message.id] = message.message
    return data

def get_groups(dialogs):
    groups = []
    for dialog in dialogs:
        if dialog.is_group:
            groups.append(dialog)
    return groups

def find_message(username):
    pass

def main():
    with open('config/config.json', 'r') as file:
        data = json.load(file)

    id, hash, phone = data['380939793299']['id'], data['380939793299']['hash'], data['380939793299']['phone']
    client = TelegramClient(phone, id, hash)

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('[+] Enter the verification code: '))
    
    dialogs = client.get_dialogs()

    groups = get_groups(dialogs)
    msgs = get_messages(client, groups[0].title, limit=1000)
    practicipants = client.get_participants(groups[0])

    users = {}
    for user in practicipants:
        users[user.id] = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone
        }

    result = find_user_message(msgs, 'Fiery0304')

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    with open('practicipants.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4, ensure_ascii=False)

    with open('messages.json', 'w', encoding='utf-8') as file:
        json.dump(msgs, file, indent=4, ensure_ascii=False)

main()