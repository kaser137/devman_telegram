FROM python:3.10-slim

WORKDIR dvmn-bot

COPY requirements.txt /dvmn-bot/requirements.txt

RUN pip install -r requirements.txt

ADD . /dvmn-bot/

CMD ["python", "dvmn-bot.py"]