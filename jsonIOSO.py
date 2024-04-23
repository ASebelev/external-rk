import json

with open('./IOSO-Py-DRK/IN.json', 'r') as f:
    inputData = json.load(f)

inputData.pop(0)
with open('./IOSO-Py-DRK/entryppoint.csv', 'w') as f:
    values = ''
    for i,loadCase in enumerate(inputData):
        for title, value in loadCase.items():
            if 'Target' in title:
                continue
            f.write(f'{title}{i + 1};')
            values += str(value).replace('.',',') + ';'
    f.write(f'\n{values}')
