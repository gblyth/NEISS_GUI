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
        self.progress=ttk.Progressbar(self.master, orient=HORIZONTAL, length=100, mode='determinate')
#        self.progress2=ttk.Progressbar(self.master, orient=HORIZONTAL, length=100, mode='determinate')
        self.data_years=StringVar()
        self.data_years.set("Years of Data Loaded=\nNone")
        self.data_events=StringVar()
        self.data_events.set("Number of Injury Events Loaded=\nNone")
        self.data_loaded=False
        self.file_to_dl=False
        ### Data loaded string
        self.load_str=StringVar()
        self.load_str.set("Datasets Loaded=\n"+str(self.data_loaded))
        ### Download availablity string
        self.dl_str=StringVar()
        self.dl_str.set("File Ready To Download=\n"+str(self.file_to_dl))
        ### Progress Bar String
        self.progress_str=StringVar()
        self.progress_str.set("Ready")
        ### Dates
        self.entry1=StringVar()
        self.entry1.set("(MM/DD/YYYY)or(MM/DD/YYYY-MM/DD/YYYY)")
        ### Age
        self.entry2=StringVar()
        self.entry2.set("singlular(#) or range(#-#)")
        ### Narrative
        self.entry14=StringVar()
        self.entry14.set("Enter as: Word1,Word2,ect...")
        ### PSU
        self.entry16=StringVar()
        self.entry16.set("Enter as: 1,2,3,...,100")
        ### Count Cases vs Non-Cases
        self.case_num=StringVar()
        self.case_num.set("Number of Cases:"+str(self.num_cases)+" Number of Non-Cases:"+str(self.num_n_cases))
        

        ### Sex
        self.m1i1=IntVar()
        self.m1i2=IntVar()
        self.m1i3=IntVar()
        
        ### Race
        self.m2i1=IntVar()
        self.m2i2=IntVar()
        self.m2i3=IntVar()
        self.m2i4=IntVar()
        self.m2i5=IntVar()
        self.m2i6=IntVar()
        self.m2i7=IntVar()
        
        ### Location
        self.m3i1=IntVar()
        self.m3i2=IntVar()
        self.m3i3=IntVar()
        self.m3i4=IntVar()
        self.m3i5=IntVar()
        self.m3i6=IntVar()
        self.m3i7=IntVar()
        self.m3i8=IntVar()
        self.m3i9=IntVar()
        
        ### Fire Involvement
        self.m4i1=IntVar()
        self.m4i2=IntVar()
        self.m4i3=IntVar()
        self.m4i4=IntVar()
        
        #Hospital Stratum
        self.m5i1=IntVar()
        self.m5i2=IntVar()
        self.m5i3=IntVar()
        self.m5i4=IntVar()
        self.m5i5=IntVar()
        
        ### Disposition
        self.m6i1=IntVar()
        self.m6i2=IntVar()
        self.m6i3=IntVar()
        self.m6i4=IntVar()
        self.m6i5=IntVar()
        self.m6i6=IntVar()
        self.m6i7=IntVar()

        path="/Users/Gavin/Desktop/U of C/MScBMI 33100/Final/NEISS/diagnosis.tsv"
        f=open(path)
        self.diag=[]
        self.diag_nums=[]
        for row in f:
            temp=row.split("\t")
            self.diag.append("=".join(temp))
            self.diag_nums.append(str(int(temp[0])))
        self.diag_data={}
        f.close()

        path="/Users/Gavin/Desktop/U of C/MScBMI 33100/Final/NEISS/body_parts.tsv"
        f=open(path)
        self.body=[]
        self.body_nums=[]
        for row in f:
            temp=row.split("\t")
            self.body.append("=".join(temp))
            self.body_nums.append(str(int(temp[0])))
        self.body_data={}
        f.close()

        path="/Users/Gavin/Desktop/U of C/MScBMI 33100/Final/NEISS/product_codes.tsv"
        f=open(path)
        self.prdcts=[]
        self.prdct_nums=[]
        for row in f:
            temp=row.split("\t")
            self.prdcts.append("=".join(temp))
            self.prdct_nums.append(str(int(temp[0])))
        self.prd_data={}
        f.close()    
        
        self.nyears=[str(year) for year in range(1997,2018)]
        self.nyears_data={}
        
        
    def updateProgress(self, number, total):
        if(total==0):
            number=0
            total=1
        value=int((number/total)*100)
        self.progress['value']=value
        self.master.update()

