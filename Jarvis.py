# Jarvis -Virtual Assistance
import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install SpeechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import math
import time
import smtplib
import random
import sys
import time
from selenium import webdriver #pip install selenium
from selenium.webdriver.common.keys import Keys
import click #pip install click
import autoit #pip install autoit
import wolframalpha #pip install wolframalpha
import requests #pip install requests
import bs4 #pip install bs4
from email.message import EmailMessage #pip install email
from currency_converter import CurrencyConverter #pip install CurrencyConvertor
import json
import operator
#python -m pip install --upgrade pip => it is used to update the pip 

#setting up engine to set the voice of the system.

engine = pyttsx3.init('sapi5') # setting up engine as sapi5 as it is defined for windows
sys_voices = engine.getProperty('voices') #getting the voices of the system
sys_rate=engine.getProperty('rate') # getting the speed at which jarvis say the content
engine.setProperty('rate',sys_rate-20) # changing the rate of speech of jarvis
# print(voices[1].id) # used to get the voice either male or female
engine.setProperty('voice', sys_voices[1].id) # used to set the jarvis voice either male or female
wcheck=0
ucheck=0

#Jarvis Speak the audio
def speak(audio):
    engine.say(audio) # text to speech
    engine.runAndWait() # wait for some time

# Jarvis wishes based on time
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        print("Good Morning!")
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        print("Good Afternoon!")   
        speak("Good Afternoon!")   

    else:
        print("Good Evening!")  
        speak("Good Evening!")  

    print("Jarvis your Virtual Assistance Any task or work for me?")       
    speak("Jarvis your Virtual Assistance Any task or work for me?")       

#It takes microphone input from the user and returns string output or setting up speech to text engine
def takeCommand():

    r = sr.Recognizer() # used to recognize the source of speech
    with sr.Microphone() as source: # source used is microphone
        print("Listening...")
        r.pause_threshold = 0.8 #listen until 0.8 sec
        audio = r.listen(source) # converts the source data into audiodata

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') # converts the audiodata to the text
        print(f"User said: {query}\n")
    except Exception as e:
        # print(e)    
        print("sorry! I didn't get u")  
        speak("Sorry! I didn't get u")  
        return "None"
    return query

#sending an email with attachment(using smtp)
def sendEmailAttachment(to,subject,body,attachment_path):
    msg=EmailMessage()
    msg['Subject']=subject
    msg['From']=os.environ.get('my_mail')
    msg['To']=to
    msg.set_content(body) 
    file=open(attachment_path,'rb') # Read Byte Mode 
    file_data=file.read()
    file_name=file.name
    msg.add_attachment(file_data,maintype='application',subtype='octet-stream',filename=file_name)
    server = smtplib.SMTP('smtp.gmail.com', 587) # setting  up the smtp server or an smtp connection    
    server.ehlo() #it is used to identity the server.
    server.starttls() # tls is transport layer security i.e, set up a smtp connection in tls mode for security reasons
    server.login(os.environ.get('my_mail'), os.environ.get('my_password'));# os.environ returns the dictionary and get, set operations are performed on to the dictionary    
    server.send_message(msg)
    server.close()

#sending an email with only message(using smtp)
def sendEmailMessage(to,subject,body):
    msg=EmailMessage()
    msg['Subject']=subject
    msg['From']=os.environ.get('my_mail')
    msg['To']=to
    msg.set_content(body)
    server = smtplib.SMTP('smtp.gmail.com', 587) # setting  up the smtp server or an smtp connection    
    server.ehlo() #it is used to identity the server.
    server.starttls() # tls is transport layer security i.e, set up a smtp connection in tls mode for security reasons
    server.login(os.environ.get('my_mail'), os.environ.get('my_password'));# os.environ returns the dictionary and get, set operations are performed on to the dictionary    
    server.send_message(msg)
    server.close()
    print("email has sended")

