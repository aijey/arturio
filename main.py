# -*- coding: UTF-8 -*-
import telebot
import urllib
import requests
import urllib.request
import ssl
import psycopg2
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

TOKEN = "743596317:AAFGbmXQOXakO_MpFWFkXzltzLB6__eRYOs"
PASSWORD = "admin"

schedule_message_id = 0

bot = telebot.TeleBot(TOKEN)

lastNotUsed = 0
transChatId = {} # Transformed chatId into freeSpaceIndex
state = []
pos = []
ls = [[]]
def initDB():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')

        cursor = connection.cursor();

        commands = """ INSERT INTO PARAMS(var_name)
                       VALUES(%s)"""

        cursor.execute(commands, ('schedule_message_id',))
        connection.commit()
        connection.close()
        cursor.close()
        print("Successful initDB")
    except (Exception, psycopg2.Error) as er:
        print(er)

def saveSchedule(message_id):
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')

        cursor = connection.cursor();

        commands = """ UPDATE PARAMS
                       SET value = %s
                       WHERE var_name = 'schedule_message_id' """

        cursor.execute(commands, (message_id,))
        connection.commit()
        connection.close()
        cursor.close()
        print("Successfully saved")
        return True;
    except (Exception, psycopg2.Error) as er:
        print(er)
        return False;
def getSchedule():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')

        cursor = connection.cursor()

        commands = """
        SELECT value
        FROM params
        WHERE var_name = 'schedule_message_id';
        """

        cursor.execute(commands)
        message_id = cursor.fetchone()[0]
        cursor.close()
        connection.close()

        return message_id



    except (Exception, psycopg2.Error) as er:
        print(er)
        return None;


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


def getFile(a,chat):
    file_name = 'music/file'+str(chat)+'.mp3'
    url = 'http://music.xn--41a.ws' + a[0]
    print('downloading: ' + a[1] + '-' + a[2])
    gcontext = ssl.SSLContext()  # Only for gangstars
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(url, file_name)
    print('music downloaded: ' + a[1] + '-' + a[2])
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


    ### LOG ###
    print ('User:' + message.from_user.first_name + ' chat_id:' + str(message.chat.id) +
           ' chat:' + str(transChatId[message.chat.id]))
    if (message.text != None):
        print('Message: ' + message.text)

def log(message, answer):
    print('Reply to ' + message.from_user.first_name + ': ' + answer)


@bot.message_handler(commands=['help'])
def handle_help(message):
    global state,transChatId
    init(message)
    state[transChatId[message.chat.id]] = 0
    answer = "Поки я вмію шукати музику. Пишеш /music, щоб ввімкнути режим музики, потім назву пісні або автора. Отримуєш список з 11 пісень (або менше) і" \
             " вибераєш ту, яка тобі підходить. Потім чекаєш в середньому секунд 20 і отримуєш свій трек 😎😎😎. Після цього можеш знову написати /music і " \
             " вимкнути режим пошуку музики, або написати назву іншої пісні, якщо плануєш знайте ще одну."
    bot.send_message(message.chat.id, answer)


    ### LOG ###
    log(message,answer)

@bot.message_handler(commands=['start'])
def handle_start(message):
    global state, transChatId
    init(message)
    state[transChatId[message.chat.id]] = 0
    answer = "Дороуля, тикай /help і всьо узнаєш"
    bot.send_message(message.chat.id, answer)
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
        bot.send_message(message.chat.id, answer)
    else:
        if (state[chat] < 200):
            answer = "logged out"
            log(message, answer)
            bot.send_message(message.chat.id, answer)
            state[chat] = 0

@bot.message_handler(commands=['setschedule'])
def handle_setschedule(message):
    global state, transChatId
    init(message)
    chat = transChatId[message.chat.id]
    if (state[chat] == 100):
        answer = "Скинь фотку розкладом"
        log(message, answer)
        bot.send_message(message.chat.id, answer)
        state[chat] = 102

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global state, transChatId
    init(message)
    chat = transChatId[message.chat.id]
    if (state[chat] == 102):
        schedule_message_id = message.message_id
        saveSchedule(schedule_message_id);
        answer = "Сохранив розклад. "
        log(message, answer)
        bot.send_message(message.chat.id, answer)
        state[chat] = 100

