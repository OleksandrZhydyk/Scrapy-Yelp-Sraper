# Scrapy Yelp.com Scraper

The scraper gathers info about contractors by categories and locations.

## Prerequisites
- For the scraper interaction with browser you need to required driver (Chrome, Firefox, etc)
- To be allowed parse the site you also need to add your `proxy server`. In this example, we use `srapeops` proxy. When you get your `API key` please add it to the `.env` file in the root, under name `SCRAPEOPS_API_KEY`.


## Usage
- To retrieve available contractors' categories run the command:
```sh 
   cd yelp_parser/yelp_parser &&
   scrapy crawl get_categories -O data/get_categories/categories.json
 ```

- To get an info by specific category or location:
```sh 
   cd yelp_parser/yelp_parser &&
   scrapy crawl yelp -a category=restaurants -a location='New York, NY'
 ```

- To get all contractors, from all categories and all locations run: 
```sh 
   cd yelp_parser/yelp_parser &&
   scrapy crawl yelp
 ```
