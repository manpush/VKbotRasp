import vk_api
import requests
import re
from datetime import datetime, timedelta
import os
import urllib.request
import subprocess
import csv
import camelot
import sys
import time
from threading import Thread
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
os.system("pwd")
class mailer(Thread):
    def __init__(self, text):
        Thread.__init__(self)
        self.text = text

    def run(self):
        vk_session = VkApi(token="14ddcb3b6b0b32b3eb6267d173aff130fa57d50869ce8aae629a96cd9ef749651c9d5e1705fd7e1683458")
        longpoll = VkBotLongPoll(vk_session, "194668032")
        vk = vk_session.get_api()

        t=self.text
        i=10
        grs=[]
        while t[i]!=' ':
            if t[i]==',': 
                i+=1
            grs.append(str(t[i]+t[i+1]+t[i+2]))
            i+=3
        text=[]
        while t[i]!='|':
            text.append(t[i])
            i+=1
        print(text)
        for i in grs:
            if groupsN.get(i)!=None:
                for j in groupsN[i]:
                    vk.messages.send(random_id=0, peer_id=j ,message=''.join(text))
            else:
                vk.messages.send(random_id=0, peer_id=230245992 ,message='not found '+i)

       




class MyThread(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id
    
    def run(self):
        id=self.id
        vk_session = VkApi(token="14ddcb3b6b0b32b3eb6267d173aff130fa57d50869ce8aae629a96cd9ef749651c9d5e1705fd7e1683458")
        longpoll = VkBotLongPoll(vk_session, "194668032")
        vk = vk_session.get_api()

        f=0
        if groups.get(id)==None and f==0:
                vk.messages.send(random_id=0, peer_id=id,message='Я забыл из какой ты группы, напиши номер группы пж')
                f=1
        else:
                vk.messages.send(random_id=0, peer_id=id,message='На когда группа '+str(groups.get(id))+' желает расписание?')
                f=2
        for event in longpoll.listen():
            if f==1 and re.fullmatch('[0-9]{3}',event.object['text'].lower()) and event.object['peer_id']==id:
                groups[id]=re.search('[0-9]{3}',event.object['text'].lower()).group()
                file = open("groups.txt", "a")
                file.write(str(id)+'\n')
                file.write(re.search('[0-9]{3}',event.object['text'].lower()).group()+'\n')
                file.close()
                vk.messages.send(random_id=0, peer_id=id,message='На когда группа '+str(groups.get(id))+' желает расписание?')
                f=2
            elif f==1:
                vk.messages.send(random_id=0, peer_id=id,message='Номер группы пожалуйста..')
            
            elif re.fullmatch('^(после)*завтра',event.object['text'].lower()) and f==2 and id==event.object['peer_id']:
                f=3
                date=datetime.now() + timedelta(days=1+len(re.findall('после',event.object['text'].lower())))
                date = date.strftime("%d.%m.%y")
                vk.messages.send(random_id=0, peer_id=id,message='Ща буит расписание на '+date)
                go(id, date, str(groups.get(id)))
                break
               
            elif re.fullmatch('^сегодня',event.object['text'].lower()) and f==2 and id==event.object['peer_id']:
                date=datetime.now().strftime("%d.%m.%y")
                vk.messages.send(random_id=0, peer_id=id,message='Ща буит расписание на '+date)
                go(id, date, str(groups.get(id)))
                break
               
            elif re.fullmatch('[0-9]{2}\.[0-9]{2}\.[0-9]{4}',event.object['text'].lower()) and f==2 and id==event.object['peer_id']:
                date=re.search('[0-9]{2}\.[0-9]{2}\.[0-9]{4}',event.object['text'].lower()).group()
                vk.messages.send(random_id=0, peer_id=event.object['peer_id'],message='Ща буит расписание на '+date)
                go(id, date, str(groups.get(id)))
                break
            elif event.object['peer_id']==id and f==2:
                vk.messages.send(random_id=0, peer_id=id,message='Напиши, когда? Завтра? Сегодня? Полслезавтра?')
        

def go(id, date, group):
    if findfile(date):
        vk.messages.send(random_id=0, peer_id=id,message="Расписания нет(((")
    else:
        getCsv(date)
        createRasp(date, group)
        fi = open('txt/'+date+'.txt')
        vk.messages.send(random_id=0, peer_id=id,message=fi.read())
        fi.close()
def findRasp(id):

    my_thread = MyThread(id)
    my_thread.start()

def mailing(text):
    m=mailer(text)
    m.start()


def getCsv(name):#function from NET
    tables = camelot.read_pdf('./pdf/'+name+'.pdf')
    tables
    # <TableList n=1>
    tables.export('foo.csv', f='csv', compress=True) # json, excel, html, sqlite
    tables[0]
    # <Table shape=(7, 7)>
    tables[0].parsing_report
    {
        'accuracy': 99.02,
        'whitespace': 12.24,
        'order': 1,
        'page': 1
    }
    tables[0].to_csv('csv/'+name+'.csv') # to_json, to_excel, to_html, to_sqlite
    tables[0].df # get a pandas DataFrame!
def getUrl(line):
    i=0
    while(i<len(line)-8):
        if line[i]=='<' and line[i+1]=='a' and line[i+2]==' ' and line[i+3]=='h' and line[i+4]=='r' and line[i+5]=='e' and line[i+6]=='f' and line[i+7]=='=':
            i+=9
            res=''
            while(line[i]!='\"'):
                res+=line[i]
                i+=1
                if line[i]=='&' and line[i+1]=='a' and line[i+2]=='m' and line[i+3]=='p':
                    break
        i+=1
    print(res)
    return res
def findfile(now):
    # try:
    #     if open(now+'.pdf'):
    #         res=0
    # except FileNotFoundError:
    # # else:
    link=urllib.request.urlopen('http://www.mgkit.ru/studentu/raspisanie-zanatij')
    #go to url and open html file
    lines = []
    for line in link.readlines():
        if line.find(now.encode('utf-8')) != -1: # find files now date
            lines.append(line.decode('utf-8')) #save strings with links
    for i in range(len(lines)):
        lines[i]=getUrl(lines[i]) # save oll lonks
    link.close()
    if len(lines)==0:
        res=1
    else:
        print(lines[0])
        os.system('wget -O pdf/'+now+'.pdf '+'http://www.mgkit.ru'+lines[0]+' 2> logDownload.txt') # get file
        res=0
    # except:
    #     print("unspected err")
    #     res = 0
    return res
def createRasp(now, group):
    mass=[]

    #findGroup=input("Введите номер группы: ")
    findGroup=group
    with open('csv/'+now+'.csv', newline='') as File:  
        reader = csv.reader(File)
        for row in reader:
            mass.append(row)
    #save csv to mass[][] : 1st arg - line, 2nd arg - column
    out = open('txt/'+now+'.txt', "w")
    out.write('Расписание на '+now)
    for i in range(len(mass)):
        for j in range(len(mass[i])):
            if (re.search(''+findGroup, mass[i][j])!=None or re.search(r''+findGroup[0]+r'.*Курс', mass[i][j])!=None) and re.search(r"[0-9][0-9]:[0-9][0-9]", mass[i][0])!=None:
                out.write('\n')
                out.write(mass[i][0]+'\n')
                for k in range(4):
                    out.write(mass[i+k][j].replace("\n", "")+'\n')
    out.close()
    print("good")
#--------------main---------------
# if findfile(date):
#     vk.messages.send(random_id=0, peer_id=event.object['peer_id'],message="Расписания нет(((")
# else:
#     getCsv(date)
#     createRasp(date)
#     fi = open(date+'.txt')
#     vk.messages.send(random_id=0, peer_id=event.object['peer_id'],message=fi.read())
#     fi.close()
logs = open("allLog.txt", "a")
groups={}
groupsN={}
while 1:
    vk_session = VkApi(token="14ddcb3b6b0b32b3eb6267d173aff130fa57d50869ce8aae629a96cd9ef749651c9d5e1705fd7e1683458")
    longpoll = VkBotLongPoll(vk_session, "194668032")
    vk = vk_session.get_api()

    file = open("groups.txt", "r")
    i=0
    for line in file.readlines():
        if i==0:
            buf=int(line)
            i+=1
        else:
            i=0
            groups[buf]=str(int(line))
            if groupsN.get(str(int(line)))==None:
                groupsN[str(int(line))]=[buf]
            else:
                groupsN[str(int(line))].append(buf)
    file.close()
    try:
        # print(str(groupsN))
        vk.messages.send(random_id=0, peer_id=230245992,message=str(groupsN))
        f=0
        ui=0
        for event in longpoll.listen():
            try:
                if event.type == VkBotEventType.MESSAGE_NEW:
                    print('user https://vk.com/id'+str(event.object['from_id']), event.object['peer_id'], event.object['text'])
                    logs.write("from "+str(event.object['peer_id'])+' user https://vk.com/id'+str(event.object['from_id'])+ "-"+str(event.object['text'])+'\n')
                    if re.fullmatch('^.расписание', event.object['text'].lower())and f==0:
                        findRasp(event.object['peer_id'])
                    elif event.object['peer_id']==230245992 and re.fullmatch(r'^.рассылка.*', event.object['text'].lower()):
                        print('maill') 
                        mailing(event.object['text'].lower())

                    elif  event.object['peer_id']<2000000000:
                        print(event.object['peer_id'])
                        vk.messages.send(random_id=0, peer_id= 230245992 ,message="from "+"https://vk.com/id"+str(event.object['from_id'])+'\n'+str(event.object['text']))
                    # time.sleep(1)
                    # vk.messages.send(random_id=0, peer_id=event.object['peer_id'],message='Соре, мне нужна помощь, напиши любой текст (это временно, просто мой разраб лошара)')

                    # if groups.get(event.object['peer_id'])==None:
                    #     vk.messages.send(random_id=0, peer_id=event.object['peer_id'],message='Я забыл из какой ты группы, напиши номер группы пж')
                    # ui=event.object['peer_id']
                    # #if event.from_user:
                    # f=1
                    # vk.messages.send(random_id=0, peer_id=event.object['peer_id'],message='На когда?')
                # elif re.fullmatch('^(после)*завтра',event.object['text'].lower()) and f==1 and ui==event.object['peer_id']:
                #     f=0
                #     date=datetime.now() + timedelta(days=1+len(re.findall('после',event.object['text'].lower())))
                #     date = date.strftime("%d.%m.%y")
                #     vk.messages.send(random_id=0, peer_id=event.object['peer_id'],message='Ща буит расписание на '+date)
                #     findRasp(event.object['peer_id'], date, group)
                   
                # elif re.fullmatch('^сегодня',event.object['text'].lower()) and f==1 and ui==event.object['peer_id']:
                #     f=0
                #     date=datetime.now().strftime("%d.%m.%y")
                #     vk.messages.send(random_id=0, peer_id=event.object['peer_id'],message='Ща буит расписание на '+date)
                #     findRasp(event.object['peer_id'], date, group)
                   
                # elif re.fullmatch('[0-9]{2}\.[0-9]{2}\.[0-9]{4}',event.object['text'].lower()) and f==1 and ui==event.object['peer_id']:
                #     f=0
                #     date=re.search('[0-9]{2}\.[0-9]{2}\.[0-9]{4}',event.object['text'].lower()).group()
                #     vk.messages.send(random_id=0, peer_id=event.object['peer_id'],message='Ща буит расписание на '+date)
                #     findRasp(event.object['peer_id'], date, group)


                # elif event.object['peer_id']==ui and f==1:
                #     vk.messages.send(random_id=0, peer_id=event.object['peer_id'],message='Напиши, когда? Завтра? Сегодня? Полслезавтра?')
                # print("from ", event.object['peer_id'], " ", event.object['text'])
            except vk_api.AuthError as err_msg:
                print(event)
                print("\a\aerr"+err_msg)
                continue
            # except:
            #     print(event)
            #     print("\a\aerr")
                    

    except vk_api.AuthError as err_msg:
        print('\a\a\aerr: '+err_msg)
        logs.close()
    except:
        print('\a\a\aerr')
        logs.close()
