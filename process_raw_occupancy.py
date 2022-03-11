import pandas as pd
import random
import datetime
random.seed(2)


"""
Idea: for now, will just 
"""


def create_sim_booked_dataset(df):
    df_ = df.copy()
    df_['available'] = df['available'].apply(lambda x: bool(~(~x | bool(random.getrandbits(1)))))   # should only randomly switch to false
    df_['pulled'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return df_


if __name__ == "__main__":
    df = pd.read_parquet("data/parquet")
    df2 = create_sim_booked_dataset(df)
    df2.to_csv("data/sim_new_parquet/df.csv")

    big_df = pd.concat([df, df2]).sort_values(by=["id", "date", "pulled"])

    big_df['diff'] = big_df['available'].diff()
    print(big_df)
    big_df.to_csv("test.csv")

    """
    Idea is to window and do a diff on groups of listings days - keep wherever diff is not zero or is null
    that would mean there was cancellation or booking
    """


