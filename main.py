import requests
import deezer
from transliterate import translit
import os
from mutagen.flac import FLAC
import json
import appex


#SOON
auth = 0 #Use deezer auth (0 = Use without auth, 1 = Use with auth)
auth_login = 'DEEZER LOGIN'
auth_password = 'DEEZER PASSWORD'
#SOON

#DCLOUD
dcloud_url = "" #DCLOUD URL
dcloud_token = "" #DCLOUD TOKEN
#DCLOUD

#Download server
download_server = "" #URL to download server (http://github.com/superdima05/deezer-grabber-server/)
#Download server

music_dir = "music_f/"

client = deezer.Client()

def dcloud(token, url, method, data):
    if(url == ""):
        return ""
    if(token == ""):
        return ""
    url = url+"?token="+token+"&data="+data+"&method="+method
    try:
        r = requests.get(url).text
        r = json.loads(r)
    except Exception:
        return "Incorrect url."
    if(method == "auth"):
        if(r['code'] == 200):
            return True
        if(r['code'] == 102):
            return r['message']
        else:
            return False
    else:
        return r

m = 0
def getmode():
    global m
    print("Select mode:")
    print("1) Download track")
    print("2) Download playlist")
    print("3) Download album")
    print("4) Search")
    dcl = dcloud(dcloud_token, dcloud_url, "auth", "")
    if(dcl == True):
        print("Dcloud connected!")
        print("5) Get all tracks")
        print("6) Remove track from cloud")
        print("7) Update library")
        print("8) Re-download all library")
    else:
        if(dcl != ""):
            print("Dcloud error while connecting: "+dcl)
    try:
        m = int(input())
        if(dcl == True):
            if(m > 8):
                getmode()
        else:
            if(m > 4):
                getmode()
        if(m < 1):
            getmode()
    except Exception:
        getmode()

def d(url, file_name):
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

def download(trlist):
    global music_dir, m
    if not os.path.exists(music_dir):
        os.mkdir(music_dir)
    for i in trlist:
        dcl = dcloud(dcloud_token, dcloud_url, "auth", "")
        if(dcl == True):
            dcl = dcloud(dcloud_token, dcloud_url, "add", str(i[0]))
            if(dcl['code'] == 200):
                if(dcl['message'] == ""):
                    if(m != 7):
                        if(m != 8):
                            print("Track was added to Dcloud")
                else:
                    if(m != 7):
                        if(m != 8):
                            print("Dcloud message: "+dcl['message'])
        print(i[1].artist.name+" - "+i[1].title)
        trurl = "https://dz.loaderapp.info/deezer/1411/"+i[1].link
        if(download_server != ""):
            trurl = download_server+i[1].link
        d(trurl, music_dir+translit(i[1].title, "ru", reversed=True)+".flac")
        audio = FLAC(music_dir+translit(i[1].title, "ru", reversed=True)+".flac")
        audio['albumartist'] = i[1].artist.name
        audio['artist'] = i[1].artist.name
        audio['comment'] = str(i[0])
        audio.save()

    print("Done")

