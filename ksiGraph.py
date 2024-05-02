import json
import os
import matplotlib.pyplot as plt
import numpy as np


resDir = './FromServ'
inputDir = './ForMAP/'
fileOut = './ForMAP/OUT.csv'
listDir = os.listdir(inputDir)
ksi = {}
coeffAB = {}
coeffAB_press = {}
for fileIn in listDir:
    if '.json' not in fileIn:
        continue
    print(f'Read: {fileIn}')
    currentRPM = 0
    with open(inputDir + fileIn, 'r') as f:
        rawData = json.load(f)
        currentRPM = rawData[0]['RPM']
        ksi[currentRPM] = []
        coeffAB[currentRPM] = []
        data = rawData.copy()
        data.pop(0)
    print(currentRPM)
    for item in data:
        ksi[currentRPM].append([item['KsiIn'], item['TargetPressure']])
        coeffAB[currentRPM].append([item['A'], item['B'], ])
        if item['TargetPressure'] not in coeffAB_press.keys():
            coeffAB_press[item['TargetPressure']] = []
        coeffAB_press[item['TargetPressure']].append([item['A'], item['B'], currentRPM])

t = True
for pressure, AB in coeffAB_press.items():
    if t:
        print(f'0;{";".join([str(val[2]).replace(".", ",") for val in AB])}')
        t = False
    print(f'{str(pressure).replace(".", ",")};{";".join([str(round(val[0],4)).replace(".", ",") for val in AB])}')


print('|-----------------|')
t = True
for pressure, AB in coeffAB_press.items():
    if t:
        print(f'0;{";".join([str(val[2]).replace(".", ",") for val in AB])}')
        t = False
    print(f'{str(pressure).replace(".", ",")};{";".join([str(round(val[1],4)).replace(".", ",") for val in AB])}')


del ksi[850]
del ksi[1200]
del ksi[1500]
del ksi[1800]
del ksi[2800]
fig = plt.figure('KSI')
for key, value in ksi.items():
    ksiY = [x[0] for x in value]
    ksiX = [x[1] for x in value]

    plt.plot(ksiX, ksiY, marker='h', label=key)
    plt.xlabel('TargetPressure, bar')
    plt.ylabel('Ksi')


plt.grid()
plt.legend()
plt.show()

