from flask import Flask, request, redirect
from twilio import twiml
import os
from twilio.twiml.messaging_response import MessagingResponse
import bhfilter
import urllib2
import urllib
import json



def propose_tracks(a):

    a = urllib.quote(a)
    array = []

    content = urllib2.urlopen("https://api.spotify.com/v1/search?q=" + a + "&type=track").read()
    content = json.loads(content)
    array = []

    length = len(content['tracks']['items'])
    if length == 0:
        return reply_false()
    else:
        for x in range(length):
            artist_name = content['tracks']['items'][x]['album']['artists'][0]['name']
            if (x == 3):
                break;
            else:
                if (artist_name not in array):
                    array.append(artist_name)
    return array


def array_to_string(array):
    string = 'Who is your favorite artist?\n'
    length = len(array)
    for x in range(length):
        string += "(" + str(x + 1) + ") " + array[x] + "\n"
    return string




app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    phone_number, song_request = bhfilter.filterfunction(message_body)


    resp = MessagingResponse()

    a_array = propose_tracks(song_request)
    a_string = array_to_string(a_array)

    resp.message(a_string)

    return str(resp)

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
