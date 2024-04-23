import json
import matplotlib.pyplot as plt
import numpy as np


directory = './ResultIOSO/'
listFiles = ['IN1.json', 'IN2.json', 'IN3.json', 'IN4.json', 'IN5.json', 'IN6.json', 'IN7.json']
#listFiles = ['IN7.json']
data = []

for filename in listFiles:
    rpm = ''
    with open (directory + filename, 'r') as f:
        rawData = json.load(f)
        rpm = rawData[0]['RPM']
        data = rawData.copy()
        data.pop(0)
    _label = rpm
    fig, axs = plt.subplots(2, 1)
    plt.suptitle(f'Freq: {rpm}')

    aCoord = []
    bCoord = []
    pressCoord = []
    for item in data:
        aCoord.append(item['A'])
        bCoord.append(item['B'])
        pressCoord.append(item['TargetPressure'])
    axs[0].scatter(pressCoord, aCoord, label='A', color='red')
    axs[0].set_title('A')
    z1 = np.polyfit(pressCoord, aCoord, 1)
    p1 = np.poly1d(z1)
    axs[0].plot(pressCoord, p1(pressCoord))

    axs[1].scatter(pressCoord, bCoord, label='B', color='blue')
    axs[1].set_title('B')
    z2 = np.polyfit(pressCoord, bCoord, 1)
    p2 = np.poly1d(z2)
    axs[1].plot(pressCoord, p2(pressCoord))
    # z2 = np.polyfit(pressCoord, bCoord,  1)
    # p2 = np.poly1d(z2)
    # axs[1].plot(p2(bCoord), bCoord)

    axs[0].set(xlabel='Pressure', ylabel='A or B')
    axs[1].set(xlabel='Pressure', ylabel='A or B')
    print(rpm)
    for point in zip (aCoord, bCoord, pressCoord):
        print(f'{point[0]};{point[1]};{point[2]}')
    print('\n')
    for i in range(1, len(rawData)):
        item = rawData[i]
        item['A'] = p1(item['TargetPressure'])
        item['B'] = p2(item['TargetPressure']) if p2(item['TargetPressure']) > 0 else 0.0

    with open(directory + filename.replace('.json','test.json'), 'w') as out:
        json.dump(rawData, out)




for ax in axs.flat:
    ax.set(xlabel='Pressure', ylabel='A or B')
plt.show()
pass