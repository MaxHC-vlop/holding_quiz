import random

import vk_api as vk

from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def make_keyboard():
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_button('Мой счет', color=VkKeyboardColor.POSITIVE)

    return keyboard


def echo(event, vk_api):
    keyboard = make_keyboard()

    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        keyboard=keyboard.get_keyboard(),
        random_id=random.randint(1, 1000)
    )


def main():
    env = Env()
    env.read_env()

    token = env.str("VK_TOKEN")
    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


if __name__ == "__main__":
    main()
