import requests
import dotenv
import os
import time
import telegram
import logging




def main():
    logging.basicConfig(level=logging.INFO)
    dotenv.load_dotenv()
    dvmn_token = os.environ['DVMN_TOKEN']
    bot_token = os.environ['TG_BOT_TOKEN']
    chat_id = os.environ['TC_CHAT_ID']
    bot = telegram.Bot(token=bot_token)

    class LogTgHandler(logging.Handler):
        def emit(self, record):
            bot.send_message(chat_id=chat_id,
                             text=f'{record}')
    logger = logging.getLogger('dvmn-bot')
    logger.setLevel(logging.INFO)
    logger.addHandler(LogTgHandler())
    logger.info('start bot')
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}'}
    timestamp = time.time()
    while 1:
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
        except requests.exceptions.ConnectionError:
            print('connection error, next attempt in 2 seconds')
            logger.info('connection error, next attempt in 2 seconds')
            time.sleep(2)
        except requests.exceptions.ReadTimeout:
            pass


if __name__ == '__main__':
    main()
