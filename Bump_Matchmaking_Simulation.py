import random
import time
import math

# Auburn Simulation
# Limitation : Friends are randomly assigned so there won't be many common friends between people.

# Name key to friend array value
friendDatabase = {}

# Interests
differentInterests = ["Sports", "Music", "Greek Life", "Technology", "Politics", "Gym", "Photography", "Cooking", "Anime", "Gaming",
                      "Television", "Traveling", "Reading", "Fashion", "Drawing"]

# Array of bump arrays
bumps = []

# Dictionary of people looking for a bump, key is the name, value is the wait time
needBumpEF = {}
needBumpNF = {}

# Radius for looking
radius = 500

# Minimum U value
MIN_U = 7

# need types for what kind of bump
newFriend = "n"
existingFriend = "f"

database = {}

names = []

# Creating People
for i in range(5000000):
    name = "Person" + str(i + 1)
    names.append(name)



# Make bumps
for i in range(len(names) // 2):
    bumps.append([names[i], names[len(names) - i - 1]])

# Makes friend
for i in range(len(names)):
    if not names[i] in friendDatabase:
        friendDatabase[names[i]] = []

    numFriends = random.randint(25, 75)
    for j in range(numFriends):
        randomFriend = random.randint(0, len(names) - 1)
        while randomFriend == i or names[randomFriend] in friendDatabase[names[i]]:
            randomFriend = random.randint(0, len(names) - 1)

        friendDatabase[names[i]].append(names[randomFriend])
        if not names[randomFriend] in friendDatabase:
            friendDatabase[names[randomFriend]] = []
        friendDatabase[names[randomFriend]].append(names[i])


# Populate database
needType = 0
location = 1
interests = 2
friends = 3
timeWithBump = 4
timeUntilMatch = 5

for i in range(len(names)):
    if random.randint(0, 1) == 0:
        need = newFriend
    else:
        need = existingFriend

    numInterests = random.randint(5,8)
    interestArray = []
    for j in range(numInterests):
        while True:
            interest = differentInterests[random.randint(0,14)]
            if interest not in interestArray:
                interestArray.append(interest)
                break
    database[names[i]] = [need, i, interestArray, friendDatabase[names[i]]]



#Setting time for each Bump
for bump in bumps:
    timeWithBumpFrames = random.randint(59, 83)
    database[bump[0]].append(timeWithBumpFrames)
    database[bump[1]].append(timeWithBumpFrames)


# Maximizing user time by grading the bump between two people
def U(person1, person2):
    intOfCommonInterests = len([interest for interest in database[person1][interests] if interest in database[person2][interests]])
    intOfCommonFriends = len([friend for friend in database[person1][friends] if friend in database[person2][friends]])

    # U_ValueI = 1/2 + 1/2 * (math.tanh((intOfCommonInterests - 4) / 3))
    # U_ValueF = math.tanh(intOfCommonFriends / 9)

    return intOfCommonFriends * 2 + intOfCommonInterests



# Algorithm to looks for new bumps
def lookForNewBump(bump):
    print(bump[0] + " and " + bump[1] + " are looking for a bump.")

    for i in range(len(bump)):
        # Check if looking for new friend
        if database[bump[i]][needType] == newFriend:
            possibleBumps = []
            for person in needBumpNF:
                if person != bump[i] and person not in bump:
                    if abs(database[person][location] - database[bump[i]][location]) <= radius:
                        possibleBumps.append(person)

            if len(possibleBumps) == 0:
                needBumpNF[bump[i]] = 0
                print(bump[i] + " needs a bump!")
            else:
                chosenNF = possibleBumps[0]
                for j in range(1, len(possibleBumps)):
                    if U(bump[i], possibleBumps[j]) > U(bump[i], chosenNF):
                        chosenNF = possibleBumps[j]

                #Check to make sure you have at least things in common with your bump

                if U(bump[i], chosenNF) >= MIN_U:

                    newBump = [bump[i], chosenNF]

                    #Changing Need Type
                    database[bump[i]][needType] = existingFriend
                    database[chosenNF][needType] = existingFriend

                    # Setting Time Frames
                    timeWithBumpFrames = random.randint(59, 83)
                    database[bump[i]][timeWithBump] = timeWithBumpFrames
                    database[chosenNF][timeWithBump] = timeWithBumpFrames

                    bumps.append(newBump)
                    print(bump[i] + " and " + chosenNF + " are now bumped!")
                    commonInterests = [interest for interest in database[bump[i]][interests] if interest in database[chosenNF][interests]]
                    print("They have these common interests.")
                    print(commonInterests)
                    commonFriends = [friend for friend in database[bump[i]][friends] if friend in database[chosenNF][friends]]
                    print("They have these common friends.")
                    print(commonFriends)

                    print(chosenNF + " waited " + str(needBumpNF[chosenNF]) + " hours.")

                    # Remving chosenNF from the needBump queue
                    needBumpNF.pop(chosenNF)

                    print("They have " + str(database[bump[i]][timeWithBump]) + " hours together.")

                else:
                    needBumpNF[bump[i]] = 0
                    print(bump[i] + " needs a bump!")

        else:
            # Looking among existing friends
            possibleBumps = []
            for person in needBumpEF:
                if person != bump[i] and person not in bump:
                    if person in friendDatabase[bump[i]]:
                        possibleBumps.append(person)

            if len(possibleBumps) == 0:
                needBumpEF[bump[i]] = 0
                print(bump[i] + " needs a bump!")
            else:
                chosenEF = possibleBumps[random.randint(0, len(possibleBumps) - 1)]
                newBump = [bump[i], chosenEF]

                #Changing Need Type
                database[bump[i]][needType] = newFriend
                database[chosenEF][needType] = newFriend

                #Setting Time Frames
                timeWithBumpFrames = random.randint(59, 83)
                database[bump[i]][timeWithBump] = timeWithBumpFrames
                database[chosenEF][timeWithBump] = timeWithBumpFrames

                bumps.append(newBump)
                print(bump[i] + " and " + chosenEF + " are now bumped!")
                print("They are existing friends.")


                print(chosenEF + " waited " + str(needBumpEF[chosenEF]) + " hours.")

                # Removing element from the needBump Queue
                needBumpEF.pop(chosenEF)

                print("They have " + str(database[bump[i]][timeWithBump]) + " hours together.")

    bumps.remove(bump)


# Start simulation

count = 0
while True:
    for bump in bumps:
        if(database[bump[0]][timeWithBump] == 0):
            lookForNewBump(bump)
        else:
            database[bump[0]][timeWithBump] -= 1
            database[bump[1]][timeWithBump] -= 1

    #Incrementing wait time
    for person in needBumpNF:
        needBumpNF[person] += 1
    for person in needBumpEF:
        needBumpEF[person] += 1

    count += 1
    print("END OF FRAME " + str(count))

