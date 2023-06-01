import Parser
import os
from treelib import Node, Tree

AST = Tree()

#address 000 is reserved for def_val "Default Value"
address = 1
codeLine = 0
varList = []
#varlist [address, name_of_variable, default_value, size]
instructionList = []
#instructionList [opcode, operand 1, operand 2, operand 3]

# A function to read the abstract syntax tree by going through the children of the root
# Other functions can act as the root to execute instructions that are nested in them
def read(node):
    global address,varList,codeLine
    for element in AST.children(node):
        if element.tag in Parser.Data_types:
            # if we find an initialization, we add to varList its address, name from the code, default_value, and size
            # we also add to the varList the value of the declared variable
            varList.append([address,AST.leaves(element.identifier)[0].tag,0,1])
            varList.append(['+0',0,0,0])
            address+=1
        elif element.tag == 'SET_RES':
            # checking is the assignment expression has the form: id/int_lit operator id/int_lit
            op1 = op2 = op3 = 0

            # the case of SET ID = ID/INT_LIT operator ID/INT_LIT;
            # in this case we split the work into two parts:
            # the first part is calculating the result of the ID/INT_LIT operator ID/INT_LIT and storing in the def_value address of 000
            # the second part is assigning the result from 000 to the destination variable
            if len(AST.children(element.identifier)) - 2 == 3:
                # we check if the one of the elements in the expression is a INT_LIT
                if AST.children(element.identifier)[2].tag.isnumeric():
                    # if the element is a INT_LIT and it does not have a unique variable declared that holds it value, we create one
                    if getAddress(AST.children(element.identifier)[2].tag) == 'not found':
                        varList.append([address,AST.children(element.identifier)[2].tag,AST.leaves(element.identifier)[2].tag,1])
                        if len(AST.children(element.identifier)[2].tag)<=3:
                            op3 = AST.children(element.identifier)[2].tag[0:3]
                            varList.append(['+0',0,0,op3])
                        elif len(AST.children(element.identifier)[2].tag) <= 6:
                            op3 = AST.children(element.identifier)[2].tag[3:6]
                            op2 = AST.children(element.identifier)[2].tag[0:3]
                            varList.append(['+0',0,op2,op3])
                        elif len(AST.children(element.identifier)[2].tag)<=9:
                            op3 = AST.children(element.identifier)[2].tag[6:9]
                            op2 = AST.children(element.identifier)[2].tag[3:6]
                            op1 = AST.children(element.identifier)[2].tag[0:3]
                            varList.append(['+0',op1,op2,op3])
                        else:
                            op3 = AST.children(element.identifier)[2].tag[7:10]
                            op2 = AST.children(element.identifier)[2].tag[4:7]
                            op1 = AST.children(element.identifier)[2].tag[1:4]
                            varList.append([('+' + AST.children(element.identifier)[2].tag[0]),op1,op2,op3])
                        address+=1
                if AST.children(element.identifier)[4].tag.isnumeric():
                    # if the other element is a INT_LIT and it does not have a unique variable declared that holds it value, we create one
                    if getAddress(AST.children(element.identifier)[4].tag) == 'not found':
                        varList.append([address,AST.children(element.identifier)[4].tag,AST.leaves(element.identifier)[4].tag,1])
                        if len(AST.children(element.identifier)[4].tag)<=3:
                            op3 = AST.children(element.identifier)[4].tag[0:3]
                            varList.append(['+0',0,0,op3])
                        elif len(AST.children(element.identifier)[4].tag) <= 6:
                            op3 = AST.children(element.identifier)[4].tag[3:6]
                            op2 = AST.children(element.identifier)[4].tag[0:3]
                            varList.append(['+0',0,op2,op3])
                        elif len(AST.children(element.identifier)[4].tag)<=9:
                            op3 = AST.children(element.identifier)[4].tag[6:9]
                            op2 = AST.children(element.identifier)[4].tag[3:6]
                            op1 = AST.children(element.identifier)[4].tag[0:3]
                            varList.append(['+0',op1,op2,op3])
                        else:
                            op3 = AST.children(element.identifier)[4].tag[7:10]
                            op2 = AST.children(element.identifier)[4].tag[4:7]
                            op1 = AST.children(element.identifier)[4].tag[1:4]
                            varList.append([('+' + AST.children(element.identifier)[4].tag[0]),op1,op2,op3])
                        address+=1



                #we get the addresses of the ID/INT_LITs used
                op1 = getAddress(AST.children(element.identifier)[2].tag)
                op2 = getAddress(AST.children(element.identifier)[4].tag)
                op3 = getAddress(AST.children(element.identifier)[0].tag)
                
                
                #we add to the instructionList according to the type of operation in the statement
                if AST.children(element.identifier)[3].tag == 'MULT_OP':
                #instruction= +2 address_of_id1 address_of_id2 address_of_destination
                    instructionList.append([+2,op1,op2,0])
                    codeLine+=1
                elif AST.children(element.identifier)[3].tag == 'DIV_OP':
                #instruction= -2 address_of_id1 address_of_id2 address_of_destination
                    instructionList.append([-2,op1,op2,0])
                    codeLine+=1
                elif AST.children(element.identifier)[3].tag == 'SUB_OP':
                #instruction= -1 address_of_id1 address_of_id2 address_of_destination
                    instructionList.append([-1,op1,op2,0])
                    codeLine+=1
                elif AST.children(element.identifier)[3].tag == 'ADD_OP':
                #instruction= +1 address_of_id1 address_of_id2 address_of_destination
                    instructionList.append([+1,op1,op2,0])
                    codeLine+=1
                instructionList.append([+0,000,000,op3])
                codeLine+=1
                
                
            # the case of SET ID = ID/INT_LIT;
            elif len(AST.children(element.identifier)) - 2 == 1:
                # we check if the element in the expression is a INT_LIT
                if AST.children(element.identifier)[2].tag.isnumeric():
                    # if the element is a INT_LIT and it does not have a unique variable declared that holds it value, we create one
                    if getAddress(AST.children(element.identifier)[2].tag) == 'not found':
                        varList.append([address,AST.children(element.identifier)[2].tag,AST.leaves(element.identifier)[2].tag,1])
                        if len(AST.children(element.identifier)[2].tag)<=3:
                            op3 = AST.children(element.identifier)[2].tag[0:3]
                            varList.append(['+0',0,0,op3])
                        elif len(AST.children(element.identifier)[2].tag) <= 6:
                            op3 = AST.children(element.identifier)[2].tag[3:6]
                            op2 = AST.children(element.identifier)[2].tag[0:3]
                            varList.append(['+0',0,op2,op3])
                        elif len(AST.children(element.identifier)[2].tag)<=9:
                            op3 = AST.children(element.identifier)[2].tag[6:9]
                            op2 = AST.children(element.identifier)[2].tag[3:6]
                            op1 = AST.children(element.identifier)[2].tag[0:3]
                            varList.append(['+0',op1,op2,op3])
                        else:
                            op3 = AST.children(element.identifier)[2].tag[7:10]
                            op2 = AST.children(element.identifier)[2].tag[4:7]
                            op1 = AST.children(element.identifier)[2].tag[1:4]
                            varList.append([('+'+AST.children(element.identifier)[2].tag[0]),op1,op2,op3])

                        op1 = getAddress(AST.children(element.identifier)[2].tag)
                        op3 = getAddress(AST.children(element.identifier)[0].tag)
                        instructionList.append([+0,op1,000,op3])
                        codeLine+=1
                        address+=1
                    else:
                        op1 = getAddress(AST.children(element.identifier)[2].tag)
                        op3 = getAddress(AST.children(element.identifier)[0].tag)
                        instructionList.append([+0,op1,000,op3])
                        codeLine+=1
                #if its not an INT_LIT, we find the address of the variable used 
                else:

                    op1 = getAddress(AST.children(element.identifier)[2].tag)
                    op3 = getAddress(AST.children(element.identifier)[0].tag)
                    instructionList.append([+0,op1,000,op3])
                    codeLine+=1
                
        elif element.tag == 'WHILE_RES':
            # in the while loop
            # if the condition is not satisfied, we skip the while loop's instructions
            # if the condition is satisfied, we do not jump, and we run the instructions,
            # and check at the end the condition again, and jump back if it is still satisfied

            # To check if the condition is not satisfied, and jump over the while loop:
            # We check if the negation of the condition is satisfied
            # This part of the code adds an instruction that will do the jump 
            op1 = getAddress(AST.children(element.identifier)[1].tag)
            op2 = getAddress(AST.children(element.identifier)[3].tag)
            # The op3 is set to 'jumpSkip' so that it can found later and changed to
            # the correct line to jump to after we handle the rest of the while loop
            op3 = 'jumpSkip'
            
            if AST.children(element.identifier)[2].tag == 'BT_OP':
                instructionList.append([+5,op2,op1,op3])
                codeLine+=1
            elif AST.children(element.identifier)[2].tag == 'LT_OP':
                instructionList.append([+5,op1,op2,op3])
                codeLine+=1
            elif AST.children(element.identifier)[2].tag == 'BTOE_OP':
                instructionList.append([-5,op1,op2,op3])
                codeLine+=1
            else:
                instructionList.append([-5,op2,op1,op3])
                codeLine+=1
            codeLineOg = codeLine

            # This part of the code handles the instructions in the while loop
            # by calling the read function with the start of the while loop as the root
            read(element.identifier)
            
            # This part of the code adds a check at the end of the while loop instructions
            # to check if the condition is still satisfied and that we have to go back through
            # the loop again 
            op1 = getAddress(AST.children(element.identifier)[1].tag)
            op2 = getAddress(AST.children(element.identifier)[3].tag)
            # The op3 is set to 'jumpLoopStart' so that it can found later and changed to
            # the correct line to jump to after we handle the rest of the while loop
            op3 = 'jumpLoopStart'
            if AST.children(element.identifier)[2].tag == 'BT_OP':
                instructionList.append([-5,op2,op1,op3])
                codeLine+=1
            elif AST.children(element.identifier)[2].tag == 'LT_OP':
                instructionList.append([-5,op1,op2,op3])
                codeLine+=1
            elif AST.children(element.identifier)[2].tag == 'BTOE_OP':
                instructionList.append([+5,op1,op2,op3])
                codeLine+=1
            else:
                instructionList.append([+5,op2,op1,op3])
                codeLine+=1
            

            # This part finds the op3 that need to be changed and sets them to the
            # correct line that must be jumped to
            for i in range(0,len(instructionList)):

                if instructionList[i][3] == 'jumpSkip':
                    instructionList[i][3] = codeLine
                if instructionList[i][3] == 'jumpLoopStart':
                    instructionList[i][3] = codeLineOg
                    break
        
        elif element.tag == 'IF_RES':
            # in the IF statement
            # if the condition is not satisfied, we skip the if statement's instructions
            # if the condition is satisfied, we do not jump, and we run the instructions

            # To check if the condition is not satisfied, and jump over the if statement:
            # We check if the negation of the condition is satisfied
            # This part of the code adds an instruction that will do the jump 
            op1 = getAddress(AST.children(element.identifier)[1].tag)
            op2 = getAddress(AST.children(element.identifier)[3].tag)
            # The op3 is set to 'jumpSkip' so that it can found later and changed to
            # the correct line to jump to after we handle the rest of the if statement
            op3 = 'jumpSkip'
            if AST.children(element.identifier)[2].tag == 'BT_OP':
                instructionList.append([+5,op2,op1,op3])
                codeLine+=1
            elif AST.children(element.identifier)[2].tag == 'LT_OP':
                instructionList.append([+5,op1,op2,op3])
                codeLine+=1
            elif AST.children(element.identifier)[2].tag == 'BTOE_OP':
                instructionList.append([-5,op1,op2,op3])
                codeLine+=1
            else:
                instructionList.append([-5,op2,op1,op3])
                codeLine+=1
            
            # This part of the code handles the instructions in the if statement
            # by calling the read function with the start of the if statement as the root
            read(element.identifier)

            # This part finds the op3 that need to be changed and sets them to the
            # correct line that must be jumped to
            for i in range(0,len(instructionList)):

                if instructionList[i][3] == 'jumpSkip':
                    instructionList[i][3] = codeLine
        
        elif element.tag == 'ELSE_RES':
            # This part of the code handles the instructions in the if statement
            # by calling the read function with the start of the if statement as the root

            # if the 'if' statement before the 'else' is skipped, it jumps directly into
            # the instructions of the else statement
            read(element.identifier)
        
        elif element.tag == 'READ_RES':
            # we find the address of the variable in the read function call
            op3 = getAddress(AST.children(element.identifier)[1].tag)
            # we add the 'read from input' instruction to the list of instructions with
            # with the appropriate address of the variable to be read to
            instructionList.append([+8,0,0,op3])
        
        elif element.tag == 'PRINT_RES':
            # we find the address of the variable in the print function call
            op1 = getAddress(AST.children(element.identifier)[1].tag)
            # we add the 'write to output' instruction to the list of instructions with
            # with the appropriate address of the variable to be written from
            instructionList.append([-8,0,0,op1])
        
        elif element.tag == 'main':
            # if we find the main, we handle its instructions by calling the read function
            # with main as the root
            read('main')
            return
        
        else:
            # if none of the above is found, we assume that we are dealing with a function call
            # we jump over to the function by finding it in the children of the root of the
            # whole program, and running a read function on it as the root
            # after that is done we go back to handle the rest of the statements in the main
            l = AST.children('root')
            for sublist in l:
                if sublist.tag == element.tag:
                    read(sublist.identifier)


