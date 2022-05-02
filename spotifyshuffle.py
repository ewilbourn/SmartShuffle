import random
import copy 
#Emily Wilbourn
#implement the spotify shuffle algorithm
#this algorithm is outlined at: https://codegolf.stackexchange.com/questions/198094/spotify-shuffle-music-playlist-shuffle-algorithm?newreg=e4fef50fb1a14427a99bbafa4e520390

######################################################################################################

artists = [[['A', 5], ['AA',2], ['AAA',7]], [['B',9], ['B', 6]], [['C', 3], ['CC',7], ['CC',1]], [['D',5]], [['E',2], ['EE',7], ['EEE',1], ['EEEE',2]]]

print("\n\nPlaylist Order - Before Shuffle")
for artist in artists:
        for song in artist:
            print("['{}', {}]".format(song[0], song[1]))

# first, shuffle items in each group
# use fisher-yates
# https://www.geeksforgeeks.org/shuffle-a-given-array-using-fisher-yates-shuffle-algorithm/ 
def randomize (arr):
    n = len(arr)
    # Start from the last element and swap one by one. We don't

    for i in range(n-1,0,-1):
        # Pick a random index from 0 to i
        j = random.uniform(0,i+1)
 
        # Swap arr[i] with the element at random index
        arr[i],arr[j] = arr[j],arr[i]
    return arr

# MAIN ALGORITHM

# Initialize positional value dictionary v
# In this array, map: Artist name -> [random offset, genre type]
# When shuffling the artists, we NEED to preserve the genre.
v = {}
for artist in artists:
    numSongs = len(artist)

    #iterate through all songs and initialize our dictionary entries
    #add the random offset variable to be the first in the list of values for a key value; then append the genre type
    for i in range(numSongs):
        v[artist[i][0]] = []
        v[artist[i][0]].append(i/numSongs)           # append random offset variable
        v[artist[i][0]].append(artist[i][1]) # append the genre type

    # Generate initial random offset (io) and add to each song for a specific artist in v
    io = random.uniform(0, (1/numSongs))
    for i in range(numSongs):
        v[artist[i][0]][0] += io
        # Generate another random offset and add to each value
        randoffset = random.uniform((-1/10)*numSongs, (1/10)*numSongs)
        v[artist[i][0]][0] += randoffset
    
# sort all items by positional values
# https://stackabuse.com/how-to-sort-dictionary-by-value-in-python/

sorted_dict = {}
sorted_keys = sorted(v, key=v.get)  

for key in sorted_keys:
    sorted_dict[key] = v[key]

print("\nPlaylist Order - Spotify Shuffle")
for key in sorted_dict.keys():
    print("['{}', {}]".format(key, sorted_dict[key][1]))

###########################################################################################3

# Apply the Smart Shuffle Algorithm to the playlist that was previously shuffled by artist name.

genres = []
# Create a list of all integers representing genre so we can find the highest integer.
for artist in artists:
    for song in artist:
        genres.append(song[1])

highestLevel = max(genres)
lowestLevel = min(genres)
#maxGenreDifference defines the threshold of when we decide to smart shuffle
#this is the maximum difference between genres of two neighboring songs.
maxGenreDifference = (highestLevel-lowestLevel)//2

# Create a list of lists with [artist, genre]
newList = []
for key in sorted_keys:
    songs = []
    songs.append(key)
    songs.append(sorted_dict[key][1])
    newList.append(songs)

"""
LOGIC OF THE WHILE LOOP BELOW:

While length of list of [artist,genre] is greater than 0:
    Find the current front of the list of [artist,genre] lists
    If the len(list) > 1, then get the second element in the list of [artist,genre].

    We need the first and second elements in this list so that we can compare the difference between genre types.

    Determine the difference between genre types. If the difference between these values is smallest than the
    maximum allowed difference between genres, pop the first song from the front of the list and continue.

    If not, implement the smart shuffle.

    Smart shuffle:
    -create a copy of the list of [artist, genre] elements and remove the front two values (current song, next song)
    -set the random range parameters for the lower index and upper index.
        -lower: current genre integer value - maximum genre integer value; if this is less than 0, set to 1
        -upper: current genre integer value + maximum genre integer value; if this is greater than the highest genre level
        stored in the list, set this value to the highest genre level
    -randomly generate a genre integer value in between lower and upper
    -find a song in the copy of the list of [artist, genre] that has the randomly generated genre value. If a song
    cannot be found, then randomly generate a new genre integer value until a song in the appropriate threshold can be found.


"""
print("\nPlaylist Order - Spotify Shuffle and then Smart Shuffle\nCloseness threshold: current and next song danceability integers within {} of each other".format(maxGenreDifference))
while len(newList) > 3:
    currentSongGenre = newList[0][1]
    nextSongGenre = newList[1][1]

    #check difference in genres in current and next song
    genreDifference = abs(nextSongGenre-currentSongGenre)

    #If the current difference between genres isn't larger than the maximum
    #difference in genres, then pop off the current song from the list and
    #go back to the top of the loop.
    if genreDifference <= maxGenreDifference:
        #pop off the current song from front of list
        print(newList[0])
        newList.pop(0)
        continue

    #SMART SHUFFLE BEGINS
    else:
        #create temp so we can search through the rest of the list of songs
        #pop off the first two songs because we don't want the "currentSong" or "nextSong" to be included in this
        temp = copy.deepcopy(newList)
        temp.pop(0)
        temp.pop(0)
        if len(temp) == 0:
                continue
        #set the random range parameters 
        lowerIndex = (currentSongGenre-maxGenreDifference) if (currentSongGenre-maxGenreDifference) >= lowestLevel  else lowestLevel
        upperIndex = (currentSongGenre+maxGenreDifference) if (currentSongGenre+maxGenreDifference) <= highestLevel else highestLevel

        #generate random level - gets the level of a song to grab
        valuesInRange = list(temp.index(x) for x in temp if lowerIndex <= x[1] <= upperIndex)
        #all(ele >= lowerIndex and ele <= upperIndex for ele in temp)
        if len(valuesInRange) > 0:
            index = random.randint(0, len(valuesInRange))
        else:
            index = random.randint(0, len(temp))

        newList.insert(1, newList[index+2])
        newList.pop(index+3)
        print(newList[0])
        newList.pop(0)

print(newList[0])
newList.pop(0)
print(newList[0])
newList.pop(0)
print(newList[0], "\n")
newList.pop(0)



