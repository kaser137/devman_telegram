import requests
import dotenv
import os
import time
import telegram
import logging

logger = logging.getLogger(__file__)


class LogTgHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    dotenv.load_dotenv()
    dvmn_token = os.environ['DVMN_TOKEN']
    bot_token = os.environ['TG_BOT_TOKEN']
    chat_id = os.environ['TC_CHAT_ID']
    bot = telegram.Bot(token=bot_token)
    logger.setLevel(logging.INFO)
    logger.addHandler(LogTgHandler(bot, chat_id))
    logger.info('start bot')
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}'}
    timestamp = time.time()
    while 1:
        try:
            try:
                response = requests.get(url, headers=headers, params={'timestamp': f'{timestamp}'}, timeout=91)
                response.raise_for_status()
                review_results = response.json()
                if review_results['status'] == 'timeout':
                    timestamp = review_results['timestamp_to_request']
                else:
                    timestamp = review_results['last_attempt_timestamp']
                    if review_results['new_attempts'][-1]['is_negative']:
                        bot.send_message(chat_id=chat_id,
                                         text=f'У Вас проверили работу: {review_results["new_attempts"][-1]["lesson_title"]}'
                                              f'\nК сожалению, в работе нашлись ошибки')
                        logger.info('работа не сдана')
                    else:
                        bot.send_message(chat_id=chat_id,
                                         text=f'У Вас проверили работу: {review_results["new_attempts"][-1]["lesson_title"]}'
                                              f'\nПреподавателю все понравилось, можно приступать к следующему уроку')
                        logger.info('работа сдана')
            except requests.exceptions.ConnectionError as err:
                print('connection error, next attempt in 5 seconds')
                logger.exception(err, exc_info=True)
                time.sleep(5)
            except requests.exceptions.ReadTimeout as err:
                logger.exception(err, exc_info=True)
        except Exception as err:
            logger.exception(err, exc_info=True)
            time.sleep(5)


if __name__ == '__main__':
    main()
