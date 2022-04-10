# airbnb_id_scraper

# TODO
## Listing Indexer
* Get code to final V1 deployment state (clean it up)
* decide on initial trial areas for scraping
  * break initial areas into reasonable chunks for distributing 
    the load on aws job
* where do we want to pull? how frequently? set up AWS job?
## Proxies
* run benchmarks for how many proxies dont work etc, how long to wait
  * ~41% of proxies failed in benchmark
* see if benchmark matches what we see in practice, if not we may need 
  vary the headers etc
  * Actually see less failure in practice... interesting
* Quick run with  my IP and no timeouts, try on AWS so we dont care if IP blocked
* Add variables that track types of failures in scraper class, output
  stats at the end of run 
* So far good results no blockage for airbnb scraper by id tested for 300 ids at a time

## Headers

## ID Based Detail Scraper
* Better logging
* Figure out frequency of pricing pull and build into config easily
* Is running with public IP the right way to do it? 
  * needs to be able to reach ECR and make requests outbound
* how do we know if it fails? What kind of checks can we run? 
  how do we get notified if everything starts failing?

* ### Occupancy Scraper
  * decide on storage format/pull frequency
    * Storage format - append all data from pull with date it
      was pulled. Post process and remove anywhere the 
      availability switches from the most recent value
  * Lets say we see one week a listing goes from unbooked to 
    booked... how do we know what price it was booked at?
    * Need to have price for that listing on that day...
  * need dynamic change of month when new month hits year etc
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
* ### Detailed Price ID scraper
  * Need to pull the weird ID you use to get pricing...
  * This shouldnt change at least... so we can probably pull it
    then join it to the master ID table in a postprocessing script
* ### Review Scraper
  * decide on storage format/pull frequency
  * How many reviews to pull each time? how to only get new ones? how 
    frequently should we pull? (probably not very)
  * we end up getting a weird error where it seems like we get an inconsistant
    schema or something... json error in loading columns when writing parquet idk
  * write the code!
* ### Other Scrapers??
  * Amenities?

## Post Processing / Other Scripts
## Config Creator
* Using the indexing data, create configs that are run for ID scrapers
  * knob for number of IDs per container 
  * handle how frequently and far into future to pull pricing data
### Post Process Loading of ID Scraper data
* When we scrape, we need to write to individual s3 buckets because there are
  collisions if we try to write to the same file (maybe there is a solution to this
  but I couldn't figure it out..). 
* Read all the data in scraper "temp" directory and append to prod directory with 
  appropriate partitions etc. 
  * make sure to watch out for corruption of the dataset, we need to ensure types 
    are consistant etc. 
* Process occupancy data to only keep rows that show a switch in occupancy or the 
  first row of occupancy pull
* Figured this out with EMR, but maybe we should just use pandas and iterate
  through files if this is feasible to start (EMR is expensive)
### ID Batch Job Configuration Creator
* Write script to get unique IDs from Listing Index
* Based on configurable batch job size - break those IDs into
  evenly distributed batches of listings to run on each node
* Figure out how to load this into a db on s3 so we can query
  it for run configuration based on environment index
  * think we should table this for now
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
* need indexer script running in some frequency
  * what areas do we want to pull
  * how frequent
* Need script to pull unique IDs and make config scripts for ID scrapers
  * read id scraper data
  * drop duplicates/take only last pull? (do we need to keep a time series here?)
  * create configs based on some inputs (number nodes in job, how many prices at 
    what time in future etc)
* Pricing data frequency
* NEED TO ADD MULTI CONFIG SUPPORT


# Postprocess Notes
## Occupancy
* drop rows where change in occupancy 
* how to do this without having to check every row in the whole dataset?
  * can only look at prev year if we are pulling a year fwd?


# TODO 0406
* dynamic date config occupancy - month we are in fwd
* easy config number of days into future to pull for listings
  * if it is multi config, need to fix loop in scraper.py
* how many dates in future to pull, skip days? pull all for a sample? 
* figure out initial locations to pull/how many listings we should start with 
  * get script that will at some freq create configs based on index table
* clean up logging in ID scraper
* Get index scraper to final state
* How to run EMR on a schedule? Probably lambda
* Figure out DB issues with Review scraper, get that running on a lower 
  frequency

# Indexer TODO
* George
* Trigger by EventBridge rule?

# Config Generator
* Could be a lambda function that then kicks off the ID scraper after
  creating configs
  * but id_config might be emr?

# ID Scraper TODO
* date configuration for occupancy, price, ability to pull many days of pricing
* improve logging
* get a config creation job that the scraping job would be dependent on?
  * can also just run it earlier before this runs
* Trigger by EventBridge Rule? OR kick off from lambda that creates the configs

# Postprocessing
* DECIDE IF THESE SHOULD BE EMR OR PANDAS ON EC2/LAMBDA/FARGATE
* Trigger by EventBridge rule, can be lower freq then ID scraper since it 
  can get a bunch of runs at once 