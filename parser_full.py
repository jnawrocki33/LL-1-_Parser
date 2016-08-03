#Lab Assignment 3
#Jason Nawrocki
#Type system and semantic analysis
#Takes as input a text file of lexemes and tokens
#It then parses out the syntax, and while doing so the program
#checks for type errors, and maintains the semantic state of the program
import sys

#global var
symTable = {}
iNextToken = 0
tokenStream = []
lexemeStream = []


def main(inputFileName):
    global tokenStream, lexemeStream, iNextToken, symTable
    tokenStream = []
    lexemeStream = []
    iNextToken = 0
    symTable = {}

    #Process the input file and build lists of tokens and lexemes
    inputFileObj = open(inputFileName, "r")
    bigStr = inputFileObj.read()
    bigList = bigStr.split() #bigList is a list of tokens and lexemes (alternating)
    tokenStream = bigList[0: :2] #List of tokens sliced from bigList (even elements)
    lexemeStream = bigList[1: :2] #List of lexemes

    print "Tokens:", tokenStream
    print "Lexemes:", lexemeStream

    program() #Start at the start symbol Program
    if iNextToken < len(tokenStream): #had to stop early
        print "end", iNextToken
        error(0)
    #print "success!"
    inputFileObj.close()

#this function parses out the opening, overall structure of the program
#it then calls declarations() and statements()
def program():
    global tokenStream, lexemeStream, iNextToken, symTable
    if tokenStream[iNextToken] == "type":
        iNextToken += 1
        if tokenStream[iNextToken] == "main":
            iNextToken += 1
            if tokenStream[iNextToken] == "(":
                iNextToken += 1
                if tokenStream[iNextToken] == ")":
                    iNextToken += 1
                    if tokenStream[iNextToken] == "{":
                        iNextToken += 1
                        declarations()
                        statements()
                        if tokenStream[iNextToken] == "}":
                            iNextToken += 1

#this function takes all the declarations while they are being made                    
def declarations():
    global tokenStream, lexemeStream, iNextToken, symTable
    while iNextToken < len(tokenStream) and \
          tokenStream[iNextToken] == 'type':
        declaration()

#this function takes a single declaration, and stores the varName in the symbol table
def declaration():
    global tokenStream, lexemeStream, iNextToken, symTable
    if tokenStream[iNextToken] == 'type':
        iNextToken += 1
        varType = lexemeStream[iNextToken - 1]
        while tokenStream[iNextToken] == 'id':
            varName = lexemeStream[iNextToken]
            if exists(varName): #check that the variable hasn't been declared before
                error(1)
            symTable[varName] = [varType, None] #store the variable in the symTable
            iNextToken += 1
            if tokenStream[iNextToken] == ",": #check for inline, continued declaration
                iNextToken += 1
        if tokenStream[iNextToken] == ';':
                iNextToken += 1
                return

    error(0)

#this function takes repeated statements
def statements():
    global tokenStream, lexemeStream, iNextToken, symTable
    while iNextToken < len(tokenStream) and \
          (tokenStream[iNextToken] == 'print' or tokenStream[iNextToken] == 'id' \
          or tokenStream[iNextToken] == "if" or tokenStream[iNextToken] == "return") \
          or tokenStream[iNextToken] == "while":
        statement(True)


