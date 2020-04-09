import sqlite3
import pandas as pd
import surprise
import numpy as np
import os
def load_dataframes():
    # connect to DB
    con = sqlite3.connect("db.sqlite3") # 모듈 호출시 사용경로
    # print (os.getcwd()) #현재 디렉토리의
    # con = sqlite3.connect("../db.sqlite3") # main용
    cur = con.cursor()
    # read table 
    df_store = pd.read_sql_query("SELECT * from api_store", con)
    df_review = pd.read_sql_query("SELECT * from api_storereview", con)

    # clonse DB connection
    con.close()

    # select some columns
    stores = df_store.loc[:,['id','store_name','category','address']]
    reviews = df_review.loc[:,['user_id','store_id','total_score']]

    # rename columns and return data
    reviews.rename(columns={'total_score':'rating'}, inplace=True)
    stores.rename(columns={'id':'store_id'},inplace=True)

    df = pd.merge(reviews, stores, on="store_id")
    return df,stores


# 예측모델 지정해주기 ~~!
def set_algo(user_id,area=None):
    # dump file 지정
    file_name = os.path.expanduser('dump_file')

    # load dataframe
    df, stores = load_dataframes()
    #swapping columns
    raw=df.loc[:,['user_id','store_id','rating']] 
    # when importing from a DF, you only need to specify the scale of the ratings.
    reader = surprise.Reader(rating_scale=(0,5)) 
    #into surprise:
    dataframe = surprise.Dataset.load_from_df(raw,reader)
    trainset = dataframe.build_full_trainset()

    try:
        _, algo = surprise.dump.load(file_name)
     
    except FileNotFoundError:
        # 파일이 존재하지않는 경우
        print("Dump file Doesn't exists.")
        # Use the famous SVD algorithm.
        algo = surprise.SVD()
        algo.fit(trainset)
        surprise.dump.dump(file_name, algo=algo)

    finally:
        # 전국 검색
        if area is None:
            iids = raw['store_id'].unique()
        else:
            tmp = df[df['address'].str.contains(area)]
            iids = tmp['store_id'].unique()
            
        iidsUsrnotVisited = raw.loc[raw['user_id']==user_id, 'store_id']
        iids_to_pred = np.setdiff1d(iids,iidsUsrnotVisited) # 안 간 가게 구함(차집합)
        # user_id가 가지않은 가게들로 testset 생성
        testset = [[user_id, iid, 5.] for iid in iids_to_pred]
        predictions = algo.test(testset)
        print(surprise.accuracy.rmse(predictions))
        pred_ratings = np.array([pred.est for pred in predictions])
        i_max = pred_ratings.argsort()[::-1][:5] # 역순으로 상위 5개
        #i_max = pred_ratings.argmax()
        iid = iids_to_pred[i_max]
        results = {}
        for i,m in zip(iid,i_max):
            # print('{0} : {1}'.format(i,pred_ratings[m]))
            results[i] = pred_ratings[m]
        return results

def main():
    result = set_algo(4974)
    pass

if __name__ == "__main__":
    main()
