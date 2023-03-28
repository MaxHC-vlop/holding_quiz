# Holding quiz

This bot allows you to conduct quizzes from Telegram and VK .

## How to install

- Сlone this repository:
```bash
git clone git@github.com:MaxHC-vlop/sending_notifications.git
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

- Set environment variables:
    - `TG_TOKEN_BOT`
    - `VK_TOKEN`
    - `REDIS_DATABASE_HOST`
    - `REDIS_DATABASE_PORT`
    - `REDIS_DATABASE_PASSWORD`
    - `TG_TOKEN_ADMIN`
    - `TG_CHAT_ID`

## Run
```bash
poetry run python3 vk_bot.py
```

## Deploy with ubuntu

- Let's create a bot.service file in the /etc/systemd/system directory:
```bash
sudo touch /etc/systemd/system/devman_bot.service
```

- Edit devman_bot.service file:
```bash
sudo nano /etc/systemd/system/devman_bot.service
```

- Fill it with the following content:
```bash
[Service]
ExecStart='path_to_interpreter' 'path_to_executable_file'
Restart=always

[Install]
WantedBy=multi-user.target
```

- Execute commands:
```bash
# daemons reload
sudo systemctl daemon-reload

# enable daemon devman_bot
sudo systemctl enable devman_bot

# start daemon devman_bot
sudo systemctl start devman_bot

# check status
sudo systemctl status devman_bot

# check process status
# grep + executable file
ps -aux | grep main.py
```
