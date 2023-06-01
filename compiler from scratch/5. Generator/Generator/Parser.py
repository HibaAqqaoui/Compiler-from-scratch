import Lexer
from treelib import Node, Tree

Operators = ['ADD_OP', 'SUB_OP', 'DIV_OP', 'MULT_OP', 'MOD_OP']
Conditional_Operators = ['EQL_OP', 'NEQL_OP', 'BTOE_OP', 'LTOE_OP', 'BT_OP', 'LT_OP']
Data_types=['INT_RES', 'BOOL_RES', 'CHAR_RES','CTCHAR_RES']
CST = Tree()
AST = Tree()
stack = []

#this list will contain all the called functions
func_call_check = []
#this list will contain all the defined functions
func_defined =[]



assignInd = 0
idInd = 0
exprInd = 0
iniInd = 0
loopInd = 0
condInd = 0
predefInd = 0
procedureInd = 0

Symbol_Table= []

# For <Code>:
def Code():
    global iniInd, idInd, procedureInd, scopeInd
    # Adding the roots of the concrete and abstract syntax trees
    CST.create_node("Program", "root")
    AST.create_node("Program", "root")
    i=0
    # Executing the Lexer
    Lexer.main()
    # Define Global Variables: { < type_def >  S_COLON}  
    if  canIncrement(i) and Lexer.stream_of_tokens[i+1]!='MAIN_RES':
        while canIncrement(i+2) and Lexer.stream_of_tokens[i] in Data_types  and Lexer.stream_of_tokens[i+1]=='ID':
            if Lexer.stream_of_tokens[i+2]== 'S_COLON':
                # Adding the initialize statement to the concrete syntax tree
                CST.create_node("initialize", ("ini"+str(iniInd)), parent="root")
                CST.create_node(Lexer.stream_of_tokens[i], parent=("ini"+str(iniInd)))
                CST.create_node(Lexer.stream_of_tokens[i+1], ("id" + str(idInd)) ,parent=("ini"+str(iniInd)))
                CST.create_node(Lexer.string_lexeme[i+1], parent=("id" + str(idInd)))
                # Adding the initialize statement to the abstract syntax tree
                AST.create_node(Lexer.stream_of_tokens[i], ("ini"+str(iniInd+1)), parent="root")
                AST.create_node(Lexer.string_lexeme[i+1], parent=("ini"+str(iniInd+1)))
                # Checking if a variable has already been declared prior to reaching the current statement
                if not inSymbolTable(Lexer.string_lexeme[i+1]):
                    Symbol_Table.append([Lexer.string_lexeme[i+1],Lexer.stream_of_tokens[i],"global"])
                else:
                    print(Lexer.string_lexeme[i+1], "has already been declared")
                    exit()
                iniInd+=2
                idInd+=1
                i=i+2
                print("-------------- Global Variable Defined ---------- ")
            else:
                display_error(i+2,1)
            i=i+1
        if Lexer.stream_of_tokens[i] not in Data_types:
            display_error(i,1)
        elif canIncrement(i) and Lexer.stream_of_tokens[i+1]!='ID' and Lexer.stream_of_tokens[i+1]!='MAIN_RES':
            display_error(i+1,1)
    #Define Main Function <Main>
    if Lexer.stream_of_tokens[i]== 'INT_RES' and canIncrement(i) and Lexer.stream_of_tokens[i+1]=='MAIN_RES':
        i=main(i+2)+1
        idInd+=1
        if i< len(Lexer.stream_of_tokens) and canIncrement(i+2):
            # For {< type_def >  <arg> <function> ) } :
            while canIncrement(i+2) and (Lexer.stream_of_tokens[i] in Data_types or Lexer.stream_of_tokens[i]=='VOID_RES' ) and Lexer.stream_of_tokens[i+1]=='ID':
                # Adding the main function to the concrete syntax tree
                CST.create_node("procedure", ("procedure" + str(procedureInd)) ,parent="root")
                CST.create_node(Lexer.string_lexeme[i+1], ("id" + str(idInd)), parent= ("procedure" + str(procedureInd)))
                # Adding the main function to the abstract syntax tree
                AST.create_node(Lexer.string_lexeme[i+1], ("procedure" + str(procedureInd+1)) ,parent="root")
                
                if Lexer.stream_of_tokens[i+2]== 'L_PAREN':
                    i= parse_arg(i+3,("id" + str(idInd)), ("procedure" + str(procedureInd+1)),Lexer.string_lexeme[i+1])
                else:
                    display_error(i+2,1)
                idInd+=1
                procedureInd+=2
                scopeInd+=1
                i=i+1   
        else:
            if canIncrement(i+1)== True:
                display_error(i+2,2)
            elif canIncrement(i)== True:
                display_error(i+1,2)
            elif canIncrement(i-1)== True:
                display_error(i,2)

        print("\n************** Acceptor Message: Correct! *******\n")

    else:
        print("Main Function Unfound")

    call_functions_check()
    print('\n',"**************** Concrete Syntax Tree **************")
    CST.show(key=False)
    print("*************** Abstract Syntaxt Tree **************")
    AST.show(key=False)


