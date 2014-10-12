from api import api_v1 as app
from api.response import response
from flask import request, g, jsonify
from data.music import MusicDataAccess
from bson.json_util import dumps

@app.before_request
def before_request():
    g.db = MusicDataAccess()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db = None

""" Song Queue API"""
# Get song queue list
@app.route("/queue/songs", methods=['GET'])
def index():
    songs = g.db.get_queue()

    if songs:

        resp = response(messages="Songs were found in the queue.", data=[song for song in songs], status=200)
    else:
        resp = response(messages="Queue is empty", status=200)

    return resp

# Find song by id
@app.route("/queue/songs/<id>", methods=['GET'])
def show(id):

    song = g.db.find_in_queue(id=song_id)

    if song.count():
        song = song.next()

        resp = response(messages="Found '{0}: {1} -- {2}' in the queue".format(song["artist"], song["title"], song["album"]), status=200)
    else:
        resp = response(messages="No song was found in the queue", status=200)

    return resp

# Add song to queue
@app.route("/queue/songs", methods=['POST'])
def create():

    try:
        song_title = request.json["song_title"]
        artist = request.json["artist"]
        album = request.json["album"]

        song = {
            "title": song_title,
            "artist": artist,
            "album": album,
        }

        g.db.queue(song)
        resp = response(messages="Added new song to queue. '{0}: {1} -- {2}'".format(artist,song_title,album), status=201)
    except KeyError, e:
        resp = response(messages="Incomplete song information, cannot process request.", status=400)

    return resp

# Remove song from queue
@app.route("/queue/songs/<song_id>", methods=['DELETE'])
def destroy(song_id):

    song = g.db.find_in_queue(id=song_id)

    if song.count():
        song_name = song.next()["song_name"]
        g.db.remove_from_queue(id=song_id)
        resp = response(messages="Removed '{0}' from the queue".format(song_name), status=200)
    else:
        resp = response(messages="Song could not be found in queue, cannot remove.", status=200)

    return resp

""" TODO Expose Some grooveshark api options directly """
