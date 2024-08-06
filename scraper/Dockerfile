# scraper/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY scraper/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY scraper/ .
COPY kafka/producer/ /app/kafka/producer/

CMD ["python", "scraper.py"]
