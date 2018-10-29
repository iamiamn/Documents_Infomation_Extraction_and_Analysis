
# coding: utf-8
# In[1]:
import pickle, re, warnings
import pandas as pd
from fileProcessing import *
start = 5
end = 6
# ## 1. Load the 80211 pickle Data
# In[3]:
# this is a dictionary, with filename as key and content as value
filepath_fulldict_80211 = "./80211Data/full_80211_wl_dict.dat"
data80211 = pickle.load(open(filepath_fulldict_80211, "rb"))
# In[4]:
# In[5]:
keys = list(data80211.keys())
# In[6]:
#take a look at the data
# print("key:\n", keys[0])
#07__ as prefix means this document is the 2007
#11-07-2208-01-000y-802-11y-conditional-sponsor-ballot-report.pdf  is the real file name
# print("content:\n", data80211[keys[0]])
# In[7]:
contents = [v for k,v in data80211.items()]
# In[8]:
#build up a data frame
df80211 = pd.DataFrame()
df80211["Filename"] = keys
df80211["Content"] = contents
# In[9]:
# save as csv output.
# df80211.to_csv("./80211Data/80211mentor_file_content.csv")
# ## 2. fileter for 80211
# In[10]:
author_info_80211 = pd.read_csv("./author_info/80211_mentor_1to573_author_info.csv")
# In[11]:
titles_80211 = author_info_80211["Title"]
downloads_80211 = author_info_80211["Download"]
filenames_80211 = [link.split("/")[-1] for link in downloads_80211]
years_80211 = [int(file[3:5]) for file in filenames_80211]
# In[12]:
#take a look at data
# print(titles_80211.head(),"\n\n")
# print(filenames_80211[:10], "\n\n")
## explanation on the file name:
#11-09-0830-01-0wng-public-easements-for-802-11.ppt is the file name
#039 in 11-09 is the year
# print(years_80211[:10])
# ### 2. 1 change parameters of your filter here
# In[13]:
from toolFunc import isTechFile
filter_words = ["minutes","comment","resolution", "CR", "closing report", "agenda", "press release", "comment resolution", "voting", "ballot", "comments","vote","agenda", "motions"]
start_year = 90 #means 1994, including 94
end_year = 18 # means 2018, including 18
# In[15]:
filepath_techfilecsv_80211 = "./80211Result/80211mentor_tech.csv"
filepath_nontech_80211 = "./80211Result/80211mentor_nontech.csv"
filepath_techfilename_80211 = "./80211Result/80211tech_filenames.pkl"
# #### 2.1.1key words filtering
# In[16]:
t_idxs = []
for i in range(len(titles_80211)):
    if isTechFile(titles_80211[i], filter_words):
        t_idxs.append(i)
print("%d / %d files are considered as technical files"%(len(t_idxs), len(titles_80211)))
# In[17]:
## take a look at the data
num2show = 20
titles_80211[t_idxs[:num2show]]
# #### 2.1.2 year filter
# In[18]:
y_idxs = []
if start_year > 80:
    start_year = start_year - 100
for i in range(len(years_80211)):
    year = years_80211[i]
    if year <= end_year and year >= start_year:
        y_idxs.append(i)
print("%d / %d files are from the choosen years" % ( len(y_idxs), len(years_80211)))
# #### 2.1.3 combine fiter
# In[19]:
idxs = set(y_idxs)
tech_idxs = idxs.intersection(set(t_idxs))
print("%d / %d files are selected" % (len(tech_idxs), len(years_80211)))
# #### 2.2 save filename into 2 csv files under 80211Result folder
# In[20]:
nonTech_idxs = [i for i in range(len(years_80211)) if i not in tech_idxs]
tech_idxs = list(tech_idxs)
# In[21]:
nonTech_80211DF = author_info_80211.iloc[nonTech_idxs]
tech_80211DF = author_info_80211.iloc[tech_idxs]
nonTech_80211DF.to_csv(filepath_nontech_80211)
tech_80211DF.to_csv(filepath_techfilecsv_80211)
filenames_tech_80211 = [filenames_80211[i] for i in tech_idxs]
pickle.dump(filenames_tech_80211, open(filepath_techfilename_80211, "wb"))
# In[22]:
filenames_tech_80211[:10]
# In[23]:
tech_80211DF.head()
# ## 3. key words extraction on the selected files
# In[24]:
filepath_oneGram = "./techTerm/oneGram.csv"
filepath_twoGram = "./techTerm/twoGram.csv"
filepath_threeGram = "./techTerm/threeGram.csv"
oneGram_pkl = "./techTerm/techTerm_oneGram_set.dat"
twoGram_pkl = "./techTerm/techTerm_twoGram_dict.dat"
threeGram_pkl = "./techTerm/techTerm_threeGram_dict.dat"
filepath_AB_80211 = "./80211Result/ab_wl_dict.dat"
filepath_full_80211 = "./80211Result/full_dict.dat"
# ### 3.1 after change the csv file for one tow three grams, run this part of codes to update the dictionary for technical terms
# In[25]:
#generate the tech words and tech words + abbreviation
oneGram = list(pd.read_csv(filepath_oneGram)["words"])
twoGram = [w.strip() for w in pd.read_csv(filepath_twoGram)["words"]]
threeGram = [w.strip() for w in pd.read_csv(filepath_threeGram)["words"]]
oneGramSet = set(oneGram)
twoGramDict= {}
for v in twoGram:
    try:
        k = v.split()[0]
        twoGramDict[k] = v
    except:
        continue
