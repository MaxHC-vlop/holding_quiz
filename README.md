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
    - `TG_TOKEN` - telegram bot token
    - `VK_TOKEN` - vk bot token
    - `TG_LOGGER_TOKEN` - telegram logger token
    - `TG_ADMIN_CHAT_ID` - id admin chat id
    - `REDIS_DATABASE_HOST` - redis host
    - `REDIS_DATABASE_PORT` - redis port
    - `REDIS_DATABASE_PASSWORD` - super secret password
    - `FOLDER` - directory with files for conducting polls(default `quiz-questions`)

## Run vk bot
```bash
poetry run python3 vk_bot.py
```

## Run telegram bot
```bash
poetry run python3 tg_bot.py
```