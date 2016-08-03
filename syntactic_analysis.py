#lab assignment 2
#syntactic analysis, LL(1) parser
#Jason Nawrocki

#Input: Text file where each line has a token and the corresponding lexeme
#Output: Success iff no syntax error

def main():
    #read the file into a string, then split into a list
    fileName = raw_input("Enter the file name: ")
    inputFile = open(fileName, 'r')
    string = inputFile.read()
    bigList = string.split()
    tokenList = bigList[0::2] #List of tokens, even elements
    lexemeList = bigList[1::2] #List of lexemes, odd elements
    
    inputFile.close()
    print "List of tokens:"
    print tokenList
    print "\n List of lexemes:"
    print lexemeList
    
    i = 0 #this i the index which is incremented through the tokenList
    i = program(i, tokenList) # running program() will begin the recursive descent
    
    #after parsing, i will be equal to the length of the list, because every
    #token will be succesfully consumed
    #if every token cannot be consumed, or if the index goes beyond the list length
    #then there must be a syntactic error
    if i == len(tokenList):
        print "Syntactically Correct"
        return
    print "Unsuccessful parsing - syntactically incorrect"
    return

#all of the following functions take i and the tokenList as inputs
#they return the possibly changed i

#they also repeatedly check that the index has not exceeded the list size
#if so, error() will be called which terminates the program, indicating a failed parse

#this function checks that the structure of the main declaration is inact.
#it makes calls to declarations and statements
def program(i, tokenList):
    if tokenList[len(tokenList)-1] != "}": #simple case where the code does not end with a brace. error.
        error()
    #check the overall structure of the main function declaration:
    if tokenList[i] == "type":
        i += 1
        if i >= len(tokenList):
            error()
        if tokenList[i] == "main":
            i += 1
            if i >= len(tokenList):
                error()
            if tokenList[i] == "(":
                i += 1
                if i >= len(tokenList):
                    error()
                if tokenList[i] == ")":
                    i += 1
                    if i >= len(tokenList):
                        error()
                    if tokenList[i] == "{":
                        i += 1
                        if i >= len(tokenList):
                            error()
                            
                        #call declarations and statements  
                        i = declarations(i, tokenList)
                        if i >= len(tokenList):
                            error()
                        i = statements(i, tokenList)
                        if i >= len(tokenList):
                            error()
                            
                        if tokenList[i] == "}":
                            i += 1
    return i

#consume declarations
def declarations(i, tokenList):
    while i < len(tokenList) and tokenList[i] == "type":
        i = declaration(i, tokenList)
    return i

#consume a declaration
def declaration(i, tokenList):
    while i < len(tokenList) and tokenList[i] == "type":
        i += 1
        if i >= len(tokenList):
            error()
        if tokenList[i] == "id":
            i += 1
            #must check for multiple declarations in one line
            while i < len(tokenList) and tokenList[i] == ",":
                i += 1
                if i >= len(tokenList):
                    error()
                if tokenList[i] == "id":
                    i += 1
        if i >= len(tokenList):
            error()
        if tokenList[i] == ";":
            i += 1
                
    return i


#consume statements, possible statements are print, if, while, return, or assignment
#while loop makes it possible to consume multiple statements
def statements(i, tokenList):
    while i < len(tokenList) and (tokenList[i] == "print" or tokenList[i] == "if" or \
          tokenList[i] == "while" or tokenList[i] == "return" or \
          tokenList[i] == "id"):
        
        i = statement(i, tokenList)
        if i >= len(tokenList):
            error()
        
    return i

