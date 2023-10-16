from funread.legado.base import url_manage
from funread.legado.base.url import  DataType
from tqdm import tqdm


def load_data1():
    url_manage.add_source(cate1="XIU2", uid=1, url="https://bitbucket.org/xiu2/yuedu/raw/master/shuyuan")
    url_manage.add_source(
        cate1="aoaostar",
        uid=1,
        url="https://jihulab.com/aoaostar/legado/-/raw/release/cache/8274870a1493d7c4e51c41682a8d1e9500457826.json",
    )
    url_manage.add_source(
        cate1="aoaostar",
        uid=2,
        url="https://jihulab.com/aoaostar/legado/-/raw/release/cache/3fc2c64c5489c491de6284dca2c2dfce7f551bc9.json",
    )
    url_manage.add_source(
        cate1="aoaostar",
        uid=3,
        url="https://jihulab.com/aoaostar/legado/-/raw/release/cache/71e56d4f1d8f1bff61fdd3582ef7513600a9e108.json",
    )
    url_manage.add_source(
        cate1="aoaostar",
        uid=4,
        url="https://jihulab.com/aoaostar/legado/-/raw/release/cache/1b8256c78b385543b5e8aa6a0d7693c76f8e60d4.json",
    )
    url_manage.add_source(
        cate1="aoaostar",
        uid=5,
        url="https://jihulab.com/aoaostar/legado/-/raw/release/cache/4dc410d1d0a674de21c5d869496efd60a7fcba7c.json",
    )
    url_manage.add_source(
        cate1="aoaostar",
        uid=6,
        url="https://jihulab.com/aoaostar/legado/-/raw/release/cache/edeb9b5490b7028906ad3cd2c2b7404b2e4052b9.json",
    )
    url_manage.add_source(
        cate1="aoaostar",
        uid=7,
        url="https://jihulab.com/aoaostar/legado/-/raw/release/cache/290e0bb1f148e963941fade280a938df81b374b7.json",
    )
    url_manage.add_source(
        cate1="aoaostar",
        uid=8,
        url="https://jihulab.com/aoaostar/legado/-/raw/release/cache/346da4b785d3dd5aed990a553e10d03d1ececec4.json",
    )
    url_manage.add_source(
        cate1="aoaostar",
        uid=9,
        url="https://jihulab.com/aoaostar/legado/-/raw/release/cache/6a2c6bb280c2508b7946a6fbe908e3208254f529.json",
    )
    url_manage.add_source(
        cate1="aoaostar",
        uid=10,
        url="https://jihulab.com/aoaostar/legado/-/raw/release/cache/c495b2f09c55df7acec91eb34588e78b1add7908.json",
    )
    url_manage.add_source(
        cate1="aoaostar",
        uid=11,
        url="https://jihulab.com/aoaostar/legado/-/raw/release/cache/0a189226b495a6b15c57acc06177ee15db8cd33c.json",
    )


def load_yck_ceo(uri="http://yckceo1.com", book_size=4200, books_size=200, rss_size=200, rsses_size=30):
    for _id in tqdm(range(1, rsses_size), "load"):
        url = f"{uri}/yuedu/rsss/json/id/{_id}.json"
        url_manage.add_source(url=url, uid=_id, type=DataType.RSS, cate1="源仓库")

    for _id in tqdm(range(1, books_size), "load"):
        url = f"{uri}/yuedu/shuyuans/json/id/{_id}.json"
        url_manage.add_source(url=url, uid=_id, cate1="源仓库")

    for _id in tqdm(range(1, rss_size), "load"):
        url = f"{uri}/yuedu/rss/json/id/{_id}.json"
        url_manage.add_source(url=url, uid=_id, type=DataType.RSS, cate1="源仓库")

    for _id in tqdm(range(1, book_size), "load"):
        url = f"{uri}/yuedu/shuyuan/json/id/{_id}.json"
        url_manage.add_source(url=url, uid=_id, cate1="源仓库")


def load_all():
    load_data1()
    load_yck_ceo()
