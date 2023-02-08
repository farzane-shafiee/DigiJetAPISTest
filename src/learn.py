


class Farzan:

    def __init__(self, name, age):

        self.name = name
        self.age = age

    def show(self):
        print(f"{self.name} - {self.age}")


class Bahram(Farzan):
    pass
    # def show(self):
    #     print("my name is bahram")
p = Bahram(name="bahram", age=30)
p.show()