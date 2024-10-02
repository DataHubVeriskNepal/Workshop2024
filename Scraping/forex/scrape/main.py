from dotenv import load_dotenv
from scraper import ForexScraper

def main():
    load_dotenv()  # Load environment variables
    scraper = ForexScraper()
    scraper.run()

if __name__ == '__main__':
    main()