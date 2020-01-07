
from search import please_search
from nltk.stem import PorterStemmer
import time



IMPORTANTPOS = "finishedimportantpositions.txt"
NORMALPOS = "finishedindexpositions.txt"
URLS = "initialurls.txt"

def load_position_dict(filename):

    with open(filename, 'r')as file:
        a_dict = eval(file.readline().rstrip())
    return a_dict

def load_urls():
    a_dict = dict()
    with open(URLS, 'r') as file:
        for line in file:
            line = line.rstrip().split(":",maxsplit=1)
            docid = int (line[0])
            domain = line[1]
            a_dict[docid] = domain
    return a_dict


def main_loop():
    # impposdict = load_position_dict(IMPORTANTPOS)
    impposdict = dict() # not using important words anymore; i dont know how to weight them
    maindict = load_position_dict(NORMALPOS)
    urls = load_urls()
    ps = PorterStemmer()
    query = input("Search for something! ")
    print("----------------------")
    while query != "-1":
        try:
            start = time.time()
            # print("hello")

            results = please_search(query,impposdict,maindict,urls,ps)
            print("Results for query \""+ query +'\"')
            if len(results) > 0:
                count = 1
                current_set = set()
                for docid, tfidf in sorted(results.items(),key = lambda t: -t[1]):
                    if count == 11:
                        break
                    if tfidf not in current_set and "eppstein" not in docid:    #helps eliminate displaying duplicate documents
                        # print(str(count)+". "+ docid,"score",tfidf)
                        print(str(count) + ". " + docid)
                        count+=1
                        current_set.add(tfidf)


            else:
                print("No results found for "+query)
        except:
            print("No results found for " + query)
        end = time.time()
        print(end - start)
        query = input("Search for something! ")
        print("----------------------")

# main_loop()