 
file1 = open('text1.txt','r')
f = file1.read()
f = f.replace('\n',' ')
f = f.split(' ')
file1.close()
textDict = {}
for i in enumerate(f):
    x,y = i
    textDict[y] = f.count(y)
file2 = open('textDict.txt','w')
file2.write(str(textDict))
file2.close()