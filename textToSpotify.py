'''
textToSpotify
Approach : 
Text file with song names and artists
Read file and create list of song names and artists 
Get authentication token for Spotify API
Use auth token to send in queries to API 
Use the list from text file and get IDs/URLs for each song in list if available
Create a playlist from the IDs/URLs 
Provide the created playlist to User 
'''

import pathlib
import sys
import spotipy.util as util
import requests
import json



#Gets filename from user
#If user provides text file without .txt extension
#.txt extension is added to the filename
def getFileName():
    filename = input('Enter the text filename (.txt) which contains list of songs: ')
    if not(filename.endswith(".txt")):
        filename = filename + ".txt"
    return filename


'''
#Get track names from the text file
#Format for the text file: File should contains list of all songs on different lines 
#PlaylistTextFile.txt sample file with 10 songs provided for reference 
#If file is not found then program will stop running and prompt user to try again 
'''
def getTracksfromFile():
    filename = getFileName()
    
    file = pathlib.Path(filename)
    tracks = []
    if file.exists ():
        with open(filename) as f:
            for line in f:
                line = line.strip()
                tracks.append(line)
        return tracks
    else:
        sys.exit(filename  + " file not found, try keeping the file in same directory")


'''
Get access token which will be used for further requests
'''
def getAccessToken():
    redirect_uri = 'http://localhost:7777/callback'
    scope = 'user-read-private user-read-email playlist-read-collaborative playlist-modify-public playlist-modify-private'
    SPOTIPY_CLIENT_ID  = '01124143b207431fa629a5ac2f1784be'
    SPOTIPY_CLIENT_SECRET  = '473a32a70cab42c78d246ba995e681ce'
    token = util.prompt_for_user_token(scope=scope, 
                                   client_id=SPOTIPY_CLIENT_ID,   
                                   client_secret=SPOTIPY_CLIENT_SECRET,     
                                   redirect_uri=redirect_uri)

    return token


'''
Get header
'''
def getHeader(access_token):
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {token}'.format(token=access_token),
    }   
    return headers    
    
'''
get User id 
'''
def getUserID(headers):
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    user_profile = response.json()
    user_id = user_profile['id']
    #print('User ID' + str(user_id))
    return user_id


'''
Get playlist name from User
'''
def getPlaylistName():
    playListName = input("Enter the name for playlist: ")
    if playListName == "":
        print("Setting the name of playlist as default, TextToPlaylist")
        playListName = "TextToPlaylist"
    return playListName


'''
Get playlist description name from User
'''
def playlistDescription():
    playlist_description = input("Enter description for playlist: ")
    if playlist_description == "":
        print("Setting the description of playlist as default")
        playlist_description = "Playlist created from list of Text provided"
    return playlist_description

'''
create playlist
'''
def createPlaylist(user_id, headers):
#Update code to get user defined name and description    
    playlist_name = getPlaylistName()
    playlist_description = playlistDescription()

    data = {
    "name": playlist_name,
    "description": playlist_description
    }

    data = json.dumps(data)

    response = requests.post('https://api.spotify.com/v1/users/' + user_id + '/playlists', headers=headers, data=data)
    playlist_json = response.json()
    playlist_id = playlist_json['id']
    return playlist_id


'''
Get track URIs
Search spotify API for all the URIs of tracks and create a list to provide
for creation of playlist
'''
#create id list from the list of tracks 
def GetURIs(tracks, header):
    
    SEARCH_BASE_URL = 'https://api.spotify.com/v1/search?'
    track_URIs = []

    for track_title in tracks:
        if track_title == "":
            continue
        id_request_url = SEARCH_BASE_URL + 'q=' + track_title + '&type=' + 'track'
        id_request = requests.get(id_request_url, headers=header) 
        json_id = id_request.json()
        items = json_id['tracks']['items']
        if len(items) > 0:
            track = items[0]
            print(track['name'])
            track_URIs.append(track['uri'])

    #print(track_URIs)
    return track_URIs


'''
Get URI String
Reformat the URI List so that its comma separated string which 
can be passed through for playlist creation function 
'''
def GetURIString(trackURIs):
    track_URIs = trackURIs
    track_string_for_query = ""

    for uri in track_URIs:
        track_string_for_query += uri + ","
    
    track_string_for_query = track_string_for_query[:-1]
    return track_string_for_query


'''
add tracks to playlist
'''
def addTracksToPlaylist( playlist_id, trackURIString, headers):
    response = requests.get('https://api.spotify.com/v1/playlists/' + playlist_id, headers=headers)
    playlist_json = response.json()
    playlist_id = playlist_json['id']
    playlist_name = playlist_json['name']
    
    params = (
        ('uris', trackURIString ),
    )
    response = requests.post('https://api.spotify.com/v1/playlists/'+ str(playlist_id) + '/tracks', headers=headers, params=params)
    return response.status_code


def main():
    tracks = getTracksfromFile()
    access_token = getAccessToken()
    header = getHeader(access_token)
    user_id = getUserID(header)
    playlist_id = createPlaylist(user_id, header)
    trackURIs = GetURIs(tracks, header)
    trackURIString = GetURIString(trackURIs)
    status = addTracksToPlaylist( playlist_id, trackURIString, header)
    
    if (status == 201):
        print("Playlist has been created")
        playlist_url = 'https://open.spotify.com/playlist/' + playlist_id
        print("You can access your playlist at: " + playlist_url)
    
if __name__ == '__main__':
    main()
