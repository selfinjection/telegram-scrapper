import csv

def dict_to_csv_message(path, data):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ['Group_name', 'User_id', 'Username', 'Message']
        writer.writerow(header)
        for group_name, v in data.items():
            for user_id, x in v.items():
                for _, message in x['content'].items():
                    row = [group_name, user_id, x['username'], message]
                    writer.writerow(row)

def dict_to_csv_participants(path, data):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ['Group_name', 'User id', 'Username', 'First name', 'Last name', 'Phone number']
        writer.writerow(header)
        for group_name, v in data.items():
            for user_id, content in v.items():
                row = [group_name, user_id, content['username'], content['first_name'], content['last_name'], content['phone_number']]
                writer.writerow(row)