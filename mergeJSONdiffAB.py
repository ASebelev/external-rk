import json
import matplotlib.pyplot as plt
directory = './ResultIOSO/interpolation/'
listFiles = ['IN1.json', 'IN2.json', 'IN3.json', 'IN4.json', 'IN5.json', 'IN6.json', 'IN7.json']
data = []

for filename in listFiles:
    with open (directory + filename, 'r') as f:
        rawData = json.load(f)
        rawData.pop(0)
        data.append(rawData)

averageA = [0 for _ in range(len(data))]
averageB = [0 for _ in range(len(data))]
countPoint = len(rawData)
aCoord = []
bCoord = []
pressCoord = []
for i in range(countPoint):
    averageA = 0
    averageB = 0
    for doc in data:
        averageA += doc[i]['A']
        averageB += doc[i]['B']
    averageA /= len(data)
    averageB /= len(data)
    for doc in data:
        doc[i]['A'] = averageA
        doc[i]['B'] = averageB
    print(f'Numer point: {i}\nA: {averageA}\nB: {averageB}\n----')
    aCoord.append(averageA)
    bCoord.append(averageB)
    pressCoord.append(data[0][i]['TargetPressure'])

for i, file in enumerate(data):
    with open(directory + 'out_diffAB/' + 'IN' + str(i) + '.json', 'w') as f:
        json.dump(file, f)

fig, axs = plt.subplots(2, 1)
#plt.suptitle(f'Freq: {rpm}')
axs[0].scatter(pressCoord, aCoord, label='A', color='red')
axs[0].set_title('A')


axs[1].scatter(pressCoord, bCoord, label='B', color='blue')
axs[1].set_title('B')


plt.show()