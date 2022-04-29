from hashlib import new
import random
import copy

#levels = [5, 3, 1, 2, 4]
#levels = [1, 5, 4, 2, 3]
#levels = [5, 1, 4, 1, 5, 2, 4, 1, 3]
levels = [6, 1, 5, 6, 2, 3, 6, 4, 2, 1, 3]
#levels = [10, 1, 8, 9, 2, 7, 4, 6, 3, 5]
print("\nGenre Order - Before Applying Smart Shuffle")
for i in range(0, len(levels)):
     print(levels[i])

highestLevel = max(levels)
lowestLevel = min(levels)
diff = (highestLevel-lowestLevel)//2
print("\nGenre Order - After Applying Smart Shuffle\nCloseness threshold: each pair of integers within {} of each other".format(diff))
while len(levels) > 3:
    currentSong = levels[0]
    if 2 != len(levels):
        nextSong = levels[1]
    else:
        print(levels[0])
        levels.pop(0)
        break

    #check difference in levels in current and next song
    newdiff = abs(nextSong-currentSong)
    if newdiff <= diff:
        #pop off the current song from front of list
        print(levels[0])
        levels.pop(0)
        continue

    #this is where the smart shuffle algorithm happens
    else:
        #create temp so we can search through 
        temp = copy.deepcopy(levels)
        temp.pop(0)
        temp.pop(0)

        #set the random range parameters 
        lowerIndex = (currentSong-diff) if (currentSong-diff) >= lowestLevel  else lowestLevel
        upperIndex = (currentSong+diff) if (currentSong+diff) <= highestLevel else highestLevel

        #generate random level - gets the level of a song to grab
        valuesInRange = list(temp.index(x) for x in temp if lowerIndex <= x <= upperIndex)
        #all(ele >= lowerIndex and ele <= upperIndex for ele in temp)
        if len(valuesInRange) > 0:
            index = random.randint(0, len(valuesInRange))
        else:
            index = random.randint(0, len(temp))

        levels.insert(1, levels[index+2])
        levels.pop(index+3)
        print(levels[0])
        levels.pop(0)
print(levels[0])
levels.pop(0)
print(levels[0])
levels.pop(0)
print(levels[0], "\n")
levels.pop(0)

