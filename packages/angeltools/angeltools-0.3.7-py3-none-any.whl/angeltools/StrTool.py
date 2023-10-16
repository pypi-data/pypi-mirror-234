import hashlib
import json
import os
import random
import re
import sys
import time
import uuid
from pathlib import Path

import urllib3


def get_domain(url):
    domain = ''
    if url and url.strip():
        domain = urllib3.get_host(url)[1]
        if '.' in url:
            second_domain = domain.split('.')[-2]
            if second_domain in {"com", "net", "org", "gov"}:
                dml = domain.split(".")[-3:]
            else:
                dml = domain.split(".")[-2:]
            domain = '.'.join(dml)
    return domain


def hash_str(data):
    md5 = hashlib.md5()
    md5.update(str(data).encode('utf-8'))
    return md5.hexdigest()


def gen_uid1():
    return str(uuid.uuid1())


def get_linux_cmd_path(name):
    res = [x.strip() for x in os.popen(f"whereis {name}").read().split(" ") if x.strip()]
    if len(res) > 1:
        return res[1]
    return None


class ScrapyXpath:
    """
    包装 scrapy response 的xpath方法，不用每次都 extract 再判断结果，使爬虫更整洁
    也可以传入由 requests 获取的 response text 和 url，变成 scrapy selector 对象方便提取
    """
    from scrapy import Selector

    def __init__(self, scrapy_selector: Selector = None, url=None, html_content=None):
        """
        :param scrapy_selector:     response.xpath('//div[@class="xxx"]')
        """
        from scrapy.http import HtmlResponse

        self.HtmlResponse = HtmlResponse
        if scrapy_selector:
            self.raw = scrapy_selector
        elif url and html_content:
            self.raw = self.response_selector(url, html_content)
        else:
            raise ValueError('scrapy_selector or url and html_content required!')

    def scrapy_response(self, url, html_content):
        return self.HtmlResponse(url=url, body=html_content, encoding="utf-8")

    def response_selector(self, url, html_content):
        return self.scrapy_response(url, html_content).xpath('//html')

    def __map_str(self, map_dic, raw_str):
        if map_dic:
            n_res = ""
            for si in raw_str:
                t = map_dic.get(si, si)
                n_res += t
        else:
            n_res = raw_str
        return n_res

    def xe(self, xpath_str, strip_str=None, map_dic=None, sep=None, replace_str=None, auto_sep=False, default=""):
        """
        selector = response.xpath('//div[@class="xxx"]')
        sx = ScrapyXpath(selector)

        div_text_list = sx.xe('.//text()')
        div_link = sx.xe('./@href')

        :param xpath_str:   xpath表达式
        :param strip_str:
        :param map_dic:
        :param sep:
        :param replace_str:
        :param auto_sep:
        :param default:
        :return:
        """
        res = self.raw.xpath(xpath_str).extract()
        if res:
            res = [x.strip() for x in res if x and x.strip()]
            if not res:
                return default
            elif len(res) == 1:
                res = res[0].strip(strip_str) if strip_str else res[0]
                if replace_str:
                    res = res.replace(replace_str, "")
                if auto_sep:
                    res = "".join([x.strip() for x in res.split("\n") if x and x.strip()])
                res = self.__map_str(map_dic, res) or res
                return res
            else:
                nw = []
                for w in res:
                    if replace_str:
                        w = w.replace(replace_str, "")
                    if auto_sep:
                        w = "".join([x.strip() for x in w.split("\n") if x and x.strip()])
                    nw.append(self.__map_str(map_dic, w) or w)
                if sep is not None:
                    nw = sep.join(nw)
                return nw
        return default


