from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from backend import settings
from api import models

# 메뉴 없다 200408
class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = Path(settings.BASE_DIR).parent.parent / "data"
    DATA_FILE = str(DATA_DIR / "dump_with_rev_store.pkl") # review정보 포함한것 + 주소 업데이트한 store
    DATA_FILE_SPOT_LODGING = str(DATA_DIR / "dump_spot_lodging.pkl") # 숙박 + 관광지 정보
    # DATA_FILE = str(DATA_DIR / "dump_with_rev.pkl") # review정보 포함한것
    # DATA_FILE = str(DATA_DIR / "dump.pkl") #포함 안한것

    def _load_dataframes(self):
        try:
            data = pd.read_pickle(Command.DATA_FILE)
            data_spot = pd.read_pickle(Command.DATA_FILE_SPOT_LODGING)
        except:
            print(f"[-] Reading {Command.DATA_FILE} failed")
            exit(1)
        return data, data_spot

    def _initialize(self):
        """
        Sub PJT 1에서 만든 Dataframe을 이용하여 DB를 초기화합니다.
        """
        print("[*] Loading data...")
        dataframes, dataframes_spot = self._load_dataframes()
# load store dataframe with reviewcount , total_score
# store
        print("[*] Initializing stores...( + review : score, count)")
        models.Store.objects.all().delete()
        stores = dataframes["stores"]
        stores_bulk = [
            models.Store(
                id=store.id,
                store_name=store.store_name,
                branch=store.branch,
                area=store.area,
                tel=store.tel,
                address=store.address,
                latitude=store.latitude,
                longitude=store.longitude,
                category=store.category,
                review_count=store.count,
                review_total_score=store.total,
            )
            for store in stores.itertuples()
        ]
        models.Store.objects.bulk_create(stores_bulk)

        print("[+] Done")


# user
        print("[*] Initializing users...")
        models.User.objects.all().delete()
        users = dataframes["users"]
        users_bulk = [
            models.User(
                id = user.id,
                email="None"+str(user.id)+"@co.co",
                birth_year=user.age,
                gender=user.gender,
                nickname="user"+str(user.id),
            )
            for user in users.itertuples()
        ]
        models.User.objects.bulk_create(users_bulk)

        print("[+] Done")

# review
        print("[*] Initializing reviews...")
        models.Review.objects.all().delete()
        reviews = dataframes["reviews"]
        reviews_bulk = [
            models.Review(
                id=review.id,
                store=models.Store.objects.get(id=review.store),
                user=models.User.objects.get(id=review.user),
                total_score=review.score,
                content=review.content,
                reg_time=review.reg_time,
            )
            for review in reviews.itertuples()
        ]
        models.Review.objects.bulk_create(reviews_bulk)

        print("[+] Done")

# spot
        print("[*] Initializing spot...")
        models.Spot.objects.all().delete()
        spots = dataframes_spot["spots"]
        spots_bulk = [
            models.Spot(
                spot_name=spot.spot_name,
                road_address=spot.road_address,
                address=spot.address,
                latitude=spot.latitude,
                longitude=spot.longitude,
                description=spot.description
            )
            for spot in spots.itertuples()
        ]
        models.Spot.objects.bulk_create(spots_bulk)

        print("[+] Done")

# lodging
        print("[*] Initializing lodging...")
        models.Lodging.objects.all().delete()
        lodgings = dataframes_spot["lodgings"]
        lodgings_bulk = [
            models.Lodging(
                lodging_name=lodging.lodging_name,
                lodging_type=lodging.lodging_type,
                road_address=lodging.road_address,
                address=lodging.address,
                latitude=lodging.latitude,
                longitude=lodging.longitude,
                description=lodging.description
            )
            for lodging in lodgings.itertuples()
        ]
        models.Lodging.objects.bulk_create(lodgings_bulk)

        print("[+] Done")


    def handle(self, *args, **kwargs):
        self._initialize()