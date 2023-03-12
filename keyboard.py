from telegram import ReplyKeyboardMarkup


def get_keyboard():
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True
    )

    return reply_markup
