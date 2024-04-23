import json
import subprocess
from glob import glob


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
fileIn  = './IOSO-Py-DRK/IN.json'
fileOut = './IOSO-Py-DRK/OUT.txt'
with open(fileIn, 'r') as f:
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
    subprocess.run(COMMAND + resDir + ' 3')
    try:
        resFile = glob(resDir + '/*.res')[0]
        with open(resFile, 'r') as f:
            outputData = f.readlines()
        for j, item in enumerate(outputData):
            if 'Ne' in item:
                _ne = float(item.split()[0])
            elif 'Ps' in item:
                _ps = float(item.split()[0])
                break

        drkPower.append(_ne)
        drkPressure.append(_ps)
        diffPower.append(abs(targetPower - _ne) / targetPower)
        diffPress.append(abs(targetPressure - _ps) / targetPressure)
    except:
        print('NO .res FILE!')
        drkPower.append(0)
        drkPressure.append(0)
        diffPower.append(1)
        diffPress.append(1)


with open (fileOut, 'w') as f:
    f.write(f'RPM: {RPM}\n\n')
    f.write(f'Target power | DRK power | Targer pressure | DRK Pressure | diffPower | diffPressure\n')
    for dfpwr, dfprs, lcs, pwr, prs in zip(diffPower, diffPress, inputData, drkPower, drkPressure):
        f.write(f'{lcs["TargetPower"]} | {pwr} | {lcs["TargetPressure"]} | {prs} | {dfpwr} | {dfprs} \n')
    f.write(f'\nSummary diffPower: {sum(diffPower) / len(diffPower)}\n'
            f'Summary diffPressure: {sum(diffPress) / len(diffPress)}\n'
            f'Max diffPower: {max(diffPower)} {diffPower.index(max(diffPower)) + 1}\n'
            f'Max diffPressure: {max(diffPress)} {diffPress.index(max(diffPress)) + 1}\n\n')
    for pwr, prs in zip(drkPower, drkPressure):
        f.write(f'{pwr};{prs}\n')
