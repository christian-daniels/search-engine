import tkinter as tk
from PIL import Image
from PIL import ImageTk
from search import please_search
from searchengine import load_position_dict,load_urls
from nltk.stem import PorterStemmer
import time

'''
Constants
'''
HEIGHT = 700
WIDTH = 800
FILEWITHPOSITIONS = "indexpositions.txt"

NORMALPOS = "finishedindexpositions.txt"
URLS = "initialurls.txt"
'''
Function used to communicate to search program
'''
def run_search(query,impposdict,maindict,urls,ps):
    print("Search ran on", query)
    start = time.time()
    results = please_search(query,impposdict,maindict,urls,ps)

    # Temporary
    if len(results) == 0:
        results_label['text'] = query + " was not found"
    else:
        count = 1
        displayed_text = ""
        current_set = set()
        for docid, tfidf in sorted(results.items(), key=lambda t: -t[1]):
            if count == 11:
                break
            if tfidf not in current_set and "eppstein" not in docid:  # helps eliminate displaying duplicate documents and this giant doc thats super uninformative
                # print(str(count) + ". " + docid, "score", tfidf)
                # displayed_text += str(count) + ". " + docid + " score " + str(tfidf)+'\n'
                displayed_text += str(count) + ". " + docid + '\n'
                count += 1
                current_set.add(tfidf)


        results_label['text'] = displayed_text
    end = time.time()
    elapsed = end - start
    print("elapsed time:",elapsed,"seconds")
    # print(end - start)


'''
This file sets up:
    -the ui of the program
    -the position dictionary used for seek() (loaded from a file made before this program is even ran)
    -the search functionality
'''
# def set_up_program():

#position dictionary initialized and loaded into memory

impposdict = dict() # not using important words anymore; i dont know how to weight them
maindict = load_position_dict(NORMALPOS)
urls = load_urls()
ps = PorterStemmer()
# interface creation
root = tk.Tk()  #creates the window
root.title("Search Engine via Christian Daniels")
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH, bg = "#FFC72C")
canvas.pack()

image1 = Image.open("background.png")
image1 = image1.resize((500, 100), Image.ANTIALIAS) ## The (250, 250) is (height, width)
image1 = ImageTk.PhotoImage(image1)
background_label = tk.Label(root, image = image1, bd = 5, bg = '#0C2340')
background_label.place(relx = 0.5, rely = 0.05, anchor = 'n')


frame = tk.Frame(root, bg = '#0C2340', bd = 5)
frame.place(relx = 0.5, rely = 0.22,relwidth = 0.75, relheight = 0.1, anchor = 'n')
entry = tk.Entry(frame, font = 40)
entry.place(relwidth = 0.65, relheight = 1)

search = tk.Button(frame, text = "Search!", font = 40, command = lambda: run_search(entry.get(),impposdict,maindict,urls,ps))
search.place(relx = 0.7 , relheight = 1 , relwidth = 0.3)

results_frame = tk.Frame(root, bg = '#0C2340', bd = 5)
results_frame.place(relx = 0.5, rely = 0.35,relwidth = 0.75, relheight = 0.6, anchor = 'n')


results_label = tk.Label(results_frame,font = ('Courier',10),wraplength = 500,justify = "left")
results_label.place(relwidth = 1, relheight =1)




# renders window to screen
root.mainloop()
# set_up_program()