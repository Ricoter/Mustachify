FROM python:3.9.1-buster

WORKDIR /app

COPY requirements.txt ./
RUN apt update && apt -y upgrade && apt install -y gcc cmake python3-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn", "main:app" ]