# Scalable_Product_Duplicate_Detection
Code for scalable product duplicate detection. All software is written in python 3.8 (https://www.python.org/). 

## Project Description 
The purpose of this code is to find duplicate products in web shops. For this purpose we used data from 4 web shops that sell TVs. In order not to have to compare all products with each other, a scalable solution was used. This was done by using Locality Sensitive Hashing (LSH) to find candidate pairs of possible duplicates. We then predicted whether or not these candidate products were duplicates using hierarchical clustering.

## Structure and use of the code
- data: 
  * TVs-all-merged.json
- main_train.py:
run this file to train
- find_best_parameters.py
run this file to obtain the best parameters for testing
 - main_test.py:
run this file to test with the b and threshold obtained from the find best parameters code
- LSH_performance_plots.py
run this file to obtain the performance plots for LSH
- data_preperation.py
  contains functions to clean and prepare the data
- functions.py
  contains functions for scalability
- bootstrap.py
  contain a function to split the data in train and test
- performance.py
  contains functions to evaluate the performance of LSH
- clustering.py
  contains function for the hierarchical clustering
  
 
