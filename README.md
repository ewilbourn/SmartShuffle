# SmartShuffle
An improved shuffling algorithm for Spotify playlists. The intention is that another factor will be taken into consideration when shuffling songs, in addition to artist name: transition from genre to genre on the playlist. The application is currently in it's earliest stages, however, the intention is to ultimately find a way to map integers to genre types and sort according to these integer values.

## To Run The Programs
1. smartshuffle.py and spotifyshuffle.py were prototypes of the final program I developed. These programs do not connect to the Spotipy library and have hardcoded data.
2. spotifydanceability.py does require the use of the Spotipy library. Here is how to set up the environment to run the program:
a. Install anaconda. Create a new Conda environment via the "Environments" navigator. I installed Python 3.10.4 to my environment.
b. Open up the terminal view of your Conda environment by clicking the green triangle. Once here, type the following commands one at a time: "conda activate 'your_environment_name'", "pip install spotipy", "pip install pandas"
c. Open up the codebase in VSCode and select your newly created Conda environment for your Python interpreter.
