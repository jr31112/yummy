import json
import pandas as pd
import os
import shutil

DATA_DIR = "../../data"
DATA_FILE = os.path.join(DATA_DIR, "data.json")
DUMP_FILE = os.path.join(DATA_DIR, "dump_with_rev_store.pkl")

"""
dump_store.pkl에서 파일읽어서 dump_with_rev_store로 한다 ㅠㅠ
+ 메뉴 제거
"""
review_columns = (
    "id",  # 리뷰 고유번호
    "store",  # 음식점 고유번호
    "user",  # 유저 고유번호
    "score",  # 평점
    "content",  # 리뷰 내용
    "reg_time",  # 리뷰 등록 시간
)

user_columns = (
    "id", # 유저 고유번호
    "gender", # 유저 성별
    "age", # 유저 나이
)

def import_data(data_path=DATA_FILE):
    """
    Req. 1-1-1 음식점 데이터 파일을 읽어서 Pandas DataFrame 형태로 저장합니다
    """

    try:
        with open(data_path, encoding="utf-8") as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"`{data_path}` 가 존재하지 않습니다.")
        exit(1)

    reviews = []  # 리뷰 테이블
    users = {} # 유저 테이블
    idx = 0
    r_idx = 0
    for d in data:

        for review in d["review_list"]:
            r = review["review_info"]
            u = review["writer_info"]
            r_idx+=1
            reviews.append(
                [r_idx, d["id"], u["id"], r["score"], r["content"], r["reg_time"]]
            )
            try:
                users[u["id"]]
            except KeyError:
                user_colums = (
                    "id", # 유저 고유번호
                    "gender", # 유저 성별
                    "age", # 유저 나이
                )
                users.update({u["id"]: [u["id"], u["gender"], u["born_year"]]})

    store_frame = pd.read_pickle(os.path.join(DATA_DIR, "dump_store.pkl"))
    store_frame = store_frame[['id','store_name','branch','area','tel','address','latitude','longitude','category']]
    review_frame = pd.DataFrame(data=reviews, columns=review_columns)
    user_frame = pd.DataFrame(data=list(users.values()), columns=user_columns)

    # 데이터 끼워넣기
    stores_reviews = pd.merge(store_frame, review_frame, left_on="id", right_on="store")
    scores_group = stores_reviews.groupby(["store", "store_name"])
    scores = scores_group.agg(total=('score', 'sum'),count=('id_y','count'))
    df = scores.reset_index()
    store_rev_frame = pd.merge(store_frame, df, left_on="id", right_on="store",how='left')
    store_rev_frame[['total','count']] = store_rev_frame[['total','count']].fillna(value=0)
    store_rev_frame.drop(['store_name_y','store'], axis=1, inplace=True)
    store_rev_frame.rename(columns={'store_name_x':'store_name'},inplace=True)

    return {"stores": store_rev_frame, "reviews": review_frame, "users" : user_frame} 


def dump_dataframes(dataframes):
    pd.to_pickle(dataframes, DUMP_FILE)


def load_dataframes():
    return pd.read_pickle(DUMP_FILE)


def main():

    print("[*] Parsing data...")
    data = import_data()
    print("[+] Done")

    print("[*] Dumping data...")
    dump_dataframes(data)
    print("[+] Done\n")
    data = load_dataframes()

    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w

    print("[음식점]")
    print(f"{separater}\n")
    print(data["stores"].head())
    print(f"\n{separater}\n\n")

    print("[리뷰]")
    print(f"{separater}\n")
    print(data["reviews"].head())
    print(f"\n{separater}\n\n")

    print("[유저]")
    print(f"{separater}\n")
    print(data["users"].head())
    print(f"\n{separater}\n\n")


if __name__ == "__main__":
    main()