class UrlFormat:
    def __init__(self, url=None):
        from urllib.parse import quote, urlparse, unquote

        self.quote = quote
        self.urlparse = urlparse
        self.unquote = unquote
        self.url = url

    def quote_str(self, s):
        res = self.quote(str(s).encode())
        return res

    def unquote_str(self, s):
        res = self.unquote(s)
        return res

    def make_url(self, base, params_add_dic, quote_param=True):
        new_url = base
        new_url += f'?{"&".join([f"{k}={self.quote_str(v) if quote_param else v}" for k, v in params_add_dic.items()])}'
        return new_url

    def split_url(self):
        url_data = dict()
        if self.url:
            temp_data = self.urlparse(self.unquote(self.url))
            url_data["queries"] = {x.split("=")[0]: self.unquote("=".join(x.split("=")[1:])) for x in temp_data.query.split("&")}
            url_data["host"] = temp_data.netloc
            url_data["protocol"] = temp_data.scheme
            url_data["path"] = temp_data.path
            url_data["require_params"] = temp_data.params
            url_data["fragment"] = temp_data.fragment
        return url_data

    def url_format(self, url_base=None, require_params=None, params_only=False, unquote_params=False, unquote_times=1):
        """
        获取url参数
        :param url_base:        url 前缀
        :param require_params:  需要的参数名，True全部，或者参数名列表 ['page', 'name', ...]
        :param params_only:     True只返回参数字典，否则根据require_params重组url
        :param unquote_params:  是否解密url
        :param unquote_times:   解密次数
        :return:
        """
        if not self.url:
            return {}
        if require_params is None:
            require_params = True
        if url_base:
            self.url = self.join_up([url_base, self.url], duplicate_check=True)
        if re.findall(r'\?', self.url):
            u_temp = self.url.split('?')
            new_url = re.sub(r"ref=[\s\S]+", "", u_temp[0])
            if require_params is True:
                dic = {x.split('=')[0]: x.split('=')[1].strip(" ").strip("/") for x in u_temp[1].split('&') if
                       x.split('=')[0] and len(x.split('=')) > 1}
            else:
                require_params = set(require_params)
                dic = {x.split('=')[0]: x.split('=')[1].strip(" ").strip("/") for x in u_temp[1].split('&') if
                       x.split('=')[0] in require_params and len(x.split('=')) > 1}
            if unquote_params:
                for _ in range(unquote_times):
                    dic = {k: self.unquote_str(v) for k, v in dic.items()}
            if params_only:
                return dic
            if dic:
                new_url += '?{}'.format("&".join(["{}={}".format(k, v) for k, v in dic.items()]))
        else:
            if params_only:
                return {}
            new_url = re.sub(r"ref=[\s\S]+", "", self.url)
        return new_url

    def join_up(self, path_lis, duplicate_check=False, sep=None) -> str:
        """
        拼接路径用的
        url 或者 文件路径都可以
        自动检测是否是url，自动加上分隔符
        如果不确定是否重复了，就把 duplicate_check 设置为 True

        :param path_lis: 需要传入待拼接的路径的列表，['part1', 'part2', 'part3' ...]，注意顺序
        :param duplicate_check: 去掉重复的路径，注意有些路径是重复的，所以默认关闭
        :param sep: 自定义间隔符， 如果不确定就留空
        :return: 返回拼接好的路径字符串 str
        """
        is_url = any([True if re.findall(r'(https?://)|(www\.)', x)
                      else False for x in path_lis if x])
        if sep is None and not is_url:
            sep = os.sep
        elif sep is None and is_url:
            sep = '/'
        path_lis = [x.strip('/').strip('\\') for x in path_lis if x]
        paths_rev = path_lis[::-1]
        new_url = ''
        if duplicate_check:
            for p in paths_rev:
                if p and p not in new_url:
                    new_url = p + sep + new_url
        else:
            new_url = sep.join(path_lis)
        return new_url


file_lock_prefix = 'file_lock_'


class LocalData:
    def __init__(self, store_path=None, name=None):
        file_dir = self._init_local_path(store_path)
        file_pre = f"{name}_" if name else "local_store_"
        self.f_pre = f"{file_dir}/{file_pre}"
        self.expire_time = 3600 * 24 * 365 * 100

    def _init_local_path(self, file_path):
        import subprocess

        if not file_path:
            file_path = '/tmp'
        if not os.path.exists(file_path):
            params = [
                f"mkdir -p {file_path}",
            ]
            dp = subprocess.run(params, shell=True, capture_output=True)
            if "无法创建目录" in dp.stderr.decode('utf-8'):
                file_path = '/tmp'
        return file_path

    def _file_name(self, fid):
        return f"{self.f_pre}{fid}.json"

    def get_fid(self, data):
        if not isinstance(data, str):
            data = json.dumps(data)
        return hash_str(data)

    def dump(self, data, fid=None, expire=None):
        exp = int(expire or self.expire_time) + int(time.time())
        dm_data = {"data": data, "expire": exp}
        dm_data = json.dumps(dm_data)
        if not fid:
            fid = self.get_fid(data=data)
        fn = self._file_name(fid)
        # if os.path.exists(fn):
        #     return fid
        with FileLock(lock_id=file_lock_prefix + fid, timeout=10):
            if os.path.exists(fn):
                os.remove(fn)
            with open(fn, 'w') as wf:
                wf.write(dm_data)
                wf.flush()
            wf.close()
        return fid

    def load(self, fid, default=None):
        fn = self._file_name(fid)
        if os.path.exists(fn):
            try:
                with open(fn, 'r') as rf:
                    data = json.loads(rf.read())
                    expire = int(data.get("expire"))
                    data = data.get("data")
                    if expire and int(time.time()) > expire:
                        os.remove(fn)
                        data = default
                rf.close()
            except Exception as E:
                print(E)
                os.remove(fn)
                data = default
        else:
            data = default
        return data