#this function parses out a single statement
#boolCheck, input, is a check if assignment or print should be carried out or not
#boolCheck will be true unless the statement follows a false if/while condition
def statement(boolCheck):
    global tokenStream, lexemeStream, iNextToken, symTable
    
    if tokenStream[iNextToken] == 'print':
        iNextToken += 1
        value = expr()
        if tokenStream[iNextToken] == ";":
            iNextToken += 1
            if boolCheck: #only print if boolCheck is true
                print value
            return
           
    elif tokenStream[iNextToken] == 'id':
        varName = lexemeStream[iNextToken] #for use later
        if not exists(lexemeStream[iNextToken]): #var not declared?
            error(2)
        varType = symTable[varName][0]
        iNextToken += 1
        if tokenStream[iNextToken] == 'assignOp':
            iNextToken += 1
            value = expr()
            if tokenStream[iNextToken] == ';':
                iNextToken += 1
                
                if boolCheck: #check that the assignment statement isn't in a false if-statement
                    #check proper type assignment for bool, float, and int
                    if varType == "bool":
                        if isinstance(value, bool):
                            symTable[varName][1] = value
                        else:
                            error(3)
                    elif varType == "int":
                        if isinstance(value, bool): #must check, b/c boolLiteral = 1 or 0 in python
                            error(3)
                        elif isinstance(value, int):
                            symTable[varName][1] = value
                        else:
                            error(3)
                    #for floats, allow widening type conversion
                    #float or int can be assigned to this variable
                    elif varType == "float":
                        if isinstance(value, bool):
                            error(3)
                        elif isinstance(value, float):
                            symTable[varName][1] = value
                        elif isinstance(value, int):
                            symTable[varName][1] = value
                        else:
                            error(3)
                    else:
                        error(3)
                            
                return #success

    elif tokenStream[iNextToken] == "if":
        iNextToken += 1
        if tokenStream[iNextToken] == "(":
            iNextToken += 1
            value = expr() #consume the condition
            if not isinstance(value, bool): #condition must be true or false
                error(3)
            if tokenStream[iNextToken] == ")":
                iNextToken += 1
                statement(value) #consume a statement. value is a flag for assignment Yes/No
                if tokenStream[iNextToken] == "else":
                    iNextToken += 1
                    #in else statement, the flag value is reversed. evaluate if flag is false, don't evaluate if flag is true
                    if value == False:
                        statement(True)
                    else:
                        statement(False)
        return #success
                    
    elif tokenStream[iNextToken] == "while":
        iNextToken += 1
        if tokenStream[iNextToken] == "(":
            iNextToken += 1
            whileIndex = iNextToken #save the index at the beggining of the condition expression
            #while the expression is evaluated to True, parse/execute the statement
            while(expr()):
                if tokenStream[iNextToken] == ")":
                    iNextToken +=1
                    statement(True)
                    iNextToken = whileIndex
            #once the expression is evaluated false, parse the statement but do not execute
            if tokenStream[iNextToken] == ")":
                iNextToken += 1
                statement(False)
                return #success

    elif tokenStream[iNextToken] == "return":
        iNextToken += 1
        expr()
        if tokenStream[iNextToken] == ";":
            iNextToken += 1
            if boolCheck:
                exit() #exit once a return statement is called. no more should be carried out
            return

    #otherwise, there is an error case:
    print "here now", iNextToken 
    error(0)


#this function parses out an expression
#an expression is one or more conjunctions
#return the value of the expression
def expr():
    global tokenStream, lexemeStream, iNextToken, symTable

    result = conjunction() #consume a conjunction first, save its result

    #consume other conjunctions of they are connected by "||"
    while iNextToken < len(tokenStream) and (lexemeStream[iNextToken] == "||"):
        iNextToken += 1
        result2 = conjunction()
        #make sure the conjunctions evaluate to boolean in this case.
        if not isinstance(result, bool):
            error(0)
        if not isinstance(result2, bool):
            error(0)
        #if one conjunction is true, the condition is true
        if result == True:
            return result
        #if not, make current result result2, and look for the next conjunction
        result = result2
    return result

#this function parses out a conjunction
#a conjunction is one or more equalities
#it returns the result
def conjunction():
    global tokenStream, lexemeStream, iNextToken, symTable
    result = equality()
    
    #take more equalities if possible
    while iNextToken < len(tokenStream) and lexemeStream[iNextToken] == "&&":
        iNextToken += 1
        result2 = equality()
        if not isinstance(result, bool):
            error(0)
        if not isinstance(result2, bool):
            error(0)
        #if result is true, make sure the other results are also true
        if result == True:
            result = result2
        #as soon as one result is false, the whole condition is false
        else:
            break
    return result

#this function parses out an equality
#an equality is one or two relations
#it returns the value
def equality():
    global tokenStream, lexemeStream, iNextToken, symTable
    result = relation()
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "equOp":
        #two cases, "==" or "!=". evaluate and return the result
        if lexemeStream[iNextToken] == "==":
            iNextToken += 1
            result2 = relation()
            if result == result2:
                return True
            return False
        elif lexemeStream[iNextToken] == "!=":
            iNextToken += 1
            result2 = relation()
            if result != result2:
                return True
            return False

    return result


#this function parses out a relation
#a relation is one or two additions
#it returns the result
def relation():
    global tokenStream, lexemeStream, iNextToken, symTable
    result = addition()
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "relOp":
        op = lexemeStream[iNextToken]
        iNextToken += 1
        result2 = addition()
        #evaluate for whichever of the 4 operations is being used, then return
        if op == "<":
            return result < result2
        if op == "<=":
            return result <= result2
        if op == ">":
            return result > result2
        if op == ">=":
            return result >= result2
    return result


