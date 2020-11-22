
###                                                                                ###
### To input your Pokemon/moves, scroll until you see the area boxed in hash signs ###
###                                                                                ###

# Imports the functions we need from Python libraries
from random import seed, randint, uniform
from time import time
from math import floor

# This converts types to an index number, which is used in an array below to determine type advantage.
typeget = {
            "normal": 0, "fire": 1, "water": 2, "electric": 3, "grass": 4, "ice": 5, "fighting": 6, "poison": 7,
            "ground": 8, "flying": 9, "psyhic": 10, "bug": 11, "rock": 12, "ghost": 13, "dragon": 14, "dark": 15,
            "steel": 16, "fairy": 17
        }

# Stores messages for when certain status conditions are applied to a Pokemon
statusget = {
    "burn":"{} was burned!", "paralyze":"{} was paralyzed!", "sleep":"{} fell asleep!", "freeze":"{} was frozen solid!",
    "poison":"{} was poisoned!", "poison_bad":"{} was badly poisoned!"
}

# Stores messages for when certain weather starts
weatherhere = {
    "sun": "Harsh sunlight appeared!", "rain": "It started raining!", "sandstorm": "A sandstorm has spawned!",
    "hail": "It started hailing!"
}

# Stores messages for when certain weather ends
weathergone = {
    "sun": "The harsh sunlight has faded.", "rain": "The rain has stopped.", "sandstorm": "The sandstorm has subsided.",
    "hail": "The hail has stopped."
}

# This global variable tracks the weather in the game. Globals allow variables to be accessed by all functions.
fieldweather = [None]

#########################################################################################
# Input Pokemon/moves here (this is the only part you need to change)

# These are Pokemon moves with specified data, which are then stored to variables.
Tackle = {"name":"Tackle", "type":typeget.get("normal"), "force":"physical", "damage":40, "accuracy":100,
          "status":None, "weather":None}
Fire_Blast = {"name":"Fire Blast", "type":typeget.get("fire"), "force":"special", "damage":110, "accuracy":85,
              "status":"burn", "statusAccuracy":10, "weather":None}
Heavy_Slam = {"name":"Heavy Slam", "type":typeget.get("normal"), "force":"physical", "damage":85, "accuracy":100,
              "status":"paralyze", "statusAccuracy":30, "weather":None}
Sunny_Day = {"name":"Sunny Day", "type":typeget.get("fire"), "force":"status", "damage":None,
             "status":None, "weather":"sun"}
Will_O_Wisp = {"name":"Will O Wisp", "type":typeget.get("fire"), "force":"status", "damage":None, "status":"burn",
               "statusAccuracy":85, "weather":None}

# This is a dictionary storing data for the Pokemon Tepig.
Tepig = {"type": (typeget.get("fire"), None), "hp":125, "maxhp":125, "atk":68, "def":50, "spa":50, "spd": 50, "spe": 50,
         "status": " "}

# These are Pokemon with specified data, which are then stored to variables.
player1 = Tepig; player1["moves"] = (Tackle, Fire_Blast, Heavy_Slam, Sunny_Day)
player2 = Tepig.copy(); player2["moves"] = (Will_O_Wisp, Fire_Blast, Heavy_Slam, Sunny_Day)

#########################################################################################

