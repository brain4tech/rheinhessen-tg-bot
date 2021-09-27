# This is the main script of the main Telegrambot of the Rheinhessen Telegramgroup Initiative
# Published on GitHub for transparency and showing progress
# Author: (c) Brain4Tech

# --- IMPORT STATEMENTS ---
# packages
from time import sleep
from telegram_bot import TelegramBot, BotCommand, BotCommandList, InlineButton, ButtonList

# libaries
import path_setup as setup
from lib.misc import debug_print

# classes
from classes.user_id_list import UserIdList, UserIdTimestampList


# --- CONSTANTS ---
DEBUG = True

# --- FUNCTIONS ---

def newChatMember(chat_id, user_id, user_name, time, userlist):
    debug_print (f"New chat member {user_id} in {chat_id} at {time}", DEBUG)
    # TODO: restrict user
    userlist.register(chat_id, user_id, time)
    welcome_message = f"Willkommen im Chat {user_name}!. Bitte drücke auf den untenstehenden Knopf um der Konversation beitreten zu können:"
    button_dict = ButtonList (InlineButton, [InlineButton("Der Konversation beitreten", "join_button", f"https://t.me/rheinhessen_test_group_bot?start={chat_id}")]).toBotDict()
    bot.sendMessage(chat_id, welcome_message, button_dict)

# --- START OF SCRIPT ---

# TODO: create paths and files if not existent

setup.enable()

with open('bot_credentials/chat_id.txt', 'r') as file:
    chat_id = file.read()

with open('bot_credentials/token.txt', 'r') as file:
    bot = TelegramBot(file.read(), return_on_update_only=False)

bot.deleteBotCommands()
bot.setBotCommands(BotCommandList([BotCommand("sim", "Simulation einer Aktion [event] [parameter]")]))

userlist = UserIdTimestampList("user_id_timestamp.json", time_interval_=10)

print ("--- Started Rheinhessen TelegramBot ---")

while True:

    for user in userlist.getExpiredUsers():
        response_ban = bot.kickChatMember(user[0], user[1])
        debug_print (f"kicked user {user[1]} in {user[0]}: {response_ban}", DEBUG)
        userlist.unregister(user[0], user[1])
        # TODO: delete welcome message in group

    update, response = bot.poll()
    # debug_print(response)
    if not update:
        sleep(1)
        continue

    # --- SIMULATION OF GROUP-JOINING ---
    command_entity = update.isBotCommand()

    if command_entity:
        command = update.message.text[command_entity.offset:command_entity.length]
        command_params = update.message.text[command_entity.offset + command_entity.length:].strip()
        
        # a user has started conversation with bot
        # if conversation initianted from a group, then payload of command matches group-id
        if "/start" in command:
            payload = command_params.replace(" ", "")

            if payload in userlist:
                bot.sendMessage(update.message.chat.id, "Willkommen in der Gang!")
                userlist.unregister (payload, update.message.sender.id)
                # TODO: update user permissions
                # TODO: update previous message to other message

        if "/sim" in command:
            # simulate different states of script

            if "join" in command_params:
                # simulate first join in group

                user_id = command_params.replace("join", "").replace(" ", "")

                #TODO: get user_name from group if user_param is given

                newChatMember(update.message.chat.id, user_id if user_id else update.message.sender.id, update.message.sender.first_name, update.message.date, userlist)
            
            """
            # simulation registration is not neccessary as it is integrated in "/sim join"
            if command_params == "reg":
                # simlate registering of user
                userlist.register(update.message.chat.id, update.message.sender.id, update.message.date)
            
            if command_params == "unreg":
                # simlate unregistering of user
                userlist.unregister(update.message.chat.id, update.message.sender.id)
            """

        continue

    # --- REAL LIFE ACTION ---

    """
    # left out to prevent spamming in console output
    if update.isMessage():
        debug_print (f"{update.message.text} from {update.message.sender.id} in {update.message.chat.id}")
        pass
    """

    if update.isnewChatMember():
        for new_member in update.message.new_chat_members:
            newChatMember (update.message.chat.id, new_member.id, update.message.date, userlist)
    
    # security issue: check if correct user has pressed correct button for his message
    # temporarily store user with connected message-id and check with:

    if update.isCallback():
        # TODO: see above
        pass

    # check frequently to not overuse capacities
    sleep(1)

setup.disable()

