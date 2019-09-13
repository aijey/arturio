from __future__ import unicode_literals
import urllib.request
import requests
import youtube_dl
import ssl
import json
import os
from math import *
import html.parser
gcontext = ssl.SSLContext()  # Only for gangstars
ssl._create_default_https_context = ssl._create_unverified_context
def search(query):
    headers = {
    # 'User-Agent': 'My User777Agent 1.0',
    # 'From': 'youremai654567l@domain.com'  # This is another valid field
    }

    link = "https://youtube.com/results?search_query="+query

    htmlPage = requests.get(link,headers = headers)
    print("RESULTING ENCODING: " + str(htmlPage.encoding))
    file = open('Search/output.html',"w")
    htmlContent = htmlPage.content.decode()
    htmlContent = html.parser.HTMLParser().unescape(htmlContent)

    file.write(htmlContent)
    file.close()

    pos = 0
    results = []
    while True:
        pos = htmlContent.find("class=\"yt-lockup-title",pos)
        if (pos == -1):
            break
        pos = htmlContent.find("<a href=",pos)
        if (pos == -1):
            break
        pos += 9
        link = ""
        title = ""
        while True:
            if (htmlContent[pos]!="\""):
                link += htmlContent[pos]
                pos+=1
            else:
                break
        if (len(link)>20):
            print("BAD LINK")
            continue
        link = "https://youtube.com" + link
        pos = htmlContent.find("title=",pos)
        pos+=6
        to = htmlContent.find(" rel=\"spf-prefetch\"", pos)
        to2 = htmlContent.find(" aria-describedby", pos)
        to = min(to, to2)
        title = htmlContent[pos+1:to-1]
        print(title)
        # pos = htmlContent.find(">",pos)
        # pos+=1
        # pos = htmlContent.find(">",pos)
        # pos+=1
        # while (htmlContent[pos]!='<'):
        #     title+=htmlContent[pos]
        #     pos+=1
        results.append([link,title])
        if (pos == -1):
            break
    return results
def download(link, videoonly = False, chat=""):
    print(link)
    ydl_opts = {}
    if (videoonly == False):
        ydl_opts = {
            'nocheckcertificate': True,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'workaround': 'no-check-certificate',
            'audioformat': 'mp3',
            'outtmpl': './Video/file' + str(chat) +'.%(ext)s'
        }
    else:
        os.system('rm Video/file' + str(chat) +'.mp4')
        ydl_opts = {
            'format': '(mp4)',
            'nocheckcertificate': True,
            'outtmpl': './Video/file' + str(chat) +'.%(ext)s',
            'nooverwrites': False
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

def downloadPlaylist(playlist_link,chat,playlistend=10):
    print("D-loading playlist for: " + str(chat))
    ydl_opts = {
        'nocheckcertificate': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'workaround': 'no-check-certificate',
        'audioformat': 'mp3',
        'playlistend' : playlistend,
        'outtmpl': './Music/playlist/' + str(chat) + '?%(playlist_index)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_link])

def titleParse(title):
    pos = title.find('-')
    if (pos == -1):
        return title, title
    pos2 = title.find('-', pos + 1)
    if (pos2 == -1):
        performer = title[:(pos - 1)]
        title = title[(pos + 1):]
        return performer, title
    else:
        return title, title

def getPlaylist(query):
    res = search(query)
    if (len(res)==0):
        return None
    link = res[0][0]
    htmlContent = requests.get(link).content.decode()
    pos = 0
    to_search = "<li class=\"video-list-item related-list-item  show-video-time related-list-item-compact-radio\"><a href=\""

    pos = htmlContent.find(to_search,pos)
    playlist_link = "https://youtube.com"
    if (pos == -1):
        return None
    else:
        pos+=len(to_search)
        while htmlContent[pos]!="\"":
            playlist_link += htmlContent[pos]
            pos+=1
    return playlist_link

def getPlaylistInfo(playlist_link,chat="",playlistend=10):
    if (playlistend > 20):
        playlistend = 20
    print(playlist_link)
    ydl_opts = {
        'nocheckcertificate': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'workaround': 'no-check-certificate',
        'audioformat': 'mp3',
        'playlistend' : playlistend,
        'outtmpl': './Music/playlist/' + str(chat) + '?%(playlist_index)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_link, download = False)
        file = open("output.txt", mode = "w")
        file.write(json.dumps(info))
        file.close()
        res = []
        for item in info['entries']:
            video = ["https://www.youtube.com/watch?v=" + item['id'], item['title']]
            res.append(video)
        return res
