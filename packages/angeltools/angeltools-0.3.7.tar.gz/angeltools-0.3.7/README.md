AngelTools
=======================
自用的 python 小工具合集  
就是开发过程中常用的一些小方法、小轮子的合集，免去每次用到都得复制  
每个人开发思维都不一样，不一定适合其他人  
  
  

安装
=========
```linux shell
$ pip install angeltools
```
或者直接下载 duplremover 文件夹到你的项目目录下也行
  

现有方法：  
=========
 - 比例控制器：Scaler  
```python
"""
控制数值区间的方法
"""
from angeltools.MathTool import Scaler

scaler = Scaler()

num = 998
scaler.arctan(x=num, lower_point_x=80, lower_limit=80, upper_limit=100)

# arctan 反正切函数, 用于控制连续变量最大值区间。
# 人话就是用反正切计算比例，确保一个数不超出你锁定的范围
# 要确定一个反正切函数，最少需要确定函数过某一个点，此处称为 锚点
#   变量x
#   锚点的x值
#   锚点的y值
#   y值上限

```  

 - 顺序多线程工具 Slaves  
```python
from angeltools.Slavers import Slaves
import time
import random

def do_add(args):
    x, y = args
    time.sleep(random.randint(1, 2))
    return x + y

data = [[x0, y0] for x0, y0 in zip(range(10, 20), range(1, 10))]
ts = time.time()

results = Slaves(workers=10).work(do_add, params_list=data)

te = time.time()
print(results, te - ts)

# Slaves start working: do_add
# [11, 13, 15, 17, 19, 21, 23, 25, 27] 2.007810354232788
```  
  
 - 顺序多进程工具 BigSlaves  
```python
from angeltools.Slavers import BigSlaves
import time
import random

def do_add(args):
    x, y = args
    time.sleep(random.randint(1, 2))
    return x + y

data = [[x0, y0] for x0, y0 in zip(range(10, 20), range(1, 10))]
ts = time.time()

results = BigSlaves().work(do_add, params_list=data)    # 默认进程数是当前系统可用进程-1

te = time.time()
print(results, te - ts)

# BigSlaves start working: do_add
# [11, 13, 15, 17, 19, 21, 23, 25, 27] 3.0164289474487305
```  

 - 其他工具
 1. 基于文件的异步锁

```python
# 由于文件io的延迟性，文件锁不适用于高并发的场景，也不能实现分布式，只适合单机器低速异步进程的隔离
# 优点是不需要数据库或第三方依赖，即开即用
# 高并发可以使用 python-redis-lock
from angeltools.StrTool import FileLock


def do_jobs():
    pass


with FileLock(lock_id='test-lock'):
    do_jobs()
```  

 2. url 组合拆解

```python
from angeltools.StrTool import UrlFormat

uf = UrlFormat(url='http://www.baidu.com?page=1&user=me&name=%E5%BC%A0%E4%B8%89')

uf.url_format(params_only=True, unquote_params=True)  # {'page': '1', 'user': 'me', 'name': '张三'}
uf.split_url()  # {'queries': {'page': '1', 'user': 'me', 'name': '张三'}, 'host': 'www.baidu.com', 'protocol': 'http', 'path': '', 'require_params': '', 'fragment': ''}
uf.make_url(
    'http://www.baidu.com', 
    params_add_dic={'page': '1', 'user': 'me','name': '张三'}
)  # 'http://www.baidu.com?page=1&user=me&name=%E5%BC%A0%E4%B8%89'
```


 3. scrapy 爬虫xpath包装  
```python
from angeltools.StrTool import ScrapyXpath
# 包装 scrapy response 的xpath方法，不用每次都 extract 再判断结果，使爬虫更整洁
# 也可以传入由 requests 获取的 response text 和 url，变成 scrapy selector 对象方便提取

import scrapy

div = scrapy.http.HtmlResponse().xpath('//div[@class="xxx"]')
sx = ScrapyXpath(scrapy_selector=div)
sx.xe('./@href')  # https://www.xxx.com
sx.xe('.//text()')  # ["abc", "efg", ...]     结果有多个时返回列表

# 或者
import requests

url = 'http://www.baidu.com'
html_content = requests.get(url)

sx = ScrapyXpath(url='http://www.baidu.com', html_content=html_content)
sx.xe('./@href')  # https://www.xxx.com
sx.xe('.//text()')  # ["abc", "efg", ...]     结果有多个时返回列表
```


 4. 图片转字符块工具  