#    Needed to remove this method because it take way too long... maybe multithread it?
    def updateProgress2(self, number, total):
        value=int((number/total)*100)
        self.progress2['value']=value
        self.master.update_idletasks()

    # Get a file based on a URL and cache it locally
    # if already exists, we don't have to go to the web for it
    def getFile(self,url):
        filesize_r = requests.head(url)
        size_b = int(filesize_r.headers['content-length'])
        chunks = int(size_b / 1024)
        local_filename = ".cache/"+url.split('/')[-1]
        # Should check filesize here as well
        if (    not os.path.isfile(local_filename)
                or os.path.getsize(local_filename) != size_b
            ):
            self.progress_str.set("Downloading {0}".format(url.split('/')[-1]))
            r = requests.get(url, stream=True)
            if not os.path.exists(os.path.dirname(local_filename)):
                os.makedirs(os.path.dirname(local_filename))
            with open(local_filename,'wb') as f:
                chunk_count = 0
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        chunk_count += 1
                    if chunk_count % 1000 == 0:
                        self.updateProgress(chunk_count,chunks)
        return local_filename

    def loadFiles(self):
        self.master.update_idletasks()
        self.data=[]
        years_down=[]

        # Dictionary comprehension that reduces years to only the ones checked
        years = {key:value for (key,value) in self.nyears_data.items() if value.get() == 1}
        for year in years.keys():
            self.progress_str.set("Loading {0}".format(year))
            if self.yearchecks[year].get() == 1:
                url = 'https://www.cpsc.gov/cgibin/NEISSQuery/Data/Archived%20Data/{0}/neiss{0}.tsv'.format(year)
                filename = self.getFile(url)
                r_data=open(filename,'r',encoding="ISO-8859-1").readlines()
                if(len(self.data)==0):
                    for row in r_data:
                        self.data.append(row.split("\t"))
                else:
                    for row in range(1,len(r_data)):
                        self.data.append(r_data[row].split("\t"))
                years_down.append(year)
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
        self.entry14.set("Enter as: Word1,Word2,ect...")
        self.entry16.set("Enter as: 1,2,3,...,100")
        
                ### Sex
        self.m1i1.set(0)
        self.m1i2.set(0)
        self.m1i3.set(0)
        
        ### Race
        self.m2i1.set(0)
        self.m2i2.set(0)
        self.m2i3.set(0)
        self.m2i4.set(0)
        self.m2i5.set(0)
        self.m2i6.set(0)
        self.m2i7.set(0)
        
        ### Location
        self.m3i1.set(0)
        self.m3i2.set(0)
        self.m3i3.set(0)
        self.m3i4.set(0)
        self.m3i5.set(0)
        self.m3i6.set(0)
        self.m3i7.set(0)
        self.m3i8.set(0)
        self.m3i9.set(0)
        
        ### Fire Involvement
        self.m4i1.set(0)
        self.m4i2.set(0)
        self.m4i3.set(0)
        self.m4i4.set(0)
        
        #Hospital Stratum
        self.m5i1.set(0)
        self.m5i2.set(0)
        self.m5i3.set(0)
        self.m5i4.set(0)
        self.m5i5.set(0)
        
        ### Disposition
        self.m6i1.set(0)
        self.m6i2.set(0)
        self.m6i3.set(0)
        self.m6i4.set(0)
        self.m6i5.set(0)
        self.m6i6.set(0)
        self.m6i7.set(0)
        
        # Clear diagnosis data
        temp=self.diag_data.keys()
        for spot in temp:
            self.diag_data[spot].set(0)
        # Clear body part data
        temp=self.body_data.keys()
        for spot in temp:
            self.body_data[spot].set(0)
        # Clear diagnosis data
        temp=self.prd_data.keys()
        for spot in temp:
            self.prd_data[spot].set(0)
        self.case_num.set("Number of Cases:"+str(self.num_cases)+" Number of Non-Cases:"+str(self.num_n_cases))
        self.updateProgress(0,len(self.data))
        self.master.update_idletasks()
        
        
    def checkCase(self):
        check=[]
        for i in range(16):
            check.append([])
        e1=str(self.entry1.get())
        e2=str(self.entry2.get())
        e14=str(self.entry14.get())
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
            
        ### Sex
        if(self.m1i1.get()==True):
            check[2].append('1')
        if(self.m1i2.get()==True):
            check[2].append('2')
        if(self.m1i3.get()==True):
            check[2].append('0')
            
        ### Race
        if(self.m2i1.get()==True):
            check[3].append('1')
        if(self.m2i2.get()==True):
            check[3].append('2')
        if(self.m2i3.get()==True):
            check[3].append('3')
        if(self.m2i4.get()==True):
            check[3].append('4')
        if(self.m2i5.get()==True):
            check[3].append('5')
        if(self.m2i6.get()==True):
            check[3].append('6')
        if(self.m2i7.get()==True):
            check[3].append('0')
            
        ### Body Part
        values = [(code, var.get()) for code, var in self.body_data.items()]
        for i in range(len(self.body_nums)):
            if(values[i][1]==True):
                check[5].append(self.body_nums[i])
            
        ### Diagnosis
        values = [(code, var.get()) for code, var in self.diag_data.items()]
        for i in range(len(self.diag_nums)):
            if(values[i][1]==True):
                check[6].append(self.diag_nums[i])
                
        ### Disposition
        if(self.m6i1.get()==True):
            check[8].append('1')
        if(self.m6i2.get()==True):
            check[8].append('2')
        if(self.m6i3.get()==True):
            check[8].append('4')
        if(self.m6i4.get()==True):
            check[8].append('5')
        if(self.m6i5.get()==True):
            check[8].append('6')
        if(self.m6i6.get()==True):
            check[8].append('8')
        if(self.m6i7.get()==True):
            check[8].append('9')
                
        ### Location
        if(self.m3i1.get()==True):
            check[9].append('1')
        if(self.m3i2.get()==True):
            check[9].append('2')
        if(self.m3i3.get()==True):
            check[9].append('4')
        if(self.m3i4.get()==True):
            check[9].append('5')
        if(self.m3i5.get()==True):
            check[9].append('6')
        if(self.m3i6.get()==True):
            check[9].append('7')
        if(self.m3i7.get()==True):
            check[9].append('8')
        if(self.m3i8.get()==True):
            check[9].append('9')
        if(self.m3i9.get()==True):
            check[9].append('0')
            
        ### Fire Involvement
        if(self.m4i1.get()==True):
            check[9].append('1')
        if(self.m4i2.get()==True):
            check[9].append('2')
        if(self.m4i3.get()==True):
            check[9].append('3')
        if(self.m4i4.get()==True):
            check[9].append('0')
            
        ### Product Number
        values = [(code, var.get()) for code, var in self.prd_data.items()]
        for i in range(len(self.prdct_nums)):
            if(values[i][1]==True):
                check[11].append(self.prdct_nums[i])
            
        ### Narrative
        if(e14!="Enter as: Word1,Word2,ect..." and e14!=""):
            check[13]=e14.split(",")
            
        ### Stratum
        if(self.m5i1.get()==True):
            check[15].append('C')
        if(self.m5i2.get()==True):
            check[15].append('V')
        if(self.m5i3.get()==True):
            check[15].append('L')
        if(self.m5i4.get()==True):
            check[15].append('M')
        if(self.m5i5.get()==True):
            check[15].append('S')
            
        ### PSU
        if(e16!="Enter as: 1,2,3,...,100" and e16!=""):
            check[15]=e16.split(",")
            
        print(check)
        self.setCases(check)
        
    def setCases(self, check):
        self.progress_str.set("Setting Case Definition")
        self.master.update_idletasks()
        self.case=["Case"]
        trues=0
        falses=0
        print("Length of self.data:",len(self.data)-1)
        for i in range(1, len(self.data)):
            if(len(self.data[i])==19):
                row_case=True
                j=0
                while(row_case and j<len(check)):
                    if(len(check[j])!=0):
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
                            if(self.data[i][3]  not in check[2]):
                                row_case=False
                                
                        ### Check Race
                        if(j==3):
                            if(self.data[i][4] not in check[3] and self.data[i][5] not in check[3]):
                                row_case=False
                                
                        ### Check Body Part
                        if(j==5):
                            if(self.data[i][6] not in check[5]):
                                row_case=False
                                
                        ### Check Diagnosis
                        if(j==6):
                            if(self.data[i][7] not in check[6] and self.data[i][8] not in check[6]):
                                row_case=False
                                
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
                                
                        ### Check Product#
                        if(j==11):
                            if(self.data[i][12] not in check[11] and self.data[i][13] not in check[11]):
                                row_case=False
                                
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

        Button(self.master, text="Load Selected Data", command=self.loadFiles).grid(column=4, row=1)
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
        Label(self.master, text="Body_Part").grid(column=2, row=5)
        Label(self.master, text="Diagnosis").grid(column=2, row=6)
        Label(self.master, text="Disposition").grid(column=2, row=7)
        Label(self.master, text="Location").grid(column=2, row=8)
        Label(self.master, text="Fire_Involvement").grid(column=2, row=9)
        Label(self.master, text="Product#").grid(column=2, row=10)
        Label(self.master, text="Narrative Field").grid(column=2, row=11)
        Label(self.master, text="Stratum").grid(column=2, row=12)
        Label(self.master, text="PSU").grid(column=2, row=13)
        Entry(self.master, textvariable=self.entry1, width=34).grid(column=3, row=1)
        Entry(self.master, textvariable=self.entry2, width=34).grid(column=3, row=2)
        Entry(self.master, textvariable=self.entry14, width=34).grid(column=3, row=11)
        Entry(self.master, textvariable=self.entry16, width=34).grid(column=3, row=13)
        Button(self.master, text="Count Cases", command=self.checkCase).grid(column=4, row=4)
