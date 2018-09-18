import os
import sys
import json
import requests
import datetime

from dotenv import load_dotenv
from pathlib import Path

env_path = Path('./') / '.env'
load_dotenv(dotenv_path=env_path)

class NewsApi():
    def __init__(self, endpoint, output_filename, **kwargs):
        self._base_url = 'https://newsapi.org/v2/{}'.format(endpoint)
        self._output_filename = output_filename
        self._params = {**kwargs, 'apiKey': os.getenv('API_KEY')}

        self._data = {'custom_params': {**kwargs},
                      'datetime': str(datetime.datetime.now()),
                      'total_articles': 0}

    def _query(self, current_page):
        print('\nGrabbing page: {}...'.format(current_page))

        self._params['page'] = current_page

        response = requests.get(self._base_url, params=self._params)

        if response.status_code != 200:
            print('\nRequest failed with a status code: {}'.format(response.status_code))
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
        page_size = 20

        if 'pageSize' in self._params:
            page_size = self._params['pageSize']

        if total_result <= 100:
            return 1
        elif total_result % page_size == 0:
            return total_result / page_size
        else:
            return int(total_result / page_size) + 1

    def _save(self):
        total_articles = len(self._data['articles'])

        print('\nSaving the data into a file...')
        print('\nTotal number of articles obtained: ', total_articles)

        self._data['total_articles'] = total_articles

        with open(self._output_filename, 'w') as file:
            json.dump(self._data, file, indent=4)

        print('\nData saved in {}!'.format(self._output_filename))

    def _main(self):
        current_page = 1
        response = self._query(current_page)

        total_result = response['totalResults']
        total_page = self._calculate_total_page(total_result)

        self._data = {**self._data, 'articles': response['articles']}

        print('\nTotal number of pages to paginate: {}'.format(total_page))

        while current_page < total_page:
            current_page += 1
            response = self._query(current_page)

            self._data['articles'].extend(response['articles'])

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

def create_params_from_input(keys):
    params = {}

    for key in keys:
        value = input('Enter a value for "{}": '.format(key))

        if value != '':
            if key == 'pageSize':
                params[key] = int(value)
            else:
                params[key] = value

    return params

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: news_api.py <endpoint> <output_filename>')
        print('e.g. news_api.py everything test.txt')
        exit(1)

    endpoint = sys.argv[1]
    output_filename = sys.argv[2]

    if os.path.exists(output_filename):
        print('The file {} already exists. Please provide another filename.'.format(output_filename))
        exit(1)

    params = {}

    if endpoint == 'everything':
        keys = ['q',
                'sources',
                'domains',
                'from',
                'to',
                'language',
                'sortBy',
                'pageSize']

    elif endpoint == 'top-headlines':
        keys = ['q',
                'sources',
                'category',
                'language',
                'country',
                'pageSize']

    print('\nConstructing query parameters for /{} endpoint...'.format(endpoint))
    print('Documentation (default/available values etc.): https://newsapi.org/docs/endpoints/{}\n'.format(endpoint))

    params = create_params_from_input(keys)

    NewsApi(endpoint, output_filename, **params).execute()