```python
from angeltools.ImageTool import image2chars

image2chars(
    '/home/Angel.png',
    width=30,
    k=1.0,
    # outfile='/home/测试123.txt',
    reverse=True
)
"""
      - .                                               -   
    + @ #                                             . @ - 
    # # @ .     . + - + -       - + . -     . + -     . @ - 
  . @ - # =     + @ # # @ -   + @ # # @ . - @ * # *   . @ - 
  = @   = @     + @ .   @ =   # *   - @ . # # - = @ . . @ - 
  # @ @ @ @ -   + @     @ =   @ =   . @ . # # = = =   . @ - 
- @ + - - @ *   + @     @ =   * @ - * @ . * # . + *   . @ - 
= *       + *   - *     * +   . * @ * @ .   * # # -   . * . 
                              + = . + @ .                   
                              - # # # +                     
"""
```


 5. 文字转字符块工具  
```python
from angeltools.ImageTool import text2chars

text2chars(
    text="ANGEL",
    # font_path='/etc/fonts/msyh.ttf',
    width=50,
    k=0.6,
    # outfile='/home/测试123.txt',
    chart_list=[' ', '-', '/', '%'],
)
"""
        - -             - -         - -         - / / / -         - - / / / / / -     - -           
      / % % %           % % %       % % -   - % % / / / % % -     % % / / / / / -   - % /           
      % / / % -         % % % %     % % -   % % -         - -     % % -             - % /           
    % %     % %         % %   / % - / % -   % %       / % / /     % % % % % % %     - % /           
  - % % % % % % /       % %     / % % % -   % % -       - % %     % % -             - % /           
  % % -       % % -     % %       / % % -   - % % / / / % % %     % % % / / / / /   - % % / / / / - 
  -             - -     - -         - -         - / / / -   -     - - - - - - - -     - - - - - - -               
"""
```
  



 6. 使用redis的文件缓存器（模仿fdfs）  
```python
from angeltools.Db.redis_connector import RedisFdfs


conn = {
    "host": '127.0.0.1',
    "port": 6379,
    "password": None,
}
rdfs = RedisFdfs(
    db=1,                   
    connect_params=conn,    # redis 连接配置
    expire=30               # 缓存过期时间（默认1星期）
)

test_id = rdfs.upload('test data 001')
print(test_id)
# RedisFdfsFile_cceceb50-cc40-11ec-bb8b-adb0630c08c7

test_data = rdfs.get('RedisFdfsFile_cceceb50-cc40-11ec-bb8b-adb0630c08c7')
print(test_data)
# test data 001
# 没有结果或出错的时候返回空字符 ''

test_del = rdfs.delete('RedisFdfsFile_cceceb50-cc40-11ec-bb8b-adb0630c08c7')
print(test_del)
# True
```  
  


 - 终端工具  
  
1. 图片转字符块工具

```shell
ima2char [image] [-h 查看帮助]
```  
示例：
```shell
img2char /home/ABC.png -w 20
```
输出：
```text
                                . . .   
      *         = + = +       + + - + . 
    - = -     . +     = .   = .         
    + . =     . +     +   . +           
    +   + .   . = - = -   - -           
  - -   - +   . = . - = . - -           
  = + + + *   . +     . + . +           
. +       + .   +     - -   = .         
+ .       . +   = - + +       = + + + . 
                . . .           . .     
```  
  
  
2. 文字转字符块工具
```shell
txt2char [text] [-h 查看帮助]
```
  
例如：
```shell
txt2char ABC -w 30
```
  
输出
```text
        . .             . . . .                 . . .       
      - @ @ +         # @ @ @ @ @ *         + # @ @ @ * .   
      * @ @ #         # @ * = = # @ *     + @ @ = + # @ #   
      @ # # @ .       # @ .       @ @     @ @ -       # @ + 
    + @ = + @ =       # @ = + + * @ =   - @ #           .   
    # @ .   @ @       # @ @ @ @ @ @ .   + @ *               
  . @ @ - . # @ -     # @ + - - + @ #   - @ *               
  = @ @ @ @ @ @ *     # @ .       # @ . . @ @         = @ + 
  # @ = + + + @ @     # @ + - - + @ @ .   * @ * .   - @ @ . 
- @ #         * @ +   # @ @ @ @ @ @ +       # @ @ @ @ @ +   
. + .         . + -   - + + + + - .           + = * = .     
                                                            
```
