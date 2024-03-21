import time
import sys
import ctypes
import wikipedia
from datetime import datetime
import threading
import json
import re
import json
import subprocess
from win10toast import ToastNotifier
import webbrowser
import numpy as np 
from PIL import Image 
import smtplib
import os
import requests
import urllib
import speech_recognition
import playsound
import urllib3 
import urllib.request as urllib2
from random import choice
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch
import cv2
import sqlite3
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning 
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) 
from youtubesearchpython import SearchVideos
from tkinter import Tk, RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style
from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox as mbox
wikipedia.set_lang('vi')
language = 'vi'

#---------------------------------------------------------------------------------------------------------------------------
def khaibaoytevalue():
    khaibao_f = get_text()
    if khaibao_f:
        khaibaoyte1(khaibao_f)
    elif "hủy" in khaibao_f:
        return 0



#---------------------------------------------------------------------------------------------------------------------------
def khaibaoyte(khaibao_f):
    def insertOrUpdate(Id,khaibao):
        conn=sqlite3.connect("data_cdc.db")
        cmd="SELECT * FROM nguoidung WHERE ID ="+str(Id)
        cursor=conn.execute(cmd)
        isRecordExist=0
        for row in cursor:
            isRecordExist=1
        if(isRecordExist==1):
            cmd="UPDATE nguoidung SET khaibao= "+str(khaibao)+" WHERE ID = "+str(Id)
        else:
            cmd="INSERT INTO NGUOIDUNG(ID,khaibao) Values("+str(Id)+","+str(khaibao)+")"
        conn.execute(cmd)  
        conn.commit()
        conn.close()
    id=1
    khaibao = '"'+khaibao_f+'"'
    insertOrUpdate(id, khaibao)

#-----------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------------
def facedetect():
    recognizer = cv2.face.LBPHFaceRecognizer_create(); #create a recognizer, LBPH is a face recognition algorithm.Local Binary Patterns Histograms 
    recognizer.read("recognizer\\trainingData.yml")
    faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
    path = 'dataSet'
    cam = cv2.VideoCapture(cv2.CAP_DSHOW);
    font = cv2.FONT_HERSHEY_SIMPLEX #5=font size
    fontscale = 1
    fontcolor = (255,255,255)
    stroke = 2
    profiles={}
    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5);
        for(x,y,w,h) in faces:
            id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            profile=getProfile(id)
            if(conf<60):
               if(conf<60):
                if(id==1):
                    print(profile[1])
                    return khamsuckhoe()
            else:   
                id=0
                profile=getProfile(id)
                speak("khuôn mặt của bạn không có trong cơ sở dữ liệu, vui lòng làm thủ tục trước khi khám bệnh")
                return thutuc()
            if(profile!=None):
                cv2.putText(frame,"Name:" +str(profile[1]), (x,y+h+30), font, fontscale, fontcolor, stroke)
                cv2.putText(frame,"merm:" +str(profile[2]), (x,y+h+60), font, fontscale, fontcolor, stroke)
        cv2.imshow("frame",frame);
        if cv2.waitKey(20) & 0xFF == ord('q'):
           break
    cam.release()
    cv2.destroyAllWindows()
#----------------------------------------------------------------------------------------------------------------------------------------
#Thủ tục 1
def thutuc():
    speak("tôi sẽ hướng dẫn bạn cách làm thủ tục")
    speak("đầu tiên hãy đọc họ và tên của bạn không kèm theo câu đệm")
    name_f = get_text()
    if name_f:
        choice_1 = ["liệu tên của bạn có phải là {}".format(name_f),
                     "hãy xác nhận tên của bạn có phải là {}".format(name_f), 
                      "vui lòng xác nhận bạn có phải là {}".format(name_f)]
        speak(choice(choice_1))
        text = get_text()
        if "không" in text:
            speak("bây giờ bạn sẽ làm lại thủ tục")
            return thutuc()
        if "đúng" or "có" or "phải" in text:
            speak("cảm ơn bạn đã xác minh.")
            speak("bây giờ là bước cuối cùng trong thủ tục. bạn hãy nhìn thẳng vào camera để quét khuôn mặt. thời gian thực hiện là 5 giây.")
            sqlitedata(name_f)
    root.update()