# To call Predefined functions:    
def predef_functions(i,prnt,prnt2):
    global predefInd,idInd
    idInd+=1
    predefInd+=1
    # Adding the predefined function to the concrete syntax tree
    CST.create_node("predefined function", ("predef" + str(predefInd)), parent=prnt)
    CST.create_node(Lexer.stream_of_tokens[i-1], ("id" + str(idInd)),parent=("predef" + str(predefInd)))
    CST.create_node(Lexer.string_lexeme[i-1], parent=("id" + str(idInd)))
    # Adding the predefined function to the abstract syntax tree
    AST.create_node(Lexer.string_lexeme[i-1], ("predef" + str(predefInd+1)), parent=prnt2)
    if canIncrement(i+1) and Lexer.stream_of_tokens[i]== 'L_PAREN' and (Lexer.stream_of_tokens[i-1]=='PRINT_RES' or Lexer.stream_of_tokens[i-1]=='READ_RES'):
        if Lexer.stream_of_tokens[i-1] == 'PRINT_RES':
            AST[("predef" + str(predefInd+1))].tag = 'PRINT_RES'
        else:
            AST[("predef" + str(predefInd+1))].tag = 'READ_RES'
        i=i+1
        CST.create_node("L_PAREN",parent=("predef" + str(predefInd)))
        AST.create_node("L_PAREN",parent=("predef" + str(predefInd+1)))
        
        if Lexer.stream_of_tokens[i]=='ID':
            idInd+=1
            CST.create_node(Lexer.stream_of_tokens[i],("id" + str(idInd)) ,parent=("predef" + str(predefInd)))
            CST.create_node(Lexer.string_lexeme[i], parent= ("id" + str(idInd)))
            AST.create_node(Lexer.string_lexeme[i], parent=("predef" + str(predefInd+1)))
            if canIncrement(i+1) and Lexer.stream_of_tokens[i+1]=='R_PAREN' and Lexer.stream_of_tokens[i+2]=='S_COLON':
                CST.create_node("R_PAREN",parent=("predef" + str(predefInd)))
                AST.create_node("R_PAREN",parent=("predef" + str(predefInd+1)))
                return i+2
            else:
                if canIncrement(i)== False:
                    display_error(i,2)
                elif Lexer.stream_of_tokens[i+1]!='R_PAREN':
                    display_error(i+1,1)
                elif canIncrement(i+1)== False:
                    display_error(i+1,2)
                elif Lexer.stream_of_tokens[i+2]!='S_COLON':
                    display_error(i+2,1)
        else:
            display_error(i,1)
    elif canIncrement(i+1) and Lexer.stream_of_tokens[i]== 'L_PAREN' and Lexer.stream_of_tokens[i+1]== 'R_PAREN' and Lexer.stream_of_tokens[i+2]== 'S_COLON':
        CST.create_node("L_PAREN",parent=("predef" + str(predefInd)))
        CST.create_node("R_PAREN", parent=("predef" + str(predefInd)))
        AST.create_node("L_PAREN",parent=("predef" + str(predefInd+1)))
        AST.create_node("R_PAREN", parent=("predef" + str(predefInd+1)))
        predefInd+=2
        idInd+=1
        return i+2  
    elif canIncrement(i+1)== False: 
        display_error(i,2)
    else:
        if Lexer.stream_of_tokens[i]!= 'L_PAREN':
            display_error(i,1)
        elif Lexer.stream_of_tokens[i+1]!= 'R_PAREN':
            display_error(i+1,1)
        else:
           display_error(i+2,1) 

