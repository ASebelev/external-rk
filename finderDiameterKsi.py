from math import ceil
import subprocess
import os
import shutil
from glob import glob
import parseData
from sys import argv

class MapData:
    def __init__(self, power=0, pressure=0, diameter=0, drkPressure=0, drkPower=0, sigma=0):
        self.power = float(power)
        self.drkPower = float(drkPower)
        self.pressure = float(pressure)
        self.drkPressure = float(drkPressure)
        self.diameter = float(diameter)
        self.sigma = float(sigma)

class Mode:
    def __init__(self, freq, mapData, listDRK=[]):
        self.freq = float(freq)
        self.mapData = mapData
        self.listDRK = listDRK
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

# fullMode = [Mode(1500, [MapData(1.76, 20000), MapData(5.88, 25000), MapData(9.97, 30000), MapData(14.05, 35000),
#                        MapData(18.13, 40000), MapData(22.17, 45000), MapData(26.23, 50000), MapData(30.34, 55000),
#                        MapData(34.40, 60000), MapData(38.46, 65000), MapData(42.61, 70000), MapData(46.69, 75000),
#                        MapData(50.72, 80000), MapData(54.80, 85000), MapData(58.89, 90000), MapData(62.98, 95000)])]

fullMode = [Mode(1500, [MapData(18.13, 40000), MapData(22.17, 45000), MapData(26.23, 50000), MapData(30.34, 55000),
                        MapData(34.40, 60000), MapData(38.46, 65000), MapData(42.61, 70000), MapData(46.69, 75000),
                        MapData(50.72, 80000), MapData(54.80, 85000), MapData(58.89, 90000), MapData(62.98, 95000)]),
            Mode(1800, [MapData(24.22, 40000), MapData(29.01, 45000), MapData(33.87, 50000), MapData(38.61, 55000),
                        MapData(43.55, 60000), MapData(53.21, 65000), MapData(53.21, 70000), MapData(57.98, 75000),
                        MapData(62.73, 80000), MapData(67.56, 85000), MapData(72.52, 90000), MapData(77.16, 95000)]),
            Mode(2100, [MapData(30.99, 40000), MapData(36.76, 45000), MapData(42.61, 50000), MapData(48.43, 55000),
                        MapData(54.25, 60000), MapData(60.06, 65000), MapData(65.92, 70000), MapData(71.79, 75000),
                        MapData(77.6, 80000), MapData(83.35, 85000), MapData(89.17, 90000), MapData(95.02, 95000)]),
            Mode(2400, [MapData(36.65, 40000), MapData(43.59, 45000), MapData(50.52, 50000), MapData(57.51, 55000),
                        MapData(64.51, 60000), MapData(71.55, 65000), MapData(78.54, 70000), MapData(85.58, 75000),
                        MapData(92.51, 80000), MapData(99.51, 85000), MapData(106.5, 90000), MapData(113.49, 95000)]),
            Mode(2700, [MapData(40.29, 40000), MapData(48.2, 45000), MapData(56.05, 50000), MapData(63.92, 55000),
                        MapData(71.79, 60000), MapData(79.69, 65000), MapData(87.55, 70000), MapData(95.45, 75000),
                        MapData(103.27, 80000), MapData(111.14, 85000), MapData(119.02, 90000), MapData(126.91, 95000)]),
            Mode(3000, [MapData(42.16, 40000), MapData(50.76, 45000), MapData(59.42, 50000), MapData(68.08, 55000),
                        MapData(76.71, 60000), MapData(85.37, 65000), MapData(94.03, 70000), MapData(102.69, 75000),
                        MapData(111.28, 80000), MapData(119.95, 85000), MapData(128.61, 90000), MapData(137.24, 95000)]),
            Mode(3300, [MapData(49.77, 40000), MapData(59.06, 45000), MapData(68.41, 50000), MapData(77.76, 55000),
                        MapData(87.11, 60000), MapData(96.48, 65000), MapData(105.84, 70000), MapData(115.18, 75000),
                        MapData(124.49, 80000), MapData(133.87, 85000), MapData(143.21, 90000), MapData(152.57, 95000)])
            ]
pass


