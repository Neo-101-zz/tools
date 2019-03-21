from __future__ import print_function
import time

path_txt = r'TEMP.txt'
path_pro = input('Input the path of result file: ')

if __name__ == '__main__':
    import sys
    start = time.time()
    with open(path_txt,'rb') as fread:
        count = 0
        last_data = '\n'
        while True:
            data = fread.read(0x400000)
            if not data:
                break
            count += data.count(b'\n')
            last_data = data
        if last_data[-1:] != b'\n':
            count += 1 # Remove this if a wc-like count is needed
    end = time.time()
    print(count)
    print((end-start) * 1000)
    fread.close()

empty_or_not = []
with open(path_txt,'r', encoding='utf-8') as fread:
    for i in range(count):
        line = fread.readline()
        if line == '\n':
            empty_or_not.append(True)
        else:
            empty_or_not.append(False)
fread.close()

print(empty_or_not[0:10])

with open(path_txt,'r', encoding='utf-8') as fread:
    with open(path_pro,'w', encoding='utf-8') as fwrite:
        for i in range(0, count-1):
            line = fread.readline()
            line = line.replace("- ", "")
            line = ' '.join(filter(None, line.split(' ')))
            if empty_or_not[i] == True:
                if empty_or_not[i+1] == False:
                    fwrite.write(line)
            else:
                if line[-2:-1] != "." and empty_or_not[i+1] == False:
                    fwrite.write(line.strip('\n'))
                else:
                    fwrite.write(line)
        line = fread.readline()
        fwrite.write(line)
    fwrite.close()
fread.close()
