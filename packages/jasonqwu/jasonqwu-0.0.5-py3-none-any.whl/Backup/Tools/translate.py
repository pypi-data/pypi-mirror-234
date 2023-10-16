#
# -*- coding: UTF-8 -*-
# @author Jason Q. Wu
# @create 2021-04-30 14:48
#
# import pyforest
import sys
import requests
import json
from jasonqwu_lib import Config

# 设置文件的读写
config_name = sys.argv[0][:-3] + ".ini"
cfg = Config(config_name.encode('utf-8').decode('utf-8'))
cfg.read_config()
config = cfg.get_config()
config["Default"]["passwd"] = "654321"
cfg.set_config(config)
cfg.write_config()
#cfg.show_config()

post_url = "https://fanyi.baidu.com/sug"
# post_url = "https://fanyi.baidu.com/langdetect"
# post_url = "https://miao.baidu.com/abdr"
# post_url = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"
# post_url = "https://miao.baidu.com/abdr"
# post_url = "https://fanyi.baidu.com/pcnewcollection?req=check&fanyi_src=dog&direction=en2zh&_=1619769503754"

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"
}
# headers = {
# "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
# }
word = input("请输入一个单词：")
data = {
    # "from": "en",
    # "to": "zh",
    "kw": word,
    # "query": word,
    # "simple_means_flag": 3,
    # "sign": "871501.634748",
    # "token": "52fb205ec8206671c5bcd11af516e5b8",
    # "domain": "common"
}

response = requests.post(url=post_url, data=data, headers=headers)
dic_obj = response.json()
print(dic_obj)
#file_name = word + ".json"
#with open(file_name, 'w', encoding="utf8") as fp:
#    json.dump(dic_obj, fp=fp, ensure_ascii=False)
#print("Over!!")
