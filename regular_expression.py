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

    
    def parse(self,pattern):
        a=self.subparse (pattern)
        for i in range(len(a)):
            m=self.brackets(a[i][0][0])
            print(m)
            if(m!=0):
                a[i]=[self.parse(a[i][0][0]),a[i][1]]
        return a;
        
    





if __name__=="__main__":
    clearConsole()
    r=regularExpression()
    print(r.parse("(ab)*| ((a|ab)*b*(a|b)*)"))
    

