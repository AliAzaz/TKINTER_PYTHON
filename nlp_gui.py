# Core Packages
import os
import threading
import time
import tkinter as tk
import xml.etree.ElementTree as ET
# NLP Packages for lemmatization
from collections import Counter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

import PyPDF2
import nltk
import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet  # To get words in dictionary with their parts of speech
from nltk.stem import WordNetLemmatizer  # lemmatizes word based on it's parts of speech

# Note: tk or ttk has same functionality but the appearance is different
window = Tk()
window.title("NLP MINING")

# **** For Tab Layout ****
tab_control = ttk.Notebook(window)
tab_analysis = ttk.Frame(tab_control)
tab_corpus = ttk.Frame(tab_control)
tab_about = ttk.Frame(tab_control)

# **** For Adding Tabs to Notebook ****
tab_control.add(tab_about, text="About")
tab_control.add(tab_analysis, text="Text Analysis")
tab_control.add(tab_corpus, text="Processing Corpus")
tab_control.pack(expand=1, fill='both')  # For displaying Tabs

# **** For NLPGUI Tab ****
label1 = Label(tab_analysis, text="NLP for Simple text", padx=5, pady=5)  # padx and pady is used for padding
label1.grid(row=0, column=0)
label2 = Label(tab_corpus, text="Processing of Corpus", padx=20, pady=10)
label2.grid(row=0, column=0)
label3 = Label(tab_about,
               text="NATURAL LANGUAGE PROCESSING TOOL\nDEVELOPED BY: \nKASHMALA JAMSHAID \nAND \nALI AZAZ ALAM", padx=5,
               pady=5,
               font='Helvetica 18 bold')
label3.grid(row=0, column=0)
label3.pack(expand=True)
# **** Progress Bar widget
analysisProgressBar = Progressbar(tab_analysis, orient=HORIZONTAL, mode='determinate', length=200)
analysisProgressBar.grid(column=1, row=0, sticky=W, padx=250, pady=10)
corpusProgressBar = Progressbar(tab_corpus, orient=HORIZONTAL, mode='determinate', length=200)
corpusProgressBar.grid(column=1, row=0, sticky=W, padx=250, pady=10)


# ********* FOR FUNCTIONS FOR NLP TABs **********

#  **** Supporting function's ****
def listToString(s):
    # using list comprehension
    listToStr = ' '.join([str(elem) for elem in s])
    return listToStr


def xmlParsing(sublist, subroot):
    if len(subroot):
        for subchild in subroot:
            xmlParsing(sublist, subchild)
    else:
        sublist.append(subroot.text)


def txtResultEnableDisable(flag):
    if flag == TRUE:
        txtResultDisplay.config(state=NORMAL)
    else:
        txtResultDisplay.config(state=DISABLED)


def txtCorpusResultEnableDisable(flag):
    if flag == TRUE:
        c_txtResultDisplay.config(state=NORMAL)
    else:
        c_txtResultDisplay.config(state=DISABLED)


def txtInsertInResultTextArea(result):
    txtResultEnableDisable(TRUE)
    txtResultDisplay.delete(0.0, END)
    txtResultDisplay.insert(tk.END, result)
    txtResultEnableDisable(FALSE)


def txtInsertInCorpusResultTextArea(result):
    txtCorpusResultEnableDisable(TRUE)
    c_txtResultDisplay.delete(0.0, END)
    c_txtResultDisplay.insert(tk.END, result)
    txtCorpusResultEnableDisable(FALSE)


def progress(current_value, progress_bar):
    progress_bar["value"] = current_value


def progressStarting(progress_bar):
    currentValue = 0
    progress_bar["value"] = currentValue
    progress_bar["maximum"] = 100
    divisions = 10
    for i in range(divisions):
        currentValue = currentValue + 10
        progress_bar.after(500, progress(currentValue, progress_bar))
        progress_bar.update()  # Force an update of the GUI
    progress_bar["value"] = 0


