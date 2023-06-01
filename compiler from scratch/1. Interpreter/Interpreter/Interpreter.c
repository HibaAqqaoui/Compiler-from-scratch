//Hajar El Boutahri <80389>
//Hiba Aqqaoui <94519>
//Youssef Yousfi <85369>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define SEPARATOR 9999999999
#define Size_of_Memory 100
#define line_length 50
#define table_length 100

FILE *fileDir; //file Directory

// A structure to form an instruction with all of its elements
struct instruction{
   int operand_1; //to store the the first operand
   int operand_2; //to store the the second operand
   int operand_3; //to store the the third operand
   int opcode; //to store the opcode
   int sign; //to store the sign
}data[Size_of_Memory], code[Size_of_Memory];

int goOld = 1, loopIndex = Size_of_Memory, arrayToBeCreated = 0;

// structure that defines a symbol table and a label table
typedef struct table {
    int address;
    int index;
}l;

struct table symbolTable[table_length],labelTable[table_length];

//count of the number of elements in the symbol table, label table, and code array respectively
int stCount = 0, ltCount =0, cCount = 0;
//Initialize The Instruction Pointer
int IP = 0;
// A function to remove spaces from a string
void remove_spaces(char *line){
    int l=0, counter = 0;
    do{
        line[counter] = line[counter+l];
        if (line[counter] == ' ' || line[counter] == '\t'){
            counter--;
            l++;
        }
        counter++;
    }while(line[counter]);
}
// A function to turn a string with no spaces into a long long int
long long str_to_llong(char *str){
    char *lasting_characters;
    remove_spaces(str);
    long long result = strtoll (str, &lasting_characters, 10);
    return result;
}
// A function to store a string inside the data memory structure after turning it into a long long int first (sign, opcode, operand 1, operand 2, operand 3)
// It also checks if an array needs to be created if the size of a variable is different than 1
void putInData(char *line, int count){

    if (line[0] == '+') data[count].sign = 1;
    else if (line[0] == '-') data[count].sign = 0;

    char newLine[50];
    memcpy(newLine, &line[1], line_length);
    remove_spaces(newLine);
    long long int num = str_to_llong(newLine);

    data[count].operand_3 = abs(num % 1000);
    num /= 1000;
    data[count].operand_2 = abs(num % 1000);
    num /= 1000;
    data[count].operand_1 = abs(num % 1000);
    num /= 1000;
    data[count].opcode = num;
    if (data[count].operand_2 != 1 && count%2==0){
        arrayToBeCreated = 1;
    }
}

// A function to make sure that the labels used in the variables are known and are in the symbol table
void findInData(int address){
    int found = 0;
    for (int i = 0; i < stCount; i++){
        if (symbolTable[i].address == address) {
            found = 1;
        }
    }
    if (found == 0){
        if(address == 0){
        printf("000 is not a known label\n"); 
        exit(0);
        }
        else if ((int) log10(address) == 0){
        printf("00%d is not a known label\n", address);
        exit(0);
        }
        else if ((int) log10(address) == 1){
        printf("0%d is not a known label\n", address);
        exit(0);
        }
        else if ((int) log10(address) == 2){
        printf("%d is not a known label\n", address);
        exit(0);
        }
    }
}

