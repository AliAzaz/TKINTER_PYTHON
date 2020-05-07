# Core Packages
import tkinter as tk
from tkinter import *
from tkinter import ttk
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tkinter.filedialog import askopenfilename

import xml.etree.ElementTree as ET
import os

# Note: tk or ttk has same functionality but the appearance is different


window = Tk()
window.title("NLP GUI")
window.geometry("800x600")  # To add dimensions or setting window display size

'''
# For label
label1 = Label(window, text="NLPGUI")
label1.grid(row=0, column=1)  # In order to set row and column
'''
# **** For Tab Layout ****
# Note:A ttk.Notebook widget manages a collection of windows and displays a single one at a time. Each slave window is associated with a tab, which the user may select to change the currently-displayed window.
# Note: A ttk.frame widget is a container, used to group other widgets together.
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)

# **** For Adding Tabs to Notebook ****
tab_control.add(tab1, text="NLPGUI")
tab_control.add(tab2, text="Processing File")
tab_control.add(tab3, text="About")

tab_control.pack(expand=1, fill='both')  # For displaying Tabs

# **** For NLPGUI Tab ****
label1 = Label(tab1, text="NLP for Simple text", padx=5, pady=5)  # padx and pady is used for padding
label1.grid(row=0, column=0)
label2 = Label(tab2, text="Processing of File", padx=5, pady=5)
label2.grid(row=0, column=0)
label3 = Label(tab3, text="About", padx=5, pady=5)
label3.grid(row=0, column=0)


# ********* FOR FUNCTIONS FOR NLP TAB1 **********


# Tokens using NLTK
def get_tokens():
    raw_text = str(raw_text_entry.get())
    new_text = nltk.word_tokenize(raw_text)
    result = '\nTokens: {}'.format(new_text)
    # For inserting into Display
    tab1_display.insert(tk.END, result)


def get_POS_tags():
    raw_text = str(raw_text_entry.get())
    new_text = nltk.word_tokenize(raw_text)
    this_new_text = nltk.pos_tag(new_text)
    result = '\nPOS tags: {}'.format(this_new_text)
    # For inserting into Display
    tab1_display.insert(tk.END, result)


def stopwords_removal():
    raw_text = str(raw_text_entry.get())
    stop_words = set(stopwords.words("english"))
    new_text = nltk.word_tokenize(raw_text)
    filtered_txt = []
    filtered_txt = [w for w in new_text if w not in stop_words]
    result = '\nStopwords Removal: {}'.format(filtered_txt)
    # For inserting into Display
    tab1_display.insert(tk.END, result)

    # Stopwords that exists in english corpus
    # print(stop_words)


# **** For Main NLP Tab1 ****
l1 = Label(tab1, text="Text for Analysis", padx=5, pady=5, bg='#ffffff')
l1.grid(row=1, column=0)

raw_text_entry = StringVar()
txtAnalysisArea = Entry(tab1, textvariable=raw_text_entry, width=50)
txtAnalysisArea.grid(row=1, column=1)

# For Adding Buttons in Tab1
Button1 = Button(tab1, text='Tokenize', width=12, bg='skyblue', fg='#FFF',
                 command=get_tokens)  # bg: background color, fg: fore ground color
Button1.grid(row=4, column=0, padx=10, pady=10)

Button2 = Button(tab1, text='POS Tagger', width=12, bg='skyblue', fg='#FFF',
                 command=get_POS_tags)  # bg: background color, fg: fore ground color
Button2.grid(row=4, column=1, padx=10, pady=10)

Button3 = Button(tab1, text='Stopwords Removal', width=14, bg='skyblue', fg='#FFF',
                 command=stopwords_removal)  # bg: background color, fg: fore ground color
Button3.grid(row=4, column=2, padx=10, pady=10)

Button4 = Button(tab1, text='Lemmatization', width=12, bg='darkblue',
                 fg='#FFF')  # bg: background color, fg: fore ground color
Button4.grid(row=5, column=0, padx=10, pady=10)

Button5 = Button(tab1, text='Reset', width=12, bg='darkblue', fg='#FFF')  # bg: background color, fg: fore ground color
Button5.grid(row=5, column=1, padx=10, pady=10)

Button6 = Button(tab1, text='Clear Text', width=12, bg='darkblue',
                 fg='#FFF')  # bg: background color, fg: fore ground color
Button6.grid(row=5, column=2, padx=10, pady=10)

# **** For Display Results on screen ****
tab1_display = Text(tab1)
# tab1_display.grid(row=7, column=0, columnspan=3, padx=5, pady=5)
tab1_display.grid(row=6, column=0, columnspan=3, padx=10, pady=10)


# **** Working for Files Input ****

# *** functionality ***
def selectFileFromPC():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filePath = askopenfilename(initialdir="/", title="Select file",
                               filetypes=(("txt files", "*.txt"), ("xml files", "*.xml"),
                                          ("pdf files", "*.pdf")))
    filename = os.path.basename(filePath)
    OpenDirectory.configure(text=filename)
    if ".xml" in filename:
        callingXMLWork(filePath)
    elif ".txt" in filename:
        callingTextWork(filePath)


def callingXMLWork(file_path):
    root = ET.parse(file_path).getroot()
    wordsList = []
    xmlParsing(wordsList, root.findall(root[1].tag))
    print(listToString(wordsList))
    txtAnalysisArea.delete(0, END)
    txtAnalysisArea.insert(0, listToString(wordsList))


def callingTextWork(file_path):
    # opening file
    root_file = open(file_path)
    # Use this to read file content as a stream:
    line = root_file.read()
    txtAnalysisArea.delete(0, END)
    txtAnalysisArea.insert(0, line)


def listToString(s):
    # using list comprehension
    listToStr = ' '.join([str(elem) for elem in s])
    return listToStr


def xmlParsing(list, subroot):
    if len(subroot):
        for subchild in subroot:
            xmlParsing(list, subchild)
    else:
        list.append(subroot.text)


# For Adding Open Directory Buttons
OpenDirectory = Button(tab1, text='Open Directory', width=12, bg='skyblue', fg='#FFF',
                       command=selectFileFromPC)  # bg: background color, fg: fore ground color
OpenDirectory.grid(row=1, column=2, padx=10, pady=10)

window.mainloop()
