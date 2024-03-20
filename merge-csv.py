import pandas as pd
import os

input_folder = './input'
output_file = 'output.xlsx'

files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

writer = pd.ExcelWriter(output_file)
for file in files:
    df = pd.read_csv(os.path.join(input_folder, file), encoding='cp1251')
    df.to_excel(writer, sheet_name=os.path.splitext(file)[0], index=False)

writer.save()