threeGramDict = {}
for v in threeGram:
    try:
        k = v.split()[0]
        threeGramDict[k] = v
    except:
        continue
pickle.dump(oneGramSet, open(oneGram_pkl, "wb"))
pickle.dump(twoGramDict, open(twoGram_pkl, "wb"))
pickle.dump(threeGramDict, open(threeGram_pkl, "wb"))
# In[26]:
from techTermExtraction import *
# In[27]:
#load the file name
filenames_tech_80211 = pickle.load(open(filepath_techfilename_80211, "rb"))
ab_wl_dict, full_wl_dict = ab_extraction(filenames_tech_80211, data80211,0, len(filenames_tech_80211))
#save two file
pickle.dump(ab_wl_dict, open(filepath_AB_80211, "wb"))
pickle.dump(full_wl_dict, open(filepath_full_80211, "wb"))
# ## 3.2 change the paras here: prefix = {"techAB", "AB", "tech"} means use both technical terms and extract all Abbreviation, use only Abbreviation, use only technical terms
# In[29]:
import pickle, re, warnings
import pandas as pd
from techTermExtraction import *
# In[30]:
dictPath = "./Resource/Abb_dict.path"
warnings.filterwarnings("ignore")
#key paras
#    minCount = 1
#    numStart = 0
#    numEnd = 2000
#    prefix = "AB"
domain = "80211"
prefix = ["tech", "AB", "techAB"][2] # 2 means choose techAB
setting = {
    "ab_dict": filepath_AB_80211,
    "full_dict": filepath_full_80211,
    "keyWord": "./" + domain + "Result/" + domain + "_" + prefix
}
# ### 3.3 start generating the input
# In[31]:
ab_wl_dict = pickle.load(open(filepath_AB_80211, "rb"))
full_wl_dict = pickle.load(open(filepath_full_80211, "rb"))
fileNames = full_wl_dict.keys()
# In[32]:
dictAbb1 = getDictOfAbb(dictPath)
oneGram = pickle.load(open(oneGram_pkl, "rb"))
twoGram = pickle.load(open(twoGram_pkl, "rb"))
threeGram = pickle.load(open(threeGram_pkl, "rb"))
# ### 3.4 following is the main code of generating the words:
# #### 1. modify the /Resource/filterCandidiate.xlsx, add new words and mark as 1, save the change
# ####  2. use python run the geneticWordsGenerator.py
# #### 3. run the following cells
# In[34]:
output = []
count = 0
for file in list(fileNames):
    tempOutput = getList(file = file, full_dict = full_wl_dict, oneGram = oneGram, twoGram = twoGram, threeGram = threeGram, abb_all = ab_wl_dict, dictAbb = dictAbb1, pattern = prefix)
    count += 1
    output.append(tempOutput)
    print("processing %d\t / %d" %(count, len(fileNames)), end = "\r")
#    print(len(output[0]))
listOfWordDict = {}
for out in output:
    if (len(out[0]) > 0):
        listOfWordDict[out[1]] = out[0]