for mode in fullMode:
    """ Коррекция файла ExtControlDAT.txt' """
    with open('./ToServ/ExtControlDAT.txt', 'r') as file:
        inputTxt = file.readlines()
    for j, item in enumerate(inputTxt):
        if '[1/мин]' in item:
            inputTxt[j] = item.replace(item.split()[0], formatNum(mode.freq))
            break
    with open(f'./ToServ/ExtControlDAT.txt', 'w') as file:
        file.writelines(inputTxt)

    listDiameter = [i for i in range(10, 51, 1)]
    listKsi = [i for i in range(0, 121, 1)]
    listPowPress = []
    for currentDiameter in listDiameter:
        for currentKsi in listKsi:
            currentKsi /= 10
            """ Коррекция файла diesel.swp """
            with open('./ToServ/diesel.swp', 'r') as file:
                inputTxt = file.readlines()
            for j, item in enumerate(inputTxt):
                if 'Диаметр трубопровода, подающего воздух во впускной коллектор, [мм]' in item:
                    inputTxt[j] = item.replace(item.split()[1], "{:.4e}".format(currentDiameter))
                elif 'Коэффициент потерь Ksi_in в тракте от охладителя наддувочного воздуха до впускного коллектора (0...5)' in item:
                    inputTxt[j] = item.replace(item.split()[1], "{:.4e}".format(currentKsi))
            with open(f'./ToServ/diesel.swp', 'w') as file:
                file.writelines(inputTxt)



            resDir = f'{globalResultDir}/freq({mode.freq})_Diameter({currentDiameter})_Ksi({currentKsi}))'
            if RUN_MODE is None:
                os.mkdir(resDir)
                subprocess.run(COMMAND + resDir + ' 3')
                files = os.listdir(resDir)
                for file in files:
                    if '.res' not in file and '.log' not in file:
                        os.remove(resDir + '/' + file)
                # if os.path.exists(resDir + '/*.fol'):
                #     os.remove(glob(resDir + '/*.fol')[0]) # удаление .fol файлов
            try:
                resFile = glob(resDir + '/*.res')[0]
                with open(f'{resFile}', 'r') as file:
                    resText = file.readlines()
                tmpMap = MapData(diameter=currentDiameter, sigma=currentKsi)
                for item in resText:
                    if 'Ne' in item:
                        tmpMap.drkPower = float(item.split()[0])
                    elif 'Ps' in item:
                        tmpMap.drkPressure = float(item.split()[0]) * 100000
                        break
                listPowPress.append(tmpMap)
            except IndexError:
                resFile = glob(resDir + '/*.log')[0]
                with open(f'{resFile}', 'r') as file:
                    resText = file.readlines()
                for item in resText:
                    if "Расчет завершен аварийно." in item:
                        print(f"NO SOLUTION for Diameter:{currentDiameter}")
                        continue
                    
    backDiameter = 999999999999999999999 # Диаметр предыдущего значения мапа
    listPowPress.reverse()
    mode.mapData.reverse()
    for currentMAP in mode.mapData:
        diffPower = 9999999999999999999999.9
        diffPressure = 9999999999999999999999.9

        for currentPowPres in listPowPress:
            #print(f"{currentMAP.power} - {currentPowPres.drkPower}")
            if abs(currentMAP.power - currentPowPres.drkPower) <= diffPower and\
                    abs(currentMAP.pressure - currentPowPres.drkPressure) <= diffPressure and\
                    currentPowPres.diameter < backDiameter and (currentMAP.ksi == currentPowPres.sigma or currentMAP.ksi == 0):

                currentMAP.drkPower = currentPowPres.drkPower
                currentMAP.drkPressure = currentPowPres.drkPressure
                currentMAP.diameter = currentPowPres.diameter
                currentMAP.ksi = currentPowPres.sigma

                backDiameter = currentPowPres.diameter

                diffPower = abs(currentMAP.power - currentPowPres.drkPower)
                diffPressure = abs(currentMAP.pressure - currentPowPres.drkPressure)


    mode.listDRK = listPowPress
for mode in fullMode:
    with open(f'{globalResultDir}/Freq_{mode.freq}.csv', 'w') as file:
        file.write("MAP_Power;DRK_Power;MAP_Pressure;DRK-Pressure;Diameter;Ksi\n")
        for currentMAP in mode.mapData:
            file.write(f"{str(currentMAP.power).replace('.',',')};{str(currentMAP.drkPower).replace('.',',')};"
                       f"{str(currentMAP.pressure).replace('.',',')};{str(currentMAP.drkPressure).replace('.',',')};"
                       f"{str(currentMAP.diameter).replace('.',',')};{str(currentMAP.ksi).replace('.', ',')}\n")
        file.write("\nDRK_Power;DRK-Pressure;Diameter;Ksi\n")
        for item  in mode.listDRK:
            file.write(f"{str(item.drkPower).replace('.',',')};{str(item.drkPressure).replace('.',',')};"
                       f"{str(item.diameter).replace('.',',')};{str(item.sigma).replace('.',',')}\n")