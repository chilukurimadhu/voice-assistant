#pip install speech_recognition
#pip install wikipedia
#pip install pyaudio
#pip install webbrowser 
#pip install gtts
#pip install googlemaps==1.0.2
#pip install google-search
import time,sys
import speech_recognition as sr
import webbrowser as wb
from gtts import gTTS
import playsound as ps
from datetime import datetime 
import wikipedia
import os
import random
from googlesearch import search
import subprocess  # #for system lock related
import ctypes,time,keyboard  #for system lock related
from googlesearch import search
import client1

r1=sr.Recognizer()
r2=sr.Recognizer()
r3=sr.Recognizer()

def Wikipedia(input_data):
    page_object = wikipedia.page(input_data)
    print(page_object.html)
    print(page_object.links[0:10])
        
    result = wikipedia.summary(input_data, sentences = 20)
    print(result)
def Google(input_data):
    
    num1 = random.randint(1, 20)
    for i in range(1,10):
        print(search(input_data)[i])
    res=search(input_data,num_results=20,lang="en")[num1-1]
    print("opening ",res)
    wb.get().open_new(res)

def Youtube(input_data):
            from youtubesearchpython import SearchVideos
            try:
                res_count=10
                search = SearchVideos(input_data, offset = 1, mode = "dict", max_results = res_count)
                print("you can manually select the url from here ")
                for i in range(res_count):
                      print(search.result()["search_result"][i-1]["link"])
                num1 = random.randint(1, res_count)
                print("searching ",num1,"video")
                wb.get().open_new(search.result()["search_result"][num1-2]["link"])
            except sr.UnknownValueError as e:
                print(e)
            except sr.RequestError as e:
                print(e)

def input_audio():
    with sr.Microphone() as source:
        audio=r3.listen(source)
        text=(r3.recognize_google(audio)).lower()
        speak_assistant(text)
        return text

def speak_assistant(mytext):
    print(mytext)
    """toSpeak = gTTS(text = mytext, lang ='en', slow = False) 
    #toSpeak.save("audio4.mp3")
    toSpeak.save("audio4.mp3") 
    # Playing the converted file 
    #os.system("audio4.mp3") 
    ps.playsound("audio4.mp3",True)
    os.remove("audio4.mp3")"""
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id) #changed voice to female
    ####SLOW DOWN VOICE RATE####
    rate = engine.getProperty('rate')
    engine.setProperty('rate',140)
    ########################
    engine.say(mytext) #speak here
    engine.runAndWait()
    

    
def web_search(input_data):
    
    if "youtube" in input_data:
        url="https://www.youtube.com/results?search_query="
        input_data=input_data.replace("youtube","")
        try:
            wb.get().open(url+input_data)
        except sr.UnknownValueError as e:
            print(e)
        except sr.RequestError as e:
            print(e)
    elif "google" in input_data:
        url="https://www.google.com/search?q ="
        input_data=input_data.replace("google","")
        try:
            wb.get().open(url+input_data)
        except sr.UnknownValueError as e:
            print(e)
        except sr.RequestError as e:
            print(e)
    elif "wikipedia" in input_data:
        
        url="https://en.wikipedia.org/wiki/Special:Search?search="
        input_data=input_data.replace("wikipedia","")
        page_object = wikipedia.page("india") 
        #print("page_object.html")
        print(page_object.links[0:10])
        
        result = wikipedia.summary(input_data, sentences = 4)
        print(result)
        try:
            wb.get().open(url+input_data)
        except sr.UnknownValueError as e:
            print("no input found")
        except sr.RequestError as e:
            print(e)
    elif "exit" in op or "abort" in op or "sleep" in op: 
        speak_assistant("Good Bye "+name_text+" Have a Nice Day")

    

    else:
        speak_assistant("please mention me where you want me to search youtube or google or wikipedia")
        output=input_audio()
        if "youtube" in output:
            Youtube(input_data)
        elif "wikipedia" in output:
            Wikipedia(input_data)
        elif "google" in output:
            Google(input_data)
        
        else:
            speak_assistant("given wrong input")

            
####where program starts here############

keywords=["youtube","google","wikipedia"]

if __name__=="__main__":
    count=0
    dt=datetime.now()
    hrs=int(dt.strftime("%H"))
    if hrs>=6 and hrs<12:
        msg="good Morning"
    elif hrs>=12 and hrs<=18:
        msg="good afternoon"
    else:
        msg="good evening"
    speak_assistant("hey "+msg+". This is madhu voice assistant..\n how may i help you ")
    speak_assistant("say ur  name")
    with sr.Microphone() as source:
        try:
            name=r2.listen(source)
            name_text=r2.recognize_google(name)
        except sr.UnknownValueError as e:
            speak_assistant("something went wrong")
    while(1):
            time.sleep(1)
            speak_assistant(name_text+" please speak Here")
            try:
                with sr.Microphone() as source:
                    audio=r1.listen(source,timeout=10,phrase_time_limit=15)
                    op=(r1.recognize_google(audio)).lower()
                    speak_assistant(op)
                    if "search" in op or "what" in op or "who" in op or "play" in op or "say" in op:
                        web_search(op)
                    elif "exit" in op or "abort" in op or "sleep" in op:
                        web_search(op)
                        break
                    elif "lock" in op:
                        try:
                            print(name_text," i am locking your system Good Bye ")
                            cmd=ctypes.windll.user32.LockWorkStation()
                            #cmd='rundll32.exe user32.dll, LockWorkStation'
                            time.sleep(1)
                            subprocess.call(cmd)
                        except sr.UnknownValueError as e:
                            print("something went wrong with you input")
                        except sr.RequestError as e:
                            print("something wrong")
                    elif "shutdown" in op or "close" in op or "shut" in op or "down" in op:
                        os.system("shutdown /s /t 1") 
                    elif "msg" in op or "sms" in op or "message" in op:
                        speak_assistant("please tell me what message i have to send")
                        msg_text=input_audio()
                        client1.sender_sms(name_text,msg_text)
                        speak_assistant("message sent successfully")
                    elif "send" in op or "beer" in op:
                        list=["Kingfisher","Tuborg" ,"Carlsberg","Budweiser","Heineken","Corona","Bira 91","Foster's"]
                        speak_assistant("what beer i need to send him . there multiple beers are there. select below")
                        for i in list:
                            speak_assistant(i)
                        
                        while True:
                            print("say here...")
                            try:

                                speech_text=input_audio()
                                speak_assistant("sending "+speech_text+" beer to ur friend.")
                            except sr.UnknownValueError as e:
                                print()
                            
                            if(speech_text):
                                break


                    else:
                        print("You are not speaking")
            except sr.UnknownValueError as e:
                speak_assistant("didnt recognize your audio")
                count+=1
                if(count>2):
                    speak_assistant("sorry your not responding....waiting time is over")
            except sr.RequestError as e:
                print("something went wrong")
                
    
           