# ***** Lemmatization functions
def get_pos(word):
    w_synsets = wordnet.synsets(word)

    pos_counts = Counter()
    pos_counts["n"] = len([item for item in w_synsets if item.pos() == "n"])
    pos_counts["v"] = len([item for item in w_synsets if item.pos() == "v"])
    pos_counts["a"] = len([item for item in w_synsets if item.pos() == "a"])
    pos_counts["r"] = len([item for item in w_synsets if item.pos() == "r"])

    most_common_pos_list = pos_counts.most_common(3)
    # first indexer for getting the top POS from list, second indexer for getting POS from tuple( POS: count )
    return most_common_pos_list[0][0]


# **** Stop Word removal
def get_stop_word_filter_text():
    raw_text = str(getTextAreaData())
    stop_words = set(stopwords.words("english"))
    new_text = nltk.word_tokenize(raw_text.lower())
    filtered_txt = [w for w in new_text if w not in stop_words]
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in symbols:
        filtered_txt = np.char.replace(filtered_txt, i, ' ')
    return filtered_txt


def getTextAreaData():
    return txtAnalysisArea.get(0.0, tk.END)


def writeFile(filename, data):
    filename = filename.replace("\t", "")
    str_filename = filename.split(".")[0].replace(" ", "") + ".txt"
    if os.path.isfile(str_filename):
        messagebox.showinfo("Error", "File already exist.\nDelete it manually!!")
        return
    file = open(str_filename, 'a+')
    file.write(data + '\n')
    file.close()
    messagebox.showinfo("Done", "Successfully saved file in Corpus")


# **** Supporting function's End ****

# Tokens using NLTK
def run_tokenize():
    if txtAnalysisArea.compare("end-1c", "==", "1.0"):
        messagebox.showinfo("Error", "Analysis Text field is empty!!")
    else:
        progressStarting(analysisProgressBar)
        raw_text = str(getTextAreaData())
        new_text = nltk.word_tokenize(raw_text.lower())
        lblAction.config(text="Tokens")
        result = '{}'.format("\n".join(new_text))
        # For inserting into Display
        txtInsertInResultTextArea(result)


def run_pos_tags():
    if txtAnalysisArea.compare("end-1c", "==", "1.0"):
        messagebox.showinfo("Error", "Analysis Text field is empty!!")
    else:
        progressStarting(analysisProgressBar)
        raw_text = str(getTextAreaData())
        new_text = nltk.word_tokenize(raw_text.lower())
        this_new_text = nltk.pos_tag(new_text)
        lblAction.config(text="POS tags")
        result = '{}'.format("\n".join(this_new_text))
        # For inserting into Display
        txtInsertInResultTextArea(result)


def run_stopwords_removal():
    if txtAnalysisArea.compare("end-1c", "==", "1.0"):
        messagebox.showinfo("Error", "Analysis Text field is empty!!")
    else:
        progressStarting(analysisProgressBar)
        lblAction.config(text="Stopwords Removal")
        result = '{}'.format("\n".join(get_stop_word_filter_text()))
        # For inserting into Display
        txtInsertInResultTextArea(result)


def run_lemmatize():
    if txtAnalysisArea.compare("end-1c", "==", "1.0"):
        messagebox.showinfo("Error", "Analysis Text field is empty!!")
    else:
        progressStarting(analysisProgressBar)
        words = get_stop_word_filter_text()
        wnl = WordNetLemmatizer()
        lematized_text = [wnl.lemmatize(word, get_pos(word)) for word in words]
        lblAction.config(text="Lemmatization")
        result = '{}'.format("\n".join(lematized_text))
        # For inserting into Display
        txtInsertInResultTextArea(result)


def resetAllText():
    txtAnalysisArea.delete(0.0, END)
    txtResultEnableDisable(TRUE)
    txtResultDisplay.delete(0.0, END)
    txtResultEnableDisable(FALSE)
    lblFileLabel.configure(text='')
    lblAction.configure(text='No Action Selected')


def clearTextResultDisplayArea():
    txtResultEnableDisable(TRUE)
    txtResultDisplay.delete(0.0, END)
    txtResultEnableDisable(FALSE)
    lblAction.configure(text='No Action Selected')


