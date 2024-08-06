# kafka/consumer/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY kafka/consumer/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY kafka/consumer/ .

CMD ["python", "consumer.py"]