#this function parses out an addition
#an addition is one or more terms
#return the result
def addition():
    global tokenStream, lexemeStream, iNextToken, symTable
   
    result = term() #Consume a Term first and save its result
    while iNextToken < len(tokenStream) and \
            (lexemeStream[iNextToken] == "+" or lexemeStream[iNextToken] == "-"):
        sign = 1 if lexemeStream[iNextToken] == "+" else -1
        iNextToken += 1 #Consumed the + or - token
        v = term() #Consume another Term
        #check that boolean and int/float aren't being added:
        if not typeChecker(result, v):
            error(3)
        result = result + sign * v
    return result

#parse out a term. one or more factors. then return the result
def term():
    global tokenStream, lexemeStream, iNextToken, symTable
    result = factor() #Consume a Factor

    while iNextToken < len(tokenStream) and \
            (lexemeStream[iNextToken] == "*" or lexemeStream[iNextToken] == "/"):
        exponent = 1 if lexemeStream[iNextToken] == "*" else -1
        if lexemeStream[iNextToken] == "%": #make modulus exponent 0 for ID purpose
            exponent = 0
        iNextToken += 1 #Consumed the * or / token
        v = factor() #Consume another Factor
        #check that boolean and int/float aren't multiplied
        if not typeChecker(result, v):
            error(3)
        if exponent == 0:
            result = result % v
        elif exponent == 1:
            result = result * v
        else:
            result = result / v
    return result


#parse out a factor, and return its value
def factor():
    global tokenStream, lexemeStream, iNextToken, symTable
    if iNextToken < len(tokenStream) and \
       (tokenStream[iNextToken] == "intLiteral" or \
        tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "boolLiteral" or \
        tokenStream[iNextToken] == "floatLiteral" or tokenStream[iNextToken] == "("):
        iPrevToken = iNextToken
        iNextToken += 1

        #consume an identifier
        if tokenStream[iPrevToken] == "id":
            varName = lexemeStream[iPrevToken]
            if not exists(varName): #make sure the identifier exists
                error(2)
            if symTable[varName][1] == None: #make sure the identifier has a value
                error(4)
            varType = symTable[varName][0]
            #depending on the type, return the properly type casted value
            if varType == "bool":
                if symTable[lexemeStream[iPrevToken]][1] == True:
                    return True
                else:
                    return False
            if varType == "int":
                return int(symTable[lexemeStream[iPrevToken]][1])
            if varType == "float": #can be an int or float
                if isinstance(symTable[lexemeStream[iPrevToken]][1], float):
                    return float(symTable[lexemeStream[iPrevToken]][1])
                if isinstance(symTable[lexemeStream[iPrevToken]][1], int):
                    return int(symTable[lexemeStream[iPrevToken]][1])
    
         #for literals, return the type casted value of the literal   
        if tokenStream[iPrevToken] == "intLiteral":
            return int(lexemeStream[iPrevToken])
        if tokenStream[iPrevToken] == "floatLiteral":
            return float(lexemeStream[iPrevToken])
        if tokenStream[iPrevToken] == "boolLiteral":
            if lexemeStream[iPrevToken] == "true":
                return True
            else:
                return False

        #for a parenthetical expression, consume and return the expression value
        if tokenStream[iPrevToken] == "(":
            exprVal = expr()
            if tokenStream[iNextToken] == ")":
                iNextToken += 1
                return exprVal
            
    error(0)

#check that the varName exists in the symbol table
def exists(varName):
    global tokenStream, lexemeStream, iNextToken, symTable
    global symTable
    return symTable.has_key(varName)

#function that returns an appropriate error message and exits
def error(e):
    if e == 1:
        print "Error! variable already declared!"
        exit()
    if e == 2:
        print "Error! variable not yet declared!"
        exit()
    if e == 3:
        print "Error! incompatable type!"
        exit()
    if e == 4:
        print "Error! variable not yet initialized!"
        exit()
    print "Error Detected!"
    exit()

#this function checks that boolean isn't added/multiplied with int/float
def typeChecker(v1, v2):
    if isinstance(v1, bool):
        return isinstance(v2, bool)
    if isinstance(v2, bool):
        return isinstance(v1, bool)
    return True

    
