import os


for file in os.listdir():
    name, ext = file.split('.')
    if ext in ['csv', 'txt']:
        os.rename(file, name+'.expect')
