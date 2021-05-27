# TextToSpotify

Program for creating a Spotify playlist from a text file 

Why ? : Some of the playlists on internet are usually listed out in text format, instead of searching each song manually and creating a playlist. We can use this Program for creating the spotify playlist programmatically

## Dependencies

Following libraries need to be installed  
* spotipy
* requests

## Working logic

Approach : 

* Read file name from user 
* Read file and create list of song names and artists 
* Get authentication token for Spotify Web API
* Create a header with authentication token for all requests
* Create a playlist in Spotify after taking playlist name and description from user
* Use the list from text file and get IDs/URIs for each song in list if available
* Create a URI string from the list of URIs for the song
* Create a playlist by adding tracks from the file from the URI string
* Provide the created playlist URL to User 

### Example 

When we run the program, User will be prompted to enter the name of text file

[SamplePlaylist.txt ](https://raw.githubusercontent.com/maxyodedara5/TextToSpotify/master/SamplePlaylist.txt)

When filename is provided, a browser window should popup and ask you for authentication which in turn will provide an access token to be used for further requests


![Access Image ](AccessSpotify.png)

Then we provide Playlist name and description which will be reflected in Spotify
While making the example I set
* Playlist name : textToSpotify
* Playlist description : Songs we listen on repeat some of my favourites

After giving the playlist details, program will Search on Spotify for the listed tracks and if found will list them out in your terminal and then add them to your playlist

Created playlist link [textToSpotify ](https://open.spotify.com/playlist/3jsD7ExjSnCFBlJtSBPLBR)

Once done will print out a link for your playlist, the playlist should be present in your Spotify account to listen anytime

## License

This project is licensed under the [MIT License](LICENSE).

## To do items

* Update working to have command line args 
* Create a standalone python project
* Speed improvements
