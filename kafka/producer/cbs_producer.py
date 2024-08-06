from kafka import KafkaProducer
import json
import os
import time
import logging

logging.basicConfig(level=logging.DEBUG)

def get_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=os.getenv('KAFKA_BROKER', 'kafka:9092'),
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            logging.info("Connected to Kafka broker")
            return producer
        except Exception as e:
            logging.error(f"Error connecting to Kafka: {e}. Retrying in 5 seconds...")
            time.sleep(5)

producer = get_kafka_producer()

def publish_to_kafka(topic, data):
    try:
        producer.send(topic, data)
        producer.flush()
        logging.info(f"Successfully sent data to topic {topic}: {data}")
    except Exception as e:
        logging.error(f"Error sending data to Kafka topic {topic}: {e}")

def produce_cbs_data(data_list):
    logging.debug(f"Data to be sent: {data_list}")
    for data in data_list:
        topic = f"{data['category']}_news"
        logging.debug(f"Publishing to topic {topic} data: {data}")
        publish_to_kafka(topic, data)