# called when jarvis not recognises the name correctly to whom we want to send the message
def Whatsappnot(name,driver):
    wcount=0 # it is used to run the whatsapp module until a message is send
    dsend=0 # it is used when user say don't send the message
    atcheck=0 # it is used to check whether a proper document is attached or not
    ccheck=0 # it is used to send the message ot attachement if user says other than these two it repeats
    dsend1=0 # it used to come out from the inner message and attachment loop
    global ucheck
    while wcount==0: # it is used when message or attachment is not sended due to some exception
        try:
            if ucheck==0:
                user = driver.find_element_by_xpath('//span[@title="{}"]'.format(name)) # this is used to find the reciever
                user.click()  #it is used to click a specified name window to send the message
                ucheck=ucheck+1
            while ccheck==0:
                while True:
                    print("Do you want to send the message or an attachment")
                    speak("Do you want to send the message or an attachment")

                    tmsg=takeCommand().lower() # type of message either text or attachment
                    if 'don\'t send' in tmsg:  
                        print("Okay! Not sending the Message")
                        speak("Okay! Not sending the Message")
                        dsend=1
                        break
                    elif 'stop jarvis' in tmsg:
                        sys.exit()
                    elif 'none' not in tmsg:
                        break
                if dsend==1:
                    dsend=0
                    dsend1=1
                    break    
                if 'attachment' in tmsg:
                    while atcheck==0:
                        while True:
                            speak("Enter the Path of the folder of the Attachment")
                            apath=input("Enter the path of folder of the attachment:")
                            if  apath!='none':
                                break
                        while True:
                            speak("Enter the document name or filename or image name with extension that u want to send sir")
                            rname=input("enter the resource name:")
                            if rname!='none':
                                break                            
                        try:
                            clipbutton=driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
                            clipbutton.click()
                            time.sleep(5)

                            docbutton=driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button')
                            docbutton.click()
                            time.sleep(15)
                        except Exception as e:
                            print("Soory! Unable to perform the operation")
                            speak("Soory! Unable to perform the operation")
         
                        try:
                            autoit.control_focus("Open","Edit1")
                            autoit.control_send("Open","Edit1",apath+"\\"+rname)
                            time.sleep(2)
                            autoit.control_click("Open","Button1")
                            time.sleep(15)

                            whatsapp_send_button=driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span')
                            whatsapp_send_button.click()
                            time.sleep(5)
                            atcheck=atcheck+1
                            ccheck=ccheck+1
                            wcount=wcount+1
                        except Exception as e:
                            speak("Please enter a proper Path")

                elif 'message' in tmsg:
                    while True: # it is true until a valid message is specified
                        print('what is the message to be sended!')
                        speak('what is the message to be sended!')
                        msg=takeCommand().lower() # message that we want to send
                        #time.sleep(20)
                        if  'don\'t send' in msg:
                            dsend=dsend+1
                            print('Okay I won\'t be sending the message')
                            speak('Okay I won\'t be sending the message')
                            break
                        if 'stop' in msg:
                            print("Okay! Have a nice day")                          
                            speak("Okay! Have a nice day")
                            sys.exit()
                        if 'none' not in msg:
                            break
                    if dsend==1:
                        print("Okay! I won\'t be sending the message")
                        speak("Okay! I won\'t be sending the message")
                        dsend=0
                        dsend1=1
                        break
                    try: # it is important if the contact is not saved or xpath has changed by whatsaap. if xpath is changed by whatsapp then i have to edit it here. 
                        msg_box=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]') # it is the path of the messagebox in whatsapp reciever window that is obtained 
                        # by inspecting the webpage and then gettind the xpath by leftclick and copy and then xpath on the html tag.
                        msg_box.send_keys(msg) # it is to send the text in the message box.
                        driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button').click() # it is used to click the send button
                        wcount=wcount+1
                        ccheck=ccheck+1
                        print("Message is Successfully sended")                       
                        speak("Message is Successfully sended")
                    except Exception as e:
                        print("Please say a valid Name  First save the contact of your friend in your smart Phone Ilyas!")
                        speak("Please say a valid Name  First save the contact of your friend in your smart Phone Ilyas!")
            if dsend1==1:
                dsend1=0
                break   
        except Exception as e:
            print("Unable to find the name in your contact list")
            speak("Unable to find the name in your contact list")

