import bs4
from bs4 import BeautifulSoup

print('parsing input (this might take a little while)')
with open('punschRawInput', 'r') as input :
    soup = BeautifulSoup(input, 'xml')
print("parsing complete")

output = open('ppk.txt', 'w+')
print('creating output file')
output.write('Namn\tPris\tVolym\tAlkoholhalt\tAPK\tPPK\n')
for drinkType in soup.find_all('Varugrupp') :
    if drinkType.string == 'Punsch' :        
        for info in drinkType.parent :
            if info.name == 'Namn' :
                output.write(info.string + '\t')
            if info.name == 'Prisinklmoms' :
                pris = int(float(info.string))
                output.write(str(pris) + '\t')
            if info.name == 'Volymiml' :
                volym = float('{0:.2f}'.format(float(info.string)))
                output.write(str(volym) + '\t')
            if info.name == 'Alkoholhalt' :
                procent = int(float(info.string[:-1]))/100
                output.write(str(procent) + '\t')
        apk = ((procent*volym)/pris)
        output.write(str(apk) + '\t')
        output.write(str(volym/pris) + "\n")

output.close()
