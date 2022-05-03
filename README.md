# SmartShuffle
An improved shuffling algorithm for Spotify playlists. The intention is that another factor will be taken into consideration when shuffling songs, in addition to artist name: transition from genre to genre on the playlist. The application is currently in it's earliest stages, however, the intention is to ultimately find a way to map integers to genre types and sort according to these integer values.

## To Run The Programs
1. smartshuffle.py and spotifyshuffle.py were prototypes of the final program I developed. These programs do not connect to the Spotipy library and have hardcoded data.
2. spotifydanceability.py does require the use of the Spotipy library. Here is how to set up the environment to run the program:
a. Install anaconda. Create a new Conda environment via the "Environments" navigator. I installed Python 3.10.4 to my environment.
b. Open up the terminal view of your Conda environment by clicking the green triangle. Once here, type the following commands one at a time: "conda activate 'your_environment_name'", "pip install spotipy", "pip install pandas", "pip install jinja2"
c. Open up the codebase in VSCode and select your newly created Conda environment for your Python interpreter.
d. Lastly, you'll need a client id, client secret id, and playlist id. To obtain a client id and client secret id, create an account here: https://developer.spotify.com/dashboard/login and then create an application by clicking "Create an App" to obtain these keys. 
e. In regards to a playlist id, I have two different ids that I have commented out in my code that you can connect to. Just don't input the quotation marks on the command line. To connect to your own playlist, follow these instructions: https://clients.caster.fm/knowledgebase/110/How-to-find-Spotify-playlist-ID.html
