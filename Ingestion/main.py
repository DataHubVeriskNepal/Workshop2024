import sys
import os
import snowflake_data_loader as Snowflake
import s3_file_downloader as S3FileDownloader


def main():
    """
    entry function to load data from S3 to Snowflake
    """
    # Check if the correct number of arguments are supplied
    if len(sys.argv) != 4:
        print("Invalid number of argument supplied\nUsage: python main.py <data_dir> <batch_size>")
        return
    data_dir = sys.argv[1]
    batch_size = int(sys.argv[2])
    load_lookup = sys.argv[3]

    # Initialize Snowflake and S3 clients
    snowflake = Snowflake.Snowflake(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )

    # get the bucket name and data folder from the environment variables
    bucket_name = os.getenv('S3_BUCKET_NAME')
    data_folder = os.getenv('LOCAL_DATA_FOLDER')

    print(bucket_name,data_folder)
    
    # Load lookup table if load_lookup is set to 'Y'
    if load_lookup.capitalize() == 'Y':
        print("Loading lookup table")
        snowflake.load_lookup_table()
    else:
        print("no")
        # Download files from S3 and load data to Snowflake
        if S3FileDownloader.download_initializer(bucket_name,data_dir):
            snowflake.load_data_to_snowflake(data_dir, batch_size)
        else:
            print("Error downloading files from S3 bucket")


if __name__ == '__main__':
    main()
