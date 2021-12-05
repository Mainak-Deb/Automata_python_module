from io import BufferedIOBase
from dfa import DFA
from nfa import NFA
from regularExpression import regularExpression
import os



class lexical_analyzer:
    __regex_queue=[]
    __operation_queue=[]
    __filename=""
    __pattern=""
    __code=""
    __changes=[]
    __tokens=[]
    __yylex=[] #the real return 2-D array


    def __init__(self,filename):
        self.__filename=filename
        f = open(filename, "r")
        self.__pattern=f.read()
        pass

    def parse_variable():
        #used to parse the change variables starts with $ sign
        pass

    def parse_token(self,s):
        token_def=[]
        start=0;end=0
        for i in range(len(s)):
            if(s[i]=="<"):
                start=i;break
        for i in range(len(s)-1,-1,-1):
            if(s[i]==">"):
                end=i;break
        brack_unde=s[start+1:end]
        token_def=brack_unde.split(",")
        print(token_def)
        for i in range(len(token_def)):
            token_def[i]=token_def[i].strip()
        print(token_def)
        return token_def




    def parse(self,filename):
        print(self.__pattern)
        line_arr=self.__pattern.split("\n")

        # print(line_arr)
        f=open(filename)
        self.__code=f.read()

        # print(self.__code)
        self.__changes=[]
        self.__tokens=[]


        for i in line_arr:
            if((len(i)>=2) and (i[0]=="<")):
                self.__tokens.append(self.parse_token(i))
            pass

        print(self.__tokens)

        self.generate_token()

    def generate_token(self):
        regex=[]
        for i in self.__tokens:
            r=regularExpression(i[1])
            regex.append([i[0],r])
        print(regex)

        parser=""
        pointer=0

        while(pointer<len(self.__code)):
            i=0;irun=True
            while((irun) and (i<len(regex))):
                check_string=""
                jrun=True
                j=pointer
                while((jrun) and (j<len(self.__code))):
                    check_string+=self.__code[j]
                    print(check_string,regex[i][1].examine(check_string))
                    if(regex[i][1].examine(check_string)):
                        jrun=False
                        irun=False
                        pointer=j+1
                        self.__yylex.append([regex[i][0],check_string])
                        break
                    j+=1
                i+=1






        # while(pointer<len(self.__code)):
        #     for i in regex:
        #         check_string=""
        #         stop=False
        #         for j in range(pointer,len(self.__code)):
        #             check_string+=self.__code[j]
        #             print(check_string,i[1].examine(check_string))
        #             if(i[1].examine(check_string)):
        #                 stop=True
        #                 pointer=j+1
        #                 self.__yylex.append([i[0],check_string])
        #                 break
        #         if(stop):break
        #     break
        print(self.__yylex)
                        
                


        







if __name__=="__main__":
    l=lexical_analyzer("lex.l")
    l.parse("index.txt ")
