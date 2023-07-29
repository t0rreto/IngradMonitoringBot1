FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY main.py /app
COPY functions.py /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]