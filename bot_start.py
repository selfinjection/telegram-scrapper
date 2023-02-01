from telethon.sync import TelegramClient, events
from session import Session
import utils
from telethon.errors import UsernameInvalidError

ID, HASH_ID, SESSION_NAME = "fff", "fff", "+f" 
BOT_TOKEN = '5843364314:f'

bot = TelegramClient('bot', ID, HASH_ID).start(bot_token=BOT_TOKEN)
session = Session(SESSION_NAME, ID, HASH_ID)

@bot.on(events.NewMessage(pattern='/get_participants'))
async def group_scrapper(event):
    arguments = event.message.message.lower().split(' ')[1:]
    if not arguments:
        await event.respond('**Usage:**\n/get_participants GROUP_1 GROUP_2 GROUP_3')
        raise events.StopPropagation

    await event.respond('Session loaded...')
    all_praticipants = {}
    for group in arguments:
        try:
            all_praticipants[group] = await session.get_participants(group)
            await event.respond(f'**{group}** done.')
        except UsernameInvalidError:
            await event.respond(f'Sorry, but I cant find this group: **{group}**')

    file_path = f'data/participants/{event.id}.csv'

    await event.respond('Loading file...')
    utils.dict_to_csv_participants(file_path, all_praticipants)

    await event.respond(f'job result, operation id {event.id}: ')
    await bot.send_file(event.chat, file_path)
    raise events.StopPropagation

@bot.on(events.NewMessage(pattern='/get_messages'))
async def group_scrapper(event):
    arguments = event.message.message.lower().split(' ')[1:]
    if not arguments:
        await event.respond('**Usage:** \n/get_messages groups=GROUP_1,GROUP_2,GROUP_3 limit=100')
        raise events.StopPropagation
    arguments = [arg.split('=') for arg in arguments]

    if arguments[1][1] == '':
        limit =  None
    else:
        limit = int(arguments[1][1])

    if len(arguments[0][0]) > 1:
        groups = arguments[0][1].split(',')
    else:
        groups = arguments[0][1]
    print(groups)
    await event.respond('Session loaded...')
    all_messages = {}
    for group in groups:
        print(group)
        try:
            try:
                all_messages[group] = await session.get_messages(group, limit=limit)
                await event.respond(f'**{group}** done.')
            except ValueError as e:
                await event.respond(f'**Error {group}:**\n{e}')
        except UsernameInvalidError:
            await event.respond(f'Sorry, but I cant find this group: **{group}**')

    file_path = f'data/messages/{event.id}.csv'
    
    await event.respond('Loading file...')
    utils.dict_to_csv_message(file_path, all_messages)

    await event.respond(f'job result, operation id {event.id}: ')
    await bot.send_file(event.chat, file_path)
    raise events.StopPropagation

@bot.on(events.NewMessage(pattern='/help'))
async def group_scrapper(event):
    await event.respond(f'**Commands:**\n/get_participants\n/get_messages\n/get_userid_by_username ')
    raise events.StopPropagation

@bot.on(events.NewMessage(pattern='/get_userid_by_username'))
async def get_userid_by_username(event):
    arguments = event.message.message.lower().split(' ')[1:]
    if not arguments:
        await event.respond('**Usage**:\n/get_userid_by_username @username')
        raise events.StopPropagation
    try:
        user = await session.client.get_entity(arguments[0])
    except UsernameInvalidError as e:
        await event.respond(f'**Error:**\n{e}')
        raise events.StopPropagation
    except ValueError as e:
        await event.respond(f'**Error:**\n{e}')
        raise events.StopPropagation

    await event.respond(f'**Result:**\nUsername: {user.username}\nUser_ID: {user.id}')
    raise events.StopPropagation

@bot.on(events.NewMessage)
async def help(event):
    await event.respond(f'**Commands:**\n/get_participants\n/get_messages\n/get_userid_by_username')
    raise events.StopPropagation

def main():
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()
    