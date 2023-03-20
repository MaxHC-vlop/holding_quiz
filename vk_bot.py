import logging
import redis
import vk_api
import random

from environs import Env
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from fetch_questions import fetch_questions

env = Env()
env.read_env()

logger = logging.getLogger(__file__)


def make_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.PRIMARY)
    return keyboard


def handle_solution_attempt(event, vk_bot, database, questions):
    user_id = event.user_id
    keyboard = make_keyboard()
    nubmer_question = database.get(user_id)
    points = f'{user_id}_points'
    if not nubmer_question:
        database.set(points, '0', 86400)
        vk_bot.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message='Старт'
        )
        return None

    answer = questions[int(nubmer_question)]['answer']
    reply_text = event.text
    if reply_text in answer:
        database.incr(points)
        reply_text = 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»'
    else:
        reply_text = 'Неправильно… Попробуешь ещё раз?'

    vk_bot.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=reply_text,
        keyboard=keyboard.get_keyboard()
    )


def handle_new_question_request(event, vk_bot, database, questions):
    user_id = event.user_id
    logger.info(f'{user_id} requests new question')
    count_questions = len(questions)
    nubmer_question = random.randint(1, count_questions)
    question = questions[int(nubmer_question)]['question']

    database.set(user_id, nubmer_question)
    keyboard = make_keyboard()
    vk_bot.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        message=f'Новый вопрос: {question}',
        keyboard=keyboard.get_keyboard()
    )


def handle_surrender(event, vk_bot, database, questions):
    user_id = event.user_id
    logger.info(f'{user_id} gave up')
    nubmer_question = database.get(user_id)
    question = questions[int(nubmer_question)]['question']
    answer = questions[int(nubmer_question)]['answer']
    keyboard = make_keyboard()
    vk_bot.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        message=(
            f'Вопрос: {question}\n'
            f'Правильный ответ: {answer}'
        ),
        keyboard=keyboard.get_keyboard()
    )

    new_question = handle_new_question_request(
        event, vk_bot, database, questions
    )

    return new_question


def handle_score(event, vk_bot, database):
    user_id = event.user_id
    points = f'{user_id}_points'
    counter = database.get(points)
    logger.info(f'{user_id} requests points')
    keyboard = make_keyboard()
    vk_bot.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        message=f'Ваш счет: {counter}',
        keyboard=keyboard.get_keyboard()
    )


def main():
    vk_token = env.str('VK_TOKEN')
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

    questions = fetch_questions()

    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.info('VK bot running...')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if 'Новый вопрос' in event.text:
                handle_new_question_request(
                    event, vk, database, questions
                )
            elif 'Сдаться' in event.text:
                handle_surrender(
                    event, vk, database, questions
                )
            elif 'Мой счёт' in event.text:
                handle_score(
                    event, vk, database
                )
            else:
                handle_solution_attempt(
                    event, vk, database, questions
                )


if __name__ == '__main__':
    main()
