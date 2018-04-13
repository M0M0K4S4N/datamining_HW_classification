import math
import random

class Node:
    def __init__(self,object): # input is array of attribute
        count_in = len(object)
        self.changeInput(object)
        self.W_in = []
        self.bias = random.random()
        for i in range(count_in):
            self.W_in.append(random.random())
    
    def V(self):
        out = 0
        for i in range(len(self.W_in)):
            out = out + (self.W_in[i] * self.input_attr[i])
        out = out + self.bias
        return out

    def Y(self):
        return 1/(1+math.exp(- self.V()))

    def changeInput(self,object):
        self.input_attr = object


class OutputNode:
    def __init__(self,object):
        Node.__init__(self,object)
    


x = Node(4)
print(x.W_in)

