# -*- coding: utf-8 -*-

"""
Created on Sat Oct 22 13:33:21 2018

@author: zhenkai wang(Kay)
object: this code is used to a tool function collection for extracting all the technical terms
"""
#import fitz
import re, os, pickle, multiprocessing
#import nltk
from nltk import word_tokenize, pos_tag, ne_chunk, chunk
from nltk.corpus import treebank
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from functools import partial
import warnings
import pandas as pd

def getStopWords():
# =============================================================================
#     #we return the stopWords in NLTK database
# =============================================================================
    return set(stopwords.words('english'))

def transform(word):
# =============================================================================
#     if a word is all upper case then return itself otherwise should return word lower case
# =============================================================================
    isAllUpper = (word == word.upper())
    if isAllUpper:
        pass
    else:
        word = word.lower()
    return word

from nltk.corpus import words
english = words.words()
english = [word.lower() for word in english]
def getTechTerms(words, oneGram, twoGram, threeGram, extractedAbb, pattern = "AB"):
    global english
# =============================================================================
#     #given a list of words from a doc, and a list of tecnical terms, find all occurance of technical word
# =============================================================================
#    p1Match = r'^([A-Z]{2,})$'
#    p2Contain = r'802'
    result = []
    wordNum = len(words)
    if ("tech" in pattern):
        for i in range(wordNum):
            word = words[i]

            #oneGram
            if (word in oneGram):
                result.append(word)
            #twoGram
            if (word in twoGram and i < wordNum - 1 and (word + " " + words[i + 1]) == twoGram[word]):
                result.append(twoGram[word])

            #threeGram
            if (word in threeGram and i < wordNum - 2 and (word + " " + words[i + 1] + " " + words[i + 2]) == threeGram[word]):
                result.append(threeGram[word])

    #delete stopword
    stopWords = getStopWords()
    wordsFiltered = []
    for w in result:
        if w not in stopWords:
            wordsFiltered.append(w)
    appendList = []
    if ("AB" in pattern):
        if (len(extractedAbb) > 0):
            for word in extractedAbb:
                #prevent double adding abb
                if not (word in wordsFiltered):
                    appendList.append(word)#should not use wordsFilteredList.append, or it will only record one
#        else:
#            setFilterd = set(wordsFiltered)
#            for word in words:
#                if (word not in setFilterd and word.isalpha() and len(word)> 1):
#                    if not isAbbrev(word) and word.lower() not in english:
#                        appendList.append(word)
    finalResult = wordsFiltered + appendList
    finalResult = filterFunc(finalResult)
#     print("num of technical terms got\t %d" % (len(finalResult)))
    return finalResult

def notInWords(word):
    for pott in words_tec:
        if word in pott:
            return False
    return True




# from pptx import Presentation
# import docx2txt
# def getContent(textPath):
# # =============================================================================
# # #    input is the path of pdf file, return all of the words(segemented by \s \n)
# # #    remove all punctuation
# # =============================================================================
#     words = []
# #    if (textPath.endswith(".pdf")):
# #
# #        content = getPage(textPath)
# #        text1 = '.'.join(content)
# #
# #        #words = nltk.word_tokenize(text1)
# #        sents = sent_tokenize(text1)
# #        #delete punctuation
# #        for sent in sents:
# #            ws = [word.strip(string.punctuation) for word in re.split(r'\s|\n', sent)]
# #            ws = [w for w in ws if len(w) > 1]
# #            words += ws
#     if textPath.endswith(".docx") or textPath.endswith(".doc"):
#         if textPath.endswith(".doc"):
#             textPath = textPath.replace(".doc", ".docx")
#         text = docx2txt.process(textPath)
#         sents = re.split("\\n+|\\t+|\.+", text)
#         for sent in sents:
#             if (sent is None ): continue
#             ws =  [word.strip(string.punctuation) for word in re.split(r'\s|\n', sent)]
#             ws = [w for w in ws if len(w) > 1]
#             words+=ws
#     if textPath.endswith(".pptx") or textPath.endswith(".ppt"):
#         if textPath.endswith(".ppt"):
#             	textPath = textPath.replace(".ppt", ".pptx")
#         #python pptx  is good at extracting content in pptx, but ppt is not ok
#         sents = []
#         prs = Presentation(textPath)
#         for slide in prs.slides:
#             for shape in slide.shapes:
#                 if not shape.has_text_frame:
#                     continue
#                 for paragraph in shape.text_frame.paragraphs:
#                     for run in paragraph.runs:
#                         sents.append(run.text)
#         for sent in sents:
#             ws =  [word.strip(string.punctuation) for word in re.split(r'\s|\n', sent)]
#             ws = [w for w in ws if len(w) > 1]
#             words += ws
#     #delete stopword
# #     stopWords = set(stopwords.words('english'))
# #     wordsFiltered = []
# #     for w in words:
# #        if w not in stopWords:
# #            wordsFiltered.append(w)

#     wordsFiltered = [lowerlize(word) for word in words]
#     wordsFiltered = [word for word in wordsFiltered if word is not None]
#     return wordsFiltered
def lowerlize(word):
    try:

        if (word[0].isupper() and word != word.upper()):
            return word.lower()
        else:
            return word
    except:
        return None



def getList(file, full_dict, oneGram, twoGram, threeGram, abb_all, dictAbb, pattern = "AB"):
# =============================================================================
#     #get a list of word lists, each element is the word extracted from file from files
#     #replace all the words  that occurring in key set of dictAbb by corresponding full titles
# =============================================================================

#    wordsFiltered = getContent(os.path.join(fileDir, file))
    wordsFiltered = full_dict.get(file, None)
    if wordsFiltered is None:
        techTerms = []
    else:
        techTerms = getTechTerms(wordsFiltered.split(), oneGram, twoGram, threeGram, abb_all.get(file, []), pattern)
    #here try to match the full title and abbreviation

    for i in range(len(techTerms)):
        abb = techTerms[i]
        fullTitle = dictAbb.get(abb, None)
        if fullTitle is not None:
            techTerms[i] = fullTitle
#                    print("changeing ", abb, " \t to ", fullTitle)

    return (techTerms, file)


def getDictOfAbb(*paths):
# =============================================================================
#     #this file is a list of list, each of the sublist contains two string, first one is abbreviation, second one is full title
#     #make it into a dictionary
# =============================================================================
    dictAbb = {}
    for path in paths:
        with open(path, 'rb') as fp:
            l = pickle.load(fp)
#     for key, value in dictAbb.iteritems():
    for i in range(len(l)):
        dictAbb[l[i][0]] = l[i][1].lower()

    return dictAbb
def filterFunc(l):
    global filterList
    wl=[w for w in l if len(w) > 1 and not w in filterList]
    return wl
def updateFilterWords():
    df = pd.read_excel("./Resource/filterCandidiate.xlsx", index_col = None, header = None)
    allWords =list(set(df[0]))
    words = []
    #filter out null
    for w in allWords:
        try:
            if len(w)>1:
                words.append(w)
        except:
            continue
    len(words)
    wordsNeed2Filter = [df[0][i] for i in range(len(df[0])) if df[1][i] == 1 ]
    wordsNeed2Filter += ["IEEE", "ON", "DOWN", "THIS", "THAT"]
    wordsNeed2Filter += [chr(i) for i in range(97,123)]
    wordsNeed2Filter += [chr(i) for i in range(65, 91)]
    wordsNeed2Filter = set(wordsNeed2Filter)
    pickle.dump(wordsNeed2Filter, open("wordsNeedToBeFiltered.dat", "wb"))
