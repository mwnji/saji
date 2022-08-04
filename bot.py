import asyncio
import base64
import concurrent.futures
import datetime
import glob
import json
import math
import os
import pathlib
import random
import sys
import time
from json import dumps, loads
from random import randint
import re
from re import findall
from rubika_lib import _date_time
import requests
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from requests import post
from googletrans import Translator
import io
from PIL import Image , ImageFont, ImageDraw 
import arabic_reshaper
from bidi.algorithm import get_display
from mutagen.mp3 import MP3
from gtts import gTTS
from threading import Thread
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from difflib import SequenceMatcher

from api_rubika import Bot,encryption

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def hasInsult(msg):
	swData = [False,None]
	for i in open("dontReadMe.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData

def hasAds(msg):
	links = list(map(lambda ID: ID.strip()[1:],findall("@[\w|_|\d]+", msg))) + list(map(lambda link:link.split("/")[-1],findall("rubika\.ir/\w+",msg)))
	joincORjoing = "joing" in msg or "joinc" in msg

	if joincORjoing: return joincORjoing
	else:
		for link in links:
			try:
				Type = bot.getInfoByUsername(link)["data"]["chat"]["abs_object"]["type"]
				if Type == "Channel":
					return True
			except KeyError: return False

def search_i(text,chat,bot):
    try:
        search = text[11:-1]
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], 'علالت باشه دادا پیویت فرستادم', chat['last_message']['message_id'])                           
            jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
            jd = jd['results']
            a = 0
            for j in jd:
                if a <= 8:
                    try:
                        res = requests.get(j['image_link'])
                        if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '':
                            thumb = str(j['cdn_thumbnail'])
                            thumb = thumb.split('data:image/')[1]
                            thumb = thumb.split(';')[0]
                            if thumb == 'png':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                            elif thumb == 'webp':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                            else:
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                        a += 1
                    except:
                        print('image error')
                else:
                    break                                    
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], 'در حال یافت صبر کونید...', chat['last_message']['message_id'])
            print('search image')
            jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
            jd = jd['results']
            a = 0
            for j in jd:
                if a < 10:
                    try:                        
                        res = requests.get(j['image_link'])
                        if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '' and j['cdn_thumbnail'].startswith('data:image'):
                            thumb = str(j['cdn_thumbnail'])
                            thumb = thumb.split('data:image/')[1]
                            thumb = thumb.split(';')[0]
                            if thumb == 'png':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                            elif thumb == 'webp':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                            else:
                                b2 = res.content
                                tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                width, height = bot.getImageSize(b2)
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                        a += 1  
                    except:
                        print('image erorr')
        return True
    except:
        print('image search err')
        return False

