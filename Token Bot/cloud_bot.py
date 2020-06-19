import json
import requests
import time
import urllib
from datetime import date
#from datetime import datetime
import datetime
import os
from os import path
import calendar

#https://api.telegram.org/bot1211353480:AAHh1r4Kxa_J31AJ4lXAUtZN8oogPURUfyc/getUpdates
#TOKEN = "1136081344:AAH5wSQSykCB_gtLbe7wABYlIKBfB_a0luE"
TOKEN="1211353480:AAHh1r4Kxa_J31AJ4lXAUtZN8oogPURUfyc"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
DATA=[]
valid_address=['A201','A202','A203','A204','A301','A302','A303','A304','A401',
'A402','A403','A404','A501','A502','A503','A504','A601','A602','A603','A604',
'A701','A702','A703','A704','A801','A802','A803','A804','A901','A902','A903',
'A904','B001','B002','B003','B004','B101','B102','B103','B104','B201','B202',
'B203','B204','B301','B302','B303','B304','B401','B402','B403','B404','B501',
'B502','B503','B504','B601','B602','B603','B604','B701','B702','B703','B704',
'B801','B802','B803','B804','B901','B902','B903','B904','C001','C002','C101',
'C102','C201','C202','C301','C302','C401','C402','C501','C502','C601','C602',
'C701','C702','C801','C802','C901','C902','D001','D002','D003','D004','D005',
'D006','D101','D102','D103','D104','D105','D106','D201','D202','D203','D204',
'D205','D206','D301','D302','D303','D304','D305','D306','D401','D402','D403',
'D404','D405','D406','D501','D502','D503','D504','D505','D506','D601','D602',
'D603','D604','D605','D606','D701','D702','D703','D704','D705','D706','D801',
'D802','D803','D804','D805','D806','D901','D902','D903','D904','D905','D906',
'E101','E102','E103','E104','E201','E202','E203','E204','E301','E302','E303',
'E304','E401','E402','E403','E404','E501','E502','E503','E504','E601','E602',
'E603','E604','E701','E702','E703','E704','E801','E802','E803','E804','E901',
'E902','E903','E904','F401','F402','F403','F404','F501','F502','F503','F504',
'F601','F602','F603','F604','F701','F702','F703','F704','F801','F802','F803',
'F804','F901','F902','F903','F904']
TOKENS_COL=[]
ADMIN_ID=-460125915 #TMS admin group
#ADMIN_ID=928263370  Arvind YN
#ADMIN_ID=1279557157
RESIDENT_GROUP_ID=-1001432365387 #Century Owners and Residents Group ID
#RESIDENT_GROUP_ID=1279557157 #Pritika's chat id

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    try:
        url = URL + "getUpdates?timeout=100"
        if offset:
            url += "&offset={}".format(offset)
        js = get_json_from_url(url)
        return js
    except Exception as e:
        print(e)

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def validate_apt_no(apt_no):
    for va in valid_address:
        if(va==apt_no):
            return True
    return False

def unique_apt_no(apt_no):
    for token_res in DATA:
        if(token_res[1]==apt_no):
            return False
    return True

def unique_chat_id(chat_id):
    for token_res in DATA:
        if(int(token_res[3])==chat_id):
            return False
    return True

def reset_last_update_id():
    try:
        h=open("last_update_id.txt",'r')
        last_update_id=int(h.read())
        h.close()
    except:
        last_update_id=None
    return last_update_id

def get_e_bot_start_time():
    try:
        h=open("token_start_time.txt",'r')
        e_bot_start_time=float(h.read())
        h.close()
    except:
        e_bot_start_time=None
    return e_bot_start_time

def get_last_token():
    try:
        f=open('token_data.txt','r')
        content=f.read()
        f.close()
        content_list=content.split('\n')
        for i in content_list[:-1]:
            DATA.append(i.split('|'))
        token_id=len(content_list[:-1])
    except:
        token_id=0
    return token_id

