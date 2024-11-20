@echo off
REM Set environment variables for Snowflake connection
set SNOWFLAKE_USER=sujankhyaju
set SNOWFLAKE_PASSWORD=Snowfl@ke1234
set SNOWFLAKE_ACCOUNT=ABURMXV-BQ11501
set SNOWFLAKE_WAREHOUSE=COMPUTE01_WH
set SNOWFLAKE_DATABASE=DEMO_DB
set SNOWFLAKE_SCHEMA=public
set LOOKUP_FILE=formatted_dates.csv


REM Set environment variables for aws
set S3_BUCKET_NAME=workshop20241001
set AWS_ACCESS= AKIA6GBMFPXGE3I2DN4Z
set AWS_SECRET= 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
set LOCAL_DATA_FOLDER=data

REM Execute the Python script with arguments
python main.py %1 %2 %3

REM Clear environment variables after script execution
set SNOWFLAKE_USER=
set SNOWFLAKE_PASSWORD=
set SNOWFLAKE_ACCOUNT=
set SNOWFLAKE_WAREHOUSE=
set SNOWFLAKE_DATABASE=
set SNOWFLAKE_SCHEMA=