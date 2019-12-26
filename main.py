import requests
import deezer
from transliterate import translit
import os
from mutagen.flac import FLAC


#SOON
auth = 0 #Use deezer auth (0 = Use without auth, 1 = Use with auth)
auth_login = 'DEEZER LOGIN'
auth_password = 'DEEZER PASSWORD'
#SOON

client = deezer.Client()

m = 0
def getmode():
    global m
    print("Select mode:")
    print("1) Download track")
    print("2) Download playlist")
    print("3) Download album")
    print("4) Search")
    try:
        m = int(input())
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
    if not os.path.exists("music/"):
        os.mkdir("music/")
    for i in trlist:
        print(i[1].artist.name+" - "+i[1].title)
        trurl = "https://dz.loaderapp.info/deezer/1411/"+i[1].link
        d(trurl, "music/"+translit(i[1].title, "ru", reversed=True)+".flac")
        audio = FLAC("music/"+translit(i[1].title, "ru", reversed=True)+".flac")
        audio['albumartist'] = i[1].artist.name
        audio['artist'] = i[1].artist.name
        audio.save()

    print("Done")

def mode():
    global m
    tracks = []
    if(m == 1):
        try:
            trid = int(input("Enter ID: "))
            url = client.get_track(trid)
            temp = []
            temp.append(trid)
            temp.append(url)
            tracks.append(temp)
        except Exception:
            mode()
    if(m == 2):
        try:
            plid = int(input("Enter ID: "))
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
            alid = int(input("Enter ID: "))
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
            print(i.artist.name+" - "+i.title+" | Album name: "+i.album.title)
    if(m != 4):
        return tracks

def start():
    getmode()
    trlist = mode()
    if(m != 4):
        download(trlist)
    again()

def again():
    want = input("Do you want to continue [0/1]: ")
    if(want == "1"):
        start()
    if(want == "0"):
        print("OK!")
    else:
        again()

start()
