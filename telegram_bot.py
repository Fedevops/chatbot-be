from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from bot import SimpleSpacyBot

bot = SimpleSpacyBot()

TOKEN = "6645070792:AAE9oKEaZdPNDJcQp2EJcHpRjKFcuklJLqM"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Olá! Como posso ajudar você hoje?')

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    bot_response_message = bot.respond(user_message)
    update.message.reply_text(bot_response_message)


def main() -> None:
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
