# -*- coding: UTF-8 -*-
import telebot
import urllib
import requests
import urllib.request
import ssl
import psycopg2
import os
from telebot import types
from Data.Data import *
import Search.youtube as youtube


DATABASE_URL = os.environ['DATABASE_URL']
# DATABASE_URL = "postgres://autltpnfsesakf:2eb9e796e60223c7c286f518f0215f16279c629b419eff77524b6d480d978022@ec2-54-227-245-146.compute-1.amazonaws.com:5432/df8cliiof9jbhi"
TOKEN = "743596317:AAFGbmXQOXakO_MpFWFkXzltzLB6__eRYOs"
PASSWORD = "admin"

schedule_message_id = None

bot = telebot.TeleBot(TOKEN)

lastNotUsed = 0
transChatId = {} # Transformed chatId into freeSpaceIndex
state = []
playlist_link = {}
stop = {}
musicMode = []
pos = []
ls = [[]]
ytls = {}
dataBase = DataBase(DATABASE_URL)
paramsTable = ParamsTable(dataBase)
uselessMessagesTable = UselessMessagesTable(dataBase)



def getLink(s,chat):
    global pos
    search = 'download'
    j = 0
    for pos[chat] in range(pos[chat],len(s)):
        if (search[j] == s[pos[chat]]):
            j = j + 1
        else :
            j = 0
        if (j==len(search)):
            p1 = pos[chat]
            p2 = pos[chat]
            while (s[p1]!='"'):
                p1 = p1 - 1
            while (s[p2]!='"'):
                p2 = p2 + 1
            p1 = p1 + 1
            p2 = p2 - 1
            print('Link found: '+ s[p1:p2])
            return s[p1:p2]
    print('No link')
    return '0'
def getDuration(s,chat):
    global pos
    search='playlist-duration'
    j = 0
    for pos[chat] in range(pos[chat],len(s)):
        if (search[j] == s[pos[chat]]):
            j = j + 1
        else :
            j = 0
        if (j==len(search)):
            p1 = pos[chat]+3
            while (s[pos[chat]]!='<'):
                pos[chat] = pos[chat] + 1
            p2 = pos[chat] - 1
            # print(s[p1:p2])
            return s[p1:p2]

    return '0'

def getArtist(s,chat):
    global pos
    search = 'playlist-name'
    j = 0
    for pos[chat] in range(pos[chat],len(s)):
        if (search[j] == s[pos[chat]]):
            j = j + 1
        else :
            j = 0
        if (j==len(search)):
            while s[pos[chat]]!='<':
                pos[chat] = pos[chat] + 1
            p1 = pos[chat] + 3
            p2 = p1
            while s[p2]!='<' :
                p2 = p2 + 1
            pos[chat] = p2
            #print('Artist found: ' + s[p1:p2])
            return s[p1:p2]
    return '0'


def getSongName(s,chat):
    global pos
    search = '<em>'
    j = 0
    for pos[chat] in range(pos[chat], len(s)):
        if (search[j] == s[pos[chat]]):
            j = j + 1
        else :
            j = 0
        if (j==len(search)):
            p1 = pos[chat] + 1
            p2 = p1
            while (s[p2]!='<'):
                p2 = p2 + 1
            pos[chat] = p2
            #print('Title found: '+ s[p1:p2])
            return s[p1:p2]
    return '0'
def getList(song,message):
    global pos
    global transChatId
    headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'  # This is another valid field
    }
    url = "http://music.xn--41a.ws/search/"+(song)+"/"
    url = url.lower()
    print(url)
    htmlContent = requests.get(url, headers=headers)
    print(htmlContent)
    s = htmlContent.content.decode("utf-8", "strict")
    result = []
    chat = transChatId[message.chat.id]
    pos[chat] = 0
    while (True):
        link = getLink(s,chat)
        if (link == '0'):
            break
        duration = getDuration(s,chat)
        artist = getArtist(s,chat)
        songName = getSongName(s,chat)
        a = [link,artist,songName,duration]
        result.append(a)
        if (len(result) > 10):
            break
    return result


