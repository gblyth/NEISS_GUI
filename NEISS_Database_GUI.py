#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 21:11:07 2018

@author: Gavin
"""


import requests
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import simpledialog
from tkinter import ttk
import datetime

class NEISS_Data_Requester(object):
    def __init__(self, master):
        self.years=[]
        self.data=[]
        self.case=[]
        self.num_cases=0
        self.num_n_cases=0
        self.master=master
        self.var1=IntVar()
        self.var2=IntVar()
        self.var3=IntVar()
        self.var4=IntVar()
        self.var5=IntVar()
        self.var6=IntVar()
        self.var7=IntVar()
        self.var8=IntVar()
        self.var9=IntVar()
        self.var10=IntVar()
        self.var11=IntVar()
        self.var12=IntVar()
        self.var13=IntVar()
        self.var14=IntVar()
        self.var15=IntVar()
        self.var16=IntVar()
        self.var17=IntVar()
        self.var18=IntVar()
        self.var19=IntVar()
        self.var20=IntVar()
        self.progress=ttk.Progressbar(self.master, orient=HORIZONTAL, length=100, mode='determinate')
#        self.progress2=ttk.Progressbar(self.master, orient=HORIZONTAL, length=100, mode='determinate')
        self.data_years=StringVar()
        self.data_years.set("Years of Data Loaded=\nNone")
        self.data_events=StringVar()
        self.data_events.set("Number of Injury Events Loaded=\nNone")
        self.data_loaded=False
        self.file_to_dl=False
#        self.status_str=StringVar()
#        self.status_str.set("Status: Datasets Loaded="+str(self.data_loaded)+
#                           "File Ready To Download="+str(self.file_to_dl)+
#                           "Years of Data Loaded=None"+
#                           "Number of Injury Events Loaded=None"+
#                           "Number of Cases:"+str(self.num_cases)+" Number of Non-Cases:"+str(self.num_n_cases))
        self.load_str=StringVar()
        self.load_str.set("Datasets Loaded=\n"+str(self.data_loaded))
        self.dl_str=StringVar()
        self.dl_str.set("File Ready To Download=\n"+str(self.file_to_dl))
        self.progress_str=StringVar()
        self.progress_str.set("Ready")
        self.entry1=StringVar()
        self.entry1.set("(MM/DD/YYYY)or(MM/DD/YYYY-MM/DD/YYYY)")
        self.entry2=StringVar()
        self.entry2.set("singlular(#) or range(#-#)")
        self.entry3=StringVar()
        self.entry3.set("Male or Female or Not Recorded")
        self.entry4=StringVar()
        self.entry4.set("Enter as: #0,#1,#2,#3,#4,#5,#6")
#        self.entry5=StringVar()
#        self.entry5.set("Enter as: #0,#1,#2,#3,#4,#5,#6")
        self.entry6=StringVar()
        self.entry6.set("Enter as: #1,#2,ect...")
        self.entry7=StringVar()
        self.entry7.set("Enter as: #1,#2,ect...")
#        self.entry8=StringVar()
#        self.entry8.set("Enter as: #1,#2,ect...")
        self.entry9=StringVar()
        self.entry9.set("Enter as: #1,#2,#4,#5,#6,#8,#9")
        self.entry10=StringVar()
        self.entry10.set("Enter as: #0,#1,#2,#4,#5,#6,#7,#8,#9")
        self.entry11=StringVar()
        self.entry11.set("Enter as: #0,#1,#2,#3")
        self.entry12=StringVar()
        self.entry12.set("Enter as: #1,#2,ect...")
#        self.entry13=StringVar()
#        self.entry13.set("Enter as: #1,#2,ect...")
        self.entry14=StringVar()
        self.entry14.set("Enter as: Word1,Word2,ect...")
        self.entry15=StringVar()
        self.entry15.set("Enter as: \" \", \"C\",\"L\",\"M\",\"S\",\"V\"")
        self.entry16=StringVar()
        self.entry16.set("Enter as: #1,#2,ect...")
        self.case_num=StringVar()
        self.case_num.set("Number of Cases:"+str(self.num_cases)+" Number of Non-Cases:"+str(self.num_n_cases))
        
    def varStates(self):
                
        self.years=[("1998", self.var1.get()),
                   ("1999", self.var2.get()),
                   ("2000", self.var3.get()),
                   ("2001", self.var4.get()),
                   ("2002", self.var5.get()),
                   ("2003", self.var6.get()),
                   ("2004", self.var7.get()),
                   ("2005", self.var8.get()),
                   ("2006", self.var9.get()),
                   ("2007", self.var10.get()),
                   ("2008", self.var11.get()),
                   ("2009", self.var12.get()),
                   ("2010", self.var13.get()),
                   ("2011", self.var14.get()),
                   ("2012", self.var15.get()),
                   ("2013", self.var16.get()),
                   ("2014", self.var17.get()),
                   ("2015", self.var18.get()),
                   ("2016", self.var19.get()),
                   ("2017", self.var20.get())]
        self.loadFiles()
        
    def updateProgress(self, number, total):
#        print("Number:",number,"of",total)
        value=int((number/total)*100)
        self.progress['value']=value
        self.master.update_idletasks()
        
#    Needed to remove this method because it take way too long... maybe multithread it?
    def updateProgress2(self, number, total):
        value=int((number/total)*100)
        self.progress2['value']=value
        self.master.update_idletasks()
        
    def loadFiles(self):
        self.progress_str.set("Downloading Files")
        self.master.update_idletasks()
        self.data=[]
        years_down=[]
        if(len(self.years)>0):
            tot_years=0
            for year in self.years:
                if(year[1]==1):
                    tot_years+=1
            load_count=0
            for i in range(len(self.years)):
                if(self.years[i][1]==1):
                    years_down.append(self.years[i][0])
                    path=str('https://www.cpsc.gov/cgibin/NEISSQuery/Data/Archived%20Data/'+
                          self.years[i][0]+'/neiss'+self.years[i][0]+'.tsv')
#                    temp=[]
# Example of the http:  https://raw.githubusercontent.com/gblyth/NEISS_GUI/master/Bin%20Files/NEISS_1998Q1.bin
                    r=requests.get(path)
                    r_data=r.text.split("\n")
                    if(len(self.data)==0):
                        for row in r_data:
                            self.data.append(row.split("\t"))
                    else:
                        for row in range(1,len(r_data)):
                            self.data.append(r_data[row].split("\t"))
                    load_count+=1
                    self.updateProgress(load_count,tot_years)
#        print("Years downloaded are:\n",years_down)
        self.data_loaded=True
        self.file_to_dl=True
#        self.status_str.set("Status: Datasets Loaded="+str(self.data_loaded)+
#                           "File Ready To Download="+str(self.file_to_dl)+
#                           "Years of Data Loaded="+str(years_down)+
#                           "Number of Injury Events Loaded="+str(len(self.data)-1)+
#                           "Number of Cases:"+str(self.num_cases)+" Number of Non-Cases:"+str(self.num_n_cases))
        self.data_years.set("Years of Data Loaded=\n"+str(years_down))
        self.data_events.set("Number of Injury Events Loaded=\n"+str(len(self.data)-1))
        self.load_str.set("Datasets Loaded=\n"+str(self.data_loaded))
        self.dl_str.set("File Ready To Download=\n"+str(self.file_to_dl))
        self.master.update_idletasks()
        
### This version of loading NEISS data is my cheating method - before Nick and Andy gave me the link used above
    def oldloadFiles(self):
        self.data=[]
        years_down=[]
        if(len(self.years)>0):
            tot_years=0
            for year in self.years:
                if(year[1]==1):
                    tot_years+=1
            load_count=0
            for i in range(len(self.years)):
                if(self.years[i][1]==1):
                    years_down.append(self.years[i][0])
#                    temp=[]
# Example of the http:  https://raw.githubusercontent.com/gblyth/NEISS_GUI/master/Bin%20Files/NEISS_1998Q1.bin
                    r=requests.get('https://raw.githubusercontent.com/gblyth/NEISS_GUI/master/Bin%20Files/NEISS_'+
                                   self.years[i][0]+'Q1.bin')
                    r_data=r.text.split("\n")
                    if(len(self.data)==0):
                        for row in r_data:
                            self.data.append(row.split("\t"))
                    else:
                        for row in range(1,len(r_data)):
                            self.data.append(r_data[row].split("\t"))
                    load_count+=1
                    self.updateProgress(load_count,(tot_years*4))
                    r=requests.get('https://raw.githubusercontent.com/gblyth/NEISS_GUI/master/Bin%20Files/NEISS_'+
                                   self.years[i][0]+'Q2.bin')
                    r_data=r.text.split("\n")
                    for row in range(1,len(r_data)):
                        self.data.append(r_data[row].split("\t"))
                    load_count+=1
                    self.updateProgress(load_count,(tot_years*4))
                    r=requests.get('https://raw.githubusercontent.com/gblyth/NEISS_GUI/master/Bin%20Files/NEISS_'+
                                   self.years[i][0]+'Q3.bin')
                    r_data=r.text.split("\n")
                    for row in range(1,len(r_data)):
                        self.data.append(r_data[row].split("\t"))
                    load_count+=1
                    self.updateProgress(load_count,(tot_years*4))
                    r=requests.get('https://raw.githubusercontent.com/gblyth/NEISS_GUI/master/Bin%20Files/NEISS_'+
                                   self.years[i][0]+'Q4.bin')
                    r_data=r.text.split("\n")
                    for row in range(1,len(r_data)):
                        self.data.append(r_data[row].split("\t"))
                    load_count+=1
                    self.updateProgress(load_count,(tot_years*4))
#                    self.data.append(temp)
        print("Years downloaded are:\n",years_down)
        self.data_loaded=True
        self.file_to_dl=True
#        self.status_str.set("Status: Datasets Loaded="+str(self.data_loaded)+
#                           "File Ready To Download="+str(self.file_to_dl)+
#                           "Years of Data Loaded="+str(years_down)+
#                           "Number of Injury Events Loaded="+str(len(self.data)-1)+
#                           "Number of Cases:"+str(self.num_cases)+" Number of Non-Cases:"+str(self.num_n_cases))
        self.data_years.set("Years of Data Loaded=\n"+str(years_down))
        self.data_events.set("Number of Injury Events Loaded=\n"+str(len(self.data)-1))
        self.load_str.set("Datasets Loaded=\n"+str(self.data_loaded))
        self.dl_str.set("File Ready To Download=\n"+str(self.file_to_dl))
        self.master.update_idletasks()
        
    def setFileName(self):
        import os
        root=Tk()
        cmd = """osascript -e 'tell app "Finder" to set frontmost of process "Python" to true'"""
        os.system(cmd)
        root.withdraw()
        new_window=simpledialog.askstring("File Name","Please Name Your File:")
        root.destroy()
        return new_window
        
    
    def downloadFiles(self):
        place=askdirectory()
        print("Place=",place)
        name=self.setFileName()
        if(type(name)==str):
            name=name.split(" ")
            name="_".join(name)
            print("Name=",name)
            path=place+"/"+name
            print("File path=\n",path)

            output_file=open(str(str(place)+"/"+str(name)+".tsv"), 'w')

            if(len(self.case)>0):
                for row in range(len(self.data)):
                    output_file.write("\t".join(self.data[row])+"\t"+str(self.case[row])+"\n")
            else:
                for row in self.data:
                    output_file.write("\t".join(row)+"\n")
            output_file.close()

    
    def clearCase(self):
        self.case=[]
        self.num_cases=0
        self.num_n_cases=0
        self.entry1.set("(MM/DD/YYYY)or(MM/DD/YYYY-MM/DD/YYYY)")
        self.entry2.set("singlular(#) or range(#-#)")
        self.entry3.set("Male or Female or Not Recorded")
        self.entry4.set("Enter as: #0,#1,#2,#3,#4,#5,#6")
#        self.entry5.set("Enter as: #0,#1,#2,#3,#4,#5,#6")
        self.entry6.set("Enter as: #1,#2,ect...")
        self.entry7.set("Enter as: #1,#2,ect...")
#        self.entry8.set("Enter as: #1,#2,ect...")
        self.entry9.set("Enter as: #1,#2,#4,#5,#6,#8,#9")
        self.entry10.set("Enter as: #0,#1,#2,#4,#5,#6,#7,#8,#9")
        self.entry11.set("Enter as: #0,#1,#2,#3")
        self.entry12.set("Enter as: #1,#2,ect...")
#        self.entry13.set("Enter as: #1,#2,ect...")
        self.entry14.set("Enter as: Word1,Word2,ect...")
        self.entry15.set("Enter as: \" \", \"C\",\"L\",\"M\",\"S\",\"V\"")
        self.entry16.set("Enter as: #1,#2,ect...")
        self.case_num.set("Number of Cases:"+str(self.num_cases)+" Number of Non-Cases:"+str(self.num_n_cases))
        self.updateProgress(0,len(self.data))
#        self.updateProgress2(0,len(self.data))
        self.master.update_idletasks()
        
        
    def checkCase(self):
        check=[]
        for i in range(16):
            check.append("")
        e1=str(self.entry1.get())
        e2=str(self.entry2.get())
        e3=str(self.entry3.get())
        e4=str(self.entry4.get())
#        e5=self.entry5.get()
        e6=str(self.entry6.get())
        e7=str(self.entry7.get())
#        e8=self.entry8.get()
        e9=str(self.entry9.get())
        e10=str(self.entry10.get())
        e11=str(self.entry11.get())
        e12=str(self.entry12.get())
#        e13=self.entry13.get()
        e14=str(self.entry14.get())
        e15=str(self.entry15.get())
        e16=str(self.entry16.get())
        if(e1!="(MM/DD/YYYY)or(MM/DD/YYYY-MM/DD/YYYY)" and e1!=""):
            temp=e1.split("-")
            if(len(temp)==2):
                try:
                    checkit=datetime.datetime.strptime(temp[0], '%m/%d/%Y')
                    try:
                        checkit=datetime.datetime.strptime(temp[1], '%m/%d/%Y')
                        check[0]=e1.split("-")
                    except ValueError:
                        print("Dates Entered Incorrrectly")
                except ValueError:
                    print("Dates Entered Incorrrectly")
            elif(len(temp)==1):
                try:
                    checkit=datetime.datetime.strptime(temp[0], '%m/%d/%Y')
                    check[0]=e1
                except ValueError:
                    print("Dates Entered Incorrrectly")
#            check[0]=e1.split("-")
        if(e2!="singlular(#) or range(#-#)" and e2!=""):
            temp=e2.split("-")
            if(len(temp)==1):
                try:
                    checkit=int(temp[0])
                    check[1]=e2
                except ValueError:
                    print("Please re-enter as a number")
            elif(len(temp)==2):
                try:
                    checkit=int(temp[0])
                    try:
                        checkit=int(temp[1])
                        check[1]=e2.split("-")
                    except ValueError:
                        print("Please re-enter range in numbers")
                except ValueError:
                    print("Please re-enter range in numbers")
            check[1]=e2.split("-")
        if(e3!="Male or Female or Not Recorded" and e3!=""):
            if(e3.lower()=="male" or e3.lower()=="m"):
                check[2]='1'
            elif(e3.lower()=="female" or e3.lower()=="f"):
                check[2]='2'
            elif(e3.lower()=="not recorded" or e3.lower()=="nr"):
                check[2]='0'
        if(e4!="Enter as: #0,#1,#2,#3,#4,#5,#6" and e4!=""):
            check[3]=e4.split(",")
#        if(e5!="Enter as: #0,#1,#2,#3,#4,#5,#6" and e5!=""):
#            check[4]=e5.split(",")
        if(e6!="Enter as: #1,#2,ect..." and e6!=""):
            check[5]=e6.split(",")
        if(e7!="Enter as: #1,#2,ect..." and e7!=""):
            check[6]=e7.split(",")
#        if(e8!="Enter as: #1,#2,ect..." and e8!=""):
#            check[7]=e8.split(",")
        if(e9!="Enter as: #1,#2,#4,#5,#6,#8,#9" and e9!=""):
            check[8]=e9.split(",")
        if(e10!="Enter as: #0,#1,#2,#4,#5,#6,#7,#8,#9" and e10!=""):
            check[9]=e10.split(",")
        if(e11!="Enter as: #0,#1,#2,#3" and e11!=""):
            check[10]=e11.split(",")
        if(e12!="Enter as: #1,#2,ect..." and e12!=""):
            check[11]=e12.split(",")
#        if(e13!="Enter as: #1,#2,ect..." and e13!=""):
#            check[12]=e13.split(",")
        if(e14!="Enter as: Word1,Word2,ect..." and e14!=""):
            check[13]=e14.split(",")
        if(e15!="Enter as: \" \", \"C\",\"L\",\"M\",\"S\",\"V\"" and e15!=""):
            check[14]=e15.split(",")
        if(e16!="Enter as: #1,#2,ect..." and e16!=""):
            check[15]=e16.split(",")
#        print("E1=",e1)
#        print("E15=",e15)
#        case="???"
#        print(case)
#        print(check)
        self.setCases(check)
        
    def setCases(self, check):
        self.progress_str.set("Setting Case Definition")
        self.master.update_idletasks()
        self.case=["Case"]
        trues=0
        falses=0
#        print("Length of self.data:",len(self.data)-1)
        for i in range(1, len(self.data)):
            if(len(self.data[i])==19):
                row_case=True
                j=0
                while(row_case and j<len(check)):
                    if(check[j]!=""):
                        #### Check Dates
                        if(j==0):
                            if(len(check[0])==2):
                                start=datetime.datetime.strptime(check[0][0], '%m/%d/%Y')
                                end=datetime.datetime.strptime(check[0][1], '%m/%d/%Y')
                                try:
                                    date=datetime.datetime.strptime(self.data[i][1], '%m/%d/%Y')
                                    if(not start<=date<=end):
                                        row_case=False
                                except ValueError:
                                    row_case=False
                            else:
                                if(self.data[i][1]!=check[0]):
                                    row_case=False
                        ### Check Ages
                        if(j==1):
                            age=-1
                            try:
                                age=int(self.data[i][2])
                            except ValueError:
                                row_case=False
                            if(age>200):
                                age=int(int(age)%100/12)
                            if(len(check[1])==2):
                                start=int(check[1][0])
                                end=int(check[1][1])
                                if(age>=0):
                                    if(not start<=age<=end):
                                        row_case=False
                            else:
                                if(self.data[i][2]!=check[1]):
                                    row_case=False
                        ### Check Sex
                        if(j==2):
                            if(self.data[i][3]!=check[2]):
                                row_case=False
                        ### Check Race
                        if(j==3):
                            if(self.data[i][4] not in check[3] and self.data[i][5] not in check[3]):
                                row_case=False
                        ### Check Other Race
    #                    if(j==4):
    #                        if(data[i][5] not in check[4]):
    #                            row_case=False
                        ### Check Body Part
                        if(j==5):
                            if(self.data[i][6] not in check[5]):
                                row_case=False
                        ### Check Diagnosis
                        if(j==6):
                            if(self.data[i][7] not in check[6] and self.data[i][8] not in check[6]):
                                row_case=False
                        ### Check Other Diagnosis - Removed
    #                    if(j==7):
    #                        if(data[i][8] not in check[7]):
    #                            row_case=False
                        ### Check Disposition
                        if(j==8):
                            if(self.data[i][9] not in check[8]):
                                row_case=False
                        ### Check Location
                        if(j==9):
                            if(self.data[i][10] not in check[9]):
                                row_case=False
                        ### Check Fire Involvement
                        if(j==10):
                            if(self.data[i][11] not in check[10]):
                                row_case=False
                        ### Check Product#1
                        if(j==11):
                            if(self.data[i][12] not in check[11] and self.data[i][13] not in check[11]):
                                row_case=False
                        ### Check Product#2
    #                    if(j==12):
    #                        if(data[i][13] not in check[12]):
    #                            row_case=False
                        ### Check Narrative
                        if(j==13):
                            combined=str(self.data[i][14]+self.data[i][15])
                            found=False
                            spot=0
                            while(not found and spot<len(check[13])):
                                if(check[13][spot].upper() in combined.upper()):
                                    found=True
                                spot+=1
                            if(not found):
                                row_case=False
                        ### Check Stratum
                        if(j==14):
                            if(self.data[i][16] not in check[14]):
                                row_case=False
                        ### Check PSU
                        if(j==15):
                            if(self.data[i][17] not in check[15]):
                                row_case=False

                    ### Iterate up
                    j+=1
                if(row_case):
                    trues+=1
                else:
                    falses+=1
                self.case.append(row_case)
                if(i%10000==0):
                    self.updateProgress(i, len(self.data))
#                    self.updateProgress2(i, len(self.data))
        print("Cases=",trues,"Non-Cases=",falses)
        self.num_cases=trues
        self.num_n_cases=falses
        self.case_num.set("Number of Cases:"+str(self.num_cases)+" Number of Non-Cases:"+str(self.num_n_cases))
        self.master.update_idletasks()
                    
                
                
                
    def makeGUI(self):
        years=["1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006",
              "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015",
              "2016", "2017"]
#        self.var1=IntVar()

        Checkbutton(self.master, text=years[0], variable=self.var1).grid(row=1, sticky=W)
        Checkbutton(self.master, text=years[1], variable=self.var2).grid(row=2, sticky=W)
        Checkbutton(self.master, text=years[2], variable=self.var3).grid(row=3, sticky=W)
        Checkbutton(self.master, text=years[3], variable=self.var4).grid(row=4, sticky=W)
        Checkbutton(self.master, text=years[4], variable=self.var5).grid(row=5, sticky=W)
        Checkbutton(self.master, text=years[5], variable=self.var6).grid(row=6, sticky=W)
        Checkbutton(self.master, text=years[6], variable=self.var7).grid(row=7, sticky=W)
        Checkbutton(self.master, text=years[7], variable=self.var8).grid(row=8, sticky=W)
        Checkbutton(self.master, text=years[8], variable=self.var9).grid(row=9, sticky=W)
        Checkbutton(self.master, text=years[9], variable=self.var10).grid(row=10, sticky=W)
        Checkbutton(self.master, text=years[10], variable=self.var11).grid(row=11, sticky=W)
        Checkbutton(self.master, text=years[11], variable=self.var12).grid(row=12, sticky=W)
        Checkbutton(self.master, text=years[12], variable=self.var13).grid(row=13, sticky=W)
        Checkbutton(self.master, text=years[13], variable=self.var14).grid(row=14, sticky=W)
        Checkbutton(self.master, text=years[14], variable=self.var15).grid(row=15, sticky=W)
        Checkbutton(self.master, text=years[15], variable=self.var16).grid(row=16, sticky=W)
        Checkbutton(self.master, text=years[16], variable=self.var17).grid(row=17, sticky=W)
        Checkbutton(self.master, text=years[17], variable=self.var18).grid(row=18, sticky=W)
        Checkbutton(self.master, text=years[18], variable=self.var19).grid(row=19, sticky=W)
        Checkbutton(self.master, text=years[19], variable=self.var20).grid(row=20, sticky=W)
#        Label(self.master, textvariable=self.status_str).grid(column=1, sticky=S)
        Button(self.master, text="Load Selected Data", command=self.varStates).grid(column=4, row=1)
        Button(self.master, text="Download File", command=self.downloadFiles).grid(column=4, row=2)
        Button(self.master, text="Quit", command=self.master.destroy).grid(column=4, row=3)
        Label(self.master, textvariable=self.progress_str).grid(column=4, row=6)
        self.progress.grid(column=4, row=7)
        Label(self.master, textvariable=self.load_str).grid(column=4, row=17)
        Label(self.master, textvariable=self.dl_str).grid(column=4, row=18)
        Label(self.master, textvariable=self.data_years).grid(column=4, row=19)
        Label(self.master, textvariable=self.data_events).grid(column=4, row=20)
        Label(self.master, text="Date").grid(column=2, row=1)
        Label(self.master, text="Age").grid(column=2, row=2)
        Label(self.master, text="Sex").grid(column=2, row=3)
        Label(self.master, text="Race").grid(column=2, row=4)
#        Label(self.master, text="Other_Race").grid(column=4, row=5)
        Label(self.master, text="Body_Part").grid(column=2, row=5)
        Label(self.master, text="Diagnosis").grid(column=2, row=6)
#        Label(self.master, text="Other_Diagnosis").grid(column=4, row=8)
        Label(self.master, text="Disposition").grid(column=2, row=7)
        Label(self.master, text="Location").grid(column=2, row=8)
        Label(self.master, text="Fire_Involvement").grid(column=2, row=9)
        Label(self.master, text="Product#").grid(column=2, row=10)
#        Label(self.master, text="Product#2").grid(column=4, row=13)
        Label(self.master, text="Narrative Field").grid(column=2, row=11)
        Label(self.master, text="Stratum").grid(column=2, row=12)
        Label(self.master, text="PSU").grid(column=2, row=13)
        Entry(self.master, textvariable=self.entry1, width=34).grid(column=3, row=1)
        Entry(self.master, textvariable=self.entry2, width=34).grid(column=3, row=2)
        Entry(self.master, textvariable=self.entry3, width=34).grid(column=3, row=3)
        Entry(self.master, textvariable=self.entry4, width=34).grid(column=3, row=4)
#        Entry(self.master, textvariable=self.entry5, width=34).grid(column=5, row=5)
        Entry(self.master, textvariable=self.entry6, width=34).grid(column=3, row=5)
        Entry(self.master, textvariable=self.entry7, width=34).grid(column=3, row=6)
#        Entry(self.master, textvariable=self.entry8, width=34).grid(column=5, row=8)
        Entry(self.master, textvariable=self.entry9, width=34).grid(column=3, row=7)
        Entry(self.master, textvariable=self.entry10, width=34).grid(column=3, row=8)
        Entry(self.master, textvariable=self.entry11, width=34).grid(column=3, row=9)
        Entry(self.master, textvariable=self.entry12, width=34).grid(column=3, row=10)
#        Entry(self.master, textvariable=self.entry13, width=34).grid(column=5, row=13)
        Entry(self.master, textvariable=self.entry14, width=34).grid(column=3, row=11)
        Entry(self.master, textvariable=self.entry15, width=34).grid(column=3, row=12)
        Entry(self.master, textvariable=self.entry16, width=34).grid(column=3, row=13)
        Button(self.master, text="Count Cases", command=self.checkCase).grid(column=4, row=4)
#        self.progress2.grid(column=5, row=15)
        Label(self.master, textvariable=self.case_num).grid(column=3, row=20)
        Button(self.master, text="Clear Case", command=self.clearCase).grid(column=4, row=5)
        
        mainloop()
        
master=Tk()
neiss_GUI=NEISS_Data_Requester(master)
neiss_GUI.makeGUI()


