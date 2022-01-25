# a Node class

class Node:
    
    def __init__(self, number):
        self.data = number
        self.leftChild = None
        self.rightChild = None

    def getData(self):
        return self.data
    def printData(self):
        print(self.data," ",end = '')