def getFile(link,chat):
    file_name = 'music/file'+str(chat)+'.mp3'
    url = 'http://music.xn--41a.ws' + link
    print("Downloading: " + url);
    gcontext = ssl.SSLContext()  # Only for gangstars
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(url, file_name)
def init(message):
    global state,lastNotUsed,transChatId,ls,pos,message_ids
    if (transChatId.get(message.chat.id,-1) == -1):
        transChatId[message.chat.id]=lastNotUsed
        lastNotUsed = lastNotUsed + 1
    while (len(state)<=transChatId[message.chat.id]):
        state.append(0)
    while (len(ls) <= transChatId[message.chat.id]):
        ls.append([])
    while (len(pos) <= transChatId[message.chat.id]):
        pos.append(0)
    while (len(musicMode) <= transChatId[message.chat.id]):
        musicMode.append(0)

    uselessMessagesTable.addMessage(message)

    ### LOG ###
    print ('User:' + message.from_user.first_name + ' chat_id:' + str(message.chat.id) +
           ' chat:' + str(transChatId[message.chat.id]))
    if (message.text != None):
        print('Message: ' + message.text)

def log(message, answer):
    print('Reply to ' + message.from_user.first_name + ': ' + answer)

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    global stop,transChatId
    chat = transChatId[message.chat.id]
    init(message)
    stop[chat] = True
@bot.message_handler(commands=['help'])
def handle_help(message):
    global state,transChatId
    init(message)
    state[transChatId[message.chat.id]] = 0
    answer = "Поки я вмію шукати музику. Пишеш /music, щоб ввімкнути режим музики, потім назву пісні або автора. Отримуєш список з 11 пісень (або менше) і" \
             " вибераєш ту, яка тобі підходить. Потім чекаєш в середньому секунд 20 і отримуєш свій трек 😎😎😎. Після цього можеш знову написати /music і " \
             " вимкнути режим пошуку музики, або написати назву іншої пісні, якщо плануєш знайте ще одну."
    botmessage = bot.send_message(message.chat.id, answer)
    uselessMessagesTable.addMessage(botmessage)


    ### LOG ###
    log(message,answer)

@bot.message_handler(commands=['start'])
def handle_start(message):
    global state, transChatId
    init(message)
    state[transChatId[message.chat.id]] = 0
    answer = "Дороуля, тикай /help і всьо узнаєш"
    botmessage = bot.send_message(message.chat.id, answer)
    uselessMessagesTable.addMessage(botmessage)
    log(message, answer)

@bot.message_handler(commands=['admin'])
def handle_admin(message):
    global state, transChatId
    init(message)
    chat = transChatId[message.chat.id]
    if (state[chat] < 100):
        state[chat] = 101
        answer = "Уведи пароль"
        log(message, answer)
        botmessage = bot.send_message(message.chat.id, answer)
        uselessMessagesTable.addMessage(botmessage)

    else:
        if (state[chat] < 200):
            answer = "logged out"
            log(message, answer)
            botmessage = bot.send_message(message.chat.id, answer)
            uselessMessagesTable.addMessage(botmessage)
            state[chat] = 0

@bot.message_handler(commands=['setschedule'])
def handle_setschedule(message):
    global state, transChatId
    init(message)
    chat = transChatId[message.chat.id]
    if (state[chat] == 100):
        answer = "Скинь фотку розкладом"
        log(message, answer)
        botmessage = bot.send_message(message.chat.id, answer)
        uselessMessagesTable.addMessage(botmessage)
        state[chat] = 102

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global state, transChatId
    init(message)
    chat = transChatId[message.chat.id]
    if (state[chat] == 102):
        paramsTable.setSchedule(message);
        answer = "Сохранив розклад. (Кіть захочеш удалити, та удали лем для себе)"
        log(message, answer)
        uselessMessagesTable.removeMessage(message)
        botmessage = bot.send_message(message.chat.id, answer)
        uselessMessagesTable.addMessage(botmessage)
        state[chat] = 100

