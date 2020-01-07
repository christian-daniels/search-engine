

from math import log

def weighted_tfidf_normal(num_of_valid_docs):
    with open("mergingindex.txt","r") as unweighted, open("finishedindex.txt","w") as weighted:
        line = unweighted.readline().rstrip().split(":")
        print("weighted_tfidf(): working on merging.txt")
        while len(line)>1:
            term = line[0]
            posting = eval(line[1])
            df = len(posting)
            idf = log(num_of_valid_docs/df,10)
            building = []
            for docid, tf in posting:
                wtf =  1 + log(tf)
                tf_idf = wtf*idf
                building.append((docid,tf,tf_idf))
            weighted.write(term+":"+str(building)+"\n")
            line = unweighted.readline().rstrip().split(":")

def weighted_tfidf_important(num_of_valid_docs):
    with open("importantwords1.txt","r") as unweighted, open("finishedimportant.txt","w") as weighted:
        line = unweighted.readline().rstrip().split(":")
        print("weighted_tfidf(): working on importantwords1.txt")
        while len(line)>1:
            term = line[0]
            posting = eval(line[1])
            df = len(posting)
            idf = log(num_of_valid_docs/df,10)
            building = []
            for docid, tf in posting:
                wtf =  1 + log(tf,10)#rerun position and
                tf_idf = wtf*idf
                building.append((docid,tf,tf_idf))
            weighted.write(term+":"+str(building)+"\n")
            line = unweighted.readline().rstrip().split(":")