# for  <arg>: 
def parse_arg(i,prnt,prnt2,id):
    global func_defined
    index=0
    if  Lexer.stream_of_tokens [i] in Data_types and canIncrement(i):
        while canIncrement(i) and Lexer.stream_of_tokens [i]!='R_PAREN':
            if canIncrement(i+1) and Lexer.stream_of_tokens [i] in Data_types and Lexer.stream_of_tokens [i+1] =='ID':
                
                Symbol_Table.append([Lexer.string_lexeme[i+1],Lexer.stream_of_tokens[i],("scope"+str(scopeInd))])
                
                index+=1 
                if Lexer.stream_of_tokens [i+2]== 'COLON':
                    i=i+3
                elif Lexer.stream_of_tokens [i+2]== 'R_PAREN':
                    i=i+2
                    func_defined.append([index,id])
                    break
                else:# if other character used
                    
                    if Lexer.stream_of_tokens [i] not in Data_types:
                        display_error(i,1)
                    elif Lexer.stream_of_tokens [i+1] !='ID':
                        display_error(i+1,1)
                    else:
                        i=i+2 
                        
                        break    
            else:
                if Lexer.stream_of_tokens [i] not in Data_types:# no data type declared 
                    display_error(i,1)
                elif canIncrement(i)== False:
                    display_error(i,2)
                elif Lexer.stream_of_tokens [i+1] !='ID': #no id used   
                    display_error(i+1,1)
                elif canIncrement(i+1) ==False:
                    display_error(i+1,2)
                elif canIncrement(i+2) ==False: #no following characters
                    display_error(i+2,2)
                else:
                    display_error(i,2)#no following characters
        if canIncrement(i) and Lexer.stream_of_tokens [i]=='R_PAREN'and Lexer.stream_of_tokens [i-1]=='ID' and Lexer.stream_of_tokens [i+1]=='LCBRK':
            i=i+2
            while i<len(Lexer.stream_of_tokens) and Lexer.stream_of_tokens[i]!='RCBRK':
                    i= statement_type(i,prnt,prnt2)
                    i=i+1
            if canIncrement(i-1):
                if Lexer.stream_of_tokens[i]=='RCBRK':
                    print("-------------- Function Defined -----------------")
                    return i
                else:
                    if Lexer.stream_of_tokens[i]!='RCBRK':
                        display_error(i,1)
                    elif canIncrement(i)== False:
                        display_error(i,2)
            else:
                display_error(i-1,2)  
        else:
            if Lexer.stream_of_tokens [i]!='R_PAREN':
                display_error(i,1)
            # ex: int func(int a, ){
            elif Lexer.stream_of_tokens [i]=='R_PAREN' and Lexer.stream_of_tokens [i-1]!='ID' :
                display_error(i-1,2)
            elif canIncrement(i-1)== False or Lexer.stream_of_tokens [i]!='R_PAREN':
                if canIncrement(i-1)== False:
                    display_error(i-1,2)
                else:
                   display_error(i,1) 
            elif Lexer.stream_of_tokens [i-1]!='ID':
                display_error(i-1,1)
            elif canIncrement(i)== False or Lexer.stream_of_tokens [i+1]!='LCBRK' :
                display_error(i,2)
            else:
                display_error(i,1)
    elif Lexer.stream_of_tokens [i]=='VOID_RES':
        if canIncrement(i+2):
            if Lexer.stream_of_tokens [i+1]=='R_PAREN' and Lexer.stream_of_tokens [i+2]== 'LCBRK': 
                i=i+3
                while i<len(Lexer.stream_of_tokens) and Lexer.stream_of_tokens[i]!='RCBRK':
                    i= statement_type(i,prnt,prnt2)
                    i=i+1
                if canIncrement(i-1):
                    if Lexer.stream_of_tokens[i]=='RCBRK':
                        func_defined.append([index,id])
                        print("-------------- Function Defined -----------------")
                        return i
                    else:
                        if Lexer.stream_of_tokens[i]!='RCBRK':
                            display_error(i,1)
                        elif canIncrement(i)== False:
                            display_error(i,2)
                else:
                    display_error(i-1,2)   
            else:
                if Lexer.stream_of_tokens [i+1]!='L_PAREN':
                    display_error(i+1,1)
                else:
                    display_error(i+2,1) 
        else:
            if canIncrement(i) and Lexer.stream_of_tokens [i+1]!='R_PAREN':
                display_error(i+1,1)
            elif canIncrement(i+1) and Lexer.stream_of_tokens [i+2]!= 'LCBRK':
                display_error(i+2,1)
            elif canIncrement(i)==False:
                display_error(i,2)
            elif canIncrement(i+1)==False:
                display_error(i+1,2)
            elif canIncrement(i+2)==False:
                display_error(i+2,2)
    else:
        if  Lexer.stream_of_tokens [i] not in Data_types:
            display_error(i,1)
        elif canIncrement(i)== False:
            display_error(i,2)


#def canIncrement(i) to check if 'i' is out of bounds
def canIncrement(i):
    if i+1<len(Lexer.stream_of_tokens):
        return True
    else:
        return False

# Function to check the different types of statements in the code
def statement_type(i, prnt, prnt2):
    global assignInd, idInd, exprInd
    idInd+=1
    #each call returns the last element before moving on need to check  if can increment i or not
    if canIncrement(i):
        # for initialization
        if Lexer.stream_of_tokens[i] in Data_types:
            i= initialization(i+1,prnt,prnt2)
        # for assignment
        elif Lexer.stream_of_tokens[i] == 'SET_RES':
            if canIncrement(i+2) and Lexer.stream_of_tokens[i+1]=='ID' and  Lexer.stream_of_tokens[i+2]=='ASSIGN_OP':
                idInd+=1
                CST.create_node("assign", ("assign" + str(assignInd)) , parent= prnt)
                CST.create_node("SET_RES", parent= ("assign" + str(assignInd)))
                AST.create_node("SET_RES", ("assign" + str(assignInd+1)),parent=prnt2)
                CST.create_node(Lexer.stream_of_tokens[i+1], ("id" + str(idInd)), parent= ("assign" + str(assignInd)))
                CST.create_node(Lexer.string_lexeme[i+1], parent=("id" + str(idInd)))
                AST.create_node(Lexer.string_lexeme[i+1], parent=("assign" + str(assignInd+1)))
                CST.create_node("EQL_OP", parent= ("assign" + str(assignInd)))
                AST.create_node("EQL_OP", parent= ("assign" + str(assignInd+1)))
                CST.create_node("Expression",("expression" + str(exprInd)),parent = ("assign" + str(assignInd)))
                idInd+=1
                i = assignment(i+3,("expression" + str(exprInd)), ("assign" + str(assignInd+1)))
                assignInd+=2
                exprInd+=1
            else:
                if Lexer.stream_of_tokens[i+1]!='ID':
                    display_error(i,2)
                elif Lexer.stream_of_tokens[i+2]!='ASSIGN_OP':
                    display_error(i+1,2)
                else:
                    display_error(i+2,2)
        # conditional statements
        elif Lexer.stream_of_tokens[i] == 'IF_RES':
            i=conditional_stat(i+1,prnt,prnt2)
        # loop
        elif Lexer.stream_of_tokens[i] == 'WHILE_RES':
            i = loop(i+1,prnt)
        # function call
        elif Lexer.stream_of_tokens[i] == 'ID':
            i=function_call(i+1,prnt,prnt2,Lexer.string_lexeme[i])
        # call predefined functions/ these functions returns nothing
        elif Lexer.stream_of_tokens[i] == 'GOU_RES' or Lexer.stream_of_tokens[i] == 'GOU_RES' or Lexer.stream_of_tokens[i] =='GOD_RES' or Lexer.stream_of_tokens[i] == 'GOL_RES' or Lexer.stream_of_tokens[i] =='GOR_RES'or Lexer.stream_of_tokens[i] == 'PICKF_RES'or Lexer.stream_of_tokens[i] == 'PRINT_RES' or Lexer.stream_of_tokens[i]=='READ_RES':
            i=predef_functions(i+1,prnt,prnt2)
        # back statement
        elif Lexer.stream_of_tokens[i] == 'BACK_RES':
            i=back(i+1,prnt,prnt2)
        # Unexpected statement
        else:
            display_error(i,1)
        return i
    # incomplete code
    else: 
        display_error(i,2)

