# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 23:14:18 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 21:47:49 2018

@author: Zhenkai Wang
"""
#this code is used for extracting 

#this code is to use pattern matching and dictionary matching to find out the all the technical terms in documents
import fitz, re, os, pickle, multiprocessing
#import nltk
from nltk import word_tokenize, pos_tag, ne_chunk, chunk
from nltk.corpus import treebank
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from functools import partial
numCount = 0
path1 = "F:\\WireLessNLPGRA\\code\\NamedEntityRecognition\\some_proposal\\C802162a-01_01.pdf"
path2 = "F:\\WireLessNLPGRA\\code\\NamedEntityRecognition\\some_proposal\\C802162a-01_06.pdf"
techTermPath1 = "word_list1"
techTermPath2 = "word_list2"
techTermPath3 = "word_list3"
techTermPath4 = "word_list4"
pdfDir =  "F:\\WireLessNLPGRA\\80216CompProj"


def getPage(path):
    #get all the pages of file, return a list of string, each string is content of one page
    doc = fitz.open(path)
    content = []
    for i in range(doc.pageCount):
        content.append(doc.getPageText(i))
    return content
def abstractExtracter(firstPage):
    #extract abstract of the first page
    pAbstract = r'^Abstract\s(.+)'
    candidate = [re.findall(pAbstract,line) for line in firstPage.split('\n')]
    abstract = []
    for sen in candidate:
        if (len(sen) > 0):
            abstract.append(sen[0])
    return abstract[0]
def getStopWords():
    return set(stopwords.words('english'))
def transform(word):
    isAllUpper = (word == word.upper())
    if isAllUpper:
        pass
    else:
        word = word.lower()
    return word

def getTechTerms(words, listOfTechTerm):
    #given a list of words, and a list of tecnical terms, find all occurance of technical word
    p1Match = r'^([A-Z]{2,})$'
    p2Contain = r'802'

    result = []
    wordNum = len(words)
    for i in range(wordNum):
        word = words[i]
#        word = transform(word)
        #if (word in listOfTechTerm):#since they are all lowercase in listOfTechTerm
        #    result.append(word)
        isTerm = False
        for term in listOfTechTerm:
            #correct match
            if word == term:
                isTerm = True
            splited_terms = term.split()
            
            if len(splited_terms) > 1:
                isEqual = True
                for idx in range(len(splited_terms)):
                    if (i + idx > wordNum - 1):
                        break
                    if (words[i + idx] != splited_terms[idx]):
                        isEqual = False
                if (isEqual):
                    result.append(term)       
                
            
            
                
                
        if (isTerm):
            result.append(word)
#        elif (len(word) > 1):
#            p1Result = re.match(p1Match, word)#all uppercase
#            p2Result = re.findall(p2Contain, word)#contains 802.
#            p3Result = hasCharDig(word)#contains at least one char and digit
#            p4Result = re.findall('http', word)
#            #print(word, " ", p1Result, " ", p2Result)
#            if (p1Result is not None ) or len(p2Result) > 0 or p3Result:
#                if len(p4Result) == 0:
#                    result.append(word)
    #delete stopword
    stopWords = getStopWords()
    wordsFiltered = [] 
    for w in result:
        if w not in stopWords:
            wordsFiltered.append(w)
    return wordsFiltered
def hasCharDig(word):

    hasChar = False
    hasWord = False
    for i in range(len(word)):
        c = word[i]
        if(c.isdigit()):
            hasChar = True
        if(c.isalpha()):
            hasWord = True
    return hasChar & hasWord
def getListOfTechTerms(dictAbb, *paths):
    
    try:
        with open("techTerms.dat", "rb") as f:
            technicalWords = pickle.load(f)
    except:
        technicalWords = []
        for path in paths:
            with open (path, 'rb') as fp:
                technicalWords += pickle.load(fp)
        for k, v in dictAbb.items():
            technicalWords.append(k)
            technicalWords.append(v)
        temp = list(set(technicalWords))
        technicalWords = []
        for word in temp:
            if (len(word) > 1):
                technicalWords.append(word)
        with open("techTerms.dat", "wb") as f:
            pickle.dump(technicalWords, f)
    return technicalWords

def getContent(textPath):
    content = getPage(textPath)
    text1 = '.'.join(content)

    #words = nltk.word_tokenize(text1)
    sents = sent_tokenize(text1)
    words = []
    #delete punctuation
    for sent in sents:
        words += [word.strip(string.punctuation) for word in re.split(r'\s|\n', sent)]
    #delete stopword
#     stopWords = set(stopwords.words('english'))
#     wordsFiltered = [] 
#     for w in words:
#        if w not in stopWords:
#            wordsFiltered.append(w)

    wordsFiltered = words
    return wordsFiltered

def wordListToFreqDict(wordList):
    wordFreq = [wordList.count(p) for p in wordList]
    return dict(zip(wordList, wordFreq))

def getFreqDict(filePath, listOfTechTerms):
    wordsFiltered = getContent(filePath)
    #print(wordsFiltered)
    
    #listOfTechTerms.append("Recommended Practice")#just a test
    potentialTechTerms = getTechTerms(wordsFiltered, listOfTechTerms)
#    print(potentialTechTerms)
    wordFreqDict = wordListToFreqDict(potentialTechTerms)
    return wordFreqDict
def getAllFiles(dirPath):
#    print(os.listdir(dirPath))
    files = [os.path.join(dirPath, f) for f in os.listdir(dirPath)]
    
    files = list(filter(lambda f: f.endswith(('.pdf', '. PDF')), files))
    print("total number of pdf files under directory: ", len(files))
    goodFiles = []
    for file in files:
        try:
            doc = fitz.open(file)
        except:
            pass
        else:
            goodFiles.append(file)
    print("good file num: ",len(goodFiles))
    return goodFiles

def getAllDicts(files, listOfTechTerms, numFile):
    
    listOfDicts = []
    count = 0
    for file in files:
        try:
            print(count, "\t: ", file)
            listOfDicts.append(getFreqDict(file, listOfTechTerms))
            count += 1
        except:
            pass
        if (count >= numFile):
            break
                
    return listOfDicts

def getList(file, listOfTechTerms, dictAbb):
    global numCount
    listOfWords = []
    
    try:
        wordsFiltered = getContent(file)
        techTerms = getTechTerms(wordsFiltered, listOfTechTerms)
        for i in range(len(techTerms)):
            abb = techTerms[i]
            fullTitle = dictAbb.get(abb, None)
            if fullTitle is not None:
                techTerms[i] = fullTitle
#                    print("changeing ", abb, " \t to ", fullTitle)
            listOfWords.append(techTerms)
        print(numCount, "\t", file)
        numCount += 1
            #here delete the duplicate one
    except:
        pass
    return listOfWords


def getDictOfAbb(*paths):
    #this file is a list of list, each of the sublist contains two string, first one is abbreviation, second one is full title
    #make it into a dictionary
    dictAbb = {}
    for path in paths:
        with open(path, 'rb') as fp:
            l = pickle.load(fp)
#     for key, value in dictAbb.iteritems():
    for i in range(len(l)):
        dictAbb[l[i][0]] = l[i][1].lower()
        
    return dictAbb
from itertools import product
if __name__ == "__main__":
    #prepocessing
    dictAbb1 = getDictOfAbb(techTermPath2, techTermPath3)
    listOfTechTerms1 = getListOfTechTerms(dictAbb1, techTermPath1, techTermPath4)#here it can take as much doc as possible
    print("finish loading")
    #get all the files
    numFile = 200
    minCount = 5
    fileNames = getAllFiles(pdfDir)[:numFile];
    np = 16
    p = multiprocessing.Pool(np)
    output = p.map(partial(getList, listOfTechTerms = listOfTechTerms1, dictAbb = dictAbb1),  [file for file in fileNames])
#    print(len(output[0]))
    listOfWordLists = []
    for out in output:
        if (len(out) > 0):
            listOfWordLists.append(out[0])
    pickle.dump(listOfWordLists, open("listOfWOrdLists.dat", "wb"))
    vec = CountVectorizer(min_df = minCount,tokenizer=lambda doc: doc, lowercase=False)
    wordFreqArray = vec.fit_transform(listOfWordLists)
#    listOfDicts = getAllDicts(fileNames, listOfTechTerms, numFile)
#    vec = DictVectorizer()
#    wordFreqArray = vec.fit_transform(listOfDicts)
    featureName = vec.get_feature_names()
#    print(wordFreqArray)
#    print(featureName)
    keyWord = "_minDf_5"
    pickle.dump(fileNames, open(keyWord + "fileNames.dat", "wb"))
    pickle.dump(wordFreqArray, open(keyWord + "wordFreqArray.dat", "wb"))
    pickle.dump(featureName, open(keyWord + "featureName.dat", "wb"))
    
    
    
    
    
    
    