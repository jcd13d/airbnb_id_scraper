import pandas as pd


df = pd.read_parquet("/Users/justindiemmanuele/Documents/projects/id_scraper/airbnb_id_scraper/data/output/occ_miami")
print(df.shape)
print(df['id'].drop_duplicates())