@bot.message_handler(commands=['schedule'])
def handle_schedule(message):
    global state, transChatId
    init(message)
    chat = transChatId[message.chat.id]
    schedule_message_id = getSchedule()
    if (schedule_message_id is not None):
        answer = "Розклад:"
        bot.send_message(message.chat.id, answer)
        bot.forward_message(message.chat.id, message.chat.id,schedule_message_id)
        log(message, answer)
    else:
        answer = "Ниє у ня розклада"
        bot.send_message(message.chat.id, answer)
        log(message,answer)

@bot.message_handler(commands=['music'])
def handle_music(message):
    global state,transChatId
    init(message)
    if (state[transChatId[message.chat.id]] == 0):
        answer = "Включивім режим пошуку музики"
        log(message, answer)
        bot.send_message(message.chat.id,answer)
        state[transChatId[message.chat.id]] = 1
    else :
        answer = "Виключивім режим пошуку музики"
        log(message, answer)
        bot.send_message(message.chat.id,answer)
        state[transChatId[message.chat.id]] = 0



@bot.message_handler(commands=['0','1','2','3','4','5','6','7','8','9','10'])
def handle_selection(message):
    global state
    global ls,transChatId
    init(message)
    chat = transChatId[message.chat.id]
    if (state[chat] == 2):
        answer = 'Ща всьо буде'
        bot.send_message(message.chat.id,answer)
        log(message,answer)
        bot.send_chat_action(message.chat.id,'upload_audio')
        indx = int(message.text[1:])
        getFile(ls[chat][indx],chat)
        answer = 'Скачавім, гружу тепер тобі'
        bot.send_message(message.chat.id,answer)
        log(message,answer)
        # file = open('music/file'+str(chat)+'.mp3')
        bot.send_chat_action(message.chat.id,'upload_audio')
        bot.send_audio(message.chat.id,
        audio = open('music/file'+str(chat)+'.mp3', 'rb'),
        performer =  ls[chat][indx][1],
        title = ls[chat][indx][2])
        state[chat] = 1


        ### LOG ###
        print("Music sent: "+ ls[chat][indx][1] + '-' + ls[chat][indx][2])

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global state
    global ls,transChatId
    init(message)
    chat = transChatId[message.chat.id]
    if (state[chat] == 1):
        # bot.send_chat_action(message.chat.id, "record_audio")
        song_name = message.text
        song_name = song_name.replace(' ','-')
        ls[chat] = getList(song_name, message)
        if len(ls[chat])>0:
            answer = ""
            id = 0
            for i in ls[chat]:
                answer = answer + '/'+ str(id) + ' ' + (i[1]) + "- <b>" + (i[2]) + '</b> <em>' + i[3] + '</em>\n'
                id = id + 1
            # bot.send_chat_action(message.chat.id, "upload_audio")
            # file = open('music/'+song_name+'.mp3')
            # bot.send_audio(message.chat.id,file)
            bot.send_message(message.chat.id, answer,None,None,None, 'HTML' )
            log(message,answer)
            state[chat] = 2
        else:
            print('da')
            answer = 'Сорямба, я нич не найшов'
            bot.send_message(message.chat.id,answer)
            log(message,answer)

    if (state[chat] == 101):
        if (message.text == PASSWORD):
            answer = "logged in"
            log(message,answer)
            bot.send_message(message.chat.id,answer)
            state[chat] = 100
        else:
            answer = "incorrect password"
            log(message,answer)
            bot.send_message(message.chat.id,answer)
            state[chat] = 0

initDB()
bot.polling(none_stop=True, interval=1)

# states
# 0 -> default
# 1 -> waiting for music_name
# 2 -> select music from selection
# 101 -> waiting for password
# 100 -> logged in as admin
# 102 -> waiting for schedule
