# main script

from time import sleep

import path_setup as setup

from telegram_bot import TelegramBot, BotCommand, BotCommandList

# from lib.events import onNewChatMember
from classes.user_id_list import UserIdList

if __name__ == '__main__':

    setup.enable()

    with open('bot_credentials/chat_id.txt', 'r') as file:
        chat_id = file.read()

    with open('bot_credentials/token.txt', 'r') as file:
        bot = TelegramBot(file.read())

    bot.deleteBotCommands()
    bot.setBotCommands(BotCommandList([BotCommand("sim", "Simulation einer Aktion")]))

    userlist = UserIdList()
    print (userlist)

    while True:
        update = bot.poll()

        # --- simulation requirements ---
        command_entity = update.isBotCommand()

        if command_entity:
            command = update.message.text[command_entity.offset:command_entity.length]
            if "/sim" in command:

                # simulate different states of script

                command_params = update.message.text[command_entity.offset + command_entity.length:].strip()
                if command_params == "join":
                    # simulate first join in group
                    print ("Triggered Simulation: On first join")
                    continue
                
                if command_params == "reg":
                    # simlate registering of user
                    userlist.register(update.message.chat.id, update.message.sender.id, update.message.date)
                    print(userlist)
                    continue
                
                if command_params == "unreg":
                    # simlate unregistering of user
                    userlist.unregister(update.message.chat.id, update.message.sender.id)
                    print(userlist)
                    continue
        
        # --- real life action ---

        if update.isnewChatMember():
            # start captcha procedure

            # onNewChatMember()
            pass
        # check frequently to not overuse capacitites
        sleep(1)

    setup.disable()