// A function to store a string inside the code memory structure after turning it into a long long int first (sign, opcode, operand 1, operand 2, operand 3)
// It also checks if the operands correspond to an existing memory location for code instruction that use them
void putInCode(char *line, int count){
    if (line[0] == '+') code[count].sign = 1;
    else if (line[0] == '-') code[count].sign = 0;

    char newLine[50];
    memcpy(newLine, &line[1], line_length);
    remove_spaces(newLine);
    long long int num = str_to_llong(newLine);

    code[count].operand_3 = abs(num % 1000);
    num /= 1000;
    code[count].operand_2 = abs(num % 1000);
    num /= 1000;
    code[count].operand_1 = abs(num % 1000);
    num /= 1000;
    code[count].opcode = num;

    // We check if the operands used exist in the symbol table of the data memory
    if (code[count].opcode == 0){
        findInData(code[count].operand_3);
        findInData(code[count].operand_1);
    }
    else if(code[count].opcode == 4 || code[count].opcode == 5){
        findInData(code[count].operand_2);
        findInData(code[count].operand_1);
    }
    else if(code[count].sign == 1 && code[count].opcode == 8){
        findInData(code[count].operand_3);
    }
    else if(code[count].sign == 0 && code[count].opcode == 8){
        findInData(code[count].operand_1);
    }
    else if(code[count].opcode == 6){
        if (code[count].sign == 1){
            findInData(code[count].operand_1);
            findInData(code[count].operand_3);
        }
        else if(code[count].sign == 0){
            findInData(code[count].operand_1);
            findInData(code[count].operand_2);
        }
    }
    else if(code[count].opcode == 7){
        if (code[count].sign == 1){
        findInData(code[count].operand_2);
        findInData(code[count].operand_1);
        }
    }
    else if (code[count].opcode != 9){
        findInData(code[count].operand_3);
        findInData(code[count].operand_2);
        findInData(code[count].operand_ 1);
    }

    // We add to the label table when we encounter a -7 opcode
    if (code[count].sign == 0 && code[count].opcode == 7){
        labelTable[ltCount].address = code[count].operand_3;
        labelTable[ltCount].index = count + 1;
        ltCount++;
    }
    
}

// A function to check whether an address exists in the label table
int lt_find(int address){
    for (int i = 0; i<ltCount; i++){
        if (address == labelTable[i].address){
            return 1;
        }
    }
    return -1;
}
// A function to get the index of an address from the label table
int getLabelIndex(int address){
    for (int i = 0; i<ltCount; i++){
        if (address == labelTable[i].address){
            return labelTable[i].index;
        }
    }
}

// A function to check if the labels used in the code section have all been defined and stored in the label table
void checkLabelTable(){
    int ltCheck = -1;
    for (int i = 0; i < cCount ; i++){
        if (code[i].opcode == 4 || code[i].opcode == 5){
            ltCheck = lt_find(code[i].operand_3);
            if (ltCheck == -1 && code[i].operand_3>cCount-1){
                if (code[i].operand_3 == 0){
                    printf("000 is not a known label\n");
                    exit(0);
                }
                if ((int) log10(code[i].operand_3) == 0){
                    printf("00%d is not a known label\n", code[i].operand_3);
                    exit(0);
                }
                if ((int) log10(code[i].operand_3) == 1){
                    printf("0%d is not a known label\n", code[i].operand_3);
                    exit(0);
                }
                if ((int) log10(code[i].operand_3) == 2){
                    printf("%d is not a known label\n", code[i].operand_3);
                    exit(0);
                }
            }
        }
        else if(code[i].sign == 1 && code[i].opcode == 7){
            ltCheck = lt_find(code[i].operand_3);
            if (ltCheck == -1 && code[i].operand_3>cCount-1){
                if (code[i].operand_3 == 0){
                    printf("000 is not a known label\n");
                    exit(0);
                }
                if ((int) log10(code[i].operand_3) == 0){
                    printf("00%d is not a known label\n", code[i].operand_3);
                    exit(0);
                }
                if ((int) log10(code[i].operand_3) == 1){
                    printf("0%d is not a known label\n", code[i].operand_3);
                    exit(0);
                }
                if ((int) log10(code[i].operand_3) == 2){
                    printf("%d is not a known label\n", code[i].operand_3);
                    exit(0);
                }
            }
        }
        ltCheck = -1;
    }
}


// A function to get the index of an address from the symbol table
int getIndex(int address){
    for (int i=0; i<stCount; i++){
        if (symbolTable[i].address == address) return symbolTable[i].index;
    }
}

