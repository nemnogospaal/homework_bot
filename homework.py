import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

import exceptions

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверить наличие переменных окружения."""
    return all([PRACTICUM_TOKEN,
               TELEGRAM_TOKEN,
               TELEGRAM_CHAT_ID])


def send_message(bot, message):
    """Отправить сообщение в Telegram."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID,
                         message)
        logging.debug('Сообщение успешно отправлено')
    except Exception as error:
        logging.error(f'Сбой при отправке сообщения {error}')


def get_api_answer(timestamp):
    """Получить ответ от API."""
    timestamp = int(time.time())
    url = ENDPOINT
    headers = HEADERS
    payload = {'from_date': timestamp}
    try:
        homework_statuses = requests.get(url=url,
                                         headers=headers,
                                         params=payload)
        if homework_statuses.status_code != HTTPStatus.OK:
            logging.error('Недоступность ENDPOINT')
            raise exceptions.HTTPStatusError(
                'Не удалось получить ответ от API')
        return homework_statuses.json()
    except Exception:
        logging.error('Недоступность ENDPOINT')
        raise exceptions.HTTPStatusError('Недоступность ENDPOINT')


def check_response(response):
    """Проверить корректность ответа."""
    logging.debug('Начата проверка ответа API')
    if not isinstance(response, dict):
        raise TypeError('ответ получен не в виде dict')
    if 'homeworks' not in response:
        raise KeyError('отсутствует ключ homeworks')
    homework = response.get('homeworks')
    if not isinstance(homework, list):
        raise TypeError('ответ получен не в виде list')
    return homework


def parse_status(homework):
    """Парсить статус проверки работы."""
    if 'homework_name' not in homework:
        raise TypeError('отсутсвует ключ homework_name')
    status = homework['status']
    if status not in HOMEWORK_VERDICTS:
        logging.critical('Неожиданный статус работы')
        raise exceptions.MissedStatusError(
            f'Неизвестный статус работы - {status}')
    else:
        verdict = HOMEWORK_VERDICTS[status]
        homework_name = homework['homework_name']
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical('отсутствуют переменные окружения')
        sys.exit(1)

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    current_report = {}
    prev_report = {}

    while True:
        try:
            response = get_api_answer(timestamp)
            timestamp = check_response(response)
            homework_list = response.get('homeworks')
            if homework_list:
                homework = homework_list[0]
                message = parse_status(homework)
                current_report[response.get(
                    'homework_name')] = response.get('status')
                if current_report != prev_report:
                    send_message(bot, message)
                    prev_report = current_report.copy()
                    current_report[response.get(
                        'homework_name')] = response.get('status')

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.critical(message)
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
