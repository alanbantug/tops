#! python3

import tkinter
from tkinter import *

from tkinter.ttk import *
from tkinter import messagebox

from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

import threading

import setGenerate as sg
import setOddEven as so
import dataStatistics as dt
import os
import pdb
import copy
import random
import shutil
import operator
import subprocess as sp
import displayGenerate as dg
import datetime

import dataDownload as dataD
import configIO as cIO

from PIL import Image, ImageTk

class Application(Frame):

    def __init__(self, master):

        self.master = master
        self.main_container = Frame(self.master)

        self.useCount = IntVar()
        self.type = IntVar()

        self.getMatch3 = IntVar()
        self.getMatch4 = IntVar()
        self.getMatch5 = IntVar()
        self.noLastWinner = IntVar()
        self.distribution =IntVar()
        self.getMatchExtra = IntVar()
        self.numberA = StringVar()
        self.numberB = StringVar()
        self.numberC = StringVar()
        self.numberD = StringVar()
        self.numberE = StringVar()
        self.numberExtra = StringVar()

        # update this setting when data download because unavailable
        self.noDownload = IntVar()
        self.noDownload.set(1)

        # Set images. Note that the line below is needed to change the working directory of the batch file to point to where the script files, including image files are
        # It has to be commented out in the testing library

        # os.chdir("c:\\users\\alanb\\documents\\scripts\\code\\sng")

        self.topValue = 0
        self.extValue = 0
        self.workDirectory = os.getcwd()

        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # initialize the configuration file input-output class
        self.config = cIO.configIO()

        # Set Label styles
        Style().configure("M.TLabel", font="Verdana 20 bold", anchor="center")

        Style().configure("G.TLabel", foreground="white", background="green", font="Courier 8", anchor="center")
        Style().configure("L.TLabel", foreground="white", background="blue", font="Courier 8", anchor="center")
        Style().configure("R.TLabel", foreground="white", background="red", font="Courier 8", anchor="center")
        Style().configure("Y.TLabel", foreground="black", background="yellow", font="Courier 8", anchor="center")
        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")
        Style().configure("T.TLabel", font="Verdana 12 bold")
        Style().configure("S.TLabel", font="Verdana 10")
        Style().configure("B.TLabel", font="Verdana 8")
        Style().configure("SB.TLabel", font="Verdana 8", background="white")

        # Set button styles
        Style().configure("B.GButton", font="Verdana 8", relief="raised", height=10)
        Style().configure("B.TButton", font="Verdana 8", relief="raised")
        Style().configure("B.TCheckbutton", font="Verdana 8")
        Style().configure("B.TRadiobutton", font="Verdana 8")

        # Set scale styles
        Style().configure("S.TScale", orient=HORIZONTAL, width=25)

        self.parentTab = Notebook(self.main_container)
        self.staTab = Frame(self.parentTab)   # first page, which would get widgets gridded into it
        self.datTab = Frame(self.parentTab)   # second page
        self.abtTab = Frame(self.parentTab)   # third page
        self.parentTab.add(self.datTab, text='   Data     ')
        self.parentTab.add(self.staTab, text='   Stat     ')
        self.parentTab.add(self.abtTab, text='   Generate ')

        # Create widgets for the main screen

        self.mainLabel = Label(self.main_container, text="TOP NUMBERS", style="M.TLabel" )
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=self.exitRoutine)

        # Create widgets for the Data tab

        self.h_sep_da = Separator(self.datTab, orient=HORIZONTAL)
        self.h_sep_db = Separator(self.datTab, orient=HORIZONTAL)
        self.h_sep_dc = Separator(self.datTab, orient=HORIZONTAL)
        self.h_sep_dd = Separator(self.datTab, orient=HORIZONTAL)
        self.h_sep_de = Separator(self.datTab, orient=HORIZONTAL)
        self.h_sep_df = Separator(self.datTab, orient=HORIZONTAL)

        self.datLabel = Label(self.datTab, text="Data File", style="T.TLabel" )
        self.datLabelA = Label(self.datTab, text="Displays downloaded data from CALottery.com and allows filtering of ", style="B.TLabel" )
        self.datLabelB = Label(self.datTab, text="winning combinations based on provided numbers. Winners that ", style="B.TLabel" )
        self.datLabelC = Label(self.datTab, text="match 3 or 4 numbers from the combination entered are also listed.", style="B.TLabel" )

        self.typeGroup = LabelFrame(self.datTab, text=' Game Selection ', style="O.TLabelframe")
        self.typeA = Radiobutton(self.typeGroup, text="Fantasy", style="B.TRadiobutton", command=self.displayDataFile, variable=self.type, value=1)
        self.typeB = Radiobutton(self.typeGroup, text="Super", style="B.TRadiobutton", command=self.displayDataFile, variable=self.type, value=2)
        self.typeC = Radiobutton(self.typeGroup, text="Mega", style="B.TRadiobutton", command=self.displayDataFile, variable=self.type, value=3)
        self.typeD = Radiobutton(self.typeGroup, text="Powerball", style="B.TRadiobutton", command=self.displayDataFile, variable=self.type, value=4)

        self.sourceLabel = Label(self.datTab, text="None", style="SB.TLabel" )
        self.selectSource = Button(self.datTab, text="SELECT FILE", style="B.TButton", command=self.setDataFile)
        self.downloadFile = Button(self.datTab, text="DOWNLOAD DATA", style="B.TButton", command=self.downloadThread)

        self.numberEntry = LabelFrame(self.datTab, text=' Combination Check', style="O.TLabelframe")
        self.numA = Entry(self.numberEntry, textvariable=self.numberA, width="5")
        self.numB = Entry(self.numberEntry, textvariable=self.numberB, width="5")
        self.numC = Entry(self.numberEntry, textvariable=self.numberC, width="5")
        self.numD = Entry(self.numberEntry, textvariable=self.numberD, width="5")
        self.numE = Entry(self.numberEntry, textvariable=self.numberE, width="5")
        self.numExtra = Entry(self.numberEntry, textvariable=self.numberExtra, width="5")
        self.extraLabel = Label(self.numberEntry, text="EXTRA", width="7", style="B.TLabel")

        self.filterOpt = LabelFrame(self.datTab, text=' Match Filter Options ', style="O.TLabelframe")
        self.match3 = Checkbutton(self.filterOpt, text=' 3 Numbers ', style="B.TCheckbutton", variable=self.getMatch3)
        self.match4 = Checkbutton(self.filterOpt, text=' 4 Numbers  ', style="B.TCheckbutton", variable=self.getMatch4)
        self.match5 = Checkbutton(self.filterOpt, text=' 5 Numbers  ', style="B.TCheckbutton", variable=self.getMatch5)
        self.matchExtra = Checkbutton(self.filterOpt, text=' Extra ', style="B.TCheckbutton", variable=self.getMatchExtra)

        self.dataDisplay = LabelFrame(self.datTab, text=' Winners', style="O.TLabelframe")
        self.scroller = Scrollbar(self.dataDisplay, orient=VERTICAL)
        self.dataSelect = Listbox(self.dataDisplay, yscrollcommand=self.scroller.set, width=68, height=7)

        self.filter = Button(self.datTab, text="FILTER", style="B.TButton", command=self.filterProcess)
        self.reset = Button(self.datTab, text="RESET", style="B.TButton", command=self.initReadProcess)

        self.statusLabel = Label(self.datTab, text="Select source and target folders", style="G.TLabel")

        # Position widgets

        self.datLabel.grid(row=0, column=0, columnspan=4, padx=5, pady=(10, 10), sticky='NSEW')
        self.datLabelA.grid(row=1, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.datLabelB.grid(row=2, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.datLabelC.grid(row=3, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')

        self.h_sep_da.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.typeA.grid(row=0, column=0, padx=(10,0), pady=(5, 10), sticky='W')
        self.typeB.grid(row=0, column=0, padx=(130,0), pady=(5, 10), sticky='W')
        self.typeC.grid(row=0, column=0, padx=(240,0), pady=(5, 10), sticky='W')
        self.typeD.grid(row=0, column=0, padx=(350,0), pady=(5, 10), sticky='W')
        self.typeGroup.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.h_sep_db.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.dataSelect.grid(row=0, column=0, padx=(10,0), pady=(5,10), sticky='NSEW')
        self.scroller.grid(row=0, column=1, padx=(10,0), pady=(5,10), sticky='NSEW')
        self.dataDisplay.grid(row=7, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.sourceLabel.grid(row=8, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        self.selectSource.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.downloadFile.grid(row=9, column=2, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.h_sep_dc.grid(row=10, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.numA.grid(row=0, column=0, padx=(10,0), pady=(5, 10), sticky='W')
        self.numB.grid(row=0, column=0, padx=(70,0), pady=(5, 10), sticky='W')
        self.numC.grid(row=0, column=0, padx=(130,0), pady=(5, 10), sticky='W')
        self.numD.grid(row=0, column=0, padx=(190,0), pady=(5, 10), sticky='W')
        self.numE.grid(row=0, column=0, padx=(250,0), pady=(5, 10), sticky='W')
        self.extraLabel.grid(row=0, column=0, padx=(320,0), pady=(5, 10), sticky='W')
        self.numExtra.grid(row=0, column=0, padx=(380,0), pady=(5, 10), sticky='W')
        self.numberEntry.grid(row=11, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.match3.grid(row=0, column=0, padx=(10,0), pady=(5, 10), sticky='W')
        self.match4.grid(row=0, column=0, padx=(130,0), pady=(5, 10), sticky='W')
        self.match5.grid(row=0, column=0, padx=(240,0), pady=(5, 10), sticky='W')
        self.matchExtra.grid(row=0, column=0, padx=(350,0), pady=(5, 10), sticky='W')
        self.filterOpt.grid(row=12, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.filter.grid(row=13, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.reset.grid(row=13, column=2, columnspan=2, padx=5, pady=5, sticky='NSEW')

        # Create widgets for the Stats Tab

        self.h_sep_sa = Separator(self.staTab, orient=HORIZONTAL)
        self.h_sep_sb = Separator(self.staTab, orient=HORIZONTAL)
        self.h_sep_sc = Separator(self.staTab, orient=HORIZONTAL)
        self.h_sep_sd = Separator(self.staTab, orient=HORIZONTAL)
        self.h_sep_se = Separator(self.staTab, orient=HORIZONTAL)
        self.h_sep_sf = Separator(self.staTab, orient=HORIZONTAL)
        self.h_sep_sg = Separator(self.staTab, orient=HORIZONTAL)

        self.staLabel = Label(self.staTab, text="Statistics", style="T.TLabel" )
        self.staLabelA = Label(self.staTab, text="Shows pertinent statistics based on the data file selected or downloaded.", style="B.TLabel" )

        self.numDisplay = LabelFrame(self.staTab, text=' Number Count ', style="O.TLabelframe")
        self.numscroller = Scrollbar(self.numDisplay, orient=VERTICAL)
        self.numData = Listbox(self.numDisplay, yscrollcommand=self.numscroller.set, width=30, height=7)
        self.numSort = Button(self.staTab, text="SORT BY COUNT", style="B.TButton", command=self.sortNumbers)

        self.megaDisplay = LabelFrame(self.staTab, text=' Super - Power - Mega Count ', style="O.TLabelframe")
        self.megascroller = Scrollbar(self.megaDisplay, orient=VERTICAL)
        self.megaData = Listbox(self.megaDisplay, yscrollcommand=self.megascroller.set, width=30, height=7)
        self.megaSort = Button(self.staTab, text="SORT BY COUNT", style="B.TButton", command=self.sortMegas)

        self.patDisplay = LabelFrame(self.staTab, text=' Pattern Count ', style="O.TLabelframe")
        self.pat5O = Label(self.patDisplay, text="5O - ", style="B.TLabel" )
        self.pat4O = Label(self.patDisplay, text="4O - ", style="B.TLabel" )
        self.pat3O = Label(self.patDisplay, text="3O - ", style="B.TLabel" )
        self.pat3E = Label(self.patDisplay, text="3E - ", style="B.TLabel" )
        self.pat4E = Label(self.patDisplay, text="4E - ", style="B.TLabel" )
        self.pat5E = Label(self.patDisplay, text="5E - ", style="B.TLabel" )

        self.lastMatchDrawInfo = Label(self.staTab, text="", style="B.TLabel" )
        self.maxGapInfo = Label(self.staTab, text="", style="B.TLabel" )
        self.resultsPlot = Label(self.staTab)
        self.refreshGraph = Button(self.staTab, text="REFRESH GRAPH", style="B.TButton", command=self.refreshDataGraph)

        # Position widgets on the Select tab

        self.staLabel.grid(row=0, column=0, columnspan=4, padx=5, pady=(10,10), sticky='NSEW')
        self.staLabelA.grid(row=2, column=0, columnspan=4, padx=5, pady=(0, 5), sticky='NSEW')

        self.h_sep_sa.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.numData.grid(row=0, column=0, padx=(10,0), pady=(5,10), sticky='NSEW')
        self.numscroller.grid(row=0, column=1, padx=(10,0), pady=(5,10), sticky='NSEW')
        self.numDisplay.grid(row=4, column=0, rowspan=5, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.megaData.grid(row=0, column=0, padx=(10,0), pady=(5,10), sticky='NSEW')
        self.megascroller.grid(row=0, column=1, padx=(10,0), pady=(5,10), sticky='NSEW')
        self.megaDisplay.grid(row=4, column=2, rowspan=5, columnspan=2, padx=5, pady=5, sticky='NSEW')

        #self.pat5O.grid(column=0, padx=5, pady=(5,0), sticky='NSEW')
        #self.pat4O.grid(column=0, padx=5, pady=(5,0), sticky='NSEW')
        #self.pat3O.grid(column=0, padx=5, pady=(5,0), sticky='NSEW')
        #self.pat3E.grid(column=0, padx=5, pady=(5,0), sticky='NSEW')
        #self.pat4E.grid(column=0, padx=5, pady=(5,0), sticky='NSEW')
        #self.pat5E.grid(column=0, padx=5, pady=(5,0), sticky='NSEW')
        #self.patDisplay.grid(row=4, column=2, rowspan=6, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.numSort.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.megaSort.grid(row=9, column=2, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.h_sep_sb.grid(row=10, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.lastMatchDrawInfo.grid(row=11, column=0, columnspan=2, padx=5, pady=0, sticky='NSEW')
        self.maxGapInfo.grid(row=11, column=2, columnspan=2, padx=5, pady=0, sticky='NSEW')

        self.h_sep_sc.grid(row=12, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.resultsPlot.grid(row=13, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        self.refreshGraph.grid(row=14, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')

        #self.h_sep_sd.grid(row=14, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')



        # Create widgets for About tab

        self.h_sep_aa = Separator(self.abtTab, orient=HORIZONTAL)
        self.h_sep_ab = Separator(self.abtTab, orient=HORIZONTAL)
        self.h_sep_ac = Separator(self.abtTab, orient=HORIZONTAL)
        self.h_sep_ad = Separator(self.abtTab, orient=HORIZONTAL)

        self.aboutText  = Label(self.abtTab, text="About this script", style="T.TLabel" )
        self.aboutTextA = Label(self.abtTab, text="This script can be used to generate numbers for all lottery games in", style="B.TLabel" )
        self.aboutTextB = Label(self.abtTab, text="California Lottery. This script will require a valid lottery winners data", style="B.TLabel" )
        self.aboutTextC = Label(self.abtTab, text="file that may be downloaded from the California Lottery website.", style="B.TLabel" )
        self.aboutTextD = Label(self.abtTab, text="The numbers generated will come from the top numbers with regards to ", style="B.TLabel" )
        self.aboutTextE = Label(self.abtTab, text="frequency or from a predicting model. The model can also be trained, but", style="B.TLabel" )
        self.aboutTextF = Label(self.abtTab, text="have very low accuracy scores. Note also that the Powerball and MegaLotto", style="B.TLabel" )
        self.aboutTextG = Label(self.abtTab, text="number selections have changed, so stats for those games are not reliable.", style="B.TLabel" )

        self.aboutTextH = Label(self.abtTab, text="Color coding", style="T.TLabel" )
        self.aboutTextI = Label(self.abtTab, text="Combinations generated are color-coded depending on their likelyhood of ", style="B.TLabel" )
        self.aboutTextJ = Label(self.abtTab, text="occurence based on data provided. The color codes are listed below", style="B.TLabel" )

        self.legendBest = Label(self.abtTab, width=12, style="G.TLabel" )
        self.legendGood = Label(self.abtTab, width=12, style="L.TLabel" )
        self.legendLowC = Label(self.abtTab, width=12, style="Y.TLabel" )
        self.legendPrev = Label(self.abtTab, width=12, style="R.TLabel" )

        self.bestText = Label(self.abtTab, text="3O - 3E - High Occurence", style="B.TLabel" )
        self.goodText = Label(self.abtTab, text="4O - 4E - Low Occurence", style="B.TLabel" )
        self.lowCText = Label(self.abtTab, text="5O - 5E - Rare Occurence", style="B.TLabel" )
        self.prevText = Label(self.abtTab, text="Past Winner", style="B.TLabel" )

        self.showGen = Button(self.abtTab, text="SHOW GENERATE PANEL", style="B.TButton", command=self.showGenerate)

        # Position widgets in About tab

        self.aboutText.grid(row=0, column=0, columnspan=4, padx=5, pady=(10,10), sticky='NSEW')
        self.aboutTextA.grid(row=1, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.aboutTextB.grid(row=2, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.aboutTextC.grid(row=3, column=0, columnspan=4, padx=5, pady=(0,10), sticky='NSEW')
        self.aboutTextD.grid(row=4, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.aboutTextE.grid(row=5, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.aboutTextF.grid(row=6, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.aboutTextG.grid(row=7, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')

        self.h_sep_aa.grid(row=8, column=0, columnspan=4, padx=5, pady=10, sticky='NSEW')

        self.aboutTextH.grid(row=9, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        self.aboutTextI.grid(row=10, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.aboutTextJ.grid(row=11, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')

        self.h_sep_ab.grid(row=12, column=0, columnspan=4, padx=5, pady=10, sticky='NSEW')

        self.legendBest.grid(row=13, column=0, columnspan=1, padx=5, pady=5, sticky='E')
        self.bestText.grid(row=13, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.legendGood.grid(row=14, column=0, columnspan=1, padx=5, pady=5, sticky='E')
        self.goodText.grid(row=14, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.legendLowC.grid(row=15, column=0, columnspan=1, padx=5, pady=5, sticky='E')
        self.lowCText.grid(row=15, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.legendPrev.grid(row=16, column=0, columnspan=1, padx=5, pady=5, sticky='E')
        self.prevText.grid(row=16, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.h_sep_ac.grid(row=17, column=0, columnspan=4, padx=5, pady=10, sticky='NSEW')

        self.showGen.grid(row=18, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.mainLabel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')
        self.parentTab.grid(row=1, column=0, padx=5, pady=5, sticky='NSEW')
        self.exit.grid(row=5, column=0, padx=5, pady=(2,5), sticky='NSEW')

        # set the type selection to Fantasy Five
        self.type.set(1)

        self.displayDataFile()

    def genOddSet(self):

        ''' This function will initiate the thread for generating combinations
        '''

        t = threading.Thread(None, self.genOddEvenThread(1), ())
        t.start()

    def genEvenSet(self):

        ''' This function will initiate the thread for generating combinations
        '''

        t = threading.Thread(None, self.genOddEvenThread(0), ())
        t.start()

    def genOddEvenThread(self, indicator):

        ''' This function will generate combinations of numbers using the getCombination method of the sg object
        '''

        self.showProgress()

        last_draw, last_winner = self.numberStats.getLastDraw()

        self.sOE = so.getCombinations(indicator, self.type.get(), last_winner, self.noLastWinner.get())
        selection, unused = self.sOE.randomSelect()

        self.hideProgress()

        if unused > 0:
            self.unused['text'] = 'Unused: ' + str(unused)
        else:
            self.unused['text'] = ''

        # check the selection limit before showing it. this is needed since the looping limit for generating
        # may be reached without completely generating 5 combinations
        if len(selection) == 5:
            for i in range(5):
                self.dGen[i].changeTopStyle(selection[i])

            self.saveGenerated(selection)
        else:
            messagebox.showerror('Generate Error', 'Generation taking too long. Retry.')


    def generateSet(self):

        ''' This function will initiate the thread for generating combinations
        '''

        t = threading.Thread(None, self.genSetThread, ())
        t.start()

    def genSetThread(self):

        ''' This function will generate combinations of numbers using the getCombination method of the sg object
        '''

        self.showProgress()

        if self.type.get() == 1:
            self.useCount.set(25)
        else:
            self.useCount.set(25)

        last_draw, last_winner = self.numberStats.getLastDraw()

        # check if the last winner is to be excluded
        if self.noLastWinner.get():
            selected = [num for num in self.numberStats.getTopNumbers() if num not in last_winner]
        else:
            selected = self.numberStats.getTopNumbers()

        self.sGen = sg.getCombinations(selected, self.type.get(), self.useCount.get(), self.distribution.get())
        selection = self.sGen.randomSelect(self.useCount.get())

        self.hideProgress()

        self.unused['text'] = ''

        # check the selection limit before showing it. this is needed since the looping limit for generating
        # may be reached without completely generating 5 combinations
        if len(selection) == 5:
            for i in range(5):
                self.dGen[i].changeTopStyle(selection[i])

            self.saveGenerated(selection)
        else:
            messagebox.showerror('Generate Error', 'Generation taking too long. Retry.')


    def exitRoutine(self):

        ''' This function will be executed when the user exits
        '''

        root.destroy()


    def saveGenerated(self, selection):

        ''' This function will call the method to save the last generated set of combinations
        '''

        self.numberStats.writeGenerated(self.config, selection)


    def setDataFile(self):

        ''' This function will check if the selected file is valid and display information from the file
        '''

        filename = askopenfilename()

        if os.path.isfile(filename):
            datafile = open(filename)

            # Read the first record on file
            d_line = datafile.readline()
            d_list = d_line.split()

            datafile.close()

            if self.type.get() == 1:

                if "FANTASY" in d_list:
                    self.dataFile = filename
                    self.sourceLabel["text"] = os.path.dirname(filename)[:20] + "..." + os.path.basename(filename)

                    # Create an instance of number source each time a new file is selected
                    self.numberStats = dt.dataStatistics(self.config, self.dataFile, self.type.get())

                else:
                    messagebox.showerror('Invalid File', 'File selected is not a valid Fantasy Five data file.')

            elif self.type.get() == 2:

                if "SUPERLOTTO" in d_list:
                    self.dataFile = filename
                    self.sourceLabel["text"] = os.path.dirname(filename)[:20] + "..." + os.path.basename(filename)

                    # Create an instance of number source each time a new file is selected
                    self.numberStats = dt.dataStatistics(self.config, self.dataFile, self.type.get())

                else:
                    messagebox.showerror('Invalid File', 'File selected is not a valid SuperLotto data file.')

            elif self.type.get() == 3:

                if "MEGA MILLIONS" in d_list:
                    self.dataFile = filename
                    self.sourceLabel["text"] = os.path.dirname(filename)[:20] + "..." + os.path.basename(filename)

                    # Create an instance of number source each time a new file is selected
                    self.numberStats = dt.dataStatistics(self.config, self.dataFile, self.type.get())

                else:
                    messagebox.showerror('Invalid File', 'File selected is not a valid SuperLotto data file.')

            elif self.type.get() == 4:

                if "POWERBALL" in d_list:
                    self.dataFile = filename
                    self.sourceLabel["text"] = os.path.dirname(filename)[:20] + "..." + os.path.basename(filename)

                    # Create an instance of number source each time a new file is selected
                    self.numberStats = dt.dataStatistics(self.config, self.dataFile, self.type.get())

                else:
                    messagebox.showerror('Invalid File', 'File selected is not a valid SuperLotto data file.')

            else:
                self.displayDataFile()

            # copy the data source to the JSON config file
            self.config.updateSource(self.type.get(), self.dataFile)


    def downloadThread(self):

        if self.noDownload:
            messagebox.showinfo("Download not available", "Data download unavailable at this time because of site upgrade.")
            return

        t = threading.Thread(None, self.downloadData, ())
        t.start()

    def downloadData(self):

        if self.type.get() == 1:
            baseUrl = 'http://www.calottery.com/play/draw-games/fantasy-5/winning-numbers'
            dataFileName = "data\\FantasyFive.txt"

        elif self.type.get() == 2:
            baseUrl = 'http://www.calottery.com/play/draw-games/superlotto-plus/winning-numbers'
            dataFileName = "data\\SuperLottoPlus.txt"

        elif self.type.get() == 3:
            baseUrl = 'https://www.calottery.com/play/draw-games/mega-millions/winning-numbers'
            dataFileName = "data\\MegaLotto.txt"

        elif self.type.get() == 4:
            baseUrl = 'https://www.calottery.com/play/draw-games/powerball/winning-numbers'
            dataFileName = "data\\PowerBall.txt"

        else:
            messagebox.showerror("Download Error", "Download not available for game selected.")
            return

        try:
            dataFile = open(dataFileName, "w")
        except:
            os.makedirs("data")
            dataFile = open(dataFileName, "w")

        dataFile.close()

        fileNamePath = os.path.join(os.getcwd(), dataFileName)

        self.showProgress()
        dataD.dataDownload(baseUrl, fileNamePath)
        self.hideProgress()

        self.dataFile = fileNamePath
        self.sourceLabel["text"] = fileNamePath[:20] + '...' + os.path.basename(fileNamePath)

        self.numberStats = dt.dataStatistics(self.config, self.dataFile, self.type.get())

        # copy the data source to the JSON config file
        self.config.updateSource(self.type.get(), fileNamePath)

        self.readDataFile(False)
        self.showDataStats()
        self.showDataPlot()

        messagebox.showinfo("Download complete", "The latest data file for the selected game hase been downloaded.")

    def saveDataSource(self):

        response = messagebox.askquestion('Save Data Source', 'Do you want to save the current data source?')

        if response == 'no':
            return

        # copy the data source to the JSON config file
        self.config.updateSource(self.type.get(), self.dataFile)

        messagebox.showinfo("Source File Saved", "The data source file has been saved.")

    def displayDataFile(self):

        ''' This function will display the data file name
        '''

        if self.type.get() == 1:
            self.datLabel['text'] = "Fantasy Five Data"
        if self.type.get() == 2:
            self.datLabel['text'] = "SuperLotto Data"
        if self.type.get() == 3:
            self.datLabel['text'] = "MegaLotto Data"
        if self.type.get() == 4:
            self.datLabel['text'] = "Powerball Data"

        filename = self.config.getSource(self.type.get())

        if os.path.exists(filename):

            self.dataFile = filename
            self.sourceLabel["text"] = os.path.dirname(filename)[:40] + '...' + os.path.basename(filename)

            self.numberStats = dt.dataStatistics(self.config, self.dataFile, self.type.get())

            self.initReadProcess()
            self.showDataStats()
            self.showDataPlot()

        else:
            # delete the contents of the display list, if any
            self.dataSelect.delete(0, END)

            # delete all statistics
            self.numData.delete(0, END)
            self.megaData.delete(0, END)
            #self.patData.delete(0, END)

            # set the source label to None since the data file does not exist or there is no data file saved
            self.sourceLabel["text"] = "None"


    def showGenerate(self):

        ''' This function will show the generate panel depending on the game type
        '''

        if self.type.get() == 1:
            self.showFantasy()
        elif self.type.get() == 2:
            self.showSuper()
        elif self.type.get() == 3:
            self.showMega()
        elif self.type.get() == 4:
            self.showPower()

        lastset = self.config.getLastSet(self.type.get())

        if len(lastset) == 5:
            for i in range(5):
                self.dGen[i].changeTopStyle(lastset[i])

    def showFantasy(self):

        ''' This function will show the Fantasy Five generate pane
        '''

        self.popGen = Toplevel(self.main_container)
        self.popGen.title("Fantasy Five")

        self.h_sep_ga = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gb = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gc = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gd = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_ge = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gf = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gg = Separator(self.popGen, orient=HORIZONTAL)

        self.dGen = []

        for i in range(5):
            self.dGen.append(dg.displayNumbers(self.popGen, self.type.get(), self.config))

        self.genFromPanel = LabelFrame(self.popGen, text='Distribution', style="O.TLabelframe")
        self.topOnly = Radiobutton(self.genFromPanel, text="Select ", style="B.TRadiobutton", variable=self.distribution, value=1)
        self.allNumbers = Radiobutton(self.genFromPanel, text="Non-Select", style="B.TRadiobutton", variable=self.distribution, value=2)
        self.noLastFantasy = Checkbutton(self.popGen, text="Avoid last winner", style="B.TCheckbutton", variable=self.noLastWinner)
        self.genSet = Button(self.popGen, text="GENERATE", style="B.TButton", command=self.generateSet)
        self.genOdd = Button(self.popGen, text="ALL ODD", style="B.TButton", command=self.genOddSet)
        self.genEven = Button(self.popGen, text="ALL EVEN", style="B.TButton", command=self.genEvenSet)
        self.unused = Label(self.popGen, text="Unused: ", style="B.TLabel" )
        self.exitGen = Button(self.popGen, text="EXIT", style="B.TButton", command=self.popGen.destroy)

        self.topOnly.grid(row=1, column=0, padx=5, pady=(5, 0), sticky='W')
        self.allNumbers.grid(row=1, column=1, padx=(10, 5), pady=(5, 0), sticky='W')
        self.genFromPanel.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.noLastFantasy.grid(row=0, column=2, columnspan=2, padx=5, pady=25, sticky='NSEW')
        self.unused.grid(row=0, column=4, columnspan=2, padx=5, pady=25, sticky='NSEW')

        self.h_sep_ga.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionDisplays(5, i)

        self.h_sep_gb.grid(row=16, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        self.genSet.grid(row=17, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.genOdd.grid(row=17, column=3, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.genEven.grid(row=17, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.exitGen.grid(row=18, column=0, columnspan=5, padx=5, pady=(2, 5), sticky='NSEW')

        wh = 355
        ww = 490

        self.popGen.minsize(ww, wh)
        self.popGen.maxsize(ww, wh)

        # Position in center screen

        ws = self.popGen.winfo_screenwidth()
        hs = self.popGen.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popGen.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

        self.distribution.set(1)

    def showSuper(self):

        ''' This function will show the SuperLotto generate panel
        '''

        self.popGen = Toplevel(self.main_container)
        self.popGen.title("SuperLotto")

        self.h_sep_ga = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gb = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gc = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gd = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_ge = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gf = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gg = Separator(self.popGen, orient=HORIZONTAL)

        self.dGen = []

        for i in range(5):
            self.dGen.append(dg.displayNumbers(self.popGen, self.type.get(), self.config))

        self.unused = Label(self.popGen, text="", style="B.TLabel" )
        self.noLastSuper = Checkbutton(self.popGen, text="Avoid numbers from last winner", style="B.TCheckbutton", variable=self.noLastWinner)

        self.genSet = Button(self.popGen, text="GENERATE", style="B.TButton", command=self.generateSet)
        self.genOdd = Button(self.popGen, text="ALL ODD", style="B.TButton", command=self.genOddSet)
        self.genEven = Button(self.popGen, text="ALL EVEN", style="B.TButton", command=self.genEvenSet)
        self.exitGen = Button(self.popGen, text="EXIT", style="B.TButton", command=self.popGen.destroy)

        self.noLastSuper.grid(row=0, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.unused.grid(row=0, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')

        self.h_sep_ga.grid(row=4, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionDisplays(5, i)

        self.h_sep_gb.grid(row=20, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        self.genSet.grid(row=21, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.genOdd.grid(row=21, column=3, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.genEven.grid(row=21, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.exitGen.grid(row=22, column=0, columnspan=5, padx=5, pady=(2, 5), sticky='NSEW')

        wh = 410
        ww = 640

        self.popGen.minsize(ww, wh)
        self.popGen.maxsize(ww, wh)

        # Position in center screen

        ws = self.popGen.winfo_screenwidth()
        hs = self.popGen.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popGen.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

        self.distribution.set(0)

    def showMega(self):

        ''' This function will show the MegaLotto generate panel
        '''

        self.popGen = Toplevel(self.main_container)
        self.popGen.title("MegaLotto")

        self.h_sep_ga = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gb = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gc = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gd = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_ge = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gf = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gg = Separator(self.popGen, orient=HORIZONTAL)

        self.dGen = []

        for i in range(5):
            self.dGen.append(dg.displayNumbers(self.popGen, self.type.get(), self.config))

        self.unused = Label(self.popGen, text="", style="B.TLabel" )
        self.noLastMega = Checkbutton(self.popGen, text="Avoid numbers from last winner", style="B.TCheckbutton", variable=self.noLastWinner)

        self.genSet = Button(self.popGen, text="GENERATE", style="B.TButton", command=self.generateSet)
        self.genOdd = Button(self.popGen, text="ALL ODD", style="B.TButton", command=self.genOddSet)
        self.genEven = Button(self.popGen, text="ALL EVEN", style="B.TButton", command=self.genEvenSet)
        self.exitGen = Button(self.popGen, text="EXIT", style="B.TButton", command=self.popGen.destroy)

        self.noLastMega.grid(row=0, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.unused.grid(row=0, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')

        self.h_sep_ga.grid(row=4, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionDisplays(5, i)

        self.h_sep_gb.grid(row=24, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        self.genSet.grid(row=25, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.genOdd.grid(row=25, column=3, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.genEven.grid(row=25, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.exitGen.grid(row=26, column=0, columnspan=5, padx=5, pady=(2, 5), sticky='NSEW')

        wh = 460
        ww = 640

        self.popGen.minsize(ww, wh)
        self.popGen.maxsize(ww, wh)

        # Position in center screen

        ws = self.popGen.winfo_screenwidth()
        hs = self.popGen.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popGen.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

        self.distribution.set(0)

    def showPower(self):

        ''' This function will show the MegaLotto generate panel
        '''

        self.popGen = Toplevel(self.main_container)
        self.popGen.title("Powerball")

        self.h_sep_ga = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gb = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gc = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gd = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_ge = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gf = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gg = Separator(self.popGen, orient=HORIZONTAL)

        self.dGen = []

        for i in range(5):
            self.dGen.append(dg.displayNumbers(self.popGen, self.type.get(), self.config))

        self.unused = Label(self.popGen, text="", style="B.TLabel" )
        self.noLastPower = Checkbutton(self.popGen, text="Avoid numbers from last winner", style="B.TCheckbutton", variable=self.noLastWinner)

        self.genSet = Button(self.popGen, text="GENERATE", style="B.TButton", command=self.generateSet)
        self.genOdd = Button(self.popGen, text="ALL ODD", style="B.TButton", command=self.genOddSet)
        self.genEven = Button(self.popGen, text="ALL EVEN", style="B.TButton", command=self.genEvenSet)
        self.exitGen = Button(self.popGen, text="EXIT", style="B.TButton", command=self.popGen.destroy)

        self.noLastPower.grid(row=0, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.unused.grid(row=0, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')

        self.h_sep_ga.grid(row=4, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionDisplays(5, i)

        self.h_sep_gb.grid(row=25, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        self.genSet.grid(row=26, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.genOdd.grid(row=26, column=3, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.genEven.grid(row=26, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.exitGen.grid(row=27, column=0, columnspan=5, padx=5, pady=(2, 5), sticky='NSEW')

        wh = 460
        ww = 640

        self.popGen.minsize(ww, wh)
        self.popGen.maxsize(ww, wh)

        # Position in center screen

        ws = self.popGen.winfo_screenwidth()
        hs = self.popGen.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popGen.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

        self.distribution.set(0)

    def showProgress(self):

        ''' This function will show the progress bar for the different threads
        '''

        Style().configure("P.TLabel", font="Verdana 12 bold", anchor="center")
        Style().configure("B.TProgressbar", foreground="blue", background="blue")

        self.popProgress = Toplevel(self.main_container)
        self.popProgress.title("Processing")

        self.progressMessage = Label(self.popProgress, text="Processing, please wait...", style="P.TLabel" )
        self.progressBar = Progressbar(self.popProgress, orient="horizontal", mode="indeterminate", length=280)

        self.progressMessage.grid(row=0, column=0, columnspan=5, padx=10 , pady=5, sticky='NSEW')
        self.progressBar.grid(row=1, column=0, columnspan=5, padx=10 , pady=5, sticky='NSEW')

        wh = 70
        ww = 300

        self.popProgress.minsize(ww, wh)
        self.popProgress.maxsize(ww, wh)

        # Position in center screen

        ws = self.popProgress.winfo_screenwidth()
        hs = self.popProgress.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popProgress.geometry('%dx%d+%d+%d' % (ww, wh, x, y))
        self.progressBar.start()

    def hideProgress(self):

        self.progressBar.stop()
        self.popProgress.destroy()


    def readDataFile(self, filter=False):

        ''' This function will check for close matches to the numbers entered
        '''

        # Set indicator for finding exact match to False
        self.exactMatch = False

        # delete the contents of the list
        self.dataSelect.delete(0, END)

        filename = self.dataFile

        try:
            dataFile = open(filename, "r")
        except:
            return

        while True:

            d_line = dataFile.readline()

            if d_line == "":
                break

            d_list = d_line.split()

            if len(d_list) > 0:

                if d_list[0].isdigit():

                    winner = []

                    for i in range(5, 10):
                        winner.append(int(d_list[i]))

                    if len(d_list) > 10:
                        winner_extra = int(d_list[10])
                    else:
                        winner_extra = ''

                    if filter:
                        self.filterData(winner, winner_extra, d_line)
                    else:
                        self.formatDataLine(d_line, 0, 0)


        dataFile.close()

        self.scroller.config(command=self.dataSelect.yview)

    def filterData(self, winner, winner_extra, d_line):

        if len(d_line.split()) > 10:
            search_extra = int(self.numberExtra.get())
        else:
            search_extra = 0

        match_ctr = 0

        if self.numberA.get():
            match_ctr += winner.count(int(self.numberA.get()))

        if self.numberB.get():
            match_ctr += winner.count(int(self.numberB.get()))

        if self.numberC.get():
            match_ctr += winner.count(int(self.numberC.get()))

        if self.numberD.get():
            match_ctr += winner.count(int(self.numberD.get()))

        if self.numberE.get():
            match_ctr += winner.count(int(self.numberE.get()))

        if (match_ctr == 3 and self.getMatch3.get() == 1) or  (match_ctr == 4 and self.getMatch4.get() == 1) or (match_ctr == 5 and self.getMatch5.get() == 1):
            if search_extra == winner_extra and self.getMatchExtra.get() == 1:
                self.formatDataLine(d_line, match_ctr, 1)
            else:
                self.formatDataLine(d_line, match_ctr, 0)
        else:
            if search_extra == winner_extra and self.getMatchExtra.get() == 1:
                self.formatDataLine(d_line, match_ctr, 1)


    def formatDataLine(self, data_line, match_ctr, super_ctr):

        data_list = data_line.split()

        winner_data = []

        # Format draw number
        draw_number = '{:06d}'.format(int(data_list[0]))

        winner_data.append(draw_number)

        in_date = data_list[2] + ' ' + data_list[3] + ' ' + data_list[4]
        draw_date = str(datetime.datetime.strptime(in_date, '%b %d, %Y').date())

        winner_data.append(draw_date)

        for i in range(5, 10):
            number = '{:02d}'.format(int(data_list[i]))
            winner_data.append(number)

        winner_data.append(str(match_ctr))

        if len(data_list) > 10:
            winner_data.append('{:02d}'.format(int(data_list[10])))
            winner_data.append(str(super_ctr))

        format_data_line = "   |   ".join(winner_data)

        self.dataSelect.insert(END, format_data_line)


    def filterProcess(self):

        if self.getMatch3.get() == 0 and self.getMatch4.get() == 0 and self.getMatch5.get() == 0 and self.getMatchExtra.get() == 0:

            self.getMatch3.set(1)
            self.getMatch4.set(1)
            self.getMatch5.set(1)
            self.getMatchExtra.set(1)

        self.readDataFile(True)

    def initReadProcess(self):

        self.getMatch3.set(0)
        self.getMatch4.set(0)
        self.getMatch5.set(0)
        self.getMatchExtra.set(0)

        self.numberA.set('')
        self.numberB.set('')
        self.numberC.set('')
        self.numberD.set('')
        self.numberE.set('')
        self.numberExtra.set('')

        self.readDataFile(False)

    def showDataStats(self):

        self.numData.delete(0, END)
        self.megaData.delete(0, END)

        num_stats, meg_stats, pat_stats, last_match_draws, max_gap = self.numberStats.getDataStatistics()

        for k, v in num_stats.items():

            num_stat = []

            num_stat.append('{:02d}'.format(k))
            num_stat.append('{:02d}'.format(v))

            format_nstat = "    -    ".join(num_stat)
            self.numData.insert(END, format_nstat)

        self.numscroller.config(command=self.numData.yview)

        if len(meg_stats) > 0:

            for k, v in meg_stats.items():

                meg_stat = []

                meg_stat.append('{:02d}'.format(k))
                meg_stat.append('{:02d}'.format(v))

                format_mstat = "    -    ".join(meg_stat)
                self.megaData.insert(END, format_mstat)

            self.megascroller.config(command=self.megaData.yview)

        if last_match_draws == 0:
            self.lastMatchDrawInfo ['text']= "Number of draws since last winner: NA"
            self.maxGapInfo ['text'] = "Maximum draw gap: NA"
        else:
            self.lastMatchDrawInfo ['text']= "Number of draws since last winner: {}".format(last_match_draws)
            self.maxGapInfo ['text'] = "Maximum draw gap:  {}".format(max_gap)

        self.pat5O['text'] = '5O - ' + str(pat_stats['5O'])
        self.pat4O['text'] = '4O - ' + str(pat_stats['4O'])
        self.pat3O['text'] = '3O - ' + str(pat_stats['3O'])
        self.pat3E['text'] = '3E - ' + str(pat_stats['3E'])
        self.pat4E['text'] = '4E - ' + str(pat_stats['4E'])
        self.pat5E['text'] = '5E - ' + str(pat_stats['5E'])

        '''
        for k, v in pat_stats.items():
            pat_stat = []

            pat_stat.append(k)
            pat_stat.append('{:02d}'.format(v))

            format_pstat = "   -   ".join(pat_stat)
            self.patData.insert(END, format_pstat)

        self.patscroller.config(command=self.patData.yview)
        '''

    def showDataPlot(self):

        image = Image.open("data\\results.jpg")
        image = image.resize((400,215))
        results_fig = ImageTk.PhotoImage(image)

        # Define a style
        root.results_fig = results_fig
        Style().configure("DT.TLabel", image=results_fig, background="white", anchor="left", font="Verdana 2")

        self.resultsPlot['style'] = 'DT.TLabel'

    def sortNumbers(self):

        self.numData.delete(0, END)

        num_stats, _, _, _, _ = self.numberStats.getDataStatistics()

        if self.numSort['text'] == 'SORT BY NUMBERS':
            ncounts = num_stats
            check = False
            self.numSort['text'] = 'SORT BY COUNT'
        else:
            sorted_num = sorted(num_stats.items(), key=operator.itemgetter(1), reverse=True)
            ncounts = {num:count for num, count in sorted_num}
            check = True
            self.numSort['text'] = 'SORT BY NUMBERS'

        check_count = 0

        for k, v in ncounts.items():

            check_count += 1

            if check_count == 26 and check:
                self.numData.insert(END, '================')

            num_stat = []

            num_stat.append('{:02d}'.format(k))
            num_stat.append('{:02d}'.format(v))

            format_nstat = "    -    ".join(num_stat)
            self.numData.insert(END, format_nstat)

        self.numscroller.config(command=self.numData.yview)


    def sortMegas(self):

        self.megaData.delete(0, END)

        _, meg_stats, _, _, _ = self.numberStats.getDataStatistics()

        if len(meg_stats) == 0:
            return

        if self.megaSort['text'] == 'SORT BY NUMBERS':
            mcounts = meg_stats
            self.megaSort['text'] = 'SORT BY COUNT'
        else:
            sorted_meg = sorted(meg_stats.items(), key=operator.itemgetter(1), reverse=True)
            mcounts = {num:count for num, count in sorted_meg}
            self.megaSort['text'] = 'SORT BY NUMBERS'

        for k, v in mcounts.items():

            meg_stat = []

            meg_stat.append('{:02d}'.format(k))
            meg_stat.append('{:02d}'.format(v))

            format_mstat = "    -    ".join(meg_stat)
            self.megaData.insert(END, format_mstat)

        self.megascroller.config(command=self.megaData.yview)

    def refreshDataGraph(self):

        self.numberStats.analyzeData()
        self.showDataStats()
        self.showDataPlot()


root = Tk()
root.title("TOP NUMBERS")

# Set size

wh = 680
ww = 480

#root.resizable(height=False, width=False)

root.minsize(ww, wh)
root.maxsize(ww, wh)

# Position in center screen

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (ww/2)
y = (hs/2) - (wh/2)

root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

app = Application(root)

root.mainloop()
