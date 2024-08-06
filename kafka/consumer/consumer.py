from kafka import KafkaConsumer
import psycopg2
import json
import os
import time
import logging

logging.basicConfig(level=logging.DEBUG)

def get_kafka_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                'us_news', 'world_news', 'politics_news', 'healthwatch_news', 'moneywatch_news',
                'entertainment_news', 'crime_news', 'sports_news', 'essentials_news',
                bootstrap_servers=os.getenv('KAFKA_BROKER', '172.21.0.5:9092'),  # Use the IP address here
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True
            )
            logging.info("Connected to Kafka broker")
            return consumer
        except Exception as e:
            logging.error(f"Error connecting to Kafka: {e}. Retrying in 5 seconds...")
            time.sleep(5)

consumer = get_kafka_consumer()

def connect_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port='5432'
            )
            cursor = conn.cursor()
            logging.info("Connected to PostgreSQL database")
            return conn, cursor
        except Exception as e:
            logging.error(f"Error connecting to PostgreSQL: {e}. Retrying in 5 seconds...")
            time.sleep(5)

conn, cursor = connect_db()

# Function to check if data already exists
def data_exists(data):
    try:
        cursor.execute(
            "SELECT 1 FROM news WHERE url = %s",
            (data['url'],)
        )
        return cursor.fetchone() is not None
    except Exception as e:
        logging.error(f"Error checking data existence: {e}")
        return True  # If there is an error, assume the data exists to avoid inserting duplicates

# Function to save data to the database
def save_to_db(data):
    try:
        if not data_exists(data):
            logging.debug(f"Inserting data: {data}")
            cursor.execute(
                """
                INSERT INTO news (source, title, url, time, category)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (data['source'], data['title'], data['url'], data['time'], data['category'])
            )
            conn.commit()
            logging.info(f"Saved data to database: {data}")
        else:
            logging.info(f"Data already exists in database: {data['url']}")
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        conn.rollback()  # Rollback transaction if there is an error

# Consume messages from Kafka and save to database
for message in consumer:
    news_data = message.value
    logging.debug(f"Received message: {news_data}")
    save_to_db(news_data)

# Close the database connection properly when script ends
def close_connection():
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    logging.info("Database connection closed")

# Ensure the connection is closed on script exit
import atexit
atexit.register(close_connection)
