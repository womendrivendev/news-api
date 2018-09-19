# :newspaper: News API :chart_with_upwards_trend:

## Table of Contents

1. [Introduction](#one-introduction)
2. [Instructions](#two-instructions)
    - Option 1 - Use pre-collected dataset
    - Option 2 - Run custom queries to collect data
        - Preparing your local environment
        - Customising a query
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

I've made some queries and collected a ready-to-use dataset in a JSON format, which you can find in [`data.txt`](./data.txt).

It contains English news articles and blog posts that match the query term `(women OR gender OR minotiry OR gap) AND tech`, sorted by the relevancy.

You're welcome to download the file (~1MB) and explore the data. For example, you could use the link provided in each article to do a bit of web scraping, analyse what's being said with natural language processing tools and visualise the results.

For a detailed explanation of the data structure, how to load the data from the file etc., pelase see the section [Working with the Data](#working-with-the-data).

### Option 2 - Run custom queries to collect data

You can also use the script [`news_api.py`](./news_api.py) to make customised queries, should you wish so. It uses [Requests](http://docs.python-requests.org/en/master/) under the hood to make HTTP GET requests to the News API endpoints.

In order to start making queries, you need a bit of preparation to get your local environment up and running.

#### :floppy_disk: Preparing your local environment

1. Clone the repository

    ```bash
    $ git clone git@github.com:womendrivendev/news-api.git
    ```

2. Move into the `news-api` directory: `$ cd news-api`
3. Create a virtual environment to manage local dependencies: `$ virtualenv venv` (make sure you have `virtualenv` installed: [documendation](https://virtualenv.pypa.io/en/stable/installation/))
4. Activate the virtual enviromnent just created: `$ source venv/bin/activate`
5. Install dependencies: `$ pip install -r requirements.txt`
6. Obtain a unique API key from [newsapi.org](https://newsapi.org/)
7. Create a `.env` file under the `news-api` directory
    It won't work otherwise, unless you manually change the path to the `.env` file by modifying the `env_path` variable in `news_api.py`. The file structure should look something like the diagram below.

    ```txt
    news-api/
        .env  <-- Here!
        .gitignore
        README.md
        news_api.py
        load_data.py
        data.txt
        requirements.txt
        ...
    ```

    **:exclamation:IMPORTANT:exclamation:** The `.env` file is _ignored_ in `.gitignore` file in the root of the project. This means that it will not get tracked by `git`, and hence will not be checked into your commits. This is important for security purposes, as you _never_ want to expose your credentials to publically available spaces :no_good:

8. Paste your API key to the `.env` file

    ```bash
    # .env

    API_KEY="YOUR API KEY"
    ```

9. Now you're ready to make a customised query using `news_api.py` :boom:

    ```bash
    Usage: news_api.py <endpoint> <output_filename>

    e.g. $ python news_api.py everything test.txt
    ```

    You have to provide both `<endpoint>` and `<output_filename>`. In the next section I explain how to use it in detail.

#### :wrench: Customising a query

The News API provides **two endpoints** for quering articles: `top-headlines` and `everything`. [News API Endpoints](https://newsapi.org/docs/endpoints) explains what each endpoint is best used for. Once you specify the `<endpoint>`, the script will enter an interactive mode for you to set query parameters.

Depending on the endpoint you are using i.e. `top-headlines` or `everything`, there are different sets of parameters you can customise. You can see all the available parameters and their default values here: [News API Everything](https://newsapi.org/docs/endpoints/everything), [News API Top headlines](https://newsapi.org/docs/endpoints/top-headlines).

Below is an example of using the script, where I set the endpoint to `everything`.

```txt
$ python news_api.py everything test.txt

Constructing query parameters for /everything endpoint...
Documentation (default/available values etc.): https://newsapi.org/docs/endpoints/everything

Press Enter to leave the parameter as a default value.
Enter a value for "q":
...
```

## :three: Working with the Data

### :page_with_curl: Data structure

The script saves data in a JSON format.

`custom_params`: a dictionary of parameters you customised

`datetime`: date & time the query was made

`total_articles`: number of articles collected

`articles`: a list of articles that matched your query

```json
{
    "custom_params": {
        "q": "gender AND technology",
        "language": "en",
        "pageSize": 100
    },
    "datetime": "2018-09-18 21:23:29.426768",
    "total_articles": 2,
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

### :open_file_folder: Loading data from a text file

Here is an example of how you can load the file as a JSON object in Python.

```python
import json

with open('data.txt','r') as file:
    data = json.load(file)
```

### :mag: Access information within the data

I've created another script ([`load_data.py`](./load_data.py)) to make a quick inspection of the data easier. It uses `python-dateutil` package to parse the `publishedAt` attribute which is in ISO 8601 format.

```bash
Usage: load_data.py <filename>

e.g. $ python load_data.py data.txt
```

```txt
$ python load_data.py data.txt

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

## :five: Author

### Misa Ogura

:computer: Software Engineer @ [BBC R&D](https://www.bbc.co.uk/rd/blog)

:rainbow: Co-founder @ [Women Driven Development](https://womendrivendev.org/)

[Github](https://github.com/MisaOgura) | [Twitter](https://twitter.com/misa_ogura) | [Medium](https://medium.com/@misaogura/latest)
