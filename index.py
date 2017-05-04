import urllib2, urllib, json, os, spotdl, sys
from flask import Flask, request, redirect, session, Response
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from bhfilter import *
from lxml import etree
reload(sys)  
sys.setdefaultencoding('utf8')

account_sid = "---"
auth_token  = "---"
MP3_PATH    = "---"
FROM_NUM    = "---"
SECRET_KEY  = "---"

def propose_tracks(a):
    a = urllib.quote(a)
    array = []

    content = urllib2.urlopen("https://api.spotify.com/v1/search?q=" + a + "&type=track").read()
    content = json.loads(content)
    array = []

    length = len(content['tracks']['items'])
    count = 0
    num_artist = 0
    while (count < length):
        if (num_artist == 3):
            break;
        artist_name = content['tracks']['items'][count]['album']['artists'][0]['name']
        if (artist_name not in array):
            array.append(artist_name)
            num_artist += 1
        count += 1
    return array


def array_to_string(array):
    string = 'Which one do you like?\n'
    length = len(array)
    for x in range(length):
        string += "(" + str(x + 1) + ") " + array[x] + "\n"
    return string



# Use session to store infos
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/sms', methods=['POST'])
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
        
        reply_string = "Gotcha! " + "We are sending your love to " + session["receiver_number"] + " . . ."

        client = Client(account_sid, auth_token)
        file = spotdl.getThis(session["song_request"] + " by " + session["tracks_array"][index])
        path = request.url[:-3] + "xml/"
        call = client.calls.create(\
            to="+1" + session["receiver_number"],\
             from_=FROM_NUM,\
             url=path\
              + file.encode('utf-8')\
               + ".xml".encode('utf-8'))
        print(path + file + ".xml")
        print(call.sid)
        resp.message(reply_string)
        return str(resp)

@app.route('/xml/<file>.xml', methods=['POST', 'GET'])
def generate_xml(file):
    root = etree.Element('Response')
    child = etree.Element('Say')
    child.text = "someone sent you this song"
    child.attrib['voice'] = "alice"
    root.append(child)
    child = etree.Element('Play')
    child.text = MP3_PATH + file
    root.append(child)
    s = etree.tostring(root, pretty_print=True)
    return Response(s, mimetype='text/xml')


if __name__ == '__main__':
    app.run(host= '0.0.0.0')
