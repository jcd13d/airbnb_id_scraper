# airbnb_id_scraper

# TODO
## Listing Indexer
* Get code to final V1 deployment state (clean it up)
* decide on initial trial areas for scraping
  * break initial areas into reasonable chunks for distributing 
    the load on aws job

## ID Based Detail Scraper
* Right now writing parquet in append mode... need to think about 
  paritioning... may need to post process repartition?
* TODO 
  * Think about other errors to catch 
    * simulate malformed input response/other request errors`
    * Index out of bounds error? Some tasks rely on indexing
* ### Occupancy Scraper
  * decide on storage format/pull frequency
    * Storage format - append all data from pull with date it
      was pulled. Post process and remove anywhere the 
      availability switches from the most recent value
  * Lets say we see one week a listing goes from unbooked to 
    booked... how do we know what price it was booked at?
  * write the code!
    * About done i think...
    * need to decide how to append data to bucket, postprocessing, etc
* ### Detailed Price Scraper 
  * decide on storage format/pull frequency
  * do we want future prices? how many? 
  * see if any other valuable information in the returned json
  * make parsing of returned json more robust?
    * For some reason fails ~50% of the time, key we need isnt returned 
      to the json... any way to improve that?
  * second pricing ID
    * setting up to ask for it every time
    * solution would be to create mapping and query databse for it
      each time
  * write the code!
* ### Detailed Price ID scraper
  * Need to pull the weird ID you use to get pricing...
  * This shouldnt change at least... so we can probably pull it
    then join it to the master ID table in a postprocessing script
* ### Review Scraper
  * decide on storage format/pull frequency
  * write the code!
* ### Pricing ID Scraper
* ### Other Scrapers??
  * Amenities?

## Post Processing / Other Scripts
### ID Batch Job Configuration Creator
* Write script to get unique IDs from Listing Index
* Based on configurable batch job size - break those IDs into
  evenly distributed batches of listings to run on each node
* Figure out how to load this into a db on s3 so we can query
  it for run configuration based on environment index
### Join Detailed Pricing ID to Master ID table?
* to avoid having to ping airbnb for it every time? Maybe we can
  just query a db with the mapping?
  * and on error, run the request to get the id again if it changes
    for some reason

## Questions
* should we use proxies to request from AWS? Or just run the 
  datacenter proxies to see what happens?
* How do we handle errors when running on aws?
* How implement logs so that they are readable?
* How to analyze errors/counts of errors to know if there is 
  something really wrong with code and not just a random api 
  failure?

# Notes
* running very slow... huge limitation is proxies when we get a
  bad ip... Also just slower requests I think