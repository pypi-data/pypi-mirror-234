import jieba as jb
import re
from jasonqwu_lib import *

content = '''
    大家好，最近常常有粉丝问我，入坑数据分析师靠谱吗？前景如何？怎么入手？有没有相关系统学习资源？对我现在的工作有什么帮助？
    等等一系列问题...今天就来详细说一说！
    如今我们已经身处大数据时代。我们的一言一行都产生着大量数据，而这些数据也在改变着我们的生活，数据中更是蕴藏着不菲商业价值。
'''
content = re.sub(r"[\s，.？！]", '', content)
word_list = jb.cut(content)
debug(set(list(word_list)))