def run_save_corpus():
    if c_txtResultDisplay.compare("end-1c", "==", "1.0"):
        messagebox.showinfo("Error", "Analysis Text field is empty!!")
    else:
        progressStarting(corpusProgressBar)
        time.sleep(2)
        file_name = c_lblFileLabel['text'].split(":")
        print(file_name)
        threading.Thread(target=writeFile(file_name[1], c_txtResultDisplay.get(0.0, tk.END))).start()


# **** Working for Files Input Functionality****

def selectAnalysisFileFromPC():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filePath = askopenfilename(initialdir="/", title="Select file",
                               filetypes=(("txt files", "*.txt"), ("xml files", "*.xml")))
    filename = os.path.basename(filePath)
    lblFileLabel.configure(text="Filename:\n" + filename)
    if ".xml" in filename:
        threading.Thread(target=callingXMLWork(filePath, analysisProgressBar)).start()
    elif ".txt" in filename:
        threading.Thread(target=callingTextWork(filePath, 1, analysisProgressBar)).start()


def selectCorpusFileFromPC():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filePath = askopenfilename(initialdir="/", title="Select file",
                               filetypes=(("txt files", "*.txt"), ("pdf files", "*.pdf")))
    filename = os.path.basename(filePath)
    c_lblFileLabel.configure(text="Filename:\t" + filename)
    if ".pdf" in filename:
        threading.Thread(target=callingPDFWork(filePath)).start()
    elif ".txt" in filename:
        threading.Thread(target=callingTextWork(filePath, 2, corpusProgressBar)).start()


def callingXMLWork(file_path, progress_bar):
    progressStarting(progress_bar)
    time.sleep(2)
    root = ET.parse(file_path).getroot()
    wordsList = []
    xmlParsing(wordsList, root.findall(root[1].tag))
    print(listToString(wordsList))
    txtAnalysisArea.delete(0.0, END)
    txtAnalysisArea.insert(0.0, listToString(wordsList))


def callingTextWork(file_path, tab_type, progress_bar):
    progressStarting(progress_bar)
    time.sleep(2)
    # opening file
    root_file = open(file_path)
    # Use this to read file content as a stream:
    line = root_file.read()
    if tab_type == 1:
        txtAnalysisArea.delete(0.0, END)
        txtAnalysisArea.insert(0.0, line)
    else:
        txtInsertInCorpusResultTextArea(line)


