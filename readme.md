### These are codes record for Graduate Research Assistant Job in Mccombs Business School in The University of Texas in Austin

## Author: ##zhenkai(Kay) wang
## Automatic_code Project:
1. This project is done by myself after nearly two months of works. 
2. I re-organized all the previous codes from team into a single program, and trying to combine:
   a. 5 kinds of filters and selectors;
   b. LDA model input data generationa module for both R code/Python code.
   c. LDA model module
   into signle progam. 
3. I create several tool functions collections for reusing.
4. Here is the main program
https://github.com/iamiamn/Documents_Infomation_Extraction_and_Analysis/blob/master/automatic_code/MainProgram_802116.ipynb

## Spider_mentor Project:
Develop crawler using Scarpy to iteratively crawl down table information for Wifi WiMax data

1. [802.11 after 2000](https://mentor.ieee.org/802.11/documents)
file:80211_mentor_1to573.csv, crawled from totally 573 Pages.
2. [802.11 before 2000](http://grouper.ieee.org/groups/802/11/Documents/DocumentArchives/)
file: grouper_1990to1996.csv and grouper_1997to2000.csv
3. [802.16 after 2012](https://mentor.ieee.org/802.16/documents)
file:80216_mentor_1to21.csv, crawled from totally 21 pages.

### Command line
#### open terminal and use Scrapy
scrapy crawl mentor -o 80211_mentor_1to573.csv
#### change the start_urls to 802.16 websiet in spiders1.py
scrapy crawl mentor -o 80211_mentor_1to22.csv
#### then use grouper Spider
scrapy crawl grouperNew -o grouper_1990to1996.csv
scrapy crawl grouper2 -o grouper_1997to2000.csv

## Author Information Extraction Project
Use regular expression to extract author and affiliation in messy data format


## Technical Terms to Frequencey Project
Use pattern matching to extract technical terms in documents, store with pickle library for usage in LDA model



