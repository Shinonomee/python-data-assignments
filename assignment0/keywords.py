import os
filedir = os.getcwd()+ '//articles'
filenames = os.listdir(filedir)
f=open('result.txt','w',encoding = 'utf-8')
for filename in filenames:
    filepath = filedir+'//'+filename
    for line in open(filepath,encoding='utf-8'):
        f.writelines(line)
        f.write('\n')
f.close()

with open('result.txt','r',encoding='utf-8')as f:
    contents = f.read()
contents.split()

frequency = {}
for word in contents.split():
    if word not in frequency:
        frequency[word]=1
    else:
        frequency[word]+=1

stop_words = ["the", "and", "of", "a", "in","as","on","with","that","to","is","The","for","it","has","are","not","have","its"]
for i in stop_words:
    if frequency.get(i):
        del frequency[i]

mylist = sorted(frequency.items(),key=lambda frequency:frequency[1],reverse=True)

import csv
with open('keywords.csv','w',newline = '') as  f:
    mywriter = csv.writer(f)
    header = ['keyword','frequency']
    mywriter.writerow(header)
    mywriter.writerows(mylist[0:15])