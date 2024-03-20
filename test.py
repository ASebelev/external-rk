with open('./testPyRK/FromServ0/ul520is.res', 'r') as f:
    tmp = f.readlines()
variable = []
dicc = {}
for i in range(7, len(tmp)):
    line = tmp[i]
    if "-----" in line or len(line.replace('\n','')) == 0 or 'Ядро' in line or 'Оцен' in line:
        continue
    line = line.split()
    try:
        first = line[2].replace('-', '')
        variable.append(first)
        second = ' '.join(line[3:]).replace('- ', '').replace(',',';')
        print(f'{first};{second}')
        dicc[first] = second
    except:
        pass
print(variable)
for key, val in dicc.items():
    print(f"'{key}':'{val}',")