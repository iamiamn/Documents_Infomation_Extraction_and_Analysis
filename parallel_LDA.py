import multiprocessing, warnings
from runLDA import *
warnings.filterwarnings("ignore")
def parallel_process(paras):
    random.seed(200)
    filepath_wl_dict, filepath_html, filepath_csv0, filepath_csv1,filepath_pkl, topic_num = paras
    process(filepath_wl_dict, filepath_html, filepath_csv0, filepath_csv1, topic_num, filepath_pkl)

if __name__ == "__main__":
    np = 3 #number of processer you want to use
    domain = "80216"# you can change it to 80211
    prefix = ["tech", "AB", "techAB"][1] #we can change it into 0, 1, 2 
    start = 2
    end = 5
    
    
    filepath_wl_dict = "./" + domain + "Result/" + domain + "_" + prefix + '_wl_dict_filtered.dat'
    parasList = []
    #generating the paras
    filepath_prefix = "./" + domain + "LDA/" + prefix + "/" + domain + "_" + prefix
    for i in range(start, end):

        filepath_html = filepath_prefix + "All_abbr" + str(i) + ".html"
        filepath_csv0 = filepath_prefix + "Abbr_rep_Docs" + str(i) + ".csv"
        filepath_csv1 = filepath_prefix +'Abbr_Docs' + str(i) + '.csv'
        filepath_pkl = filepath_prefix +'Model' + str(i) + '.csv'
        parasList.append([filepath_wl_dict, filepath_html, filepath_csv0, filepath_csv1, filepath_pkl, i])
    
    p = multiprocessing.Pool(np)
    output = p.map(parallel_process, parasList)
