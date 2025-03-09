# Basic ETL S3 to Postgresql Pipeline

This project is a basic ETL (Extract, Transform, Load) pipeline that extracts data from an S3 bucket, processes it using Pandas, and loads it into a PostgreSQL database.

## Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <project-directory>
    ```

2. **Create a virtual environment and activate it**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file**:
    Copy the `.env.sample` file to `.env` and fill in the required values.
    ```sh
    cp .env.sample .env
    ```

## Environment Variables

The `.env` file should contain the following variables:

```env
S3_BUCKET_NAME=bucket_name
S3_PREFIX=prefix_if_any

POSTGRES_USERNAME=username
POATGRES_PASSSWORD=password
POSTGRES_DATABASE=database
POSTGRES_HOST=localhost # Change this if needed
POSTGRES_PORT=5432 # Change this if needed
```

## Running the Pipeline

To run the ETL pipeline, execute the following command:

```sh
python etl_pipeline.py
```

## How It Works

1. **Extract**: The `extract_data_from_s3` function connects to the specified S3 bucket and retrieves all CSV files matching the given prefix. It reads these files into Pandas DataFrames and concatenates them into a single DataFrame.

2. **Load**: The `load_to_postgres` function takes the concatenated DataFrame and loads it into a PostgreSQL database table named `sales_transactions`.

3. **Main**: The `main` function loads the environment variables, constructs the PostgreSQL connection string, and calls the extract and load functions.

## Dependencies

- `boto3`: AWS SDK for Python to interact with S3.
- `pandas`: Data manipulation and analysis library.
- `sqlalchemy`: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- `python-dotenv`: Reads key-value pairs from a `.env` file and adds them to environment variables.