@bot.message_handler(commands=['clear'])
def handle_clear(message):
    init(message)
    messages = uselessMessagesTable.getMessages(message.chat.id)
    for message_id in messages:
        try:
            bot.delete_message(message.chat.id,message_id)
        except Exception as er:
            print("Unsuccessful attempt of deleting message")
            print(er)
    uselessMessagesTable.clearMessages(message.chat.id)

@bot.message_handler(commands=['schedule'])
def handle_schedule(message):
    global state, transChatId
    init(message)
    chat = transChatId[message.chat.id]
    schedule = paramsTable.getSchedule()
    try:
        answer = "Розклад:"
        botmessage = bot.send_message(message.chat.id, answer)
        uselessMessagesTable.addMessage(botmessage)
        botmessage = bot.forward_message(message.chat.id, schedule[0],schedule[1])
        uselessMessagesTable.addMessage(botmessage)
        log(message, answer)
    except Exception as er:
        print(er)
        answer = "Ниє у ня розклада"
        botmessage = bot.send_message(message.chat.id, answer)
        uselessMessagesTable.addMessage(botmessage)
        log(message,answer)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    global ls,transChatId,ytls
    message = call.message
    indx = int(call.data[1:])
    type = int(call.data[0])
    chat = transChatId[message.chat.id]
    answer = 'Ща всьо буде'
    botmessage = bot.send_message(message.chat.id, answer)
    uselessMessagesTable.addMessage(botmessage)
    log(message,answer)
    bot.send_chat_action(message.chat.id,'upload_audio')
    if (type == 1):
        getFile(ls[chat][indx][0],chat)
        performer = ls[chat][indx][1]
        title = ls[chat][indx][2]
    if (type == 2):
        youtube.download(ytls[chat][indx][0],chat = chat)
        performer,title = youtube.titleParse(ytls[chat][indx][1])
    answer = 'Скачавім, гружу тепер тобі'
    botmessage = bot.send_message(message.chat.id, answer)
    uselessMessagesTable.addMessage(botmessage)
    log(message,answer)
    # file = open('music/file'+str(chat)+'.mp3')
    bot.send_chat_action(message.chat.id,'upload_audio')
    bot.send_audio(message.chat.id,
    audio = open('music/file'+str(chat)+'.mp3', 'rb'),
    performer =  performer,
    title = title
    )
    state[chat] = 0
    answer = 'Пиши /clear , щоб удалити лишні повідомлення'
    botmessage = bot.send_message(message.chat.id,answer)
    uselessMessagesTable.addMessage(botmessage)
    print("Music sent: " + performer + " -- " + title)
@bot.message_handler(commands=['music'])
def handle_music(message):
    global state,transChatId
    init(message)
    chat_id = transChatId[message.chat.id]
    if (musicMode[chat_id] == 0):
        answer = "Включивім режим пошуку музики"
        log(message, answer)
        botmessage = bot.send_message(message.chat.id, answer)
        uselessMessagesTable.addMessage(botmessage)
        musicMode[chat_id] = 1
    else :
        answer = "Виключивім режим пошуку музики"
        log(message, answer)
        botmessage = bot.send_message(message.chat.id, answer)
        uselessMessagesTable.addMessage(botmessage)
        musicMode[chat_id] = 0

