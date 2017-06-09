# This file is part of Ulfen's PPK-Calculator.
# 
# Ulfen's PPK-Calculator is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# Ulfen's PPK-Calculator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Ulfen's PPK-Calculator.  If not, see
# <http://www.gnu.org/licenses/>.

import os, sys, time
import bs4
import re
from bs4 import BeautifulSoup
from datetime import datetime
from shutil import get_terminal_size
from pathlib import Path
from operator import itemgetter

def downloadData() :
    print("Downloading...")
    os.system("bash ./data/download.sh")
    print("Download complete!")
    time.sleep(5)
    return True

def calculatePPK(inputCheckInternal) :
    if inputCheckInternal == True :
        print('parsing input (this might take a little while)')
        with open('./data/punschRawInput', 'r') as input :
            soup = BeautifulSoup(input, 'xml')
        
        print("parsing complete")

        output = open('./data/ppk.txt', 'w+')
        print('creating output file')
        time.sleep(5)
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
        time.sleep(5)
        return False

def displayResult(sortValue, outputCheckInternal) :
    if outputCheckInternal == False :
        print("No calculated data found. Please run calculation again.")
        time.sleep(5)
        return None
    resultDB = []
    with open("./data/ppk.txt", 'r') as ppkRawCalc :
        ppkRawLabels = ppkRawCalc.readline()
        ppkLabels = ppkRawLabels.split(",")
        ppkRawLines = ppkRawCalc.readlines()
    print("\n")
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
            if labInd == 3 :
                labelStr = labelStr + " %"
            labelCurr = labelStr.ljust(longList[labInd]+2)
            labelLine = labelLine + labelCurr
        print(labelLine)
    terminalSize = get_terminal_size().lines
    print("\n" * (terminalSize-len(displayData)-10))
    input("press ENTER to return to main menu")
    return

def menu(menuTitle, optionlist) :
    if (menuTitle or optionlist) == False :
        print("Something went wrong. Please try again.")
        input("press ENTER to return to main menu")
        return None
    terminalSize = get_terminal_size().lines
    print("\n" * 11, end='')
    print(menuTitle)
    print("\n" * 4, end='')
    for option in optionlist :
        print(optionlist.index(option)+1, ")   ", option)
    print("\n" * (terminalSize - len(optionlist) - 20))
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
    print("(Y/N)")
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

def checkInput(mainPunschPath):
    punschInputPath = Path(mainPunschPath + "/data/punschRawInput")
    if punschInputPath.is_file() :
        punschInputInfo = os.stat("./data/punschRawInput")
        if punschInputInfo.st_size > 20 :
            inputCheck = True
            with open("./data/punschRawInput", 'r') as inputData :
                dateRaw = ""
                for byte in range(20) :
                    dateRaw = dateRaw + inputData.read(byte)
        elif punschInputInfo.st_size < 20 :
            print("It seems that something is wrong with your input data. Try downloading it again.")
            dateRaw = "0000-00-00"
            inputCheck = False
            time.sleep(5)
    else :
        print("It seems that this is the first time you're running this program (or someone removed your input data). \nTry downloading it again.")
        dateRaw = "0000-00-00"
        inputCheck = False
        time.sleep(5)
    return dateRaw, inputCheck


def checkOutput(mainPunschPath):
    punschOutputPath = Path(mainPunschPath + "/data/ppk.txt")
    if punschOutputPath.is_file() :
        return True
    else :
        return False

def checkData(dateRaw, inputCheck):
    dateTemp = re.search("[0-9]{4}-[0-1][0-9]-[0-3][0-9]", dateRaw)
    dlDate = dateTemp.group()[8:10]
    dlMonth = dateTemp.group()[5:7]
    dateToday = datetime.today().day
    monthToday = datetime.today().month
    if dateToday < 10 :
        dateToday = "0" + str(dateToday)
    if monthToday < 10 :
        monthToday = "0" + str(monthToday)
    checkDataMenu = ["Download new data (old data will be deleted)", "Back to main menu"]
    checkDataTitle = ""
    if dlDate == dateToday and dlMonth == monthToday :
        checkDataTitle = "Data is up to date!"
    elif inputCheck == True :
        checkDataTitle = "Data was last uppdated on "+ dlDate + "/" + dlMonth + " (DD/MM)"
    else :
        checkDataTitle = "No data found. Download recommended"
        checkDataMenu[0] = "Download data"
    return checkDataTitle, checkDataMenu

### Begin setup

displayResultTitle = "What do you want to sort by?"
displayResultMenu = ["Namn", "Pris", "Volym", "Alkoholhalt", "APK", "PPK"]

with open("./data/welcomemsg.txt", 'r') as msg :
    welcome = msg.read()
mainMenu = ["Check/download data", "Calculate", "Display result", "Quit"]

mainPunschPath = os.path.abspath(".")
dateRaw, inputCheck = checkInput(mainPunschPath)
outputCheck = checkOutput(mainPunschPath)
checkDataTitle, checkDataMenu = checkData(dateRaw, inputCheck)

### END setup

### Main Loop

choiceLog = []
mainLoop = None
while mainLoop != "Quit" :
    userChoice = menu(welcome, mainMenu)
    mainLoop = mainMenu[userChoice]
    choiceLog.append(mainLoop)
    if mainLoop == mainMenu[0] :
        checkDataTitle, checkDataMenu=checkData(dateRaw, inputCheck)
        result = menu(checkDataTitle, checkDataMenu)
        if result == 0 :
            print("Are you sure?")
            answ = yesNoPrompt()
            if answ == True :
                downloadData()
                dateRaw, inputCheck = checkInput(mainPunschPath)
            else :
                mainLoop = None
        elif result == 1 :
            mainLoop = None
    elif mainLoop == mainMenu[1] :
        if outputCheck == True :
            print("Previous calculation already exists. Do you want to redo the calculation anyway?\n(Recommended if you recently downloaded new input data.)")
            result = yesNoPrompt() 
        else :
            result = True
        if result == True :
            calculatePPK(inputCheck)
        else :
            mainLoop = None
    elif mainLoop == mainMenu[2] :
        outputCheck = checkOutput(mainPunschPath)
        result = menu(displayResultTitle, displayResultMenu)
        print("\n" * 5)
        print("sorting by: ", displayResultMenu[result])
        display = displayResult(result, outputCheck)
        
### Exit ppk-calculator

print("Bye, bye!")
