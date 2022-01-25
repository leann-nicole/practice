class Test:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def printMessage(self):
        print('Name: '+self.name)
        print('Age: '+self.age)

t1 = Test()
t1.printMessage()