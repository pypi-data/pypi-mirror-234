class LivingThings:
    def __init__(self, name=None, gender=None):
        self.name = name
        self.gender = gender
        self.attack = 15
        self.life = 100

class Weapon:
    def stick(self, obj, attack=40):
        self.name = "打狗棒"
        self.attack = attack
        obj.life -= self.attack
        self.show(obj)

    def knife(self, obj, attack=80):
        self.name = "屠龙刀"
        self.attack = attack
        obj.life -= self.attack
        self.show(obj)

    def gun(self, obj, attack=100):
        self.name = "AK47"
        self.attack = attack
        obj.life -= self.attack
        self.show(obj)

    def show(self, obj):
        print(f"[{obj.name}]被[{self.name}]攻击了，掉血[{self.attack}]，还剩血量[{obj.life}]...")

class Person(LivingThings):
    def __init__(self, name=None, gender=None, age=None):
        super().__init__(name, gender)
        if not hasattr(Person, "person_id"):
            Person.person_id = 0
        else:
            Person.person_id += 1
        self.id = self.person_id
        self.age = age
        self.weapon = Weapon()
        self.attack = 3
        if self.age > 18:
            self.attack = 5

    def __str__(self):
        return f"{self.id}, {self.name}, {self.gender}, {self.age}, {self.attack}, {self.life}"

    def beat(self, dog=None):
        if type(dog) != Dog:
            print("{} 不是一条狗。".format(dog.name))
            return
        dog.life -= self.attack
        print(f"人 {self.name} 打了狗 {dog.name} 一棒，狗掉血 {self.attack}，还剩血量 {dog.life}")

    def work_with_dog(self, dog):
        dog.work()

class Dog(LivingThings):
    __tooth = 10

    @classmethod
    def get_tooth(cls):
        return cls.__tooth

    @classmethod
    def set_tooth(cls, tooth=10):
        cls.__tooth = tooth

    @staticmethod
    def info_print():
        print("这是一个狗类，用于创建狗实例...")

    def __init__(self, name=None, gender=None, age=None, breed=None, master=None):
        super().__init__(name, gender)
        if not hasattr(Dog, "dog_id"):
            Dog.dog_id = 0
        else:
            Dog.dog_id += 1
        self.id = self.dog_id
        self.attack_table = {
            "京巴": 30,
            "藏獒": 80
        }
        # ipdb.set_trace()
        self.age = age
        self.breed = breed
        self.master = master
        if self.breed in self.attack_table:
            self.attack = self.attack_table[breed]
        self.life = 10

    def __str__(self):
        return f"{self.id}, {self.__tooth}, {self.name}, {self.gender}, {self.age}, {self.breed}, master = {self.master}, attack = {self.attack}, {self.life}"

    def bite(self, person=None):
        if type(person) != Person:
            print("{} 不是一个人。".format(person.name))
            return
        person.life -= self.attack
        print(f"狗 {self.name} 咬了人 {person.name} 一口，人掉血 {self.attack}，还剩血量 {person.life}")

    def work(self):
        print("指哪打哪...")

class ArmyDog(Dog):
    def work(self):
        print("追击敌人...")

class DrugDog(Dog):
    def work(self):
        print("追查毒品...")

def main():
    p1 = Person("Alex", "女", 22)
    print(p1)
    p2 = Person("Mike", "男", 17)
    print(p2)
    d1 = Dog("mjj", "母", 5, "京巴", p1)
    print(d1)
    d2 = Dog("mjj2", "公", 3, "藏獒", p2)
    print(d2)
    d3 = Dog("mjj3", "公", 10, "日本田园")
    print(d3)
    d1.bite(d2)
    p1.beat(d1)
    p1.weapon.stick(d1)
    p1.weapon.knife(d1)
    p1.weapon.gun(d1)
    ad = ArmyDog()
    dd = DrugDog()
    p2.work_with_dog(ad)
    p2.work_with_dog(dd)
    print(ad.get_tooth())
    ad.set_tooth(30)
    print(ad.get_tooth())
    ad.info_print()
    Dog.info_print()

if __name__ == '__main__':
    main()
