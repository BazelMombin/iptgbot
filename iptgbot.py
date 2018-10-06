from telegram import Bot, MessageEntity, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                                                  Dispatcher, CallbackQueryHandler)
import logging
import requests
import json


#telegram bot token
TOKEN = "XXXX"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                        level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    user = update.message.from_user
    update.message.reply_text('Чтобы узнать об IP адресе просто напишите его и мы расскажем вам о нем')

def insert(bot, update):
    user = update.message.from_user
    text = update.message.text
    caption = update.message.caption
    response = requests.post("http://api.hostip.info/get_html.php?ip="+text+"&position=true")

    log_file = open("log.txt", "a")
    s1 = str(user)+"\n"
    log_file.write(s1)
    log_file.close()
    print(response.status_code)
    print(user)
    if response.status_code == 200:
        reply_string = response.text
        print(reply_string)
    else:
        reply_string = "Произошла ошибка, напишите IP адрес информацию о котором вы хотите узнать"
        



    update.message.reply_text(reply_string,parse_mode="HTML")



def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main(webhook_url=None):
        # Get the dispatcher to register handlers
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher

        start_handler = CommandHandler('start', start)
        insert_handler = MessageHandler(Filters.all , insert)
        dp.add_handler(start_handler)
        dp.add_handler(insert_handler)
        dp.add_error_handler(error)

        # Start the Bot
        updater.start_polling()
        updater.idle()



if __name__ == '__main__':
        main()