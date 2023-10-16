import ipdb

class House():
    def __init__(self, name=None, area=None, furniture=None):
        if not hasattr(House, "id"):
            House.id = 0
        else:
            House.id += 1
        self.name = name
        self.area = area
        self.free_area = area
        self.furniture = []

    def __str__(self):
        return f"{self.id}, {self.name}, {self.area}, {self.free_area}, {self.furniture}"

    def add(self, item):
        if self.free_area >= item.area:
            self.free_area -= item.area
            self.furniture.append(item.name)
        else:
            print(f"{item.name} 太大，剩余面积不足，无法容纳。")

    def remove(self, item):
        self.furniture.remove(item.name)
        self.free_area += item.area

class Furniture():
    def __init__(self, name=None, type=None, area=None):
        if not hasattr(Furniture, "id"):
            Furniture.id = 0
        else:
            Furniture.id += 1
        # ipdb.set_trace()
        self.name = name
        self.type = type
        self.area = area

    def __str__(self):
        return f"{self.id}, {self.name}, {self.type}, {self.area}"

def main():
    bed = Furniture("bed", "双人床", 6)
    print(bed)
    sofa = Furniture("sofa", "沙发", 10)
    print(sofa)
    h1 = House("h1", 1000)
    print(h1)
    h1.add(bed)
    print(h1)
    h1.add(sofa)
    print(h1)
    h1.remove(bed)
    print(h1)
    ball = Furniture("ball", "篮球场", 2000)
    h1.add(ball)
    print(h1)

if __name__ == '__main__':
    main()
