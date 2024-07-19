import pandas as pd
import json
from kafka import KafkaConsumer
import requests


def consume_from_kafka(topic_name):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    data = []
    for message in consumer:
        data.append(message.value)
        if len(data) >= 1000:  # Example limit
            break

    return data


# Function to read and clean the dataset
def read_and_clean_dataset(data):
    df = pd.DataFrame(data)
    # Drop rows with null values in the specified columns
    df.dropna(subset=['Power Reserve', 'Price (USD)'], inplace=True)

    # Combine the specified columns into a new column 'watch_details'
    df['watch_details'] = df.apply(lambda row: ' '.join([
        str(row['Brand']),
        str(row['Model']),
        str(row['Case Material']),
        str(row['Strap Material']),
        str(row['Movement Type']),
        str(row['Dial Color'])
    ]), axis=1)

    return df


def fetch_embeddings_from_api(text):
    url = "https://api.openai.com/v1/embeddings"  # OpenAI API endpoint
    api_key = "GIVE YOUR API-KEY"
    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        "input": text,
        "model": "text-embedding-ada-002"  # Replace with the model you are using
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()['data'][0]['embedding']
    else:
        print(f"Error fetching embedding for text: {text}")
        return None

def invokeApi(text):
    url = "https://api.openai.com/v1/embeddings"

    payload = json.dumps({
        "input": text,
        "model": "text-embedding-ada-002"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer GIVE YOUR API-KEY',
        'Cookie': '__your cookie key'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()['data'][0]['embedding']
    else:
        print(f"Error fetching embedding for text: {text}")
        return None


# Function to generate embeddings for each text in multiple columns
def generate_embeddings_via_api(df, columns):
    embeddings = []
    for _, row in df.iterrows():
        combined_text = ' '.join([str(row[col]) for col in columns])
        embedding = invokeApi(combined_text)
        if embedding is not None:
            embeddings.append(embedding)
    return embeddings


if __name__ == "__main__":
    # Step 1: Consume data from Kafka
    topic_name = 'quickstart-events'
    data = consume_from_kafka(topic_name)
    print(f"Consumed {len(data)} messages from Kafka topic '{topic_name}'")

    # Step 2: Read and clean the dataset
    df = read_and_clean_dataset(data)
    print("Data read and cleaned.")

    # Step 3: Generate embeddings
    columns_to_embed = ['watch_details']  # Replace with the appropriate column names in your CSV
    embeddings = generate_embeddings_via_api(df, columns_to_embed)
    df['embeddings'] = embeddings
    print("Embeddings generated.")

    # Step 4: Save the DataFrame to a CSV file
    output_file_path = 'output_with_embeddings.csv'
    df.to_csv(output_file_path, index=False)
    print(f"Data with embeddings saved to {output_file_path}")