class FileLock:
    """
    使用文件操作实现的异步锁

    使用方式：
    with FileLock(lock_id='xxxx', timeout=xx.xx):
        do_the_jobs()

    """
    def __init__(self, lock_id=None, timeout: float or int = None):
        self.lock_id = lock_id
        self.timeout = float(timeout) if timeout else 3600 * 24 * 30 * 12
        self.__lock_dir()
        self.__get_lock_prefix()
        self.__init_lock(lock_id)
        self.fps = self.fp.absolute()
        self.enter_with_acquire = False

    def __enter__(self):
        if not self.enter_with_acquire:
            self.__acquire_lock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__exit_lock()

    def __call__(self, *args, **kwargs):
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']

    def clear(self, lock_id=None):
        if lock_id:
            self.__init_lock(lock_id)
            self.__exit_lock()
        else:
            for file in os.listdir(self.lock_dir):
                if file.startswith(file_lock_prefix):
                    try:
                        os.remove(self.lock_dir / file)
                    except:
                        pass

    def __lock_dir(self):
        if sys.platform == 'linux' or sys.platform == 'darwin':
            self.lock_dir = Path(f'/tmp/')
        else:
            self.lock_dir = Path(__file__).parent / 'FileLock'

    def __get_lock_prefix(self):
        self.fp_prefix = self.lock_dir / file_lock_prefix

    def __init_lock(self, lock_id):
        if not lock_id:
            lock_id = gen_uid1()
        lock_id_hash = hash_str(str(lock_id))
        self.fp = Path(f'{str(self.fp_prefix.absolute())}{lock_id_hash}.lock')

    def __acquire_lock(self):
        expire_time = time.time() + self.timeout
        try:
            while True:
                try:
                    if self.__get_size() and time.time() - expire_time < 0:
                        self.__wait()
                    else:
                        break
                except Exception as E:
                    print(f"acquire_lock error; lock id: {self.lock_id}: \n{E}")
                    break
        except KeyboardInterrupt:
            sys.exit()
        self.__add_num()
        return self

    def __read_num(self):
        num = "0"
        try:
            with open(self.fps, 'r') as rf:
                num = rf.read().strip()
        except:pass
        num = int(num) if num else 0
        return num

    def __get_size(self):
        try:
            size = 0 if not os.path.exists(self.fps) else os.path.getsize(self.fps)
        except:
            size = 0
        return size

    def __write_num(self, num):
        with open(self.fps, 'w+') as wf:
            wf.write(str(num))
            wf.flush()

    def __add_num(self):
        # self.fp.write_text("1" * (self.__get_size() + 1))
        self.__write_num("1" * (self.__get_size() + 1))

    def __sub_num(self):
        num = self.__get_size()
        if num > 1:
            # self.fp.write_text("1" * (num - 1))
            self.__write_num("1" * (num - 1))
        else:
            os.remove(self.fps)

    def __occupy(self):
        if not self.fp.exists():
            return False
        num = self.fp.read_text(encoding='utf-8')
        if num and num.isdigit() and int(num) >= 1:
            return True
        return False

    def __exit_lock(self):
        try:
            self.__sub_num()
        except:
            pass

    def __wait(self):
        time.sleep(random.randint(1, 5)/10)

    def acquire(self, **kwargs):
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']
        self.enter_with_acquire = True
        return self.__acquire_lock()

    def lock_time(self, format_time: str or bool = False):
        """
        :param format_time: True or "%Y-%m-%d %H:%M:%S" or False
        :return:
        """

        if self.fp.exists():
            tm = os.path.getatime(self.fps)
        else:
            tm = 0
        if not format_time:
            return tm
        else:
            if format_time is True:
                format_time = '%Y-%m-%d %H:%M:%S'
            return time.strftime(format_time, time.localtime(tm))

    def mark(self):
        """
        更新文件日期，返回更新后的时间戳
        :return:
        """
        self.fp.touch()
        return self.lock_time()

    def unmark(self):
        """
        清除锁文件，返回最后更新时间戳
        :return:
        """
        lock_time = self.lock_time()
        self.__exit_lock()
        return lock_time


