import os
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

class DFA:
    __graph=[];
    __alphabets=[];
    __final=[];
    __states=0;



    def __init__(self,states,alphabets) :
        #print(states,alphabets)

        self.__alphabets=alphabets;
        self.__states=states;

        for i in range(self.__states):
            self.__graph.append([-1]*len(alphabets))
        #print(self.__graph)


    def connect(self,st1,alph,st2):
        self.__graph[st1][self.__alphabets.index(alph)]=st2;



    def finalStates(self,final):
        self.__final =final

    def printDFA(self):
        for i in range(self.__states):
            for j in range(len(self.__graph[i])):
                if(self.__graph[i][j]!=-1):
                    if(i in self.__final):
                        state_to=f"(({i}))"
                    else:
                        state_to=f" ({i}) "
                    
                    if((self.__graph[i][j]) in self.__final):
                        state_from=f"(({self.__graph[i][j]}))"
                    else:
                        state_from=f" ({self.__graph[i][j]}) "

                    print(state_to+ f"  -> {self.__alphabets[j]} -> "+ state_from)
    
    def examine(self,pattern):
        current_state = 0
        for i in pattern:
            if(i not in self.__alphabets):return False
            current_state=self.__graph[current_state][self.__alphabets.index(i)]
            #print(i," -> ",current_state+1)
        if(current_state in self.__final):
            return True
        return False
   




if __name__=="__main__" :

    clearConsole()

    #a=DFA(2,['a','b'])

    # a.connect(1,'b',1)
    # a.connect(1,'a',2)
    # a.connect(2,'b',1)
    # a.connect(2,'a',2)
    # a.finalStates([2])
    # a.printDFA();
    # print(a.examine("abbababbababababbababab"))


    b=DFA(5,['a','b'])

    b.connect(1,'a',2)
    b.connect(1,'b',4)

    b.connect(2,'a',2)
    b.connect(2,'b',3)

    b.connect(3,'b',3)
    b.connect(3,'a',2)

    b.connect(4,'b',4)
    b.connect(4,'a',4)

    b.finalStates([3])
    b.printDFA()
    print(b.examine("abab"))








    
    