#        self.progress2.grid(column=5, row=15)
        Label(self.master, textvariable=self.case_num).grid(column=3, row=20)
        Button(self.master, text="Clear Case", command=self.clearCase).grid(column=4, row=5)
        
        ### Checkbox Menu #1 - Sex
        m1= Menubutton(self.master, text="Sex", relief=RAISED)
        m1.menu=Menu(m1, tearoff=0)
        m1["menu"]=m1.menu
        m1.menu.add_checkbutton(label="1=Male", variable=self.m1i1)
        m1.menu.add_checkbutton(label="2=Female", variable=self.m1i2)
        m1.menu.add_checkbutton(label="0=Not recorded", variable=self.m1i3)
        
        m2=Menubutton(self.master, text="Race", relief=RAISED)
        m2.menu=Menu(m2, tearoff=0)
        m2["menu"]=m2.menu
        m2.menu.add_checkbutton(label="1=White", variable=self.m2i1)
        m2.menu.add_checkbutton(label="2=Black/African American", variable=self.m2i2)
        m2.menu.add_checkbutton(label="3=Asian", variable=self.m2i3)
        m2.menu.add_checkbutton(label="4=American Indian/Alaska Native", variable=self.m2i4)
        m2.menu.add_checkbutton(label="5=Native Hawaiian/Pacific Islander", variable=self.m2i5)
        m2.menu.add_checkbutton(label="6=Other", variable=self.m2i6)
        m2.menu.add_checkbutton(label="0=Not Stated in ED record", variable=self.m2i7)
        
        m3=Menubutton(self.master, text="Location", relief=RAISED)
        m3.menu=Menu(m3, tearoff=0)
        m3["menu"]=m3.menu
        m3.menu.add_checkbutton(label="1=Home", variable=self.m3i1)
        m3.menu.add_checkbutton(label="2=Farm/ranch", variable=self.m3i2)
        m3.menu.add_checkbutton(label="4=Street or highway", variable=self.m3i3)
        m3.menu.add_checkbutton(label="5=Other public property", variable=self.m3i4)
        m3.menu.add_checkbutton(label="6=Mobile/Manufactured home", variable=self.m3i5)
        m3.menu.add_checkbutton(label="7=Industrial", variable=self.m3i6)
        m3.menu.add_checkbutton(label="8=School/Daycare", variable=self.m3i7)
        m3.menu.add_checkbutton(label="9=Place of recreation or sports", variable=self.m3i8)
        m3.menu.add_checkbutton(label="0=Not recorded", variable=self.m3i9)
        
        m4=Menubutton(self.master, text="Fire Involvement", relief=RAISED)
        m4.menu=Menu(m4, tearoff=0)
        m4["menu"]=m4.menu
        m4.menu.add_checkbutton(label="1=Fire involvement and/or smoke inhalation\n - Fire Dept. attended", variable=self.m4i1)
        m4.menu.add_checkbutton(label="2=Fire involvement and/or smoke inhalation\n - Fire Dept. did not attend", variable=self.m4i2)
        m4.menu.add_checkbutton(label="3=Fire involvement and/or smoke inhalation\n - Fire Dept. attendance is not recorded", variable=self.m4i3)
        m4.menu.add_checkbutton(label="0=No fire involvement or fire involvement not recorded", variable=self.m4i4)
        
        m5=Menubutton(self.master, text="Hospital Stratum", relief=RAISED)
        m5.menu=Menu(m5, tearoff=0)
        m5["menu"]=m5.menu
        m5.menu.add_checkbutton(label="C=Children\'s Hospitals", variable=self.m5i1)
        m5.menu.add_checkbutton(label="V=Very Large Hospitals", variable=self.m5i2)
        m5.menu.add_checkbutton(label="L=Large Hospitals", variable=self.m5i3)
        m5.menu.add_checkbutton(label="M=Medium Hospitals", variable=self.m5i4)
        m5.menu.add_checkbutton(label="S=Small Hospitals", variable=self.m5i5)
        
        m6=Menubutton(self.master, text="Disposition", relief=RAISED)
        m6.menu=Menu(m6, tearoff=0)
        m6["menu"]=m6.menu
        m6.menu.add_checkbutton(label="1=Treated and released or examined and released without treatment", variable=self.m6i1)
        m6.menu.add_checkbutton(label="2=Treated and transferred to another hospital", variable=self.m6i2)
        m6.menu.add_checkbutton(label="4=Treated and admitted for hospitalization (within same facility)", variable=self.m6i3)
        m6.menu.add_checkbutton(label="5=Held for observation", variable=self.m6i4)
        m6.menu.add_checkbutton(label="6=Left without being seen/Left against medical advice (AMA)", variable=self.m6i5)
        m6.menu.add_checkbutton(label="8=Fatality, including DOA, died in the ED, brain dead", variable=self.m6i6)
        m6.menu.add_checkbutton(label="9=Not recorded", variable=self.m6i7)
                    
        m7=Menubutton(self.master, text="Diagnosis", relief=RAISED)
        m7.menu=Menu(m7, tearoff=0)
        m7["menu"]=m7.menu
        for part in self.diag:
            var=IntVar()
            m7.menu.add_checkbutton(label=part, variable=var)
            self.diag_data[part]=var
                    
        m9=Menubutton(self.master, text="Body Parts", relief=RAISED)
        m9.menu=Menu(m9, tearoff=0)
        m9["menu"]=m9.menu
        for part in self.body:
            var=IntVar()
            m9.menu.add_checkbutton(label=part, variable=var)
            self.body_data[part]=var
                    
        m10=Menubutton(self.master, text="Products", relief=RAISED)
        m10.menu=Menu(m10, tearoff=0)
        m10["menu"]=m10.menu
        for code in self.prdcts:
            var=IntVar()
            m10.menu.add_checkbutton(label=code, variable=var)
            self.prd_data[code]=var
                    
        myear=Menubutton(self.master, text="Years of NEISS Data", relief=RAISED)
        myear.menu=Menu(myear, tearoff=0)
        myear["menu"]=myear.menu
        for code in self.nyears:
            var=IntVar()
            myear.menu.add_checkbutton(label=code, variable=var)
            self.nyears_data[code]=var
        
        m1.grid(column=3, row=3)
        m2.grid(column=3, row=4)
        m3.grid(column=3, row=8)
        m4.grid(column=3, row=9)
        m5.grid(column=3, row=12)
        m6.grid(column=3, row=7)
        m7.grid(column=3, row=6)
#        m8.grid(column=5, row=)
        m9.grid(column=3, row=5)
        m10.grid(column=3, row=10)
        myear.grid(column=1, row=1)
        
        mainloop()

if __name__ == "__main__":
    master=Tk()
    neiss_GUI=NEISS_Data_Requester(master)
    neiss_GUI.makeGUI()


