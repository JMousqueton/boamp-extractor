#!/usr/bin/python3 
# -*- coding: utf-8 -*-
##################################################
## BOAMP Extractor 
##################################################
## License : MIT 
##################################################
## Author: #JMousqueton (Julien Mousqueton)
## Copyright: Copyright 2022
## Version: 3.x
## Maintainer: #JMousqueton (Julien Mousqueton)
## Email: julien_at_mousqueton.io 
##################################################
# Generic/Built-in 
import boampgetter as boamp
import argparse
from datetime import datetime
from datetime import timedelta

# Other Libs
from configparser import ConfigParser

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

boamp = boamp.boampGetter()
config = ConfigParser(interpolation=None)
config.read('config.cfg')
boamp.DLRed = config.get('Deadline','DeadlineRed')
boamp.DLYellow = config.get('Deadline','DeadlineYellow')
boamp.NewFor = config.get('New','NewFor')
History = config.get('Affichage','Historique')
boamp.Teams = config.get('Notification','Teams')

### MAIN 
keyword = ''
uselist = False

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

DateBegin = datetime.now() - timedelta(days=int(History))
DateBegin = DateBegin.strftime("%Y/%m/%d")

for searchWord in searchList:
    boamp.cptKeyword += 1
    boamp.search(DateBegin,searchWord)
    adList = boamp.extractValidAd()
    for ad in adList:
        boamp.AnalyzeAO(ad,searchWord)   
boamp.makeMarkdown("docs/README.md", rejectList) 
