import os
import bs4
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
from shutil import get_terminal_size
from pathlib import Path
from operator import itemgetter

def downloadData() :
    urllib.request.retrieve('https://www.systembolaget.se/api/assortment/products/xml', './data/punschRawInput')

def calculatePPK(inputCheckInternal) :
    if inputCheckInternal == True :
        print('parsing input (this might take a little while)')
        with open('punschRawInput', 'r') as input :
            soup = BeautifulSoup(input, 'xml')
        
        print("parsing complete")

        output = open('ppk.txt', 'w+')
        print('creating output file')
        output.write('Namn,Pris,Volym,Alkoholhalt,APK,PPK\n')
        for drinkType in soup.find_all('Varugrupp') :
            if drinkType.string == 'Punsch' :        
                for info in drinkType.parent :
                    if info.name == 'Namn' :
                        output.write(info.string + ',')
                    if info.name == 'Prisinklmoms' :
                        pris = int(float(info.string))
                        output.write(str(pris) + ',')
                    if info.name == 'Volymiml' :
                        volym = float('{0:.2f}'.format(float(info.string)))
                        output.write(str(volym) + ',')
                    if info.name == 'Alkoholhalt' :
                        procent = int(float(info.string[:-1]))/100
                        output.write(str(procent) + ',')
                apk = ((procent*volym)/pris)
                output.write(str(apk) + ',')
                output.write(str(volym/pris) + "\n")

	output.close()
        return True
    else :
        print("It seems that something is wrong with the input. Try downloading again.")
        return False

### This function should probably be removed since this part is now done in the displayData function

def createResultDB(resultDBInternal, outputCheckInternal) :
    if outputCheckInternal == False :
        print("Can't find any calculated data. Please run the calculation first")
        return None
    elif resultDBInternal == True :
        return resultDBInternal
    resultDBInternal = {}
    with open("data/ppk.txt", 'r') as ppkRawCalc :
        ppkRawLabels = ppkRawCalc.readline()
        ppkLabels = ppkRawLabels.split(".")
        ppkRawLines = ppkRawCalc.readlines()
        #ppkLines = ppkRawLines.split(".")
    for ppkLine in ppkLines :
        ppkLineCurr = ppkLine.split(".")
        ppkName = ppkLineCurr[0]
        ppkLineCurr.remove(ppkLineCurr[0])
        resultDBInternal[ppkName] = ppkLineCurr
    return resultDBInternal

def displayResult(sortValue, outputCheckInternal) :
    if outputCheckInternal == False :
        print("No calculated data found. Please run calculation again.")
        return None
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
            valInd = punsch.index(value)
            if len(str(value)) > longList[valInd] :
                longList[valInd] = len(str(value))
            
    labelLine = ""
    for label in ppkLabels :
        labelCurr = label.ljust(longList[ppkLabels.index(label)] + 2)
        labelLine = labelLine + labelCurr
    print(labelLine)
    for punsch in displayData :
        labelLine = ""
        for label in punsch :
            labInd = punsch.index(label)
            labelStr = str(label)
            labelCurr = labelStr.ljust(longList[labInd]+2)
            labelLine = labelLine + labelCurr
        print(labelLine)
    return

def menu(menuTitle, optionlist) :
    if (menuTitle or optionlist) == False :
        print("Something went wrong. Please try again.")
        return None
    terminalSize = get_terminal_size().lines
    print("\n" * 10, end='')
    print(menuTitle)
    print("\n" * 4, end='')
    for option in optionlist :
        print(optionlist.index(option)+1, ")   ", option)
    print("\n" * (terminalSize - len(optionlist) - 18))
    userChoice = 'q'
    possibleChoices = []
    for l in range(1,len(optionlist)+1) :
        possibleChoices.append(str(l))
    numberOfChoices = 0
    while userChoice not in possibleChoices :
        if numberOfChoices > 0 :
            print("Invalid choice")
        userChoice = input("")
        numberOfChoices += 1
        if numberOfChoices > 5 :
            return None
    return int(userChoice)-1

