from re import L
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler

import db_helper

TOKEN = <TELEGRAM_BOT_API_KEY>
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="DRIVING BOT STARTED")

def sendInfo(message):
    updater.bot.sendMessage(chat_id="<TELE_ID>", text=message)

# CUSTOM COMMANDS =============================================
def toggleBot(update: Update, context: CallbackContext):
    currentStatus = db_helper.toggleStatus()
    if(currentStatus == "OFF"):
        currentStatus = f"{currentStatus} 💀"
    else:
        currentStatus = f"{currentStatus} 😃"
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Bot is turned {currentStatus}")

# =============================================================

if __name__ == "__main__":

    # Command Handlers
    start_handler = CommandHandler('start', start)
    toggleBot_handler = CommandHandler('toggle', toggleBot)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(toggleBot_handler)

    updater.start_polling()