#Whatsapp Messages
def Whatsappmsg():
    wcount=0 # it is used to run the whatsapp module until a message is send
    dsend=0 # it is used when user say don't send the message
    atcheck=0 # it is used to check whether a proper document is attached or not
    ycond=0 # it is to repeat the statemenets if the user have not told attachment or message
    dsend1=0 # it is used to comeout from the yes while loop
    global ucheck
    global wcheck
    global driver
    while wcount==0: # it used if the attachment or message is not sended but the thing is we have to say the name and type of message should be said agian(as there may be error in any thing specified by the user)
        if wcheck==0: # it is to scan the qr code only once
            try:
                driver = webdriver.Chrome('chromedriver.exe') # it is used to open the chrome by using chromedriver(that is present in this folder)
                driver.get('https://web.whatsapp.com/') # it is used to open the whatsapp
                print("Please open the whatsapp Web in your Smart phone Ilyas and scan the Q R code present on the screen")
                speak("Please open the whatsapp Web in your Smart phone Ilyas and scan the Q R code present on the screen")
                time.sleep(20)
                wcheck=wcheck+1 # incremented as only once the weebbrowser should be opened
            except Exception as e:
                print("Sorry Unable to Perfor the task")  
                speak("Sorry Unable to Perfor the task")  
        while True: # True until a valid reciever name is specified
            speak('To whom u want to send the message Ilyas')
            name=takeCommand().lower()
            if 'don\'t send' in name:
                dsend=1
                print('Okay! As your Wish')
                speak('Okay! As your Wish')
                break
            if 'stop jarvis' in name:
                sys.exit()
            if 'none' not in name:
                break
        if dsend==1:
            dsend=0
            break
        while True: # it is valid until a valid yes or not  is given by the user
            print(f"Do u want to send the Message to {name} Please say yes or not")
            speak(f"Do u want to send the Message to {name} Please say yes or not")
            yon=takeCommand().lower()
            if 'don\'t send' in yon:
                dsend=1
                print("Okay As your Wish")
                speak("Okay As your Wish")
                break
            if 'stop jarvis' in yon:
                print("Okay! Have a nice day")
                speak("Okay! Have a nice day")
                sys.exit()
            if 'none' not in yon:
                break
        if dsend==1: # it is to come out from the main while loop of whatsapp
            dsend=0
            break
        elif 'yes' in yon: 
            while ycond==0:
                try:
                    if ucheck==0:
                        user = driver.find_element_by_xpath('//span[@title="{}"]'.format(name)) # this is used to find the reciever
                        user.click()  #it is used to click a specified name window to send the message
                        ucheck=ucheck+1
                    while True:
                        print("Do you want to send the message or an attachment")
                        speak("Do you want to send the message or an attachment")
                        tmsg=takeCommand().lower() # type of message either text or attachment
                        if 'don\'t send' in tmsg:
                            print("Okay! iam not sending the message")
                            speak("Okay! iam not sending the message")
                            dsend=1
                            break
                        elif 'stop jarvis' in tmsg:
                            sys.exit()
                            break
                        elif 'none' not in tmsg:
                            break
                    if dsend==1:
                        dsend=0
                        dsend1=1
                        break
                    if 'attachment' in tmsg:
                        while atcheck==0:
                            while True:
                                speak("Enter the Path of the folder of the Attachment")
                                apath=input("Enter the path of folder of the attachment:")
                                if apath!=None:
                                    break
                            while True:
                                speak("Enter the document name or filename or image name with extension that u want to send sir")
                                rname=input("enter the resource name:")
                                if rname!=None:
                                    break                            
                            try:
                                clipbutton=driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
                                clipbutton.click()
                                time.sleep(5)

                                docbutton=driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button')
                                docbutton.click()
                                time.sleep(15)
                            except Exception as e:
                                print("Soory! Unable to perform the operation")
                                speak("Soory! Unable to perform the operation")
                            try:
                                autoit.control_focus("Open","Edit1")
                                autoit.control_send("Open","Edit1",apath+"\\"+rname)
                                time.sleep(2)
                                autoit.control_click("Open","Button1")
                                time.sleep(15)

                                whatsapp_send_button=driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span')
                                whatsapp_send_button.click()
                                time.sleep(5)
                                atcheck=atcheck+1
                                wcount=wcount+1
                                ycond=ycond+1
                            except Exception as e:
                                print("Please enter a proper Path")
                                speak("Please enter a proper Path")

                    elif 'message' in tmsg:
                        while True: # it is true until a valid message is specified
                            print('what should I say')
                            speak('what should I say')
                            msg=takeCommand().lower() # message that we want to send
                            if  'don\'t send' in msg:
                                dsend=1
                                print('Okay!  I won\'t be sending the message')
                                speak('Okay!  I won\'t be sending the message')
                                break
                            elif 'stop' in msg:
                                print("Okay! Have a nice day")
                                speak("Okay! Have a nice day")
                                sys.exit()
                            elif 'none' not in msg:
                                break
                        if dsend==1:
                            dsend=0
                            dsend1=1
                            break
                        try: # it is important if the contact is not saved or xpath has changed by whatsaap. if xpath is changed by whatsapp then i have to edit it here. 
                            msg_box=driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]') # it is the path of the messagebox in whatsapp reciever window that is obtained 
                            # by inspecting the webpage and then gettind the xpath by leftclick and copy and then xpath on the html tag.
                            msg_box.send_keys(msg) # it is to send the text in the message box.
                            driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button').click() # it is used to click the send button
                            wcount=wcount+1
                            ycond=ycond+1
                            print("Message is Successfully sended Ilyas")
                            speak("Message is Successfully sended Ilyas")
                        except Exception as e:
                            print("Please say a valid Name Ilyas! First save the contact of your friend in your smart Phone")
                            speak("Please say a valid Name Ilyas! First save the contact of your friend in your smart Phone")
                except Exception as e:
                 print("Please attach a proper file or say the correct message")
                 speak("Please attach a proper file or say the correct message")
            if dsend1==1:
                dsend1=0
                break    
        elif 'not' in yon:
            speak('Oops! I have Recognised the wrong name . Please enter the name to whom u want to send the message')
            rwname=input("Enter the name to whom u want to send the message")
            Whatsappnot(rwname,driver)  
            wcount=wcount+1

        else:
            print("Please say a proper command ")
            speak("Please say a proper command ")

