from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from backend import settings
from api import models


class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = Path(settings.BASE_DIR).parent.parent / "data"
    DATA_FILE = str(DATA_DIR / "dump.pkl")

    def _load_dataframes(self):
        try:
            data = pd.read_pickle(Command.DATA_FILE)
        except:
            print(f"[-] Reading {Command.DATA_FILE} failed")
            exit(1)
        return data

    def _initialize(self):
        """
        Sub PJT 1에서 만든 Dataframe을 이용하여 DB를 초기화합니다.
        """
        print("[*] Loading data...")
        dataframes = self._load_dataframes()

# # user
        print("[*] Initializing users...")
        models.CustomUser.objects.all().delete()
        users = dataframes["users"]
        users_bulk = [
            models.CustomUser(
                id = user.id,
                email="None"+str(user.id)+"@co.co",
                birth_year=user.birth_year,
                gender=user.gender,
                nickname="user"+str(user.id),
            )
            for user in users.itertuples()
        ]
        models.CustomUser.objects.bulk_create(users_bulk)

        print("[+] Done")
# store
        print("[*] Initializing stores...")
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
            )
            for store in stores.itertuples()
        ]
        models.Store.objects.bulk_create(stores_bulk)

        print("[+] Done")
# review
        print("[*] Initializing reviews...")
        models.Review.objects.all().delete()
        reviews = dataframes["reviews"]
        reviews_bulk = [
            models.Review(
                id=review.id,
                store=models.Store.objects.get(id=review.store),
                user=models.CustomUser.objects.get(id=review.user),
                total_score=review.score,
                content=review.content,
                reg_time=review.reg_time,
            )
            for review in reviews.itertuples()
        ]
        models.Review.objects.bulk_create(reviews_bulk)

        print("[+] Done")

# menu
        print("[*] Initializing menus...")
        models.Menu.objects.all().delete()
        menus = dataframes["menus"]
        menus_bulk = [
            models.Menu(
                id=menu.id,
                store=models.Store.objects.get(id=menu.store),
                menu_name=menu.menu_name,
                price=menu.price,
            )
            for menu in menus.itertuples()
        ]
        models.Menu.objects.bulk_create(menus_bulk)

        print("[+] Done")

    def handle(self, *args, **kwargs):
        self._initialize()
