from typing import Pattern, final
from dfa import DFA
from nfa import NFA
import os

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')




class regularExpression:
    __patern="";
    __mpat="";
    __alphabets=[None]
    __small_latters="";
    __capital_latters="";
    for i in range(ord('a'),ord('z')):__small_latters+=chr(i)+"|"
    __small_latters+="z"
    for i in range(ord('A'),ord('Z')):__capital_latters+=chr(i)+"|"
    __capital_latters+="Z"
    __graph=[]
    __nfa_steps=[]
    __nfa_queue=[]
    __nfa_states=0;
    __nfa="";

    __changes={
        "0-9":"0|1|2|3|4|5|6|7|8|9",
        "a-z":__small_latters,
        "A-Z":__capital_latters
    }


    def __init__(self,pattern):
        self.__patern=pattern
        self.interchange()
        self.alphaStore()
        self.modify()
        
        pass

    def interchange(self):
        self.__patern=self.__patern.replace(" ","")
        for i in self.__changes.keys():
            self.__patern=self.__patern.replace(i,self.__changes[i]) 
        self.__patern=self.__patern.replace("[","(")
        self.__patern=self.__patern.replace("]",")")
        #print(self.__patern)



    def alphaStore(self):
        for i in range(len(self.__patern)):
             if((self.__patern[i]!='*') 
            and (self.__patern[i]!='|')
            and (self.__patern[i]!='+')
            and (self.__patern[i]!='.')
            and (self.__patern[i]!='(')
            and (self.__patern[i]!=')')
            and (self.__patern[i]!='?')
            ):
                if(self.__patern[i] not in self.__alphabets):
                    self.__alphabets.append(self.__patern[i])
        #print(self.__alphabets)

    def trail_brackets(self,s):
        while((s[0]=="(") and (s[-1]==")")):
            s=s[1:-1]
        return s
        

    def divide(self,st):
        b=0;
        s=""
        arr=[]
        final_arr=[]
        operation=None
        for i in range(len(st)):
            if(st[i]=="("):b+=1
            elif(st[i]==")"):b-=1
            if((st[i]=="|") and (b==0)):
                arr.append(s)
                s=""
            else:
                s+=st[i]
        arr.append(s)
        ##print(arr,"|")    
        operation="|"
        if(len(arr)==1):
            b=0;
            s=""
            arr=[]
            for i in range(len(st)):
                if(st[i]=="("):b+=1
                elif(st[i]==")"):b-=1
                if((st[i]=="~") and (b==0)):
                    arr.append(s)
                    s=""
                else:
                    s+=st[i]
            arr.append(s)
            ##print(arr,"~")  
            operation="~"
        
        ##print(arr)     
        if((len(arr)==1)and ((arr[0][-1]=="*") or (arr[0][-1]=="+")  or (arr[0][-1]=="?"))):
            operation=arr[0][-1]
            arr[0]=arr[0][:-1]
            #arr[0]=self.trail_brackets(arr[0])
        elif((len(arr)==1)):
            operation=None
        if(operation!=None) :  
            for i in range(len(arr)):arr[i]=self.trail_brackets(arr[i])

        final_arr=[arr,operation]
        ##print("final: ",final_arr)
        return final_arr
        

    def modify(self):
        self.__mpat=""
        for i in range(len(self.__patern)):
            self.__mpat+=self.__patern[i];
            try:
                if((self.__patern[i] in self.__alphabets)
                and (self.__patern[i+1] in self.__alphabets)):
                    self.__mpat+="~";
                elif(((self.__patern[i]=="*") or (self.__patern[i]=="+")  or (self.__patern[i]=="?"))
                and (self.__patern[i+1] in self.__alphabets)):
                    self.__mpat+="~";
                
                elif(((self.__patern[i]=="*") or (self.__patern[i]=="+")  or (self.__patern[i]=="?"))
                and (self.__patern[i+1]=="(")):
                    self.__mpat+="~";
                
                elif((self.__patern[i] in self.__alphabets)
                and (self.__patern[i+1]=="(")):
                    self.__mpat+="~";
                elif((self.__patern[i]==")")
                and (self.__patern[i+1]=="(")):
                    self.__mpat+="~";

                elif((self.__patern[i]==")")
                and (self.__patern[i+1] in self.__alphabets)):
                    self.__mpat+="~"; 
            except:
                continue 
        #print("here")  
        #print(self.__mpat)
        self.__nfa_steps =[[0,self.__mpat,1]]
        self.__nfa_states+=2;
        self.__nfa_queue=[self.__mpat]
        

    def create_nfa(self):
        # split_arr=self.divide(self.__nfa_queue[0])
        counter=0;
        graph=[[[] for i in range(len(self.__alphabets))]]
        for j in range(400):graph.append([[] for k in range(len(self.__alphabets))]);
        #print(self.divide(self.__nfa_queue[0]))
        # #print(self.divide(split_arr[0]))
        while(len(self.__nfa_queue)>0):
            ##print(self.__nfa_queue[0])  
            split_arr=self.divide(self.__nfa_queue[0])
            if(split_arr[1]==None):
                counter+=1
                self.__nfa_queue.pop(0)
                continue;
            for i in range(len(split_arr[0])):            
                # #print(self.__nfa_states,counter)
                # #print(self.__nfa_queue[0],self.__nfa_steps[counter])
                self.__nfa_queue.append(split_arr[0][i])
                self.__nfa_steps.append([self.__nfa_states,split_arr[0][i],self.__nfa_states+1])
                if(split_arr[1]=="|"):
                    # #print(self.__nfa_steps[counter],self.__nfa_states,counter)
                    graph[self.__nfa_steps[counter][0]][0].append(self.__nfa_states);
                    graph[self.__nfa_states+1][0].append(self.__nfa_steps[counter][2]);
                if(split_arr[1]=="~"):
                    # #print(self.__nfa_states,i)
                    if(i==0):
                        # #print(self.__nfa_states,counter)
                        graph[self.__nfa_steps[counter][0]][0].append(self.__nfa_states);
                    if(i==len(split_arr[0])-1):
                        # #print(self.__nfa_states,counter)
                        graph[self.__nfa_states+1][0].append(self.__nfa_steps[counter][2]);
                    else:
                        graph[self.__nfa_states+1][0].append(self.__nfa_states+2);
                if(split_arr[1]=="+"):
                    graph[self.__nfa_steps[counter][0]][0].append(self.__nfa_states)
                    graph[self.__nfa_states+1][0].append(self.__nfa_steps[counter][2])
                    graph[self.__nfa_states+1][0].append(self.__nfa_states)
                if(split_arr[1]=="*"):
                    graph[self.__nfa_steps[counter][0]][0].append(self.__nfa_states)
                    graph[self.__nfa_states+1][0].append(self.__nfa_steps[counter][2])
                    graph[self.__nfa_states+1][0].append(self.__nfa_states)
                    graph[self.__nfa_steps[counter][0]][0].append(self.__nfa_steps[counter][2])

                if(split_arr[1]=="?"):
                    graph[self.__nfa_steps[counter][0]][0].append(self.__nfa_states)
                    graph[self.__nfa_states+1][0].append(self.__nfa_steps[counter][2])
                    #graph[self.__nfa_states+1][0].append(self.__nfa_states)
                    graph[self.__nfa_steps[counter][0]][0].append(self.__nfa_steps[counter][2])

                if(split_arr[0][i] in self.__alphabets):
                    #print(split_arr[0][i],self.__nfa_states)
                    graph[self.__nfa_states][self.__alphabets.index(split_arr[0][i])].append(self.__nfa_states+1);
                elif(split_arr[0][i]=="!"):
                    graph[self.__nfa_states][0].append(self.__nfa_states+1);
                self.__nfa_states+=2 

            self.__nfa_queue.pop(0)
            counter+=1
        #print(self.__nfa_steps)
        # for k in range(self.__nfa_states+1):
        #     print(f"{k}: ",graph[k])

        #print(graph[:self.__nfa_states+1])

        self.__nfa=NFA(self.__nfa_states+2,self.__alphabets)

        for states in range(self.__nfa_states+1):
            for i in range(len(graph[states])):
                for j in graph[states][i]:
                    self.__nfa.connect(states,self.__alphabets[i],j)
        
        self.__nfa.finalStates([1])
        #self.__nfa.printNFA()

        #self.__nfa.toDFA();

        #print(self.__nfa.examine("bababbabacdd"))


    def printNFA(self):
        self.create_nfa()
        self.__nfa.printNFA()

    def printDFA(self):
        self.create_nfa()
        self.__nfa.printDFA()


    def examine(self,pattern):
        self.create_nfa()
        return self.__nfa.examine(pattern)



 

if __name__=="__main__":
    clearConsole()
    r=regularExpression("(ca)*b")
    #r.printNFA()
    #r.printDFA()
    print(r.examine("b"))
    print(r.examine("cab"))
    print(r.examine("cacab"))
    #r=regularExpression("((ab)*)")

