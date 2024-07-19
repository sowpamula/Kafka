import pandas as pd
from kafka import KafkaProducer
import json

# Function to read the e-commerce dataset
def read_dataset(file_path):
    # Replace with the path to your e-commerce dataset
    return pd.read_csv(file_path)

# Function to publish messages to Kafka
def publish_to_kafka(producer, topic, messages):
    for message in messages:
        producer.send(topic, value=message)
        producer.flush()


if __name__ == "__main__":
    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # Read the dataset
    file_path = 'Luxurywatch.csv'
    df = read_dataset(file_path)

    # Convert dataframe to list of dictionaries
    messages = df.to_dict(orient='records')

    # Publish messages to Kafka
    publish_to_kafka(producer, 'quickstart-events', messages)

    print("Data published to Kafka topic 'quickstart-events'")
