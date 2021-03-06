# TextToSpotify

Program for creating a Spotify playlist from a text file 

Why ? : Some of the playlists on internet are usually listed out in text format, instead of searching each song manually and creating a playlist. We can use this Program for creating the spotify playlist programmatically

## CodeInPlace Final Project

This project was a submission for CodeInPlace Course a 5-week introductory online Python programming course based on material from the first half of Stanford’s introductory programming course, CS106A.  

The project is also displayed at [CodeInPlace's Public Showcase for projects](https://codeinplace.stanford.edu/2021/showcase/1240)

For more info about Code in Place you can take a look [here](https://codeinplace.stanford.edu/)

## Dependencies

Following libraries need to be installed  
* spotipy
* requests

## Dependencies
To get started, install spotipy and create an app on https://developers.spotify.com/.
Add your new ID, SECRETa and redirect URL to textToSpotify.py

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

If you haven't logged in to Spotify it will ask User to login and provide access to the application/program for updating playlist

![Access Image ](AccessSpotify.png)  

![Access Image ](SpotifyAppAccess.jpg)

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
