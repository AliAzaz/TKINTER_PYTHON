# Core Packages
import os
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

import nltk
from nltk.corpus import stopwords

# Note: tk or ttk has same functionality but the appearance is different
window = Tk()
window.title("NLP MINING")
# window.geometry("800x600")  # To add dimensions or setting window display size

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
tab_control.add(tab3, text="About")
tab_control.add(tab1, text="Text Analysis")
tab_control.add(tab2, text="Processing Corpus")
tab_control.pack(expand=1, fill='both')  # For displaying Tabs

# **** For NLPGUI Tab ****
label1 = Label(tab1, text="NLP for Simple text", padx=5, pady=5)  # padx and pady is used for padding
label1.grid(row=0, column=0)
label2 = Label(tab2, text="Processing of Corpus", padx=5, pady=5)
label2.grid(row=0, column=0)
label3 = Label(tab3, text="NATURAL LANGUAGE PROCESSING TOOL\nDEVELOPED BY KASHMALA & ALI AZAZ", padx=5, pady=5,
               font='Helvetica 18 bold')
label3.grid(row=0, column=0)
label3.pack(expand=True)
# **** Progress Bar widget
progressBar = Progressbar(tab1, orient=HORIZONTAL, mode='determinate', length=200)
progressBar.grid(column=1, row=0, sticky=W, padx=120, pady=10)


# ********* FOR FUNCTIONS FOR NLP TAB1 **********

#  **** Supporting function's ****
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


def txtResultEnableDisable(flag):
    if flag == TRUE:
        txtResultDisplay.config(state=NORMAL)
    else:
        txtResultDisplay.config(state=DISABLED)


def txtInsertInResultTextArea(result):
    txtResultEnableDisable(TRUE)
    txtResultDisplay.delete(1.0, END)
    txtResultDisplay.insert(tk.END, result)
    txtResultEnableDisable(FALSE)


def progress(current_value):
    progressBar["value"] = current_value


def progressStarting():
    currentValue = 0
    progressBar["value"] = currentValue
    progressBar["maximum"] = 100
    divisions = 10
    for i in range(divisions):
        currentValue = currentValue + 10
        progressBar.after(500, progress(currentValue))
        progressBar.update()  # Force an update of the GUI
    progressBar["value"] = 0


# **** Supporting function's End ****

# Tokens using NLTK
def get_tokens():
    if txtAnalysisArea.compare("end-1c", "==", "1.0"):
        messagebox.showinfo("Error", "Analysis Text field is empty!!")
    else:
        progressStarting()
        raw_text = str(getTextAreaData())
        new_text = nltk.word_tokenize(raw_text)
        result = '\nTokens: {}'.format(new_text)
        # For inserting into Display
        txtInsertInResultTextArea(result)


def get_POS_tags():
    if txtAnalysisArea.compare("end-1c", "==", "1.0"):
        messagebox.showinfo("Error", "Analysis Text field is empty!!")
    else:
        progressStarting()
        raw_text = str(getTextAreaData())
        new_text = nltk.word_tokenize(raw_text)
        this_new_text = nltk.pos_tag(new_text)
        result = '\nPOS tags: {}'.format(this_new_text)
        # For inserting into Display
        txtInsertInResultTextArea(result)


def stopwords_removal():
    if txtAnalysisArea.compare("end-1c", "==", "1.0"):
        messagebox.showinfo("Error", "Analysis Text field is empty!!")
    else:
        progressStarting()
        raw_text = str(getTextAreaData())
        stop_words = set(stopwords.words("english"))
        new_text = nltk.word_tokenize(raw_text)
        filtered_txt = [w for w in new_text if w not in stop_words]
        result = '\nStopwords Removal: {}'.format(filtered_txt)
        # For inserting into Display
        txtInsertInResultTextArea(result)


def resetAllText():
    txtAnalysisArea.delete(0.0, END)
    txtResultEnableDisable(TRUE)
    txtResultDisplay.delete(1.0, END)
    txtResultEnableDisable(FALSE)
    lblFileLabel.configure(text='')


