# -*- coding: utf-8 -*-

"""
Created on Sat Ocy 28 16:33:32 2018

@author: zhenkai wang(Kay)
object: this code is used to a tool function collection for filtering out non technical documents
"""
import pickle, re
import numpy as np
import pandas as pd
fileNameFilterKeyWords = ["minutes","comment","resolution", "CR", "closing report", "agenda", "press release", "comment resolution", "voting", "ballot", "comments","vote","agenda", "motions"]

def isTechFile(title, filterWords = fileNameFilterKeyWords):
    filterKeyWords = set([w.lower() for w in fileNameFilterKeyWords])
    #input the title, return whether the title is a technical document title
    try:
        title = title.lower()
        split1 = re.split("\(|\)|\s+|-", title)
        split2 = []
        for i in range(len(split1) - 1):
            split2.append(split1[i] + " " + split1[i + 1])
        split = split1 + split2
        for w in split:
            if w in filterKeyWords:
                return False
    except:
        print(str(title) + "\t is not a technical files")
    return True