# Array containing type advantages. Each index is another array containing all possible advantages for each type.
row = ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1/2, 0, 1, 1, 1/2, 1],
        [1, 1/2, 1/2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1/2, 1, 1/2, 1, 2, 1],
        [1, 2, 1/2, 1, 1/2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1/2, 1, 1, 1],
        [1, 1, 2, 1/2, 1/2, 1, 1, 1, 0, 2, 1, 1, 1, 1, 1/2, 1, 1, 1],
        [1, 1/2, 2, 1, 1/2, 1, 1, 1/2, 2, 1/2, 1, 1/2, 2, 1, 1/2, 1, 1/2, 1],
        [1, 1/2, 1/2, 1, 2, 1/2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1/2, 1],
        [2, 1, 1, 1, 1, 2, 1, 1/2, 1, 1/2, 1/2, 1/2, 2, 0, 1, 2, 2, 1/2],
        [1, 1, 1, 1, 2, 1, 1, 1/2, 1/2, 1, 1, 1, 1/2, 1/2, 1, 1, 0, 2],
        [1, 2, 1, 2, 1/2, 1, 1, 2, 1, 0, 1, 1/2, 2, 1, 1, 1, 2, 1],
        [1, 1, 1, 1/2, 2, 1, 2, 1, 1, 1, 1, 2, 1/2, 1, 1, 1, 1/2, 1],
        [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1/2, 1, 1, 1, 1, 0, 1/2, 1],
        [1, 1/2, 1, 1, 2, 1, 1/2, 1/2, 1, 1/2, 2, 1, 1, 1/2, 1, 2, 1/2, 1/2],
        [1, 2, 1, 1, 1, 2, 1/2, 1, 1/2, 2, 1, 2, 1, 1, 1, 1, 1/2, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1/2, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1/2, 0],
        [1, 1, 1, 1, 1, 1, 1/2, 1, 1, 1, 2, 1, 1, 2, 1, 1/2, 1, 1/2],
        [1, 1/2, 1/2, 1/2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1/2, 2],
        [1, 1/2, 1, 1, 1, 1, 2, 1/2, 1, 1, 1, 1, 1, 1, 2, 2, 1/2, 1])

# Function which handles selecting moves. Needs to be a function since it is recursive
def moveselect():

    # Checks if the move selected is valid. If it doesn't, it re-runs the function. Should re-run if the move
    # selected is None
    try:
        # Asks the player for their move. Prints all moves so they can see them before selecting.
        player1["move"] = int(input("What is {}'s move? {} = 1, {} = 2, {} = 3, {} = 4\n".format(player1["trainer"],
        player1["moves"][0]["name"], player1["moves"][1]["name"], player1["moves"][2]["name"],
        player1["moves"][3]["name"])))
    except ValueError:
        return moveselect()
    if 1 <= player1["move"] <= 4:
        print("You selected {}!".format(player1["moves"][int(player1["move"]) - 1]["name"]))
    else: return moveselect()

    # Repeats code from above, but for player 2.
    try:
        player2["move"] = int(input("What is {}'s move? {} = 1, {} = 2, {} = 3, {} = 4\n".format(player2["trainer"],
        player2["moves"][0]["name"],player2["moves"][1]["name"],player2["moves"][2]["name"],
        player2["moves"][3]["name"])))
    except ValueError:
        return moveselect()
    if 1 <= int(player2["move"]) <= 4:
        print("You selected {}!".format(player2["moves"][int(player2["move"]) - 1]["name"]))
    else: return moveselect()

