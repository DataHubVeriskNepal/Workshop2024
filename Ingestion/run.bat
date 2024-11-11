@echo off
REM Set environment variables for Snowflake connection
set SNOWFLAKE_USER=sushanshakya
set SNOWFLAKE_PASSWORD=Verisk123
set SNOWFLAKE_ACCOUNT=XONCIZQ-CT07153
set SNOWFLAKE_WAREHOUSE=COMPUTE_WH
set SNOWFLAKE_DATABASE=DEMO_DB
set SNOWFLAKE_SCHEMA=public
set LOOKUP_FILE=formatted_dates.csv


REM Set environment variables for aws
set S3_BUCKET_NAME=workshop20241001
set AWS_ACCESS=
set AWS_SECRET=
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