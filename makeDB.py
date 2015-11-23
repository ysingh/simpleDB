#---------------------------------------- makeDB.py ------------------------------------------------#
# makedb.py reads a file containing data. The data in the file consists of documents, one per line. #      
# Each document is a number of key: value pairs. Here it is assumed that all values are integers.   #
# makedb.py reads such a file and stores each document as a python dictionary.                      #
# The entire database is stored as a list of such dictionaries in binary form.                      #
#                                       USAGE                                                       #
# import makeDB.py then use writeDB(inFile, out) to write the database and store it to disk         #
# inFile - the data file.                                                                           #
# out - the binary file representing the database                                                   #
# to load the database into a list use l = loadDB(dbfile)                                           #            
# Where dbfile is the file containing the binary representation of the database, this is the        #
# same file as the out argument to writeDB(inFile, out)                                             #
#---------------------------------------------------------------------------------------------------#

import pickle

def readData(dataFile):
    with open(dataFile, 'r') as f:
        l = []
        for line in f:
            w = []
            for word in line.split():
                if word.endswith(':'):
                    word = word[:-1]
                w.append(word)
            l.append(w)
        return l

def dictify(dataFile):
    l = readData(dataFile)
    n = []
    j = 1
    for line in l:
        i = iter(line)
        b = dict(zip(i,i))
        b['ID'] = j
        j += 1
        n.append(b)
    #convert all values for all key, value pairs in every dictionary to an integer
    for dct in n:
        for key in dct:
            dct[key] = int(dct[key])
    return n

def writeDB(inFile, out):
    l = dictify(inFile)
    with open(out, "wb") as f:
        pickle.dump(l, f , -1)

def loadDB(dbfile):
    with open(dbfile, "rb") as f:
        l = pickle.load(f)
    return l
  
#For Testing
#def main():
#   writeDB("data.txt", "final")
#    with open("final", "rb") as f:
#        n = pickle.load(f)
#    n = loadDB("final")
#    print(n)
#    for line in n:
#        print(line)

#main()