print("number of files extracted:", len(output))
pickle.dump(listOfWordDict, open(setting["keyWord"] + "_wl_dict.dat", "wb"))
## repeating
dictPath = "./Resource/Abb_dict.path"
warnings.filterwarnings("ignore")
#key paras
#    minCount = 1
#    numStart = 0
#    numEnd = 2000
#    prefix = "AB"
domain = "80211"
prefix = ["tech", "AB", "techAB"][1] # 2 means choose techAB
setting = {
    "ab_dict": filepath_AB_80211,
    "full_dict": filepath_full_80211,
    "keyWord": "./" + domain + "Result/" + domain + "_" + prefix
}
# ### 3.3 start generating the input
# In[31]:
# In[32]:
# ### 3.4 following is the main code of generating the words:
# #### 1. modify the /Resource/filterCandidiate.xlsx, add new words and mark as 1, save the change
# ####  2. use python run the geneticWordsGenerator.py
# #### 3. run the following cells
# In[34]:
output = []
count = 0
for file in list(fileNames):
    tempOutput = getList(file = file, full_dict = full_wl_dict, oneGram = oneGram, twoGram = twoGram, threeGram = threeGram, abb_all = ab_wl_dict, dictAbb = dictAbb1, pattern = prefix)
    count += 1
    output.append(tempOutput)
    print("processing %d\t / %d" %(count, len(fileNames)), end = "\r")
#    print(len(output[0]))
listOfWordDict = {}
for out in output:
    if (len(out[0]) > 0):
        listOfWordDict[out[1]] = out[0]
print("number of files extracted:", len(output))
pickle.dump(listOfWordDict, open(setting["keyWord"] + "_wl_dict.dat", "wb"))
#repeating
dictPath = "./Resource/Abb_dict.path"
warnings.filterwarnings("ignore")
#key paras
#    minCount = 1
#    numStart = 0
#    numEnd = 2000
#    prefix = "AB"
domain = "80211"
prefix = ["tech", "AB", "techAB"][0] # 2 means choose techAB
setting = {
    "ab_dict": filepath_AB_80211,
    "full_dict": filepath_full_80211,
    "keyWord": "./" + domain + "Result/" + domain + "_" + prefix
}
# ### 3.3 start generating the input
# In[31]:
# In[32]:
# ### 3.4 following is the main code of generating the words:
# #### 1. modify the /Resource/filterCandidiate.xlsx, add new words and mark as 1, save the change
# ####  2. use python run the geneticWordsGenerator.py
# #### 3. run the following cells
# In[34]:
output = []
count = 0
for file in list(fileNames):
    tempOutput = getList(file = file, full_dict = full_wl_dict, oneGram = oneGram, twoGram = twoGram, threeGram = threeGram, abb_all = ab_wl_dict, dictAbb = dictAbb1, pattern = prefix)
    count += 1
    output.append(tempOutput)
    print("processing %d\t / %d" %(count, len(fileNames)), end = "\r")
#    print(len(output[0]))
listOfWordDict = {}
for out in output:
    if (len(out[0]) > 0):
        listOfWordDict[out[1]] = out[0]
