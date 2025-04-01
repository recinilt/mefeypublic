from telegram import Update, Bot
import imghdr
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Merhaba! Bir mesaj gönderin, size cevap vereyim.')

def reply_good(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('iyi')

def main() -> None:
    updater = Updater("6754523785:AAFBKjgW3K_Wj3QIhe-mKzOtxRZwaLVPHOU")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_good))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