def mode():
    global m, music_dir, id
    tracks = []
    if(m == 1):
        try:
            if(id == 0):
                trid = int(input("Enter ID: "))
            else:
                trid = id
            url = client.get_track(trid)
            temp = []
            temp.append(trid)
            temp.append(url)
            tracks.append(temp)
        except Exception:
            mode()
    if(m == 2):
        try:
            if(id == 0):
                plid = int(input("Enter ID: "))
            else:
                plid = id
            url = client.get_playlist(plid)
            for i in url.tracks:
                temp = []
                temp.append(i.id)
                temp.append(i)
                tracks.append(temp)
        except Exception:
            mode()
    if(m == 3):
        try:
            if(id == 0):
                alid = int(input("Enter ID: "))
            else:
                alid = id
            url = client.get_album(alid)
            for i in url.tracks:
                temp = []
                temp.append(i.id)
                temp.append(i)
                tracks.append(temp)
        except Exception:
            mode()
    if(m == 4):
        query = input("Search: ")
        result = client.search(query)
        for i in result:
            print(i.artist.name+" - "+i.title+" | Album name: "+i.album.title+" ID: "+str(i.id))
    if(m == 5 or m == 6 or m == 7 or m == 8):
        dcl = dcloud(dcloud_token, dcloud_url, "auth", "")
        if(dcl == True):
            if(m == 5):
                dcl = dcloud(dcloud_token, dcloud_url, "get", "")
                for i in dcl['result']:
                    print(i[1]+" - "+i[2]+" ID: "+i[0])
            if(m == 6):
                print("1) Remove track")
                print("2) Remove album")
                print("3) Remove playlist")
                try:
                    t = int(input())
                    if(t == 1):
                        t = int(input("Enter ID: "))
                        dcl = dcloud(dcloud_token, dcloud_url, "rem", str(t))
                        if(dcl['code'] == 106):
                            print(dcl['message'])
                        else:
                            print("Track was deleted")
                    if(t == 2):
                        t = int(input("Enter ID: "))
                        url = client.get_album(t)
                        for i in url.tracks:
                            dcl = dcloud(dcloud_token, dcloud_url, "rem", str(i.id))
                            if(dcl['code'] == 106):
                                print(dcl['message'])
                            else:
                                print("Track was deleted")
                    if(t == 3):
                        t = int(input("Enter ID: "))
                        url = client.get_playlist(t)
                        for i in url.tracks:
                            dcl = dcloud(dcloud_token, dcloud_url, "rem", str(i.id))
                            if(dcl['code'] == 106):
                                print(dcl['message'])
                            else:
                                print("Track was deleted")
                except Exception:
                    mode()
            if(m == 7):
                if not os.path.exists(music_dir):
                    os.mkdir(music_dir)
                d = os.scandir(music_dir)
                tid = []
                dcl = dcloud(dcloud_token, dcloud_url, "get", "")
                for i in d:
                    if(i.path.replace(".flac", "") != i.path):
                        try:
                            audio = FLAC(i.path)
                        except Exception:
                            os.remove(i.path)
                        try:
                            temp = []
                            temp.append(int(audio['comment'][0]))
                            temp.append(i.path)
                            tid.append(temp)
                        except Exception:
                            none = 1
                for i in tid:
                    exist = 0
                    for b in dcl['result']:
                        if(i[0] == int(b[0])):
                            exist = 1
                    if(exist == 0):
                        print("Remove "+i[1])
                        os.remove(i[1])
                for b in dcl['result']:
                    exist = 0
                    for i in tid:
                        if(int(b[0]) == i[0]):
                            exist = 1
                    if(exist == 0):
                        print("Download "+b[1])
                        temp = []
                        c = client.get_track(b[0])
                        temp.append(c.id)
                        temp.append(c)
                        tracks.append(temp)
            if(m == 8):
                if not os.path.exists(music_dir):
                    os.mkdir(music_dir)
                d = os.scandir(music_dir)
                for i in d:
                    if(i.path.replace(".flac", "") != i.path):
                        os.remove(i.path)
                dcl = dcloud(dcloud_token, dcloud_url, "get", "")
                for i in dcl['result']:
                    temp = []
                    c = client.get_track(i[0])
                    print("Download "+c.title)
                    temp.append(c.id)
                    temp.append(c)
                    tracks.append(temp)


        else:
            return tracks
    if(m != 4):
        return tracks

def start():
    global m, id
    id = 0
    if appex.is_running_extension():
            url = appex.get_url()
            if not url:
                print('No input URL found.')
                exit()
            else:
                if(url.replace("track", "") != url):
                    m = 1
                    id = url.split("/")
                    id = id[len(id)-1]
                elif(url.replace("playlist", "") != url):
                    m = 2
                    id = url.split("/")
                    id = id[len(id)-1]
                elif(url.replace("album", "") != url):
                    m = 3
                    id = url.split("/")
                    id = id[len(id)-1]
                else:
                    print("No method, use search")
                    m = 4
    else:
        getmode()
    trlist = mode()
    if(m != 4):
        if(m != 5):
            if(m != 6):
                download(trlist)
    again()

def again():
    if appex.is_running_extension():
        return
    want = input("Do you want to continue [0/1]: ")
    if(want == "1"):
        start()
    if(want == "0"):
        print("OK!")
        exit()
    else:
        again()

start()