strInd = 0
backInd = 0

# For <Back>:
def back(i,prnt,prnt2):
    global backInd, idInd
    CST.create_node(Lexer.stream_of_tokens[i-1], ("back" + str(backInd)), parent = prnt)
    AST.create_node(Lexer.stream_of_tokens[i-1], ("back" + str(backInd+1)), parent= prnt2)
    if (Lexer.stream_of_tokens[i]=='ID' or Lexer.stream_of_tokens[i] == 'INT_LIT' ) and canIncrement(i) and Lexer.stream_of_tokens[i+1]=='S_COLON':
        if Lexer.stream_of_tokens[i]=='ID':
            if not inSymbolTable([Lexer.string_lexeme[i]]):
                print(Lexer.string_lexeme[i], "not defined in this scope")
                exit()
        CST.create_node(Lexer.stream_of_tokens[i], ("id" + str(idInd)), parent= ("back" + str(backInd)))
        CST.create_node(Lexer.string_lexeme[i], parent=("id" + str(idInd)))
        AST.create_node(Lexer.string_lexeme[i], parent=("back" + str(backInd+1)))

        idInd+=1
        backInd+=2
        print("-------------- Return Statement -----------------")
        return i+1
    else:
        if Lexer.stream_of_tokens[i]!='ID' and Lexer.stream_of_tokens[i]!= 'INT_LIT':
            display_error(i,1) 
        else:
            display_error(i,2)

# A function to get the type of a variable from the Symbol Table
def getType(x):
    global scopeInd
    for list in Symbol_Table:
        if list[0] == x and (list[2] == "global" or list[2] == ("scope"+str(scopeInd))):
            return list[1]

# A function to get the scope of a variable from the Symbol Table
def getScope(x):
    global scopeInd
    for list in Symbol_Table:
        if list[0] == x:
            return list[2]

