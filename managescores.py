import os
from fnmatch import fnmatch
import docx

filenames=[]
quiznames=[]
topscores=[]
maxscores=[]

def getquizinfo():
    global filenames
    global quiznames
    global topscores
    global maxscores

    file1 = open('topscores.txt', 'r')
    lineon=0
    filenames=[]
    quiznames=[]
    topscores=[]
    maxscores=[]
    for line in file1: 
        line=line.strip()
        if(line!=''):
            print(line)
            if(lineon%4==0):
                quiznames.append(line)
            elif(lineon%4==1):
                filenames.append(line)
            elif(lineon%4==2):
                topscores.append(int(line))
            else:
                maxscores.append(int(line))
            lineon+=1
    print(quiznames)
    print(filenames)
    print(topscores)
    print(maxscores)
    file1.close()

def updatequizinfo(filename,quizscore):
    global filenames
    global quiznames
    global topscores
    global maxscores

    file1 = open('topscores.txt', 'w')
    for i in range(len(quiznames)):
        if(filenames[i]==filename):
            print(quizscore,topscores[i])
            file1.write(quiznames[i]+'\n')
            file1.write(filenames[i]+'\n')
            if(quizscore>topscores[i]):
                file1.write(str(quizscore)+'\n')
            else:
                file1.write(str(maxscores[i])+'\n')
            file1.write(str(maxscores[i])+'\n')
        else:
            file1.write(quiznames[i]+'\n')
            file1.write(filenames[i]+'\n')
            file1.write(str(topscores[i])+'\n')
            file1.write(str(maxscores[i])+'\n')
        file1.write('\n')
    file1.close()
def resetdata():
    root = 'quizzes/'
    pattern = "*.docx"
    quizfiles=[]
    quiztitles=[]
    maxscores=[]
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern) and '$' not in name:
                print(os.path.join(path, name))
                totalquestions=0
                lineon=0
                started=False
                gettitlenext=False
                title=''
                doc = docx.Document(os.path.join(path, name))
                for paragraph in doc.paragraphs:
                    line=paragraph.text
                    if(started):
                        if(line!=''):
                            if(lineon%6==5):
                                totalquestions+=1
                            lineon+=1
                    if(gettitlenext):
                        title=line
                        gettitlenext=False
                    if(line=='TITLE'):
                        gettitlenext=True
                    if(line=='START'):
                        started=True
                        print('START')
                    if(line=='END'):
                        print('END')
                        quizfiles.append(name)
                        quiztitles.append(title)
                        maxscores.append(totalquestions)
                        break
    print(quizfiles)
    print(quiztitles)
    print(maxscores)
    file1 = open('topscores.txt', 'w')
    for i in range(len(quiztitles)):
        file1.write(quiztitles[i]+'\n')
        file1.write(quizfiles[i]+'\n')
        file1.write('0\n')
        file1.write(str(maxscores[i])+'\n')
        file1.write('\n')
    file1.close()

def main():
    getquizinfo()
    #updatequizinfo('structuretutorial.docx',4)
    resetdata()
main()