class SortedWithFirstPinyin(object):

    def __init__(self, file_path, save_path=None, full_match=False, reverse=False):
        from BaseColor.base_colors import hred
        from pypinyin import lazy_pinyin

        file_path = Path(file_path)
        if not os.path.exists(str(file_path.absolute())):
            print(f"No such file: {hred(file_path.absolute())}")
            sys.exit(1)
        self.file_path = file_path
        self.lazy_pinyin = lazy_pinyin

        if not save_path:
            save_path_split = self.file_path.name.split('.')
            file_name = '.'.join(save_path_split[:-1])
            sub = save_path_split[-1]
            save_path = self.file_path.parent / f"{file_name}_sorted.{sub}"
        self.save_path = str(Path(save_path).absolute())
        self.full_match = full_match
        self.reverse = reverse

    def get_pinyin_first(self, text):
        return self.lazy_pinyin(text)[0][0] if not self.full_match else self.lazy_pinyin(text)[0]

    def get_pinyin(self, text):
        if not re.findall(r'[\ue4e00-\u9fa5]', text):
            return text

        n_line = ''
        for i in text:
            if re.findall(r'[\u4e00-\u9fa5]', i):
                lt = self.get_pinyin_first(i)
            else:
                lt = i
            n_line += lt
        return ''.join(n_line)

    def run(self):
        from angeltools.Slavers import Slaves
        from BaseColor.base_colors import hgreen

        with open(self.file_path, 'r') as rf:
            lines = rf.readlines()
        lines = [x for x in lines if x.strip()]
        py_raw_lines_map = {}
        py_lines = Slaves().work(self.get_pinyin, lines)
        for raw, py in zip(lines, py_lines):
            py_raw_lines_map[py] = raw

        sorted_py_lines = sorted(py_lines, reverse=self.reverse)
        sorted_lines = [py_raw_lines_map.get(x) for x in sorted_py_lines]

        with open(self.save_path, 'w') as wf:
            wf.writelines(sorted_lines)

        print(f"data saved: {hgreen(self.save_path)}")


class Printer:
    def __init__(self, name, highlight=False):
        self.name = name
        from BaseColor.base_colors import hred, hgreen, hyellow, hmagenta, hblue, hcyan, red, green, yellow, magenta, \
            blue, cyan
        if highlight:
            self.color = random.choice([hred, hgreen, hyellow, hmagenta, hblue, hcyan])
        else:
            self.color = random.choice([red, green, yellow, magenta, blue, cyan])

    def __call__(self, *args):
        txt = ' '.join([str(i) for i in args])
        txt = f"[{self.name}]-[{self.get_timestr()}]>>> " + txt
        print(self.color(txt))
        return self.name

    def get_timestr(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    # with FileLock('test-lock', timeout=10) as lock:
    #     # print(lock.lock_time(format_time=True))
    #     for i in range(100):
    #         print(i)
    #         time.sleep(0.5)
    #     # print(lock.lock_time(format_time=True))

    def do_job(job_name):
        time.sleep(random.randint(1, 10) / 10)
        with FileLock(f'test-lock_s1', timeout=12):
            for i in range(10):
                print(f"s1-{job_name}: {i}")
                time.sleep(0.5)
            with FileLock(f'test-lock_s2', timeout=12):
                for i in range(10):
                    print(f"s2-{job_name}: {i}")
                    time.sleep(0.5)
                    # if i == 5:
                    #     raise ValueError("进程出错了")


    # do_job("进程1")
    from angeltools.Slavers import BigSlaves
    BigSlaves(7).work(do_job, ["进程1", "进程2", "进程3"])

    # FileLock().clear(lock_id='test-lock')

    # uf = UrlFormat('http://www.baidu.com?page=1&user=me&name=%E5%BC%A0%E4%B8%89')
    # print(uf.split_url())

    # SortedWithFirstPinyin(
    #     file_path='/home/ga/Guardian/For-Python/AngelTools/angeltools/testfiles/res.txt',
    #     # save_path=save_path,
    #     full_match=True,
    #     reverse=False,
    # ).run()
