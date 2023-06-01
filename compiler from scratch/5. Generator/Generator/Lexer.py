# import module os and re to handle files 
import os
# global variable to store our line codes
line_counter =[] 
# global variable to increment our line code index
line= 1
# global variable to store our lexemes
string_lexeme = [] 
# global variable to store our lexemes
stream_of_tokens = []
# global variable to define our operators
operator =['+','-','/','%','=','and','or','*','<=','<','>=','>','!']
# global variable to define our punctuation signs
punctuation=[',',';','{','}','(',')','"', '[',']']
# global variable to define our reserved words
RES_WORDS = ['main', 'void', 'back', 'SET', 'IF', 'ELSE', 'WHILE', 'BEGIN', 'END', 'int', 'bool', 'char', 'GOUP','GODOWN','GOLEFT','GORIGHT', 'PICKFLOWER']
# global variable for our symbol table
symbol_table=[]
# global variable for our literal table
Literal_Table=[]
# A function to read from the file
def read_from_file():
    global line
    # if the file exists
    if os.path.exists(os.path.join(os.path.dirname(__file__),"file.txt")):
        # open the file
        input_file = open(os.path.join(os.path.dirname(__file__),'file.txt'), 'r')
        while True:
            for line_f in input_file:
                # reading word by word from the input file        
                for word in line_f.split():
                    #send lexemes to function process_lexeme to be further processed
                    process_lexeme(word)    
                line = line +1
            char = input_file.read(1)         
            # To mark the end of the File
            if not char:
                break
        # close the file
        input_file.close()
    #error message if the file does not exist
    else:
        print("\n************File Not Found !************\n")



def getToken(lexeme):
    global Invalid_lex
    # The function get_token returns the corresponding token_id
    #  and token name for a given lexeme
    if lexeme == "back":
        return [1,'BACK_RES']
    elif lexeme == "if":
        return [2, 'IF_RES']
    elif lexeme == "else":
        return [3, 'ELSE_RES']
    elif lexeme == "print":
        return [4, 'PRINT_RES']
    elif lexeme == "SET":
        return [5, 'SET_RES']
    elif lexeme == "WHILE":
        return [6, 'WHILE_RES']
    elif lexeme == "END":
        return [7, 'END_RES']
    elif lexeme == "main":
        return [8, 'MAIN_RES']
    elif lexeme == "void":
        return [9, 'VOID_RES']
    elif lexeme == "int":
        return [10, 'INT_RES']
    elif lexeme == "bool":
        return [11, 'BOOL_RES']
    elif lexeme == "char":
        return [12, 'CHAR_RES']
    elif lexeme == "ctchar":
        return [13, 'CTCHAR_RES']
    elif lexeme == "*":
        return [14, 'MULT_OP']
    elif lexeme == "+":
        return [15, 'ADD_OP']
    elif lexeme == "-":
        return [16, 'SUB_OP']
    elif lexeme == "/":
        return [17, 'DIV_OP']
    elif lexeme == "%":
        return [18, 'MOD_OP']
    elif lexeme == "==":
        return [19, 'EQL_OP']
    elif lexeme == '!=':
        return [20, 'NEQL_OP']
    elif lexeme == "=":
        return [21, 'ASSIGN_OP']
    elif lexeme == ">=":
        return [22, 'BTOE_OP']
    elif lexeme == "<=":
        return [23, 'LTOE_OP']
    elif lexeme == ">":
        return [24, 'BT_OP']
    elif lexeme == "<":
        return [25, 'LT_OP']
    elif lexeme == "read":
        return [4, 'READ_RES']
    elif lexeme == "(":
        return [28, 'L_PAREN']
    elif lexeme == ")":
        return [29, 'R_PAREN']
    elif lexeme == "[":
        return [30, 'LSQR']
    elif lexeme == "]":
        return [31, 'RSQR']
    elif lexeme == "{":
        return [32, 'LCBRK']
    elif lexeme == "}":
        return [33, 'RCBRK']
    elif lexeme == ";":
        return [34, 'S_COLON']
    elif lexeme.isnumeric():
        return [35, 'INT_LIT']
    elif lexeme == '"':
        return [36, 'Q_MARKS']
    elif lexeme == ",":
        return [37, 'COLON']
    elif lexeme == 'GOUP':
        return [38, 'GOU_RES']
    elif lexeme == 'GODOWN':
        return [39, "GOD_RES"]
    elif lexeme == 'GOLEFT':
        return [40, "GOL_RES"]
    elif lexeme == 'GORIGHT':
        return [41, "GOR_RES"]
    elif lexeme == 'PICKFLOWER':
        return [42, "PICKF_RES"]
    elif lexeme == 'True' or lexeme == 'False':
        return [43, 'BOOL_LIT']
    elif lexeme == 'BEGIN':
        return [44, 'BEGIN_RES']
    # if the lexeme is acceptable as an identifier by Python language 
    # and hence our language (we both have the same conditions)
    elif lexeme.isidentifier():
        return [45, 'ID']
    # The lexeme does not belong to our language
    else:
        return [46,'UNKNOWN']