def clearTextResultDisplayArea():
    txtResultEnableDisable(TRUE)
    txtResultDisplay.delete(1.0, END)
    txtResultEnableDisable(FALSE)


def getTextAreaData():
    return txtAnalysisArea.get(0.0, tk.END)


# **** Working for Files Input Functionality****

def selectFileFromPC():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filePath = askopenfilename(initialdir="/", title="Select file",
                               filetypes=(("txt files", "*.txt"), ("xml files", "*.xml"),
                                          ("pdf files", "*.pdf")))
    filename = os.path.basename(filePath)
    lblFileLabel.configure(text="Filename:\n" + filename)
    if ".xml" in filename:
        callingXMLWork(filePath)
    elif ".txt" in filename:
        callingTextWork(filePath)


def callingXMLWork(file_path):
    progressStarting()
    root = ET.parse(file_path).getroot()
    wordsList = []
    xmlParsing(wordsList, root.findall(root[1].tag))
    print(listToString(wordsList))
    txtAnalysisArea.delete(0.0, END)
    txtAnalysisArea.insert(0.0, listToString(wordsList))


def callingTextWork(file_path):
    progressStarting()
    # opening file
    root_file = open(file_path)
    # Use this to read file content as a stream:
    line = root_file.read()
    txtAnalysisArea.delete(0.0, END)
    txtAnalysisArea.insert(0.0, line)


# **** For Main NLP Tab1 ****

l1 = Label(tab1, text="Text for Analysis", padx=10, pady=10, bg='#ffffff')
l1.grid(row=1, column=0)
l2 = Label(tab1, text="Analysis Result\nScroll it through trackball", padx=10, pady=10, bg='#ffffff')
l2.grid(row=6, column=0)

# raw_text_entry = StringVar()
txtAnalysisArea = ScrolledText(tab1, height=6)
txtAnalysisArea.grid(row=1, column=1)

lblFileLabel = Label(tab1, text="", padx=0, pady=5, fg='darkblue')
lblFileLabel.grid(row=1, column=3)

# For Adding Open Directory Buttons
btnOpenDirectory = Button(tab1, text='Open Directory', width=18, bg='skyblue', fg='#FFF',
                          command=selectFileFromPC)  # bg: background color, fg: fore ground color
btnOpenDirectory.grid(row=1, column=2, padx=10, pady=10)

# For Adding Buttons in Tab1
btnToken = Button(tab1, text='Tokenize', width=18, bg='skyblue', fg='#FFF',
                  command=get_tokens)  # bg: background color, fg: fore ground color
btnToken.grid(row=4, column=0, padx=10, pady=10)

btnPOSTagger = Button(tab1, text='POS Tagger', width=18, bg='skyblue', fg='#FFF',
                      command=get_POS_tags)  # bg: background color, fg: fore ground color
btnPOSTagger.grid(row=4, column=1, padx=10, pady=10)

bntStopWordRM = Button(tab1, text='Stopwords Removal', width=18, bg='skyblue', fg='#FFF',
                       command=stopwords_removal)  # bg: background color, fg: fore ground color
bntStopWordRM.grid(row=4, column=2, padx=10, pady=10)

btnLemma = Button(tab1, text='Lemmatization', width=18, bg='darkblue',
                  fg='#FFF')  # bg: background color, fg: fore ground color
btnLemma.grid(row=5, column=0, padx=10, pady=10)

btnReset = Button(tab1, text='Reset', width=18, bg='darkblue', fg='#FFF',
                  command=resetAllText)  # bg: background color, fg: fore ground color
btnReset.grid(row=5, column=1, padx=10, pady=10)

btnClear = Button(tab1, text='Clear Text', width=18, bg='darkblue', fg='#FFF',
                  command=clearTextResultDisplayArea)  # bg: background color, fg: fore ground color
btnClear.grid(row=5, column=2, padx=10, pady=10)

# **** For Display Results on screen ****
txtResultDisplay = Text(tab1)
txtResultDisplay.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
txtResultDisplay.config(state=DISABLED)


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
