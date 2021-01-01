# Simple enough, just import everything from tkinter.
from tkinter import *
from functools import partial
import docx
import random
import os
from fnmatch import fnmatch
#action_with_arg = partial(action, arg)



# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        print('Init')
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    def readquestions(self,filename,quizname):
        self.questionon=0
        self.totalquestions=0
        self.questions=[]
        self.options=[]
        self.answers=[]
        self.filename=filename
        self.quizname=quizname
        doc = docx.Document('quizzes/'+filename)
        lineon=0
        started=False
        for paragraph in doc.paragraphs:
            line=paragraph.text
            if(started):
                if(line!=''):
                    if(lineon%6<1):
                        self.options.append([])
                        self.questions.append(line)
                    elif(lineon%6<5):
                        self.options[-1].append(line)
                    else:
                        self.answers.append(line)
                        self.totalquestions+=1
                    lineon+=1
            if(line=='START'):
                started=True
                print('START')
            if(line=='END'):
                print('END')
                break
        #print(self.questions)
        #print(self.options)
        #print(self.answers)
        self.setupquestions()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("Robotics Quiz Game")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        mainmenu = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        mainmenu.add_command(label="Exit", command=self.client_exit)

        #added "Exit" to our menu
        menu.add_cascade(label="Quiz Game", menu=mainmenu)

        #OTHER VARIABLES
        self.aiscore=0
        self.difficulty=0
        self.difficultynames=['Easy','Normal','Hard','Intense']
        self.correctchances=[40,60,80,100]

        self.create_elements()
        self.startmenu()

    def getquizinfo(self):
        print('Get Quiz info')
        file1 = open('topscores.txt', 'r')
        lineon=0
        self.quizfiles=[]
        self.quiztitles=[]
        self.topscores=[]
        self.maxscores=[]
        for line in file1: 
            line=line.strip()
            if(line!=''):
                if(lineon%4==0):
                    self.quiztitles.append(line)
                elif(lineon%4==1):
                    self.quizfiles.append(line)
                elif(lineon%4==2):
                    self.topscores.append(int(line))
                else:
                    self.maxscores.append(int(line))
                lineon+=1
        print(self.quiztitles)
        print(self.quizfiles)
        print(self.topscores)
        print(self.maxscores)
        file1.close()

    def startmenu(self):
        
        print('Start Menu')
        
        self.getquizinfo()
        
        self.startbuttons=[]
        i=0
        print(self.quiztitles)
        for i in range(len(self.quiztitles)):
            print('Go')
            title=self.quiztitles[i]+' '+str(self.topscores[i])+'/'+str(self.maxscores[i])
            #self.optiona.config(text=self.options[self.questionon][0],command=partial(self.enteranswer, self.options[self.questionon][0]))
            self.startbuttons.append(Button(text=title, command=partial(self.readquestions,self.quizfiles[i],self.quiztitles[i]),font=('Courier',32),width=len(title)+1))
            self.startbuttons[-1].place(x=125, y=350+i*100)
            i+=1
        
        self.hidequizelements()
        self.showmenuelements()

    def enteranswer(self,answerselected):
        print('You selected',answerselected)
        roll=random.randint(1,100)
        if(self.difficulty==len(self.difficultynames)-1 and self.questionon==self.totalquestions-1):
            self.aiscore+=0
        else:
            if(roll>=100-self.correctchances[self.difficulty]):
                self.aiscore+=1
                self.aiscorelabel.config(text=str(self.aiscore))
        
        if(answerselected==self.answers[self.questionon]):
            self.resultlabel.config(text='Correct')
            self.correctanswers+=1
        else:
            self.resultlabel.config(text='Incorrect')
        self.nextquestion()
    
    def create_elements(self):
        self.titleLabel=Label(self.master,text='Robotics Quiz',font=('Courier',64),width=14,borderwidth=5,relief='solid')

        self.questionlabel=Message(text='',font=("Courier",20))
        self.quiztitlelabel=Label(text="Quiz Title",font=("Courier", 36))
        self.resultlabel=Label(text='',width=10,borderwidth=3,relief='solid',font=("Courier", 36))
        self.questionondescriptor=Label(text='Question #',font=("Courier",24))
        self.questiononlabel=Label(text='',width=7,borderwidth=3,relief='solid',font=("Courier", 36))
        
        self.optiona=Button(text='',width=20,height=8,wraplength=250,borderwidth=3,relief='solid',font=("Courier", 20))
        self.optionb=Button(text='',width=20,height=8,wraplength=250,borderwidth=3,relief='solid',font=("Courier", 20))
        self.optionc=Button(text='',width=20,height=8,wraplength=250,borderwidth=3,relief='solid',font=("Courier", 20))
        self.optiond=Button(text='',width=20,height=8,wraplength=250,borderwidth=3,relief='solid',font=("Courier", 20))
        self.quiztitlelabel=Label(text="Quiz Title",font=("Courier", 36))

        self.resultlabel=Label(text='',width=10,borderwidth=3,relief='solid',font=("Courier", 24))

        self.questionondescriptor=Label(text='Question #',font=("Courier",18))
        self.questiononlabel=Label(text='',width=7,borderwidth=3,relief='solid',font=("Courier", 20))

        self.tallydescriptor=Message(text='Correct vs Incorrect',font=("Courier",18),width=125)
        self.tallylabel=Label(text='',width=7,borderwidth=3,relief='solid',font=("Courier", 24))

        self.aiscoredescriptor=Label(text='AI Score',font=("Courier",18))
        self.showaidifficulty=Label(text=self.difficultynames[0],font=("Courier",24))
        self.aiscorelabel=Label(text='0',width=3,borderwidth=3,relief='solid',font=("Courier", 24))

        self.displaywinner=Label(text='Player Wins',font=("Courier",36))
        self.returntostartmenu=Button()

        #Difficulty elements
        self.difficultylabel=Label(text='Select Difficulty',font=("Courier",36))
        self.difficultybuttons=[]
        for i in range(len(self.difficultynames)):
            self.difficultybuttons.append(Button(text=self.difficultynames[i],font=("Courier",36),command=partial(self.showquizelements,i)))

    def hidequizelements(self):
        self.questionlabel.place_forget()
        self.quiztitlelabel.place_forget()
        self.resultlabel.place_forget()

        self.questionondescriptor.place_forget()
        self.questiononlabel.place_forget()

        self.tallylabel.place_forget()
        self.tallydescriptor.place_forget()


        self.optiona.place_forget()
        self.optionb.place_forget()
        self.optionc.place_forget()
        self.optiond.place_forget()

        self.returntostartmenu.place_forget()

        self.aiscorelabel.config(text='0')
        self.aiscorelabel.place_forget()
        self.aiscoredescriptor.place_forget()
        self.showaidifficulty.place_forget()
        self.displaywinner.place_forget()

    def showquizelements(self,difficulty):
        self.hidedifficultyelements()

        self.questionlabel.place(x=50,y=50)
        self.quiztitlelabel.place(x=50,y=0)
        self.resultlabel.place(x=50,y=250)

        self.questionondescriptor.place(x=300,y=200)
        self.questiononlabel.place(x=300,y=250)
        self.questionlabel.config(font=("Courier",20))

        self.tallylabel.place(x=450,y=250)
        self.tallydescriptor.place(x=450,y=200)

        self.aiscoredescriptor.place(x=650,y=200)
        self.showaidifficulty.place(x=650,y=220)
        self.aiscorelabel.place(x=650,y=250)

        self.optiona.place(x=50,y=350)
        self.optionb.place(x=400,y=350)
        self.optionc.place(x=50,y=600)
        self.optiond.place(x=400,y=600)

        self.difficulty=difficulty
        self.showaidifficulty.config(text=self.difficultynames[self.difficulty])

    def hidemenuelements(self):
        self.titleLabel.place_forget()
        for i in range(len(self.startbuttons)):
            self.startbuttons[i].place_forget()

    def showmenuelements(self):
        self.titleLabel.place(x=125, y=50)
        for i in range(len(self.startbuttons)):
            self.startbuttons[i].place(x=125, y=250+i*100)
    
    def showdifficultyelements(self):
        self.difficultylabel.place(x=125,y=100)
        for i in range(len(self.difficultybuttons)):
            self.difficultybuttons[i].place(x=125,y=200+100*i)

    def hidedifficultyelements(self):
        self.difficultylabel.place_forget()
        for i in range(len(self.difficultybuttons)):
            self.difficultybuttons[i].place_forget()

    def endgame(self):
        self.updatequizinfo(self.filename,self.correctanswers)
        self.tallylabel.config(text=str(self.correctanswers)+'/'+str(self.totalquestions))
        self.questionlabel.config(text='Quiz Completed',font=("Courier",48))

        self.resultlabel.config(text='Results')

        self.returntostartmenu.config(text='Return to Main Menu',font=("Courier",48),command=self.startmenu)
        self.returntostartmenu.place(x=50,y=400)
        if(self.aiscore>self.correctanswers):
            self.displaywinner.config(text='AI Wins')
        else:
            self.displaywinner.config(text='Player Wins')
        self.displaywinner.place(x=50,y=200)

        self.optiona.place_forget()
        self.optionb.place_forget()
        self.optionc.place_forget()
        self.optiond.place_forget()
        self.aiscore=0
    
    def updatequizinfo(self,filename,quizscore):

        file1 = open('topscores.txt', 'w')
        for i in range(len(self.quiztitles)):
            if(self.quizfiles[i]==filename):
                print(quizscore,self.topscores[i])
                file1.write(self.quiztitles[i]+'\n')
                file1.write(self.quizfiles[i]+'\n')
                if(quizscore>self.topscores[i]):
                    file1.write(str(quizscore)+'\n')
                else:
                    file1.write(str(self.topscores[i])+'\n')
                file1.write(str(self.maxscores[i])+'\n')
            else:
                file1.write(self.quiztitles[i]+'\n')
                file1.write(self.quizfiles[i]+'\n')
                file1.write(str(self.topscores[i])+'\n')
                file1.write(str(self.maxscores[i])+'\n')
            file1.write('\n')
        file1.close()

    def nextquestion(self):
        print(self.questionon,self.totalquestions)
        if(self.questionon<self.totalquestions-1):
            self.questionon+=1
            self.questiononlabel.configure(text=str(self.questionon+1)+'/'+str(self.totalquestions))
            self.tallylabel.configure(text=str(self.correctanswers)+'/'+str(self.questionon))
            print(self.options[self.questionon])

            random.shuffle(self.options[self.questionon])
            self.questionlabel.config(text=self.questions[self.questionon])
            self.optiona.config(text=self.options[self.questionon][0],command=partial(self.enteranswer, self.options[self.questionon][0]))
            self.optionb.config(text=self.options[self.questionon][1],command=partial(self.enteranswer, self.options[self.questionon][1]))
            self.optionc.config(text=self.options[self.questionon][2],command=partial(self.enteranswer, self.options[self.questionon][2]))
            self.optiond.config(text=self.options[self.questionon][3],command=partial(self.enteranswer, self.options[self.questionon][3]))
        else:
            self.endgame()
            
    
    def setupquestions(self):
        self.questionon=0
        self.questionlabel.configure(text=self.questions[0],borderwidth=3,relief='solid')
        self.questionlabel.configure(width=700)

        self.quiztitlelabel.config(text=self.quizname,font=("Courier", 36))

        self.resultlabel.config(text='',width=10,borderwidth=3,relief='solid')

        self.questionondescriptor.config(text='Question #')
        self.questiononlabel.config(text='',width=7,borderwidth=3,relief='solid',font=("Courier", 24))


        self.tallylabel.config(text='',width=7,borderwidth=3,relief='solid')


        random.shuffle(self.options[self.questionon])

        self.correctanswers=0

        self.tallylabel.config(text=str(self.correctanswers)+'/'+str(self.questionon))
        self.questiononlabel.config(text=str(self.questionon+1)+'/'+str(self.totalquestions))

        self.optiona.config(text=self.options[self.questionon][0],command=partial(self.enteranswer, self.options[self.questionon][0]))

        self.optionb.config(text=self.options[self.questionon][1],command=partial(self.enteranswer, self.options[self.questionon][1]))

        self.optionc.config(text=self.options[self.questionon][2],command=partial(self.enteranswer, self.options[self.questionon][2]))

        self.optiond.config(text=self.options[self.questionon][3],command=partial(self.enteranswer, self.options[self.questionon][3]))

        self.hidemenuelements()
        #self.showquizelements()
        self.showdifficultyelements()

    def client_exit(self):
        exit()


# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

root.geometry("900x800")

#creation of an instance
app = Window(root)


#mainloop 
root.mainloop()