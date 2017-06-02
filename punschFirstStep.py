from datetime import datetime

with open('punsch.log', 'r') as logFile :
    print("parsing log file...")
    logLines = logFile.readlines()
    logIndexReversed = 1
    while logIndexReversed <= len(logLines) : # this part looks for the latest "dl_status" message in the log file
        lastLogLine = logLines[-logIndexReversed]
        tempLogList = lastLogLine.split(".")
        if tempLogList[0] == "dl_status" :
            latestStatusEntry = tempLogList
            break
        elif tempLogList[0] == ("calc_request" or "dl_request") :
            exit
        else :
            logIndexReversed += 1
    if logIndexReversed >= len(logLines) :
        print("missing proper log. please contact admin.")
        exit

print("log entry found")
timeToUpdate = False
requestCalculation = False

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

currentDate = datetime.today().day
currentMonth = datetime.today().month
dlTime = latestStatusEntry[3]
dlDate = dlTime[2:]
dlMonth = dlTime[:2]
#print("current: ",currentMonth, currentDate)
#print("dl: ", dlMonth,dlDate)
if int(currentDate) != int(dlDate) or int(currentMonth) != int(dlMonth) :
    print('The inputfile might not be up to date. It was last updated on ', dlDate, "/", dlMonth)
    print("Do you want to update now? (Y/N)")
    userChoice = yesNoPrompt()
    if userChoice == True :
        timeToUpdate = True
        with open('punsch.log', "a") as logFile :
            logFile.write('dl_request.' + currentMonth + "." + currentDate + ".1\n")
    elif userChoice == False :
        print("Do you want to continue with the old data? (Y/N)")
        requestCalculation = yesNoPrompt()
        if requestCalculation == False :
            with open("punsch.log", "a") as logFile :
                logFile.write("calc_request."+currentMonth+"."+currentDate+".0\n")
        elif requestCalculation == True :
            with open("punsch.log", "a") as logFile :
                logFile.write("calc_request."+currentMonth+"."+currentDate+".1\n")
elif int(currentDate) == int(dlDate) or int(currentMonth) == int(dlMonth) :
    print("input is up to date! Continuing to calculation!")
    with open("punsch.log", 'a') as logFile :
        logFile.write("calc_request."+currentMonth+'.'+currentDate+'.1\n')
else :
    print("something went wrong...")
    exit



    
