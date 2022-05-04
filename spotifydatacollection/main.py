#Importing required modules
from distutils.log import debug
from posixpath import split
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template, request, send_from_directory
from flask import Markup
import gunicorn
import os
from flask import Flask,render_template,request,redirect


#defining flask name
app = Flask(__name__)

#Defining favicon (Still in development of fixing server issues with heroku displaying corrrect info)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'logoo.png', mimetype='image/png') 

#Defining home page(form.html)
@app.route('/')
def form():
    return render_template('index.html')
@app.route('/artistinfo')
def artistname():
    return render_template('artist.html')
@app.route('/playlist')
def playlist():
    return render_template('playlist.html')


#requesting form for playlist link
@app.route('/songdata', methods = ['POST', 'GET'])
def repo():
    if request.method == 'POST':
        playlistlink = request.form['playlistlink']
        playlistlinkparsed = playlistlink.split("/")[-1].split("?")[0]

        return redirect(f"/users/{playlistlinkparsed}")

#Defining repo function for returning data
@app.route('/users/<playlistlinkparsed>')
def users(playlistlinkparsed):
    #Initializing spotipy API and IDS
    client_credentials_manager = SpotifyClientCredentials(client_id='xxxxxx', client_secret='xxxxxxxxx')
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    #interating through playlist tracks
    for track in sp.playlist_tracks(playlistlinkparsed)["items"]:
        artist_uri = track["track"]["artists"][0]["uri"]
        track_name = track["track"]["name"]


        #Saving for later :)
        artist_info = sp.artist(artist_uri)

        #defining data picking up
        genres = artist_info["genres"]
        name = track["track"]["artists"][0]["name"]
        clout = artist_info["popularity"]
        songnum = len(track["track"]["album"]["name"])
        embed_spotify = f"https://open.spotify.com/embed/playlist/{playlistlinkparsed}?utm_source=generator" 

    return render_template("songdata.html", infodata = Markup(f'<b>Genere: </b>{genres}<br><b>Track Name: </b>{track_name}<br><b>Arist Name: </b>{name}<br><b>Artist Popularity: </b>{clout}<br><b>Number of songs: </b>{songnum}<br><iframe src="{embed_spotify}" width="400" height="480" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>')
)





#Running Flask
if __name__ == "__main__":
    app.run(debug=True)