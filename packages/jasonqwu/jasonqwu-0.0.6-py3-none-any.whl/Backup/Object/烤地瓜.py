'''烤地瓜'''
class SweetPotato():
    '''地瓜类'''
    def __init__(self, name=None):
        if not hasattr(SweetPotato, "id"):
            SweetPotato.id = 1
        else:
            SweetPotato.id += 1
        self.name = name
        self.time = 0
        self.state = "生的"
        self.condiments = []

    def __str__(self):
        return f"{self.id}烤了 {self.time} 分钟。\n{self.name} 的状态是 {self.state}，调料有 {self.condiments}"

    def cook(self, time):
        self.time += time
        match self.time:
            case x if x < 3:
                self.state = "生的"
            case x if 3 <= x < 5:
                self.state = "半生不熟"
            case x if 5 <= x < 8:
                self.state = "熟了"
            case _:
                self.state = "烤糊了"

    def add(self, condiment):
        '''添加调料'''
        self.condiments.append(condiment)

    def remove(self, condiment):
        '''删除调料'''
        if condiment in self.condiments:
            self.condiments.remove(condiment)

def main():
    '''主函数'''
    sp = SweetPotato("sp")
    sp.cook(2)
    sp.add("酱油")
    print(sp)
    sp1 = SweetPotato()
    sp1.cook(2)
    sp1.cook(2)
    sp1.add("醋")
    sp1.add("辣椒")
    print(sp1)
    sp1.remove("醋")
    sp1.remove("油")
    print(sp1)

if __name__ == '__main__':
    main()