#Jarvis Read the news based on command by using selenium and beautifulsoup
def News():
    driver = webdriver.Chrome('chromedriver.exe') # it is used to open the chrome by using chromedriver(that is present in this folder)
    ncount=0 # it is to print the number of headlines
    driver.get("https://timesofindia.indiatimes.com/news")
    time.sleep(1)
    req=requests.get('https://timesofindia.indiatimes.com/news') # it requests the specified page i.e we get the page source of the given href
    soup=bs4.BeautifulSoup(req.text,'lxml') # here we can also use html parsar(converting into the type of bs4 because now bs4 can be used to extract the imp info as requests can't do that)
    for i in soup.find_all('span'): # find dthe span element
        if i.get('class')!=None: # it is important as some classes are None
           if ncount==0: # it is to read only one headline
                if i.get('class')[0]=='w_desc':
                    speak(i.text)
                    ncount=ncount+1

#wikipedia module using wikipedia api
def Wikipedia(query):
    print('Searching Wikipedia...')
    speak('Searching Wikipedia...')
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=2)
    print("According to Wikipedia")
    speak("According to Wikipedia")
    print(results)
    speak(results)
        
# Playing the music
def Music(query):
    sc=0 # if it is zero that means no song has yet played sc=song condition
    scount=0 # it is used  to count no. of songs in the folder . if count exceeds the no. of songs in the folder then it  prints song is not found
    dplay=0 # it is to stop playing a song in global i.e in specific song
    dplay1=0 # it is also to stop playing a song in local i.e for loop of specific song asking for which song
    tcheck=0 # it is used to check whether it is true or not. if it is true then while loop continues to ask which song u would like to p
    music_dir=os.environ["songspath"] #it is to get the directory path from environment variable songspath
    
    songs = os.listdir(music_dir) # it gives the list of songs that are present in that directory 
    songswe=[x.split('.')[0] for x in songs] # it deletes the part of the name of the song starting with .
            

    while sc==0:
        print("do u want to play a random song or any specific song")
        speak("do u want to play a random song or any specific song")
        content=takeCommand().lower()
                

        if 'random' in content:
            sc=sc+1
            a=random.randrange(0,(len(songs)-1),3)# selecting  a random number with step 3
            os.startfile(os.path.join(music_dir, songs[a])) # it opens the directory and then the song by using the index
             
                
        elif 'specific' in content:
            print(songswe)
            sc=sc+1; # sc is incremented so that only one song should be played
                    
                    
            while True:
                print("Which one u would like to play")
                speak("Which one u would like to play")
                content1=takeCommand().lower()
                    

                for i in songswe:
                    scount=scount+1  # it is used to count no. of songs are being compared if no song matches then it used to raise the exception 
                    #print(scount)
                            
                            
                    if i in content1:
                       tcheck=tcheck+1
                       os.startfile(os.path.join(music_dir, songs[scount-1])) # integer is passed to the songs list. we cant use i.                         
                       break # break as only one song should be played
                            
                            
                    elif 'don\'t play' in content1:
                        dplay1=dplay1+1
                        break    
                            
                            
                    elif scount==len(songs):
                      scount=0
                      print("Oops! Please try the different Song")              
                      speak("Oops! Please try the different Song")              
                        

                if 'stop' in content1:
                    print('okay! have a nice day')
                    speak('okay! have a nice day')
                    sys.exit()          
                        

                if tcheck==1:
                    break;               
                        

                elif 'don\'t play' in content1:
                    dplay=dplay+1
                    print("okay! Iam not playing")
                    speak("okay! Iam not playing")
                    break    
                
                
        elif 'stop' in content:
            print("okay! have a nice day")
            speak("okay! have a nice day")
            sys.exit()
                
                
        elif 'don\'t play' in content:
            print("okay! Iam not Playing")
            speak("okay! Iam not Playing")
            break
                
                
        elif dplay==1 or dplay1==1:
            break
                
                
        elif 'specific' not in content or 'random' not in content:
            print("Please Say a Proper Command!")
            speak("Please Say a Proper Command!")

