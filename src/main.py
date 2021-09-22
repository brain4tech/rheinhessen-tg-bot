# main script

from time import sleep, time

import path_setup as setup

from telegram_bot import TelegramBot, BotCommand, BotCommandList, InlineButton, ButtonList

# from lib.events import onNewChatMember
from classes.user_id_list import UserIdList

if __name__ == '__main__':
    setup.enable()

    with open('bot_credentials/chat_id.txt', 'r') as file:
        chat_id = file.read()

    with open('bot_credentials/token.txt', 'r') as file:
        bot = TelegramBot(file.read(), return_on_update_only=False)

    
    def newChatMember(chat, user, time, userlist):
        print (f"New chat member {user} in {chat} at {time}")
        # TODO: restrict user
        userlist.register(chat, user, time)
        welcome_message = f"Willkommen im Chat {user}!. Bitte drücke auf den untenstehenden Knopf um der Konversation beitreten zu können:"
        button_dict = ButtonList (InlineButton, [InlineButton("Der Konversation beitreten", "join_button", f"https://t.me/johannes_group_mod_bot?start={chat}")]).toBotDict()
        bot.sendMessage(chat, welcome_message, button_dict)

    bot.deleteBotCommands()
    bot.setBotCommands(BotCommandList([BotCommand("sim", "Simulation einer Aktion")]))

    userlist = UserIdList(time_interval_=10)

    while True:

        for user in userlist.timeUp():
            print (f"kicked user {user[1]} in {user[0]}")
            print (bot.kickChatMember(user[0], user[1]))
            userlist.unregister(user[0], user[1])
            # TODO: delete welcome message in group

        update = bot.poll()
        if not update:
            sleep(1)
            continue

        # --- simulation requirements ---
        command_entity = update.isBotCommand()

        if command_entity:
            command = update.message.text[command_entity.offset:command_entity.length]
            command_params = update.message.text[command_entity.offset + command_entity.length:].strip()
            if "/start" in command:
                # a user has started conversation with bot
                # if conversation initianted from a group, then chat-id of group will be payload
                payload = command_params.replace(" ", "")

                if payload in userlist:
                    bot.sendMessage(update.message.chat.id, "Willkommen in der Gang!")
                    userlist.unregister (payload, update.message.sender.id)
                    # TODO: update user permissions
                    # TODO: update previous message to other message
                
                continue

            if "/sim" in command:
                # simulate different states of script

                if "join" in command_params:
                    # simulate first join in group

                    user_param = command_params.replace("join", "")
                    user_param = user_param.replace(" ", "")

                    newChatMember(update.message.chat.id, user_param if user_param else update.message.sender.id, update.message.date, userlist)
                
                if command_params == "reg":
                    # simlate registering of user
                    userlist.register(update.message.chat.id, update.message.sender.id, update.message.date)
                
                if command_params == "unreg":
                    # simlate unregistering of user
                    userlist.unregister(update.message.chat.id, update.message.sender.id)

                continue

        # --- real life action ---

        if update.isMessage():
            print (f"{update.message.text} from {update.message.sender.id} in {update.message.chat.id}")
            # print (f"{update.message.text} from {update.message.sender.id} in {update.message.chat.id}:\n{update.content}")
            pass

        if update.isnewChatMember():
            # print("new chat member")
            # userlist.register(update.message.chat.id, update.message.sender.id, update.message.date)
            for new_member in update.message.new_chat_members:
                newChatMember (update.message.chat.id, new_member.id, update.message.date, userlist)
        
        # security issue: check if correct user has pressed correct button for his message
        # temporarily store user with connected message-id and check with:

        if update.isCallback():
            # TODO: see above
            pass

        # check frequently to not overuse capacitites
        sleep(1)

    setup.disable()

