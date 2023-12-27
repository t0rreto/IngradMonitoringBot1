FROM python:3.9

WORKDIR /app
COPY . /app

ENV TZ Europe/Moscow

RUN pip install -r requirements.txt

CMD [ "python", "-u", "main.py"]