import tkinter as tk
from tkinter import filedialog
import pandas as pd
import glob
import numpy as np
#import matplotlib.pyplot as plt
import itertools
import os, sys
from fnmatch import fnmatch
import tkinter.font as tkFont

class TkFileDialogExample(tk.Frame):

  def __init__(self, root):

    tk.Frame.__init__(self, root)

    #define widgets
    fontStyle = tkFont.Font(family="Lucida Grande", size=14)
    titleFontStyle = tkFont.Font(family="Lucida Grande", size=20)
    
    tk.Label(self, text = 'READ THIS FIRST!!!!!!!', font = titleFontStyle).grid(row = 0, column = 0, columnspan = 2)
    tk.Label(self, text = 'Type in any new volunteer positions in the box at the bottom', font = fontStyle).grid(row = 1, column = 0, columnspan = 2)
    tk.Label(self, text = "Format is [VolunteerPosition], [Points];", font = fontStyle).grid(row = 2, column = 0, columnspan = 2)
    tk.Label(self, text = 'Must use comma between name and points.', font = fontStyle).grid(row = 3, column = 0, columnspan = 2)
    tk.Label(self, text = 'Must use semicolon after points', font = fontStyle).grid(row = 4, column = 0, columnspan = 2)
    tk.Label(self, text = 'Example: Treasurer,5; Vice President,10; ', font = fontStyle).grid(row = 5, column = 0, columnspan = 2)
    tk.Label(self, text = 'Click RUN and select requested csv files',font = fontStyle).grid(row = 6, column = 0, columnspan = 2)
    
    tk.Label(self, text = "", font = fontStyle).grid(row = 7, column = 0)
    tk.Label(self, text = "Fill Additional Volunteer Positions Below (if none, leave empty):", font = fontStyle).grid(row = 8, column = 0)
    self.AdditionalVolunteerEntry = tk.StringVar()
    tk.Entry(self, textvariable = self.AdditionalVolunteerEntry).grid(row = 9, column = 0, columnspan = 2 ,rowspan = 3, sticky = 'nesw')
    
    tk.Button(self, text='RUN', command=self.askopenfilename).grid(row = 12, column = 1, columnspan = 2)

    # define options for opening or saving a file
    self.file_opt = options = {}
    options['defaultextension'] = '.csv'
    options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['initialfile'] = 'myfile.txt'
    options['parent'] = root
    options['title'] = 'Select Volunteer List File'

    # This is only available on the Macintosh, and only when Navigation Services are installed.
    #options['message'] = 'message'

    # if you use the multiple file version of the module functions this option is set automatically.
    #options['multiple'] = 1

    # defining options for opening a directory
    self.contactFile_opt = contactFileoptions = {}
    contactFileoptions['defaultextension'] = '.csv'
    contactFileoptions['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    contactFileoptions['initialdir'] = 'C:\\'
    contactFileoptions['initialfile'] = 'myfile.txt'
    contactFileoptions['parent'] = root
    contactFileoptions['title'] = 'Select Contacts List File'


  DuplicateExists = False
  def askopenfilename(self):

    """Returns an opened file in read mode.
    This time the dialog just returns a filename and the file is opened by your own code.
    """
    
    #self.VolunteerPointsDict("Rider - Very Short").value = int(self.AdditionalVolunteerEntry.get())
    parseVolunteerEntryIsGood = True
    if(len(self.AdditionalVolunteerEntry.get()) != 0):
       parseVolunteerEntryIsGood = self.parseAdditionalVolunteers(self.AdditionalVolunteerEntry.get())
       
    if (parseVolunteerEntryIsGood == False):
        return

    #get filename
    volunteerListFilename = filedialog.askopenfilename(**self.file_opt)
    #print(riderListFilename)
    
    contactListFilename = filedialog.askopenfilename(**self.contactFile_opt)
    #print(contactListFilename)
    
    # open file on your own
    if volunteerListFilename:
       self.volunteerFileStuff(volunteerListFilename)
       
    # open file on your own
    if contactListFilename:
       self.contactFileStuff(contactListFilename)
    
    return


  EventFileHeaderNames = ['Registration type/Invitee reply']
  EventFileOtherHeaderNames = ['First name', 'Last name']
  EventCompleteFirstNames = []
  EventCompleteLastNames = []
  VolunteerIds = []
  VolunteerPoints = []
  EventCompleteUserIdList = []
  
  VolunteerPointsDict = {
    "No-Drop Leader" : 2,
    "Food Purchaser" : 3,
    "Officer in Charge" : 4,
    "Registration Host" : 5,
    "Lead SAG" : 6,
    "Volunteer - SAG" : 10
    }  


  def volunteerFileStuff (self, volunteerFilename):
    dfs = pd.read_csv(volunteerFilename)
    dfs.columns = dfs.columns.str.strip()
    
    tempRegistrationTypeList = []
    
    
    self.EventCompleteFirstNames.clear()
    self.EventCompleteLastNames.clear()
    self.VolunteerIds.clear()
    self.VolunteerPoints.clear()
    self.EventCompleteUserIdList.clear()
    
    self.EventCompleteFirstNames = dfs['First name'].tolist()
    self.EventCompleteLastNames = dfs['Last name'].tolist()
    
    #rint eventCompleteFirstNames
    #print eventCompleteLastNames
    
    #print dfs
    for headerNameIndex, value in enumerate (self.EventFileHeaderNames):
        tempRegistrationTypeList = dfs[value].tolist()
        self.EventCompleteUserIdList = dfs['User ID'].tolist()
        
        for registrationTypeIndex, registrationValue in enumerate (tempRegistrationTypeList):
            for key in self.VolunteerPointsDict:
                #print (key)
                if key in registrationValue:
                    self.VolunteerIds.append(self.EventCompleteUserIdList[registrationTypeIndex])
                    self.VolunteerPoints.append((self.VolunteerPointsDict[key]))
                    #print (registrationTypeIndex)



  ListOfDuplicates = []
  def checkIfDuplicates(self, listOfElems):
    ''' Check if given list contains any duplicates '''    
    setOfElems = set()
    del self.ListOfDuplicates [:]
    for elem in listOfElems:
        if elem in setOfElems:
            self.ListOfDuplicates.append(elem)
        else:
            setOfElems.add(elem)         
    
    if(len(self.ListOfDuplicates) > 0):
        return True
    else:
        return False


  ContactsFileHeaderNames = ['User ID', 'Volunteer Points', 'Membership level']
  def contactFileStuff (self, contactFileName):
    df = pd.read_csv(contactFileName)
    df.columns = df.columns.str.strip()
    
    ContactsUserIDList = df[self.ContactsFileHeaderNames[0]].tolist()
    TotalVolunteerPointsList = df[self.ContactsFileHeaderNames[1]].tolist()
    MembershipLevelList = df[self.ContactsFileHeaderNames[2]].tolist()
    
    #generate output file
    for userIdIndex, userIdToUpdate in enumerate (self.VolunteerIds):
        #print userIdToUpdate
        indexToUpdate = ContactsUserIDList.index(userIdToUpdate)
        #print 'TotalVolunteerPointsList before' + str(TotalVolunteerPointsList)
        TotalVolunteerPointsList[indexToUpdate] = TotalVolunteerPointsList[indexToUpdate] + self.VolunteerPoints[userIdIndex]
        
        processedDf = pd.DataFrame()
        processedDf['User ID'] = ContactsUserIDList
        processedDf['Volunteer Points'] = TotalVolunteerPointsList
        processedDf['Membership level'] = MembershipLevelList
        processedDf.to_csv('volunteerPointsOutput.csv', sep=',')
        print ("Output File Generated")
        self.popupmsgOutputGenerated()


  ListOfDuplicatesFullName = []
  def printDuplicates (self, 
                        listOfDuplicates, 
                        listEventCompleteUserIds, 
                        listEventCompleteFirstNames,
                        listEventCompleteLastNames):
    self.ListOfDuplicatesFullName.clear()
    for elements in listOfDuplicates:
        #print (listOfDuplicates)
        #print (elements)
        #print (len(listEventCompleteUserIds))
        #print (listEventCompleteUserIds)
        #print ("indexNeeded")
        indexNameNeeded = listEventCompleteUserIds.index(elements)
        #print (indexNameNeeded)
        #print (len(listEventCompleteFirstNames))
        #print (len(listEventCompleteLastNames))
        #print ("This rider has duplicate entries " + listEventCompleteFirstNames[indexNameNeeded] + " " + listEventCompleteLastNames[indexNameNeeded])
        #print ("Delete same entry from events list and rerun code")
        self.ListOfDuplicatesFullName.append(listEventCompleteFirstNames[indexNameNeeded] + " " + listEventCompleteLastNames[indexNameNeeded])
    fullMsgString = ""
    for fullNames in self.ListOfDuplicatesFullName:
        fullMsgString = fullMsgString + fullNames + ", "
    self.popupmsg(fullMsgString)
        
  def popupmsg(self, msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text= "")
    label.pack(side="top", fill="x", pady=10)
    label = tk.Label(popup, text= msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()
    
  def popupmsgOutputGenerated(self):
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text= "Output file generated in the same folder as your input files")
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()
    
  def parseAdditionalVolunteers(self, stringInput):
    foundCommaCount = 0
    foundSemiColonCount = 0
    commaLocationList = []
    semiColonLocationList = []
    newPositionNameList = []
    newPositionPointsList = []
    startIndex = 0
    
    #find comma and semicolon and store their index
    for index, letter in enumerate (stringInput):
         if letter == ',':
            foundCommaCount += 1
            commaLocationList.append(index)
            newPositionNameList.append(str.strip(stringInput[startIndex:index]))
            startIndex = index + 1
         elif letter == ';':
            foundSemiColonCount += 1
            semiColonLocationList.append(index)
            newPositionPointsList.append(int(str.strip(stringInput[startIndex:index])))
            startIndex = index + 1
            
    #print ("Comma location list" + str(len(commaLocationList)))
    #print ("Semi location list" + str(len(semiColonLocationList)))
    #print (newPositionNameList)
    #print (newPositionPointsList)
    
    #error if we don't have the same number of comma and semicolon
    if len(commaLocationList) != len(semiColonLocationList):
        #print ("ERROR COMMA not equal SEMICOLON")
        self.popupmsg("ERROR: Check additional volunteer input format (note the comma and semicolon). It should be volunteerPostionName, Points ; eg. Treasurer, 5;")
        return False
    
    for positionIndex, positionName in enumerate(newPositionNameList):
        updateVal = {positionName: newPositionPointsList[positionIndex]}
        self.VolunteerPointsDict.update(updateVal)
        #print (self.VolunteerPointsDict)

if __name__=='__main__':
  root = tk.Tk()
  root.title("Volunteer Points")
  #TkFileDialogExample(root).pack()
  #root.mainloop()
  TkFileDialogExample(root).grid(row = 0, column = 0)
  root.mainloop()
