#--------------------------------------------- queries.py ------------------------------------------#
# A simple query engine. The query engine can read queries from the command line or text files.     #
# A parser first parses the queries. Then a validator performs simple and superficial validation,   #
# ensuring the query is of the form db.final.<<operationName>>(args) where operationName is one of  #
# find, count, min or cartprod. The validator does not check the argument lists because different   #
# operations take in different kinds of arguments. The parser reads the query and detects which     #
# operation is being requested. It calls the correct method for the operation being requested,      #
# extracts the argument list and sends it to this method. Each method is responsible for parsing    #
# it's own argument list. Finally the methods, one for each operation, find(args), a_min(args),     #
# a_count(args), cartprod(args) perform the operations against the database file.                   #
# The database file is defined by the global variable FINAL.                                        #
#                                              USAGE                                                #
# Import the parse(query) module and feed the user input to this function.                          #
# Eg: from queries import parse                                                                     #
#     query = input("Enter a query: ")                                                              #
#     parse(query)                                                                                  #
# The parse function will take care of calling the requested operation, loading the database file,  #
# running the operation against the database file and printing the results.                         #
# Finally to read queries from a file, which contains one query per line use readFile(queryFile)    #
# readFile calls parse so nothing else is required. ReadFile takes one argument the location, name  #
# of the file containing queries.                                                                   #
# Expected input: The database file must be a binary file and consist of a single collection.       #
# Each collection is a list of dictionaries. Use the python pickle module to write a binary file.   #
# This parser is brittle and will only work on queries that match the specification defined above   #
#---------------------------------------------------------------------------------------------------#


import re
from makeDB import writeDB, loadDB

FINAL = "final"
#def main():
    #data = input("Enter the location of the data file:")
    #writeDB("check.txt","final2")
    #print("Database Written. Loading DB file.")
    #l = loadDB("final")
    #print("Database Loaded.")
    #for document in l:
    #    print(document)
    #query = " "
    #while query != "":
    #    query = input("Enter a query: ")
    #    if valid(query):
            #print("Valid query")
    #        parse(query.split('.')[2])
            #parse(query)
    #    else:
    #        print("Invalid query.")

def readFile(queryFile):
    with open (queryFile,'r') as f:
        for line in f:
            print("query: {0}".format(line), end="")
            parse(line)

def valid(query):
    valid_operations = ['find', 'count', 'min', 'cartprod']
    #Check if query is valid
    q = query.split('.')
    if ( q[0] != 'db' or q[1] != 'final') :
        return False
    else :
        if ( q[2].split("(")[0] in valid_operations and q[2].endswith(')') ):
            return True
        else:
            return False

def parse(query):
    query = re.sub(r'\s+', '', query)
    query = query.split('.')[2]
    command, sep, args = query.partition('(')
    args = args[:-1]
    #print(command, args)
    if command == 'find':
        #print("find")
        find(args)
    elif command == 'count':
        #print("count")
        a_count(args)
    elif command == 'min':
        #print('min')
        a_min(args)
    elif command == 'cartprod':
        #print('cartprod')
        cartprod(args)
    else :
        print("Unrecognized Command")

def printData(data):
    for doc in data:
        for key in doc:
            print( "{0}: {1}".format(key, doc[key]), end=" " )
        print()

def getVals(key):
    data = loadDB(FINAL)
    l = []
    for doc in data:
        if key in doc:
            l.append(doc[key])
    #print(l)
    return l

def find(args):
    #print(args)
    if args == '' or args == "{},{}":
        printData(loadDB(FINAL))
    else:
        sel,proj = getFindArgs(args)
        data = loadDB(FINAL)
        #print( "SELECTION:  {0}, PROJ: {1}".format(sel,proj) )
        while sel:
            currarg = sel.pop(0)
            #print(currarg)
            if currarg != "":
                if currarg.find("=") == -1:
                    currKey = currarg
                    #print(currKey)
                    currVal = None
                    data = getDocs(currKey,currVal,data)
                else:
                    currKey,currVal = currarg.split("=")
                    #print("KEY: {0}, VAL: {1}".format(currKey,currVal) )
                    data = getDocs(currKey,currVal,data)
        #print(data)
        l = project(proj,data)
        printData(l)

def project(arg,data):
    if len(arg) == 0 :
        return data
    elif arg[0] == "" :
        return data
    else :
        l = []
        for doc in data:
            d = {}
            for key in arg:
                if key in doc:
                    d[key] = doc[key]
            l.append(d)
        return l

def getDocs(key,val,data):
    #print("DATA",data)
    l = []
    for doc in data:
        if key in doc:
            if val ==  None:
              l.append(doc)
            #print(key,doc[key],val)
            elif doc[key] == int(val):
                #print("TRUE")
                l.append(doc)
    #print(l)
    return l

def getFindArgs(args):
    sel, proj = args.split("},{")
    sel = sel[1:]
    proj = proj[:-1]
    sel = sel.split(",")
    proj = proj.split(",")
    #print(sel)
    #print(proj)
    return sel,proj

def a_count(args):
    #print(args)
    l = getVals(args)
    if l:
        print(len(l))

def a_min(args):
    #print(args)
    l = getVals(args)
    if l:
        print(min(l))

def cartprod(args):
    #print(args)
    field1, field2 = args.split(',')
    #print(field1, field2)
    l1 = getVals(field1)
    l2 = getVals(field2)
    for i in l1:
        for j in l2:
            print( "{0}: {1} {2}: {3}".format(field1,i,field2,j) )

#main()
