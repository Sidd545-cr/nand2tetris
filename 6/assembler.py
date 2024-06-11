import sys
import re

def get_dest(line):
    dest = {"null":"000","M":"001","D":"010","DM":"011","MD":"011","A":"100","AM":"101","AD":"110","ADM":"111"}
    return dest[line.strip()]

def get_jump(line):
    jump = {"null":"000","JGT":"001","JEQ":"010","JGE":"011","JLT":"100","JNE":"101","JLE":"110","JMP":"111"}
    return jump[line.strip()]

def get_comp(line):
    comp_A = {"0":"101010","1":"111111","-1":"111010","D":"001100","A":"110000","!D":"001101","!A":"110001","-D":"001111","-A":"110011","D+1":"011111","A+1":"110111","D-1":"001110","A-1":"110010","D+A":"000010","D-A":"010011","A-D":"000111","D&A":"000000","D|A":"010101"}
    comp_M = {"M":"110000","!M":"110001","-M":"110011","M+1":"110111","M-1":"110010","D+M":"000010","D-M":"010011","M-D":"000111","D&M":"000000","D|M":"010101"}
    if "M" in line:
        return "1" + comp_M[line.strip()]
    else:
        return "0" + comp_A[line.strip()]

def A_handler(line):
    line=line.strip()
    try:
        line1 = int(line[1:])
        line1 = "0" + format(line1, "b").zfill(15) 
    except ValueError:
        try:
            line1 = line[1:]
            line1 = "0" +format(Symbol_table[line1], "b").zfill(15)
        except KeyError:
            print("[!] Error: Symbol_table failed")

    print(f"{line1} : {line}")
    return line1

def C_handler(line):
    if re.findall(".*=",line) !=[]:
        d = re.findall(".*=",line)[0][:-1]
    else:
        d = "null"
    if re.findall(";.*",line) !=[]:
        j = re.findall(";.*",line)[0][1:]
    else:
        j = "null"
    if re.findall("=.*",line)!=[]:
        c = re.findall("=.*",line)[0][1:]
        if ";" in c:
            c = c[:-4]
    elif re.findall(".*;",line) !=[]:
        c = re.findall(".*;",line)[0][:-1]

    dest = get_dest(d)
    jump = get_jump(j)
    comp = get_comp(c)
    print("111" + comp + dest + jump,":", line)
    line = "111" + comp + dest + jump
    return line

def analyze_line(lines):
    lineNo=len(lines)
    i=0
    while i<lineNo:
        line = lines[i]

        if "@" in line:
            line = A_handler(line.strip("\n"))
            lines[i]=line
        elif "=" in line or ";" in line:
            line = C_handler(line)
            lines[i]=line
        i+=1
    return lines

def create_symbol_table():
    global Symbol_table
    Symbol_table = {"R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,"R6":6,"R7":7,"R8":8,"R9":9,"R10":10,"R11":11,"R12":12,"R13":13,"R14":14,"R15":15,"SCREEN":16384,"KBD":24576,"SP":16,"LCL":17,"ARG":18,"THIS":19,"THAT":20,"LOOP":21,"STOP":22,}

def Eliminate_comments(lines):
    new_lines = []
    for i in lines:
        if "//" not in i:
            new_lines.append(i)
    return new_lines

def First_pass(lines):

    noLines = len(lines)
    i=0
    while i<noLines:
        if re.findall(r"\(.*\)",lines[i]) !=[]:
            symbol = re.findall(r"\(.*\)",lines[i])[0][1:-1]
            Symbol_table.update({symbol:i})
            print("Symbol table updated")
            lines.pop(i)
            noLines=len(lines)
        i+=1

def Second_pass(lines):
    noLines= len(lines)
    i=0
    addr=23
    while i<noLines:
        if "@" in lines[i]:
            if re.findall("[^1-9].*",lines[i][1:]) !=[]:
                symbol = re.findall("[^1-9].*",lines[i][1:])[0].strip() 
                try:
                    Symbol_table[symbol]
                except KeyError:
                    Symbol_table.update({symbol:addr})
                    addr+=1
        i+=1

def main():
    #path = sys.argv[1]
    path = input("Enter File Path: ")
    new_path = path.split(".")[0] + ".hack"

    f1 = open(path,"r")
    text = f1.readlines()
    f1.close()

    create_symbol_table()
    text = Eliminate_comments(text)
    First_pass(text)
    Second_pass(text)
    text = analyze_line(text)

    f2 = open(new_path,"w")
    for line in text:
        if "\n" in line:
            pass
        else:
            f2.writelines(line+"\n")
    f2.close
    #print(text)

main()