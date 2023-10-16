import random as r
import re


def get_a_char(char_type):
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = "abcdefghijklmnopqrstuvwxyz"
    digital = "0123456789"
    special = "!@#$%^&*"
    if char_type == "upper":
        return r.choice(upper)
    elif char_type == "lower":
        return r.choice(lower)
    elif char_type == "digital":
        return r.choice(digital)
    else:
        return r.choice(special)


def make_password(min=6, max=20):
    full = ["upper", "lower", "digital", "special"]
    pw_len = r.randint(min, max)
#    print(pw_len)
    ret = ""
    for _ in range(pw_len):
        #        print(get_a_char(r.choice(full)))
        ret += get_a_char(r.choice(full))
    print(ret)
    return ret


def check_password(password, min=6, max=20):
    '''
        验证密码是否满足条件
        1. 长度位于[6, 20]之间
        2. 必须包含至少一个小写字母
        3. 必须包含至少一个大写字母
        4. 必须包含至少一个数字
        5. 必须包含至少一个特殊字符

        返回
            正确
            错误原因
    '''
    if len(password) < min:
        return "密码长度太短"
    elif len(password) > max:
        return "密码长度太长"
    elif not re.findall(r"[a-z]", password):
        return "没有小写字母"
    elif not re.findall(r"[A-Z]", password):
        return "没有大写字母"
    elif not re.findall(r"\d", password):
        return "没有数字"
    elif not re.findall(r"[^A-Za-z0-9]", password):
        return "没有特殊字符"
    else:
        return "正确"


if __name__ == "__main__":
    print(check_password(make_password()))
