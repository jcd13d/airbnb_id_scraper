import pandas as pd


if __name__ == "__main__":
    path = "s3://jd-s3-test-bucket9/data/occupancy_3/by_pull/array_4/20220321025057/"
    path = "s3://jd-s3-test-bucket9/data/occupancy_3/by_pull/array_4"
    path = "s3://jd-s3-test-bucket9/data/occupancy_3/by_pull"
    # TODO really slow probably because we are paritioning by id... just dont partition?
    print(pd.read_parquet(path))