def write_image(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                paramiters = text[8:-1]
                paramiters = paramiters.split(':')
                if len(paramiters) == 5:
                    b2 = bot.write_text_image(txt_xt,paramiters[0],int(paramiters[1]),str(paramiters[2]),int(paramiters[3]),int(paramiters[4]))
                    tx = bot.requestFile('code_image.png', len(b2), 'png')
                    access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                    width, height = bot.getImageSize(b2)
                    bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                    print('sended file') 
                    return True
        return False	              
    except:
        print('server ban bug')
        return False

def uesr_remove(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if chat['last_message']['author_object_guid'] in admins:
            c_id = chat['last_message']['message_id']
            msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
            msg_data = msg_data[0]
            if 'reply_to_message_id' in msg_data.keys():
                msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                if not msg_data['author_object_guid'] in admins:
                    bot.banGroupMember(chat['object_guid'], msg_data['author_object_guid'])
                    bot.sendMessage(chat['object_guid'], 'کاربر سیکتیر شد @monji024 🎃' , chat['last_message']['message_id'])
                    return True
        return False
    except:
        print('server ban bug')
        return False

def speak_after(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                speech = gTTS(txt_xt)
                changed_voice = io.BytesIO()
                speech.write_to_fp(changed_voice)
                b2 = changed_voice.getvalue()
                tx = bot.requestFile('sound.ogg', len(b2), 'sound.ogg')
                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                f = io.BytesIO()
                f.write(b2)
                f.seek(0)
                audio = MP3(f)
                dur = audio.info.length
                bot.sendVoice(chat['object_guid'],tx['id'] , 'ogg', tx['dc_id'] , access, 'sound.ogg', len(b2), dur * 1000 ,message_id= c_id)
                print('sended voice')
                return True
        return False
    except:
        print('server gtts bug')
        return False

def get_gok(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
        return True
    except:
        print('code bz server err')
        
        
        return False

def info_qroz(text,chat,bot):
    try:
        user_info = bot.getInfoByUsername(text[7:])	
        if user_info['data']['exist'] == True:
            if user_info['data']['type'] == 'User':
                bot.sendMessage(chat['object_guid'], 'name:\n  ' + user_info['data']['user']['first_name'] + ' ' + user_info['data']['user']['last_name'] + '\n\nbio:\n   ' + user_info['data']['user']['bio'] + '\n\nguid:\n  ' + user_info['data']['user']['user_guid'] , chat['last_message']['message_id'])
                print('sended response')
            else:
                bot.sendMessage(chat['object_guid'], 'ننتو کاناله' , chat['last_message']['message_id'])
                print('sended response')
        else:
            bot.sendMessage(chat['object_guid'], 'وجود نداره' , chat['last_message']['message_id'])
            print('sended response')
        return True
    except:
        print('server bug6')
        return False

def search(text,chat,bot):
    try:
        search = text[9:-1]    
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + '\n\n'
            bot.sendMessage(chat['object_guid'], 'پیوی چک کون', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User':
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + '\n\n'
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
        return True
    except:
        print('search zarebin err')
        bot.sendMessage(chat['object_guid'], 'در حال حاضر این دستور محدود یا در حال تعمیر است' , chat['last_message']['message_id'])
        return False

def p_danesh(text,chat,bot):
    try:
        res = requests.get('http://api.codebazan.ir/danestani/pic/')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended file')                       
        return True
    except:
        print('code bz danesh api bug')
        return False

def anti_insult(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if not chat['last_message']['author_object_guid'] in admins:
            print('yek ahmagh fohsh dad: ' + chat['last_message']['author_object_guid'])
            bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
            return True
        return False
    except:
        print('delete the fohsh err')

def anti_tabligh(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if not chat['last_message']['author_object_guid'] in admins:
            print('yek ahmagh tabligh kard: ' + chat['last_message']['author_object_guid'])
            bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
            return True
        return False
    except:
        print('tabligh delete err')

def get_curruncy(text,chat,bot):
    try:
        t = json.loads(requests.get('https://api.codebazan.ir/arz/?type=arz').text)
        text = ''
        for i in t:
            price = i['price'].replace(',','')[:-1] + ' تومان'
            text += i['name'] + ' : ' + price + '\n'
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('code bz arz err')
    return True

def shot_image(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                res = requests.get('https://api.otherapi.tk/carbon?type=create&code=' + txt_xt + '&theme=vscode')
                if res.status_code == 200 and res.content != b'':
                    b2 = res.content
                    tx = bot.requestFile('code_image.png', len(b2), 'png')
                    access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                    width, height = bot.getImageSize(b2)
                    bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                    print('sended file')    
    except:
        print('code bz shot err')
    return True

def get_ip(text,chat,bot):
    try:
        ip = text[5:-1]
        if hasInsult(ip)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/ipinfo/?ip=' + ip).text)
            text = 'نام شرکت:\n' + jd['company'] + '\n\nکشور : \n' + jd['country_name'] + '\n\nارائه دهنده : ' + jd['isp']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz ip err')  
    return True

def get_weather(text,chat,bot):
    try:
        city = text[10:-1]
        if hasInsult(city)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/weather/?city=' + city).text)
            text = 'دما : \n'+jd['result']['دما'] + '\n سرعت باد:\n' + jd['result']['سرعت باد'] + '\n وضعیت هوا: \n' + jd['result']['وضعیت هوا'] + '\n\n بروز رسانی اطلاعات امروز: ' + jd['result']['به روز رسانی'] + '\n\nپیش بینی هوا فردا: \n  دما: ' + jd['فردا']['دما'] + '\n  وضعیت هوا : ' + jd['فردا']['وضعیت هوا']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz weather err')
    return True

def get_whois(text,chat,bot):
    try:
        site = text[8:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/whois/index.php?type=json&domain=' + site).text)
        text = '🐘مالک : \n'+jd['owner'] + '\n\n 🐺آیپی:\n' + jd['ip'] + '\n\n🐴آدرس مالک : \n' + jd['address'] + '\n\ndns1 : \n' + jd['dns']['1'] + '\ndns2 : \n' + jd['dns']['2'] 
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz whois err')
    return True

def get_font(text,chat,bot):
    try:
        name_user = text[7:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/font/?text=' + name_user).text)
        jd = jd['result']
        text = ''
        for i in range(1,100):
            text += jd[str(i)] + '\n'
        if hasInsult(name_user)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], 'دادا پیویت ارسال کردم', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + name_user + ') : \n\n'+text)                                        
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz font err')
    return True

def get_ping(text,chat,bot):
    try:
        site = text[7:-1]
        jd = requests.get('https://api.codebazan.ir/ping/?url=' + site).text
        text = str(jd)
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz ping err')
    return True

def get_gold(text,chat,bot):
    try:
        r = json.loads(requests.get('https://www.wirexteam.ga/gold').text)
        change = str(r['data']['last_update'])
        r = r['gold']
        text = ''
        for o in r:
            text += o['name'] + ' : ' + o['nerkh_feli'] + '\n'
        text += '\n\nآخرین تغییر : ' + change
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('gold server err')
    return True

def get_wiki(text,chat,bot):
    try:
        t = text[7:-1]
        t = t.split(':')
        mozoa = ''
        t2 = ''
        page = int(t[0])
        for i in range(1,len(t)):
            t2 += t[i]
        mozoa = t2
        if hasInsult(mozoa)[0] == False and chat['abs_object']['type'] == 'Group' and page > 0:
            text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
            if not 'codebazan.ir' in text_t:
                CLEANR = re.compile('<.*?>') 
                def cleanhtml(raw_html):
                    cleantext = re.sub(CLEANR, '', raw_html)
                    return cleantext
                text_t = cleanhtml(text_t)
                n = 4200
                text_t = text_t.strip()
                max_t = page * n
                min_t = max_t - n                                            
                text = text_t[min_t:max_t]
                bot.sendMessage(chat['object_guid'], 'مقاله "'+ mozoa + '" صفحه : ' + str(page) + '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
                bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + mozoa + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User' and page > 0:
            text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
            if not 'codebazan.ir' in text_t:
                CLEANR = re.compile('<.*?>') 
                def cleanhtml(raw_html):
                    cleantext = re.sub(CLEANR, '', raw_html)
                    return cleantext
                text_t = cleanhtml(text_t)
                n = 4200
                text_t = text_t.strip()
                max_t = page * n                                            
                min_t = max_t - n
                text = text_t[min_t:max_t]
                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('code bz wiki err')
    return True

def get_pa_na_pa(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/pa-na-pa/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz pa na pa err')
    return True

def get_dastan(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/dastan/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz dastan err')
    return True   

def get_search_k(text,chat,bot):
    try:
        search = text[11:-1]
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                                
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
            bot.sendMessage(chat['object_guid'], 'پیویت ارسال کردم دادا', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User':
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('zarebin search err')
    return True

def get_bio(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/bio/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz bio err')
    return True

def get_khabar(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/khabar/?kind=iran').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz khabar err')
    return True

def get_trans(text,chat,bot):
    try:
        t = text[8:-1]
        t = t.split(':')
        lang = t[0]
        t2 = ''
        for i in range(1,len(t)):
            t2 += t[i]
        text_trans = t2
        if hasInsult(text_trans)[0] == False:
            t = Translator()
            text = 'متن ترجمه شده به ('+lang + ') :\n\n' + t.translate(text_trans,lang).text
            jj = hasInsult(text)
            if jj[0] != True:
                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
        elif chat['abs_object']['type'] == 'User':
            t = Translator()
            text = 'متن ترجمه شده به ('+lang + ') :\n\n' + t.translate(text_trans,lang).text
            jj = hasInsult(text)
            if jj[0] != True:
                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('google trans err')
    return True

def get_khatere(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/khatere/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz khatere err')
    return True

def get_danesh(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/danestani/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz danesh err')
    return True

def get_sebt(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/monasebat/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz sebt err')
    return True

def get_alaki_masala(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/alaki-masalan/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz alaki masala err')
    return True

def get_hadis(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/hadis/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz hadis err')
    return True

def get_dialog(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/dialog/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz dialog err')
    return True

def get_zeikr(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/zekr/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz zekr err')
    return True

def name_shakh(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/name/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz name err')

def get_qzal(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/ghazalsaadi/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz qazal err')
    return True

def get_vaj(text,chat,bot):
    try:
        vaj = text[6:-1]
        if hasInsult(vaj)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/vajehyab/?text=' + vaj).text)
            jd = jd['result']
            text = 'معنی : \n'+jd['mani'] + '\n\n لغتنامه معین:\n' + jd['Fmoein'] + '\n\nلغتنامه دهخدا : \n' + jd['Fdehkhoda'] + '\n\nمترادف و متضاد : ' + jd['motaradefmotezad']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz vaj err')

def get_font_fa(text,chat,bot):
    try:
        site = text[10:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/font/?type=fa&text=' + site).text)
        jd = jd['Result']
        text = ''
        for i in range(1,10):
            text += jd[str(i)] + '\n'
        if hasInsult(site)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], 'ارسال کردم دادا', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + site + ') : \n\n'+text)                                        
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz font fa err')

def get_leaved(text,chat,bot):
    try:
        group = chat['abs_object']['title']
        date = _date_time.historyIran()
        time = _date_time.hourIran()
        send_text = 'karbar dar tarikh ' + date + ' az groh left dad @monji024 😶'   
        bot.sendMessage(chat['object_guid'],  send_text, chat['last_message']['message_id'])
    except:
        print('rub server err')

def get_added(text,chat,bot):    
    try:
        group = chat['abs_object']['title']
        date = _date_time.historyIran()
        time = _date_time.hourIran()
        send_text = 'iek karbar>>' + date + ' be ' + group + ' goroh joiin shod \n @monji024 😟'
        bot.sendMessage(chat['object_guid'],  send_text, chat['last_message']['message_id'])
    except:
        print('rub server err')

def get_help(text,chat,bot):                                
    text = open('help.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'پیویت ارسال کردم🗿', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('help guid sended')

def get_car(text,chat,bot):                                
    text = open('car.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'پیویت ارسال کردم', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('sar guid sended')
def get_srch(text,chat,bot):                                
    text = open('srch.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'پیویت ارسال کردم', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('srch guid sended')
    
def get_srch(text,chat,bot):                                
    text = open('srch.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'پیویت ارسال کردم', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('srch guid sended')
    
    #کاربردی
def gets_karborde(text,chat,bot):                                
    text = open('karborde.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'پیویت ارسال کردم', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('karborde guid sended')
    
    #کاربردی

def usvl_save_data(text,chat,bot):
    jj = False
    while jj == False:
        try:
            c_id = chat['last_message']['message_id']
            msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
            msg_data = msg_data[0]
            if 'reply_to_message_id' in msg_data.keys():
                msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                    txt_xt = msg_data['text']
                    f3 = len(open('farsi-dic.json','rb').read())
                    if f3 < 83886080:
                        f2 = json.loads(open('farsi-dic.json','r').read())
                        if not txt_xt in f2.keys():
                            f2[txt_xt] = [text]
                        else:
                            if not text in f2[txt_xt]:
                                f2[txt_xt].append(text)
                        c1 = open('farsi-dic.json','w')
                        c1.write(json.dumps(f2))
                        c1.close
                    else:
                        bot.sendMessage(chat['object_guid'], '!usvl_stop') 
                        b2 = open('farsi-dic.json','rb').read()
                        tx = bot.requestFile('farsi-dic.json', len(b2), 'json')
                        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                        bot.sendFile(chat['object_guid'] ,tx['id'] , 'json', tx['dc_id'] , access, 'farsi-dic.json', len(b2), message_id=c_id)
                    jj = True
                    return True
            jj = True
        except:
            print('server rubika err')

def usvl_test_data(text,chat,bot):
    t = False
    while t == False:
        try:
            f2 = json.loads(open('farsi-dic.json','r').read())
            shebahat = 0.0
            a = 0
            shabih_tarin = None
            shabih_tarin2 = None
            for text2 in f2.keys():
                sh2 = similar(text, text2)
                if sh2 > shebahat:
                    shebahat = sh2
                    shabih_tarin = a
                    shabih_tarin2 = text2
                a += 1
            print('shabih tarin: ' + str(shabih_tarin) , '|| darsad shebaht :' + str(shebahat))
            if shabih_tarin2 != None and shebahat > .45:
                bot.sendMessage(chat['object_guid'], str(random.choice(f2[shabih_tarin2])), chat['last_message']['message_id'])
            t = True
        except:
            print('server rubika err')

def get_backup(text,chat,bot):
    try:
        b2 = open('farsi-dic.json','rb').read()
        tx = bot.requestFile('farsi-dic.json', len(b2), 'json')
        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
        bot.sendFile(chat['object_guid'] ,tx['id'] , 'json', tx['dc_id'] , access, 'farsi-dic.json', len(b2), message_id=chat['last_message']['message_id'])
    except:
        print('back err')

def code_run(text,chat,bot,lang_id):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                h = {
                    "Origin":"https://sourcesara.com",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                }
                p = requests.post('https://sourcesara.com/tryit_codes/runner.php',{'LanguageChoiceWrapper':lang_id,'Program':txt_xt},headers=h)
                p = p.json()
                jj = hasInsult(p['Result'])
                jj2 = hasInsult(p['Errors'])
                time_run = p['Stats'].split(',')[0].split(':')[1].strip()
                if jj[0] != True and jj2[0] != True:
                    if p['Errors'] != None:
                        if len(p['Result']) < 4200:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nErrors:\n' + p['Errors'] + '\n\nResponse:\n'+ p['Result'], chat['last_message']['message_id'])
                        else:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nErrors:\n' + p['Errors'] + '\n\nResponse:\nپاسخ بیش از حد تصور بزرگ است' , chat['last_message']['message_id'])
                    else:
                        if len(p['Result']) < 4200:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nResponse:\n'+ p['Result'], chat['last_message']['message_id'])
                        else:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nResponse:\nپاسخ بیش از حد تصور بزرگ است', chat['last_message']['message_id'])
    except:
        print('server code runer err')

g_usvl = ''
test_usvl = ''
auth = "yfvnqnbtbhcatoccojbvunynpzsrcjpv"
#توکن
bot = Bot(auth)
list_message_seened = []
time_reset = random._floor(datetime.datetime.today().timestamp()) + 350
while(2 > 1):
    try:
        chats_list:list = bot.get_updates_all_chats()
        qrozAdmins = open('qrozAdmins.txt','r').read().split('\n')
        if chats_list != []:
            for chat in chats_list:
                access = chat['access']
                if chat['abs_object']['type'] == 'User' or chat['abs_object']['type'] == 'Group':
                    text:str = chat['last_message']['text']
                    if 'SendMessages' in access and chat['last_message']['type'] == 'Text' and text.strip() != '':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            print('new message')
                            if text == '!start' or text == '!Start' or text == 'start' or text == 'Start' or text == '!استارت' or text == 'استارت' or text == 'on' or text == '!on' or text == '!On' or text == '!ON' or text == 'روشن' or text == '/start' or text == '/Start':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'HI refigh be bot monji khosh omadi barad estefade az robat kalame [دستورات] ersal kon \n user spuort @monji024 👹',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
#شروع متون
                            if text == 'گروه' or text == 'لینک گروه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'تو چنل دادات جویین شو @monji024',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'شوخوش' or text == 'شوبخیر' or text == 'شب بخیر' or text == 'شب خوش' :
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'shab bekheir refigh🔹',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'آها' or text == 'اها' or text == 'عاها' :
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'Are😂',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '😕' or text == '😕😕':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'chete refigh🔹',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '🗿' or text == '🗿🗿' or text == '🗿🗿🗿' or text == '🗿🗿🗿🗿' or text == '🗿🗿🗿🗿🗿' or text == '🗿🗿🗿🗿🗿🗿':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'nistin be kiram methl kaka sangi😂😐',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'رلپی' or text == 'رل پی' or text == 'رل میخام' or text == 'برلیم؟' or text == 'برلیم' or text == 'عاشقتم' or text == 'عشقم' or text == 'عشقمی' or text == 'دوست دارم':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'bast kun koskesh bitarbiat khastam🐴',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '😐😂' or text == '😂😐' or text == '😐🤣' or text == '🤣😐' or text == '😐😹' or text == '😹😐' or text == '😐😂🤣' or text == '🙂' or text == '🙃' or text == '😸':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'vaghti dadat monji nmikhande chera mikhandi🐎🐴',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'وایجر' or text == 'وای جر' or text == 'جر' or text == 'وایجر😂' or text == 'وایجر😐😂' or text == 'جر😐😂' or text == 'جر😂😐' or text == 'جرر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'age pesari kiram tot age dokhtari baz kiram tot🐺',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'ایجان' or text == 'ای جان' or text == 'عیجان' or text == 'عی جان':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'Gomoji🤭',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'هن' or text == 'ها؟' or text == 'چی میگی' or text == 'چیمیگی' or text == 'چ میگی' or text == 'چمیگی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'nemidonm dada🤨',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'مشخصات' or text == 'اطلاعات':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '@niroumand 🔹',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'آفرین' or text == 'افرین' or text == 'آفری' or text == 'افری' or text == 'ن خشم اومد' or text == 'خوشم میاد ازش' or text == 'ن خوشم اومد':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'nokrtam dada🤨',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'خب' :
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'naro ro mokham aghab monde🐺',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'نه' or text == 'ن' or text == 'No' or text == 'no' or text == 'نع' or text == 'نح':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], ' شومارو به خاطر نعرم لوطفا موزاحم نشوید باتشکور داداتون مونجی',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '‌' or text == '‌‌' or text == '‌‌‌':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'net nadari dada manm ndarm🐎',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '♥️' or text == '💜' or text == '❤️' or text == '❣️' or text == '💘':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'dam madaret garm ba in bachash🤨',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'اره' or text == 'آره' or text == 'آرع' or text == 'ارع'or text == 'آرح' or text == 'ارح' or text == 'رح' or text == 'رع':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عا دادا😆',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کی' or text == 'کی؟':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'فقط خودا🐺',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'ریدم' or text == 'ریدوم':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'منم واقعا مدفوع نکردم فقط بخاطر دلقک بازیاش ریدم🐎',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                            if text == 'سلام دادا' or text == 'سلام داش' or text == 'سلام داداش':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'صامولیک دادا🐎',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                            if text == 'جالب' or text == 'عالی' or text == 'گانگ' or text == 'گنگ' or text == 'جذاب':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عالی مینوازی 🐴',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کص میگی' or text == 'کصمیگی' or text == 'کسمیگی' or text == 'کس میگی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عل باو عله🐴',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')   
                            if text == 'رباتی؟' or text == 'رباتی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عا دادا انقدر سطح نباش🐺',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'خوبه' or text == 'عالیه':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عا دادا',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '😐🚶' or text == '😐🚶‍♀️' or text == '😐🚶🏿‍♀' or text == '😐🚶🏿‍♂':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'صامولیک دادا بنده افلاین بودم موشکلی پیش اومده🤨',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '؟' or text == '؟؟' or text == '?' or text == '??' or text == '?!' or text == '؟!':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ها چیه🦄',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '!' or text == '!!' or text == '!!!':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سلام رفیق صدا منو داری🐎',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'عجب' or text == 'اجب' or text == 'عجب😐😂' or text == 'عجب😂😐' or text == 'عجب😐' or text == 'عجب😂':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'درست میگویی دادا واقعا کم اوردم🐴',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'رباته؟😐' or text == 'رباته؟' or text == 'رباته؟😐😂' or text == 'رباته😂😐':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'دادا برا اخرین بار میگم موسطح نباش🐎',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'حوسین' or text == 'حسین':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'دادات دونیا دونیا دادات ',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'چنل' or text == 'پشتیبانی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '🔹- user support @monji024',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'منجی' or text == 'منجی بات' or text == 'بات منجی' or text == 'منجی ربات' or text == 'منجی جون' or text == 'منجی😐😂' or text == 'منجی😐' or text == 'منجی😂' or text == 'منجی😂😐' or text == 'shiba' or text == 'shiba bot' or text == 'منجی جون':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مادرتو سرچولی میزنم مانند مادر سجاد صونی🐎🐴',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کسمادرت' or text == 'کس مادرت' or text == 'کصمادرت' or text == 'کص مادرت' or text == 'مادر جنده':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'فحاشی نکن بچه سال👺',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'جون' or text == 'جان':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عل باو😃',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'قوانین گپ' or text == 'قوانین' or text.startswith('[قوانین]'):
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '🔹شوما تاموشی نده بقیش گردن ما دادا🐺',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'خرید' or text == 'ربات میخام' or text == 'بات میخام' or text == 'خرید ربات' or text == 'خرید بات':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عل باو بورو از دادات مونجی درخواست کون🐴🐎',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'امیر' or text == 'منجی' or text == 'سازنده' or text == 'سازندت کیه' or text == 'سازندت کیه؟':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مونجی شوده قوموجی',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'س' or text == 'ص' or text == 'صلام'  or text == 'سلام' or text == 'سلم' or text == 'صلم' or text == 'سل' or text == 'صل':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سلاپ دادا',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'خبی؟' or text == 'خبی' or text == 'خوبی؟' or text == 'خوبی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'زنگی کیریست ولی میگذرد',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '.' or text == '..':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'شومارتو پیوی ارسال کون برات نت بزنم🐎🐴',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'شکر' or text == 'شک':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عا دا🦄',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '😞' or text == '🙁' or text == '😔' or text == '☹' or text == '️😣' or text == '😖' or text == '😫' or text == '😩' or text == '😭' or text == '🤕' or text == '💔' or text == '😓' or text == '😟' or text == '😰' or text == '🤒' or text == '😥' or text == '😢':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'دادا چرا میخای قوپی بیای 🐎',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'نمال' or text == 'بمال' or text == 'کصکش' or text == 'کسکش':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'با کیر پیدرت بازی نکون دادا',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کسنگو' or text == 'کس نگو' or text == 'کصنگو' or text == 'کص نگو':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مامانت باو',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '😐😐😐😐' or text == '😐😐😐' or text == '😐😐' or text == '😐':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'شوک شودی ابجیت زیدمه ها',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'بای' or text == 'بحی' or text == 'خداحافظ' or text == 'فعلن' or text == 'فعلا' or text == 'فعلاً':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خداحافظ رفیق',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'اخی' or text == 'آخی' or text == 'اوخی' or text == 'اوخ':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'با دادات دروست چت کون عل😆',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '😂' or text == '😂😂' or text == '😂😂😂' or text == '😂😂😂😂' or text == '😂😂😂😂😂':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'صامولیک دادا تایپرح لحشیح ترو خودا منو نترسون🤨',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '🤣' or text == '🤣🤣' or text == '🤣🤣🤣' or text == '🤣🤣🤣🤣' or text == '🤣🤣🤣🤣🤣':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'زندگی که کردنی بود اینگونه گوذشت جان که دادنی هست چه شود🐎🐴',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'ربات' or text == 'بات' or text == 'روبات' or text == 'رب' or text == 'ربا'  or text == '!bot':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ها دادا🐴',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'چخبر' or text == 'چخبرا':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خبری نیست دادا',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'هعب' or text == 'هعی' or text == 'هیب' or text == 'هعپ':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'هعیی تر',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
#اتمام متون
                            if text == '/zaman' or text == '!zaman' or text == 'زمان' :
                                print('message geted and sinned')
                                try:
                                    date = _date_time.historyIran()
                                    time = _date_time.hourIran()

                                    bot.sendMessage(chat['object_guid'], 'تاریخ: \n' + date + '\nساعت:\n'+ time,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '/date' or text == 'تاریخ' or text == '!date' :
                                print('message geted and sinned')
                                try:
                                    date = _date_time.historyIran()

                                    bot.sendMessage(chat['object_guid'], 'تاریخ \n' + date ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '/time' or text == '!time' or text == 'ساعت' or text == 'تایم' :
                                print('message geted and sinned')
                                try:
                                    time = _date_time.hourIran()

                                    bot.sendMessage(chat['object_guid'], 'ساعت  \n' + time ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'منم خبم' or text == 'منم خوبم' or text == 'منم خبمح' or text == 'خوبم' or text == 'خبم' or text == 'خبمح':
                                print('message geted and sinned')
                                try:

                                    bot.sendMessage(chat['object_guid'], 'اوکب',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'تست' or text == 'test' or text == '!test' or text == '/test' or text == '/Test' or text == '!Test':
                                print('message geted and sinned')
                                try:

                                    bot.sendMessage(chat['object_guid'], '@niroumand on',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            elif text.startswith('!nim http://') == True or text.startswith('!nim https://') == True:
                                try:
                                    bot.sendMessage(chat['object_guid'], "darhal amade sazi ....",chat['last_message']['message_id'])
                                    print('sended response')
                                    link = text[4:]
                                    nim_baha_link=requests.post("https://www.digitalbam.ir/DirectLinkDownloader/Download",params={'downloadUri':link})
                                    pg:str = nim_baha_link.text
                                    pg = pg.split('{"fileUrl":"')
                                    pg = pg[1]
                                    pg = pg.split('","message":""}')
                                    pg = pg[0]
                                    nim_baha = pg    
                                    try:
                                        bot.sendMessage(chat['object_guid'], 'لینک نیم بها شما با موفقیت آماده شد ✅ \n لینک : \n' + nim_baha ,chat['last_message']['message_id'])
                                        print('sended response')    
                                    except:
                                        print('server bug2')
                                except:
                                    print('server bug3')
                            elif text.startswith('!monji @'):
                                tawd10 = Thread(target=info_qroz, args=(text, chat, bot,))
                                tawd10.start()
                            elif text.startswith('!srch ['):
                                tawd11 = Thread(target=search, args=(text, chat, bot,))
                                tawd11.start()
                            elif text.startswith('!wiki-s ['):
                                try:
                                    search = text[9:-1]    
                                    search = search + 'ویکی پدیا'
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '!wiki [1:' + title + ']\n\n' 
                                        bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
                                        bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '!wiki [1:' + title + ']\n\n'
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('wiki s err')              
                            elif text.startswith('!zekr') or text.startswith('ذکر'):
                                tawd219 = Thread(target=get_zeikr, args=(text, chat, bot,))
                                tawd219.start()
                            elif text.startswith('حدیث') or text.startswith('!hadis'):
                                tawd275 = Thread(target=get_hadis, args=(text, chat, bot,))
                                tawd275.start()
                            elif text.startswith('!name_shakh')  or text.startswith('نام شاخ'):
                                tawd32 = Thread(target=name_shakh, args=(text, chat, bot,))
                                tawd32.start()
                                
                            elif text.startswith('!jok') or text.startswith('جوک'):
                                tawd21 = Thread(target=get_gok, args=(text, chat, bot,))
                                tawd21.start()
                                
                            elif text.startswith('!khatere')  or text.startswith('خاطره'):
                                tawd29 = Thread(target=get_khatere, args=(text, chat, bot,))
                                tawd29.start()
                            elif text.startswith('!danesh')  or text.startswith('دانش'):
                                tawd30 = Thread(target=get_danesh, args=(text, chat, bot,))
                                tawd30.start()
                            elif text.startswith('!pa_na_pa')  or text.startswith('پ ن پ'):
                                tawd24 = Thread(target=get_pa_na_pa, args=(text, chat, bot,))
                                tawd24.start()
                            elif text.startswith('دیالوگ') or text.startswith('!dialog'):
                                tawd215 = Thread(target=get_dialog, args=(text, chat, bot,))
                                tawd215.start()
                            elif text.startswith('!alaki_masala')  or text.startswith('الکلی مثلا'):
                                tawd31 = Thread(target=get_alaki_masala, args=(text, chat, bot,))
                                tawd31.start()
                            elif text.startswith('!dastan')  or text.startswith('داستان'):
                                tawd25 = Thread(target=get_dastan, args=(text, chat, bot,))
                                tawd25.start()
                            elif text.startswith('!bio')  or text.startswith('بیو'):
                                tawd27 = Thread(target=get_bio, args=(text, chat, bot,))
                                tawd27.start()
                            elif text.startswith('/mont') or text.startswith('!mont') or text.startswith('مناسبت'):
                                tawd27 = Thread(target=get_sebt, args=(text, chat, bot,))
                                tawd27.start()
                            elif text.startswith('!srch-k ['):
                                tawd26 = Thread(target=get_search_k, args=(text, chat, bot,))
                                tawd26.start()
                            elif text.startswith('!ban [') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                try:
                                    user = text[6:-1].replace('@', '')
                                    guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
                                    admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
                                    if not guid in admins and chat['last_message']['author_object_guid'] in admins:
                                        bot.banGroupMember(chat['object_guid'], guid)
                                        bot.sendMessage(chat['object_guid'], 'کاربر به همراه ایدی سیکتیر شد @niroumand 👺' , chat['last_message']['message_id'])
                                except:
                                    print('ban bug')
                            elif text.startswith('!srch-p ['):
                                print('mpa started')
                                tawd = Thread(target=search_i, args=(text, chat, bot,))
                                tawd.start()
                            elif text.startswith('بن') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                print('mpa started')
                                tawd2 = Thread(target=uesr_remove, args=(text, chat, bot,))
                                tawd2.start()
                            elif text.startswith('!trans ['):
                                tawd28 = Thread(target=get_trans, args=(text, chat, bot,))
                                tawd28.start()
                            elif text.startswith('!myket ['):
                                try:
                                    search = text[10:-1]
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
                                        bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])                           
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)                               
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('myket server err')
                            elif text.startswith('!viki ['):
                                tawd23 = Thread(target=get_wiki, args=(text, chat, bot,))
                                tawd23.start()
                            elif text.startswith('/arz'):
                                print('mpa started')
                                tawd15 = Thread(target=get_curruncy, args=(text, chat, bot,))
                                tawd15.start()
                            elif text.startswith('/gold'):
                                tawd22 = Thread(target=get_gold, args=(text, chat, bot,))
                                tawd22.start()
                            elif text.startswith('!ping ['):
                                tawd21 = Thread(target=get_ping, args=(text, chat, bot,))
                                tawd21.start()
                            elif text.startswith('!font-en ['):
                                tawd20 = Thread(target=get_font, args=(text, chat, bot,))
                                tawd20.start()
                            elif text.startswith('!font-fa ['):
                                tawd34 = Thread(target=get_font_fa, args=(text, chat, bot,))
                                tawd34.start()
                            elif text.startswith('!whois ['):
                                tawd19 = Thread(target=get_whois, args=(text, chat, bot,))
                                tawd19.start()
                            elif text.startswith('!vaj ['):
                                tawd33 = Thread(target=get_vaj, args=(text, chat, bot,))
                                tawd33.start()
                            elif text.startswith('!hvs ['):
                                tawd18 = Thread(target=get_weather, args=(text, chat, bot,))
                                tawd18.start()
                            elif text.startswith('!ip ['):
                                tawd17 = Thread(target=get_ip, args=(text, chat, bot,))
                                tawd17.start()
                            elif text.startswith("!add [") and chat['abs_object']['type'] == 'Group' and 'AddMember' in access:
                                try:
                                    user = text[6:-1]
                                    bot.invite(chat['object_guid'], [bot.getInfoByUsername(user.replace('@', ''))["data"]["chat"]["object_guid"]])
                                    bot.sendMessage(chat['object_guid'], 'رفیقمون اضافه شود @monji024 👺' , chat['last_message']['message_id'])                         
                                except:
                                    print('add not successd')  
                            elif text.startswith('!math ['):
                                try:
                                    amal_and_value = text[7:-1]
                                    natije = ''
                                    if amal_and_value.count('*') == 1:
                                        value1 = float(amal_and_value.split('*')[0].strip())
                                        value2 = float(amal_and_value.split('*')[1].strip())
                                        natije = value1 * value2
                                    elif amal_and_value.count('/') > 0:
                                        value1 = float(amal_and_value.split('/')[0].strip())
                                        value2 = float(amal_and_value.split('/')[1].strip())
                                        natije = value1 / value2
                                    elif amal_and_value.count('+') > 0:
                                        value1 = float(amal_and_value.split('+')[0].strip())
                                        value2 = float(amal_and_value.split('+')[1].strip())
                                        natije = value1 + value2
                                    elif amal_and_value.count('-') > 0:
                                        value1 = float(amal_and_value.split('-')[0].strip())
                                        value2 = float(amal_and_value.split('-')[1].strip())
                                        natije = value1 - value2
                                    elif amal_and_value.count('**') > 0:
                                        value1 = float(amal_and_value.split('**')[0].strip())
                                        value2 = float(amal_and_value.split('**')[1].strip())
                                        natije = value1 ** value2
                                    
                                    if natije != '':
                                        bot.sendMessage(chat['object_guid'], natije , chat['last_message']['message_id'])
                                except:
                                    print('math err')  
                                    #شات
                            elif text.startswith('!shot') or text.startswith('شات'):
                                tawd516 = Thread(target=shot_image, args=(text, chat, bot,))
                                tawd516.start()
                                #شات
                            elif text.startswith('!bgo') or text.startswith('بگو'):
                                print('mpa started')
                                tawd6 = Thread(target=speak_after, args=(text, chat, bot,))
                                tawd6.start()
                            elif text.startswith('/danpic') or text.startswith('عکس دانستنی'):
                                tawd12 = Thread(target=p_danesh, args=(text, chat, bot,))
                                tawd12.start()
                            elif text.startswith('!write ['):
                                print('mpa started')
                                tawd5 = Thread(target=write_image, args=(text, chat, bot,))
                                tawd5.start()
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasInsult(text)[0] == True:
                                tawd13 = Thread(target=anti_insult, args=(text, chat, bot,))
                                tawd13.start()
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasAds(text) == True:
                                tawd14 = Thread(target=anti_tabligh, args=(text, chat, bot,))
                                tawd14.start()
                            elif text.startswith('/help') or text.startswith('!help') or text.startswith('دستورات') or text.startswith('پنل'):
                                tawd112 = Thread(target=get_help, args=(text, chat, bot,))
                                tawd112.start()
                            elif text.startswith('سرگرمی ها') or text.startswith('!sar') or text.startswith('لیست سرگرمی') or text.startswith('سرگرمی') or text.startswith('[سرگرمی]') or text.startswith('[سرگرمی ها]'):
                                tawd3668 = Thread(target=get_car, args=(text, chat, bot,))
                                tawd3668.start()                            
                            elif text.startswith('جستجو') or text.startswith('موتور جستجو') or text.startswith('[موتور جستجو]'):
                                tawd358 = Thread(target=get_srch, args=(text, chat, bot,))
                                tawd358.start()
 #کاربردی
                            elif text.startswith('کاربردی') or text.startswith('ابزار کاربردی') or text.startswith('[ابزار کاربردی]'):
                                tawd238 = Thread(target=gets_karborde, args=(text, chat, bot,))
                                tawd238.start()
#کاربردی                         
                            elif text.startswith('66') or text.startswith('666'):
                                tawd348 = Thread(target=get_sar, args=(text, chat, bot,))
                            elif text.startswith('شروع') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in qrozAdmins and g_usvl == '':
                                g_usvl = chat['object_guid']
                                bot.sendMessage(chat['object_guid'], 'یادگیری فعال شد', chat['last_message']['message_id'])
                            elif text.startswith('پایان') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in qrozAdmins and g_usvl != '':
                                g_usvl = ''
                                bot.sendMessage(chat['object_guid'], 'یادگیری غیرفعال شد.', chat['last_message']['message_id'])  
                            elif text.startswith('فعال') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in qrozAdmins and g_usvl == '' and test_usvl == '':
                                test_usvl = chat['object_guid']
                                bot.sendMessage(chat['object_guid'], 'پاسخگویی فعال شد.', chat['last_message']['message_id'])
                            elif text.startswith('غیرفعال') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in qrozAdmins and test_usvl == chat['object_guid']:
                                test_usvl = ''
                                bot.sendMessage(chat['object_guid'], 'پاسخگویی غیرفعال شد.', chat['last_message']['message_id'])   
                            elif text.startswith('!backup') and chat['object_guid'] in qrozAdmins:
                                tawd44 = Thread(target=get_backup, args=(text, chat, bot,))
                                tawd44.start()
                            elif chat['object_guid'] == g_usvl and chat['last_message']['author_object_guid'] != 'u0DcA7S0def8612b339488bb4fe40f50' and chat['abs_object']['type'] == 'Group':
                                tawd42 = Thread(target=usvl_save_data, args=(text, chat, bot,))
                                tawd42.start()
                            elif test_usvl == chat['object_guid'] and chat['last_message']['author_object_guid'] != 'u0DcA7S0def8612b339488bb4fe40f50' and chat['abs_object']['type'] == 'Group':
                                print('usvl tested')
                                tawd43 = Thread(target=usvl_test_data, args=(text, chat, bot,))
                                tawd43.start()
                            list_message_seened.append(m_id)
                    elif 'SendMessages' in access and chat['last_message']['type'] == 'Other' and text.strip() != '' and chat['abs_object']['type'] == 'Group' and chat['abs_object']['type'] == 'Group':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if text == 'یک عضو گروه را ترک کرد.':
                                tawd35 = Thread(target=get_leaved, args=(text, chat, bot,))
                                tawd35.start()
                            elif text == '1 عضو جدید به گروه افزوده شد.' or text == 'یک عضو از طریق لینک به گروه افزوده شد.':
                                tawd36 = Thread(target=get_added, args=(text, chat, bot,))
                                tawd36.start()
                            list_message_seened.append(m_id)
                    elif 'SendMessages' in access and text.strip() != '' and chat['abs_object']['type'] == 'Group':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if 'DeleteGlobalAllMessages' in access and hasInsult(text)[0] == True:
                                tawd39 = Thread(target=anti_insult, args=(text, chat, bot,))
                                tawd39.start()
                                list_message_seened.append(m_id)
                            elif 'DeleteGlobalAllMessages' in access and hasAds(text) == True:
                                tawd40 = Thread(target=anti_tabligh, args=(text, chat, bot,))
                                tawd40.start()
                                list_message_seened.append(m_id)
        else:
            print('چت ها را آپدیت کنید ')
    except:
        print('ارور کلی')
    time_reset2 = random._floor(datetime.datetime.today().timestamp())
    if list_message_seened != [] and time_reset2 > time_reset:
        list_message_seened = []
        time_reset = random._floor(datetime.datetime.today().timestamp()) + 350