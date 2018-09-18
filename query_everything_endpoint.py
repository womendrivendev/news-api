import os
import json
import requests
import sys

from dotenv import load_dotenv
from pathlib import Path

# Load environmental variables from .env file

env_path = Path('./') / '.env'
load_dotenv(dotenv_path=env_path)

# Load the value of API_KEY

API_KEY = os.getenv('API_KEY')

# Set some constants

PAGE_SIZE = 100
BASE_URL = 'https://newsapi.org/v2/everything'


def run():
    # Get parameter from stdin
    query = sys.argv[1]

    print(query)

    # Construct parameters to send

    params = {
        'q': query,
        'language': 'en',
        # 'country': 'gb',  # only supported by the headline endpoint
        'apiKey': API_KEY,
        'sortBy': 'publishedAt',
        'pageSize': PAGE_SIZE,
        'page': 1,
    }

    # Get the first set of data from News API with the parameters set above

    print('\nGrabbing the first page...')
    response = requests.get(BASE_URL, params=params)

    # Printing the status code for debugging

    print('Received a response with status code: ', response.status_code)

    # Extract the JSON representation of the response data

    data = response.json()

    # Calculate total number of pages to paginate through

    total_results = data['totalResults']
    total_pages = calculate_total_pages(PAGE_SIZE, total_results)
    print('Total number of pages to paginate: ', total_pages, '\n')

    # Grab the rest of the articles by paginating 100 articles at a time

    current_page = 1
    while current_page < total_pages:
        # Increment current_page and set it to the page param

        current_page += 1
        params['page'] = current_page

        # Obtain next page from the API

        print('\nGrabbing page: ', current_page, '...')
        response = requests.get(BASE_URL, params=params)

        # Printing status for debugging

        print('Received a response with status code: ', response.status_code)

        # Breaks out from the while loop if the request fails

        new_data = response.json()
        if 'articles' not in new_data:
            break

        # Merge new articles to the obtained list of articles

        new_articles = new_data['articles']
        data['articles'].extend(new_articles)

    print('\nTotal number of articles obtained: ', len(data['articles']))

    # Save the data into a file

    print('\nSaving the data into a file...')
    with open('news_api_data.txt', 'w') as file:
        json.dump(data, file, indent=4)
    print('\nData saved as news_api_data.txt!')


def calculate_total_pages(page_size, total_results):
    if total_results <= 100:
        return 1
    elif total_results % PAGE_SIZE == 0:
        return total_results / PAGE_SIZE
    else:
        return int(total_results / PAGE_SIZE) + 1


if __name__ == '__main__':
    run()