# Function to Remove empty elements "spaces" from the string of lexemes and line counters
def remove_empty():
    i=0
    for val in string_lexeme:
        if len(val)==0:
            del string_lexeme[i] 
            del line_counter[i] 
        i+=1
    

# to output our stream of tokens, list of lexemes, and corresponding line codes to the file
def write_to_file():
    # Open the output file
    output_file = open(os.path.join(os.path.dirname(__file__),'file2.txt'),'w')
    i=0 # initialize our index
    output_file.write("Code Line\t\t"+"Lexemes:"+'\t\t\t\t\t\t' + "Tokens:\n")
    for value in stream_of_tokens:
        # to output by columns: write to the file
        output_file.write(f"{str(line_counter[i])  : <15}{string_lexeme[i]  : <20}{value : >20} \n")
        # increment the index
        i=i+1 
    # close the output file
    output_file.close()


def in_symbol_table(element):
    global symbol_table
    # Check if the element exists in the symbol table
    for keyword in symbol_table :
        # Return True if the element exists in the symbol table
        if keyword[0] == element:
            return True
    # Return False if the element does not exist in the symbol table
    return False


def define_tokens():
    # This function is used to define lexemes with their respective token
    # To by default consider lexemes as non-string literals
    quotesFound = False
    # To add to the symbol table the list of reserved words and assign them to RES_WORD
    index =0 # send it as argument to gettoken in case of invalid lexeme
    for i in RES_WORDS:
        symbol_table.append([i,"RES_WORD"])
        
    for element in string_lexeme:
        # if lexeme is an Identifier,is still not in symbol table 
        # and is not a string literal
        if getToken(element)[0] == 45 and not in_symbol_table(element) and not quotesFound:
            # add lexeme and its type to the symbol table
            symbol_table.append([element, "ID"])
         # if lexeme is an int literal
        if getToken(element)[0] == 35:
            # add lexeme and its type to the literal table
            Literal_Table.append(['Int Literal', element])
             # if lexeme is a bool literal
        if getToken(element)[0] == 43:
            # add lexeme and its type to the literal table
            Literal_Table.append(['Boolean Literal', element])
         # if lexeme is a string literal    
        if element == '"' and not quotesFound:
            # the lexeme is a string literal=> change the default value to true
            quotesFound = True
            # add token to the stream of tokens
            stream_of_tokens.append(getToken(element)[1])
        # if lexeme is a string literal and it is still not the end of the literal
        elif quotesFound and element != '"':
            # add token to the stream of tokens
            stream_of_tokens.append('STR_LIT')
            # add lexeme and its type to the symbol table
            Literal_Table.append(['String Literal', element])
            # if it's the end of the string literal
        elif quotesFound and element == '"':
            # add token to the stream of tokens
            stream_of_tokens.append(getToken(element)[1])
            # reassign quotesFound to it's default value False 
            quotesFound = False
            # other types of lexemes: go check the token's name 
            # and add it to the stream of tokens  
        else:
            stream_of_tokens.append(getToken(element)[1])
            if getToken(element)[0] == 46:
                print("\nError: Unkown Lexeme: "+ string_lexeme[index] +" Line: "+ str(line_counter[index])+"\n")
                exit()
        index+=1    