#Sending Email if it is not stored in the database
def Emailnotstored(recievermid):
    to = recievermid
    while True:
        print("What is the subject of the mail?")
        speak("What is the subject of the mail?")
        subject= takeCommand().lower()         # the content that has to be sended
        if 'don\'t send' in subject: # it is used to come out from the second inner while loop
            print('okay! as your wish...')
            speak('okay! as your wish...')
            break    # it is used to exit from the second inner while loop
        elif 'stop' in subject:
            print('okay! have a nice day')
            speak('okay! have a nice day')
            sys.exit()    
        elif 'none' not in subject:                
            break # it is to come out from the second inner loop
    while True:
        print("What is the body of the mail?")
        speak("What is the body of the mail?")
        body= takeCommand().lower()         # the content that has to be sended
        if 'don\'t send' in body: # it is used to come out from the second inner while loop
            print('okay! as your wish...')            
            speak('okay! as your wish...')
            break    # it is used to exit from the second inner while loop
        elif 'stop' in body:
            print('okay! have a nice day')
            speak('okay! have a nice day')
            sys.exit()    
        elif 'none' not in body:
            break                
    while True:
        print("Do want to attach the Documents or any files Please say yes or not")
        speak("Do want to attach the Documents or any files Please say yes or not")
        eaf=takeCommand().lower() #afe attachment file 
        if 'don\'t send' in eaf:
            print("Okay! iam not sending the email")
            speak("Okay! iam not sending the email")
            break
        if 'stop' in eaf:
            print('Okay! Have a nice day')
            speak('Okay! Have a nice day')
            sys.exit()
        elif 'none' not in eaf:
            break
    if 'yes' in eaf:
        while True:
            speak("Please enter the path of the Document or a file")
            peaf=input("Enter the path of the Document for email:")
            if 'none' not in peaf:#path of the email attachment file
                break
        while True:
            speak("Please enter the file name or document name that you wanted to send with extension")
            neaf=input("Enter the file name or document name with extension")
            if 'none' not in neaf: #name of email attachment file
                attachment_path=peaf+"\\"+neaf
                sendEmailAttachment(to,subject,body,attachment_path)
                print("Email has been sended")
                speak("Email has been sended")
                break
    elif 'not' in eaf:
        sendEmailMessage(to,subject,body)
        print("Email has been sended")
        speak("Email has been sended")
    
