import logging

from environs import Env
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import CallbackContext, ConversationHandler
from telegram.ext import Filters, Updater

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


MENU = 0


def start(update: Update, context: CallbackContext) -> MENU:
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    user = update.effective_user.first_name
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    message = fr'Здравствуйте, {user}'

    update.message.reply_text(
        message,
        reply_markup=reply_markup
    )

    return MENU


def get_new_question(update: Update, context: CallbackContext) -> MENU:
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    message = 'Новый вопрос'

    update.message.reply_text(
        message,
        reply_markup=reply_markup
    )

    return MENU


def get_fail(update: Update, context: CallbackContext) -> MENU:
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    message = 'Ты сдался'

    update.message.reply_text(
        message,
        reply_markup=reply_markup
    )

    return MENU


def view_invoice(update: Update, context: CallbackContext) -> MENU:
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    message = 'Твой счет'

    update.message.reply_text(
        message,
        reply_markup=reply_markup
    )

    return MENU


def cancel(update: Update, context: CallbackContext) -> ConversationHandler.END:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Счастливо! Будем рады помочь вам.'
    )

    return ConversationHandler.END


def main() -> None:
    env = Env()
    env.read_env()
    token = env.str("token")
    updater = Updater(token)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                MessageHandler(Filters.regex(r'Новый вопрос'), get_new_question),
                MessageHandler(Filters.regex(r'Сдаться'), get_fail),
                MessageHandler(Filters.regex(r'Мой счет'), view_invoice)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
