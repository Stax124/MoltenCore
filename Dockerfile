FROM python:3.10-slim

ARG TOKEN
ENV DISCORD_BOT_TOKEN=${TOKEN}

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y git curl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY frontend/dist frontend/dist

HEALTHCHECK --interval=1m --timeout=3s CMD curl --fail http://localhost:8080/api/system/healthy || exit 1

CMD [ "python", "./main.py", "--disable-virtualenv-check" ]