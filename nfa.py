import os
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
from dfa import DFA

class NFA:
    __graph=[];
    __alphabets=[];
    __final=[];
    __states=0;


    def __init__(self,states,alphabets) :
        #print(states,alphabets)

        self.__alphabets=alphabets;
        self.__states=states+1;

        for i in range(self.__states):
            self.__graph.append([[] for i in range(len(alphabets))])
        #print(self.__graph)


    def connect(self,st1,alph,st2):
        if(st2 not in self.__graph[st1][self.__alphabets.index(alph)]):
            self.__graph[st1][self.__alphabets.index(alph)].append(st2);

    def dotparse(s):
        if(s[0]=='.'):
            s=s[1:]
        if(s[-1]=='.'):
            s=s[:-1]   
        return s;  


    def finalStates(self,final):
        self.__final =final

    def printNFA(self):
        print(self.__graph)
        
        for i in range(self.__states):
            for j in range(len(self.__graph[i])):
                if(len(self.__graph[i][j])!=0):
                    for k in range(len(self.__graph[i][j])):
                        if((i) in self.__final):
                            state_to=f"(({i}))"
                        else:
                            state_to=f" ({i}) "
                        
                        if((self.__graph[i][j][k]) in self.__final):
                            state_from=f"(({self.__graph[i][j][k]}))"
                        else:
                            state_from=f" ({self.__graph[i][j][k]}) "

                        print(state_to+ f"  ->{self.__alphabets[j]}-> "+ state_from)


    def efsilon_closure(self,n):   
        closure=[i for i in n]
        ans=[i for i in n]
        while(len(closure)>0):
            if(len(self.__graph[closure[0]][self.__alphabets.index(None)])!=0):
                for i in self.__graph[closure[0]][self.__alphabets.index(None)]:
                    if(i not in ans):
                        closure.append(i)
                        ans.append(i)
            closure.pop(0)
        #print(ans)
        return ans


    def toDFA(self):
        DFAgraph=[]

        DFAstate=[self.efsilon_closure([0])]
        DFAqueue=[self.efsilon_closure([0])]
        DFAcount=0;    

        alpl=len(self.__alphabets)
        dfalen=2**len(self.__graph)
       
        #DFAgraph.append([[] for i in range(alpl)])

        while(len(DFAqueue)>0):
            DFAgraph.append([-1 for i in range(alpl)])
            for i in range(alpl):
                if(self.__alphabets[i]!=None):
                    # print(DFAcount)
                    if(None in self.__alphabets):
                        efcl=self.efsilon_closure(DFAqueue[0])
                    else:
                        efcl=DFAqueue[0]
                    #print("efcl: ",efcl)
                    nextstep=[]
                    for j in range(len(efcl)):
                        #print("moveto: ",efcl[j],self.__alphabets[i],self.__graph[efcl[j]][i])
                        movepos=self.__graph[efcl[j]][i]
                        if(len(movepos)!=0):
                            for k in movepos:
                                if(k not in nextstep):nextstep.append(k)
                        # print(movepos)
                    nextstep=self.efsilon_closure(nextstep)
                    nextstep.sort();
                    print(efcl,f"->{self.__alphabets[i]}->",nextstep)

                    if(nextstep not in DFAstate):
                        print(DFAcount,f"->{self.__alphabets[i]}->",len(DFAstate))
                        DFAgraph[DFAcount][i]=len(DFAstate)
                        
                        DFAstate.append(nextstep)
                        DFAqueue.append(nextstep)
                    else:
                        print(DFAcount,f"->{self.__alphabets[i]}->",DFAstate.index(nextstep))
                        DFAgraph[DFAcount][i]=DFAstate.index(nextstep)
                    print(DFAgraph)
            DFAcount+=1;
            
        
            #print(DFAstate)
            #print(DFAgraph)

            DFAqueue.pop(0)

        # print(DFAgraph)
        print("DFAstate: ",DFAstate)

        alphabets=[i for i in self.__alphabets]

        if(None in alphabets):
            alphabets.remove(None)
        print(self.__final)
        b=DFA(DFAcount+1,self.__alphabets)

        for i in range(len(DFAgraph)):
            for j in range(len(DFAgraph[0])):
                if(DFAgraph[i][j]!=-1):
                    print(i,self.__alphabets[j],DFAgraph[i][j])
                    b.connect(i,self.__alphabets[j],DFAgraph[i][j])

        DFAfinal=[]    
        # print(DFAgraph)
        for i in DFAstate:
            print(i)
            for j in self.__final:
                if(j in i):DFAfinal.append(DFAstate.index(i))
        print("DFAfinal ",DFAfinal)
        b.finalStates(DFAfinal)
       
        return b;






    def examine(self,pattern):
        exam=self.toDFA()
        exam.printDFA()
        return exam.examine(pattern)
   




if __name__=="__main__" :

    clearConsole()


    b=NFA(10,[None,'a','b'])

    # b.connect(1,'a',1)
    # b.connect(1,'b',1)
    # b.connect(1,'a',2)

    # b.connect(2,'b',3)
    # b.connect(0,None,1)
    # b.connect(1,None,2)
    # b.connect(1,None,4)
    # b.connect(1,None,7)
    # b.connect(2,'a',3)
    # b.connect(4,'b',5)
    # b.connect(3,None,6)
    # b.connect(5,None,6)
    # b.connect(6,None,7)
    # b.connect(6,None,1)
    # b.connect(7,'a',8)










    # b.connect(8,'b',9)
    # b.connect(9,'b',10)
    b.connect(0,None,2)
    b.connect(0,None,2)
    b.connect(2,'a',3)
    b.connect(4,'b',5)
    b.connect(3,None,1)
    b.connect(5,None,1)


    b.finalStates([1])
    b.printNFA()

    b.toDFA();

    print(b.examine("b"))
   







    
    