def get_collected_tokens():
    try:
        f=open("collected_tokens.txt",'r')
        content=f.read()
        f.close()
        content_list=content.split('\n')
        for i in content_list[:-1]:
            TOKENS_COL.append(i)
        token_counter=len(content_list[:-1])
    except:
        token_counter=0
    return token_counter

def write_token(token_info):
    f=open('token_data.txt','a')
    string=''
    for info in token_info[:-1]:
        string+=str(info)+'|'
    string+=str(token_info[-1])+'\n'
    f.write(string)
    f.close()

def current_status(chat_id,token_counter,last_token_id):
    int_tokens_col=[]
    for tok in TOKENS_COL:
        int_tokens_col.append(int(tok))
    int_tokens_col.sort()
    if(token_counter!=0):
        send_message("Total tokens issued: {} \nTokens Processed: {}\nMax Token Processed: {}".format(last_token_id,token_counter,int_tokens_col[-1]),chat_id)
    else:
        send_message("Total tokens issued: {} \nTokens Processed: {}".format(last_token_id,token_counter),chat_id)

def list_all(chat_id):
    message='Issued Tokens List:\n'
    for info in DATA:
        message+=str(info[0]).rjust(3,'0')+" "+str(info[1])+" "+str(info[2])+'\n'
    message+="\nProcessed Token Numbers:\n"
    int_tokens_col=[]
    for tok in TOKENS_COL:
        int_tokens_col.append(int(tok))
    int_tokens_col.sort()
    for tok in int_tokens_col:
        message+=str(tok).rjust(3,' ')+", "
    if(len(int_tokens_col)==0):
        send_message(message,chat_id)
    else:
        send_message(message[:-2],chat_id)

def inform_admin(token_counter):
    send_message("{} tokens have been processed. Please inform token holders {}-{}".format(token_counter,token_counter+6,token_counter+10),ADMIN_ID)
    send_message("{} tokens have been processed. Token holders {}-{}, please go down.".format(token_counter,token_counter+6,token_counter+10),RESIDENT_GROUP_ID)

def issue_token(apt_no,chat_id,name,last_token_id):
    #Adding 19800 to convert from GMT to IST to help to get the correct date in India
    today=datetime.datetime.fromtimestamp(calendar.timegm(time.gmtime())+19800).strftime('%d-%m-%Y')
    d = str(today)
    if(validate_apt_no(apt_no)):
        if(unique_apt_no(apt_no)):
            if(unique_chat_id(chat_id)):
                last_token_id+=1
                DATA.append([last_token_id,apt_no,name,chat_id])
                #write_token(DATA[last_token_id-1])
                send_message("Your token number is {} for the date {}.\nPlease maintain social distancing and wear a mask while shopping. Enter DONE after billing.".format(last_token_id,d),chat_id)
            else:
                send_message("Token has already been issued for you.",chat_id)
        else:
            send_message("Token has already been issued for this flat.",chat_id)
    else:
        send_message("Valid commands are:\n 1.Apt# (To Request Token e.g. D702)\n 2.Done (After Billing)\n 3.List All\n 4.Status",chat_id)
    return last_token_id

def collect_token(chat_id,token_counter):
    if(unique_chat_id(chat_id)==False):
        token_no=str(get_index(chat_id))
        if(unique_token(token_no)):
            send_message("Thank you! Token number {} has been processed. Don't forget to wash your hands.".format(token_no),chat_id)
            # f=open("collected_tokens.txt",'a')
            # f.write(token_no+'\n')
            # f.close()
            token_counter+=1
            TOKENS_COL.append(token_no)
        else:
            send_message('Token already processed',chat_id)
    else:
        send_message("Token not issued to this resident.",chat_id)
    return token_counter

def unique_token(token):
    for tok in TOKENS_COL:
        if(tok==token):
            return False
    return True

def get_index(chat_id):
    for info in DATA:
        if(str(info[3])==str(chat_id)):
            return info[0]