# store lexemes in a string of lexemes
def process_lexeme(word):
    start=0 #To track the beginning of our different lexemes in one word
    val=0 # default value of 0: the word does not include any operator nor punctuation
    # loop to check if the word includes an operator or/and a punctuation
    for value in word:
        # if yes assign val value 1
        if value in operator or value in punctuation:
            val=1
    # If the word is a letter, name, digit, or acceptable identifier 
    # by python Language (same conditions as ours)=> it's a lexeme
    #for an alphanumeric lexeme (non acceptable identifier)=> it will 
    # be handeled as unkown token in the following steps "getToken function"
    if word.isalpha() or word.isdigit() or word.isidentifier() or word.isalnum():
        # add the lexeme to the lexeme string 
        string_lexeme.append(word)
        # assign line code to the lexeme for "printing" purposes
        line_counter.append(line)
    # The word satisfies none of the previous condition either 
    # because it is an unknown lexeme or spaces were not used 
    # but it includes an operator or/and a punction
    elif val==1:
        for value in word:
            if value in operator or value in punctuation:
                c = word.index(value)
                # add the lexemes(operator/punctuation sign + the preceding lexeme) 
                # to the lexeme string
                string_lexeme.append(word[start:c])
                string_lexeme.append(value)
                # assign line code to the lexemes for "printing" purposes
                line_counter.append(line)
                line_counter.append(line)
                # reassign the value of start to after operator/punctuation sign index
                start=c+1
                # delete operator/punctuation sign for further scanning purposes
                word = word[:c] + " " + word[c+1:]
        # if we still have lexemes after operators/punctuation signs 
        if c<len(word):
            string_lexeme.append(word[c+1:len(word)])
            # assign line code to the lexeme for "printing" purposes
            line_counter.append(line)
    # The word satisfies none of the previous condition either 
    # because it is an unknown lexeme or spaces were not used 
    # and it includes no operator nor a punction
    else:
        # add the lexeme to the lexeme string
        string_lexeme.append(word)
        # assign line code to the lexeme for "printing" purposes
        line_counter.append(line)

def print_to_cmd():
    global Literal_Table
    # Function to visualize in the Commands Line
    response = int(input('\n***** If you want to visualize the Symbol Table and Literal Table Press 1 else Press 0 *****\n'))
    # the user wants to visualize the symbol and literal table
    if response == 1: 
        # To visualize Symbol Table
        print("\t    Symbol Table:\n")
        print ("{:<30} {:<20}\n".format('Lexeme:','Type of Lexeme:'))
        for i in symbol_table:
            print(f"{i[0]: <30} {i[1]  : <20} ")
        # To visualize Literal Table
        print("\n\n\t    Literal Table:\n")
        print ("{:<30} {:<20}\n".format('Type:','Name:'))
        for i in Literal_Table:
            print(f"{i[0]: <30} {i[1]  : <20} ")
    # the user doesn't want to visualize thr symbol and literal table
    elif response == 0:
        print(" ")
    # the user entered another integer
    else:
        print("Invalid Entry")

# this function tackles the issue of substrings of tokens
def doubleCharacterFix():
    for i, element in enumerate(string_lexeme):
        if i+1 < len(string_lexeme):
            if string_lexeme[i] == '>' and string_lexeme[i+1] == '=':
                string_lexeme[i] = '>='
                string_lexeme.pop(i+1)
                line_counter.pop(i+1)
            elif string_lexeme[i] == '<' and string_lexeme[i+1] == '=':
                string_lexeme[i] = '<='
                string_lexeme.pop(i+1)
                line_counter.pop(i+1)
            elif string_lexeme[i] == '=' and string_lexeme[i+1] == '=':
                string_lexeme[i] = '=='
                string_lexeme.pop(i+1)
                line_counter.pop(i+1)
            elif string_lexeme[i] == '!' and string_lexeme[i+1] == '=':
                string_lexeme[i] = '!='
                string_lexeme.pop(i+1)
                line_counter.pop(i+1)
    
            


# Our Main Function
def main():
    read_from_file()
    remove_empty()
    remove_empty()
    doubleCharacterFix()
    define_tokens()
    write_to_file()
    # print_to_cmd()

#To Launch the Program   
if __name__=='__main__':
    main()