# Function which calculates damage, status, and weather changes based on the move selected + the attacker and victim.
def BattleCalculator(attacker, move, victim):

    # Pre-setting values to default states
    statusMiss = False
    damage = ' '
    status = ' '
    weather = ' '
    global row
    typeadvantage = 1

    # This checks if one of the user's types is equal to the move's type. If so, the damage is multiplied by 1.5.
    if attacker["type"][0] == move["type"] or attacker["type"][1] == move["type"]: typeadvantage *= 1.5

    # This is the first type advantage calculation.
    typeadvantage *= row[move["type"]][victim["type"][0]]

    # This is the second type advantage calculation. It must check if a second type exists before calculating.
    # Notice that it multiplies on top of the first damage calculation which multiplies on top of 1.
    if victim["type"][1] is not None: typeadvantage *= row[move["type"]][victim["type"][1]]

    # If the user is paralyzed, we add a 25% chance the user's move is cancelled
    if attacker["status"][0] == "paralyze":
        hit = randint(1, 4)
        if hit == 1:
            print("{} is paralyzed!".format(attacker["name"]))

            # Returning blank values to indicate nothing should happen
            return damage, status, weather

    # If the user is frozen or asleep, their move is cancelled until a certain number of turns later
    if attacker["status"][0] == "freeze" or attacker["status"][0] == "sleep":
        if attacker["status"][1] != 0:
            attacker["status"][1] -= 1
            if attacker["status"][0] == "freeze": print("{} is frozen!".format(attacker["name"]))
            if attacker["status"][0] == "sleep": print("{} is asleep.".format(attacker["name"]))
            return damage, status, weather
        else:
            # If the number of turns left is 0, the user should be allowed to move from now on and status cleared
            if attacker["status"][0] == "freeze": print("{} thawed out!".format(attacker["name"]))
            if attacker["status"][0] == "sleep": print("{} woke up!".format(attacker["name"]))
            attacker["status"] = None

    # Skips damage calculation if move deals no damage
    if move["damage"] is not None:

        # Skips accuracy check if move never misses
        if move["accuracy"] is not None:
            hit = randint(1, 100)
            if move["accuracy"] < hit:
                print("{}'s attack missed!".format(attacker["name"]))
                return damage, status, weather

        # Variable which determines weather's effect on damage taken from a move.
        weatherboost = 1
        if fieldweather[0] == "sun" and move["type"] == typeget.get("fire"): weatherboost = 1.5
        if fieldweather[0] == "rain" and move["type"] == typeget.get("water"): weatherboost = 1.5
        if fieldweather[0] == "sun" and move["type"] == typeget.get("water"): weatherboost = 0.5
        if fieldweather[0] == "rain" and move["type"] == typeget.get("fire"): weatherboost = 0.5

        # If a burn is inflicted on the user, their physical damage should always be halved
        burn = 1
        if attacker["status"][0] == "burn" and move["force"] == "physical": burn = 0.5

        # There is a 1/24 chance of critical hit, which multiplies damage by 1.5 along with other effects not added yet
        crit = randint(1, 24)
        if crit == 1: crit = 1.5
        else: crit = 1
        if crit == 1.5: print("Critical hit!")

        # Damage varies between 85% of the original damage to 100% of the original damage.
        rand = uniform(0.85, 1)

        # Adds and multiplies all the previous variables together to equate the damage taken, which will be returned
        damage = (((22 * move["damage"] * (attacker["atk"] if move["force"] == "physical" else attacker["spa"]) /
              (victim["def"] if move["force"] == "physical" else victim["spd"]))/50 + 2) * typeadvantage * rand * crit
              * weatherboost * burn)

    # Skips status application if move has no possible status conditions
    if move["status"] != None:

        # Skips accuracy check if status condition never misses
        if move["statusAccuracy"] != None:
            hit = randint(1, 100)
            if move["statusAccuracy"] < hit:
                if move["force"] == "status": print("{}'s attack missed!".format(attacker["name"]))
                statusMiss = True

        # Checks if the status missed, the victim is immune to the move's type (only applies to Thunder Wave, needs to
        # be changed later), the victim has a status already, and if the status is trying to burn a Fire type or
        # paralyze an Electric type before applying a status condition
        if statusMiss is False and typeadvantage != 0 and victim["status"] == " " and ((victim["type"][0] !=
        typeget.get("fire") and victim["type"][1] != typeget.get("fire")) or move["status"] != "burn") and\
        ((victim["type"][0] != typeget.get("electric") and victim["type"][1] != typeget.get("electric")) or
         move["status"] != "paralyze"):

            # Will return the status condition
            status = [move["status"]]

    # Skips weather change if the move has no weather changes or if the requested weather already exists on the field
    if move["weather"] != None and move["weather"] != fieldweather[0]:

        # Will return the weather change with a specified number of turns left (will need to be changed if items are
        # added such as Damp Rock which increases turns)
        weather = [move["weather"], 5]

    # Returns damage, status and weather if not done so already
    return damage, status, weather