def process_text(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            name = update["message"]["chat"]["first_name"]
            #+' '+update["message"]["chat"]["last_name"]
        except Exception as e:
            send_message(str(e),ADMIN_ID)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def clear_data():
    #if(path.exists("last_update_id.txt")):
    #    os.remove("last_update_id.txt")
    # if(path.exists("token_data.txt")):
    #     os.remove("token_data.txt")
    # if(path.exists("collected_tokens.txt")):
    #     os.remove('collected_tokens.txt')
    # if(path.exists('token_start_time.txt')):
    #     os.remove('token_start_time.txt')
    last_update_id=None
    token_counter=0
    last_token_id=0
    e_bot_start_time=None
    DATA.clear()
    TOKENS_COL.clear()
    return last_update_id, token_counter, last_token_id, e_bot_start_time

def set_start_time(text, last_update_id, token_counter, last_token_id, e_bot_start_time):
    today=datetime.datetime.fromtimestamp(calendar.timegm(time.gmtime())+19800).strftime('%d-%m-%Y')
    start_time_text = text[6:].strip()
    if ':' in start_time_text:
        start_hour=start_time_text.split(':')[0]
        start_minutes=start_time_text.split(':')[1]
    else:
        start_hour=start_time_text
        start_minutes="00"

    try:
        if(int(start_hour) >= 0 and int(start_hour) <=24 and int(start_minutes)>=0 and int(start_minutes)<=59):
            bot_start_time = str(today)+' '+ str(start_hour)+':'+ str(start_minutes) + ':00'
            e_bot_start_time = time.mktime(time.strptime(bot_start_time, '%d-%m-%Y %H:%M:%S'))
        else:
            e_bot_start_time=None
            send_message("Hour must be between 0 and 24, minutes must be between 0 and 59. Please issue command as 'ISSUE HH:MM' in 24 hour format", ADMIN_ID)
    except:
        send_message("Hour must be between 0 and 24, minutes must be between 0 and 59. Please issue command as 'ISSUE HH:MM' in 24 hour format", ADMIN_ID)
    if(e_bot_start_time!=None):
        send_message("Token Issue start time set as {}:{}:00 for the date {}".format(str(start_hour), str(start_minutes), str(today)),ADMIN_ID)
        send_message("Token Issue start time set as {}:{}:00 for the date {}. Use @CCTMS_bot to request for token.".format(str(start_hour), str(start_minutes), str(today)),RESIDENT_GROUP_ID)
        last_update_id, token_counter, last_token_id, e_bot_start_time1=clear_data()
        # h=open("token_start_time.txt",'w')
        # h.write(str(e_bot_start_time))
        # h.close()
    return last_update_id, token_counter, last_token_id, e_bot_start_time

def main():
    # last_update_id = reset_last_update_id()
    # token_counter=get_collected_tokens()
    # last_token_id=get_last_token()
    #e_bot_start_time=get_e_bot_start_time()

    send_message("Server started",ADMIN_ID)

    flag=True
    last_update_id, token_counter, last_token_id, e_bot_start_time=clear_data()

    while flag:
        today=datetime.datetime.fromtimestamp(calendar.timegm(time.gmtime())+19800).strftime('%d-%m-%Y')
        updates = get_updates(last_update_id)
        if "result" in updates:
            if len(updates["result"]) > 0:
                for update in updates["result"]:
                    try:
                        chat = update["message"]["chat"]["id"]
                        epoch= update["message"]["date"]
                        try:
                            type = update["message"]["chat"]["type"]
                            text = update["message"]["text"]
                        except:
                            continue
                        # Process only if the message has text and epoch is greater than or equal to start time
                        if(e_bot_start_time==None) and ((text.strip().upper().startswith('ISSUE') or text.strip().upper().startswith('/ISSUE')) and chat==ADMIN_ID):
                            if len(text.strip()) > 6:
                                last_update_id, token_counter, last_token_id, e_bot_start_time=set_start_time(text.strip(), last_update_id, token_counter, last_token_id, e_bot_start_time)
                            else:
                                send_message("Please issue command as 'ISSUE HH:MM' in 24 hour format", ADMIN_ID)
                        elif ((e_bot_start_time!=None and (epoch+19800)>=e_bot_start_time) or chat==ADMIN_ID):
                            if(type=="private"):
                                name = update["message"]["chat"]["first_name"]
                            if(text.strip().upper()=='DONE'):
                                token_counter_new=collect_token(chat,token_counter)
                                if token_counter < token_counter_new:
                                   token_counter=token_counter_new
                                   if(token_counter==last_token_id):
                                       send_message("All tokens processed",ADMIN_ID)
                                   elif((token_counter%5==0) and (token_counter!=0) and (token_counter+5<last_token_id)):
                                       inform_admin(token_counter)
                            elif(text=="/start"):
                                send_message("Welcome to Token Management System\nValid commands are:\n 1.Apt# (To Request Token e.g. D702)\n 2.Done (After Billing)\n 3.List All\n 4.Status",chat)
                            elif((text.strip().upper().startswith('ISSUE') or text.strip().upper().startswith('/ISSUE')) and chat==ADMIN_ID):
                                send_message("Token issue time already set as {} for the date {}. To change time, type '/clear' command and then type '/issue '".format(str(datetime.datetime.fromtimestamp(e_bot_start_time).strftime('%H:%M:%S')),str(today)),ADMIN_ID)
                            elif(text.strip().upper()=='STATUS' or text.strip().upper()=='/STATUS'):
                                current_status(chat,token_counter,last_token_id)
                            elif(text.strip().upper()=='LIST ALL' or text.strip().upper()=='/LIST ALL'):
                                list_all(chat)
                            elif((text.strip().upper()=='/CLEAR' or text.strip().upper()=='CLEAR') and chat==ADMIN_ID):
                                send_message("Data cleared. Server Restarted",ADMIN_ID)
                                last_update_id, token_counter, last_token_id, e_bot_start_time=clear_data()
                                break
                            elif(type=="private"):
                                last_token_id=issue_token(text.strip().upper(),chat,name,last_token_id)
                            else:
                                if(type!="supergroup"):
                                    send_message("Invalid Command",chat)
                        else:
                            if(type=="private"):
                                if (e_bot_start_time!=None):
                                    send_message("Your request time is: {}\nPlease request for token after {}".format(datetime.datetime.fromtimestamp(epoch+19800).strftime('%H:%M:%S'),datetime.datetime.fromtimestamp(e_bot_start_time).strftime('%H:%M:%S')),chat)
                                else:
                                    send_message("Please wait for admin to set Token issue time",chat)
                    except Exception as e:
                        # f=open("Exception.txt",'a')
                        # f.write(str(e)+'\n')
                        # f.close()
                        send_message(str(e),ADMIN_ID)
                        # flag=False
                        # break

                #if (flag):
                last_update_id = get_last_update_id(updates)+1
                #else:
                #    last_update_id = update["update_id"]+1
                # h=open("last_update_id.txt",'w')
                # h.write(str(last_update_id))
                # h.close()
        else:
            time.sleep(90)

        e_today=calendar.timegm(time.gmtime())
        e_bot_stop_time=time.mktime(time.strptime(str(today)+" 21:00:00", '%d-%m-%Y %H:%M:%S'))

        if(e_today+19800>=e_bot_stop_time):
            time.sleep(36000)
            updates=get_updates(last_update_id)
            last_update_id, token_counter, last_token_id, e_bot_start_time=clear_data()
            last_update_id=get_last_update_id(updates)
            # send_message("Bot in Sleep Mode."+" "+str(e_today+19800)+" "+str(e_bot_stop_time) + " "+ str(calendar.timegm(time.gmtime())),ADMIN_ID)
            # time.sleep(300)
            # send_message(str(calendar.timegm(time.gmtime())), ADMIN_ID)
        else:
            time.sleep(1)

if __name__ == '__main__':
    main()