#Sending the mail
def Email(query):
    cond=0 # it is used to repeat a while loop until a valid id is mentioned
    dsend=0 # it is used to not to send the mail
    dsend1=0# it is used to comeout from the outer loop
    while cond==0:  # it is true until a user does not say a command
        recievermid='none' # it is used to check a proper mail id either it is stored or not
        print("To Whom U Want to send the Mail")
        speak("To Whom U Want to send the Mail")
        reciever=takeCommand().lower()
        if 'hello' in reciever: # we have to just add an environ. variable and  these two line code of try and catch to add the new gmail id.
            try:
                recievermid=os.environ['aijaz']
                cond=cond+1 # it is used to cancel the outer loop
            except KeyError:
                print("no mail id for aijaz")
                speak("no mail id for aijaz")
        elif 'champion' in reciever:
            try:
                recievermid=os.environ['champion']
                cond=cond+1
            except KeyError:
                print("no mail id for champion") 
                speak("no mail id for champion") 
        elif 'don\'t send' in reciever:
            print("Okay! as your wish...")
            speak("Okay! as your wish...")
            break
        elif 'stop' in reciever:
            print("Okay! have a nice day")
            speak("Okay! have a nice day")
            sys.exit()
        if 'none' not  in recievermid:
            while cond==1: # it is to get executed only once the user says the command and it is false if user accepts the mail id
                try: # this part is generic irrespective of any mail id.
                    print(recievermid)
                    print(f"Do u Want to send the mail to {recievermid}. Please say Yes or not!..")
                    speak(f"Do u Want to send the mail to {recievermid}. Please say Yes or not!..")
                    content1=takeCommand().lower() # taking input as yes or not. remember not if we take no it wont work properly as string contains bydefault none.
                    if 'yes' in content1: #checking whether the user accepting the id to send the mail
                        cond=cond+1# it is used to exit the first inner while loop
                        to = recievermid
                        while True:
                            print("What is the subject of the mail?")
                            speak("What is the subject of the mail?")
                            subject= takeCommand().lower()         # the content that has to be sended
                            #print("listening...")
                            if 'don\'t send' in subject: # it is used to come out from the second inner while loop
                                print('okay!  as your wish...')
                                speak('okay!  as your wish...')
                                dsend=1 # it is used to exit from first inner and main while loop
                                break    # it is used to exit from the second inner while loop
                            elif 'stop' in subject:
                                print('okay! have a nice day')
                                speak('okay! have a nice day')
                                sys.exit()    
                            elif 'none' not in subject:                
                                break # it is to come out from the second inner loop
                        if dsend==1: # it is very important it is to come out from the first inner while loop
                            dsend=0
                            dsend1=0
                            break

                        while True:
                            print("What is the body of the mail?")
                            speak("What is the body of the mail?")
                            body= takeCommand().lower()         # the content that has to be sended
                            if 'don\'t send' in body: # it is used to come out from the second inner while loop
                                print('okay! as your wish...')
                                speak('okay! as your wish...')
                                dsend=1 # it is used to exit from first inner and main while loop
                                break    # it is used to exit from the second inner while loop
                            elif 'stop' in body:
                                print('okay!  have a nice day')
                                speak('okay!  have a nice day')
                                sys.exit()    
                            elif 'none' not in body:
                                break
                        if dsend==1:
                            dsend=0
                            dsend1=1
                            break                
                        while True:
                            print("Do want to attach the Documents or any files Please say yes or not")
                            speak("Do want to attach the Documents or any files Please say yes or not")
                            eaf=takeCommand().lower() #afe attachment file 
                            if 'don\'t send' in eaf:
                                print("Okay Iam not sending ")
                                speak("Okay Iam not sending ")
                                dsend=1
                                break
                            if 'stop' in eaf:
                                print('Okay! Have a nice day')
                                speak('Okay! Have a nice day')
                                sys.exit()
                            elif 'none' not in eaf:
                                break
                        if dsend==1:
                            dsend=0
                            dsend1=1
                            break
                        if 'yes' in eaf:
                            while True:
                                speak("Please enter the path of the Document or a file")
                                peaf=input("Enter the path of the Document for email:")
                                if 'none' not in peaf:#path of the email attachment file
                                    break
                            while True:
                                speak("Please enter the file name or document name that you wanted to send with extension")
                                neaf=input("Enter the file name or document name with extension:")
                                if 'none' not in neaf: #name of email attachment file
                                    attachment_path=peaf+"\\"+neaf
                                    sendEmailAttachment(to,subject,body,attachment_path)
                                    dsend=1
                                    print("Email sended successfully")
                                    speak("Email sended successfully")
                                    break
                        elif 'not' in eaf:
                            sendEmailMessage(to,subject,body)
                            print("Email has been sended")
                            speak("Email has been sended")
                            break
                        if dsend==1:
                            dsend=0
                            dsend1=1
                            break
                    elif 'not' in content1:
                        cond=cond+1# it is used to exit the inner loop
                        speak("Ohh!.please enter the mail")
                        myinput=input('enter the mail:')  # it is used to manually enter the mail id. and send the mail
                        to=myinput
                        Emailnotstored(to)
                    elif 'don\'t send' in content1:
                        dsend=1 # it is to come out from the main while loop
                        print('okay! I am sending')
                        speak('okay! I am sending')
                        break # it is to come out from the first while loop                
                    if dsend==1:
                        dsend=0
                        break
                    elif 'stop' in content1:
                        print("Okay! Have a nice day")
                        speak("Okay! Have a nice day")
                        sys.exit()                    
                except Exception as e:
                    print("Oops!. I am not able to send this email")    
                    speak("Oops!. I am not able to send this email")    
        elif 'none' in reciever:
            print("you have not told any name to whom u want to send the mail. Please say a proper name Ilyas..")
            speak("you have not told any name to whom u want to send the mail. Please say a proper name Ilyas.")
            recievermid="1"
        elif 'none' in recievermid:
            cond=cond+1# it is used to exit the inner loop
            speak("Ohh! I dont have mail id.please enter the mail")
            to=input('enter the mail:')  # it is used to manually enter the mail id. and send the mail
            Emailnotstored(to)
            print("Email has been sended successfully")
            speak("Email has been sended successfully")

        if dsend==1:
            dsend=0
            break # it is come out from the main while loop
        if dsend1==1:
            dsend1=0
            break
       
