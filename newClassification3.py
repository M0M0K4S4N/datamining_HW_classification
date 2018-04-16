import math
import random
import pandas as pd

learning_rate = 0.1
nodeList = []
weightList = []

def calculateY(inputList,weightList,nodeBias):
    V = 0
    for i in range(len(inputList)):
        V += inputList[i]*weightList[i]
    V += nodeBias
    return 1/(1+math.exp(-V))

def calculateFprime(Y):
    return Y*(1-Y)

def binaryParse(listOutput):
    out = listOutput
    for i in range(len(out)):
        if(abs(1-out[i]) < abs(0-out[i])):
            out[i] = 1
        else:
            out[i] = 0
    return out

def initNode(layerCount,nodeInlayerList): #node include input node
    
    for i in range(layerCount):
        node = []

        for j in range(nodeInlayerList[i+1]):
            node.append(random.random())
           
        weight = []
        for k in range(nodeInlayerList[i]*nodeInlayerList[i+1]):
            weight.append(random.random())
        weightList.append(weight)   
        nodeList.append(node)


# nodeList.append([0.2,0.4])
# nodeList.append([0.1,0.2])

# weightList.append([0.3,0.1,0.2,0.1,0.2,0.2,0.1,0.3])
# weightList.append([0.1,0.1,0.2,0.2])
#data = [[1,0,1,1]]

initNode(2,[15,3,2])
data = []
expect = []
loadData = pd.read_csv('autism-child-data-train.csv',header=None)

# data must have class at last attribute
# number of all attr
numberOfAttr = 15

for i in range(len(loadData[0])):
    tmp = []
    for j in range(numberOfAttr):
        tmp.append(loadData[j][i])
    expect.append(loadData[numberOfAttr][i])
    data.append(tmp)


expectOutput = [1,0]
maxTrain = 300

for hop in range(maxTrain):
    print(hop * 100 / maxTrain)

    for dataCount in range(len(data)):

        if(expect[dataCount] == 0):
            expectOutput = [1,0]
        elif(expect[dataCount] == 1):
            expectOutput = [0,1]
        
        
        saveY = []
        error = []

        inputNextNode = data[dataCount]
        # Y calc
        for layer in range(len(nodeList)):
            output = []
            weightToNode = int(len(weightList[layer]) / len(nodeList[layer]))
            startNeedWeight = 0
            for nodeCount in range(len(nodeList[layer])):
                lastNeedWeight = startNeedWeight + weightToNode +2
                Y = calculateY(inputNextNode,weightList[layer][startNeedWeight:lastNeedWeight],nodeList[layer][nodeCount])
                startNeedWeight += weightToNode
                output.append(Y)
            inputNextNode = output
            saveY.append(output)
            #print(output)

        #error calc
        for i in range(len(output)):
            error.append( output[i] - expectOutput[i] )
        #print(error)
        
        saveY =  list(reversed(saveY))
        saveY.append(data[dataCount])
        nodeList = list(reversed(nodeList))
        weightList = list(reversed(weightList))
        #print(weightList)
        listRoll = []
        #roll calc
        for layer in range(len(nodeList)):
            roll = []
            for nodeCount in range(len(nodeList[layer])):
                if(layer == 0):
                    roll.append(error[nodeCount] * calculateFprime(saveY[layer][nodeCount]))
                else:
                    sum = 0
                    
                    weightToNode = int(len(weightList[layer-1]) / len(nodeList[layer]))
                    weightCurrent = nodeCount
                    for beforeRoll in range(len(listRoll[layer-1])):
                        #print(str(listRoll[layer-1][beforeRoll]) + " * " +str(weightList[layer-1][weightCurrent]))
                        #print(listRoll[layer-1][beforeRoll]*weightList[layer][weightCurrent])
                        val = (listRoll[layer-1][beforeRoll]*weightList[layer-1][weightCurrent])
                        sum += val
                        weightCurrent += weightToNode
                    #print(sum)
                    roll.append(calculateFprime(saveY[layer][nodeCount]) * sum)
            listRoll.append(roll)
        
        for layer in range(len(weightList)):
            node = 0
            weightToNode = int(len(weightList[layer]) / len(nodeList[layer]))
            weightEnd = weightToNode 
            for weightCount in range(len(weightList[layer])):
                weightList[layer][weightCount] += (-learning_rate)*(listRoll[layer][node])*(saveY[layer+1][weightCount%weightToNode])
                if(weightCount == weightEnd -1):
                    node += 1
                    weightEnd += weightToNode
            
            for nodeCount in range(len(nodeList[layer])):
                nodeList[layer][nodeCount] += (-learning_rate)*(listRoll[layer][nodeCount])
    
        nodeList = list(reversed(nodeList))
        weightList = list(reversed(weightList))
    print(nodeList)
    print(weightList)



data = []
expect = []
loadData = pd.read_csv('autism-child-data-test.csv',header=None)
for i in range(len(loadData[0])):
    tmp = []
    for j in range(numberOfAttr):
        tmp.append(loadData[j][i])
    expect.append(loadData[numberOfAttr][i])
    data.append(tmp)

correct = 0
all = len(loadData[0])
#print(expect)
#------test 
for dataCount in range(len(data)):
    #print(expect[dataCount])
    if(expect[dataCount] == 0):
        expectOutput = [1,0]
    elif(expect[dataCount] == 1):
        expectOutput = [0,1]
 
        
    #print(expectOutput)
    saveY = []
    error = []
    #saveRoll = []
    inputNextNode = data[dataCount]
    # Y calc
    for layer in range(len(nodeList)):
        output = []
        weightToNode = int(len(weightList[layer]) / len(nodeList[layer]))
        startNeedWeight = 0
        for nodeCount in range(len(nodeList[layer])):
            lastNeedWeight = startNeedWeight + weightToNode +2
            Y = calculateY(inputNextNode,weightList[layer][startNeedWeight:lastNeedWeight],nodeList[layer][nodeCount])
            startNeedWeight += weightToNode
            output.append(Y)
        inputNextNode = output
    print(output)
    #output = list(reversed(output))
    if(binaryParse(output) == expectOutput):
        correct += 1
    print(str(output) + " - " + str(expectOutput) )

print(correct / all)