from __future__ import unicode_literals
import urllib.request
import requests
import youtube_dl
import ssl
gcontext = ssl.SSLContext()  # Only for gangstars
ssl._create_default_https_context = ssl._create_unverified_context
def search(query):
    headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'  # This is another valid field
    }

    link = "https://youtube.com/results?search_query="+query

    html = requests.get(link,headers = headers)
    file = open('output.html',"w")
    file.write(html.content.decode())

    htmlContent = html.content.decode()
    pos = 0
    results = []
    while True:
        pos = htmlContent.find("class=\"yt-lockup-title",pos)
        if (pos == -1):
            break
        pos = htmlContent.find("<a href=",pos)
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
        pos = htmlContent.find(">",pos)
        pos+=1
        pos = htmlContent.find(">",pos)
        pos+=1
        while (htmlContent[pos]!='<'):
            title+=htmlContent[pos]
            pos+=1
        results.append([link,title])
        if (pos == -1):
            break
    return results
def download(link,chat=""):
    print(link)
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
        'outtmpl': './music/file' + str(chat) + '.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

def titleParse(title):
    pos = title.find('-')
    pos2 = title.find('-',pos)
    if (pos2-pos > 1):
        return title,title
    if (pos2 == -1):
        pos2 = pos
    return title[:(pos-1)],title[(pos2+1):]
