from math import ceil
import matplotlib.pyplot as plt
from glob import glob
import parseData


class MapData:
    def __init__(self, power=0, pressure=0, diameter=0, drkPressure=0, drkPower=0, ksi=0):
        self.power = float(power)
        self.pressure = float(pressure)

        self.drkPower = float(drkPower)
        self.drkPressure = float(drkPressure)
        self.diameter = float(diameter)
        self.ksi = float(ksi)

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

def NearestSearch(targetPower, targetPressure, listPower, listPressure):
    diffPower = [abs(targetPower - x) for x in listPower]
    diffPressure = [abs(targetPressure - x) for x in listPressure]

    resIndexPower = diffPower.index(min(diffPower))
    resIndexPressure = diffPressure.index(min(diffPressure))

    if resIndexPower != resIndexPressure:
        if diffPower[resIndexPressure] < diffPower[resIndexPower] or\
                diffPressure[resIndexPressure] < diffPressure[resIndexPower]:
            answerIndex = resIndexPressure
        else:
            answerIndex = resIndexPower
    else:
        answerIndex = resIndexPower

    return answerIndex, diffPower[answerIndex], diffPressure[answerIndex]

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

globalResultDir = './testPyRK'
indexes = parseData.indexesBlank

# fullMode = [Mode(1500, [MapData(1.76, 20000), MapData(5.88, 25000), MapData(9.97, 30000), MapData(14.05, 35000),
#                        MapData(18.13, 40000), MapData(22.17, 45000), MapData(26.23, 50000), MapData(30.34, 55000),
#                        MapData(34.40, 60000), MapData(38.46, 65000), MapData(42.61, 70000), MapData(46.69, 75000),
#                        MapData(50.72, 80000), MapData(54.80, 85000), MapData(58.89, 90000), MapData(62.98, 95000)])]

