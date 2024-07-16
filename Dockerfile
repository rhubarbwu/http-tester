FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y python3-venv

WORKDIR /app
COPY . /app

RUN python3 -m venv env && . env/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["./env/bin/python", "tester.py"]
