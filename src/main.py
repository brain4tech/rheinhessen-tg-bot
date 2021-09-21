# main script

from time import sleep, time

import path_setup as setup

from telegram_bot import TelegramBot, BotCommand, BotCommandList

# from lib.events import onNewChatMember
from classes.user_id_list import UserIdList

if __name__ == '__main__':

    def newChatMember(chat, user, time, userlist):
        print (f"New chat member {user} in {chat} at {time}")
        userlist.register(chat, user, time)

    setup.enable()

    with open('bot_credentials/chat_id.txt', 'r') as file:
        chat_id = file.read()

    with open('bot_credentials/token.txt', 'r') as file:
        bot = TelegramBot(file.read(), return_on_update_only=False)

    bot.deleteBotCommands()
    bot.setBotCommands(BotCommandList([BotCommand("sim", "Simulation einer Aktion")]))

    userlist = UserIdList(time_interval_=5)

    while True:

        for user in userlist.timeUp():
            print ("kicked a user after 5 seconds")
            bot.kickChatMember(user[0], user[1])
            userlist.unregister(user[0], user[1])

        update = bot.poll()
        if not update:
            sleep(1)
            continue

        # --- simulation requirements ---
        command_entity = update.isBotCommand()

        if command_entity:
            command = update.message.text[command_entity.offset:command_entity.length]
            if "/sim" in command:
                # simulate different states of script
                command_params = update.message.text[command_entity.offset + command_entity.length:].strip()

                if "join" in command_params:
                    # simulate first join in group
                    # register user-id

                    user_param = command_params.replace("join", "")
                    user_param = user_param.replace(" ", "")

                    newChatMember(update.message.chat.id, user_param, update.message.date, userlist)
                    continue
                
                if command_params == "reg":
                    # simlate registering of user
                    userlist.register(update.message.chat.id, update.message.sender.id, update.message.date)
                
                if command_params == "unreg":
                    # simlate unregistering of user
                    userlist.unregister(update.message.chat.id, update.message.sender.id)


        # --- real life action ---

        if update.isMessage():
            print (f"{update.message.text} from {update.message.sender.id} in {update.message.chat.id}")


        if update.isnewChatMember():
            # print("new chat member")
            # userlist.register(update.message.chat.id, update.message.sender.id, update.message.date)
            newChatMember (update.message.chat.id, update.message.sender.id, update.message.date, userlist)
        
        # check frequently to not overuse capacitites
        sleep(1)

    setup.disable()