#consume a single statement
def statement(i, tokenList):
    
    if i >= len(tokenList):
        error()
    #print statement, consume the proper elements (while ensuring index in bound)
    if tokenList[i] == "print":
        i += 1
        if i >= len(tokenList):
            error()
        i = expression(i, tokenList)
        if i >= len(tokenList):
            error()
        if tokenList[i] == ";":
            i += 1
        else:
            error()
            
    #if statement, consume the proper elements
    elif tokenList[i] == "if":
        i += 1
        if i >= len(tokenList):
            error()
        if tokenList[i] == "(":
            i += 1
            if i >= len(tokenList):
                error()
            i = expression(i, tokenList)
            if i >= len(tokenList):
                error()
            if tokenList[i] == ")":
                i += 1
                if i >= len(tokenList):
                    error()
                i = statement(i, tokenList)
                
                #check if it has an else part
                if i >= len(tokenList):
                    error()
                if tokenList[i] == "else":
                    i += 1
                    if i >= len(tokenList):
                        error()
                    i = statement(i, tokenList)
                    
    #while loop
    elif tokenList[i] == "while":
        i += 1
        if i >= len(tokenList):
            error()
        if tokenList[i] == "(":
            i += 1
            if i >= len(tokenList):
                error()
            i = expression(i, tokenList)
            if i >= len(tokenList):
                error()
            if tokenList[i] == ")":
                i += 1
                if i >= len(tokenList):
                    error()
                i = statement(i, tokenList)
                
    #return statement
    elif tokenList[i] == "return":
        i += 1
        if i >= len(tokenList):
            error()
        i = expression(i, tokenList)
        if i >= len(tokenList):
            error()
        if tokenList[i] == ";":
            i += 1
        else:
            error()

    #assignment statement
    elif tokenList[i] == "id":
        if i >= len(tokenList):
            error()
        i += 1
        if i >= len(tokenList):
            error()
        if tokenList[i] == "assignOp":
            i += 1
            if i >= len(tokenList):
                error()
            i = expression(i, tokenList)
            if i >= len(tokenList):
                error()
            if tokenList[i] == ";":
                i += 1
            else:
                error()
    return i

#consume an expression, which is one or more conjunctions
def expression(i, tokenList):
    i = conjunction(i, tokenList)
    
    while i < len(tokenList) and tokenList[i] == "||":
        i += 1
        i = conjunction(i, tokenList)
                          
    return i

#consume a conjunction, which is one or more equalities
def conjunction(i, tokenList):
    i = equality(i, tokenList)
    while i < len(tokenList) and tokenList[i] == "&&":
        i += 1
        i = equality(i, tokenList)

    return i

#consume an equality, which is one or two relations
def equality(i, tokenList):
    i = relation(i, tokenList)
    if i >= len(tokenList):
        error()
    if tokenList[i] == "equOp":
        i += 1
        i = relation(i, tokenList)

    return i

#consume a relation, which is one or two additions
def relation(i, tokenList):
    i = addition(i, tokenList)
    if i >= len(tokenList):
        error()
    if tokenList[i] == "relOp":
        i += 1
        i = addition(i, tokenList)
    return i

#consume an addition, which is one or more terms
def addition(i, tokenList):
    i = term(i, tokenList)
    while i < len(tokenList) and tokenList[i] == "addOp":
        i += 1
        i = term(i, tokenList)
    return i

#consume a term, which is one or more factors
def term(i, tokenList):
    i = factor(i, tokenList)
    while i < len(tokenList) and tokenList[i] == "multOp":
        i += 1
        i = factor(i, tokenList)
    return i

#consume a factor, which is an id, a literal, or a parenthetical expression
def factor(i, tokenList):
    if i >= len(tokenList):
        error()
    if tokenList[i] == "id" or tokenList[i] == "intLiteral" or \
       tokenList[i] == "boolLiteral" or tokenList[i] == "floatLiteral":
        i += 1
    if i >= len(tokenList):
        error()
        
    #possible consumption of a parenthetical expression
    if tokenList[i] == "(":
        i += 1
        if i >= len(tokenList):
            error()
        i = expression(i, tokenList)
        if i >= len(tokenList):
            error()
        if tokenList[i] == ")":
            i += 1
    return i


#error function
#called in cases where the index exceedes the list size
#the function prints an error message then exits
def error():
    print "Unsuccessful parsing - syntactically incorrect"
    exit()

    
