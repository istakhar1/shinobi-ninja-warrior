import urllib
import cv2
import pyttsx3
import speech_recognition as sr
import numpy as np
import sys
import smtplib as s
import datetime
from datetime import date

if sys.version_info[0] == 3:#this if else is for use ip cam streming video
    from urllib.request import urlopen
else:
    from urllib import urlopen
#video_file = "video_1.mp4"


#now AI speech recognition start
engine = pyttsx3.init('sapi5')
voices =engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice',voices[0].id)

def speak(audio):
    """
it say what i pass
"""
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    #it take microphone input  from user and return string output
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query =r.recognize_google(audio,language='en-in')
        #print(f"user said:{query}\n")

    except Exception as e:
        #print(e)
       # print("say that again plese...")
        return "None"
    return query


#for mail sending
def sendEmail():
    ob = s.SMTP("smtp.gmail.com",587)
    ob.starttls()
    ob.login("abc73301@gmail.com","@Istakhar054")
    sub="Fire warning"
    body="fire found at Dumka jharkhand (814101)"
    today = date.today()
    hour = int(datetime.datetime.now().hour) 
    message="Subject:{}\n\n{}\n\nDate:- {}\n\nTime:- {}".format(sub,body,today,hour)
    listofadd=["istakhar054@gmail.com","smriti.sharma@aot.edu.in","ishanksubudhi49@gmail.com"]
    ob.sendmail("abc73301@gmail.com",listofadd,message)
    print("send mail")
    ob.quit()

#this is deep learning model
while True:
    imgResp=urlopen("http://10.85.224.85:8080/shot.jpg")#this will be change day by day its depends on our curernt ip wecam address
    imgnp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    video=cv2.imdecode(imgnp,-1)
    grabbed=video
    frame=video
    #cv2.imshow('test',grabbed)
    #cv2.waitKey(10)
    if not grabbed.any():
        break
 
    blur = cv2.GaussianBlur(frame, (25, 25), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
 
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
    
 
 
    output = cv2.bitwise_and(frame, hsv, mask=mask)
    no_red = cv2.countNonZero(mask)
    cv2.imshow("output", output)
    #print("output:", frame)
    if int(no_red) > 100000:
        print ('Fire detected')
        speak("Hello sir I m shinobi made by ninza warrior i got a fire plese verified to send neares fire control room")
        
        while True:        
            query = takeCommand().lower()
            if 'verified' in query:
                speak("ok thank you mail send")
                sendEmail()
                break
            elif 'ok' in query:
                speak("ok thank you mail send")
                sendEmail()
                break
            elif 'yes' in query:
                speak("ok thank you mail send")
                sendEmail()
                break
            elif 'no' in query:
                speak("ok thank you i i will not send mail")
                break
            else:
                speak("hello sir plese response")




        #sendEmail()
        #break
        
    #print(int(no_red))
   #print("output:".format(mask))
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
 
cv2.destroyAllWindows()
#video.release()
