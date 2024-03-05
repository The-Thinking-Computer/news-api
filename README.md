# news-api

The `news-api` is a modular application designed for scraping and processing news articles into structured data.

## operation

The application runs in cycles, scraping news websites and processing articles into a structured format, then stored.

**Cycle**

1. `scraper.py` creates new Website object and grabs the latest articles
2. `post_process.py` handles processing the scraped articles/checks domain
3. `categorizer.py` categorizes articles
4. processed website scrapes get dumped into `\data\` as .json files

[Click here](https://drive.google.com/open?id=17x-F9UhgHQGtzpG6EbO9pZ9Y2ckS-wTu&usp=drive_fs) to watch Ben demonstrate how the api works.

## structure

- api
- data
- jobs
- scraper (_Website_ class defined in `scraper.py`)
- site
  - \controllers (routes)
  - \templates (AI generated to test data)
