# news-api

The `news-api` is a modular application designed for scraping and processing news articles into structured data.

## operation

The application runs in cycles, scraping news websites and processing articles into a structured format, then stored.

**Cycle**

Please note that all these steps currently take place in general or as written.

1. `/scraper/scraper.py` creates new Website object and grabs the latest articles. This is where scraaper functions for individual websites are stored.
2. `'scraper/post_process.py` processes the articles and returns structured data in JSON format, written into the /data folder.
3. `/api/categorizer.py` categorizes articles using the most recent file in /data. A Laten-Derelicht-Allocation algorithm is employed using gensim. 
4. `/api/__init__.py` API starts up *or* verifies access to the most recent data file at the /v1/articles/today endpoint
5. `/site/run.py` Website starts up *or* runs test to ensure that the most recent news at /v1/articles/today can be consumed and displayed on a webpage.

[Click here](https://drive.google.com/open?id=17x-F9UhgHQGtzpG6EbO9pZ9Y2ckS-wTu&usp=drive_fs) to watch Ben demonstrate how the api works.

## structure

- api (verifies and serves data for consumption by web application(s))
- data (store of data in JSON files. The goal is to have this data added to SQL databaase after it's processed, for more efficient consumption)
- scraper (stores files related to web scraping. Scraping functions stored in scraper.py along with Website class)
- site (consumes data from the API and displays it on webpage)
  - \controllers (route functions that consume data)
  - \templates 
- jobs (will call each of these modules to run the website, api, and data processing independently)
