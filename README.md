# Отправляем уведомления о проверке работ
Телеграм бот уведомляет о результатах проверки работ на [dvmn.org](https://dvmn.org/)


## Как установить

- Скачайте код
- Установите зависимости командой
```commandline
pip install -r requirements.txt
```

Создайте бота в телеграм с помощью https://t.me/BotFather.
Создайте файл `.env` с переменными окружения в папке проекта:
- DVMN_TOKEN= токен доступа к [API Devman](https://dvmn.org/api/docs/)  
- TG_BOT_TOKEN= токен бота
- TC_CHAT_ID=  id Вашей учетной записи в телеграм, можно узнать https://telegram.me/userinfobot

## Как использовать
Запустить бот:
```commandline
python3 dvmn-bot.py 
```

Как только работа будет проверена, бот пришлёт Вам оповещение, например:

`Преподаватель проверил работу "Отправляем уведомления о проверке работ
К сожалению, в работе нашлись ошибки`

# Часть 2. Докеризация.

## Как создать и запустить контейнер.
- Установите Докер с сайта [docker.com](https://www.docker.com/)
- Создайте образ из директории проекта командой в терминале:
```commandline
docker build -t <name_of_image:tag(default=latest)> .
```
- не забудьте поставить точку, или путь к файлу Dockerfile
- Создайте контейнер командой в терминале:
```commandline
docker run --env-file .env --name <name_of_container> <name_of_image:tag(default=latest)>
```
вместо .env надо указать ссылку на файл .env, в случае если Вы находитесь в разных директориях. 
- Контейнер с именем `<name_of_container> ` создан и запущенб, бот работает.
- Для остановки контейнера наберите команду:
```commandline
docker stop <name_of_container>
```
- Для следующего запуска контейнера достаточно команды:
```commandline
docker start <name_of_container>
```
- Часто помогает команда:
```commandline
docker --help
```
