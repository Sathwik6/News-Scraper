import sys
import os

# Append the producer directory to the system path
sys.path.append('/app/kafka/producer')

from cbs_producer import produce_cbs_data
from cbs_scraper import scrape_cbs

source = 'cbs'
fields = ['us', 'world', 'politics', 'healthwatch', 'moneywatch', 'entertainment', 'crime', 'sports', 'essentials']

if __name__ == "__main__":
    data_list = scrape_cbs(fields, source)
    print("Scraped Data:")
    for data in data_list:
        print(data)
    produce_cbs_data(data_list)