// A function to turn an instruction from structure form into a long long int
long long int Inst_to_LL(struct instruction inst){
    long long int n=0;
    n += (long long int)inst.operand_3;
    n += (long long int)inst.operand_2 * 1000;
    n += (long long int)inst.operand_1 * 1000000;
    n += (long long int)inst.opcode * 1000000000;
    if (inst.sign == 0) n*=-1;
    return n;
}

// A function to turn a long long int into a instruction in structure form and store it in the address given
void LL_to_Inst(long long int x, int address){
    int ind = getIndex(address) + 1;
    if (x >= 0)  data[ind].sign = 1;
    else {
        data[ind].sign = 0;
        x *= -1;
    }
    data[ind].operand_3 = abs(x % 1000);
    x /= 1000;
    data[ind].operand_2 = abs(x % 1000);
    x /= 1000;
    data[ind].operand_1 = abs(x % 1000);
    x /= 1000;
    data[ind].opcode = x;
}

// A function to create an array and initialize its elements beginning from the variable with the size that is different than 1
void createArray(int count){
    count--;
    int arrayStart = data[count-1].operand_1;
    int size = data[count-1].operand_2;
    for (int i=0; i<size; i++){
        data[count+1].sign = data[getIndex(arrayStart)+1].sign;
        data[count+1].opcode = data[getIndex(arrayStart)+1].opcode;
        data[count+1].operand_1 = data[getIndex(arrayStart)+1].operand_1;
        data[count+1].operand_2 = data[getIndex(arrayStart)+1].operand_2;
        data[count+1].operand_3 = data[getIndex(arrayStart)+1].operand_3;

        symbolTable[stCount].address = arrayStart + i + 1;
        symbolTable[stCount].index = count+1;
        stCount++;
        count++;
    }
    stCount--;
}

// A function to load the input file and store its instructions in the correct memory location
void load(FILE *fileDir){
    long long int num;
    int count = 0;
    char line[line_length];

    //loading the data section
    while(!feof(fileDir)){
        fgets(line,sizeof(line),fileDir);
        if(line == NULL || strlen(line) == 0) continue;
        
        char newLine[50];
        memcpy(newLine, &line[1], line_length);
        remove_spaces(newLine);
        num = str_to_llong(newLine);
        if (num == SEPARATOR) break;
        
        putInData(line,count);
        
        if (count%2 ==0){
        symbolTable[stCount].address = data[count].operand_1;
        symbolTable[stCount].index = count;
        stCount++;
        }
        count++;
    }
    
    // Check if an array needs to be created
    if (arrayToBeCreated == 1) {
        //handle the creation of the array
        createArray(count);
    }
    count = 0;
    
    //loading the code section
    while(!feof(fileDir)){
        fgets(line,sizeof(line),fileDir);
        if(line == NULL || strlen(line) == 0) continue;
        
        char newLine[50];
        memcpy(newLine, &line[1], line_length);
        remove_spaces(newLine);
        num = str_to_llong(newLine);
        if (num == SEPARATOR) break;

        putInCode(line, count);
        count++;
    }

    cCount = count;
    checkLabelTable();
}

