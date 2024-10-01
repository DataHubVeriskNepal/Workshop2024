import csv
import os
from datetime import datetime

class CSVHandler:
    def __init__(self, date):
        # Convert the date string to a datetime object
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.filename = f'forex_{self.date.strftime("%Y_%m")}.csv'
        
        # Create a directory for CSV files if it doesn't exist
        os.makedirs('forex', exist_ok=True)
        
        self.filepath = os.path.join('forex', self.filename)

        # Open the file in append mode and write header if the file is new
        try:
            self.file = open(self.filepath, mode='a', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file)
            if os.stat(self.filepath).st_size == 0:  # Write header if file is empty
                self.writer.writerow(['date', 'currency', 'buy', 'sell', 'unit'])  # Header row
        except Exception as e:
            print(f'Error opening CSV file: {e}')
            self.file = None

    def write_row(self, row_data):
        if self.file is not None:
            try:
                self.writer.writerow(row_data)
                self.file.flush()  # Immediate flush to disk for visibility
            except Exception as e:
                print(f'Error writing row to CSV: {e}')

    def close(self, s3_uploader):
        if self.file is not None:
            try:
                self.file.close()
                # Upload the CSV file to S3 after closing
                s3_file = f'forex/{self.filename}'  # S3 key
                s3_uploader.upload_file(self.filepath, s3_file)
            except Exception as e:
                print(f'Error closing CSV file: {e}')
