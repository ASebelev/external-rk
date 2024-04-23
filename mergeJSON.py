import json

directory = './ResultIOSO/interpolation/'
listFiles = ['IN1.json', 'IN2.json', 'IN3.json', 'IN4.json', 'IN5.json', 'IN6.json', 'IN7.json']
data = []
rawDataList = []
for filename in listFiles:
    with open (directory + filename, 'r') as f:
        rawData = json.load(f)
        rawDataList.append(rawData.copy())
        rawData.pop(0)
        data.append(rawData)

averageA = [0 for _ in range(len(data))]
averageB = [0 for _ in range(len(data))]

for i, file in enumerate(data):
    averageA[i] = 0
    averageB[i] = 0
    for point in file:
        averageA[i] += point['A']
        averageB[i] += point['B']
    averageA[i] /= len(file)
    averageB[i] /= len(file)
generalAverageA = sum(averageA) / len(averageA)
generalAverageB = sum(averageB) / len(averageB)
print(f'A: {generalAverageA}\nB: {generalAverageB}')
for i, file in enumerate(rawDataList):
    for j in range(1,len(file)):
        point = file[j]
        point['A'] = generalAverageA
        point['B'] = generalAverageB
    with open(directory + 'out_generalAB/' + 'IN' + str(i) + '.json', 'w') as f:
        json.dump(file, f)