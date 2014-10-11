from api import api_v1 as app
from flask import request

# Get song queue list
@app.route("/queue/songs", methods=['GET'])
def index():
    return "This is a list of songs"

# Find song by title
@app.route("/queue/songs/<title>", methods=['GET'])
def show(title):
    return "You searched for song with title '{0}'".format(title)

# Add song to queue
@app.route("/queue/songs", methods=['POST'])
def create():
    song = request.get_json().get("song", "")
    return "Added new song to queue. '{0}'".format(song)

# Remove song from queue by title
@app.route("/queue/songs/<title>", methods=['DELETE'])
def destroy(title):
    return "Deleting song with title '{0}'".format(title)