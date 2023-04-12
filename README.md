# Holding quiz

This bot allows you to conduct quizzes from Telegram and VK .

## How to install

- Сlone this repository:
```bash
git clone git@github.com:MaxHC-vlop/holding_quiz.git
```
- You must have python3.10 (or higher) installed .

- Install [poetry](https://python-poetry.org/docs/) :
```bash
pip install poetry
```
- Install project dependencies:
```bash
poetry install
```

- Set environment variables taken from [BotFather](https://t.me/BotFather), [Redis](https://redislabs.com/):
    - `TG_TOKEN`
    - `VK_TOKEN`
    - `TG_LOGGER_TOKEN`
    - `TG_ADMIN_CHAT_ID`
    - `REDIS_DATABASE_HOST`
    - `REDIS_DATABASE_PORT`
    - `REDIS_DATABASE_PASSWORD`
    - `FOLDER`

## Run vk bot
```bash
poetry run python3 vk_bot.py
```

## Run telegram bot
```bash
poetry run python3 tg_bot.py
```