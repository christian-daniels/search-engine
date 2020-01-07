



import os,glob

from shutil import copyfile
from collections import defaultdict
from math import log
#partial_indexes = ["partialindex1.txt","partialindex2.txt","partialindex3.txt","partialindex4.txt","partialindex5.txt","partialindex6.txt"]

# CURRENT_DIR = "C:\\Users\\Christian\\cs121proj3" #dont really need this



def merge_main():

    partial_indexes = []
    # os.chdir(CURRENT_DIR) #dont really need this
    for file in glob.glob("*.txt"):
        if "partial" in file:
            print(file)
            partial_indexes.append(file)
    if os.path.exists("mergingindex.txt"):
        os.remove("mergingindex.txt") # if we are running this then we are remaking this index anyway
    if len(partial_indexes) == 1:
        loadone(partial_indexes.pop())

    else:
        partial_indexes = sorted(partial_indexes,reverse=True)
        first = partial_indexes.pop()
        second = partial_indexes.pop()
        merge_while_writing(first,second,True)
        while len(partial_indexes) > 0:
            merge_while_writing("mergingindex.txt",partial_indexes.pop(),False)




def loadone(filename): #used only if the partial index is size 1 ! this means we only have 1 index so simply rename it
    copyfile(filename,"mergingindex.txt")


def merge_while_writing(first,second,firstime = True):

    third = "building_index.txt"

    print("merger.py:",first,"and",second)
    with open(first,"r") as file1, open(second,"r") as file2, open(third,"w") as file3:
        line1 = file1.readline()
        line1 = line1.rstrip().split(":")

        line2 = file2.readline()
        line2 = line2.rstrip().split(":")

        while len(line1) > 1 and len(line2) > 1:
            line1_term = line1[0]
            line1_posting = eval(line1[1])
            line2_term = line2[0]
            line2_posting = eval(line2[1])
            if(line1_term == line2_term):
                total_posting = line1_posting + line2_posting
                file3.write(line1_term+":"+ str(total_posting)+'\n')
                line1 = file1.readline()
                line1 = line1.rstrip().split(":")
                line2 = file2.readline()
                line2 = line2.rstrip().split(":")

            elif(line1_term < line2_term):
                file3.write(line1_term+":"+str(line1_posting)+'\n')
                line1 = file1.readline()
                line1 = line1.rstrip().split(":")

            else:
                file3.write(line2_term+":"+str(line2_posting)+'\n')
                line2 = file2.readline()
                line2 = line2.rstrip().split(":")
        if len(line1) > 1:
            while len(line1) > 1:
                line1_term = line1[0]
                line1_posting = eval(line1[1])
                file3.write(line1_term + ":" + str(line1_posting) + '\n')
                line1 = file1.readline()
                line1 = line1.rstrip().split(":")
        elif len(line2) > 1 :
            while len(line2) > 1:
                line2_term = line2[0]
                line2_posting = eval(line2[1])
                file3.write(line2_term + ":" + str(line2_posting) + '\n')
                line2 = file2.readline()
                line2 = line2.rstrip().split(":")
    if firstime == False:
        os.remove(first)
    os.rename(third,"mergingindex.txt")


# merge_main()