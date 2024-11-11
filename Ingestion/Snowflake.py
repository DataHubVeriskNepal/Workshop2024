import snowflake.connector
import os
import pandas as pd
import csv
import shutil


class Snowflake:
    def __init__(self, user, password, account, warehouse, database, schema):
        try:
            self.ctx = snowflake.connector.connect(
                user=user,
                password=password,
                account=account,
                warehouse=warehouse,
                database=database,
                schema=schema,
                ocsp_fail_open=False  # Disable OCSP
            )
            print("Connection successful")
            print(f"Connection ID: {self.ctx.session_id}")
            print(f"Database: {self.ctx.database}")
            print(f"Warehouse: {self.ctx.warehouse}")
        except Exception as e:
            print(f"Connection to Snowflake failed: {e}")
            raise

    def load_lookup_table(self):
        lookup_file = os.environ.get("LOOKUP_FILE")
        if not lookup_file:
            print("LOOKUP_FILE environment variable is not set")
            return

        try:
            with open(lookup_file, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file)
                rows = [(row[0], row[1]) for row in csv_reader]

            insert_query = 'INSERT INTO Date_Lookup (bs_date, ad_date) VALUES (%s, %s)'
            with self.ctx.cursor() as cursor:
                cursor.executemany(insert_query, rows)
            print("Lookup table loaded successfully")
        except Exception as e:
            print(f"Failed to load lookup table: {e}")

    def get_date_lookup(self, min_date, max_date):
        try:
            lookup_query = f"""
                SELECT bs_date, ad_date 
                FROM Date_Lookup 
                WHERE bs_date >= '{min_date}' AND bs_date <= '{max_date}'
            """
            print(lookup_query)
            with self.ctx.cursor() as cursor:
                cursor.execute(lookup_query)
                lookup_dict = {row[0]: row[1] for row in cursor.fetchall()}
            return lookup_dict
        except Exception as e:
            print(f"Failed to fetch date lookup: {e}")
            return {}

    def load_data_to_snowflake(self, base_data_dir, batch_size=1000):
        try:
            for subdir, _, files in os.walk(base_data_dir):
                table_name = os.path.basename(subdir)
                if not files:
                    continue

                for file_name in files:
                    if file_name.endswith('.csv'):
                        file_path = os.path.join(subdir, file_name)
                        df = pd.read_csv(file_path)

                        # Get min and max dates from the file
                        min_date = df.date.min()
                        max_date = df.date.max()

                        # Fetch lookup dates within the range
                        
                        #make it generic to handle all files
                        if not file_name.startswith('forex'):                        
                           lookup_dict = self.get_date_lookup(min_date, max_date)
                           # Replace dates using the lookup dictionary
                           for col in df.columns:                            
                            df[col] = df[col].apply(lambda x: lookup_dict.get(x, x))
                        
                        # Handle null values
                        df.fillna('NULL', inplace=True)
                        columns = df.columns

                        # Load data into the table in batches
                        for start in range(0, len(df), batch_size):
                            batch_df = df.iloc[start:start + batch_size]
                            values = [tuple(row) for row in batch_df.to_numpy()]
                            insert_query = f'INSERT INTO "{table_name}" VALUES ({", ".join(["%s"] * len(columns))})'
                            with self.ctx.cursor() as cursor:
                                cursor.executemany(insert_query, values)
                        print(f"Data loaded into table '{table_name}' successfully")

                        # Move the processed file to the archive folder outside the data folder
                        archive_dir = os.path.join(os.path.dirname(base_data_dir), 'archive', table_name)
                        os.makedirs(archive_dir, exist_ok=True)
                        shutil.move(file_path, os.path.join(archive_dir, file_name))
                        print(f"File '{file_name}' moved to archive")

        except Exception as e:
            print(f"Failed to load data from nested folders: {e}")