def sqlitedata(name_f):
    cam = cv2.VideoCapture(cv2.CAP_DSHOW)
    faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
    def insertOrUpdate(Id,Name):
        conn=sqlite3.connect("data_cdc.db")
        cmd="SELECT * FROM nguoidung WHERE ID ="+str(Id)
        cursor=conn.execute(cmd)
        isRecordExist=0
        for row in cursor:
            isRecordExist=1
        if(isRecordExist==1):
            cmd="UPDATE nguoidung SET Name= "+str(Name)+" WHERE ID = "+str(Id)
        else:
            cmd="INSERT INTO NGUOIDUNG(ID,Name) Values("+str(Id)+","+str(Name)+")"
        conn.execute(cmd)  
        conn.commit()
        conn.close()
    listid = list(range(1,22))
    pickid = random.choice(listid)
    id=pickid
    name = '"'+name_f+'"'
    insertOrUpdate(id, name)
    sampleNum=0
    timeout = 5
    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        ret, frame = cam.read();
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5);
        for (x,y,w,h) in faces:
            sampleNum=sampleNum+1;
            cv2.imwrite("dataSet/user."+str(id)+'.'+ str(sampleNum) +".jpg",frame[y:y+h,x:x+w])
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)    
            cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == 30:
            break
    facetrain() 
    facedetect3()
    cam.release()
    cv2.destroyAllWindows()
#------------------------------------------------------------------------------------------------------------

def sqlitedata2(name_f):
    cam = cv2.VideoCapture(cv2.CAP_DSHOW)
    faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
    def insertOrUpdate(Id,Name):
        conn=sqlite3.connect("data_cdc.db")
        cmd="SELECT * FROM nguoidung WHERE ID ="+str(Id)
        cursor=conn.execute(cmd)
        isRecordExist=0
        for row in cursor:
            isRecordExist=1
        if(isRecordExist==1):
            cmd="UPDATE nguoidung SET Name= "+str(Name)+" WHERE ID = "+str(Id)
        else:
            cmd="INSERT INTO NGUOIDUNG(ID,Name) Values("+str(Id)+","+str(Name)+")"
        conn.execute(cmd)  
        conn.commit()
        conn.close()
    listid = list(range(1,22))
    pickid = random.choice(listid)
    id=pickid
    name = '"'+name_f+'"'
    insertOrUpdate(id, name)
    sampleNum=0
    timeout = 5
    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        ret, frame = cam.read();
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5);
        for (x,y,w,h) in faces:
            sampleNum=sampleNum+1;
            cv2.imwrite("dataSet/user."+str(id)+'.'+ str(sampleNum) +".jpg",frame[y:y+h,x:x+w])
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)    
            cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == 30:
            break
    facetrain() 
    speak("bạn đã hoàn tất thủ tục, chúc mừng bạn")
    root.update()
    return ham_main()
    cam.release()
    cv2.destroyAllWindows()
#------------------------------------------------------------------------------------------------------------------------------------
#thủ tục 3
#---------------------------------------------------------------------------------------------------------------------------------------------
def facetrain():
    recognizer = cv2.face.LBPHFaceRecognizer_create(); 
    path='dataSet'  
    def getImagesWithID(path): 
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        faces=[] 
        IDs=[] 
        for imagePath in imagePaths: 
            faceImg=Image.open(imagePath).convert("L");
            faceNp=np.array(faceImg,'uint8') 
            ID=int(os.path.split(imagePath)[-1].split('.')[1]) 
            faces.append(faceNp)
            print(ID)
            IDs.append(ID)
            cv2.imshow("training",faceNp)
            cv2.waitKey(10)
        return np.array(IDs), faces 
    Ids, faces=getImagesWithID(path) 
    recognizer.train(faces,Ids) 
    recognizer.save('recognizer/trainingData.yml')
    cv2.destroyAllWindows()

#path=ChromeDriverManager().install()
root = Tk()
text_area = Text(root, height=26, width=45)
scroll = Scrollbar(root, command=text_area.yview)
#hệ thống thu âm và chuyển đổi ngôn ngữ sang văn bản
#----------------------------------------------------------------------------------------
def speak(text):
    print("[#1301-#0203] >>:  {}".format(text))
    text_area.insert(INSERT,"[#1301-#0203] >>: "+text+"\n")
    tts = gTTS(text=text, lang=language, slow=False)
    date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "filesound//voice"+date_string+".mp3"
    tts.save(filename)
    playsound.playsound(filename)

def get_audio():
    playsound.playsound("Ping.mp3", False)
    time.sleep(1)
    print("\n[#1301-#0203] >>:  Đang nghe ...")
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("USER >>: ")
        audio = r.listen(source, phrase_time_limit=6)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text.lower()
        except:
            print("\n")
            return ""

def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 3:
            nghe_khong_ro = ["Tôi không nghe rõ. bạn có thể nói lại được không!",
                             "Xin lỗi bạn, tôi nghe không rõ",
                             "xin lỗi bạn, liệu bạn có thể nói lại được chứ"]
            speak(choice(nghe_khong_ro))
            time.sleep(4)
    time.sleep(3)
    return 0


def kbspeak(kbtext):
    print("[#1301-#0203] >>:  {}".format(kbtext))
    text_area.insert(INSERT,"[#1301-#0203] >>: "+kbtext+"\n")
    tts = gTTS(kbtext=kbtext, lang=language, slow=False)
    date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "filesound//voice"+date_string+".mp3"
    tts.save(filename)
    playsound.playsound(filename)

