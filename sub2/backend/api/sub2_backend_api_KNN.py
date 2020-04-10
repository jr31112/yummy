import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_dataframes():
    # connect to DB
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    # read table 
    df_store = pd.read_sql_query("SELECT * from api_store", con)
    df_review = pd.read_sql_query("SELECT * from api_review", con)

    # clonse DB connection
    con.close()

    # select some columns
    stores = df_store.loc[:,['id','store_name','category','address']]
    reviews = df_review.loc[:,['user_id','store_id','total_score']]

    # rename columns and return data
    reviews.rename(columns={'total_score':'rating'}, inplace=True)
    stores.rename(columns={'id':'store_id'},inplace=True)

    df = pd.merge(reviews, stores, on="store_id")
    return df, stores

def sim_df(df):
    data = df.pivot_table('rating', index='user_id', columns='store_id')
    data = data.fillna(0)
    data = data.transpose()
    data_sim = cosine_similarity(data, data)
    store_sim_df = pd.DataFrame(data = data_sim, index = data.index, columns = data.index)
    return store_sim_df

def main():
    df, stores = load_dataframes()
    store_sim = sim_df(df)
    store_id = input()
    store_sim[store_id].sort_values(ascending=False)[1:10]


if __name__ == "__main__":
    main()