def yesNoPrompt() :
    userPromptChoice = False
    numberOfChoices = 0
    while userPromptChoice not in ["Y","y","N","n"] :
        if numberOfChoices > 0 :
            print("(Y/N)")
        userPromptChoice = input("")
        numberOfChoices += 1
        if numberOfChoices > 5 :
            return None
    if userPromptChoice in ["Y","y"] :
        return True
    else :
        return False

### Find the date for last download
### This block is probably not needed anymore.

mainPunschPath = os.path.abspath(".")
punschLogPath = Path(mainPunschPath + "/data/punsch.log")
if punschLogPath.is_file() :
    logCheck = True
    with open("punsch.log", 'r') as logFile :
        lastLogLine = logFile.readline()[-1]
        lastLogEntry = lastLogLine.split(".")
else :
    print("It seems that something is wrong with your installation. Try running the setup.sh file again.")
    exit
        
punschInputPath = mainPunschPath + "/data/punschRawInput"
if punschInputPath.is_file() :
    punschInputInfo = os.stat("/data/punschRawInput")
    if punschInputInfo.st_size > 20 :
        inputCheck
        with open("punschRawInput", 'r') as inputData :
            dateRaw = ""
            for byte in range(20) :
                dateRaw = dateRaw + inputData.read(byte)
    elif punschInputInfo.st_size < 20 :
        print("It seems that something is wrong with your input data. Try downloading it again.")
        dateRaw = "00000000000000000000"
else :
    print("It seems that this either is the first time you're running this program or there is something wrong with your input data. Try downloading it again.")
    dateRaw = "00000000000000000000"

punschOutputPath = Path(mainPunschPath + "/data/ppk.txt")
if punschOutputPath.is_file() :
    punschOutputInfo = os.stat(str(punschOutputPath))
    punschModifiedSec = punschOutputInfo.st_mtime
    dateRaw = str(datetime.utcfromtimestamp(punschModifiedSec))
    outputCheck = True
#    punschModifiedDate = punschModifiedRaw[5:7]
#    punschModifiedMonth = punschModifiedRaw[8:10]
else :
#    punschModifiedMonth = 0
#    punschModifiedDate = 0
    dateRaw = "0000000000000000000000000000"
    outputCheck = False

### Setup
        
dateTemp = re.search("[0-9]{4}-[0-1][0-9]-[0-3][0-9]", dateRaw)
dlDate = dateTemp.group()[8:10]
dlMonth = dateTemp.group()[5:7]

dateToday = datetime.today().day
monthToday = datetime.today().month
checkDataMenu = ["Download new data (old data will be deleted)", "Back to main menu"]
if dlDate == dateToday and dlMonth == monthToday :
    checkDataTitle = "Data is up to date!"
elif inputCheck == True :
    chechDataTitle = "The data was last uppdated on "+ dlDate, "/", dlMonth, "(DD/MM)"
else :
    checkDataTitle = "No data found. Download recommended"
    checkDataMenu[0] = "Download data"

 ### check for prev calc output and prompt to do again
#displayResultMenu ### ask what attr to sort by then do

#userChoice = menu(welcome, mainMenu)
#print(mainMenu[userChoice])
displayResultTitle = "What do you want to sort by?"
displayResultMenu = ["Namn", "Pris", "Volym", "Alkoholhalt", "APK", "PPK"]

with open("welcomemst.txt", 'r') as msg :
    welcome = mgs.read()
mainMenu = ["Check/download data", "Calculate", "Display result", "Quit"]

### END setup

### Main Loop

mainLoop = None
while mainLoop != "Quit" :
    userChoice = menu(welcome, mainMenu)
    mainLoop = mainMenu[userChoice]
    if mainLoop == 0 :
        result = menu(checkDataTitle, checkDataMenu)
        if result == True :
            ### initiate download
            elif result == False :
                mainLoop = None
        ### ngt med result
    elif mainLoop == 1 :
        if outputCheck == True :
            print("Previous calculation already exists. Do you want to redo the calculation anyway?\n(Recommended if you recently downloaded new input data.)")
            result = yesNoPrompt() 
        else :
            result = True
        if result == True :
            calculatePPK(inputCheck)
        else :
            mainLoop = None
    elif mainLoop == 2 :
        result = menu(displayResultTitle, displayResultMenu)
        
    elif mainLoop == 4 :
        mainLoop = "Quit"
