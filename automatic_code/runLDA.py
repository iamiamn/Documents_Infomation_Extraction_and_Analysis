
# coding: utf-8

"""
Created on Sat Oct 10  12:33:41 2018

@author: zhenkai wang(Kay)
object: this code is used to a tool function collection for running the LDA and save all the files
"""


import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pickle
import pyLDAvis.gensim
from gensim import corpora, models
import gensim
import os
import pandas as pd
from gensim.models import LdaModel
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import warnings
import random
warnings.filterwarnings('ignore')
from xlrd import open_workbook
# os.environ['MALLET_HOME'] = 'G:\\mallet\\mallet-2.0.8'
# mallet_path = "G:\\mallet\\mallet-2.0.8\\bin\\mallet"


# In[3]:


def read_catagory_completed_project(filename):
    book = open_workbook(filename, on_demand=True)
    catagory_dict = {}
    for name in book.sheet_names():
        sheet = book.sheet_by_name(name)
        for row in range(1, sheet.nrows):
            catagory_dict[sheet.row(row)[9].value] = sheet.row(row)[1].value
    return catagory_dict


# In[5]:


def draw_pie_chart(X, label):
    fig = plt.figure()
    plt.pie(X,labels=labels,autopct='%1.2f%%')
    plt.title("Pie chart")
    plt.show()


# In[6]:


def read_data(filename):
    with open (filename, 'rb') as fp:
        X = pickle.load(fp)
    return X


# In[7]:


def write_data(filename, content):
    with open(filename, 'wb') as fp:
        pickle.dump(content, fp)


# In[8]:


def filter(filename):
    worddic = read_data(filename)
    for file in worddic:
        while 'If' in worddic[file]:
            worddic[file].remove('IEEE')
    return worddic


# In[9]:


def compute_coherence_values(dictionary, corpus, texts, limit, start, step=1):

    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []


    for num_topics in range(start, limit, step):
        model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=dictionary)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        cur_coh = coherencemodel.get_coherence()
        print("%d,%f" %(num_topics, cur_coh))

    return cur_coh, model_list[0]


# In[10]:


def lda_model(word_lst, output, num_topic):
    train  =[]
    for file in word_lst.keys():
        train.append(word_lst[file])

    dictionary = corpora.Dictionary(train)
    corpus = [dictionary.doc2bow(text) for text in train]


#     coh_value, lda_coh = compute_coherence_values(dictionary=dictionary, corpus=corpus, texts=train, start=num_topic, limit=num_topic + 1, step=1)

    lda = gensim.models.ldamodel.LdaModel(corpus, num_topic, id2word = dictionary, passes=10)

    data = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    pyLDAvis.save_html(data, output)
    return corpus, lda


# In[11]:


def format_topics_sentences(ldamodel, corpus, texts=None):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']
    sent_topics_df[['Dominant_Topic']] = sent_topics_df[['Dominant_Topic']].astype(int)

    # Add original text to the end of the output
#     contents = pd.Series(texts)
#     sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)


# In[12]:


def document_representation(lda_model, corpus, filename, catagory=None):
    name_cln = pd.DataFrame({'Document Name': filename})
    if catagory != None:
        catagory_cln = pd.DataFrame({'Catagory' : catagory})
    df_topic_sents_keywords = format_topics_sentences(ldamodel=lda_model, corpus=corpus, texts=None)
    # Format
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords']
    df_dominant_topic = df_dominant_topic.join(name_cln)
    if catagory != None:
        df_dominant_topic = df_dominant_topic.join(catagory_cln)
    # Show
    return df_dominant_topic


# In[13]:


def get_catagory(filenames, overall_catagory_dict):
    catagory_dict = {}
    for filename in filenames:
        catagory_dict[filename] = overall_catagory_dict[filename]
    return catagory_dict


# In[14]:


def save_doc_topics(word_dic, corpus, lda_model, output):
    doc_id = []
    doc_name = []
    topic_id = []
    probability = []
    for idx, file, doc_bow in zip(range(len(word_dic)), word_dic.keys(), corpus):
        doc_lda = lda_model[doc_bow]
        for topic in doc_lda:
            doc_id.append(idx)
            doc_name.append(file)
            topic_id.append(topic[0])
            probability.append(topic[1])
    d = {'Document Id': doc_id, 'Document Name': doc_name, 'Topic ID': topic_id, 'Topic_Perc_Contrib': probability}
    df = pd.DataFrame(data=d)
    df.to_csv(output)


# In[20]:


def process(filename, html_output, df_output, matrix_output, i, pkl_output = None):

    word_dic = read_data(filename)
    corpus, lda = lda_model(word_dic, html_output, i)
#     catagory_dict = get_catagory(word_dic.keys(), overall_catagory_dict)
    print(html_output, " done!")

    df_document = document_representation(lda, corpus, list(word_dic.keys()))
    df_document.to_csv(df_output)
    print(df_output, " done!")

    save_doc_topics(word_dic=word_dic, corpus=corpus, lda_model=lda, output=matrix_output)
    print(matrix_output, " done!")

    #save tuple of result
    result = {i: lda}
    if not pkl_output == None:
        pickle.dump(result, open(pkl_output, "wb"))



# In[25]:


# overall_catagory_dict = read_catagory_completed_project('./802_16_Completed_Projects.xls')
if __name__ == "__main__":
    domain = "80211"
    prefix = ["tech", "AB", "techAB"][2]
    filepath_wl_dict = "./80211Result/" + domain + "_" + prefix + '_wl_dict_filtered.dat'

    start = 7
    # end = 21
    end = 21
    for i in range(start, end):
        random.seed(200)
        filepath_html = "./80211LDA/" + prefix + "/" + domain + "_" + prefix + "All_abbr" + str(i) + ".html"
        filepath_csv0 = './80211LDA/'+ prefix + "/" + domain + "_" + prefix + "Abbr_rep_Docs" + str(i) + ".csv"
        filepath_csv1 = './80211LDA/'+ prefix + "/"+ domain + "_" + prefix  +'Abbr_Docs' + str(i) + '.csv'
        filepath_pkl = './80211LDA/'+ prefix + "/" + domain + "_" + prefix  +'Model' + str(i) + '.csv'
        process(filepath_wl_dict, filepath_html, filepath_csv0, filepath_csv1, i, filepath_pkl)


# In[44]:
