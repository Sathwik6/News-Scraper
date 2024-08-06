# webserver/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY webserver/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY webserver/ .

CMD ["python", "app.py"]
