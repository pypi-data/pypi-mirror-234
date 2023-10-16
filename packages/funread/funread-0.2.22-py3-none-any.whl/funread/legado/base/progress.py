import json
import os
import re
from datetime import datetime

from fundb.sqlalchemy import Base
from fundrive.lanzou import LanZouSnapshot
from funsecret import BaseTable, create_engine_sqlite
from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import mapped_column
from tqdm import tqdm

from .source import ReadODSSourceDataManage

tqdm.pandas(desc="pandas bar")


class DataType:
    BOOK = 1
    RSS = 2
    THEME = 3


def retain_zh_ch_dig(text):
    return re.sub("[^\u4e00-\u9fa5a-zA-Z0-9\[\]]+", "", text)


class Progress:
    def __init__(self, data):
        self.data = data
        self.source = json.loads(data["source"])
        self.source["bookSourceComment"] = ""
        self.source["bookSourceUrl"] = self.source["bookSourceUrl"].rstrip("/|#")
        if "httpUserAgent" in self.source.keys():
            self.source["header"] = self.source.pop("httpUserAgent")

        for key in ["bookSourceGroup", "bookSourceName"]:
            self.source[key] = retain_zh_ch_dig(self.source.get(key, ""))

    def run(self):
        self.format_book_info()
        self.format_content()
        self.format_search()
        self.format_explore()
        self.format_toc()
        self.data["source"] = json.dumps(self.source)
        return self.data

    def __format_base(self, group, map):
        book_info = self.source.get(group, {})

        for key, name in map.items():
            if key not in self.source:
                continue
            value = self.source.pop(key)
            if value:
                book_info[name] = value
        if len(book_info) > 0:
            self.source[group] = book_info

    def format_book_info(self):
        map = {
            "ruleBookAuthor": "author",
            "ruleBookContent": "content",
            "ruleBookContentReplace": "contentReplace",
            "ruleBookInfoInit": "init",
            "ruleBookKind": "kind",
            "ruleBookLastChapter": "lastChapter",
            "ruleBookName": "name",
            "ruleBookUrlPattern": "urlPattern",
            "ruleBookWordCount": "wordCount",
        }
        self.__format_base("ruleBookInfo", map)

    def format_content(self):
        map = {
            "ruleContentUrl": "url",
            "ruleContentUrlNext": "urlNext",
            "ruleBookContentReplaceRegex": "replaceRegex",
            "ruleBookContentSourceRegex": "sourceRegex",
            "ruleBookContentWebJs": "webJs",
        }
        self.__format_base("ruleContent", map)

    def format_search(self):
        map = {
            "ruleSearchUrl": "url",
            "ruleSearchName": "name",
            "ruleSearchAuthor": "author",
            "ruleSearchList": "bookList",
            "ruleSearchCoverUrl": "coverUrl",
            "ruleSearchIntroduce": "intro",
            "ruleSearchKind": "kind",
            "ruleSearchLastChapter": "lastChapter",
            "ruleSearchNoteUrl": "noteUrl",
            "ruleSearchWordCount": "wordCount",
        }
        self.__format_base("ruleSearch", map)

    def format_explore(self):
        map = {
            "ruleFindUrl": "url",
            "ruleFindName": "name",
            "ruleFindAuthor": "author",
            "ruleFindList": "bookList",
            "ruleFindCoverUrl": "coverUrl",
            "ruleFindIntroduce": "intro",
            "ruleFindKind": "kind",
            "ruleFindLastChapter": "lastChapter",
            "ruleFindNoteUrl": "noteUrl",
        }
        self.__format_base("ruleExplore", map)

    def format_toc(self):
        map = {
            "ruleChapterList": "chapterList",
            "ruleChapterName": "chapterName",
            "ruleChapterUpdateTime": "updateTime",
            "ruleChapterUrl": "chapterUrl",
            "ruleChapterUrlNext": "nextTocUrl",
        }
        self.__format_base("ruleToc", map)


class ReadODSProgressData(Base):
    __tablename__ = "read_ods_progress"

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


class ReadODSProgressDataManage(BaseTable):
    def __init__(self, url=None, *args, **kwargs):
        self.url = url
        engine = create_engine_sqlite(url)
        super(ReadODSProgressDataManage, self).__init__(table=ReadODSProgressData, engine=engine, *args, **kwargs)
        self.snapshot = LanZouSnapshot()

    def progress(self, source_manage: ReadODSSourceDataManage):
        df = source_manage.select_all()
        # df = df[df["status"] == 2]
        df = df.sort_values("gmt_solved").reset_index(drop=True)

        def solve(row):
            try:
                self.upsert(Progress(data=dict(row)).run())
            except Exception as e:
                # print(e)
                # source_manage.row_solved(row["uuid"], status=1)
                pass

        df.progress_apply(lambda row: solve(row), axis=1)

    def snapshot_download(self):
        self.snapshot.download(os.path.dirname(self.url), url='https://bingtao.lanzoub.com/b01lj2wkb', pwd='1he3')

    def snapshot_upload(self):
        self.snapshot.update(self.url, fid='8822121')

    def row_solved(self, uuid, status=2) -> bool:
        data = {"uuid": uuid, "gmt_solved": datetime.now(), "status": status}
        self.upsert(data)
        return True
