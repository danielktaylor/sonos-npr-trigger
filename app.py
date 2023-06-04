from __future__ import print_function
from flask import Flask
import soco
from threading import Thread

# Page scraping
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import operator

app = Flask(__name__)
print("Server started.")

def get_sonos():
    sonos = soco.discovery.any_soco()
    if not sonos.group:
        return sonos
    return sonos.group.coordinator

def get_latest_playlist():
    base = 'https://www.npr.org/programs/'
    urls = {
        'all_things_considered': 'all-things-considered/',
        'weekend_edition': 'weekend-edition-saturday/',
        'weekend_edition_sunday': 'weekend-edition-sunday/',
        'morning_edition': 'morning-edition/'
    }
    dates = {}
    m3u = {}

    for program, url in urls.items():
        url = base + url
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        audioLabels = soup.find_all(class_='audio-tool-label')
        dates[program] = parse(
            soup.find("div", {"class": "current"}).find("time")['datetime'])

        files = []
        for a in audioLabels:
            if (a.text == 'Download'):
                p = a.parent
                href = p.get('href')
                href = href.split('?')[0]
                #story_title = a.find_parent('article', {"class": "rundown-segment"}).find('h3', {"class": "rundown-segment__title"}).find('a').text
                story_title = "Title"
                files.append([href, story_title])

        m3u[program] = files

    # Get latest program
    if m3u["all_things_considered"] == []:
        del dates['all_things_considered']
    if m3u["morning_edition"] == []:
        del dates['morning_edition']
    if m3u["weekend_edition"] == []:
        del dates['weekend_edition']
    if m3u["weekend_edition_sunday"] == []:
        del dates['weekend_edition_sunday']

    if 'morning_edition' in dates and 'all_things_considered' in dates and dates['morning_edition'] == dates['all_things_considered']:
        del dates['morning_edition']
    if 'weekend_edition' in dates and 'all_things_considered' in dates and dates['all_things_considered'] == dates['weekend_edition']:
        del dates['weekend_edition']
    if 'weekend_edition_sunday' in dates and 'all_things_considered' in dates and dates['all_things_considered'] == dates['weekend_edition_sunday']:
        del dates['weekend_edition_sunday']
    latest = max(dates.items(), key=operator.itemgetter(1))[0]

    return m3u[latest]

def start_npr():
    # Grab the Sonos
    s = get_sonos()
    
    # Create a group with all devices
    s.partymode()
    
    # Stop and clear queue
    s.stop()
    s.clear_queue()
    
    # Set volume to 25%
    if not s.group:
        s.volume = 25
    else:
        for g in s.group.members:
            g.volume = 25
            
    # Send the playlist and start playing
    playlist = get_latest_playlist()
    for mp3 in playlist:
        print("Adding MP3: %s" % mp3)
        s.add_uri_to_queue(mp3[0])
    s.play_from_queue(0)
    return "OK"

@app.route("/listen", methods=['POST','GET'])
def listen():
    print("Starting...")
    Thread(target=start_npr).start()
    return "OK"

@app.route("/pause")
def pause():
    print("Pausing")
    s = get_sonos()
    s.pause()
    return "OK"

@app.route("/resume")
def resume():
    print("Resuming track")
    s = get_sonos()
    s.play()
    return "OK"

@app.route("/skip")
def skip():
    print("Skipping track")
    s = get_sonos()
    s.next()
    return "OK"

@app.route("/volumeup")
def volumeup():
    print("Turning volume up")
    sonos = get_sonos()
    vol = sonos.volume
    sonos.volume = vol+10
    return "OK"

@app.route("/volumedown")
def volumedown():
    print("Turning volume down")
    sonos = get_sonos()
    vol = sonos.volume
    sonos.volume = vol-10
    return "OK"
