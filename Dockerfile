FROM python:alpine

ARG TRINITY_TOKEN
ENV TRINITY=${TRINITY_TOKEN}

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY frontend/dist frontend/dist

CMD [ "python", "./main.py" ]