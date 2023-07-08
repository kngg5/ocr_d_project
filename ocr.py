import pandas as pd
from collections import Counter

import pyautogui
import numpy as nm
import pytesseract as pt
import cv2
from PIL import ImageGrab as ig
import re
import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
import string


def ocr_app():
    window = tk.Tk()
    window.title("OCR Program *** Main Window")
    window.geometry('300x300+300+200')
    window.resizable(0,0)
    label1 = Label(window, text='Check any text for offensive word', font=("Helvetica",13))
    label1.pack(ipadx=10, ipady=10)

#################################     screen scan        #####################################################               #########################################

    def findBadWords():
        # https://github.com/UB-Mannheim/tesseract/wiki
        result.withdraw()
        
        scan_buttn.config(state="disabled")
        """  pt.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        tesstr = ""
        cap = ig.grab(bbox = None)
        tesstr = pt.image_to_string(
                cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY), 
                lang ='eng') """
        pt.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        screenshot = pyautogui.screenshot()
        text = pt.image_to_string(screenshot, lang='eng',config='--psm 6')
        text = re.sub(r'[^\w\s]', '', text)
        read_dataset=pd.read_csv("bad-words.csv") 
        print(text)
       
        series=read_dataset.squeeze()
        global offensive_items
        offensive_items=list(series)
        s1 = text
        s1=s1.lower()

     
        store_list=[]
        for i in s1.split():
            if i in offensive_items:
                store_list.append(i)
        if len(store_list)>0:
            count = dict(Counter(store_list))
            val = 0
            print(store_list)
            for j in count.values():
                val += j
                d=0
            if(val >= 1 or val <= 3):
                d = 1
            elif(val > 3 or val <=6):
                d = 4
            else:
                d = 5
            result_info()
            label2 = Label(result_window, text='Danger level: '+str(d), font=("Helvetica",20))
            label2.pack(ipadx=20, ipady=20)

            global words
            words = Label(result_window, text='', font=("Helvetica",15))
            words.pack(ipadx=25, ipady=25)
            words['text'] = '\n'.join('{} {}'.format(k, d) for k, d in count.items())
        else:
            words['text'] = "sentence have no offensive words"
        
  
    
    def result_info():
            window.withdraw()
            global result_window
            result_window = tk.Tk()
            result_window.title("OCR Result of Scan")
            result_window.geometry('600x500+600+200')
            quit = Button(result_window,text="Quit",command=result_window.quit)
            quit.pack(ipadx=20,ipady=20)
            go_back = Button(result_window,text="Back to main window",command=scan_from_scrn)
            go_back.pack(ipadx=20,ipady=20)


    def scan_voice():
        global scan_speech
        scan_speech = tk.Tk()
        scan_speech.title("OCR Result of Scan")
        scan_speech.geometry('600x500+600+200')
        label2 = Label(scan_speech, text='Audio file: audio-test', font=("Helvetica",20))
        label2.pack(ipadx=20, ipady=20)
        quit = Button(scan_speech,text="Quit",command=scan_speech.quit)
        quit.pack(ipadx=20,ipady=20)
        go_back = Button(scan_speech,text="Back to main window",command=ocr_app)
        go_back.pack(ipadx=20,ipady=20)

    def scan_from_scrn():
        def repeat_scan():
            scan_buttn.config(state="normal")
        
        global result_info
        

        window.withdraw()
        global result
        result = tk.Tk()
        result.title("OCR Screen Scan")
        result.geometry('300x300+1100+300')
        result.resizable(0,0)
        label5 = Label(result, text='Check for offensive!', font=("Helvetica",15))
        label5.pack(ipadx=10, ipady=10)
        global scan_buttn
        scan_buttn = Button(result,text="Scan from screen",command=findBadWords)
        scan_buttn.pack(ipadx=20,ipady=20)
        
        go_back = Button(result,text="Back to main window",command=ocr_app)
        go_back.pack(ipadx=20,ipady=20)
        
        

#########################################   document  scan   ###########################################################################################   ##################
  
    """ 
    def display_offensive_words():
        display_words = tk.Tk()
        display_words.title("OCR Document Scan")
        display_words.geometry('500x500+300+200')
        label1 = Label(display_words, text='Check any text for offensive word', font=("Helvetica",15))
        label1.pack(ipadx=10, ipady=10)
 """
    def scan_from_docmnt():
        window.destroy()
        global doc_scan
        doc_scan = tk.Tk()
        doc_scan.title("OCR Document Scan")
        doc_scan.geometry('800x500+300+200')
      
        label1 = Label(doc_scan, text='Please choose file which should be scanned', font=("Helvetica",15))
        label1.pack(ipadx=10, ipady=10)
        global doc_scan_res
        doc_scan_res = Label(doc_scan, font=("Helvetica",15))
        doc_scan_res.pack(ipadx=10, ipady=10)
        
        
        def find_file():
            global filetypes
            filetypes = (
             ('text files', '*.txt'),
             ('All files', '*.*')
            )
            filename = filedialog.askopenfilename(title='Select file to scan',filetypes=filetypes)
            file_read = open(filename,'r')
            file_content = file_read.read().lower()
            file_content = file_content.split()
            new_content = str.maketrans('','', string.punctuation)
            remove_punctuation = [l.translate(new_content) for l in file_content]
           
            
           

            csv_file=pd.read_csv("bad-words.csv") 
            
            ser=csv_file.squeeze()
            
            offensive_items=list(ser)
            danger = 0
            other = 0
            offensive = 0
            other_needs = ["i","will","we","us","you","them","they","his","her","their","black","negr","islam"]

            for m in remove_punctuation:
                if(m in other_needs):
                    other+=1
                if(m in offensive_items):
                    offensive+=1

            if(offensive > 0):
                danger = 1
            
            if(other > 0 and other <= 3):
                danger = 3
            if(other > 3 and offensive > 0):
                danger = 4
            if(other > 6 and offensive > 0):
                danger = 5
            
            print(other)
            print(offensive)

            doc_scan_res['text'] = "Danger level: " + str(danger)
           
            file_read.close()

        open_file = Button(doc_scan,text="open file",command=find_file)
        open_file.pack(ipadx=15,ipady=15)

        back_to_main_window = Button(doc_scan,text="Back to main window",command=ocr_app)
        back_to_main_window.pack(ipadx=20,ipady=20)

        quit = Button(doc_scan,text="Quit",command=doc_scan.quit)
        quit.pack(ipadx=15,ipady=15)

###############################         ###########################################          ###################################################
    

        


##############################################           ########################## #################3    
    
    scan_from_screen = Button(window,text="Scan from screen",command=scan_from_scrn)
    scan_from_screen.pack(ipadx=20,ipady=20)

    scan_from_doc = Button(window,text="Scan from document",command=scan_from_docmnt)
    scan_from_doc.pack(ipadx=20,ipady=20)

    scan_from_voice = Button(window,text="Scan from voice",command=scan_voice)
    scan_from_voice.pack(ipadx=20,ipady=20)

    quit = Button(window,text="Quit",command=window.destroy)
    quit.pack(ipadx=15,ipady=15)
    window.mainloop()

ocr_app()

