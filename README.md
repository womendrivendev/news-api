# :newspaper: News API :chart_with_upwards_trend:

## Table of Contents

1. [Introduction](#one-introduction)
2. [Instructions](#two-instructions)
    - Option 1 - Use pre-collected dataset
    - Option 2 - Run custom queries to collect data
        - Preparing your local environment
        - Customising a query - endpoint
        - Customising a query - parameters
3. [Working with the Data](#three-working-with-the-data)
    - Data structure
    - Loading data from a text file
    - Access information within the data
4. [Contributions](#four-contributions)
5. [Authour](#five-authour)

## :one: Introduction

[News API](https://newsapi.org/) is an amazing source of information as it provides a single API that exposes breaking news headlines and older articles from over 3,000 news sources and blogs!

You can [sign up here](https://newsapi.org/account) for a free developer plan which allows you to make 1,000 requets per day (with a limit of 250 requests per every 6 hours). Please be aware that it _is_ possible to accidentally exceed the limit, e.g. by entering an infinite loop whilst making batch requests... :see_no_evil:

## :two: Instructions

There are two options for you to work on this topic.

### Option 1 - Use pre-collected dataset

We analysed a large number of APIs, hand-picked ones that suited our purpose and have collected ready-to-use dataset in a form of JSON.

In case of News API, we collected English news articles and blog posts that contain the words `gender AND tech`, sorted by the newest articles. The exact query used to collect this data can be found in [`query_everything_endpoint.py`](./query_everything_endpoint.py), and you can find the data in [`news_api_data.txt`](./news_api_data.txt).

You're welcome to download the file (3.4MB) and explore the data. For a detailed explanation of the data structure, how to load the data from the file etc., pelase see the section [:three: Working with the Data](#working-with-the-data).

### Option 2 - Run custom queries to collect data

You can also use the script [`custom_query.py`](./custom_query.py) provided in this directory as well to make your own custom queries, should you wish so.

We use [Requests](http://docs.python-requests.org/en/master/) to make HTTP GET requests to the News API. They actually provide a [Python client](https://github.com/mattlisiv/newsapi-python), which essentially is a wrapper around Requests, but I didn't particularly see the benefit of using it, partially because it doesn't support passing parameters as a dictionary, which would lead to repetitive codes :fearful: Also, this is a great opportunity to learn about Requests if you aren't familiar, as you can make HTTP to any APIs you can think of with Request under your toolbelt. It's a really powerful tool :)

Right, in order to start making queries, you need a bit of preparation to get your local environment up and running.

#### :floppy_disk: Preparing your local environment

1. Clone the repository: `$ git clone git@github.com:womendrivendev/news-api.git`
2. Move into the `news-api` directory: `$ cd mentors-repo/news-api`
3. Create a virtual environment to manage local dependencies: `$ virtualenv venv`
4. Activate the virtual enviromnent just created: `$ source venv/bin/activate`
5. Install dependencies: `$ pip install -r requirements.txt`
6. Obtain a unique API key from [newsapi.org](https://newsapi.org/)
7. Create a `.env` file :exclamation:within:exclamation: the `news-api` directory
    It won't work otherwise, unless you manually change the path to the `.env` file by modifying the `env_path` variable in `custom_query.py`. The file structure should look something like the diagram below.

    ```
    mentors-repo  <-- Project root
    │   README.md
    │   LICENSE
    │   .gitignore  <-- Any .env files are ignored here
    │   ...
    │
    └─── news-api
    │        .env  <-- Here!
    │        README.md
    │        custom_query.py
    │        query_everything_endpoint.py
    │        load_data.py
    │        news_api_data.txt
    │        requirements.txt
    │      ...
    │
    └─── another-project
    │        ...
    │        ...
    │   ...
    ```

    **:closed_book: N.B.** The `.env` file is ignored in `.gitignore` file in the root of the project. This means that it will not get tracked by `git`, and hence will not be checked into your commits. This is important for security purposes, as you _never_ want to expose your credentials to publically available spaces :no_good:

8. Paste your API key to the `.env` file

    ```bash
    # .env

    API_KEY="YOUR API KEY"
    ```

9. Now you should be all ready to fire up a query :boom: `$ python custom_query.py`
    If everything goes well, you should see the response printed out in the console and you should have a file called `data.txt` which stores the JSON data from the News API :100:

#### :wrench: Customising a query - endpoints

By default, `custom_query.py` makes a request to `/everthing` endpoint of News API. They provide two additional endpoints `/top-headlines` and `/sources`. [News API Endpoints](https://newsapi.org/docs/endpoints) explains what each endpoint provides.

You can change the endpoint to query by editing `BASE_URL` constant inside `custom_query.py`.

```python
# custom_query.py

BASE_URL = 'https://newsapi.org/v2/everything'
```

#### :hammer: Customising a query - parameters

You can also customise a query by changing parameters - this is where things get really exciting! So I encourage you to play around with it.

The default parameters in `custom_query.py` are below. You can add/remove parameters by adding/removing key-value pairs in the `params` dictionary.

```python
# custom_query.py

params = {
    'q': 'gender AND tech',
    'apiKey': API_KEY
}
```

For each endpoint, there are a range of additional parameters you can specify, such as `pageSize`, `sources`, `from`, `to`, `language`, `sortBy` etc. For example, for the list of parameters available for the `/everything` endpoint, check out the `Request parameters` section on [News API Everything](https://newsapi.org/docs/endpoints/everything) :point_left:

## :three: Working with the Data

### :page_with_curl: Data structure

The typical JSON response from News API looks like this:

```json
{
    "status": "ok",
    "totalResults": 2,
    "articles": [
        {
            "source": {
                "id": null,
                "name": "Insidehighered.com"
            },
            "author": "Colleen Flaherty",
            "title": "New analysis suggests women's success in STEM Ph.D. programs has much to do with having female peers, especially in their first year in graduate school",
            "description": "Having female peers -- even just a few of them -- can increase a woman\u2019s odds of making it through her Ph.D. program in the natural sciences, technology, engineering or math, says a new working paper from the National Bureau of Economic Research. Based on a s\u2026",
            "url": "https://www.insidehighered.com/news/2018/09/18/new-analysis-suggests-womens-success-stem-phd-programs-has-much-do-having-female",
            "urlToImage": "https://www.insidehighered.com/sites/default/server_files/media/723520409-170667a.jpg",
            "publishedAt": "2018-09-18T07:00:00Z",
            "content": "Having female peers -- even just a few of them -- can increase a woman\u2019s odds of making it through her Ph.D. program in the natural sciences, technology, engineering or math, says a new working paper from the National Bureau of Economic Research. Based on a s\u2026 [+7864 chars]"
        },
        {
            "source": {
                "id": null,
                "name": "Qz.com"
            },
            "author": "Ananya Bhattacharya",
            "title": "Overwhelming evidence why India Inc should hire and promote more women",
            "description": "Women rarely make it to the top in Indian companies, but once they do, they stick. With an attrition rate of just 4%, women are\u2026",
            "url": "https://qz.com/india/1392825/why-india-inc-should-hire-and-promote-more-women/",
            "urlToImage": "https://cms.qz.com/wp-content/uploads/2018/09/RTR3E3E0-e1537216571463.jpg?quality=75&strip=all&w=1400",
            "publishedAt": "2018-09-18T06:23:05Z",
            "content": "Women rarely make it to the top in Indian companies, but once they do, they stick. With an attrition rate of just 4%, women are twice as likely to stay back in their organisations at the C-Suite level, according to a 2018 study by workplace diversity expert A\u2026 [+3163 chars]"
        }
    ]
}
```

The exact structure of the JSON data is described in the `Response object` section on [News API Everything](https://newsapi.org/docs/endpoints/everything) :point_left:

### :open_file_folder: Loading data from a text file

Here is an example of how you can load the file as a JSON object in Python.

```python
import json

with open('news_api_data.txt','r') as file:
    data = json.load(file)
```

### :mag: Access information within the data

Now you can access each field as follows - the below uses `python-dateutil` package to parse the `publishedAt` attribute which is in ISO 8601 format.

```python
import json
import dateutil.parser

with open('news_api_data.txt','r') as file:
    data = json.load(file)

for article in data['articles']:
    published_datetime = dateutil.parser.parse(article['publishedAt'])

    print('\n')
    print('Source: ', article['source']['name'])
    print('Title: ', article['title'])
    print('Written by: ', article['author'])
    print('Published at:', published_datetime)
    print('URL: ', article['url'])
```

`Console output:`

```txt
Source:  Insidehighered.com
Title:  New analysis suggests women's success in STEM Ph.D. programs has much to do with having female peers, especially in their first year in graduate school
Written by:  Colleen Flaherty
Published at: 2018-09-18 07:00:00+00:00
URL:  https://www.insidehighered.com/news/2018/09/18/new-analysis-suggests-womens-success-stem-phd-programs-has-much-do-having-female


Source:  Qz.com
Title:  Overwhelming evidence why India Inc should hire and promote more women
Written by:  Ananya Bhattacharya
Published at: 2018-09-18 06:23:05+00:00
URL:  https://qz.com/india/1392825/why-india-inc-should-hire-and-promote-more-women/

...
```

## :four: Contributions

Please feel free to raise issues or pull requests as you see room for improvement :pray:

## :five: Authour

### Misa Ogura

:computer: Software Engineer @ [BBC R&D](https://www.bbc.co.uk/rd/blog)

Co-founder @ [Women Driven Development](https://womendrivendev.org/)

:rainbow: Organiser @ [AI Club for Gender Minorities](https://www.meetup.com/en-AU/ai-club/)

[Github](https://github.com/MisaOgura) | [Twitter](https://twitter.com/misa_ogura) | [Medium](https://medium.com/@misaogura/latest)
