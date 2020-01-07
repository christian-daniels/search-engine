# from nltk.tokenize import word_tokenize
from collections import defaultdict
from math import log, sqrt
from nltk.stem import PorterStemmer

'''
This file contains all the methods that retrieve and process posting data
'''


INDEX = "finishedindex.txt"
IMPORTANT = "finishedimportant.txt"
def please_search(query:str, seekimportant,seekmain,urls, ps):
    # query = query.strip(" ")
    query = query.lower()


    query = "".join(c for c in query if c not in ('!', '?',"-","=", ':'))

    # print(query)                  #debug

    query_list = query.split()
    # print(query_list)             #debug
    query_set = {ps.stem(i) for i in query_list}
    query_list = list(query_set)
    # print(query_list)             #debug
    query_list.sort(reverse=True)
    stemmed_query = list()

    # a = input("debgu")



    if(len(query_list) > 1):
        for i in query_list:
            if i not in {'a','the','an','be','in','for','it','i','is',"of","to","and"}:
                stemmed_query.append(ps.stem(i))
        # print(stemmed_query)      #debug
        results, query_dict = find_postings(stemmed_query, seekimportant, seekmain)
        if len(results)> 0:
            return findScores(results, query_dict,urls)
        return dict()
    else:

        stemmed_query.append(ps.stem(query_list[0]))
        results, query_dict = find_postings(stemmed_query, seekimportant, seekmain)
        if len(results) > 0:
            return findScores(results, query_dict, urls)
        return dict()


def find_postings(query_list, seekimp, seekmain):
    # to_compare = list((query_list[0],query_list[1]))
    # print("in find postings",query_list)
    word_post = dict()
    query_dict = defaultdict(int)       #keeps track of query term freq
    for i in query_list:
        query_dict[i] +=1
    # first find all the postings of each term in the query

    # with open(INDEX, 'r') as file, open(IMPORTANT, 'r') as file2:
    with open(INDEX, 'r') as file:
        for current_word in query_dict.keys():

            first_letter = current_word[0]
            position1 = seekmain[first_letter]
            file.seek(position1)
            line = file.readline().rstrip()
            didnotfind = False
            while line != "":
                line = line.split(":")
                # print(line)
                if current_word == line[0]:
                    posting = line[1]
                    # term = line[0]
                    break
                if first_letter != line[0][0]:
                    didnotfind = True
                    break
                line = file.readline().rstrip()
                # line = file2.readline().rstrip()

            if didnotfind:
                pass
            else:
                # list_of_postings = posting
                word_post[current_word] = eval(posting)


    return word_post, query_dict


def findScores(word_post,query_dict,urls):
    # query dict tracks query frequencies
    Scores = defaultdict(int)           # stores document id and its current score
    docLength = defaultdict(int)        # key docid value doclength     used for Cosine Similarity
    queryLength = defaultdict(int)      # key docid value querylength   used for Cosine Similarity

    for term in word_post:
        current_posting = word_post[term]
        for document, tf, tfidf in current_posting:

            inside = query_dict[term] * tfidf / (1 + log(tf, 10))
            docLength[document]+= tfidf * tfidf
            queryLength[document]+= inside * inside
            Scores[document] += inside * tfidf

    for s in Scores:
        Scores[s] = Scores[s] / (sqrt(docLength[s]) + sqrt(queryLength[s]))

    # print(Scores)
    to_return = dict()
    for docid, score in Scores.items():
        if urls[docid] in to_return:
            pass
        else:
            to_return[urls[docid]] = score

    # print()
    return to_return



def single_term_frequency(posting,urls):
    posting = eval(posting)
    # posting.sort(key = lambda t:-t[1]) dont want to sort it
    a_dict= dict()
    for docid,tf,tfidf in posting:
        if urls[docid] in a_dict:
            pass
        else:
            a_dict[urls[docid]] = tfidf
    return a_dict

def single_retrieval(query,seekimportant,seekmain):

    word = query[0]
    first_letter = word[0]
    position1 = seekmain[first_letter]

    with open(INDEX, 'r') as file:
        file.seek(position1)
        line = file.readline().rstrip()


        didnotfind = False
        while line != "":
            line = line.split(":")

            if word == line[0]:
                posting = line[1]

                break
            if word[0] != line[0][0]:
                didnotfind = True
                break
            line = file.readline().rstrip()


        if didnotfind:
            results = []
        else:
            results = posting
    return results
