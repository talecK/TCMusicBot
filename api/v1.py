from api import api_v1 as app
from api.response import response
from flask import request, g, jsonify
from data.music import MusicDataAccess, extract_song_data
from core.cli.music import MusicClient
from core.commands.music import MusicCommand
from core.commands.server import ServerCommand
from bson.json_util import dumps
import json

@app.before_request
def before_request():
    g.db = MusicDataAccess()
    g.client = MusicClient()
    g.music_cmd = MusicCommand()
    g.server_cmd = ServerCommand()

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

    song = g.db.find_in_queue(id=id)

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

""" Server interface Api """

# TODO: Add server stats document to mongodb.
#      "server_stats":{
#                       "currently_playing":"song obj",
#                       "status": ['polling', 'playing'],
#                       "volume": 100,
#                       "number_of_songs_played": 1000
#                     }
#

# TODO: Change the playing volume of the music server via api.
@app.route("/server/volume", methods=["POST"])
def change_volume():
    try:
        volume = request.get_json().get("volume")
        g.server_cmd.change_volume(volume)
        resp = response(messages="Volume updated successfully.", status=200)
    except Exception as e:
        resp = response(messages="There was an error updating the volume. "+str(e), status=500)

    return resp

# TODO: Show the current playing song.
@app.route("/server/currently_playing", methods=["GET"])
def get_currently_playing():
    song = g.server_data.get_currently_playing()

    if song:
        resp = response(messages="Current playing song retrieved.", data={"currently_playing": song}, status=200)
    else:
        resp = response(messages="No song is currently playing.", status=200)

    return resp

""" Grooveshark Api Exposed """

# Search Grooveshark for songs/playlists/albums
@app.route("/gs/search/song", methods=["POST"])
def search_grooveshark_songs():

    term = request.get_json().get("search")
    songs = g.client.find(search=term, max_results=10)

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

@app.route("/gs/radio/list/<genre>", methods=["GET"])
def search_grooveshark_radio(genre):

    # genre = request.get_json().get("genre")
    songs = g.client.radio(search=genre)

    if songs:

        resp = response(messages="Successfully retrieved songs from Grooveshark.", data=songs, status=200)
    else:
        resp = response(messages="No results found for: {0}".format(genre), status=404)

    return resp
