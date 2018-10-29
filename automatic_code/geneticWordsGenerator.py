import pickle, re
import pandas as pd
if __name__ == "__main__":
        ### filter step: open "filterCandidiate.xlsx", mark  1 in the second column if you don't want to consider the word in document,
    filepath_excel = "./Resource/filterCandidiate.xlsx"
    filepath_pkl = "./Resource/wordsNeedToBeFiltered.dat"

    df = pd.read_excel(filepath_excel, index_col = None, header = None)


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

    # writeToXlsx(words, "filterCandidiate.xlsx")

    #open the file again and collect all the words that need to be filtered
    # df = pd.read_excel("filterCandidiate.xlsx", index_col = None, header = None)
    wordsNeed2Filter = [df[0][i] for i in range(len(df[0])) if df[1][i] == 1 ]
    wordsNeed2Filter += ["IEEE", "ON", "DOWN", "THIS", "THAT"]
    wordsNeed2Filter = set(wordsNeed2Filter)

    wordsNeed2Filter

    pickle.dump(wordsNeed2Filter, open(filepath_pkl, "wb"))
