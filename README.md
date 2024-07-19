# Kafka


A scalable URL shortener service combined with a Kafka-based data processing pipeline for ingesting, cleaning, and embedding data from CSV files.

## Table of Contents
- [Getting Started](#getting-started)
- [Kafka Installation](#kafka-installation)
- [Using Kaggle Dataset](#using-kaggle-dataset)
- [Starting Kafka](#starting-kafka)
- [Producing and Consuming CSV Files](#producing-and-consuming-csv-files)
- [Data Cleaning and Embedding](#data-cleaning-and-embedding)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features
- URL Shortener Service
  - Shorten long URLs
  - Redirect to original URLs using shortened URLs
  - Track and provide usage statistics for each shortened URL
- Kafka-based Data Processing Pipeline
  - Produce CSV files to Kafka topics
  - Consume CSV files from Kafka
  - Clean and embed data

## Architecture
The system architecture consists of several components working together to provide a scalable URL shortening service and a data processing pipeline using Kafka:

- **API Service**: Handles URL shortening and redirection.
- **Analytics Service**: Tracks and provides usage statistics.
- **Kafka**: Manages the data ingestion pipeline.
- **Data Processing Service**: Consumes, cleans, and processes data from Kafka topics.

![Architecture Diagram](path/to/architecture-diagram.png)

## Tech Stack
- **Backend**: Python
- **Kafka**: Apache Kafka


## Getting Started

### Prerequisites
- Apache Kafka
- Zookeeper


