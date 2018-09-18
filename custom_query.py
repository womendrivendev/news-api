import os
import json
import requests
import dateutil.parser

from dotenv import load_dotenv
from pathlib import Path

# Load environmental variables from .env file - you have to create one yourself!
env_path = Path('./') / '.env'
load_dotenv(dotenv_path=env_path)

# Load the value of API_KEY
API_KEY = os.getenv('API_KEY')

# Set some constants
PAGE_SIZE = 100
BASE_URL = 'https://newsapi.org/v2/everything'

def run():
    # Construct parameters to send
    params = {
        'q': 'gender AND tech',
        'apiKey': API_KEY
    }

    # Get the first set of data from News API with the parameters set above
    print('\nGrabbing articles...')
    response = requests.get(BASE_URL, params=params)

    # Printing status for debugging
    print('Received a response with status code: ', response.status_code)

    # Extract the JSON representation of the response data
    data = response.json()
    print('\nTotal number of articles obtained: ', len(data['articles']))

    # Save the JSON representation of the response data into a file
    print('\nSaving the data into a file...')
    with open('data.txt', 'w') as file:
        json.dump(data, file, indent=4)

    # Load the JSON data
    print('\nLoading data...')
    with open('data.txt','r') as file:
        data = json.load(file)
    print('\nLoaded ', len(data['articles']), ' articles')

    # Access information within the data - showing first 5 for demo purposes
    print('\nDisplaying information of the first 5 articles...')
    for article in data['articles'][:5]:
        published_datetime = dateutil.parser.parse(article['publishedAt'])

        print('\n')
        print('Source: ', article['source']['name'])
        print('Title: ', article['title'])
        print('Written by: ', article['author'])
        print('Published at:', published_datetime)
        print('URL: ', article['url'])

if __name__ == '__main__':
    run()