def kbget_audio():
    playsound.playsound("Ping.mp3", False)
    time.sleep(1)
    print("\n[#1301-#0203] >>:  Đang nghe ...")
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("USER >>: ")
        audio = r.listen(source, phrase_time_limit=25)
        try:
            kbtext = r.recognize_google(audio, language="vi-VN")
            print(kbtext)
            return kbtext.lower()
        except:
            print("\n")
            return ""
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def queryall(tc):
    con = sqlite3.connect('data_cdc.db')
    cur = con.cursor()
    querrycmd = "SELECT * FROM benhli where "
    for i in tc:
        querrycmd += "trieuchung like '%" + i + "%' And "
    cur = cur.execute(querrycmd[:-4])
    row = cur.fetchone()
    speak("bạn có thể đã bị bệnh "+row[1])
    speak("tôi khuyên bạn nên "+row[4])
    root.update()
    saveinfo()

def khambenhprogram():
    mang = ["tai", "mắt", "mũi", "miệng", "da", "thịt", "răng", "lợi" , "mồm", "mi", "thị", "giác", "ngoài", "ống", "trong", "âm" , "dương", "trán", "đầu", "đau", "bụng", "cổ", "lưng", "chân", "tay", "bướm", "vật", "hậu", "môn", "lỗ", "nhị", "trắng", "đỏ", "cam", "nước", "tiêu" , "chảy", "ỉa", "đi", "ngoài", "chất", "lỏng", "thần", "kinh", "dây", "thính", "viễn", "dái", "dài", "ngắn", "rộng", "ù", "dữ", "dội", "kém", "tốt", "nhanh", "bầm", "thâm"]
    mang_new = []
    text = kbget_audio()
    for word in mang:
        if word in text:
            mang_new.append(word)
    queryall(mang_new)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def saveinfo():
    speak("vui lòng nhìn vào camera để lưu lại thông tin bệnh án vào hồ sơ của bạn")
    root.update()
    facedetect2()


def dangnhap():
    os.system("loginform.exe")


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent) 
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        self.parent.title("TRÍ TUỆ NHÂN TẠO KHÁM BỆNH HỌC ĐƯỜNG")
        self.style = Style()
        self.style.theme_use("default")
        
        scroll.pack(side=RIGHT, fill=Y)
        text_area.configure(yscrollcommand=scroll.set)
        text_area.pack(side=RIGHT)

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)


        closeButton = Button(self, text="COVID-19",width=10,command= covid19, fg="white", bg="#009999",bd=3)
        closeButton.pack(side=RIGHT, padx=11, pady=10)
        okButton = Button(self, text="BẮT ĐẦU",command = ham_main,width=10,fg="white", bg="#009999",bd=3)
        okButton.pack(side=RIGHT, padx=11, pady=10)
        doimau = Button(self,text="ĐĂNG NHẬP",width=10,command = dangnhap, fg="white", bg="#009999",bd=3)
        doimau.pack(side=RIGHT,padx=11, pady=10)
        doimau = Button(self,text="BÁO CÁO",width=10,command = baocao,fg="white", bg="#009999",bd=3)
        doimau.pack(side=RIGHT,padx=11, pady=10)
        thongtin = Button(self,text="THỦ TỤC",width=10,command = thutuc2, fg="white", bg="#009999",bd=3)
        thongtin.pack(side=RIGHT,padx=11, pady=10)
        donhiptim = Button(self,text="ĐO NHỊP TIM",command = heartbeat,width=10,fg="white", bg="#009999",bd=3)
        donhiptim.pack(side=RIGHT,padx=11, pady=10)
        khambenh = Button(self,text="KHÁM BỆNH",command = khambenh_v,width=10,fg="white", bg="#009999",bd=3)
        khambenh.pack(side=RIGHT,padx=11, pady=10)
        infomation = Button(self,text="THÔNG TIN",command = infomation_v,width=10,fg="white", bg="#009999",bd=3)
        infomation.pack(side=RIGHT,padx=11, pady=10)
        csdl= Button(self,text="CƠ SỞ DỮ LIỆU",command = sqlite,width=10,fg="white", bg="#009999",bd=3)
        csdl.pack(side=RIGHT,padx=11, pady=10)
    
        image_1 = ImageTk.PhotoImage(Image.open("image\\trolyao.png"))    
        label1 = Label(self, image=image_1)
        label1.image = image_1
        label1.place(x=7, y=43)

        l = Label(root, text='[+CUỘC HỘI THOẠI+]', fg='yellow', bg='blue')
        l.place(x = 750, y = 10, width=120, height=25)
        l1 = Label(root, text='BÁC SĨ AVA', fg='yellow', bg='blue')
        l1.place(x = 45, y = 11, width=120, height=25)

root.geometry("1600x510+250+500")
root.iconbitmap('logo.ico')
root.resizable(True, True)
app = Example(root)
root.mainloop()

