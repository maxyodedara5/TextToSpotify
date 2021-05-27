import pathlib
import sys
import spotipy.util as util
import requests
import json

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
Access token function will open up the browser and ask the User to 
provide access to thier spotify account so that playlists can be added 
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
Access token will be passed so that web api requests are authorized 
'''
def getHeader(access_token):
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {token}'.format(token=access_token),
    }   
    return headers    
    
'''
get User ID 
Headers passed which have access token so all requests are authorized
We need user ID to create a playlist for that user 
'''
def getUserID(headers):
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    if (response.status_code != 201 and response.status_code != 200):
        print("Error with getting User ID")
        print("Status code for getting User ID response" + str(response.status_code))
        print(response.text)
        sys.exit()
    user_profile = response.json()
    user_id = user_profile['id']
    #print('User ID' + str(user_id))
    return user_id


'''
Get playlist name from User
User Enters the playlist name which will be used 
If nothing is entered default text will be used TextToPlaylist
'''
def getPlaylistName():
    playListName = input("Enter the name for playlist: ")
    if playListName == "":
        print("Setting the name of playlist as default, TextToPlaylist")
        playListName = "TextToPlaylist"
    return playListName


'''
Get playlist description name from User
User Enters the playlist description which will be used 
If nothing is entered default description will be used
'''
def playlistDescription():
    playlist_description = input("Enter description for playlist: ")
    if playlist_description == "":
        print("Setting the description of playlist as default")
        playlist_description = "Playlist created from list of Text provided"
    return playlist_description

'''
Create playlist
Pass user ID to playlist is created for authenticated user 
Returns a playlist ID of created playlist so tracks can be added to
that playlist
'''
def createPlaylist(user_id, headers):    
    playlist_name = getPlaylistName()
    playlist_description = playlistDescription()

    data = {
    "name": playlist_name,
    "description": playlist_description
    }

    data = json.dumps(data)

    response = requests.post('https://api.spotify.com/v1/users/' + user_id + '/playlists', headers=headers, data=data)

    if response.status_code != 201 and response.status_code != 200:
        print("Error with creation of playlist")
        print("Status code for playlist creation response" + str(response.status_code))
        print(response.text)
        sys.exit()

    playlist_json = response.json()
    playlist_id = playlist_json['id']
    return playlist_id


'''
Get track URIs
Search spotify API for all the URIs of tracks and create a list to provide
for creation of playlist
'''
#Create id list from the list of tracks 
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
        print("Tracks being added to playlist")
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
Add tracks to playlist
Playlist ID and track URIs are passed along with headers 
Track URIs are list of all URIs of tracks which need to be added 
'''
def addTracksToPlaylist( playlist_id, trackURIString, headers):
    response = requests.get('https://api.spotify.com/v1/playlists/' + playlist_id, headers=headers)
    playlist_json = response.json()
    playlist_id = playlist_json['id']
    #playlist_name = playlist_json['name']
    
    params = (
        ('uris', trackURIString ),
    )
    response = requests.post('https://api.spotify.com/v1/playlists/'+ str(playlist_id) + '/tracks', headers=headers, params=params)
    if response.status_code != 201 and response.status_code != 200:
        print("Error with addition of tracks for playlist")
        print("Status code for addition of tracks response" + str(response.status_code))
        print(response.text)
        sys.exit()
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
    else:
        print("There was an error with addition of tracks in playlist")
    
if __name__ == '__main__':
    main()
