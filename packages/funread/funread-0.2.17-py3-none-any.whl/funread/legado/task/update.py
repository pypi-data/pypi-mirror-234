import os.path
from datetime import datetime

from fundrive.lanzou import LanZouDrive
from funfile import tarfile
from funsecret import read_secret


class UpdateData:
    def __init__(self, url="https://bingtao.lanzoub.com/b01liv12f", pwd="3wy3"):
        self.db_dir = "/home/bingtao/workspace/tmp"
        # self.db_dir = "./tmp"
        self.db_path = f"{self.db_dir}/funread.db"
        self.gz_path = f"{self.db_path}-{datetime.now().strftime('%Y%m%d%H%M%S')}.tar"
        self.url = url
        self.pwd = pwd
        read_secret("funread", "db", "sqlite", "uri", value=self.db_path)

    def upload(self):
        with tarfile.open(self.gz_path, "w:xz") as fw:
            fw.add(self.db_path, arcname=os.path.basename(self.db_path))
        drive = LanZouDrive()
        drive.login()
        drive.upload_file(self.gz_path, fid="8811915")

    def download(self):
        drive = LanZouDrive()
        datas = drive.get_file_list(url=self.url, pwd=self.pwd)
        datas = sorted(datas, key=lambda x: x["name"], reverse=True)
        drive.download_file(dir_path=self.db_dir, url=datas[0]["url"], pwd=datas[0]["pwd"], overwrite=True)
        with tarfile.open(f"{self.db_dir}/{datas[0]['name']}", "r:xz") as fr:
            fr.extractall(path=self.db_dir)

    def update(self):
        from funread.legado.base.progress import progress_manage
        from funread.legado.base.source import source_manage
        from funread.legado.load.url import load_data1, load_yck_ceo

        load_data1()
        load_yck_ceo(book_size=2000)
        source_manage.progress()
        progress_manage.progress()

    def run(self):
        # self.download()
        # self.update()
        self.upload()


UpdateData().run()
