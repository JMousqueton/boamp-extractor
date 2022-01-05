import boampgetter as boamp
import argparse

def getWordList(fileNme):
    """Return list of line writen in file and skip '\n' '\r'
    """
    read = ''
    with open(fileNme, 'r') as fichier:
        read = fichier.read()
    read = read.replace('\n',';')
    read = read.replace('\r',';')
    read = read.replace(';;',';')
    
    lineOut = []
    for line in read.split(';'):
        if line != '':
            lineOut.append(line)
    return lineOut
   

### MAIN 
keyword = ''
uselist = False


boamp = boamp.boampGetter()
boamp.printAll = 0
outputfile='annonces.txt'
parser = argparse.ArgumentParser()
parser.version = '1.0'
parser.add_argument('-d','--debug', action='store_true',help='increase output verbosity')
parser.add_argument('-k','--keyword', action='store', type=str, metavar='<keyword>', dest='keyword', help='the keyword')
args = parser.parse_args()

if args.debug:
    boamp.printAll = True


if args.keyword:
    searchList = [args.keyword]
    rejectList = []
else: 
    searchList = getWordList('keywords.txt')
    try:
        rejectList = boamp.getWordList('exception.txt')
    except:
        rejectList = []

for searchWord in searchList:
	boamp.search('2021/11/01',searchWord)
	adList = boamp.extractValidAd()
	for ad in adList:
		boamp.pushAd(ad)

boamp.makeMarkdown("docs/README.md", rejectList) 

