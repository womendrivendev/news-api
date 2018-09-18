import os
import sys
import json
import requests
import datetime

from dotenv import load_dotenv
from pathlib import Path

# Load environmental variables from .env file

env_path = Path('./') / '.env'
load_dotenv(dotenv_path=env_path)

class NewsApi():
    def __init__(self, query_term, output, endpoint='everything'):
        self._api_key = os.getenv('API_KEY')
        self._pagesize = 100
        self._base_url = 'https://newsapi.org/v2/{}'.format(endpoint)

        self._output = output

        self._data = {'query_term': query_term,
                      'datetime': str(datetime.datetime.now()),
                      'total_articles': 0}

        self._params = {'q': query_term,
                        'apiKey': self._api_key,
                        'pageSize': self._pagesize,
                        'language': 'en',
                        'sortBy': 'publishedAt'}

    def _query(self, current_page):
        print('\nGrabbing page: {}...'.format(current_page))

        self._params['page'] = current_page

        response = requests.get(self._base_url, params=self._params)

        if response.status_code != 200:
            print('\nRequest failed with: ', response.status_code)
            print('\nDetails: ', response.text)
            self._cleanup()
        else:
            data = response.json()

            if 'articles' not in data:
                print('Could not retrieve any articles...')
                self._cleanup()
            else:
                return data

    def _calculate_total_page(self, total_result):
        if total_result <= 100:
            return 1
        elif total_result % self._pagesize == 0:
            return total_result / self._pagesize
        else:
            return int(total_result / self._pagesize) + 1

    def _save(self):
        total_articles = len(self._data['articles'])

        print('\nSaving the data into a file...')
        print('\nTotal number of articles obtained: ', total_articles)

        self._data['total_articles'] = total_articles

        with open(self._output, 'w') as file:
            json.dump(self._data, file, indent=4)

        print('\nData saved in {}!'.format(output_file))

    def _main(self):
        current_page = 1

        response = self._query(current_page)

        total_result = response['totalResults']
        total_page = self._calculate_total_page(total_result)

        self._data = {**self._data, 'articles': response['articles']}

        print('\nTotal number of pages to paginate: {}'.format(total_page))

        while current_page < total_page:
            # Obtain next page from the API

            current_page += 1
            new_data = self._query(current_page)

            # Merge new articles to the obtained list of articles

            self._data['articles'].extend(new_data['articles'])

        self._save()

    def _cleanup(self):
        self._save()
        sys.exit(1)

    def execute(self):
        try:
            self._main()
        except KeyboardInterrupt:
            print('\nDetected SIGINT!!!')
            self._cleanup()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: news_api.py <query_term> <output_file>')
        print('e.g. news_api.py "gender AND tech" my_data.txt')
        exit(1)
    else:
        query = sys.argv[1]
        output_file = sys.argv[2]

        NewsApi(query, output_file).execute()
