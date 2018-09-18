import json
import dateutil.parser

print('\nLoading data from data.txt...')
# Load JSON data
with open('data.txt','r') as file:
    data = json.load(file)

print('\nLoaded ', len(data['articles']), ' articles')

# Access information within the data - showing first 5 for demo purposes
print('\nDisplaying information on the first 5 articles...')
for article in data['articles'][:5]:
    published_datetime = dateutil.parser.parse(article['publishedAt'])

    print('\n')
    print('Source: ', article['source']['name'])
    print('Title: ', article['title'])
    print('Written by: ', article['author'])
    print('Published at:', published_datetime)
    print('URL: ', article['url'])