#  A function to check the assignment statement
def assignment(i, prnt,prnt2):
    global strInd,idInd
    idInd+=1
    if Lexer.stream_of_tokens[i] == 'Q_MARKS':

        if Lexer.stream_of_tokens[i-2] == 'ID':
            if not inSymbolTable([Lexer.string_lexeme[i-2]]):
                print(Lexer.string_lexeme[i-2], "not defined in this scope")
                exit()

        if getType(Lexer.string_lexeme[i-2]) != 'CTCHAR_RES':
            print((Lexer.string_lexeme[i-2]), " is not of type const char ")
            exit()
        s = ''
        CST.create_node("Q_MARKS",parent=prnt)
        AST.create_node("Q_MARKS",parent=prnt2)
        if canIncrement(i):
            i+=1
            if Lexer.string_lexeme[i] == ';':
                display_error(i-1,2)
            if Lexer.stream_of_tokens[i] == 'STR_LIT':
                CST.create_node("STR_LIT", ("str" + str(strInd)),parent=prnt)
            while Lexer.stream_of_tokens[i] != 'Q_MARKS':
                s=s + Lexer.string_lexeme[i] + ' '
                if canIncrement(i):
                    i+=1
                else:
                    display_error(i,1)
            if CST.contains(("str" + str(strInd))):
                CST.create_node(s, parent=("str" + str(strInd)))
                AST.create_node(s, parent=prnt2)
            if Lexer.stream_of_tokens[i] == 'Q_MARKS':
                CST.create_node("Q_MARKS",parent=prnt)
                AST.create_node("Q_MARKS",parent=prnt2)
                if canIncrement(i):
                    i+=1
                    if Lexer.stream_of_tokens[i] != 'S_COLON':
                        display_error(i,1)
                else:
                    display_error(i,2)
            strInd+=2
        else:
            display_error(i,2)
    
    elif Lexer.stream_of_tokens[i] == 'ID' or Lexer.stream_of_tokens[i] == 'INT_LIT':
        if Lexer.stream_of_tokens[i-2] == 'ID':
            if not inSymbolTable([Lexer.string_lexeme[i-2]]):
                print(Lexer.string_lexeme[i-2], "not defined in this scope")
                exit()

        if getType(Lexer.string_lexeme[i-2]) != 'INT_RES':
            print((Lexer.string_lexeme[i-2]), "is not of type int")
            exit()
        
        if Lexer.stream_of_tokens[i] == 'ID' and canIncrement(i) and Lexer.stream_of_tokens[i+1] != 'L_PAREN':
            if not inSymbolTable([Lexer.string_lexeme[i]]):
                print(Lexer.string_lexeme[i], "not defined in this scope")
                exit()
        if canIncrement(i):
            if Lexer.stream_of_tokens[i+1] == 'S_COLON':
                CST.create_node(Lexer.stream_of_tokens[i], ("id" + str(idInd)) , parent = prnt)
                CST.create_node(Lexer.string_lexeme[i], parent= ("id" + str(idInd)))
                AST.create_node(Lexer.string_lexeme[i], parent= prnt2)
                idInd+=1
                print("-------------- Assignment Done ------------------")
                return i+1
            elif Lexer.stream_of_tokens[i+1] == 'L_PAREN':
                i = function_call(i+1,prnt,prnt2,Lexer.string_lexeme[i])
            elif Lexer.stream_of_tokens[i+1] in Operators:
                CST.create_node(Lexer.stream_of_tokens[i], ("id" + str(idInd)) , parent = prnt)
                CST.create_node(Lexer.string_lexeme[i], parent= ("id" + str(idInd)))
                AST.create_node(Lexer.string_lexeme[i], parent= prnt2)
                idInd+=1
                CST.create_node(Lexer.stream_of_tokens[i+1], parent= prnt)
                AST.create_node(Lexer.stream_of_tokens[i+1], parent= prnt2)
                if canIncrement(i+1):
                    if Lexer.stream_of_tokens[i+2] == 'ID' or Lexer.stream_of_tokens[i+2] == 'INT_LIT':
                        
                        if Lexer.stream_of_tokens[i+2] == 'ID':
                            if not inSymbolTable([Lexer.string_lexeme[i+2]]):
                                print(Lexer.string_lexeme[i], "not defined in this scope")
                                exit()

                        CST.create_node(Lexer.stream_of_tokens[i+2], ("id" + str(idInd)) , parent = prnt)
                        CST.create_node(Lexer.string_lexeme[i+2], parent= ("id" + str(idInd)))
                        AST.create_node(Lexer.string_lexeme[i+2], parent= prnt2)
                        idInd+=1
                        if canIncrement(i+2):
                            if Lexer.stream_of_tokens[i+3] == 'S_COLON':
                                print("-------------- Assignment Done ------------------")
                                return i+3
                            else:
                                display_error(i+3,1)
                        else:
                            display_error(i+2,2)
                    else:
                        display_error(i+2,1)
                else:
                    
                    display_error(i+1,2)
            else:
                display_error(i+1,1)
        else:
            display_error(i,2)
    else:
       
        display_error(i,1)
    
    print("-------------- Assignment Done ------------------")
    return i


# A function to check if a variable is in the symbol table
def inSymbolTable(l):
    global scopeInd
    L = []
    for element in l:
        L.append(element)
    for list in Symbol_Table:
        if L[0] == list[0]:
            return True
    return False

# A function to check the condition in a loop statement or conditional statement and give errors if the condition is not correct
def condition(i,prnt,prnt2):
    # a + c < b & condition
        global condInd, idInd
        idInd+=1
        CST.create_node("condition", ("cond" + str(condInd)), prnt)
        if Lexer.stream_of_tokens[i] == 'ID' or Lexer.stream_of_tokens[i] == 'INT_LIT':
            CST.create_node("L_PAREN", parent=("cond" + str(condInd)))
            AST.create_node("L_PAREN",parent=prnt2)
            CST.create_node(Lexer.stream_of_tokens[i], ("id" + str(idInd)) , parent=("cond" + str(condInd)))
            CST.create_node(Lexer.string_lexeme[i], parent=("id" + str(idInd)))
            AST.create_node(Lexer.string_lexeme[i], parent=prnt2)

            if Lexer.stream_of_tokens[i] == 'ID':
                if not inSymbolTable([Lexer.string_lexeme[i]]):
                    print(Lexer.string_lexeme[i], "not defined in this scope")
                    exit()
            idInd+=1
            goodCond = True
            while i < len(Lexer.stream_of_tokens):
                i+=1
                if Lexer.stream_of_tokens[i] == 'R_PAREN':
                    if goodCond:
                        CST.create_node("R_PAREN", parent=("cond" + str(condInd)))
                        AST.create_node("R_PAREN", parent= prnt2)
                        condInd+=1
                        return i
                    else:
                        display_error(i,1)
                elif Lexer.stream_of_tokens[i] == 'ID' or Lexer.stream_of_tokens[i] == 'INT_LIT':
                    if goodCond:
                        display_error(i,1)
                    else:
                        if Lexer.stream_of_tokens[i] == 'ID':
                            if not inSymbolTable([Lexer.string_lexeme[i]]):
                                print(Lexer.string_lexeme[i], "not defined in this scope")
                                exit()
                        goodCond = True
                        CST.create_node(Lexer.stream_of_tokens[i], ("id" + str(idInd)) , parent=("cond" + str(condInd)))
                        CST.create_node(Lexer.string_lexeme[i], parent=("id" + str(idInd)))
                        AST.create_node(Lexer.string_lexeme[i], parent= prnt2)
                        idInd+=1
                elif Lexer.stream_of_tokens[i] in Operators or Lexer.stream_of_tokens[i] in Conditional_Operators:
                    if goodCond:
                        goodCond = False
                        CST.create_node(Lexer.stream_of_tokens[i] , parent=("cond" + str(condInd)))
                        AST.create_node(Lexer.stream_of_tokens[i], parent=prnt2)
                    else:
                        display_error(i,1)
                else:
                    display_error(i,1)
        else:
            display_error(i,1)     

