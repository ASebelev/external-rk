import json
import os
import subprocess
from glob import glob
import parseData

def formatNum(num):
    """
    Функция приведения числа к строке с 2+ знаками после запятой.
    Иначе ругается дизель-рк.

    :param num:
    :return:
    """
    if type(num) is float:
        num = str(num)
        if len(num) < 8:
            while len(num) < 8:
                num += '0'
    else:
        num = str(num) + '000'
    return num
def ChangeInputData(freq, diameter, ksi, sigma, a, b):
    """ Коррекция файла ExtControlDAT.txt """
    with open('./ToServ/ExtControlDAT.txt', 'r') as file:
        inputTxt = file.readlines()
    for j, item in enumerate(inputTxt):
        if '[1/мин]' in item:
            inputTxt[j] = item.replace(item.split()[0], formatNum(freq))
        elif 'Sigma_in' in item:
            inputTxt[j] = item.replace(item.split()[0], formatNum(sigma))
    with open(f'./ToServ/ExtControlDAT.txt', 'w') as file:
        file.writelines(inputTxt)

    """ Коррекция файла diesel.swp """
    with open('./ToServ/diesel.swp', 'r') as file:
        inputTxt = file.readlines()
    for j, item in enumerate(inputTxt):
        if 'Диаметр трубопровода, подающего воздух во впускной коллектор, [мм]' in item:
            inputTxt[j] = item.replace(item.split()[1], "{:.4e}".format(diameter))
        elif 'Коэффициент потерь Ksi_in в тракте от охладителя наддувочного воздуха до впускного коллектора (0...5)' in item:
            inputTxt[j] = item.replace(item.split()[1], "{:.4e}".format(ksi))
        elif 'Коэффициент A' in item:
            inputTxt[j] = item.replace(item.split()[1], "{:.4e}".format(a))
        elif 'Коэффициент B' in item:
            inputTxt[j] = item.replace(item.split()[1], "{:.4e}".format(b))

    with open(f'./ToServ/diesel.swp', 'w') as file:
        file.writelines(inputTxt)


COMMAND = './ajax2_32.exe ./ToServ '  # Вызов ядра в субпроцессе

resDir = './FromServ'
inputDir = './ForMAP/'
fileOut = './ForMAP/OUT.csv'
listDir = os.listdir(inputDir)
indexes = parseData.indexesBlank

for fileIn in listDir:
    print(f'Read&Calc {fileIn}')
    if '.json' not in fileIn:
        continue
    with open(inputDir + fileIn, 'r') as f:
        inputData = json.load(f)

    RPM = float(inputData[0]['RPM'])
    inputData.pop(0)
    drkPower = []
    drkPressure = []

    diffPower = []
    diffPress = []

    for loadCase in inputData:
        for key, value in loadCase.items():
            loadCase[key] = float(value)

        targetPower = loadCase['TargetPower']
        targetPressure = loadCase['TargetPressure']
        ChangeInputData(freq=RPM, diameter=loadCase['Diameter'],ksi=loadCase['KsiIn'], sigma=loadCase['SigmaIn'],
                        a=loadCase['A'], b=loadCase['B'])
        std = subprocess.run(COMMAND + resDir + ' 3')
        resFile = glob(resDir + '/*.res')[0]
        with open(resFile, 'r') as f:
            resText = f.readlines()
        for key in indexes:
            for num in range(7, len(resText)):
                string = resText[num]
                if key in string:
                    indexes[key].append((string.split()[0]))
                    break




with open(fileOut, 'w') as file:
    for key, value in indexes.items():
        file.write(f"{key};{parseData.indexes[key]};{';'.join(value).replace('.', ',')}\n")

