from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler

TOKEN = <TELEGRAM_BOT_API_KEY>
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def sendInfo(message):
    updater.bot.sendMessage(chat_id="<TELE_ID>", text=message)

if __name__ == "__main__":

    # Command Handlers
    start_handler = CommandHandler('start', start)

    dispatcher.add_handler(start_handler)

    updater.start_polling()