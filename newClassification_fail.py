import math
import random
import pandas as pd

learning_rate = 0.1
nodeList = []
WNodeList = []
saveY = []
def initNode(inputAttrCount,hiddenlayerList,outputLayer):
    hiddenlayerList.append(outputLayer)

    for count in hiddenlayerList:
        tmp = []
        for i in range(count):
            tmp.append(random.random())
        nodeList.append(tmp)
        tmp = []
        for i in range(inputAttrCount * count):
            tmp.append(random.random())
        WNodeList.append(tmp)
        inputAttrCount = count    


def calcucateV(listInput,listWeight,nodeBias):
    V = 0
    for i in range(len(listInput)):
        V += listInput[i]*listWeight[i]
        #print(listInput[i]*listWeight[i])
    V += nodeBias
    return V

def calculateY(V):
    return 1/(1+math.exp(-V))

def rollOutput(Y,error):
    return error*Y*(1-Y)

def calculateF(Y):
    return Y*(1-Y)

def parseBinary(value):
    if(abs(1-value) < abs(0-value)):
        return 1
    else:
        return 0
def outputParsing(output):
    for i in range(len(output)):
        output[i] = parseBinary(output[i])
    return output

initNode(4,[2],2)
data = pd.read_csv('iris-train.csv')
maxHop = 1
for hop in range(maxHop):
    print("Training " + str(hop*100 / maxHop)+"%")
    for dataCount in range(len(data['attr1'])):
        saveY = []
        inputData = [data['attr1'][dataCount],data['attr2'][dataCount],data['attr3'][dataCount],data['attr4'][dataCount]]
        inputList = inputData
        if(data['attr6'][dataCount] == 1):
            expectOutput = [0,0]
        elif(data['attr6'][dataCount] == 2):
            expectOutput = [0,1]
        elif(data['attr6'][dataCount] == 3):
            expectOutput = [1,0]
        elif(data['attr6'][dataCount] == 4):
            expectOutput = [1,1]
        #print(inputList)
        
        for layerCount in range(len(nodeList)):
            output = []
            nodeInLayer = len(nodeList[layerCount])
            WeightToNode =(int)(len(WNodeList[layerCount]) / nodeInLayer)
            wInterrest = 0
            for nodeCount in range(nodeInLayer):
                lastInterest = wInterrest + WeightToNode +2
                #print(WNodeList[layerCount][wInterrest:lastInterest])
                V = calcucateV(inputList,WNodeList[layerCount][wInterrest:lastInterest],nodeList[layerCount][nodeCount])
                Y = calculateY(V)
                output.append(Y)
                #print("----")
            saveY.append(output)
            inputList = output
            # print("---")
        
        #break
        print(str(output) + " - " + str(expectOutput))

        error = []
        for outputCount in range(len(output)):
            #print(expectOutput[outputCount] - output[outputCount])
            error.append(expectOutput[outputCount] - output[outputCount])
        

        saveRoll = []
        nodeList = list(reversed(nodeList))
        WNodeList = list(reversed(WNodeList))
        saveY = list(reversed(saveY))
        newNodeList = nodeList
        newWNodeList = WNodeList
        for i in range(len(nodeList)):
            
            if(i == 0):
                roll = []
                for errCount in range(len(error)):
                    roll.append(rollOutput(output[errCount],error[errCount]))
                saveRoll.append(roll)
                
            else:
                roll = []

                Wstart = 0
                Wstep = int(len(WNodeList) / len(saveY[i]))
                for Ycount in range(len(saveY[i])):
                    sum = 0
                    WNow = Wstart
                    for nodeCount in range(len(nodeList[i-1])):
                        sum += saveRoll[i-1][nodeCount] * WNodeList[i-1][WNow]
                        WNow += Wstep
                    Y = saveY[i][Ycount]
                    roll.append(Y*(1-Y)*sum)
                    Wstart += 1
                saveRoll.append(roll)
        #print(saveRoll)
        saveY.append(inputData)
        for i in range(len(nodeList)):
            WPerNode = int(len(WNodeList[i]) / len(nodeList[i]))
            Wstart = WPerNode
            for j in range(len(nodeList[i])):
                nodeList[i][j] += (-(learning_rate)*saveRoll[i][j]*saveY[i][j])
            nowRoll = 0
            for j in range(len(WNodeList[i])):
                #print("-"+str(WPerNode))
                #print(j%WPerNode)
                WNodeList[i][j] += (-(learning_rate)*saveRoll[i][nowRoll]*saveY[i+1][j%WPerNode])
                if(j == WPerNode -1):
                    Wstart = WPerNode + Wstart
                    nowRoll += 1

        nodeList = list(reversed(nodeList))
        WNodeList = list(reversed(WNodeList))
        saveY = list(reversed(saveY)) 


data = pd.read_csv('iris-test.csv')
allDataCount = len(data['attr1'])
correctCount = 0
for dataCount in range(len(data['attr1'])):
        #saveY = []
    inputData = [data['attr1'][dataCount],data['attr2'][dataCount],data['attr3'][dataCount],data['attr4'][dataCount]]
    inputList = inputData
    if(data['attr6'][dataCount] == 1):
        expectOutput = [0,0]
    elif(data['attr6'][dataCount] == 2):
        expectOutput = [0,1]
    elif(data['attr6'][dataCount] == 3):
        expectOutput = [1,0]
    elif(data['attr6'][dataCount] == 4):
        expectOutput = [1,1]
    #print(inputList)
        
    for layerCount in range(len(nodeList)):
        output = []
        nodeInLayer = len(nodeList[layerCount])
        WeightToNode =(int)(len(WNodeList[layerCount]) / nodeInLayer)
        wInterrest = 0
        for nodeCount in range(nodeInLayer):
            lastInterest = wInterrest + WeightToNode +2
            #print(WNodeList[layerCount][wInterrest:lastInterest])
            V = calcucateV(inputList,WNodeList[layerCount][wInterrest:lastInterest],nodeList[layerCount][nodeCount])
            Y = calculateY(V)
            output.append(Y)
            #print("----")
        #saveY.append(output)
        inputList = output
    #output = outputParsing(output)
    if(output == expectOutput):
        correctCount += 1
    #print(str(output) + " - " + str(expectOutput))


print("Correct -- " + str(correctCount*100 / allDataCount) + "%")






