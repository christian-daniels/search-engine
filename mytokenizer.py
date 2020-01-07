# this is where I processed tokens
# from html2text import HTML2Text
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import re


"""
Grabs all text in every important area of a document
    important text is saved in 2 locations - the current partial index and the important dictionary
"""
def tokenizer1(soup):
    for script in soup(["script", "style"]):
        script.extract()


    normal = []
    important = []
    # print("All paragraph text")
    for i in soup.find_all('p'):
        normal += word_tokenize(i.text)

    '''IMPORTANT WORD SECTIONS'''
    # print("All headings")
    for i in soup.find_all(re.compile('^h[1-6]$')):
        normal += word_tokenize(i.text)
        important += word_tokenize(i.text)    #temp

    # print("All titles")
    for i in soup.find_all('title'):
        normal += word_tokenize(i.text)
        important += word_tokenize(i.text)    #temp

    # print("All strong")
    for i in soup.find_all('strong'):
        normal += word_tokenize(i.text)
        important += word_tokenize(i.text)    #temp

    # print("All bold")
    for i in soup.find_all('b'):
        normal += word_tokenize(i.text)
        important += word_tokenize(i.text)    #temp

    return normal,important



'''
Word processor that matches alphanumeric strings only
    specifically:
        1. words without numbers ie computers
        2. acronyms ie i.b.m.
        3. numbers 1-999
'''
def tokenizer2(token_list):

    final = []
    ps = PorterStemmer()
    # could use 1 pattern ^(?:(?:[a-zA-Z]\.){2,}|^[a-zA-Z]+$)$
    pattern1 = re.compile(r"^[a-zA-Z]+$") # words/letters
    pattern2 = re.compile(r"^(?:[a-zA-Z]\.){2,}$")  # acronyms
    pattern3 = re.compile(r"^[0-9]{,3}$")   # numbers - only from 1-999 for class numbers
    for word in token_list:

        if re.match(pattern1,word):
            final.append(ps.stem(word.lower()))
        elif re.match(pattern2,word):
            final.append(word.lower())
            # when we match an acronym i just add it to the index
            # i thought about removing .'s but remembered sometimes they could get mixed up
            # for actual words and that would lead to so many other complications
        elif re.match(pattern3,word):
            final.append(word)

    return final

def computeWordFrequencies(token_list : list) -> dict:
    freq = dict()
    for token in token_list:
        if token.lower() not in freq:
            freq[token.lower()] = 1
        else:
            freq[token.lower()] += 1
    return freq

def positionTokenizer(token_list):
    final = dict()
    position = 1
    for token in token_list:
        if token.lower() in final:
            final[token.lower()] += [position]
            position+=1
        else:
            final[token.lower()] = [position]
            position+=1
    return final

def calcTF(posting):
    # posting consists of a dictionary
    # {docid : [positions], docid2: [positions]}
    count = 0
    for id,freq in posting:
        count += freq
    return count