# A function to check the loop statement and give errors if the statement is not correct
def loop(i,prnt):
    # WHILE (cond)
    #BEGIN
    #statements
    #END;
    global loopInd

    CST.create_node("loop", ("loop" + str(loopInd)) ,parent=prnt)
    CST.create_node("WHILE_RES",parent=("loop" + str(loopInd)))
    AST.create_node("WHILE_RES", ("loop" + str(loopInd+1)),prnt)
    if Lexer.stream_of_tokens[i] == 'L_PAREN':
        i = condition(i+1, ("loop" + str(loopInd)),("loop" + str(loopInd+1))) + 1
        #add condition to tree
        if Lexer.stream_of_tokens[i] == 'BEGIN_RES':
            CST.create_node("BEGIN_RES",parent=("loop" + str(loopInd)))
            AST.create_node("BEGIN_RES",parent=("loop" + str(loopInd+1)))
            i+=1
            #handle statements
            while(Lexer.stream_of_tokens[i] != 'END_RES'):
                if i == len(Lexer.stream_of_tokens) - 1:
                    display_error(i,1)
                i = statement_type(i,("loop" + str(loopInd)), ("loop" + str(loopInd+1)))
                if canIncrement(i):
                    i+=1
                else:
                    display_error(i, 2)
            #check if lexer.sot[i] == 'END_RES' and lexer.sor[i+1] == 'S_COLON'
            if canIncrement(i):
                if Lexer.stream_of_tokens[i+1] != 'S_COLON':
                    display_error(i,1)
                else:
                    CST.create_node("END_RES",parent=("loop" + str(loopInd)))
                    AST.create_node("END_RES",parent=("loop" + str(loopInd+1)))
                    loopInd+=2
                    print("-------------- While Loop -----------------------")
                    return i+1

            else:
                display_error(i,2)
        else:
            display_error(i,1)
    else:
        display_error(i,1)
    


scopeInd = 0

# A function to check the intialization statements and give errors if the statement is not correct
def initialization(i,prnt,prnt2):
    global iniInd, idInd, scopeInd
    if Lexer.stream_of_tokens[i]=='ID' and canIncrement(i) and Lexer.stream_of_tokens[i+1]=='S_COLON':
        idInd+=1
        CST.create_node("initialize", ("ini"+str(iniInd)),parent=prnt)
        CST.create_node(Lexer.stream_of_tokens[i-1],parent=("ini"+str(iniInd)))
        AST.create_node(Lexer.stream_of_tokens[i-1],("ini"+str(iniInd+1)),parent=prnt2)
        CST.create_node(Lexer.stream_of_tokens[i], ("id" + str(idInd)),parent=("ini"+str(iniInd)))
        CST.create_node(Lexer.string_lexeme[i], parent=("id" + str(idInd)))
        AST.create_node(Lexer.string_lexeme[i], parent=("ini"+str(iniInd+1)))
        if not inSymbolTable(Lexer.string_lexeme[i]):
            Symbol_Table.append([Lexer.string_lexeme[i],Lexer.stream_of_tokens[i-1],("scope"+str(scopeInd))])
        else:
            if getScope(Lexer.string_lexeme[i]) == ("scope" + str(scopeInd)):
                print(Lexer.string_lexeme[i], "has already been declared")
                exit()
            else:
                Symbol_Table.append([Lexer.string_lexeme[i],Lexer.stream_of_tokens[i-1],("scope"+str(scopeInd))])
        #AST.create_node(Lexer.stream_of_tokens[i-1],("ini"+str(iniInd+1)),parent=)
        #AST.create_node(Lexer.string_lexeme[i], parent=("ini"+str(iniInd+1)))
        idInd+=1
        iniInd+=2

        print("-------------- Initialization Done --------------") 
        return i+1
    else:
        if Lexer.stream_of_tokens[i]!='ID':
            display_error(i,1) 
        else:
            display_error(i,2) 

condstatInd = 0

