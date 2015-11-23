from  makeDB import writeDB, loadDB
from queries import parse, readFile

def main():
    FINAL = "final"
    printWelcome()
    data = input("Enter the location of the data file: ")
    writeDB(data,FINAL)
    print("Database written.")
    query = " "
    while query != "":
        query = input("Enter query: ")
        if query == 'r':
            q = input("Enter location of query file: ")
            readFile(q)
        elif query != "":
            parse(query)

def printWelcome():
    print("-------------------------------------------------------")
    print("----------- Welcome to SmallDB - NOSQL Database -------")
    print()
    print("            Enter an empty query to quit.              ")
    print("            Type r to load a query file                ")
    print()

main()
