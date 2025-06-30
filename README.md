# Scholar Venues Scraper

This is a simple script for scraping all articles from a best venue-group (of one research subject) according to Google Scholar.

*Example:* [Computer Vision and Pattern Recognition](https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_computervisionpatternrecognition)

## How to run:

1. To run the webscraper, first define your wanted parameters in the `scrape_venues.py` file:
```
# Define your parameters ==
url = "https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_computervisionpatternrecognition"   
file_xlsx = 'scholar_cv.xlsx'
wait_time = 5 
# =========================
```

where `url` is the url to the best venue-group to be scraped, `file_xlsx` the save xlsx file for all venues and `wait_time` the time to wait between each request to emulate user behavior (and avoid scholar block).

2. Once you defined your parameters, simply run:
```
python3 scholar_venues.py
```

after a short time, a xlsx file will appear with columns `(Venue Name, Article Name, URL, Citations, Year)`, where `Venue Name` is the name of the venue for the article, `Article Name` the name of the article and `URL` its url. `Authors` are the article authors, `Citations` is the number of citations and `Year` is the publication year.


