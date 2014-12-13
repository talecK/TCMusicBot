from api import api_v1 as app
from api.response import response
from flask import request, g, jsonify
from data.music import MusicDataAccess, extract_song_data
from core.cli.music import MusicClient
from bson.json_util import dumps
import json

@app.before_request
def before_request():
    g.db = MusicDataAccess()
    g.client = MusicClient()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, "db", None)
    if db is not None:
        db = None

""" Song Queue API """
# Get song queue list
@app.route("/queue/songs", methods=["GET"])
def all_songs_in_queue():
    songs = g.db.get_queue()

    if songs:

        resp = response(messages="Songs were found in the queue.", data=[song for song in songs], status=200)
    else:
        resp = response(messages="Queue is empty", status=200)

    return resp

# Find song by id
@app.route("/queue/songs/<id>", methods=["GET"])
def find_song_in_queue(id):

    song = g.db.find_in_queue(id=song_id)

    if song.count():
        song = song.next()

        resp = response(messages="Found {0}: {1} -- {2} in the queue".format(song["artist"], song["title"], song["album"]), status=200)
    else:
        resp = response(messages="No song was found in the queue", status=200)

    return resp

# Add song to queue
@app.route("/queue/songs", methods=["POST"])
def add_song_to_queue():
    try:
        search = request.get_json().get("search")

        song = g.client.find(search=search)[:1]

        if song and song[0]:
            song = song[0]
            g.db.queue(song)
            resp = response(messages="Added new song to queue. {0}: {1} -- {2}".format(song.artist.name,song.name,song.album.name), status=201)
        else:
            resp = response(messages="No song was found, nothing to queue", status=200)

    except KeyError, e:
        resp = response(messages="Incomplete song information, cannot process request.", status=400)

    return resp

# Remove song from queue
@app.route("/queue/songs/<song_id>", methods=["DELETE"])
def remove_song_from_queue(song_id):

    song = g.db.find_in_queue(id=song_id)

    if song.count():
        song_title = song.next()["title"]
        g.db.remove_from_queue(id=song_id)
        resp = response(messages="Removed {0} from the queue".format(song_title), status=200)
    else:
        resp = response(messages="Song could not be found in queue, cannot remove.", status=200)

    return resp

""" Grooveshark Api Exposed """

# Search Grooveshark for songs/playlists/albums
@app.route("/gs/search/song", methods=["POST"])
def search_grooveshark_songs():

    term = request.get_json().get("search")
    songs = g.client.find(search=term, max_results=20)

    if songs:

        resp = response(messages="Successfully retrieved songs from Grooveshark.", data=[extract_song_data(song) for song in songs], status=200)
    else:
        resp = response(messages="No results found for: {0}".format(term), status=404)

    return resp

@app.route("/gs/search/album/<term>", methods=["GET"])
def search_grooveshark_albums():
    pass

@app.route("/gs/search/playlist/<term>", methods=["GET"])
def search_grooveshark_playlists():
    pass