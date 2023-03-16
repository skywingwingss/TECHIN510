import pandas as pd
import random
import copy
import matplotlib.pyplot as plt

def delNonAlpha(wordlist):
  for i in range(len(wordlist)):
    newword=""
    for j in range(len(wordlist[i])):
      if wordlist[i][j].isalnum():
        newword+=wordlist[i][j]
    wordlist[i]=newword
  return wordlist

class chatbot():
    def __init__(self):
        self.dictPath_neg="negative_words.txt"
        self.dictpath_pos="positive_words.txt"
        self.name=""
        self.numQuestion=["How many pets have you ever raised?","How many books do you read each year?"]
        self.ynQuestion=["Do you like deserts?"]
        self.commonQuestion=["How was you last weekend?"]
        self.numAns=[-1 for i in range(len(self.numQuestion))]
        self.ynAns=[-1 for i in range(len(self.ynQuestion))]
        self.commonAns=["" for i in range(len(self.commonQuestion))]

        self.posResponse=["Great!","Cool!"]
        self.negResponse=["Too bad..","Womp, womp!"]
        self.netResponse=["Hmm..","I see.."]
        self.load_dict()

        self.answer_df=pd.DataFrame({})

    def load_dict(self):
        self.dict_pos=list(pd.read_csv(self.dictpath_pos, header=0).iloc[:,0].values)
        self.dict_neg=list(pd.read_csv(self.dictPath_neg, header=0).iloc[:,0].values)

    def addAnswer(self,Ans):
        name, numAns, ynAns, commonAns = Ans
        df_dict = {"Name":name}
        for que,ans in zip(self.numQuestion,numAns):
            df_dict[que]=ans
        for que,ans in zip(self.ynQuestion,ynAns):
            df_dict[que]=ans
        for que,ans in zip(self.commonQuestion,commonAns):
            df_dict[que]=ans
        new_df=pd.DataFrame(df_dict,index=[0])
        self.answer_df=self.answer_df.append(new_df)
        self.clean_answerbuffer()

    def clean_answerbuffer(self):
        self.numAns=[-1 for i in range(len(self.numQuestion))]
        self.ynAns=[-1 for i in range(len(self.ynQuestion))]
        self.commonAns=["" for i in range(len(self.commonQuestion))]
        self.name=""

    def get_inquiry(self):
        if self.name=="":
            return "Hello, what's your name?"
        if self.numAns[len(self.numAns)-1]==-1:
            return self.numQuestion[self.numAns.index(-1)]
        elif self.ynAns[len(self.ynAns) - 1] == -1:
            return self.ynQuestion[self.ynAns.index(-1)]

        elif self.commonAns[len(self.commonAns)-1]=="":
            return self.commonQuestion[self.commonAns.index("")]
        else:
            self.addAnswer((self.name, self.numAns, self.ynAns, self.commonAns))
            return self.get_inquiry()


    def set_answer(self,instream):
        if instream==None:
            return None
        if self.name == "":
            self.name=instream
            return "Hi, {}!".format(self.name)
        if self.numAns[len(self.numAns)-1]==-1:
            if not instream.isdigit():
                return "Input error! Please input a digit."
            else:
                self.numAns[self.numAns.index(-1)] = int(instream)
                return "Good! And..."

        if self.ynAns[len(self.ynAns) - 1] == -1:
            if not instream in ['y', 'n']:
                return "Input error! Please input 'y' or 'n'."

            else:
                if instream == 'y':
                    self.ynAns[self.ynAns.index(-1)] = 1
                else:
                    self.ynAns[self.ynAns.index(-1)] = 0
                return "Wow, and..."
        if self.commonAns[len(self.commonAns)-1]=="":
            self.commonAns[self.commonAns.index("")] = instream
            return self.responseSentimental(instream)



    def inquiry(self):
        numAns=[-1 for i in range(len(self.numQuestion))]
        ynAns=[-1 for i in range(len(self.ynQuestion))]
        commonAns=["" for i in range(len(self.commonQuestion))]
        name=str(input("Hi! What's your name?"))

        while numAns[len(numAns)-1]==-1:
            instream=input(self.numQuestion[numAns.index(-1)])
            if not instream.isdigit():
                print("Input error! Please input a digit.")
                continue
            else:
                print("Good! And...")
                numAns[numAns.index(-1)]=int(instream)

        while ynAns[len(ynAns) - 1] == -1:
            instream = str(input(self.ynQuestion[ynAns.index(-1)]))
            if not instream in ['y','n']:
                print("Input error! Please input 'y' or 'n'.")
                continue
            else:
                print("Wow, and...")
                if instream=='y':
                    ynAns[ynAns.index(-1)] = 1
                else:
                    ynAns[ynAns.index(-1)] = 0


        while commonAns[len(commonAns)-1]=="":
            instream=str(input(self.commonQuestion[commonAns.index("")]))
            commonAns[commonAns.index("")]=instream
            self.responseSentimental(instream)
        self.addAnswer((name,numAns,ynAns,commonAns))

    def responseSentimental(self,instream):
        wordlist = instream.split(" ")
        wordlist = delNonAlpha(wordlist)
        NegNum = 0
        PosNum = 0
        for word in wordlist:
            if word in self.dict_pos:
                PosNum += 1
            elif word in self.dict_neg:
                NegNum += 1
        if PosNum - NegNum > 0:
            return self.posResponse[random.randint(0, len(self.posResponse) - 1)]
        elif PosNum - NegNum < 0:
            return self.negResponse[random.randint(0, len(self.negResponse) - 1)]
        else:
            return self.netResponse[random.randint(0, len(self.netResponse) - 1)]

    def stat_bar(self,numQue_index):
        if len(self.answer_df.columns.tolist())>0:

            data=copy.deepcopy(self.answer_df)
            data.sort_values(by=[self.numQuestion[numQue_index]], ascending=False, inplace=True)
            data.set_index("Name", inplace=True)
            data.plot.bar(y=self.numQuestion[numQue_index])
            plt.savefig("./static/bar.png")
            #plt.show()
            Name = data.index[0]
            Num = str(data.iloc[0][self.numQuestion[numQue_index]])
            return Name + ' reads most books ' + Num + " each year."
            #print(Name + ' reads most books ' + Num + " each year.")
        else:
            return None



if __name__=="__main__":
    bot=chatbot()

    for i in range(3):
        bot.inquiry()
    bot.stat_bar(1)