# This function finds the address of a variable and returns it
# if the variable does not exist, we return 'not found'
def getAddress(value):
    for element in varList:
        if str(element[1]) == str(value):
            return element[0]
    return 'not found'


# A function to write the data and code section to a file
def writefunc():

    output_file = open(os.path.join(os.path.dirname(__file__),'file3.txt'),'w')
    output_file.write(('+0 000 001 000\n' ))
    output_file.write('+0 000 000 000\n')

    print('+0 000 001 000')
    print('+0 000 000 000')
    for i in range(0,len(varList),2):
        output_file.write( ('+0 ' + "{:03d}".format(varList[i][0]) +' '+ "{:03d}".format(varList[i][3])+' '+ '000\n') )
        output_file.write((varList[i+1][0]+' ' + "{:03d}".format(varList[i+1][1])+' ' + "{:03d}".format(varList[i+1][2])+' ' + "{:03d}".format(int(varList[i+1][3])) +'\n'))
        print('+0', "{:03d}".format(varList[i][0]), "{:03d}".format(varList[i][3]), '000')
        print(varList[i+1][0],"{:03d}".format(varList[i+1][1]),"{:03d}".format(varList[i+1][2]),"{:03d}".format(int(varList[i+1][3])))

    print('+9 999 999 999')
    output_file.write('+9 999 999 999\n')
    for element in instructionList:
        if element[0]>=0:
            print(('+' + str(element[0])), "{:03d}".format(element[1]), "{:03d}".format(element[2]), "{:03d}".format(element[3]))
            output_file.write( ('+' + str(element[0]))+' '+ "{:03d}".format(element[1])+' '+ "{:03d}".format(element[2])+' '+ "{:03d}".format(element[3]) +'\n' )
        else:
            print(element[0], "{:03d}".format(element[1]), "{:03d}".format(element[2]), "{:03d}".format(element[3]))
            output_file.write( (str(element[0])+' ' + "{:03d}".format(element[1])+' '+ "{:03d}".format(element[2])+' '+ "{:03d}".format(element[3]) + '\n') )
    print('+9 000 000 000')
    output_file.write('+9 000 000 000\n')
    print('+9 999 999 999')
    output_file.write('+9 999 999 999\n')

    
if __name__=='__main__':
    Parser.Code()
    AST = Parser.AST
    #AST.show(key= False)
    
    read('root')
    writefunc()