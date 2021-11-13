import os
from nfa import NFA


clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

# [[['a|b'], ['*']]
# , [['a'], []]
# , [['b'], []], 
#   [         [['a'], []],
#              [['b'], []], 
#              [['a|b'], ['?']]]]

# [
#     [['a|b'], ['*']], 
#     [['a'], []], 
#     [['b'], []], 
#     [           [['a'], []], 
#                 [['b'], []], 
#                 [
#                     [['a'], []],
#                     [['|'],[]], 
#                     [['b|c'], ['+']]
#                 ]
#     ]
# ]





class regularExpression:

    #  * , + , ? ,() , | ,

    def __init__(self):
        pass

    def subparse(self,s):
        queue=0
        parser=""
        parsed=[]
        for i in range(len(s)):
            if(s[i]=="("):queue+=1;
            if(s[i]==")"):queue-=1;
            if(((s[i]=="(") and (queue==1)) or ((s[i]==")") and (queue==0))):
                pass
            else:
                parser+=s[i]

            print(queue,parser)
            if(queue==0):
                if((parser!="*") and (parser!="+") and (parser!="?")):
                    try:
                        if((s[i+1]=="*")or(s[i+1]=="+")or(s[i+1]=="?")):
                            parsed.append([[parser],[s[i+1]]])
                        else:
                            parsed.append([[parser],[]])
                    except:
                        parsed.append([[parser],[]])
                parser=""
            
        return parsed
    def brackets(self,s):
        count=0;
        for i in s:
            if((i=="(") or (i==")")):count+=1
        return count
    def add_brackets(self):
        a=[]
        a[:0]=self.__patern
        print(a)
        i=0;
        while(i<len(a)):
            if((a[i]=='*') or (a[i]=='+')):
                try:
                    if(a[i-1] in self.__alphabets):
                        a.insert(i+1,")")
                        a.insert(i-1,"(")
                    elif(a[i-1]==")"):
                        a.insert(i+1,")")
                        b=1;j=i-2
                        while(b!=0):
                            if(a[j]==")"):b+=1
                            elif(a[j]=="("):b-=1
                            j-=1;
                        a.insert(j+1,"(")
                    i+=2;
                except:
                    continue
                i+=1;
        self.__patern="".join(a)
        print(self.__patern)
    
    def parse(self,pattern):
        a=self.subparse (pattern)
        print(a)
        for i in range(len(a)):
            m=self.brackets(a[i][0][0])
            print(m)
            if(m!=0):
                a[i]=[self.parse(a[i][0][0]),a[i][1]]
        return a;
        
    





if __name__=="__main__":
    clearConsole()
    r=regularExpression()
    # print(r.parse("(ab)*|((a|ab)*b*(a|b)*)"))
    print(r.parse("(a|b)*aab*"))
    
    
# [[0, '(a~b)*|((a|a~b)*~b*~(a|b)*)', 1],
# [2, '(a~b)*', 3],
# [4, '(a|a~b)*~b*~(a|b)*', 5],
# [6, 'a~b', 7], 
# [8, '(a|a~b)*', 9],
# [10, 'b*', 11],
# [12, '(a|b)*', 13],
# [14, 'a', 15], 
# [16, 'b', 17], 
# [18, 'a|a~b', 19],
# [20, 'b', 21], 
# [22, 'a|b', 23], 
# [24, 'a', 25], 
# [26, 'b', 27]]
