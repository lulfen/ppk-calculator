from operator import itemgetter

resultDB = []
with open("data/ppk.txt", 'r') as ppkRawCalc :
    ppkRawLabels = ppkRawCalc.readline()
    ppkLabels = ppkRawLabels.split(",")
    ppkRawLines = ppkRawCalc.readlines()
    
lnInd=0
for ppkLine in ppkRawLines :
    ppkLineCurr = ppkLine.split(",")
    for attr in ppkLineCurr :
        aInd = ppkLineCurr.index(attr)
        if aInd > 0 :
             decCheck = float("{0:.5f}".format(float(attr)))
             if decCheck.is_integer() :
                 ppkLineCurr[aInd] = int(float(attr))
             else :
                 ppkLineCurr[aInd] = decCheck
    resultDB.append(ppkLineCurr)

sortValue = 4

longList =[]
for label in ppkLabels :
    longList.append(len(label))
longValue = 0
if sortValue == 0 :
    displayData = sorted(resultDB, key=itemgetter(sortValue))
else :
    displayData = sorted(resultDB, key=itemgetter(sortValue), reverse=True)
for punsch in displayData :
    for value in punsch :
        #print(value)
        valInd = punsch.index(value)
        if len(str(value)) > longList[valInd] :
            longList[valInd] = len(str(value))
            
#nameLabel = ppkLabels[0].ljust(int(longList[0]))
labelLine = ""
for label in ppkLabels :
    labelCurr = label.ljust(longList[ppkLabels.index(label)] + 2)
    labelLine = labelLine + labelCurr
print(labelLine)
#print(nameLabel, ppkLabels[1], "\t", ppkLabels[2], "\t", ppkLabels[3], "\t", ppkLabels[4], "\t", ppkLabels[5][:-1])
for punsch in displayData :
    labelLine = ""
    for label in punsch :
        labInd = punsch.index(label)
        #print(labInd, " ", longList[labInd])
        labelStr = str(label)
        #print(labelStr,"!")
        labelCurr = labelStr.ljust(longList[labInd]+2)# int(longList[labInd]))
        #print(labelStr,"?")
        labelLine = labelLine + labelCurr
    print(labelLine)
#    print("\n")
#    namn = punsch[0].ljust(int(longList[0]))
#    print(namn, punsch[1], "\t", punsch[2], "\t", punsch[3], "\t", punsch[4], "\t", punsch[5], "\t")
    
