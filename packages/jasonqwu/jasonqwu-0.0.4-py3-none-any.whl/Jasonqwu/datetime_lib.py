#
# -*- coding: UTF-8 -*-
# @author Jason Q. Wu
# @create 2021-04-29 09:39
#
__all__ = ["get_days_in_month",
           "get_week_with_date",
           "is_leap_year"]


def get_days_in_month(year, month):
    ''' 获取指定月份的天数 '''
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 29 if is_leap_year(year) else 28


def get_week_with_date(y, m, d):
    ''' 根据年月日计算星期几 '''
    # 把 1、2 月当做上一年的 13、14 月使用
    y = y - 1 if m == 1 or m == 2 else y
    m = m + 12 if m == 1 or m == 2 else m

    # 使用公式计算出星期几并返回
    w = (d + 2 * m + 3 * (m + 1) // 5 + y +
         y // 4 - y // 100 + y // 400) % 7 + 1
    return w


def is_leap_year(year):
    ''' 判断一个年份是否是闰年 '''
    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
        return True
    return False