#if User says something different
def Nonecondition(query):
    while True:
            print(f"Did U told {query} Please say yes or not")
            speak(f"Did U told {query} Please say yes or not")
            nc=takeCommand().lower()
            if 'not' in nc:
                print("Okay! Say Once Again Please")
                speak("Okay! Say Once Again Please")
                break 
            elif 'yes' in nc:
                try:
                    i=query
                    app_id="9P5AP2-UGLKTGQHHW"
                    client=wolframalpha.Client(app_id)
                    res=client.query(i)
                    answer=next(res.results).text
                    speak(answer)
                    break
                except Exception as e:
                    print("Sorry I can\'t Perform the Operation")
                    speak("Sorry I can\'t Perform the Operation")
                    break

#Basic Calculations
def calci(cal):
    try:
        def get_operator_fn(op):
            return {
                '+' : operator.add,
                '-' : operator.sub,
                'x' : operator.mul,
                'divided' :operator.__truediv__,
                'Mod' : operator.mod,
                'mod' : operator.mod,
                '^' : operator.xor,
                }[op]
        def eval_binary_expr(op1, oper, op2):
            op1,op2 = int(op1), int(op2)
            return get_operator_fn(oper)(op1, op2)
        print(eval_binary_expr(*(cal.split())))
        return speak(f"the answer is {eval_binary_expr(*(cal.split()))}")    
    except Exception as e:
        print("Say that again please")
        speak("Say that again please")
        return "none"

#Currency Converter
def currency():
    try:
        c = CurrencyConverter()
        while True:
            print("what amount do you want to converted")
            speak("what amount do you want to converted")
            AMOUNT=takeCommand().isnumeric
            if 'none' not in AMOUNT:
                break
        while True:
            print("from which currency do you want to convert")
            speak("from which currency do you want to convert")
            FROM=takeCommand().upper()
            if 'none' not in FROM:
                break
        while True:
            print("to which currency do you want to convert")
            speak("to which currency do you want to convert")
            TO=takeCommand().upper()
            if 'none' not in TO:
                break
        print(c.convert(AMOUNT,FROM,TO))    
        speak(f"{AMOUNT} {FROM} is {c.convert(AMOUNT,FROM,TO)} {TO}  ")
    except Exception as e:
        print("Say that again Please")
        speak("Say that again please")

