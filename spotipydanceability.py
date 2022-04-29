from hashlib import new
from math import floor
import random
from numpy import format_float_scientific
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

######################################################################################################

# Method that uses the fisher-yates algorithm to shuffle the contents of a dataframe
# https://www.geeksforgeeks.org/shuffle-a-given-array-using-fisher-yates-shuffle-algorithm/ 
def randomize (df):
    n = len(df)
    # Start from the last element and swap one by one. We don't
    # need to run for the first element that's why i > 0
    for i in range(n-1,0,-1):
        # Pick a random index from 0 to i; have the if/else so it doesn't accidentally go out of range
        if i < n-1:
            j = random.randint(0,i+1)
        else:
            j = random.randint(0, i)
        # Swap df[i] with the element at random index, df[j]
        temp = df.iloc[i]
        df.iloc[i] = df.iloc[j]
        df.iloc[j] = temp

    return df

# Method to implement the Spotify shuffle algorithm
def spotify_shuffle(df, artistList):
    # create dictionary to map: track_id -> [new index in df (random offset)]         
    newIndices = {}
    keys = []
 
    for artist in artistList:
        artistDf = df[df['artist'] == artist].reset_index(drop=True) 
        numSongs = len(artistDf)

        #iterate through all the songs in the df for our given artist
        for i in range(numSongs):
            current_trackID = artistDf.at[i, "track_id"]
            newIndices[str(current_trackID)] = float(i/numSongs) #set the new index (aka random offset variable)
        
        # Generate initial random offset (io) and add to each song for a specific artist in v
        io = random.uniform(0, (1/numSongs))
        #update the index in the dictionary for each number
        for i in range(numSongs):
            current_trackID = artistDf.at[i, "track_id"]
            #add initial offset to current index
            newIndices[current_trackID] += io 
            # Generate another random offset and add to each value
            randoffset = random.uniform((-1/10)*numSongs, (1/10)*numSongs)
            newIndices[current_trackID] += randoffset
        
    # create new dataframe for values in the order of their new indices
    column_names = ["danceability", "artist", "album", "track_name", "track_id"]
    newDf = pd.DataFrame(columns=column_names)
    for key in newIndices.keys():
        newIndex = newIndices[key]
        track_id = key
        newRow = df.loc[df['track_id'] == track_id]
        rowValues = getRowInfo(newRow)
        newDf.loc[newIndex] = rowValues[0], rowValues[1], rowValues[2], rowValues[3], rowValues[4]
        #reindex the df so that all indices are integers again
        newDf = newDf.sort_index().reset_index(drop=True) 
    return newDf

#method to extract the danceability, artist, album, track_name, and track_id characteristics from a row
def getRowInfo(row):
    #we need .split()[1] because without it, the index from newRow is tied to the column value
    #e.g. "4      0.418" for dancecability
    d = str(row['danceability']).split(" ", 1)
    danceability = float(str(d[1]).split("\n", 1)[0].strip()) if len(d) > 1 else float(str(d[0]).split("\n", 1)[0].strip())

    art = str(row['artist'])
    artist = str(art.split(" ", 1)[1]).split("\n", 1)[0].strip() if art[0].isdigit() else art

    alb = str(row['album'])
    album = str(alb.split(" ", 1)[1]).split("\n", 1)[0].strip() if alb[0].isdigit() else alb

    t_n = str(row['track_name'])
    track_name = str(t_n.split(" ", 1)[1]).split("\n", 1)[0].strip() if t_n[0].isdigit() else t_n

    t_i = str(row['track_id']).split()
    track_id = t_i[1] if len(t_i) > 1 else t_i[0]
    return(danceability, artist, album, track_name, track_id)