@bot.message_handler(commands=['similar'])
def handle_similar(message):
    global state,transChatId
    init(message)
    chat = transChatId[message.chat.id]
    if (state[chat] < 100):
        answer = "Введи назву пісні"
        botmessage = bot.send_message(message.chat.id, answer)
        uselessMessagesTable.addMessage(botmessage)
        state[chat] = 50

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global state
    global ls,transChatId,ytls
    init(message)
    chat = transChatId[message.chat.id]


    if (state[chat] == 51):
        val = 0
        try:
            val = int(message.text)
        except:
            answer = "Введи ціле число"
            botmessage = bot.send_message(message.chat.id,answer)
            uselessMessagesTable.addMessage(botmessage)
            return
        answer = "Загружаю плейлист"
        botmessage = bot.send_message(message.chat.id,answer)
        uselessMessagesTable.addMessage(botmessage)
        audios = youtube.getPlaylistInfo(playlist_link[chat],chat,val)
        for audio in audios:
            if (stop[chat] == True):
                stop[chat] = None
                break
            bot.send_chat_action(message.chat.id,'upload_audio')
            youtube.download(audio[0],chat)
            try:
                file = open("./music/file" + str(chat) + ".mp3", 'rb')
                performer, title = youtube.titleParse(audio[1])
                botmessage = bot.send_audio(message.chat.id,
                audio = file,
                performer = performer,
                title = title)
                uselessMessagesTable.addMessage(botmessage)
            except Exception as er:
                print(er)
        state[chat] = 0
        anwer = "Удалити всі ці пісні - /clear"
        botmessage = bot.send_message(message.chat.id,answer)
        uselessMessagesTable.addMessage(botmessage)
        return



    if (state[chat] == 50):
        playlist_link[chat] = youtube.getPlaylist(message.text)
        if (playlist_link[chat] is None):
            answer = "Нич похожого не найшовім"
            botmessage = bot.send_message(message.chat.id,answer)
            uselessMessagesTable.addMessage(botmessage)
            log(message,answer)
            state[chat] = 0
            return
        else:
            answer = "Скільки похожих пісень скинути? (Max. 20)"
            botmessage = bot.send_message(message.chat.id,answer)
            uselessMessagesTable.addMessage(botmessage)
            state[chat] = 51
            return

    if (state[chat] == 101):
        if (message.text == PASSWORD):
            answer = "logged in"
            log(message,answer)
            botmessage = bot.send_message(message.chat.id, answer)
            uselessMessagesTable.addMessage(botmessage)
            state[chat] = 100
        else:
            answer = "incorrect password"
            log(message,answer)
            botmessage = bot.send_message(message.chat.id, answer)
            uselessMessagesTable.addMessage(botmessage)
            state[chat] = 0
        return

    if (musicMode[chat] == 1):
        # bot.send_chat_action(message.chat.id, "record_audio")
        song_name = message.text
        song_name = song_name.replace(' ','-')
        ls[chat] = getList(song_name, message)
        ytls[chat] = youtube.search(song_name)
        print(len(ytls[chat]))
        if len(ls[chat])>0 or len(ytls[chat])>0:
            answer = "Туй, але. (Після некст запроса буде недост)"
            id = 0
            markup = types.InlineKeyboardMarkup()
            for i in ls[chat]:
                # BUTTONS INSEAD
                # answer = answer + '/'+ str(id) + ' ' + (i[1]) + "- <b>" + (i[2]) + '</b> <em>' + i[3] + '</em>\n'
                button = types.InlineKeyboardButton(
                text = i[1] + " -- " + i[2] + " ( " + i[3] + " )",
                callback_data = '1'+str(id)
                )
                id += 1
                markup.add(button)
            # bot.send_chat_action(message.chat.id, "upload_audio")
            # file = open('music/'+song_name+'.mp3')
            # bot.send_audio(message.chat.id,file)
            botmessage = bot.send_message(message.chat.id, answer,parse_mode ='HTML' ,reply_markup = markup)
            uselessMessagesTable.addMessage(botmessage)
            log(message,answer)

            answer = "А туй ґомбички з ютуба"
            id = 0
            markup = types.InlineKeyboardMarkup()
            for i in ytls[chat]:
                button = types.InlineKeyboardButton(
                text = i[1],
                callback_data = '2'+str(id)
                )
                markup.add(button)
                id+=1
                if (id > 10):
                    break
            botmessage = bot.send_message(message.chat.id,answer,reply_markup = markup)
            uselessMessagesTable.addMessage(botmessage)
            log(message,answer)
        else:
            print('da')
            answer = 'Сорямба, я нич не найшов'
            botmessage = bot.send_message(message.chat.id, answer)
            uselessMessagesTable.addMessage(botmessage)
            log(message,answer)

bot.polling(none_stop=True, interval=1)

# states
# 0 -> default
# 50 -> /similar typed
# 51 -> song name typed
# 101 -> waiting for password
# 100 -> logged in as admin
# 102 -> waiting for schedule
