# telegram-captcha-bot

Source code for a Telegram Captcha-Bot, originally created for a Rheinhessen Telegramgroup Initiative in Germany. Published on GitHub for transparency and progress-showing purposes. I wrote it some time ago and made it more suitable for the public recently, without changing the codebase itself (see most recent commits).

*Some file contents or strings are written in German, other content is kept in English.*

**Requirements**
* Python 3.9
* Install modules with `pip install -r requirements.txt`

**Using the script**
1. Create a Telegram Bot with BotFather
2. Rename `credentials-template` to just `credentials`
3. Put the API-Token given by BotFather into the renamed file behind *BOT_TOKEN*
4. Put the Bot-Link given by BotFather into the renamed file behind *BOT_LINK*
5. Create a Telegram group, add your bot and make it an administrator
6. For this group, create an everlasting invite link and paste it in `credentials` behind *TG_GROUP_INVITE_LINK*
7. Execute `main.py`

**Notices**
* This codebase is NOT MAINTAINED
* The code has no tests and is kinda clean (...?)
* It is NOT RECOMMENDED to use this code in production, but you are absolutely allowed to get inspired by this repository

Licence: MIT; use this repository as you like

(c) 2022 Brain4Tech