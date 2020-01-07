# MAIN INDEXER MODULE

import json
import os

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from urllib.parse import urldefrag
from bs4 import BeautifulSoup
from collections import defaultdict
from openfiles import open_a_file
from mytokenizer import tokenizer1,tokenizer2,computeWordFrequencies,positionTokenizer,calcTF
from merger import merge_main
from tfidfcalc import weighted_tfidf_normal, weighted_tfidf_important
from makepositionsdict import make_positions

"""
This index builder uses BS4 and NLTK for tokenization
    loop will initialize the reverse index and the urldictionary
    and run through all the listed directories in the specified
    original path
"""
ORIGINAL_PATH = "/home/lopes/Datasets/IR/DEV/"
# ORIGINAL_PATH = "C:\\Users\\coolc\\PycharmProjects\\CS121Project3\\DEV\\"
# ORIGINAL_PATH = "C:\\Users\\Christian\\PycharmProjects\\cs121proj3final\\DEV\\"


def sort_and_write(reverse_index, count,name):
    file_name = name+str(count)+".txt"
    # file_binary = name+"binary"+str(count)
    with open(file_name,"w") as file:
        for k, v in sorted(reverse_index.items(), key=lambda t: t[0]):
            try:
                file.write(k+":"+ str(v)+"\n")

            except:
                continue

def start_index():

    reverse_index = defaultdict(list)
    reverse_index_important = defaultdict(list)
    num_of_documents = 0

    for current_directory in os.listdir(ORIGINAL_PATH):
        print("Counting Documents--Currently in:",current_directory)
        for file in os.listdir(ORIGINAL_PATH+current_directory):
            num_of_documents+=1
    split_every = num_of_documents//10  #10 partial indexes
    if(num_of_documents < 10):
        split_every = 1
    print(num_of_documents)
    print(split_every)
    # a = input() #FOR DEBUG



    url_dict = dict()
    count = 1
    current_doc_id = 1;
    total = 1
    for current_directory in os.listdir(ORIGINAL_PATH):
        print("Working--Currently in:",current_directory)
        for file in os.listdir(ORIGINAL_PATH+current_directory):
            path = ORIGINAL_PATH + current_directory + "/" + file
            # path = ORIGINAL_PATH + current_directory + "\\" + file
            data = open_a_file(path)
            data_dict = eval(data)
            if (data_dict["encoding"] != "utf-8" and data_dict["encoding"]!="ascii"):
                print("Skipped, NOT UTF-8 was:",data_dict["encoding"])
                total+=1
                continue


            if urldefrag(data_dict["url"])[0] in url_dict: # only skip fragments when we have already read the info from the url
                total += 1
                print("fragment already in dictionary skipped")
                continue
            if data_dict["url"] in url_dict: #skip possible repeats
                total += 1
                continue

            print("\t\tPage #",current_doc_id, "Total",total,"File",file,":", data_dict["url"])

            url_dict[urldefrag(data_dict["url"])[0]] = current_doc_id


            # BeautifulSoup method https://stackoverflow.com/a/24618186
            soup = BeautifulSoup(data_dict["content"], features="html.parser")


            tokenized_normal, tokenized_important = tokenizer1(soup)    #works on openlab


            normal = tokenizer2(tokenized_normal)
            important = tokenizer2(tokenized_important)   #not used


            final_normal = computeWordFrequencies(normal)
            final_important = computeWordFrequencies(important)   #not used

            for term in final_normal:
                if term in reverse_index:
                    reverse_index[term] += [(current_doc_id,final_normal[term])]
                else:
                    reverse_index[term] = [(current_doc_id,final_normal[term])]
            for term in final_important:      #not used
                if term in reverse_index_important:
                    reverse_index_important[term] += [(current_doc_id,final_important[term])]
                else:
                    reverse_index_important[term] = [(current_doc_id,final_important[term])]



            current_doc_id +=1
            total+=1

            if(current_doc_id % split_every == 0):
                print("Offloading partial index")
                sort_and_write(reverse_index, count, "partialindex")
                sort_and_write(reverse_index, count, "importantwords")
                # sort_and_write(reverse_index, count, "urls")
                reverse_index = defaultdict(list)
                count +=1

    sort_and_write(reverse_index,count,"partialindex")
    sort_and_write(reverse_index_important,count,"importantwords")
    with open("initialurls.txt", "w") as file2:
        for url,docid in url_dict.items():
            file2.write(str(docid) + ":" + url + "\n")

    return current_doc_id





num_of_files = start_index()
print(num_of_files-1)
merge_main()
weighted_tfidf_normal(num_of_files-1)
weighted_tfidf_important(num_of_files-1)  #not used
make_positions("finishedimportant.txt")
make_positions("finishedindex.txt")       #not used
print("Indexing Finished")