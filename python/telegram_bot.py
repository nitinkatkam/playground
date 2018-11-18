#!/bin/python

#
# Author: Katkam Nitin Reddy
# Created: October 19, 2018
# Description: Telegram bot
#

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler


# Handles the Let-Me-Google-That-For-You command
def lmgtfy_handler(bot, update, args=None):
    bot.sendMessage(chat_id=update.message.chat_id, text='Let me Google that for you: https://www.google.com/search?q='+'+'.join(args), parse_mode=ParseMode.MARKDOWN)


# Entry point
def main():
    # Get the token from BotFather
    token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    # Note: Commands have to be prefixed with "/" when entering in Telegram
    dispatcher.add_handler(CommandHandler('lmgtfy', lmgtfy_handler, pass_args=True))

    updater.start_polling()


# Invoke the entry point
if __name__ == '__main__':
    main()
