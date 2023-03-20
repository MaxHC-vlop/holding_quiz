import random
import logging

from textwrap import dedent

from fetch_questions import fetch_questions

import redis

from environs import Env
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import CallbackContext, ConversationHandler
from telegram.ext import Filters, Updater
from telegram import ReplyKeyboardMarkup


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

MENU = 0


def start(update: Update, context: CallbackContext) -> MENU:
    database = context.bot_data['redis_session']

    user = update.effective_user.first_name
    message = fr'Здравствуйте, {user}'
    database.set(user, '0', 86400)

    reply_markup = make_keyboard()

    update.message.reply_text(
        message,
        reply_markup=reply_markup
    )

    return MENU


def make_keyboard():
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )

    return reply_markup


def new_question_handler(update: Update, context: CallbackContext) -> MENU:
    questions = context.bot_data['questions']
    database = context.bot_data['redis_session']

    count_questions = len(questions)
    nubmer_question = random.randint(1, count_questions)
    question = questions[nubmer_question]['question']

    database.set(
        update.message.chat_id,
        nubmer_question
    )

    reply_markup = make_keyboard()

    update.message.reply_text(
        question,
        reply_markup=reply_markup
    )

    return MENU


def fail_handler(update: Update, context: CallbackContext) -> MENU:
    database = context.bot_data['redis_session']
    questions = context.bot_data['questions']

    nubmer_question = int(database.get(update.message.chat_id))
    answer = questions[nubmer_question]['answer']

    reply_markup = make_keyboard()

    update.message.reply_text(
        answer,
        reply_markup=reply_markup
    )
    new_question_handler(update, context)


def points_handler(update: Update, context: CallbackContext) -> MENU:
    database = context.bot_data['redis_session']
    user = update.effective_user.first_name
    points = database.get(user)

    reply_markup = make_keyboard()
    message = fr'Твой счет {points}'

    update.message.reply_text(
        message,
        reply_markup=reply_markup
    )

    return MENU


def is_right_handler(update: Update, context: CallbackContext) -> MENU:
    database = context.bot_data['redis_session']
    questions = context.bot_data['questions']
    user = update.effective_user.first_name

    nubmer_question = int(database.get(update.message.chat_id))
    asnwer = questions[nubmer_question]['answer']

    user_answer = update.message.text
    bot_answer = 'Неправильно… Попробуешь ещё раз?'
    if user_answer in asnwer:
        database.incr(user)
        bot_answer = '''\
            Правильно! Поздравляю!
            Для следующего вопроса нажми «Новый вопрос»
        '''
        bot_answer = dedent(bot_answer)

    reply_markup = make_keyboard()

    update.message.reply_text(
        bot_answer,
        reply_markup=reply_markup
    )

    return MENU


def cancel(update: Update, context: CallbackContext) -> ConversationHandler:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Счастливо! До новых встреч!',
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    env = Env()
    env.read_env()

    token = env.str("token")
    database_password = env.str('REDIS_DATABASE_PASSWORD')
    database_host = env.str('REDIS_DATABASE_HOST')
    database_port = env.int('REDIS_DATABASE_PORT')

    database = redis.Redis(
        host=database_host,
        port=database_port,
        password=database_password,
        db=0,
        decode_responses=True
    )

    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.bot_data['redis_session'] = database
    dispatcher.bot_data['questions'] = fetch_questions()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                MessageHandler(
                    Filters.regex(r'Новый вопрос'),
                    new_question_handler
                ),
                MessageHandler(
                    Filters.regex(r'Сдаться'),
                    fail_handler
                ),
                MessageHandler(
                    Filters.regex(r'Мой счет'),
                    points_handler
                ),
                MessageHandler(
                    Filters.text & ~Filters.command,
                    is_right_handler
                )
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
