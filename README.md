# airbnb_id_scraper

# TODO
## Listing Indexer
* Get code to final V1 deployment state (clean it up)
* decide on initial trial areas for scraping
  * break initial areas into reasonable chunks for distributing 
    the load on aws job

## ID Batch Job Configuration Creator
* Write script to get unique IDs from Listing Index
* Based on configurable batch job size - break those IDs into
  evenly distributed batches of listings to run on each node
* Figure out how to load this into a db on s3 so we can query 
  it for run configuration based on environment index

## ID Based Detail Scraper
* ### Occupancy Scraper
  * decide on storage format/pull frequency
  * Lets say we see one week a listing goes from unbooked to 
    booked... how do we know what price it was booked at?
  * write the code!
* ### Detailed Price Scraper 
  * decide on storage format/pull frequency
  * do we want future prices? how many? 
  * see if any other valuable information in the returned json
  * make parsing of returned json more robust?
  * write the code!
* ### Review Scraper
  * decide on storage format/pull frequency
  * write the code!
* ### Other Scrapers??
  * Amenities?

## Questions
* should we use proxies to request from AWS? Or just run the 
  datacenter proxies to see what happens?
* How do we handle errors when running on aws?
* How implement logs so that they are readable?
* How to analyze errors/counts of errors to know if there is 
  something really wrong with code and not just a random api 
  failure?