// A function to decode and execute the instruction that the IP is pointing to
void decode_execute(){
    // switch case to handle operations
        switch(code[IP].sign)
        {
            case 1: //opcode starts with '+'
                switch(code[IP].opcode)
                {
                    case 0: //hadles assignment
                    {
                        int ind_1 = getIndex(code[IP].operand_1)+1;
                        int ind_3 = getIndex(code[IP].operand_3)+1;

                        data[ind_3].sign = data[ind_1].sign;
                        data[ind_3].opcode = data[ind_1].opcode;
                        data[ind_3].operand_1 = data[ind_1].operand_1;
                        data[ind_3].operand_2 = data[ind_1].operand_2;
                        data[ind_3].operand_3 = data[ind_1].operand_3;
                    }
                    break;
                    case 1: //handles addition
                    {
                        long long int s = 0;
                        s+= Inst_to_LL(data[getIndex(code[IP].operand_1)+1]);
                        s+= Inst_to_LL(data[getIndex(code[IP].operand_2)+1]);
                        if (s > 9999999999) s = 9999999999;
                        if (s < -9999999999) s = -9999999999;
                        LL_to_Inst(s,code[IP].operand_3);
                    }
                    break;

                    case 2: //handles multiplication
                    {
                        long long int s = 0;
                        s+= Inst_to_LL(data[getIndex(code[IP].operand_1)+1]);
                        s*= Inst_to_LL(data[getIndex(code[IP].operand_2)+1]);
                        if (s > 9999999999) s = 9999999999;
                        if (s < -9999999999) s = -9999999999;
                        LL_to_Inst(s,code[IP].operand_3);
                    }
                    break;
                    
                    case 4: // equality operator
                    {
                        if (Inst_to_LL(data[getIndex(code[IP].operand_1)+1]) == Inst_to_LL(data[getIndex(code[IP].operand_2)+1])){
                           if (lt_find(code[IP].operand_3) == 1){
                            int oldIP = IP;
                            IP = getLabelIndex(code[IP].operand_3);
                            if (code[IP].opcode == 7 && code[IP].sign ==1){
                                decode_execute();
                            }
                            else{
                                decode_execute();
                                if (goOld == 1) IP = oldIP;
                            }
                           }
                           else{
                            int oldIP = IP;
                            IP = code[IP].operand_3;
                            if (code[IP].opcode == 7 && code[IP].sign ==1){
                                decode_execute();
                            }
                            else{
                                decode_execute();
                                if (goOld == 1) IP = oldIP;
                            }
                           }
                           
                        }
                    }
                    break;

                    case 5: //greater or equal to operator
                    {
                        if (Inst_to_LL(data[getIndex(code[IP].operand_1)+1]) >= Inst_to_LL(data[getIndex(code[IP].operand_2)+1])) {
                           if (lt_find(code[IP].operand_3) == 1){
                            int oldIP = IP;
                            IP = getLabelIndex(code[IP].operand_3);
                            if (code[IP].opcode == 7 && code[IP].sign ==1){
                                decode_execute();
                            }
                            else{
                                decode_execute();
                                if (goOld == 1) IP = oldIP;
                            }
                            
                           }
                           else{
                            int oldIP = IP;
                            IP = code[IP].operand_3;
                            if (code[IP].opcode == 7 && code[IP].sign ==1){
                                decode_execute();
                            }
                            else{
                                decode_execute();
                                if (goOld == 1) IP = oldIP;
                            }

                           }
                           
                        }
                    }
                    break;
                    case 6:
                       if (Inst_to_LL(data[getIndex(code[IP].operand_2)+1]) == 0){
                        data[getIndex(code[IP].operand_3)+1].sign = data[getIndex(code[IP].operand_1)+1].sign;
                        data[getIndex(code[IP].operand_3)+1].opcode = data[getIndex(code[IP].operand_1)+1].opcode;
                        data[getIndex(code[IP].operand_3)+1].operand_1 = data[getIndex(code[IP].operand_1)+1].operand_1;
                        data[getIndex(code[IP].operand_3)+1].operand_2 = data[getIndex(code[IP].operand_1)+1].operand_2;
                        data[getIndex(code[IP].operand_3)+1].operand_3 = data[getIndex(code[IP].operand_1)+1].operand_3;
                       }
                       else{
                        data[getIndex(code[IP].operand_3)+1].sign = data[getIndex(code[IP].operand_1 + Inst_to_LL(data[getIndex(code[IP].operand_2)+1]))+1].sign;
                        data[getIndex(code[IP].operand_3)+1].opcode = data[getIndex(code[IP].operand_1 + Inst_to_LL(data[getIndex(code[IP].operand_2)+1]))+1].opcode;
                        data[getIndex(code[IP].operand_3)+1].operand_1 = data[getIndex(code[IP].operand_1 + Inst_to_LL(data[getIndex(code[IP].operand_2)+1]))+1].operand_1;
                        data[getIndex(code[IP].operand_3)+1].operand_2 = data[getIndex(code[IP].operand_1 + Inst_to_LL(data[getIndex(code[IP].operand_2)+1]))+1].operand_2;
                        data[getIndex(code[IP].operand_3)+1].operand_3 = data[getIndex(code[IP].operand_1 + Inst_to_LL(data[getIndex(code[IP].operand_2)+1]))+1].operand_3;
                       }
                    break;
                    


                    case 7: //increase, test, jump
                    {
                        goOld = 0;
                        loopIndex = IP;
                        int ind_1 = getIndex(code[IP].operand_1)+1;
                        int ind_2 = getIndex(code[IP].operand_2)+1;
                        int ind_3;
                        if(lt_find(code[IP].operand_3) == 1){
                            ind_3 = getLabelIndex(code[IP].operand_3);
                        }
                        else{
                            ind_3 = code[IP].operand_3;
                        }
                        
                        
                        long long int inc = Inst_to_LL(data[ind_1]);
                        inc++;
                        LL_to_Inst(inc,code[IP].operand_1);
                        
                        // The loop takes control over the IP
                        if (Inst_to_LL(data[ind_1]) < Inst_to_LL(data[ind_2])){
                            IP = ind_3-1;
                        }
                        
                    }
                    break;
                    case 8: //read input
                    {
                        
                        long long int num;
                        char line[line_length];
                        fgets(line,sizeof(line),fileDir);
        
                        char newLine[50];
                        memcpy(newLine, &line[1], line_length);
                        remove_spaces(newLine);
                        num = str_to_llong(newLine);
                        if (line[0] == '-') num *= -1;
                        LL_to_Inst(num, code[IP].operand_3);

                    }
                    break;
                    case 9: //stop execution
                        printf("Program Execution Ended");
                        exit(0);
                    break;
                }                
            break;



            case 0: //opcode is negative
                switch (code[IP].opcode)
                {
                case 1: //handles substraction
                {
                    long long int s = 0;
                        s+= Inst_to_LL(data[getIndex(code[IP].operand_1)+1]);
                        s-= Inst_to_LL(data[getIndex(code[IP].operand_2)+1]);
                        if (s > 9999999999) s = 9999999999;
                        if (s < -9999999999) s = -9999999999;
                        LL_to_Inst(s,code[IP].operand_3);
                }
                break;
                case 2: //handles division
                {
                    long long int s = 0;
                        s+= Inst_to_LL(data[getIndex(code[IP].operand_1)+1]);
                        s/= Inst_to_LL(data[getIndex(code[IP].operand_2)+1]);
                        LL_to_Inst(s,code[IP].operand_3);
                }
                break;
                case 4: //handles inequality
                {
                 if (Inst_to_LL(data[getIndex(code[IP].operand_1)+1]) != Inst_to_LL(data[getIndex(code[IP].operand_2)+1])){
                           if (lt_find(code[IP].operand_3) == 1){
                            int oldIP = IP;
                            IP = getLabelIndex(code[IP].operand_3);
                            if (code[IP].opcode == 7 && code[IP].sign ==1){
                                decode_execute();
                            }
                            else{
                                decode_execute();
                                if (goOld == 1) IP = oldIP;
                            }
                           }
                           else{
                            int oldIP = IP;
                            IP = code[IP].operand_3;
                            if (code[IP].opcode == 7 && code[IP].sign ==1){
                                decode_execute();
                            }
                            else{
                                decode_execute();
                                if (goOld == 1) IP = oldIP;
                            }
                           }
                           
                        }   
                }
                break;

                case 5: // strictly less than operator
                {
                    if (Inst_to_LL(data[getIndex(code[IP].operand_1)+1]) < Inst_to_LL(data[getIndex(code[IP].operand_2)+1])){
                           if (lt_find(code[IP].operand_3) == 1){
                            int oldIP = IP;
                            IP = getLabelIndex(code[IP].operand_3);
                            if (code[IP].opcode == 7 && code[IP].sign ==1){
                                decode_execute();
                            }
                            else{
                                decode_execute();
                                IP = oldIP;
                            }

                           }
                           else{
                            int oldIP = IP;
                            IP = code[IP].operand_3;
                            if (code[IP].opcode == 7 && code[IP].sign ==1){
                                decode_execute();
                            }
                            else{
                                decode_execute();
                                IP = oldIP;
                            }

                           }
                           
                        }
                }
                break;
                case 6:
                { 
                if (Inst_to_LL(data[getIndex(code[IP].operand_3)+1]) == 0){
                    data[getIndex(code[IP].operand_2)+1].sign = data[getIndex(code[IP].operand_1)+1].sign;
                    data[getIndex(code[IP].operand_2)+1].opcode = data[getIndex(code[IP].operand_1)+1].opcode;
                    data[getIndex(code[IP].operand_2)+1].operand_1 = data[getIndex(code[IP].operand_1)+1].operand_1;
                    data[getIndex(code[IP].operand_2)+1].operand_2 = data[getIndex(code[IP].operand_1)+1].operand_2;
                    data[getIndex(code[IP].operand_2)+1].operand_3 = data[getIndex(code[IP].operand_1)+1].operand_3;
                }
                else{
                    data[getIndex(code[IP].operand_2 + Inst_to_LL(data[getIndex(code[IP].operand_3)+1]))+1].sign = data[getIndex(code[IP].operand_1)+1].sign;
                    data[getIndex(code[IP].operand_2 + Inst_to_LL(data[getIndex(code[IP].operand_3)+1]))+1].opcode = data[getIndex(code[IP].operand_1)+1].opcode;
                    data[getIndex(code[IP].operand_2 + Inst_to_LL(data[getIndex(code[IP].operand_3)+1]))+1].operand_1 = data[getIndex(code[IP].operand_1)+1].operand_1;
                    data[getIndex(code[IP].operand_2 + Inst_to_LL(data[getIndex(code[IP].operand_3)+1]))+1].operand_2 = data[getIndex(code[IP].operand_1)+1].operand_2;
                    data[getIndex(code[IP].operand_2 + Inst_to_LL(data[getIndex(code[IP].operand_3)+1]))+1].operand_3 = data[getIndex(code[IP].operand_1)+1].operand_3;
                }
                }
                break;
                
                case 8: //handles printing
                    printf("%lld\n", Inst_to_LL(data[getIndex(code[IP].operand_1)+1]));
                break;
                }
            break;
        }
}


// A function to handle the running of the instructions and handling of the incrementation of the IP
// => The Read Execute Cycle
void ReadExecuteCycle(){
    while(1){
        decode_execute();
        IP++;
        if(IP>loopIndex){
            // the loopIndex is used to check wether we passed a loop in the sequence of instructions
            loopIndex = Size_of_Memory;
            // the goOld is used to check wether an instruction that jumps to another will resume the sequence of instructions
            // or will hand over control of the IP to the loop.
            goOld = 1;
        }
    }
}

int main(void){
    fileDir = fopen("input.txt","r");
    // if the file is not existing or the file naming is incorrect
    if (fileDir == NULL){
      printf (" **** Error: Could Not Open The File ! ****\n");
      printf ("\t\tPlease Check Again\n");
      exit (1);
    }
    //else go through the file and execute the code
    load(fileDir);
    checkLabelTable();
    ReadExecuteCycle();
    fclose (fileDir);
    return 0;
}