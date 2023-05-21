import requests
import dotenv
import os
import time
import telegram


def main():
    dotenv.load_dotenv()
    dvmn_token = os.environ['DVMN_TOKEN']
    bot_token = os.environ['BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    bot = telegram.Bot(token=bot_token)
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}'}
    timestamp = time.time()
    while 1:
        try:
            try:
                response = requests.get(url, headers=headers, params={'timestamp': f'{timestamp}'}, timeout=91)
                response.raise_for_status()
                response_json = response.json()
                if response_json['status'] == 'timeout':
                    timestamp = response_json['timestamp_to_request']
                else:
                    timestamp = response_json['last_attempt_timestamp']
                    if response_json['new_attempts'][-1]['is_negative']:
                        bot.send_message(chat_id=chat_id,
                                         text=f'У Вас проверили работу: {response_json["new_attempts"][-1]["lesson_title"]}'
                                              f'\nК сожалению, в работе нашлись ошибки')
                    else:
                        bot.send_message(chat_id=chat_id,
                                         text=f'У Вас проверили работу: {response_json["new_attempts"][-1]["lesson_title"]}'
                                              f'\nПреподавателю все понравилось, можно приступать к следующему уроку')
            except requests.exceptions.ConnectionError:
                print('connection error, next attempt in 2 seconds')
                time.sleep(2)
        except requests.exceptions.ReadTimeout:
            pass


if __name__ == '__main__':
    main()
