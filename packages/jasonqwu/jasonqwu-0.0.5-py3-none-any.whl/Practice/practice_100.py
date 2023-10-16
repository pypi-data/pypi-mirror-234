from Jasonqwu import *


class Function:
    def function00():
        for i in trange(100, desc="训练", unit="epoch"):
            time.sleep(0.1)

    def function01():
        number1 = Tool.get_float()
        number2 = Tool.get_float()
        debug(f"{number1:.2f} + {number2:.2f} = {number1 + number2:.2f}")


def function02():
    pass


def function03():
    pass


func = {
    0: Function.function00,
    1: Function.function01,
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="运行从 begin 到 end 范围的函数")
    parser.add_argument("-b", "--begin", type=int, default=0,
                        metavar='', help="范围的起始值")
    parser.add_argument("-e", "--end", type=int, default=2,
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
