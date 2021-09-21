# main script

from time import sleep

from telegram_bot import TelegramBot, BotCommand, BotCommandList

if __name__ == '__main__':

    with open('bot_credentials/chat_id.txt', 'r') as file:
        chat_id = file.read()

    with open('bot_credentials/token.txt', 'r') as file:
        bot = TelegramBot(file.read())

    bot.deleteBotCommands()
    bot.setBotCommands(BotCommandList([BotCommand("sim", "Simulation einer Aktion")]))

    while True:
        update = bot.poll()

        try:

            # --- simulation requirements ---
            command_entity = update.isBotCommand()

            if command_entity:
                command = update.message.text[command_entity.offset:command_entity.length]
                if "/sim" in command:

                    # simulate different states of script

                    command_params = update.message.text[command_entity.offset:]
                    if "join" in command_params:
                        # simulate first join in group
                        print ("Triggered Simulation: On first join")
                        pass
            
            # --- real life action ---

            if update.isnewChatMember:
                # start captcha procedure
                pass



        except Exception as e:
            print (f"An Error occured, skipping ID: {e}")            

        # check frequently to not overuse capacitites
        sleep(1)


