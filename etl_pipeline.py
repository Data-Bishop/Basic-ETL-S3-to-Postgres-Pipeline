from io import StringIO
from dotenv import load_dotenv
import boto3
import pandas as pd
import sqlalchemy
import os

def extract_data_from_s3(bucket_name, prefix):
    
    # Defining this empty list to store each dataframe
    dataframes = []
    
    # Initializing the S3 client and listing all the objects in the bucket
    s3_client = boto3.client("s3")
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    # Getting each csv object in the bucket
    for obj in response.get("Contents", []):
        if obj["Key"].endswith(".csv"): # Checks if the object key ends with a .csv
            obj = s3_client.get_object(Bucket=bucket_name, Key=obj["Key"])
            body = obj["Body"].read().decode("utf-8")
            body_buffer = StringIO(body)
            dataframe = pd.read_csv(body_buffer)
            dataframes.append(dataframe)
            
    # Concatenate all the dataframes
    concatenated_dataframe = pd.concat(dataframes, ignore_index=True)
    return concatenated_dataframe

def load_to_postgres(dataframe, connection_string):
    engine = sqlalchemy.create_engine(connection_string)
    
    # Loads the data into postgresql
    dataframe.to_sql("sales_transactions", engine, if_exists="append")
    
def main():
    load_dotenv()
    
    bucket_name = os.getenv("S3_BUCKET_NAME")
    prefix = os.getenv("S3_PREFIX")
    
    # Postgres Configurations
    username = os.getenv("POSTGRES_USERNAME")
    passwprd = os.getenv("POATGRES_PASSSWORD")
    database = os.getenv("POSTGRES_DATABASE")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    
    connection_string = f"postgresql://{username}:{passwprd}@{host}:{port}/{database}"

    extracted_data = extract_data_from_s3(bucket_name, prefix)
    load_to_postgres(extracted_data, connection_string)
    
    print("Pipeline Successful")
    
if __name__ == "__main__":
    main()