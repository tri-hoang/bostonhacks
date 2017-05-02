from flask import Flask, request, redirect, session
from twilio import twiml
import os
from twilio.twiml.messaging_response import MessagingResponse
from bhfilter import *
import urllib2
import urllib
import json
import requests



def propose_tracks(track_title):
    # rewrite --- using requests library to get info from spotify
    search_url = 'https://api.spotify.com/v1/search'
    params = {'q': track_title, 'type': 'track'}
    track_info = requests.get(search_url, params=params).json()
    artist_list = []


    length = len(track_info['tracks']['items'])
    count = 0
    num_artist = 0
    while (count < length):
        if (num_artist == 3):
            break;
        artist_name = track_info['tracks']['items'][count]['album']['artists'][0]['name']
        if (artist_name not in artist_list):
            artist_list.append(artist_name)
            num_artist += 1
        count += 1
    return artist_list




def array_to_string(array):
    string = 'Which one do you like?\n'
    length = len(array)
    for x in range(length):
        string += "(" + str(x + 1) + ") " + array[x] + "\n"
    return string



# Use session to store infos
app = Flask(__name__)
SECRET_KEY = 'a secret key'
app.config.from_object(__name__)

@app.route('/sms', methods=['POST'])
# Handle SMS
def inbound_sms():
    sender_number = request.form['From']
    message_body = request.form['Body']
    resp = MessagingResponse()

    # User requests song with phone number
    if (len(message_body) != 1):
        receiver_number, song_request = filterfunction(message_body)
        tracks_array = propose_tracks(song_request)

        session["receiver_number"] = receiver_number
        session["tracks_array"] = tracks_array
        session["song_request"] = song_request

        # If it is not a working phone number // may need fix
        if (len(receiver_number) < 10):
            resp.message("Don't forget to type in bae's number!")

        # If the song doesn't exist
        elif (len(tracks_array) == 0):
            resp.message("We cannot find the song you requested!")
        else:
            tracks_string = array_to_string(tracks_array)
            resp.message(tracks_string)
        return str(resp)

    # Confirm user's request - Then make a call to receiver_number
    else:
        index = int(message_body) - 1


        # NEED FIX MORE
        session["index"] = index



        reply_string = "Gotcha! " + "We are sending your love to " + session["receiver_number"] + " . . ."
        resp.message(reply_string)



        return str(resp)




if __name__ == '__main__':
    app.run(host= '0.0.0.0')
