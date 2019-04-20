# -*- coding: UTF-8 -*-
import telebot
import urllib
import requests


TOKEN = "743596317:AAFGbmXQOXakO_MpFWFkXzltzLB6__eRYOs"

bot = telebot.TeleBot(TOKEN)

lastNotUsed = 0
transChatId = {} # Transformed chatId into freeSpaceIndex
state = []
pos = []
ls = [[]]

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
            #print('Link found: '+ s[p1:p2])
            return s[p1:p2]
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
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = "https://music.xn--41a.ws/search/"+song+"/"
    htmlContent = requests.get(url, headers=headers)


    s = htmlContent.content
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
    destination = 'music/file'+str(chat)+'.mp3'
    url = 'https://music.xn--41a.ws' + a[0]
    print('downloading: ' + a[1] + '-' + a[2])
    urllib.urlretrieve(url, destination)
    print('music downloaded: ' + a[1] + '-' + a[2])


def init(message):
    global state,lastNotUsed,transChatId,ls,pos
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
           ' chat:' + str(transChatId[message.chat.id]) + ' message:' + (message.text))

def log(message, answer):
    print('Reply to ' + message.from_user.first_name + ': ' + answer)


@bot.message_handler(commands=['help'])
def handle_help(message):
    global state,transChatId
    init(message)
    state[transChatId[message.chat.id]] = 0
    answer = "Поки я вмію шукати музику. Пишеш /music, потім назву пісні або автора. Отримуєш список з 11 пісень (або менше) і" \
             " вибераєш ту, яка тобі підходить. Потім чекаєш в середньому секунд 20 і отримуєш свій трек 😎😎😎"
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

@bot.message_handler(commands=['music'])
def handle_music(message):
    global state,transChatId
    init(message)
    answer = "Що за музон хочеш?"
    log(message, answer)
    bot.send_message(message.chat.id,answer)
    state[transChatId[message.chat.id]] = 1

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
        file = open('music/file'+str(chat)+'.mp3')
        bot.send_chat_action(message.chat.id,'upload_audio')
        bot.send_audio(message.chat.id, file, None, None, ls[chat][indx][1],ls[chat][indx][2])
        state[chat] = 0


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
        song_name.replace(' ', '-')
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
            state[chat] = 0




bot.polling(none_stop=True, interval=0)