fullMode = [Mode(1500, [MapData(18.13, 40000), MapData(22.17, 45000), MapData(26.23, 50000), MapData(30.34, 55000),
                        MapData(34.40, 60000), MapData(38.46, 65000), MapData(42.61, 70000), MapData(46.69, 75000),
                        MapData(50.72, 80000), MapData(54.80, 85000), MapData(58.89, 90000), MapData(62.98, 95000)]),
            Mode(1800, [MapData(24.22, 40000), MapData(29.01, 45000), MapData(33.87, 50000), MapData(38.61, 55000),
                        MapData(43.55, 60000), MapData(48.43, 65000), MapData(53.21, 70000), MapData(57.98, 75000),
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
selectedKSI = dict()
for mode in fullMode:
    listDiameter = [i for i in range(10, 51, 1)]
    listKsi = [i for i in range(0, 121, 1)]
    listPowPress = []
    listOnlyPower = []
    listOnlyPressure = []
    dictKSI = dict()
    for currentKsi in listKsi:
        currentKsi /= 10
        dictKSI[currentKsi] = []
        for currentDiameter in listDiameter:
            resDir = f'{globalResultDir}/freq({mode.freq})_Diameter({currentDiameter})_Ksi({currentKsi}))'
            try:
                resFile = glob(resDir + '/*.res')[0]
                with open(f'{resFile}', 'r') as file:
                    resText = file.readlines()
                tmpMap = MapData(diameter=currentDiameter, ksi=currentKsi)
                for item in resText:
                    if 'Ne' in item:
                        _ne  =float(item.split()[0])
                        tmpMap.drkPower = _ne

                    elif 'Ps' in item:
                        _ps = float(item.split()[0]) * 100000
                        tmpMap.drkPressure = _ps

                        break
                listPowPress.append(tmpMap)
                listOnlyPower.append(_ne)
                listOnlyPressure.append(_ps)

            except IndexError:
                print(f"NO SOLUTION for Diameter:{currentDiameter}")
                continue

        tmp = dict()

        for currentMAP in mode.mapData:
            _index, _diffPwr, _diffPrs = NearestSearch(targetPower=currentMAP.power, targetPressure=currentMAP.pressure,
                                                       listPower=listOnlyPower, listPressure=listOnlyPressure)
            # 0 - мощность, 1 - давление, 2 - диаметр, 3 - разница мощностей 4 - разница давлений
            tmp[currentMAP.power] = [listPowPress[_index].drkPower, listPowPress[_index].drkPressure,
                                     listPowPress[_index].diameter, _diffPwr, _diffPrs, currentKsi]

        mode.listDRK = listPowPress
        #if len(tmp[currentMAP.power]) != 0:
        dictKSI[currentKsi] = tmp
        pass
    minAveragePower = 999999999
    minAveragePressure = 9999999999
    selectKSI = 0
    for currentKsi, currentDict in  dictKSI.items():
        averagePower = sum(currentDict[var][3] / len(currentDict) for var in currentDict.keys())
        averagePressure = sum(currentDict[var][4] / len(currentDict) for var in currentDict.keys())
        if averagePower < minAveragePower and averagePressure < minAveragePressure:
            selectKSI = currentKsi
            minAveragePower = averagePower
            minAveragePressure = averagePressure
    listForKsi = [[data.drkPower, data.drkPressure, data.diameter] for data in listPowPress if data.ksi == selectKSI]
    for currentMAP in mode.mapData:
        _index, _diffPwr, _diffPrs = NearestSearch(targetPower=currentMAP.power, targetPressure=currentMAP.pressure,
                                                   listPower=[data[0] for data in listForKsi],
                                                   listPressure=[data[1] for data in listForKsi])
        currentMAP.drkPower = listForKsi[_index][0]
        currentMAP.drkPressure = listForKsi[_index][1]
        currentMAP.diameter = listForKsi[_index][2]
        currentMAP.ksi = selectKSI
    pass

# for mode in fullMode:
#     for currentMAP in mode.mapData:
#         diffPower = 999999999
#         diffPressure = 999999999
#         minAveragePower = 99999999999
#         minAveragePressure = 999999999
#         for currentKSI in selectedKSI:
#             for currentDRK in listPowPress:
#                 if abs(currentMAP.power - currentDRK.drkPower) <= diffPower and abs(
#                         currentMAP.pressure - currentDRK.drkPressure) <= diffPressure and currentDRK.ksi == currentKSI:
#                     flag = False
#                     if i == 0 and (currentDRK.diameter > currentMAP.diameter or currentMAP.diameter == 0):
#                         flag = True
#                     if i > 0 and currentDRK.diameter > mode.mapData[i - 1].diameter or currentMAP.diameter == 0:
#                         flag = True
#                     if flag:
#                         # currentMAP.drkPower = currentDRK.drkPower
#                         # currentMAP.drkPressure = currentDRK.drkPressure
#                         # currentMAP.diameter = currentDRK.diameter
#
#                         diffPower = abs(currentMAP.power - currentDRK.drkPower)
#                         diffPressure = abs(currentMAP.pressure - currentDRK.drkPressure)
#                         # print(f'{currentMAP.power} {currentDRK.drkPower}\n')
#                         # 0 - мощность, 1 - давление, 2 - диаметр, 3 - разница мощностей 4 - разница давлений
#                         tmp[currentMAP.power] = [currentDRK.drkPower, currentDRK.drkPressure, currentDRK.diameter,
#                                                  diffPower, diffPressure, currentKsi]
for mode in fullMode:
    _label = mode.freq
    fig = plt.figure(_label)

    plt.xlabel('Pressure')
    plt.ylabel('Power')
    xCoordOrig = []
    xCoordDRK = []
    yCoordOrig = []
    yCoordDRK = []
    diameter = []
    with open(f'{globalResultDir}/Freq_{mode.freq}.csv', 'w') as file:
        file.write("MAP_Power;DRK_Power;MAP_Pressure;DRK-Pressure;Diameter;Ksi\n")
        for currentMAP in mode.mapData:
            file.write(f"{str(currentMAP.power).replace('.',',')};{str(currentMAP.drkPower).replace('.',',')};"
                       f"{str(currentMAP.pressure).replace('.',',')};{str(currentMAP.drkPressure).replace('.',',')};"
                       f"{str(currentMAP.diameter).replace('.',',')};{str(currentMAP.ksi).replace('.', ',')}\n")

            xCoordOrig.append(currentMAP.pressure)
            xCoordDRK.append(currentMAP.drkPressure)
            yCoordOrig.append(currentMAP.power)
            yCoordDRK.append(currentMAP.drkPower)
            diameter.append(currentMAP.diameter)
            plt.title(f'Mode ksi: {currentMAP.ksi}')
        file.write("\nDRK_Power;DRK-Pressure;Diameter;Ksi\n")
        for item  in mode.listDRK:
            if item.ksi == mode.mapData[0].ksi:
                file.write(f"{str(item.drkPower).replace('.',',')};{str(item.drkPressure).replace('.',',')};"
                           f"{str(item.diameter).replace('.',',')};{str(item.ksi).replace('.', ',')}\n")

        file.write("\nDRK_Power;DRK-Pressure;Diameter;Ksi\n")
        for item  in mode.listDRK:
            file.write(f"{str(item.drkPower).replace('.',',')};{str(item.drkPressure).replace('.',',')};"
                       f"{str(item.diameter).replace('.',',')};{str(item.ksi).replace('.', ',')}\n")
    plt.plot(xCoordOrig, yCoordOrig, label='MAP', color='red')
    plt.plot(xCoordDRK, yCoordDRK, label='DRK', color='black')
    for x, y, d in zip(xCoordDRK, yCoordDRK, diameter):
        plt.text(x, y, d)
    plt.legend()
plt.show()