print("number of files extracted:", len(output))
pickle.dump(listOfWordDict, open(setting["keyWord"] + "_wl_dict.dat", "wb"))
# In[ ]:
# ### 3.5 save the <filename- wordlist> dictionary into csv files
# In[35]:
from save_lda_input import *
filepath_AB = "./80211Result/80211_AB_wl_dict.dat"
filepath_tech = "./80211Result/80211_tech_wl_dict.dat"
filepath_techAB = "./80211Result/80211_techAB_wl_dict.dat"
filepath_filterwords = "./Resource/wordsNeedToBeFiltered.dat"
# In[36]:
wl_AB = pickle.load(open(filepath_AB, "rb"))
wl_tech = pickle.load(open(filepath_tech, "rb"))
wl_tech_AB = pickle.load(open(filepath_techAB, "rb"))
wordsNeed2Filter = pickle.load(open(filepath_filterwords, "rb"))
# In[37]:
#filter the words
wl_AB = filtering(wl_AB, wordsNeed2Filter)
wl_tech = filtering(wl_tech, wordsNeed2Filter)
wl_tech_AB = filtering(wl_tech_AB, wordsNeed2Filter)
# In[38]:
#check the filter results
check(wl_AB, wordsNeed2Filter)
check(wl_tech, wordsNeed2Filter)
check(wl_tech_AB, wordsNeed2Filter)
#modify the filter file name
file_AB_filtered = "_filtered.".join(filepath_AB.split("."))[9:]
file_tech_filtered = "_filtered.".join(filepath_tech.split("."))[9:]
file_techAB_filtered = "_filtered.".join(filepath_techAB.split("."))[9:]
#write down the dictionary
pickle.dump(wl_AB, open(file_AB_filtered, "wb"))
pickle.dump(wl_tech, open(file_tech_filtered, "wb"))
pickle.dump(wl_tech_AB, open(file_techAB_filtered, "wb"))
#write the result to csv file
# saveAsCSV(wl_AB, "80211_abbr_LDA_inputs.csv")
# saveAsCSV(wl_tech, "80211_tech_LDA_inputs.csv")
# saveAsCSV(wl_tech_AB, "80211_tech_abbr_LDA_inputs.csv")
saveToCSV(file_AB_filtered)
saveToCSV(file_tech_filtered)
saveToCSV(file_techAB_filtered)
#save into previous format for prof anidiya
save_data_csv(filepath_AB, wl_AB)
save_data_csv(filepath_tech, wl_tech)
save_data_csv(filepath_techAB, wl_tech_AB)
# ### 4. run the model, exp: prefix = "AB", start = 5, end = 21,  model will choose the 80211_AB as input, try to run lda models with topic number from 5 to 20(20 = 21-1).
# In[ ]:
from runLDA import *
domain = "80211"
prefix = ["tech", "AB", "techAB"][2]
filepath_wl_dict = "./80211Result/" + domain + "_" + prefix + '_wl_dict_filtered.dat'
for i in range(start, end):
    random.seed(200)
    filepath_html = "./80211LDA/" + prefix + "/" + domain + "_" + prefix + "All_abbr" + str(i) + ".html"
    filepath_csv0 = './80211LDA/'+ prefix + "/" + domain + "_" + prefix + "Abbr_rep_Docs" + str(i) + ".csv"
    filepath_csv1 = './80211LDA/'+ prefix + "/"+ domain + "_" + prefix  +'Abbr_Docs' + str(i) + '.csv'
    filepath_pkl = './80211LDA/'+ prefix + "/" + domain + "_" + prefix  +'Model' + str(i) + '.csv'
    process(filepath_wl_dict, filepath_html, filepath_csv0, filepath_csv1, i, filepath_pkl)
prefix = ["tech", "AB", "techAB"][1]
for i in range(start, end):
    random.seed(200)
    filepath_html = "./80211LDA/" + prefix + "/" + domain + "_" + prefix + "All_abbr" + str(i) + ".html"
    filepath_csv0 = './80211LDA/'+ prefix + "/" + domain + "_" + prefix + "Abbr_rep_Docs" + str(i) + ".csv"
    filepath_csv1 = './80211LDA/'+ prefix + "/"+ domain + "_" + prefix  +'Abbr_Docs' + str(i) + '.csv'
    filepath_pkl = './80211LDA/'+ prefix + "/" + domain + "_" + prefix  +'Model' + str(i) + '.csv'
    process(filepath_wl_dict, filepath_html, filepath_csv0, filepath_csv1, i, filepath_pkl)
prefix = ["tech", "AB", "techAB"][0]
for i in range(start, end):
    random.seed(200)
    filepath_html = "./80211LDA/" + prefix + "/" + domain + "_" + prefix + "All_abbr" + str(i) + ".html"
    filepath_csv0 = './80211LDA/'+ prefix + "/" + domain + "_" + prefix + "Abbr_rep_Docs" + str(i) + ".csv"
    filepath_csv1 = './80211LDA/'+ prefix + "/"+ domain + "_" + prefix  +'Abbr_Docs' + str(i) + '.csv'
    filepath_pkl = './80211LDA/'+ prefix + "/" + domain + "_" + prefix  +'Model' + str(i) + '.csv'
    process(filepath_wl_dict, filepath_html, filepath_csv0, filepath_csv1, i, filepath_pkl)
# In[ ]:
#### this is for 80216, currently uncompleted
# In[ ]:
# ppt80216 = pickle.load(open("./80216Data/80216DOCPPT0to206init_text.dat", "rb"))
# doc80216 = pickle.load(open("./80216Data/80216DOCPPT0to2931init_text.dat", "rb"))
# pdf80216 = pickle.load(open("./80216Data/80216PDF0to8440init_text.dat", "rb"))
# data80216 = pdf80216
# for k, v in ppt80216.items():
#     data80216[k] = v
# for k, v in doc80216.items():
#     data80216[k] = v
# keys_80216 = list(data80216.keys())
# print(len(keys_80216),"files in 80216 completed projects have the content")
# # data80216[keys_80216[0]]
#
#
# # In[ ]:
#
#
# #take a look at the file
# ppt80216Keys = list(ppt80216.keys())
# print("key:\n", ppt80216Keys[0],"\nContent:")
# print(ppt80216[ppt80216Keys[0]])
