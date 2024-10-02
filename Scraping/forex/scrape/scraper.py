import requests
import re
from bs4 import BeautifulSoup
from csv_handler import CSVHandler
from s3_uploader import S3Uploader

class ForexScraper:
    def __init__(self):
        self.base_url = 'https://nvforex.pages.dev/'
        self.s3_uploader = S3Uploader()
        self.csv_handler = None  # Initialize without any active CSV handler
        self.current_month = None  # Track the current month being processed

    def run(self):
        try:
            # Fetch the base URL
            response = requests.get(self.base_url, verify=False)
            response.raise_for_status()  # Raise an error for bad responses
            print('Successfully fetched the webpage!')
            self.parse_links(response.text)
            # Ensure to close and upload the last month's file
            self.close_and_upload_csv_handler()
        except requests.exceptions.RequestException as e:
            print(f'Error fetching the homepage: {e}')

    def parse_links(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            view_rates_links = soup.find_all('a', text='View Rates')

            for link in view_rates_links:
                href = link.get('href')
                full_url = self.base_url + href

                # Extract the date from the full_url
                date = re.search(r'/(\d{4}-\d{2}-\d{2})/', full_url).group(1)
                self.handle_month_transition(date)
                self.fetch_rates_page(full_url, date)

        except Exception as e:
            print(f'Error parsing links: {e}')

    def handle_month_transition(self, date):
        """Check if the month has changed and handle file closing and opening accordingly."""
        new_month = date[:7]  # Extract 'YYYY-MM' from the date

        if self.current_month is None:
            self.current_month = new_month  # First month initialization
        elif self.current_month != new_month:
            # If the month has changed, close and upload the previous month's file
            print(f"Transitioning to new month: {new_month}, closing previous month: {self.current_month}")
            self.close_and_upload_csv_handler()
            self.current_month = new_month  # Update the current month to the new month

    def close_and_upload_csv_handler(self):
        """Close the current CSV handler and upload the file to S3 if open."""
        if self.csv_handler:
            self.csv_handler.close(self.s3_uploader)
            self.csv_handler = None  # Reset the handler after uploading

    def fetch_rates_page(self, full_url, date):
        try:
            rates_response = requests.get(full_url, verify=False)
            rates_response.raise_for_status()  # Raise an error for bad responses
            print(f'Successfully fetched the View Rates page at {full_url}')
            self.extract_data(rates_response.text, date)
        except requests.exceptions.RequestException as e:
            print(f'Error fetching the View Rates page at {full_url}: {e}')

    def extract_data(self, html_content, date):
        try:
            rates_soup = BeautifulSoup(html_content, 'lxml')
            table = rates_soup.find('table')
            
            if table:
                if not self.csv_handler:
                    self.csv_handler = CSVHandler(date)  # Create a CSVHandler for the current month

                for row in table.find_all('tr'):
                    columns = row.find_all('td')
                    row_data = [col.text.strip() for i, col in enumerate(columns) if i != 1]
                    row_data.insert(0, date)  # Prepend the date to the row data
                    if len(row_data) > 1:  # Check if there's valid data
                        self.csv_handler.write_row(row_data)
            else:
                print(f'No table found on the page.')

        except Exception as e:
            print(f'Error extracting data: {e}')
