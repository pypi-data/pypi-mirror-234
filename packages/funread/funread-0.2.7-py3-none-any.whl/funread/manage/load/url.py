from funread.manage.base.url import url_manage, DataType
from tqdm import tqdm


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
    load_yck_ceo()