# Apply the Smart Shuffle Algorithm to the playlist that was previously shuffled by fisher-yates.
def smartShuffle(df, danceabilityList):
    #find the highest danceability metric contained in the list
    highestLevel = max(danceabilityList)
    lowestLevel  = min(danceabilityList)

    #maxGenreDifference defines the threshold of when we decide to smart shuffle
    #this is the maximum difference between genres of two neighboring songs.
    maxGenreDifference = (highestLevel-lowestLevel)/2.0

    """
    LOGIC OF THE WHILE LOOP BELOW:

    While length of dataframe is greater than 0:
        Find the current front of the dataframe, or index 0.
        If the len(dataFrame) > 1, then get the second element in the dataframe.

        We need the first and second elements in this list so that we can compare the difference between genre types.

        Determine the difference between genre types. If the difference between these values is smaller than the
        maximum allowed difference between genres, print the first song from the front of the dataframe, remove it, and continue.

        If not, implement the smart shuffle.

        Smart shuffle:
        -create a copy of the dataframe elements and remove the front two values (current song, next song)
        -set the random range parameters for the lower index and upper index.
            -lower: current genre integer value - maximum genre integer value; if this is less than 0, set to 1
            -upper: current genre integer value + maximum genre integer value; if this is greater than the highest genre level
            stored in the dataframe, set this value to the highest genre level
        -randomly generate a genre integer value in between lower and upper
        -find a song in the copy of the dataframe that has the randomly generated genre value. If a song
        cannot be found, then randomly generate a new genre integer value until a song in the appropriate threshold can be found.
    """
    #create list of data to build so we can add all data to dataframe at once at the end
    data = []
    while len(df) > 0:
        #get danceability attribute from the first row in df
        currentDanceability = df.at[0, "danceability"]
        nextDanceability = 0.0
        if len(df) > 1:
            nextDanceability = df.at[1, "danceability"]
        else:
            #get the danceability, album, artist, etc. values from the row we just got
            rowValues = getRowInfo(df.iloc[0])
            data.append([rowValues[0], rowValues[1], rowValues[2], rowValues[3], rowValues[4]])
            df = df.drop(index=0)
            df = df.reset_index(drop=True)
            break

        #check difference in genres in current and next song
        genreDifference = abs(nextDanceability-currentDanceability)

        #If the current difference between genres isn't larger than the maximum
        #difference in genres, then pop off the current song from the list and
        #go back to the top of the loop.
        if genreDifference <= maxGenreDifference:
            #pop off the current song from front of list
            rowValues = getRowInfo(df.iloc[0])
            data.append([rowValues[0], rowValues[1], rowValues[2], rowValues[3], rowValues[4]])
            df = df.drop(index=0)
            df = df.reset_index(drop=True)
            continue

        #SMART SHUFFLE BEGINS
        else:
            #create deep copy of dataframe so we can search through the rest of the list of songs
            #pop off the first two songs because we don't want the "currentSong" or "nextSong" to be included in this
            temp = df.copy(deep=True)
            temp.drop(index=0)
            temp = temp.reset_index(drop=True)
            temp.drop(index=0)
            temp = temp.reset_index(drop=True)
            
            if len(temp) == 0:
                continue

            #set the random range parameters 
            lowerIndex = (currentDanceability-maxGenreDifference) if (currentDanceability-maxGenreDifference) > lowestLevel  else lowestLevel
            upperIndex = (currentDanceability+maxGenreDifference) if (currentDanceability+maxGenreDifference) < highestLevel else highestLevel

            #return 1 random row with the desired danceability level
            newRow = temp.query("danceability > @lowerIndex and danceability < @upperIndex").sample(n=1)

            #if temp dataframe doesn't have a column with a danceability value in the correct range, randomly choose a row 
            if newRow.empty:
                newRow = temp.sample()

            #get the danceability, album, artist, etc. values from the row we just got
            rowValues = getRowInfo(newRow)
        
            #get the index of the record we identified in the df so we can remove it from its current index there
            indices = df.index[(df['danceability']== rowValues[0]) & (df['artist']==rowValues[1]) & (df['album']==rowValues[2]) & (df['track_name']==rowValues[3]) & (df['track_id']==rowValues[4])].tolist()
            removeIndex = indices[0]

            #remove the record from current position in df; index+2 because index came from temp and size of temp is 2 smaller than df
            df = df.drop(index=removeIndex)
            df = df.reset_index(drop=True) 

            #the song we just found is the new "next song", so insert it inbetween the first couple songs
            newIndex = 0.50
            df.loc[newIndex] =  rowValues[0], rowValues[1], rowValues[2], rowValues[3], rowValues[4]
            #reindex the df so that all indices are integers again
            df = df.sort_index().reset_index(drop=True) 

            #pop off the current song from front of list
            rowValues = getRowInfo(df.iloc[0])
            data.append([rowValues[0], rowValues[1], rowValues[2], rowValues[3], rowValues[4]])
            df = df.drop(index=0)
            df = df.reset_index(drop=True) 

    newDf = pd.DataFrame(data, columns=["danceability", "artist", "album", "track_name", "track_id"])
    return (newDf, maxGenreDifference)

#code from  https://stackoverflow.com/questions/39086287/spotipy-how-to-read-more-than-100-tracks-from-a-playlist
def get_playlist_tracks(username,playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

#code from: https://www.linkedin.com/pulse/extracting-your-fav-playlist-info-spotifys-api-samantha-jones/
def call_playlist(creator, playlist_id):
    #step1
    playlist_features_list = ["danceability"]
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    #step2:
    playlist = get_playlist_tracks(creator, playlist_id)
    danceabilityMetrics = []
    allArtists = []
    for track in playlist:
        # Create empty dict
        playlist_features = {}
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]
        
        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        playlist_features["danceability"] = audio_features["danceability"]
        danceabilityMetrics.append(playlist_features["danceability"])
        if (playlist_features["artist"] not in allArtists):
            allArtists.append(playlist_features["artist"])

        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)

    #Step 3
    return (playlist_df, danceabilityMetrics, allArtists)

input_client_id = input("\nInput your client id: ")
input_client_secret = input("Input your client secret: ")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=input_client_id,
                                               client_secret=input_client_secret,
                                               redirect_uri="http://localhost:8888/callback",
                                             scope="user-library-read"))
#playlistID = "2Yct0n6fEv45vwi3V4eagi"#Long playlist - 767 songs
#playlistID = "69U96lggXAlr8D8IDetdJ3" #short playlist - 15 songs
playlistID = input("Input your playlist id: ")

#this allows us to print all the lines in our dataframes
pd.set_option('display.max_rows', None)

# songs[0] is df, songs[1] is danceabilitylist, songs[2] is artistlist
songs = call_playlist("spotify",playlistID)
print("\n\nPlaylist Before Shuffling: \n", songs[0])
#first shuffle
df = randomize(songs[0])
print("\nPlaylist After Applying Fisher-Yates: \n", df)

#second shuffle
spotifyShdf = spotify_shuffle(df, songs[2])
print("\nPlaylist After Applying Spotify Shuffle: \n", spotifyShdf)

#third shuffle
smartShDf = smartShuffle(spotifyShdf, songs[1])
print("\nPlaylist Order - Spotify Shuffle and then Smart Shuffle\nCloseness threshold: current and next song danceability integers within {} of each other. \n {}".format(smartShDf[1], smartShDf[0]))
