from math import ceil
import subprocess
import os
import shutil
from glob import glob
import parseData
from sys import argv

def getVarList(start, end, step):
    """
    Функция генерации списков для варьирования

    :param start: стартовое значение (должно быть всегда меньше, чем конечное)
    :param end: конечное значение
    :param step: размер шага

    :return: список [start, end], размер соответствует countStep
    """
    try:
        countStep = ceil((end - start) / step)
        return [start + step * i for i in range(0, countStep + 1)]
    except:
        return []

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

RUN_MODE = argv[1] if len(argv) > 1 else None  # Без флага - будет вызываться расчёт снуля, с флагом - только вывод .csv
COMMAND = './ajax2_32.exe ./ToServ '  # Вызов ядра в субпроцессе
globalResultDir = './testPyRK'
indexes = parseData.indexesBlank

if RUN_MODE is None:
    if os.path.exists(globalResultDir):  # Удаление существующей директории с результатами создание новой
        shutil.rmtree(globalResultDir)
    os.mkdir(globalResultDir)

# startFreq = 800.0
# endFreq = 3300.0
# sizeStepFreq = 100.0
# listFreq = getVarList(startFreq, endFreq, sizeStepFreq)
# listFreq[-1] = endFreq if listFreq[-1] > endFreq else listFreq[-1]
listFreq = [1800.0, 2100.0, 2400.0, 2800.0, 3300.0]
recoveryFactor = [0.95, 0.9]

startAlt = 0
endAlt = 0
sizeStepAlt = 0
listAlt = getVarList(startAlt, endAlt, sizeStepAlt)
listAlt = [0.0]

startTemp = 233.15  # -40 град К
endTemp = 358.15  # +85 град К
sizeStepTemp = 5.0
listTemp = getVarList(startTemp, endTemp, sizeStepTemp)

variables = [[], [], []]  # [[список RPM], [список высот], [список температур]]

for i, currentFreq in enumerate(listFreq):
    for currentAlt in listAlt:
        for currentTemp in listTemp:
            with open('./ToServ/ExtControlDAT.txt', 'r') as file:
                inputTxt = file.readlines()
            paramCounter = 0
            for j, item in enumerate(inputTxt):
                if '[1/мин]' in item:
                    inputTxt[j] = item.replace(item.split()[0], formatNum(currentFreq))
                    paramCounter += 1
                elif 'Н_ур.мор' in item:
                    inputTxt[j] = item.replace(item.split()[0], formatNum(currentAlt))
                    paramCounter += 1
                elif 'To_sea' in item:
                    inputTxt[j] = item.replace(item.split()[0], formatNum(currentTemp))
                    paramCounter += 1
                elif 'Sigma_in' in item:
                    if currentFreq == 3300:
                        inputTxt[j] = item.replace(item.split()[0], formatNum(recoveryFactor[1]))
                    else:
                        inputTxt[j] = item.replace(item.split()[0], formatNum(recoveryFactor[0]))
                    paramCounter += 1

            with open(f'./ToServ/ExtControlDAT.txt', 'w') as file:
                file.writelines(inputTxt)
            resDir = f'{globalResultDir}/FromServ_freq({currentFreq})_Alt({currentAlt})_Temp({currentTemp})'
            if RUN_MODE is None:
                os.mkdir(resDir)
                subprocess.run(COMMAND + resDir + ' 3')
                if os.path.exists(resDir + '/*.fol'):
                    os.remove(glob(resDir + '/*.fol')[0]) # удаление .fol файлов

            resFile = glob(resDir + '/*.res')[0]
            with open(f'{resFile}', 'r') as file:
                resText = file.readlines()
            for key in indexes:
                for num in range(7, len(resText) + 1):
                    string = resText[num]
                    if key in string:
                        indexes[key].append((string.split()[0]))
                        break
            variables[0].append(str(currentFreq))
            variables[1].append(str(currentAlt))
            variables[2].append(str(currentTemp))
with open(f'{globalResultDir}/out.csv', 'w') as file:
    for key, value in parseData.indexes.items():
        file.write(f"{key};{value.replace('.', ',')}\n")
    file.write('\n')
    #file.write(f"n;{';'.join(variables[0]).replace('.', ',')}\n")
    #file.write(f"Н_ур.мор;{';'.join(variables[1]).replace('.', ',')}\n")
    #file.write(f"To_sea;{';'.join(variables[2]).replace('.', ',')}\n")
    for key, value in indexes.items():
        file.write(f"{key};{';'.join(value).replace('.', ',')}\n")

# x = graphDict['To_sea']
#
# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
#
# # Настройка первого графика
# ax1.plot(x, graphDict['Ne'], 'r-', label='Мощность')
# ax1.set_xlabel('X')
# ax1.set_ylabel('Ne')
# ax1.tick_params(axis='y')
#
# # Настройка второго графика
# ax2.plot(x, graphDict['Me'], 'b-', label='Момент')
# ax2.set_ylabel('Me')
# ax2.tick_params(axis='y')
#
# # Добавление легенды
# lines, labels = ax1.get_legend_handles_labels()
# lines2, labels2 = ax2.get_legend_handles_labels()
# ax2.legend(lines + lines2, labels + labels2, loc='upper right')
#
# # Отображение графиков
# plt.show()
