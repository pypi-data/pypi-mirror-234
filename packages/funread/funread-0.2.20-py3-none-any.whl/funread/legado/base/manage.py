from .progress import ReadODSProgressDataManage
from .source import ReadODSSourceDataManage
from .url import ReadODSUrlDataManage
from funsecret import read_secret

path = read_secret(cate1="funread", cate2='legado', cate3='sqlite', cate4='path') or 'tmp'
url_manage = ReadODSUrlDataManage(url=f'{path}/funread-url.db')
source_manage = ReadODSSourceDataManage(url=f'{path}/funread-source.db')
progress_manage = ReadODSProgressDataManage(url=f'{path}/funread-progress.db')
