import sqlite3
import pandas as pd
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import dump
import surprise
import numpy as np

def load_dataframes():
    # connect to DB
    con = sqlite3.connect("../db.sqlite3")
    cur = con.cursor()
    # read table 
    df_store = pd.read_sql_query("SELECT * from api_store", con)
    df_review = pd.read_sql_query("SELECT * from api_review", con)

    # clonse DB connection
    con.close()

    # select some columns
    stores = df_store[['id','store_name','category']]
    reviews = df_review[['user_id','store_id','total_score']]

    # rename columns and return data
    reviews.rename(columns={'total_score':'rating'}, inplace=True)
    stores.rename(columns={'id':'store_id'},inplace=True)

    df = pd.merge(reviews, stores, on="store_id")
    return df

def get_predict_data(df ,raw, alg, user_id, area=None):
    if area is not None:
        tmp = df[df['address'].str.contains(area)]
    else:
        tmp = raw
    iids = tmp['store_id'].unique()
    iidsuser = raw.loc[raw['user_id']==user_id, 'store_id']
    iids_to_pred = np.setdiff1d(iids,iidsuser) # 안 간 가게 구함(차집합)

    testset = [[user_id,iid,5.] for iid in iids_to_pred]
    predictions = alg.test(testset)

    pred_ratings = np.array([pred.est for pred in predictions])
    i_max = pred_ratings.argsort()[:10]
    iid = iids_to_pred[i_max]

    return iid, i_max,pred_ratings

def print_results(iid, i_max, pred_ratings):
    for i,m in zip(iid,i_max):
        print('{0} : {1}'.format(i,pred_ratings[m]))

def get_recommandation_with_userid(df, user_id):
    #swapping columns
    raw=df[['user_id','store_id','rating']] 
    # when importing from a DF, you only need to specify the scale of the ratings.
    reader = surprise.Reader(rating_scale=(0,5)) 
    #into surprise:
    dataframe = Dataset.load_from_df(raw,reader)

    algo = surprise.SVD()
    # cross_validate(algo, dataframe,measures=['RMSE'], cv=3, verbose=True)
    algo.fit(dataframe.build_full_trainset())

    iid, i_max,pred_ratings = get_predict_data(df, raw, algo, user_id)
    print_results(iid,i_max,pred_ratings)


def main():
    df = load_dataframes()
    user_id = input(print("enter user ID : "))
    get_recommandation_with_userid(df, user_id)



if __name__ == "__main__":
    main()