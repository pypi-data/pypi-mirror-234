from Jasonqwu import *


class Function:
    @Timer(10_000)
    def function00():
        count = 0
        numbers = []
        for i in range(1, 5):
            for j in range(1, 5):
                for k in range(1, 5):
                    if (i != j) and (i != k) and (j != k):
                        count += 1
                        numbers.append((i, j, k))
        return count, numbers

    @Timer(10_000)
    def function01():
        count = 0
        numbers = []
        for i in range(1, 5):
            for j in range(1, 5):
                if j == i:
                    continue
                for k in range(1, 5):
                    if k == i or k == j:
                        continue
                    if (i != j) and (i != k) and (j != k):
                        count += 1
                        numbers.append((i, j, k))
        return count, numbers

    def function02():
        profit = Tool.get_int(0, 1_200_000)
        bonus1 = 100_000 * 0.1
        bonus2 = bonus1 + 100_000 * 0.075
        bonus3 = bonus2 + 200_000 * 0.05
        bonus4 = bonus3 + 400_000 * 0.03
        bonus5 = bonus4 + 600_000 * 0.015
        bonus6 = bonus5 + 1_000_000 * 0.01
        if profit <= 100_000:
            bonus = profit * 0.1
        elif profit <= 200_000:
            bonus = bonus2 - (100_000 - profit) * 0.075
        elif profit <= 400_000:
            bonus = bonus3 - (400_000 - profit) * 0.05
        elif profit <= 600_000:
            bonus = bonus4 - (600_000 - profit) * 0.03
        elif profit <= 1_000_000:
            bonus = bonus5 - (1_000_000 - profit) * 0.015
        else:
            bonus = bonus6 + profit * 0.01
        debug(f"profit = {profit}")
        debug(f"Total bonus = {bonus}")

    def function03():
        square = Tool.get_int(0, 20_000)
        judge1 = math.sqrt(square + 100) * \
            math.sqrt(square + 100) == square + 100
        judge2 = math.sqrt(square + 268) * \
            math.sqrt(square + 268) == square + 268
        if judge1 and judge2:
            debug(f"完全平方数 = {square}")
        else:
            debug(f"{square} 不是完全平方数")

    def function04():
        year = Tool.get_int(1900, 2100)
        if is_leap_year(year):
            days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month = Tool.get_int(1, 12)
        days = 0
        for i in range(month - 1):
            days += days_in_month[i]
        max_day = get_days_in_month(year, month)
        day = Tool.get_int(0, 31)
        while day > max_day:
            day = Tool.get_int(0, 31)
        days += day
        debug(f"{year}年{month}月{day}日 = 第{days}天")

    def function05():
        array = Tool.get_array()
        select_sort(array)
        debug(f"array = {array}")

    def function06():
        debug("Hello Python world!")
        debug("*" * 10)
        for i in range(5):
            debug("*")
        debug("*" * 10)

    def function07():
        a = 176
        b = 219
        debug(f"{chr(b),chr(a),chr(a),chr(a),chr(b)}")
        debug(f"{chr(a),chr(b),chr(a),chr(b),chr(a)}")
        debug(f"{chr(a),chr(a),chr(b),chr(a),chr(a)}")
        debug(f"{chr(a),chr(b),chr(a),chr(b),chr(a)}")
        debug(f"{chr(b),chr(a),chr(a),chr(a),chr(b)}")

    def function08():
        for i in range(1, 10):
            result = []
            for j in range(1, i + 1):
                result.append(f"{i} * {j} = {i * j:2d}")
            debug(result)

    def function09():
        for i in range(8):
            result = []
            for j in range(8):
                if (i + j) % 2 == 0:
                    result.append(f"{chr(219)}")
                else:
                    result.append(f" ")
            debug(result)

    def function10():
        for i in range(1, 11):
            result = [0]
            for j in range(1, i):
                result.append(0)
            debug(result)

    def function11():
        f1 = 1
        f2 = 1
        result = []
        for i in range(1, 21, 2):
            result.append(f1)
            result.append(f2)
            f1 += f2
            f2 += f1
        debug(result)

    def function12():
        counter = 0
        result = []
        start = Tool.get_int(0, 500)
        stop = Tool.get_int(0, 500)
        while stop < start:
            stop = Tool.get_int(0, 500)
        for i in range(start, stop + 1):
            if Tool.is_prime(i):
                counter += 1
                result.append(i)
        debug(f"{start} 到 {stop} 之间共有 {counter} 个素数：")
        debug(f"{result}")

    def function13():
        counter = 0
        result = []
        for n in range(100, 1000):
            i = int(n / 100)
            j = int(n / 10 % 10)
            k = int(n % 10)
            if n == i ** 3 + j ** 3 + k ** 3:
                counter += 1
                result.append(n)
        debug(f"三位数共有 {counter} 个水仙花数：")
        debug(f"{result}")

    def function14():
        start = 0
        stop = 100
        num = number = Tool.get_int(start, stop)
        primes = []
        result = ""
        for i in range(2, int((stop - start) / 2)):
            while Tool.is_prime(i) and number % i == 0:
                number = int(number / i)
                primes.append(i)
        for i in range(len(primes)):
            if i == 0:
                result = f"{primes[i]}"
            else:
                result += (f" * {primes[i]}")
        if result == "":
            debug(f"{num} = {num}")
        else:
            debug(f"{num} = {result}")

    def function15():
        score = Tool.get_int(0, 100)
        if score >= 90:
            grade = 'A'
        elif score >= 60:
            grade = 'B'
        else:
            grade = 'C'
        debug(f"{score} belongs to {grade}")

    def function16():
        c1 = Caculator(2)
        c1.add(6).sub(4).mul(5).div(4).print().add(5).print()
        # engine = pyttsx3.init()
        # txt = "I hope you can realize your dream as soon as possible."
        # engine.save_to_file(txt, "access.mp3")
        # engine.runAndWait()

    def function17():
        s = "There are many digits 12345 in the string.\n"
        letters = 0
        space = 0
        digit = 0
        others = 0
        for c in s:
            if c.isalpha():
                letters += 1
            elif c.isspace():
                space += 1
            elif c.isdigit():
                digit += 1
            else:
                others += 1
        debug(f"letters: {letters}, space = {space}, " +
              f"digit = {digit}, others = {others}")

    def function18():
        tn = 0
        sn = []
        n = Tool.get_int(5, 10)
        a = Tool.get_int(1, 9)
        for count in range(n):
            tn += a
            a *= 10
            sn.append(tn)
            debug(tn)
        sn = reduce(lambda x, y: x + y, sn)
        debug(f"result = {sn}")


def function19():
    pass


def function20():
    pass


func = {
    0: Function.function00,
    1: Function.function01,
    2: Function.function02,
    3: Function.function03,
    4: Function.function04,
    5: Function.function05,
    6: Function.function06,
    7: Function.function07,
    8: Function.function08,
    9: Function.function09,
    10: Function.function10,
    11: Function.function11,
    12: Function.function12,
    13: Function.function13,
    14: Function.function14,
    15: Function.function15,
    16: Function.function16,
    17: Function.function17,
    18: Function.function18,
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="运行从 begin 到 end 范围的函数")
    parser.add_argument("-b", "--begin", type=int, default=0,
                        metavar='', help="范围的起始值")
    parser.add_argument("-e", "--end", type=int, default=19,
                        metavar='', help="范围的结束值")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-q", "--quiet", action="store_true",
                       help="print quiet")
    group.add_argument("-v", "--verbose", action="store_true",
                       help="print verbose")
    args = parser.parse_args()
    for i in range(args.begin, args.end):
        debug(f"======================{i:02d}======================")
        if args.quiet:
            debug("quiet")
        elif args.verbose:
            debug("verbose")
        else:
            debug("normal")
        func[i]()