# Turn function which handles each turn in the game. (Called once, maybe delete?)
def turn(firstmover, secondmover):

    global fieldweather

    # Calls in the first set of calculations (damage, status, weather) caused by the first moving Pokemon
    calcs = BattleCalculator(firstmover, firstmover["moves"][firstmover["move"] - 1], secondmover)

    # If nothing was returned, the move failed
    if calcs[0] == " " and calcs[1] == " " and calcs[2] == " ":
            print("{}'s move failed!".format(firstmover["name"]))
    else:
            print("{} used {}!".format(firstmover["name"], firstmover["moves"][firstmover["move"] - 1]["name"]))

            # Skips if the move had no damage or if the move's damage calculated to 0
            if calcs[0] != " " and calcs[0] != 0:

                # Subtracts health from the victim
                secondmover["hp"] -= calcs[0]

                # Sets victim's health to 0 if the victim faints (HP <= 0)
                if secondmover["hp"] < 0: secondmover["hp"] = 0
                print("{} took {} damage!".format(secondmover["name"], floor(calcs[0])))
                print("{} is now at {}/{} HP!".format(secondmover["name"], floor(secondmover["hp"]),
                                                      secondmover["maxhp"]))
            # Skips if no status should be applied
            if calcs[1] != " ":

                # Applies status to victim
                secondmover["status"] = calcs[1]
                print((statusget.get(calcs[1][0])).format(secondmover["name"]))

            # Skips if no weather changes should be made
            if calcs[2] != " ":

                # Applies the new weather
                fieldweather = calcs[2]
                print(weatherhere.get(calcs[2][0]))

    # Skips the second set of calculations if the second moving Pokemon has already fainted
    # The rest of the code is the same as above, just the attacker and victim are swapped
    if secondmover["hp"] != 0:
        calcs = BattleCalculator(secondmover, secondmover["moves"][secondmover["move"] - 1], firstmover)
        if calcs[0] == " " and calcs[1] == " " and calcs[2] == " ":
            print("{}'s move failed!".format(secondmover["name"]))
        else:
            print("{} used {}!".format(secondmover["name"], secondmover["moves"][secondmover["move"] - 1]["name"]))
            if calcs[0] != ' ' and calcs[0] != 0:
                firstmover["hp"] -= calcs[0]
                if firstmover["hp"] < 0: firstmover["hp"] = 0
                print("{} took {} damage!".format(firstmover["name"], floor(calcs[0])))
                print("{} is now at {}/{} HP!".format(firstmover["name"], floor(firstmover["hp"]),
                                                      firstmover["maxhp"]))
            if calcs[1] != " ":
                firstmover["status"] = calcs[1]
                print((statusget.get(calcs[1][0])).format(firstmover["name"]))
            if calcs[2] != " ":
                fieldweather = calcs[2]
                print(weatherhere.get(calcs[2][0]))

    # Skips status damage if any Pokemon has fainted
    if firstmover["hp"] != 0 and secondmover["hp"] != 0:

        # Applies status damage to the first moving Pokemon, then the second
        for player in (firstmover, secondmover):
            if player["status"][0] == "burn":
                player["hp"] -= player["maxhp"] * 1/16
                if player["hp"] < 0: player["hp"] = 0
                print("{} took damage from the burn!".format(player["name"]))
                print("{} took {} damage!".format(player["name"], floor(player["maxhp"] * 1/16)))
                print("{} is now at {}/{} HP!".format(player["name"], floor(player["hp"]), player["maxhp"]))

                # If the first moving Pokemon faints to a status condition, the game will end without the second
                # taking damage
                if player["hp"] == 0: break

    # Skips weather turn if no weather exists
    if fieldweather[0] is not None:

        # If the current weather has expired, the weather will reset and send a message indicating such
        if fieldweather[1] == 0:
            print(weathergone.get(fieldweather[0]))
            fieldweather = [None]

        # Otherwise, decrement the turns remaining on the weather by 1
        else: fieldweather[1] -= 1


## Start of game


    # Sets names
player1["trainer"] = input("Player 1 name: ")
player1["name"] = input("Player 1 Pokemon name: ")
player2["trainer"] = input("Player 2 name: ")
player2["name"] = input("Player 2 Pokemon name: ")
if player1 is player2: print("FUCK")

    # Sets random seed
seed(time())

    # Game loop. Ends when any Pokemon faints
while player1["hp"] > 0 and player2["hp"] > 0:

    # Selects moves
    moveselect()
    speedmod1 = 1
    speedmod2 = 1

    # Halves speed if the player is paralyzed
    if player1["status"][0] == "paralyze": speedmod1 = 0.5
    if player2["status"][0] == "paralyze": speedmod2 = 0.5

    # Determines turn order based on the speed of player 1 and player 2
    if player1["spe"] * speedmod1 > player2["spe"] * speedmod2:
        turn(player1, player2)
    elif player1["spe"] * speedmod1 < player2["spe"] * speedmod2:
        turn(player2, player1)
    else:

        # Will be random if the speed is the same
        turn(player1, player2) if randint(1, 2) == 1 else turn(player2, player1)


    # Declaring the winner to whichever Pokemon is left standing
if player1["hp"] <= 0:
    print("{} has won with their {}!".format(player2["trainer"], player2["name"]))
elif player2["hp"] <= 0:
    print("{} has won with their {}!".format(player1["trainer"], player1["name"]))
else:
    print("ERROR: The game ended before any Pokemon fainted.")
