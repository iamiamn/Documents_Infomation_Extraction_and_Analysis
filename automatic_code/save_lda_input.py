import pickle, re, os
import pandas as pd
def filtering(wl_dict, filters):
    new_wl_dict = {}
    for file, wl in wl_dict.items():
        new_wl_dict[file] = [w for w in wl if w not in filters]
    return new_wl_dict
def check(wl_dict, filters):
    #see if the filters word still in there
    for file, wl in wl_dict.items():
        for w in wl:
            if w in filters:
                print(file, w)
                #use dataframe to save
#file = "80211_techAB_wl_dict.dat"
def saveToCSV(file, savefile = None):
    if (savefile == None):
        prefix = file.split("_")[0] +"_" + file.split("_")[1] + "_"
        savefile = prefix + 'LDA_input.csv'

    with open (file, 'rb') as fp:
        abbr_file_lst = pickle.load(fp)
#     print(len(abbr_file_lst))
    #create dict
    abbr_file_freq_dic = {}
    for file in abbr_file_lst:
        freq_dic = {}
        for word in abbr_file_lst[file]:
            if word in freq_dic:
                freq_dic[word] += 1
            else:
                freq_dic[word] = 1
        abbr_file_freq_dic[file] = freq_dic
    #create result
    result = []
    for file in abbr_file_freq_dic:
        for word in abbr_file_freq_dic[file]:
            result.append([file, word, abbr_file_freq_dic[file][word]])
#     print(len(result))

    data = pd.DataFrame(result)
    data.columns = ["Filenames", "Word", "Frequency"]
#     try:
#         data.columns = ['Filename', 'Word', 'Frequency']
#     except:
#         print("can't get save")
#         print(result)
    data.to_csv(savefile, mode = 'w', index=False)
def save_data_csv(filename, word_dic):
    dataframe = pd.DataFrame({'Filename':list(word_dic.keys()), 'WordList':list(word_dic.values())})
    splitted = filename.split("_")
    output = splitted[0] + "_" + splitted[1] + "_previous_format.csv"

    dataframe.to_csv(output)
