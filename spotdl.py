#!/usr/bin/env python


# +++USAGE+++
# spotdl.getThis("song name")


from bs4 import BeautifulSoup
from random import choice
from shutil import copyfileobj
from sys import path
import spotipy
import eyed3
import requests
import pafy
import os
import argparse
import sys
import base64
#import spotipy.util as util

eyed3.log.setLevel("ERROR")

os.chdir(path[0])

if not os.path.exists("Music"):
	os.makedirs("Music")
open('list.txt', 'a').close()

spotify = spotipy.Spotify()


headers = (
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
	'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko)',
	'Chrome/19.0.1084.46 Safari/536.5',
	'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko)',
	'Chrome/19.0.1084.46',
	'Safari/536.5',
	'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13',
	)

def searchYT(number):
	items = requests.get(URL, headers=header).text
	items_parse = BeautifulSoup(items, "html.parser")
	check = 1
	first_result = items_parse.find_all(attrs={'class':'yt-uix-tile-link'})[0]['href']
	while not first_result.find('channel') == -1 or not first_result.find('googleads') == -1:
		first_result = items_parse.find_all(attrs={'class':'yt-uix-tile-link'})[check]['href']
		check += 1
	del check
	full_link = "youtube.com" + first_result
	global video
	video = pafy.new(full_link)
	global raw_title
	raw_title = (video.title).encode("utf-8")
	global title
	title = ((video.title).replace("\\", "_").replace("/", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace('"', "_").replace("<", "_").replace(">", "_").replace("|", "_").replace(" ", "_")).encode('utf-8')

def checkExists(islist):
	if os.path.exists("Music/" + title + ".m4a.temp"):
		os.remove("Music/" + title + ".m4a.temp")
	global extension
	if os.path.exists("Music/" + title + ".m4a"):
		os.remove("Music/" + title + ".m4a")
	extension = '.mp3'
	if os.path.isfile("Music/" + title + extension):
		if extension == '.mp3':
			audiofile = eyed3.load("Music/" + title + extension)
			if isSpotify() and not audiofile.tag.title == content['name']:
				os.remove("Music/" + title + extension)
				return False
		if islist:
			return True
		else:
			prompt = "n"
			if prompt == "y":
				os.remove("Music/" + title + extension)
				return False
			else:
				return True

def fixSong():
	print('Fixing meta-tags')
	audiofile = eyed3.load("Music/" + title + '.mp3')
	audiofile.tag.artist = content['artists'][0]['name']
	audiofile.tag.album = content['album']['name']
	audiofile.tag.title = content['name']
	albumart = (requests.get(content['album']['images'][0]['url'], stream=True)).raw
	with open('last_albumart.jpg', 'wb') as out_file:
		copyfileobj(albumart, out_file)
	albumart = open("last_albumart.jpg", "rb").read()
	audiofile.tag.images.set(3,albumart,"image/jpeg")
	audiofile.tag.save(version=(2,3,0))


def playSong():
	if not title == '':
		if not os.name == 'nt':
			os.system('mplayer "' + 'Music/' + title + extension + '"')
		else:
			print('Playing ' + title + '.mp3')
			os.system('start ' + 'Music/' + title + extension)

def convertSong():
	global title
	title = title.replace('`', '')
	if not os.name == 'nt':
		os.system('avconv -loglevel 0 -i "' + 'Music/' + title + '.m4a" -ab 192k "' + 'Music/' + title + '.mp3"')
	else:
		os.system('Scripts\\avconv.exe -loglevel 0 -i "' + 'Music/' + title + '.m4a" -ab 192k "' + 'Music/' + title + '.mp3"')
	# os.remove('Music/' + title + '.m4a')

def downloadSong():
	a = video.getbestaudio(preftype="m4a")
	a.download(filepath="Music/" + title.replace('`', '') + ".m4a", quiet=True)

def isSpotify():
	if (len(raw_song) == 22 and raw_song.replace(" ", "%20") == raw_song) or (raw_song.find('spotify') > -1):
		return True
	else:
		return False

def trackPredict():
	global URL
	if isSpotify():
		global content
		content = spotify.track(raw_song)
		song = (content['artists'][0]['name'] + ' - ' + content['name']).replace(" ", "%20").encode('utf-8')
		URL = "https://www.youtube.com/results?sp=EgIQAQ%253D%253D&q=" + song
	else:
		song = raw_song.replace(" ", "%20")
		URL = "https://www.youtube.com/results?sp=EgIQAQ%253D%253D&q=" + song
		song = ''

title = ''
song = ''
raw_song = ''
header = {'User-agent': choice(headers)}

def getThis(request):
	global raw_song
	raw_song = request.decode('utf-8').encode('utf-8')
	trackPredict()
	searchYT(number=None)
	if not checkExists(islist=False):
		downloadSong()
		convertSong()
		if isSpotify():
			fixSong()
	return title + ".mp3"
