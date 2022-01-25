# Binary Search Tree Sort script

import sys

if "/home/leann/Desktop" not in sys.path:
    sys.path.append("/home/leann/Desktop/Python files")

from node import *

def addToTree(root, node):
    stepper = root
    while 1:
        parent = stepper;
        if (node.getData() <= stepper.getData()):
            if(stepper.leftChild == None):
                parent.leftChild = node
                break
            stepper = stepper.leftChild
        else:
            if(stepper.rightChild == None):
                parent.rightChild = node
                break
            stepper = stepper.rightChild


def traverseTree(root):
    if(root != None):
        traverseTree(root.leftChild)
        root.printData()
        traverseTree(root.rightChild)

root = Node(2)

node1 = Node(-1)
node2 = Node(2)
node3 = Node(31)
node4 = Node(0)
node5 = Node(1)
node6 = Node(3)
node7 = Node(4)
node8 = Node(8)

myNodeList = [Node(2), node1, node2, node3, node4, node5, node6, node7, node8]

for node in myNodeList:
    addToTree(root, node)

traverseTree(root)
