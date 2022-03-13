import random
#Emily Wilbourn
#implement the spotify shuffle algorithm
#this algorithm is outlined at: https://codegolf.stackexchange.com/questions/198094/spotify-shuffle-music-playlist-shuffle-algorithm?newreg=e4fef50fb1a14427a99bbafa4e520390

######################################################################################################

artists = [[['A', 1], ['AA',2], ['AAA',1]], [['B',4]], [['C', 2], ['CC',3]], [['D',5]], [['E',4], ['EE',3], ['EEE',4], ['EEEE',3]]]

# first, shuffle items in each group
# use fisher-yates
# https://www.geeksforgeeks.org/shuffle-a-given-array-using-fisher-yates-shuffle-algorithm/ 
def randomize (arr):
    n = len(arr)
    # Start from the last element and swap one by one. We don't
    # need to run for the first element that's why i > 0
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
for sublist in artists:
    n = len(sublist)
    for i in range(n):
        v[sublist[i][0]] = []
        v[sublist[i][0]].append(i/n)           # append random offset variable
        v[sublist[i][0]].append(sublist[i][1]) # append the genre type

    # Generate initial random offset (io) and add to each value in v
    io = random.uniform(0, (1/n))
    for i in range(n):
        v[sublist[i][0]][0] += io
        # Generate another random offset and add to each value
        randoffset = random.uniform((-1/10)*n, (1/10)*n)
        v[sublist[i][0]][0] += randoffset
    
# sort all items by positional values
# https://stackabuse.com/how-to-sort-dictionary-by-value-in-python/

sorted_dict = {}
sorted_keys = sorted(v, key=v.get)  

for key in sorted_keys:
    sorted_dict[key] = v[key]

for key in sorted_dict.keys():
    print(key)

