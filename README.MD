## Automatic Code for LDAModel in 80211/80216 WIFI/WIMAX Technology Trends Analysis Program
This package of codes is used for processing the technical files in 80211 mentor and 80216 completed projects.

### Date collection:
We use python library to extract the content from diffrent kinds of files, including pdf, ppt, pptx, doc, docx, and build up a <filename- content> dictionary for preprocessing.

### File filter:
Here I set up 5 kinds of filters:
   a. file name filter: change the filter word list in part2.1
   b. year filter: change the year period in part 2.1
   c. genetic words filter: modified ./Resource/filterCandidates.xlsx, add new words and mark them as one. "updateFilterWord" function will automatically recognize and use updated genetic word list for filtering
   d. technical terms selector: change csv files under ./techTerm folder, and those words will be used to match and extract techterms in the content.
   e. Abbreviation selector: In fileProcessing.py, the function "ab_extraction" is responsible on extract the abbreviation of the content. You can change the rule and find what you consider are Abbreviations.

### Input generation:
 After finishing your change in the filters, you can run 3.2-3.4 with different prefixs to generate the input for LDA models.
   a. For python version of LDA running, in ./80211Results and ./80216Results folders, the pkl/dat files with "filtered" in their names are the input for python code.
   b. For R version, all the csv files in ./80211Results and ./80216Results folders are the input for R code. For csv files with "previous format" in their names, each rows is a file, first column is file name, second column is a word list.For csv files without "previous format" in their names, each row contains three columns. They are file, word, word frequency of this word in this file

### LDA model:
 In part 4 in MainProgram_802116.ipynb and MainProgram.ipynb, we have the codes for running LDA model with different topic number parallely. I also write an individual code for parallel running LDA model, "parallel_LDA.py"


## Following are the user instractions for MainProgram.ipynb (same for MainProgram_802116.ipynb)

1. No.2 part is filter

2. try to modify the cell right behind the title of "2.1 change parameters          
    of your filter here". you can choose the year, add more filename filter words.

3. part 2.2 is try to save the result into 2 files. one csv file contains all the author info record of techical documents, the other contains all the author info record of non-technical documents

4. after runing part 2, we filter out all the non-technical documents.

5. part 3 is going to do key word extraction.

6. part 3.1, before running the cell 3.1, you can modify the techterm   	csv. they are under /techTerm folder, we just add and remove key   	words in csv file, the code will read your change and make new dictionary. Here you can also add genetic words and marked them as 1 in this file: /Resource/filterCandidate.xls,

7. part 3.2, Here you can change the prefix (you can choose one of the three options, AB:only abbreviation, tech: only technical terms, techAB: both) and try to generate different extracted word list of the documents.Exp: choose "AB", code will try to generate the input whose word list are all the abbreviation in the documents.

8. part 3.3 get all the data ready, here we will also update our genetic words list. Before running this, make sure you change the ./Resource/filterCandidate.xlsx file if you want to add genetic word.

9. part 3.4, once you choose a prefix in 3.2, run 3.3 then 3.4, it will generate the data for this prefix.

10. part 3.5 save the extracted word results.

11. part 4, change the start,end, prefix, you can run the model. all the visualization result will be stored at /80211LDA folder

12. In order to provide correct result. In part 3.2, choose every option of prefix and run 3.2 then 3.3 then 3.4. choose second option of prefix, run 3.2 3.3 3.4 again. choose another option of prefix, run 3.2 3.3 3.4 again.
after that run 3.5, generate all the input csvs that R code needs.
then you can run part 4 with different starts and ends

13. above instructions are for 80211
run MainProgram_802116.ipynb, same principle as 80211 one
