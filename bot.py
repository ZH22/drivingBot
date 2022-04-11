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
    for currentChat in db_helper.getUsers():
        updater.bot.sendMessage(chat_id=currentChat , text=message)

# CUSTOM COMMANDS =============================================
def toggleBot(update: Update, context: CallbackContext):
    currentStatus = db_helper.toggleStatus()
    if(currentStatus == "OFF"):
        currentStatus = f"{currentStatus} 💀"
    else:
        currentStatus = f"{currentStatus} 😃"
    
    currentUser = db_helper.getUserName(str(update.effective_chat.id))
    sendInfo(f"Bot is turned {currentStatus}" + f' by {currentUser}')
    # context.bot.send_message(chat_id=update.effective_chat.id, text=f"Bot is turned {currentStatus}")

def toggleTPDS(update: Update, context: CallbackContext):
    modNum = db_helper.toggleModNum()
    sendInfo(f"TPDS checker changed to module {str(modNum)}")

# =============================================================

if __name__ == "__main__":

    # Command Handlers
    start_handler = CommandHandler('start', start)
    toggleBot_handler = CommandHandler('toggle', toggleBot)
    tpds_toggle = CommandHandler('tpds', toggleTPDS)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(toggleBot_handler)
    dispatcher.add_handler(tpds_toggle)

    updater.start_polling()