#daily dairy 
def diary(myday):

      date =  datetime.datetime.now().strftime("%H:%M:%S")
      entry = "\nDear Diary\n"
      f = open("mydiary.txt", "a") # a means append, this stops new data overwriting old
      f.write(date)
      f.write(entry)
      f.write(myday)
      f.close()
#time function
def timeManipulation():
    t=time.now()
    
def weatherinfo(city):
     
    api_key = "ba74d82c297c71baa6d874a4c98d37f8"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Give city name 
    city_name = city 
  
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
     
    response = requests.get(complete_url) 

    x = response.json() 

    if x["cod"] != "404": 
        
        y = x["main"] 
        
        current_temperature = y["temp"] 
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"] 
        z = x["weather"]  
        weather_description = z[0]["description"] 
        result=(f" Temperature in {city} is {str(current_temperature)} kelvin and atmospheric pressure is{str(current_pressure)} hpa and humidity is {str(current_humidiy)} percentage  it is {str(weather_description)} here")
        print(result)           
        return  speak(result)
        
        
    else: 
        print(" City Not Found ")
# Main Method
if __name__ == "__main__":
   
    wishMe()  
    wcheck=0
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            Wikipedia(query)


        elif 'open youtube' in query:
            webbrowser.open("youtube.com")


        elif 'open google' in query:
            webbrowser.open("google.com")


        elif 'open stackoverflow' in query or 'stackoverflow' in query or 'stack overflow' in query:
            webbrowser.open('stackoverflow.com')

        elif 'news' in query:
            News()


        elif 'play music' in query:
            Music(query)
                

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            print(f"Sir, the time is {strTime}")
            speak(f"Sir, the time is {strTime}")
          
        
        elif 'visual studio code' in query or 'vscode' in query or 'vs code' in query:
            try:
                codepath=os.environ["vscode"]
                os.startfile(codepath)
            except KeyError:
                print('Oops! Unable to Open the VISUAL STUDIO CODE')
                speak('Oops! Unable to Open the VISUAL STUDIO CODE')
        # allow less secure app. open your gmail id home page and go into security and search for less secure app and allow access to less secure app
        # send a mail using your mail id please set the environ variables based on name and gmail ids. 
        
        elif 'currency' in query or 'currency convertor' in query:
            currency()
        
        if 'diary' in query:
            print("hello  how have you been? how was your day today")
            speak("hello  how have you been? how was your day today")
            myday=takeCommand()
            diary(myday)

        elif 'calculator' in query or 'calculations' in query:
            con=0
            while True:
                print("what calculation can i do for you")
                speak("what calculation can i do for you")
                cal=takeCommand()
                print(cal)
                calci(cal)
                while True:
                    print("Any more Operations Ilyas Please say yes or not")
                    speak("Any more Operations Ilyas Please say yes or not")
                    cmd=takeCommand().lower()
                    if 'yes' in cmd:
                        break
                    if 'not' in cmd: 
                        con=1
                        break
                if con==1:
                    break    
        
        if 'weather' in query:
            while True:
                print("which cities weather do you want to know")
                speak("which cities weather do you want to know")
                city=takeCommand()
                if 'none' not in city:
                    weatherinfo(city)
                    break

        elif 'email' in query or 'mail' in query:
            Email(query)
        

        elif 'stop'in query or 'jarvis' in query:
            print("Okay! Have a nice day.")
            speak("Okay! Have a nice day.")
            #sys.exit()
            break
    
        elif 'search' in query:
            query=query.replace('search','')
            webbrowser.open(query)    

        
        elif 'whatsapp' in query or 'messages' in query: # a space in the condition also plays an important role
           Whatsappmsg()
        
        
        elif 'none' not in query:
           Nonecondition(query)
        elif 'okay'in query or 'ok' in query:
            print("Okay!  As your Wish")            
            speak("Okay!  As your Wish")
            sys.exit()
       

            
      #desktop application
    
