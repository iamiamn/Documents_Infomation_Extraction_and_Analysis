1. No.2 part is filter 

2. try to modify the cell right behind the title of "2.1 change parameters          
    of your filter here". you can choose the year, add more filename filter words. 

3. part 2.2 is try to save the result into 2 files. one csv file contains all the author info record of techical documents, the other contains all the author info record of non-technical documents

4. after runing part 2, we filter out all the non-technical documents.

5. part 3 is going to do key word extraction. 

6. part 3.1, before running the cell 3.1, you can modify the techterm   	csv. they are under /techTerm folder, we just add and remove key   	words in csv file, the code will read your change and make new dictionary. Here you can also add genetic words and marked them as 1 in this file: /Resource/filterCandidate.xls, 

7. part 3.2, Here you can change the prefix (you can choose one of the three options, AB:only abbreviation, tech: only technical terms, techAB: both) and try to generate different extracted word list of the documents.Exp: choose "AB", code will try to generate the input whose word list are all the abbreviation in the documents.

8. part 3.3 get all the data ready

9. part 3.4, once you choose a prefix in 3.2, run 3.3 then 3.4, it will generate the data for this prefix.

10 part 3.5 save the extracted word results.

11 part 4, change the start,end, prefix, you can run the model. all the visualization result will be stored at /80211LDA folder

12 In order to provide correct result. In part 3.2, choose every option of prefix and run 3.2 then 3.3 then 3.4. choose second option of prefix, run 3.2 3.3 3.4 again. choose another option of prefix, run 3.2 3.3 3.4 again.
after that run 3.5, generate all the input csvs that R code needs.
then you can run part 4 with different starts and ends