class MakeCake:
    def __init__(self):
        self.formula = ""

    def __str__(self):
        return f"{self.formula}"

    def make_cake(self):
        print(f"运用{self.formula}制作煎饼果子。")

class Master(MakeCake):
    def __init__(self):
        self.formula = "[古法煎饼果子配方]"

    def make_cake(self):
        super().make_cake()

class School(MakeCake):
    def __init__(self):
        self.formula = "[黑马煎饼果子配方]"

    def make_cake(self):
        super().make_cake()

class Prentice(Master, School):
    def __init__(self):
        self.formula = "[独创煎饼果子配方]"
        self.__money = 2000000

    def get_money(self):
        return self.__money

    def set_money(self, money=2000000):
        self.__money = money

    def make_cake(self):
        self.__init__()
        print(f"运用{self.formula}制作煎饼果子。")

    def make_master_cake(self):
        Master.__init__(self)
        Master.make_cake(self)

    def make_school_cake(self):
        School.__init__(self)
        School.make_cake(self)

    def make_old_cake(self):
        super().__init__()
        super().make_cake()

class Tusun(Prentice):
    pass

def main():
    daqiu = Prentice()
    print(daqiu)
    daqiu.make_cake()
    print(Prentice.__mro__)
    daqiu.make_master_cake()
    daqiu.make_school_cake()
    daqiu.make_cake()
    daqiu.make_old_cake()
    xiaoqiu = Tusun()
    print(Tusun.__mro__)
    xiaoqiu.make_master_cake()
    xiaoqiu.make_school_cake()
    xiaoqiu.make_cake()
    print(xiaoqiu.get_money())
    xiaoqiu.set_money(500)
    print(xiaoqiu.get_money())

if __name__ == '__main__':
    main()
