import itertools
from collections import Counter
from parse import load_dataframes
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import folium
from folium.plugins import MarkerCluster

def set_config():
    # 폰트, 그래프 색상 설정
    font_list = fm.findSystemFonts(fontpaths=None, fontext="ttf")
    if any(["notosanscjk" in font.lower() for font in font_list]):
        plt.rcParams["font.family"] = "Noto Sans CJK JP"
    else:
        if not any(["malgun" in font.lower() for font in font_list]):
            raise Exception(
                "Font missing, please install Noto Sans CJK or Malgun Gothic. If you're using ubuntu, try `sudo apt install fonts-noto-cjk`"
            )

        plt.rcParams["font.family"] = "Malgun Gothic"

    sns.set_palette(sns.color_palette("Spectral"))
    plt.rc("xtick", labelsize=6)


def show_store_categories_graph(dataframes, n=20):
    """
    Tutorial: 전체 음식점의 상위 `n`개 카테고리 분포를 그래프로 나타냅니다.
    """

    stores = dataframes["stores"]
    
    # 모든 카테고리를 1차원 리스트에 저장합니다
    categories = stores.category.apply(lambda c: c.split("|"))
    categories = itertools.chain.from_iterable(categories)

    # 카테고리가 없는 경우 / 상위 카테고리를 추출합니다
    categories = filter(lambda c: c != "", categories)
    categories_count = Counter(list(categories))
    best_categories = categories_count.most_common(n=n)
    df = pd.DataFrame(best_categories, columns=["category", "count"]).sort_values(
        by=["count"], ascending=False
    )
    
    # 그래프로 나타냅니다
    chart = sns.barplot(x="category", y="count", data=df)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
    plt.title("음식점 카테고리 분포")
    plt.show()


def show_store_review_distribution_graph(dataframes):
    """
    Req. 1-3-1 전체 음식점의 리뷰 개수 분포를 그래프로 나타냅니다. 
    """
    reviews = dataframes["reviews"]
    stores = reviews.store
    stores_count = Counter(list(stores))
    stores_count = stores_count.most_common()
    df = pd.DataFrame(stores_count, columns=["stores", "count"])
    reviews_count = Counter(list(df["count"]))
    reviews_count = reviews_count.most_common()
    df = pd.DataFrame(reviews_count, columns=["count", "amount"]).sort_values(
        by=["count"], ascending=False
    )
    chart = sns.lineplot(x="count", y="amount", data=df)
    plt.title("음식점 리뷰 개수 분포")
    plt.show()

def show_store_average_ratings_graph(dataframes):
    """
    Req. 1-3-2 각 음식점의 평균 평점을 그래프로 나타냅니다.
    """
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )
    scores_group = stores_reviews.groupby(["store", "store_name"])
    scores = scores_group.agg(score=('score', 'mean'))
    scores_count = Counter(list(scores.score))
    scores_count = scores_count.most_common()
    df = pd.DataFrame(scores_count, columns=["score", "count"]).sort_values(by=["score"], ascending=False)
    chart = sns.lineplot(x="score", y="count", data=df)
    plt.title("음식점 평균 평점 분포")
    plt.show()

def show_user_review_distribution_graph(dataframes):
    """
    Req. 1-3-3 전체 유저의 리뷰 개수 분포를 그래프로 나타냅니다.
    """
    users = dataframes["reviews"].user
    user_count = Counter(list(users)).most_common()
    df = pd.DataFrame(user_count, columns=["user", "count"])
    user_amount = Counter(list(df["count"])).most_common()
    df = pd.DataFrame(user_amount, columns=["count", "amount"])
    chart = sns.lineplot(x="count", y="amount", data=df)
    plt.title("유저의 리뷰 개수 분포")
    plt.show()


def show_user_age_gender_distribution_graph(dataframes):
    """
    Req. 1-3-4 전체 유저의 성별/나이대 분포를 그래프로 나타냅니다.
    """
    users = dataframes["users"]
    users = users[users["age"]!=2021]
    male = users[users["gender"]=="남"]
    female = users[users["gender"]=="여"]
    age_male_count = Counter(list(male["age"])).most_common()
    age_female_count = Counter(list(female["age"])).most_common()
    df_male = pd.DataFrame(age_male_count, columns=["age", "count"])
    df_female = pd.DataFrame(age_female_count, columns=["age", "count"])
    sns.lineplot(x="age", y="count", data=df_male, label="men")
    sns.lineplot(x="age", y="count", data=df_female, label="women")
    plt.title("유저의 남/녀별 나이대 분포")
    plt.show()

def show_stores_distribution_graph(dataframes, min_reviews=10):
    """
    Req. 1-3-5 각 음식점의 위치 분포를 지도에 나타냅니다.
    """
    stores_reviews = pd.merge(dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store")
    scores_group = stores_reviews.groupby(["store", "store_name"])
    scores = scores_group.agg(count=('store', 'size'), score=('score', 'mean'))
    scores = scores[scores["count"]>min_reviews]
    stores = pd.merge(scores, dataframes["stores"], left_on="store", right_on="id")
    m = folium.Map(location=[36.3504567,127.3848187],zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)
        
    for i in stores.index:
        name = stores.loc[i, "store_name"]
        lat = stores.loc[i, "latitude"]
        lon = stores.loc[i, "longitude"]
        folium.Marker(
            location=[lat,lon],
            popup=name,
        ).add_to(marker_cluster)
    m.save('map.html')



def main():
    set_config()
    data = load_dataframes()
    # show_store_categories_graph(data)
    # show_store_review_distribution_graph(data)
    # show_store_average_ratings_graph(data)
    # show_user_review_distribution_graph(data)
    show_user_age_gender_distribution_graph(data)
    # show_stores_distribution_graph(data)


if __name__ == "__main__":
    main()
