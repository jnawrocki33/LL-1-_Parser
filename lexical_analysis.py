#Jason Nawrocki
#Lab 1, Lexical Analysis
#This program mimics the action of the lexical analizer part of a compiler
#It reads in a file, and runs through it, building tokens thus categorizing the parts of the file

def lexAnalizer():
    #read the file into string
    fileName = raw_input("Enter the file name: ")
    inputFile = open(fileName, 'r')
    string = inputFile.read()
    inputFile.close()
    
    #infinite while loop, inside which the text will be analized. i is the index counter
    #there are multiple if statements, representing possible cases of what character is found
    i = 0
    while True:
        
        #here is a check that the analysis hasn't reached the last character.
        #if so, make sure to not attempt to check further beyond this point
        if i >= len(string):
            break
        if i == len(string) - 1:
            if string[i].isalpha() == True:
                print 'char litteral', '\t', string[i]
                break

            if string[i].isdigit() == True:
                print 'intLitteral', '\t', string[i]
                break

        #white space is a simple advance in i
        if string[i].isspace() == True:
            i += 1
            continue

        #if a letter is found, start building an identifier
        if string[i].isalpha() == True:
            #call testID to build the identifier
            iD = testID(i, string)
            #check is returned by checkReserve(), telling if iD is a reserved word
            #checkReserve will return 1,2,3, or 4 based on what type of reserved word iD is
            check = checkReserve(iD)
            if check == 1:
                print iD, '\t', iD
            if check == 2:
                print 'type', '\t', iD
            if check == 3:
                print 'boolLitteral', '\t', iD
            if check == 4:
                print 'id', '\t', iD
            i = i + len(iD)
            continue

        #case of finding punctuation
        if isPunctuation(string[i]) == True:
            print string[i], '\t', string[i]
            i +=1
            continue

        #case of '='. Must check for '=' vs. '=='
        if string[i] == '=':
            if string[i+1] == '=':
                print 'equOp', '\t', '=='
                i += 2
                continue
            print 'assignOp', '\t', '='
            i += 1
            continue

        #case of '!'. check for '!='
        if string[i] == '!':
            if string[i+1] == '=':
                print 'equOp', '\t', '!='
                i += 2
                continue
            print 'unknown use of "!"', '\t', '!'
            i +=1
            continue

        #case of relOps
        if string[i] == '<' or string[i] == '>':
            if string[i+1] == '=':
                print 'relOp', '\t', string[i]+string[i+1]
                i += 2
                continue
            print 'relOp', '\t', string[i]
            i += 1
            continue

        #case of digit being found. then start building potential float/int
        if string[i].isdigit() == True:
            num = testNum(i, string)
            #'f' is returned from isDigit() if the number is a float
            if num[len(num)-1] == 'f':
                num = num[0, len(num) - 1]
                print 'floatLitteral', '\t', num
            print 'intLitteral', '\t', num
            i += len(num)
            continue

        #case of addOp
        if string[i] == '+' or string[i] == '-':
            print 'addOp', '\t', string[i]
            i += 1
            continue
        #case of multOp
        if string[i] == '*':
            print 'multOp', '\t', '*'
            i += 1
            continue
        
        #case of '/'. comment versus division
        if string[i] == '/':
            if string[i + 1] == '/':
                i+=1
                comment = "//"
                #build comment until end of line character
                while string[i+1] != '\n':
                    comment += string[i+1]
                    i += 1
                print 'comment', '\t', comment
                i += 1
                continue

            print 'multOp', '\t', '/'
            i += 1
            continue
        #case of a potential character, check for matching ''
        if string[i] == "'":
            #check that the index wont exceed string length
            if i >= len(string) - 2:
                print "unrecognized '", "\t", "'"
                i+=1
                continue
            
            #now check that the character is matching apostrophes with a letter inside
            if string[i+1].isalpha() == True:
                if string[i+2] == "'":
                    print "charLitteral", "\t", string[i]+string[i+1]+string[i+2]
                    i += 3
                    continue
                print "invalid token!"
                i +=2
                continue
            print "invalid token!"
            i += 1
            continue


#this function tests a potential identifier
#it is only called once a letter has been read from the input file
#it then builds the identifier with following letters and numbers, and returns the iD
def testID(index, string):
    iD = string[index]
    while string[index+1].isalpha() or string[index+1].isdigit():
        iD = iD + string[index+1]
        index = index + 1
    return iD

#this function tests a potential integer/float
#it builds digits until reaching a nondigit or decimal point
#if a decimal point is found, a 'f' is appended to the end of the string
#this is a check for float vs. integer
#it returns the integer/float found
def testNum(i, string):
    num = str(string[i])
    while string[i+1].isdigit() == True:
        num = num + str(string[i+1])
        i += 1
    if string[i + 1] == ".":
        while string[i+1].isdigit() == True:
            num = num + str(string[i+1])
            i += 1
        num = num + 'f'
        
    if string[i+1].isalpha() == True:
        print " "
        print "***invalid token!"
        print " "
        
    return num


#this function checks if an identifier is actually a reserved word
#it returns an int 1,2,3, or 4 based on what class of reserved word it is
def checkReserve(iD):
    #case where iD is reserved word
    list = ['main', 'if', 'else', 'while', 'return', 'print']
    for word in list:
        if iD == word:
            return 1

    #case where iD is a type
    list = ['int', 'float', 'bool', 'char']
    for word in list:
        if iD == word:
            return 2

    #case where iD is a boolLitteral
    list = ['true', 'false']
    for word in list:
        if iD == word:
            return 3
    #case where iD is an identifier
    return 4

#this function simply checks if a character is punctuation, returns true/false
def isPunctuation(char):
    punctuation = [';','(',')','{','}','[',']']
    for item in punctuation:
        if char == item:
            return True
    return False

