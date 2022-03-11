from hashlib import new
import random

#levels = [5, 3, 1, 2, 4]
levels = [5, 1, 4, 2, 3]

highestLevel = 5
diff = highestLevel//2

#for i in range(len(levels)):
while len(levels) > 0:
    print("LIST AT START: ", levels)
    currentSong = levels[0]
    if 2 != len(levels):
        nextSong = levels[1]
    else:
        print(levels[0])
        levels.pop(0)
        break

    #check difference in levels in current and next song
    newdiff = abs(nextSong-currentSong)
    print("newdiff: ", newdiff)
    if newdiff <= diff:
        #pop off the current song from front of list
        print(levels[0])
        levels.pop(0)
        continue

    #this is where the smart shuffle algorithm happens
    else:
        #set the random range parameters
        lowerIndex = (currentSong-diff) if (currentSong-diff) >= 0  else 1
        upperIndex = (currentSong+diff) if (currentSong+diff) <= highestLevel else highestLevel

        #generate random level - gets the level of a song to grab
        newNextSong = random.randint(lowerIndex, upperIndex)
        print("list before newSong: ", levels)
        #print("newNextSong: ", newNextSong)

        #find a song of this level in the list
        index = levels.index(newNextSong) if newNextSong in levels[1:] else -1 

        while index == -1 :
                newNextSong = random.randint(lowerIndex, upperIndex)
                index = levels.index(newNextSong) if newNextSong in levels[1:] else -1 

        print("newNextSong: ", newNextSong)
        levels.insert(1, levels[index])
        print("list before: ", levels)
        levels.pop(index+1)
        print("list after: ", levels)
        print(levels[0])
        levels.pop(0)
print(levels[0])
levels.pop(0)

