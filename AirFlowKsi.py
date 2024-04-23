from math import ceil
import os
import shutil
from glob import glob
import parseData
from sys import argv
import matplotlib.pyplot as plt


class MapData:
    def __init__(self, power=0, pressure=0, diameter=0, drkPressure=0, drkPower=0, ksi=0, gair=0):
        self.power = float(power)
        self.pressure = float(pressure)

        self.drkPower = float(drkPower)
        self.drkPressure = float(drkPressure)
        self.diameter = float(diameter)
        self.ksi = float(ksi)
        self.gair = float(gair)

class Mode:
    def __init__(self, freq, mapData, listDRK=[]):
        self.freq = float(freq)
        self.mapData = mapData
        self.listDRK = listDRK

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

listCollor = ['red', 'green', 'blue', 'cyan', 'black', 'yellow', 'pink']
globalResultDir = './testPyRK'
for i, mode in enumerate(fullMode):
    listDiameter = [i for i in range(10, 51, 1)]
    listKsi = [i for i in range(0, 121, 1)]

    listPowPress = []
    for currentDiameter in listDiameter:
        ksiList = []
        gairList = []

        fig_label = f"Diameter:{currentDiameter}"
        fig = plt.figure(fig_label)
        plt.title(f'Diameter: {currentDiameter}')
        plt.xlabel('Ksi')
        plt.ylabel('Pасход воздуха (+EGR) через цилиндры двиг.,[кг/с]')

        for j, currentKsi in enumerate(listKsi):
            currentKsi /= 10
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

                    elif 'Gair' in item:
                        _gair = float(item.split()[0])
                        tmpMap.drkPressure = _gair
                        gairList.append(_gair)
                ksiList.append(currentKsi)
            except:
                print(f'NOT FOUND *.RES FILES {resDir}')
        plt.plot(ksiList, gairList, label=mode.freq, color=listCollor[i])
        plt.legend()

plt.show()