# A function to check conditional statements and give errors if the statement is not correct
def conditional_stat(i,prnt,prnt2):
    global condstatInd
    #If Statement Implementation
    CST.create_node("conditional statement", (("condstat") + str(condstatInd)) , parent=prnt)
    CST.create_node(Lexer.stream_of_tokens[i-1],(("condstat") + str(condstatInd+1)), parent = (("condstat") + str(condstatInd)))
    AST.create_node(Lexer.stream_of_tokens[i-1],(("condstat") + str(condstatInd+2)), parent = prnt2)
    if canIncrement(i) and Lexer.stream_of_tokens[i]=='L_PAREN':

        i=i+1
        i=condition(i,(("condstat") + str(condstatInd+1)),(("condstat") + str(condstatInd+2)))
        if Lexer.stream_of_tokens[i] =='R_PAREN':
            if canIncrement(i):
                i=i+1 
                if Lexer.stream_of_tokens[i]=='LSQR':
                    i=i+1
                    while canIncrement(i) and Lexer.stream_of_tokens[i] !='RSQR':
                        i=statement_type(i,(("condstat") + str(condstatInd+1)),(("condstat") + str(condstatInd+2)))
                        i=i+1
                    if canIncrement(i-1):
                        if Lexer.stream_of_tokens[i]=='RSQR':
                            s = 1
                            print("-------------- If Statement ---------------------")
                        else:
                            if Lexer.stream_of_tokens[i]!='RSQR':
                                
                                display_error(i,1)
                            elif canIncrement(i)== False:
                                
                                display_error(i,2)
                    else:
                        display_error(i-1,2)   
                else:
                    display_error(i,1)
            else:
                display_error(i,2)
        else:
            if canIncrement(i-1) == False:
                display_error(i-1,2)
            elif Lexer.stream_of_tokens[i] !='R_PAREN':
                display_error(i,1)
    else:
        if Lexer.stream_of_tokens[i]!='L_PAREN':
            display_error(i,1)
        elif canIncrement(i)==False:
            display_error(i,2)
    #Else Statement Implementation
    condstatInd+=3
    i+=1
    if Lexer.stream_of_tokens[i]!='RCBRK':
        
        if canIncrement(i) and Lexer.stream_of_tokens[i]=='ELSE_RES':
            # Adding the conditional statement to the concrete syntax tree
            CST.create_node("conditional statement", (("condstat") + str(condstatInd)) , parent=prnt)
            CST.create_node(Lexer.stream_of_tokens[i],(("condstat") + str(condstatInd+1)), parent = (("condstat") + str(condstatInd)))
            # Adding the conditional statement to the abstract syntax tree
            AST.create_node(Lexer.stream_of_tokens[i],(("condstat") + str(condstatInd+2)), parent = prnt2)

            i=i+1
            if Lexer.stream_of_tokens[i]=='LSQR':
                i=i+1
                while canIncrement(i) and Lexer.stream_of_tokens[i] !='RSQR':
                    i=statement_type(i,(("condstat") + str(condstatInd+1)),(("condstat") + str(condstatInd+2)))
                    i=i+1
                if canIncrement(i-1):
                    if Lexer.stream_of_tokens[i]=='RSQR':
                        print("-------------- Else Statement -------------------")
                        return i
                    else:
                        if Lexer.stream_of_tokens[i]!='RSQR':            
                            display_error(i,1)
                        elif canIncrement(i)== False:            
                            display_error(i,2)
                        else:
                            display_error(i-1,2)   
                else:
                        display_error(i,1)

        else:
            if canIncrement(i)== False:
                display_error(i,2)
            else:
                display_error(i+1,1)
    else:
        if canIncrement(i-1)== False:
            display_error(i-1,2)
        elif Lexer.stream_of_tokens[i]=='RCBRK':
            return i-1


funcInd = 0

