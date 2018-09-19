import json
import sys
import dateutil.parser

if len(sys.argv) != 2:
    print('\nUsage: load_data.py <filename>')
    print('e.g. python load_data.py test.txt')
    exit(1)

filename = sys.argv[1]

print('\nLoading data from {}...'.format(filename))

# Load data as JSON

with open(filename,'r') as file:
    data = json.load(file)

print('\nFound {} articles in total'.format(len(data['articles'])))

# Access information within the data - showing first 5 for demo purposes

print('\nDisplaying information on the first 5 articles...')

for article in data['articles'][:5]:
    published_datetime = dateutil.parser.parse(article['publishedAt'])

    print('\nSource: ', article['source']['name'])
    print('Title: ', article['title'])
    print('Written by: ', article['author'])
    print('Published at:', published_datetime)
    print('URL: ', article['url'])
