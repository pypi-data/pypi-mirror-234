import json
import os
from datetime import datetime

import requests
from fundb.sqlalchemy import Base
from fundrive.lanzou import LanZouSnapshot
from funsecret import BaseTable, create_engine_sqlite, get_md5_str
from sqlalchemy import String, UniqueConstraint, func, Integer, select, PrimaryKeyConstraint, TIMESTAMP
from sqlalchemy.orm import mapped_column, Session
from tqdm import tqdm


def url_json_load(url):
    try:
        response = requests.get(url)
        return 2, response.json()
    except Exception as e:
        return 1, None


class DataType:
    BOOK = 1
    RSS = 2
    THEME = 3


class ReadODSUrlData(Base):
    __tablename__ = "read_ods_url"
    __table_args__ = (UniqueConstraint("url"), PrimaryKeyConstraint("uuid"))

    uuid = mapped_column(String(100), comment="md5", primary_key=True)
    cate1 = mapped_column(String(100), comment="源", default="")
    type = mapped_column(Integer, comment="类型", default=1)

    status = mapped_column(Integer, comment="status", default=2)
    # 创建时间
    gmt_create = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    # 修改时间：当md5不一致时更新
    gmt_modified = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    # 更新时间，当重新拉取校验时更新
    gmt_updated = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    # 下游处理时间，下游拉数据时更新
    gmt_solved = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    url = mapped_column(String(100), comment="url", default="")
    source_md5 = mapped_column(String(100), comment="md5")


class ReadODSUrlDataManage(BaseTable):
    def __init__(self, url, *args, **kwargs):
        self.url = url
        engine = create_engine_sqlite(url)
        super(ReadODSUrlDataManage, self).__init__(table=ReadODSUrlData, engine=engine, *args, **kwargs)
        self.snapshot = LanZouSnapshot()

    def update(self, values):
        values = self.__check_values__(values)
        with Session(self.engine) as session:
            try:
                session.bulk_update_mappings(self.table, values)
                session.commit()
            except Exception:
                session.rollback()

    def select_md5(self, url):
        sql = select(ReadODSUrlData.source_md5).where(ReadODSUrlData.url == url)
        data = [line for line in self.execute(sql)]
        if len(data) > 0:
            (value,) = data[0]
            return value
        return None

    def add_source(self, url, cate1, type=DataType.BOOK, version=1, *args, **kwargs):
        data = {"cate1": cate1, "type": type, "version": version, "url": url}
        data["source_md5"] = self.select_md5(url=url)
        self.row_update(**data)

    def row_update(self, **data) -> bool:
        url = data["url"]
        data["uuid"] = get_md5_str(url)
        status, source = url_json_load(url)

        [data.pop(key, 1) for key in ("gmt_updated", "gmt_create", "gmt_modified", "gmt_solved")]
        _md5 = data.get("source_md5")
        source = json.dumps(source)
        md5 = get_md5_str(source)
        data.update({"status": status, "source_md5": md5, "gmt_updated": datetime.now()})
        if _md5 is not None and _md5 != md5:
            data["gmt_modified"] = func.now()
        self.upsert(data)
        return True

    def row_solved(self, uuid, status=2) -> bool:
        data = {"uuid": uuid, "gmt_solved": datetime.now(), "status": status}
        self.upsert(data)
        return True

    def snapshot_download(self):
        self.snapshot.download(os.path.dirname(self.url), url='https://bingtao.lanzoub.com/b01lj2vxi', pwd='4jn0')

    def snapshot_upload(self):
        self.snapshot.update(self.url, fid='8822098')

    def check_available(self):
        tqdm.pandas(desc="check")
        df = self.select_all()
        df.progress_apply(lambda row: self.row_update(**row), axis=1)