def callingPDFWork(file_path):
    progressStarting(corpusProgressBar)
    time.sleep(2)
    pdfFileObj = open(file_path, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    mytext = ""
    keywords = []
    for pageNum in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        mytext += pageObj.extractText()
        # The word_tokenize() function will break our text phrases into individual words.
        tokens = word_tokenize(mytext)
        # We'll create a new list that contains punctuation we wish to clean.
        punctuations = ['(', ')', ';', ':', '[', ']', ',']
        # We initialize the stopwords variable, which is a list of words like "The," "I," "and," etc. that don't hold much value as keywords.
        stop_words = stopwords.words('english')
        # We create a list comprehension that only returns a list of words that are NOT IN stop_words and NOT IN punctuations.
        keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
    result = '\nWords: {}'.format(listToString(keywords))
    txtInsertInCorpusResultTextArea(result)
    pdfFileObj.close()


# **** For Main NLP ANALYSIS_TAB ****

l1 = Label(tab_analysis, text="Text for Analysis", padx=20, pady=20, bg='#ffffff')
l1.grid(row=1, column=0)
l2 = Label(tab_analysis, text="Analysis Result\nScroll it through trackball", padx=20, pady=20, bg='#ffffff')
l2.grid(row=6, column=0)
lblAction = Label(tab_analysis, text="No Action Selected", padx=0, pady=5, fg='black', font='Ariel 12')
lblAction.grid(row=5, column=1)

# raw_text_entry = StringVar()
txtAnalysisArea = ScrolledText(tab_analysis, height=6)
txtAnalysisArea.grid(row=1, column=1)

lblFileLabel = Label(tab_analysis, text="", padx=0, pady=5, fg='darkblue')
lblFileLabel.grid(row=1, column=3)

# For Adding Open Directory Buttons
btnOpenDirectory = Button(tab_analysis, text='Open Directory', width=18, bg='black', fg='white',
                          command=selectAnalysisFileFromPC)  # bg: background color, fg: fore ground color
btnOpenDirectory.grid(row=1, column=2, padx=10, pady=10)

btnToken = Button(tab_analysis, text='Tokenize', width=18, bg='skyblue', fg='#FFF',
                  command=run_tokenize)  # bg: background color, fg: fore ground color
btnToken.grid(row=4, column=2, padx=10, pady=10)

btnPOSTagger = Button(tab_analysis, text='POS Tagger', width=18, bg='skyblue', fg='#FFF',
                      command=run_pos_tags)  # bg: background color, fg: fore ground color
btnPOSTagger.grid(row=4, column=3, padx=10, pady=10)

bntStopWordRM = Button(tab_analysis, text='Stopwords Removal', width=18, bg='skyblue', fg='#FFF',
                       command=run_stopwords_removal)  # bg: background color, fg: fore ground color
bntStopWordRM.grid(row=5, column=2, padx=10, pady=10)

btnLemma = Button(tab_analysis, text='Lemmatization', width=18, bg='skyblue', fg='#FFF',
                  command=run_lemmatize)  # bg: background color, fg: fore ground color
btnLemma.grid(row=5, column=3, padx=10, pady=10)

btnReset = Button(tab_analysis, text='Reset', width=18, bg='darkblue', fg='#FFF',
                  command=resetAllText)  # bg: background color, fg: fore ground color
btnReset.grid(row=6, column=2, padx=10, pady=10)

btnClear = Button(tab_analysis, text='Clear Text', width=18, bg='darkblue', fg='#FFF',
                  command=clearTextResultDisplayArea)  # bg: background color, fg: fore ground color
btnClear.grid(row=6, column=3, padx=10, pady=10)

# **** For Display Results on screen ****
txtResultDisplay = ScrolledText(tab_analysis, height=25)
txtResultDisplay.grid(row=6, column=1, padx=10, pady=0)
txtResultDisplay.config(state=DISABLED)

# **** End Main NLP ANALYSIS_TAB ****

# **** For Main NLP Tab2 ****
c_l1 = Label(tab_corpus, text="Select file for Corpus", padx=20, pady=20, bg='#ffffff')
c_l1.grid(row=1, column=0)
c_lblFileLabel = Label(tab_corpus, text="Filename:", padx=0, pady=5, fg='white', bg="lightgray", width=80)
c_lblFileLabel.grid(row=1, column=1)
c_l2 = Label(tab_corpus, text="Extracted words from file\nScroll it through trackball", padx=20, pady=20, bg='#ffffff')
c_l2.grid(row=6, column=0)

# For Adding Open File Button
c_btnOpenDirectory = Button(tab_corpus, text='Select File', width=18, bg='skyblue', fg='#FFF',
                            command=selectCorpusFileFromPC)
c_btnOpenDirectory.grid(row=1, column=2, padx=10, pady=10)

# For Adding Save Corpus Button
c_btnOpenDirectory = Button(tab_corpus, text='Save in Corpus', width=18, bg='black', fg='white',
                            command=run_save_corpus)
c_btnOpenDirectory.grid(row=6, column=2, padx=10, pady=10)

# **** For Display wordlist on box ****
c_txtResultDisplay = ScrolledText(tab_corpus, height=30)
c_txtResultDisplay.grid(row=6, column=1, padx=10, pady=10)
c_txtResultDisplay.config(state=DISABLED)


# **** End Main NLP Tab2 ****


# **** Full Screen Functionality ****
class FullScreenWindow:
    def __init__(self):
        self.window = window
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)

        self.w, self.h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (self.w, self.h))

        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)

        self.window.mainloop()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)


if __name__ == '__main__':
    app = FullScreenWindow()
