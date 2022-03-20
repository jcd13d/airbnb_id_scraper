import pandas as pd
import fastparquet as fp
import s3fs

if __name__ == "__main__":

    s3 = s3fs.S3FileSystem()
    fs = s3fs.core.S3FileSystem()

    # pandas_dataframe = fp.ParquetFile('s3://jd-s3-test-bucket9/test_configs/config_review.json', open_with=s3.open).to_pandas()
    # print(pandas_dataframe)
    print(pd.read_parquet('s3://jd-s3-test-bucket9/data/reviews').to_csv("test.csv"))