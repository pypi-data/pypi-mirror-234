import json
import os.path
from datetime import datetime

import requests
from fundb.sqlalchemy import Base
from fundrive.lanzou import LanZouSnapshot
from funsecret import BaseTable, create_engine_sqlite, get_md5_str
from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import mapped_column
from tqdm import tqdm

from .url import ReadODSUrlDataManage

tqdm.pandas(desc="pandas bar")


class DataType:
    BOOK = 1
    RSS = 2
    THEME = 3


class ReadODSSourceData(Base):
    __tablename__ = "read_ods_source"

    uuid = mapped_column(String(100), comment="源md5", primary_key=True, default="")
    url_uuid = mapped_column(String(100), comment="id", default=1)
    status = mapped_column(Integer, comment="status", default=2)
    # 创建时间
    gmt_create = mapped_column(DateTime(timezone=True), server_default=func.now())
    # 修改时间：当md5不一致时更新
    gmt_modified = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # 更新时间，当重新拉取校验时更新
    gmt_updated = mapped_column(DateTime(timezone=True), server_default=func.now())
    # 下游处理时间，下游拉数据时更新
    gmt_solved = mapped_column(DateTime(timezone=True), server_default=func.now())
    source = mapped_column(String(100000), comment="源", default="")


class ReadODSSourceDataManage(BaseTable):
    def __init__(self, url=None, *args, **kwargs):
        self.url = url
        engine = create_engine_sqlite(url)
        super(ReadODSSourceDataManage, self).__init__(table=ReadODSSourceData, engine=engine, *args, **kwargs)
        self.snapshot = LanZouSnapshot()

    def row_upsert(self, source, url_uuid):
        source = json.dumps(source)
        data = {
            "uuid": get_md5_str(source),
            "url_uuid": url_uuid,
            "source": source,
        }
        self.upsert(data)

    def progress(self, url_manage: ReadODSUrlDataManage):
        df = url_manage.select_all()
        # df = df[df["status"] == 2]
        df = df.sort_values("gmt_solved").reset_index(drop=True)

        def solve(row):
            try:
                response = requests.get(row["url"])
                for source in response.json():
                    self.row_upsert(url_uuid=row["uuid"], source=source)
                url_manage.row_solved(row["uuid"])
            except Exception:
                url_manage.row_solved(row["uuid"], status=1)

        df.progress_apply(lambda row: solve(row), axis=1)

    def snapshot_download(self):
        self.snapshot.download(os.path.dirname(self.url), url='https://bingtao.lanzoub.com/b01lj2wja', pwd='fn3k')

    def snapshot_upload(self):
        self.snapshot.update(self.url, fid='8822120')

    def row_solved(self, uuid, status=2) -> bool:
        data = {"uuid": uuid, "gmt_solved": datetime.now(), "status": status}
        self.upsert(data)
        return True
