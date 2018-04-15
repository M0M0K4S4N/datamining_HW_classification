import math
import random
import pandas as pd

learning_rate = 0.1
class Node:
    

    def __init__(self,object): # input is array of attribute
        count_in = len(object)
        self.input_attr = object
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
    
    def hiddenRoll(self,listFront,i,isOutput):
        out = 0
        for node in listFront:
            if(isOutput == True):
                out += node.W_in[i] * node.roll()
            else:
                out += node.W_in[i] * node.hiddenRoll()
            
            

    def changeInput(self,object):
        self.input_attr = object


class OutputNode(Node):
    def __init__(self, object, expectValue):
        Node.__init__(self,object)
        self.expect = expectValue
    
    def changeExpect(self,expect):
        self.expect = expect

    def error(self):
        return self.expect - self.Y()
    
    def roll(self):
        return (self.error() * self.Y() *(1 - self.Y()))

node = []
def initNode():
    listNode = []
    for i in range(3):
        listNode.append(Node([0,0,0,0]))
    node.append(listNode)

    listNode = []
    for i in range(4):
        listNode.append(OutputNode([0,0,0],0))
    node.append(listNode)

H = []
data = pd.read_csv('iris.csv')
initNode()