# A function to check if a function call is correct or not
def function_call(i,prnt,prnt2,id):
    global func_call_check
    global funcInd,idInd
    idInd+=1
    index = 0
    if Lexer.stream_of_tokens[i]!='L_PAREN':
        display_error(i,1)
    # Adding the function call node to the concrete syntax tree
    CST.create_node("function call", ("func" + str(funcInd)), parent = prnt)
    CST.create_node(Lexer.stream_of_tokens[i-1], ("id"+str(idInd)) ,parent=("func" + str(funcInd)))
    CST.create_node(Lexer.string_lexeme[i-1],parent=("id"+str(idInd)))
    # Adding the function call node to the abstract  syntax tree
    AST.create_node(Lexer.string_lexeme[i-1],("func"+str(funcInd+1)),parent=prnt2)
    idInd+=2
    CST.create_node("L_PAREN", parent=("func" + str(funcInd)))
    AST.create_node("L_PAREN", parent=("func"+str(funcInd+1)))
    if canIncrement(i):
        i=i+1
    while canIncrement(i):
        # func (a, 2, c)
        #function call with passing argument(s)
        if Lexer.stream_of_tokens[i]=='ID' or Lexer.stream_of_tokens[i]== 'INT_LIT':
            CST.create_node(Lexer.stream_of_tokens[i], ("id"+str(idInd)) ,parent=("func" + str(funcInd)))
            CST.create_node(Lexer.string_lexeme[i],parent=("id"+str(idInd)))
            AST.create_node(Lexer.string_lexeme[i], parent=("func"+str(funcInd+1)))
            idInd+=1
            index+=1
            if canIncrement(i):
                i=i+1
                if Lexer.stream_of_tokens[i]=='COLON' and canIncrement(i) and (Lexer.stream_of_tokens[i+1]=='ID' or Lexer.stream_of_tokens[i+1]=='INT_LIT'):
                    # Adding the colon node in the concrete syntax tree
                    CST.create_node("COLON", parent=("func" + str(funcInd)))
                    # Adding the colon node in the abstract syntax tree
                    AST.create_node("COLON", parent=("func"+str(funcInd+1)))
                    i=i+1
                elif Lexer.stream_of_tokens[i] == 'R_PAREN':
                    # Adding the right parenthesis node in the concrete syntax tree
                    CST.create_node("R_PAREN", parent=("func" + str(funcInd)))
                    # Adding the right parenthesis node in the abstract syntax tree
                    AST.create_node("R_PAREN", parent=("func"+str(funcInd+1)))
                    break   
                else:
                    if Lexer.stream_of_tokens[i]!='COLON':
                        display_error(i,1)
                    elif Lexer.stream_of_tokens[i+1]!='ID' or Lexer.stream_of_tokens[i+1]!='INT_LIT':
                        display_error(i+1,1)
                    else:
                        display_error(i,1)
            else:
                break 
        #function call with no passing argument(s)
        elif Lexer.stream_of_tokens[i]=='R_PAREN':
            # Adding the right parenthesis node in the concrete syntax tree
            CST.create_node("R_PAREN", parent=("func" + str(funcInd)))
            # Adding the right parenthesis node in the abstract syntax tree
            AST.create_node("R_PAREN", parent=("func"+str(funcInd+1)))
            break
        else: 
            display_error(i,1)    
    if  Lexer.stream_of_tokens[i]!= 'R_PAREN' or Lexer.stream_of_tokens[i+1]!= 'S_COLON' :
        if Lexer.stream_of_tokens[i]!= 'R_PAREN':
            display_error(i,2)
        elif Lexer.stream_of_tokens[i+1]!= 'S_COLON' or canIncrement(i)== False: 
            if canIncrement(i)== False:
                display_error(i,2)
            else:
                display_error(i,2)
    elif canIncrement(i)== False:
        display_error(i,2)
    else:
        func_call_check.append([index,id])
        print("-------------- Function Called ------------------")
        funcInd+=2
        return i+1


# A function to check if the number of arguments in a function call match the number of arguments in the function's declaration 
def call_functions_check():
    for j in func_call_check:
        exist=False
        for v in func_defined:
            if j[1]==v[1]:
                if j[0]!=v[0]:
                    print("Error: Number of passed parameters of "+ j[1]+ " : "+ str(j[0])  +" is different than the number of arguments defined " + str(v[0]))
                    exit()
                else:
                    exist=True
        if exist == False:
            print("Error: Function "+j[1] +" is Not Defined")
            exit()


# A function to help display errors according to the type of error 
def display_error(i, type):
    if type ==1:
        print("Error: Unexpected lexeme "+Lexer.string_lexeme[i] +" in line "+ str(Lexer.line_counter[i]) + " After Lexeme " +Lexer.string_lexeme[i-1] )
    else:
        print("Error: Expected lexeme after "+Lexer.string_lexeme[i]+ " in line "+ str(Lexer.line_counter[i]))
    exit()


# A function to check if the main function exists and is well declared
def main(i):
        global scopeInd
        # Creating the main function node in the concrete syntax tree
        CST.create_node("main","main",parent="root")
        # Creating the main function node in the abstract syntax tree
        AST.create_node("main", "main", parent="root")
        if canIncrement(i+3):
            # check int main(void){
            
            if Lexer.stream_of_tokens[i]=='L_PAREN' and Lexer.stream_of_tokens[i+1]== 'VOID_RES'and Lexer.stream_of_tokens[i+2]=='R_PAREN' and Lexer.stream_of_tokens[i+3]=='LCBRK':
                i=i+4
                # to parse statements inside the main function
                while i<len(Lexer.stream_of_tokens) and Lexer.stream_of_tokens[i]!='RCBRK':
                    i= statement_type(i, "main","main")
                    i=i+1
                # check if the main curly brackets were closed or not   
                if canIncrement(i-1):
                    if Lexer.stream_of_tokens[i]=='RCBRK':
                        print("-------------- Main Defined ---------------------")
                        scopeInd+=1
                        return i
                    else:
                        if Lexer.stream_of_tokens[i]!='RCBRK':
                            display_error(i,1)
                        elif canIncrement(i)== False:
                            display_error(i,2)
                else:
                    if canIncrement(i-1)== False and Lexer.stream_of_tokens[i-1]!= 'RCBRK':
                        display_error(i-1,1)
                    else:
                        display_error(i-1,2)   
            else:
                if Lexer.stream_of_tokens[i]!='L_PAREN' or Lexer.stream_of_tokens[i+1]!= 'VOID_RES'or Lexer.stream_of_tokens[i+2]!='R_PAREN' or Lexer.stream_of_tokens[i+3]!='LCBRK':
                    if Lexer.stream_of_tokens[i]!='L_PAREN': 
                        display_error(i,1)
                    elif Lexer.stream_of_tokens[i+1]!= 'VOID_RES':
                        display_error(i+1,1)
                    elif Lexer.stream_of_tokens[i+2]!='R_PAREN':
                        display_error(i+2,1)
                    else:
                       display_error(i+2,2) 
        else:
            print("Invalid Main Definition")
            exit()
    



#To Launch the Program  
if __name__=='__main__':
    Code()