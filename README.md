# Homework_bot

### Описание проекта:
API сервиса Практикум.Домашка позволяет отслеживать изменение статуса домашней работы на ревью.\
Статусы домашней работы могут быть трех типов: reviewing, approved, rejected.

### Как запустить проект:

`git clone git@github.com:nemnogospaal/homework_bot.git`  клонировать репозиторий

`cd homework_bot`  перейти в директорию

`python -m venv env`  создать виртуальное окружение\

`source venv/Scripts/activate`  активировать виртуальное окружение\

`python -m pip install --upgrade pip`  обновить окружение\

`pip install -r requirements.txt`  установить зависимости из файла requirements.txt\

`python homework.py`  запуск бота\

### Как тестировать проект:
`source venv/Scripts/activate`  активировать виртуальное окружение\

`pytest`  Выполнить команду из корня проекта

### Cписок используемых технологий:
- pytest
- python-dotenv
- python-telegram-bot

### Как заполнить файл .env:
В проекте есть файл .env.example заполните свой по аналогии.

`PRACTICUM_TOKEN` - токен для доступа к эндпоинту https://practicum.yandex.ru/api/user_api/homework_statuses/(API Практикум.Домашка)\
`TELEGRAM_TOKEN` - токен для работы с Bot API\
`TELEGRAM_CHAT_ID` - это ID того чата, в который бот должен отправить сообщение\
