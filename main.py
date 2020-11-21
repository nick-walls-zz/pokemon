
# Imports the functions we need from Python libraries
from random import seed, randint, uniform
from time import time
from math import floor

# To input your Pokemon/moves, scroll until you see the area boxed in hash signs

# This converts types to an index number, which is used in an array below to determine type advantage.
typeget = {
            'normal': 0, 'fire': 1, 'water': 2, 'electric': 3, 'grass': 4, 'ice': 5, 'fighting': 6, 'poison': 7,
            'ground': 8, 'flying': 9, 'psyhic': 10, 'bug': 11, 'rock': 12, 'ghost': 13, 'dragon': 14, 'dark': 15,
            'steel': 16, 'fairy': 17
        }

# Stores messages for when certain status conditions are applied to a Pokemon
statusget = {
    "burn":"{} was burned!", "paralyze":"{} was paralyzed!", "sleep":"{} fell asleep!", "freeze":"{} was frozen solid!",
    "poison":"{} was poisoned!", "poison_bad":"{} was badly poisoned!"
}

# Stores messages for when certain weather starts
weatherhere = {
    'sun': "Harsh sunlight appeared!", 'rain': "It started raining!", 'sandstorm': "A sandstorm has spawned!",
    'hail': "It started hailing!"
}

# Stores messages for when certain weather ends
weathergone = {
    'sun': "The harsh sunlight has faded.", 'rain': "The rain has stopped.", 'sandstorm': "The sandstorm has subsided.",
    'hail': "The hail has stopped."
}

# This global variable tracks the weather in the game. Globals allow variables to be accessed by all functions.
global fieldweather; fieldweather = [None]

# Pokemon class. Stores information for each Pokemon. Should be converted to a data container as it has no function
class Pokemon:

    # Initializes an object and gives it the data specified in the arguments.
    def __init__(self, info, move1=None, move2=None, move3=None, move4=None, status=' '):

        # "Self" refers to the object.
        self.type = [typeget.get(info[0]), typeget.get(info[1])]
        self.stats = [info[2], info[3], info[4], info[5], info[6], info[7]]
        self.moves = [move1, move2, move3, move4]; self.status = status; self.maxhp = self.stats[0]

# Pokemon move class. Stores information for each move. Should be converted to a data container as it has no function
class PokemonMove:

    # Initializes an object and gives it the data specified in the arguments.
    def __init__(self, name, type, force=None, damage=None, accuracy=None, status=None, statusAccuracy=None,
                 weather=None):

        # "Self" refers to the object.
        self.type = typeget.get(type); self.damage = damage; self.accuracy = accuracy; self.status = status
        self.statusAccuracy = statusAccuracy; self.weather = weather; self.force = force; self.name = name


#########################################################################################
# Input Pokemon/moves here (this is the only part you need to change)

# These are Pokemon move objects with specified arguments, which are then stored to variables.
Tackle = PokemonMove('Tackle', 'normal', 'physical', 40, 100)
Fire_Blast = PokemonMove('Fire Blast', 'fire', 'special', 110, 85, 'burn', 10)
Heavy_Slam = PokemonMove('Heavy Slam', 'normal', 'physical', 85, 100, 'paralyze', 30)
Sunny_Day = PokemonMove('Sunny Day', 'fire', 'status', weather='sun')
Will_O_Wisp = PokemonMove('Will O Wisp', 'fire', 'status', status='burn', statusAccuracy=85)

# This is a tuple storing data for the Pokemon Tepig.
Tepig = ('fire', None, 125, 68, 50, 50, 50, 50)

# These are Pokemon objects with specified arguments, which are then stored to variables.
player1 = Pokemon(Tepig, Tackle, Fire_Blast, Heavy_Slam, Sunny_Day)
player2 = Pokemon(Tepig, Will_O_Wisp, Fire_Blast, Heavy_Slam, Sunny_Day)

#########################################################################################

# Function which handles selecting moves. Should be removed and code copied to the call location since it is only
# called once
def moveselect():

    # Asks the player for their move. Prints all moves so they can see them before selecting.
    move1 = input("What is {}'s move? {} = 1, {} = 2, {} = 3, {} = 4\n".format(player1.trainer, player1.moves[0].name,
    player1.moves[1].name, player1.moves[2].name, player1.moves[3].name))

    # Checks if the move selected is valid. If it doesn't, it re-runs the function. Should re-run if the move
    # selected is None
    try:
        int(move1)
    except ValueError:
        return moveselect()
    if 1 <= int(move1) <= 4:
        print("You selected {}!".format(player1.moves[int(move1) - 1].name))
    else: return moveselect()

    # Repeats code from above, but for player 2.
    move2 = input("What is {}'s move? {} = 1, {} = 2, {} = 3, {} = 4\n".format(player2.trainer, player2.moves[0].name,
    player2.moves[1].name, player2.moves[2].name, player2.moves[3].name))
    try:
        int(move2)
    except ValueError:
        return moveselect()
    if 1 <= int(move2) <= 4:
        print("You selected {}!".format(player2.moves[int(move2) - 1].name))
    else: return moveselect()

    # Returns the moves of players 1 and 2.
    return int(move1), int(move2)

# Function which handles type advantages and STAB advantages. This is only called once; maybe remove the function?
def typeAdvantage(user, move, victim):

    # This will be our multiplier number to return. Maybe this should be moved after the array for readability.
    value = 1

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

    # This checks if one of the user's types is equal to the move's type. If so, the damage is multiplied by 1.5.
    if user.type[0] == move.type or user.type[1] == move.type: value *= 1.5

    # This is the first type advantage calculation.
    value *= row[move.type][victim.type[0]]

    # This is the second type advantage calculation. It must check if a second type exists before calculating.
    # Notice that it multiplies on top of the first damage calculation which multiplies on top of 1.
    if victim.type[1] != None: value *= row[move.type][victim.type[1]]

    # Returns the multiplier number.
    return value

# Function which calculates damage, status, and weather changes based on the move selected + the attacker and victim.
def BattleCalculator(attacker, move, victim):

    # Pre-setting values to default states
    statusMiss = False
    damage = ' '
    status = ' '
    weather = ' '

    # Calls typeAdvantage function and retrieves the multiplier number
    typeadvantage = typeAdvantage(attacker, move, victim)

    # If the user is paralyzed, we add a 25% chance the user's move is cancelled
    if attacker.status[0] == 'paralyze':
        hit = randint(1, 4)
        if hit == 1:
            print("{} is paralyzed!".format(attacker.name))

            # Returning blank values to indicate nothing should happen
            return damage, status, weather

    # If the user is frozen or asleep, their move is cancelled until a certain number of turns later
    if attacker.status[0] == 'freeze' or attacker.status[0] == 'sleep':
        if attacker.status[1] != 0:
            attacker.status[1] -= 1
            if attacker.status[0] == 'freeze': print("{} is frozen!".format(attacker.name))
            if attacker.status[0] == 'sleep': print("{} is asleep.".format(attacker.name))
            return damage, status, weather
        else:
            # If the number of turns left is 0, the user should be allowed to move from now on and status cleared
            if attacker.status[0] == 'freeze': print("{} thawed out!".format(attacker.name))
            if attacker.status[0] == 'sleep': print("{} woke up!".format(attacker.name))
            attacker.status = None

    # Skips damage calculation if move deals no damage
    if move.damage is not None:

        # Skips accuracy check if move never misses
        if move.accuracy is not None:
            hit = randint(1, 100)
            if move.accuracy < hit:
                print("{}'s attack missed!".format(attacker.name))
                return damage, status, weather

        # Variable which determines weather's effect on damage taken from a move.
        weatherboost = 1
        if fieldweather[0] == 'sun' and move.type == typeget.get('fire'): weatherboost = 1.5
        if fieldweather[0] == 'rain' and move.type == typeget.get('water'): weatherboost = 1.5
        if fieldweather[0] == 'sun' and move.type == typeget.get('water'): weatherboost = 0.5
        if fieldweather[0] == 'rain' and move.type == typeget.get('fire'): weatherboost = 0.5

        # If a burn is inflicted on the user, their physical damage should always be halved
        burn = 1
        if attacker.status[0] == 'burn' and move.force == 'physical': burn = 0.5

        # There is a 1/24 chance of critical hit, which multiplies damage by 1.5 along with other effects not added yet
        crit = randint(1, 24)
        if crit == 1: crit = 1.5
        else: crit = 1
        if crit == 1.5: print("Critical hit!")

        # Damage varies between 85% of the original damage to 100% of the original damage.
        rand = uniform(0.85, 1)

        # Adds and multiplies all the previous variables together to equate the damage taken, which will be returned
        damage = (((22 * move.damage * (attacker.stats[1] if move.force == 'physical' else attacker.stats[3]) /
              (victim.stats[2] if move.force == 'physical' else victim.stats[4]))/50 + 2) * typeadvantage * rand * crit
              * weatherboost * burn)

    # Skips status application if move has no possible status conditions
    if move.status != None:

        # Skips accuracy check if status condition never misses
        if move.statusAccuracy != None:
            hit = randint(1, 100)
            if move.statusAccuracy < hit:
                if move.force == 'status': print("{}'s attack missed!".format(attacker.name))
                statusMiss = True

        # Checks if the status missed, the victim is immune to the move's type (only applies to Thunder Wave, needs to
        # be changed later), the victim has a status already, and if the status is trying to burn a Fire type or
        # paralyze an Electric type before applying a status condition
        if statusMiss is False and typeadvantage != 0 and victim.status == ' ' and ((victim.type[0] !=
        typeget.get('fire') and victim.type[1] != typeget.get('fire')) or move.status != 'burn') and ((victim.type[0] !=
        typeget.get('electric') and victim.type[1] != typeget.get('electric')) or move.status != 'paralyze'):

            # Will return the status condition
            status = [move.status]

    # Skips weather change if the move has no weather changes or if the requested weather already exists on the field
    if move.weather != None and move.weather != fieldweather[0]:

        # Will return the weather change with a specified number of turns left (will need to be changed if items are
        # added such as Damp Rock which increases turns)
        weather = [move.weather, 5]

    # Returns damage, status and weather if not done so already
    return damage, status, weather

# Turn function which handles each turn in the game. (Called once, maybe delete?)
def turn(firstmover, secondmover, order):

    # This determines which move the first Pokemon has out of the two moves returned from moveselect.
    # Definitely awkward, selected move should be an attribute of the Pokemon class
    move = moves[0]
    if order == 1: move = moves[1]
    global fieldweather

    # Calls in the first set of calculations (damage, status, weather) caused by the first moving Pokemon
    calcs = BattleCalculator(firstmover, firstmover.moves[move - 1], secondmover)

    # If nothing was returned, the move failed
    if calcs[0] == ' ' and calcs[1] == ' ' and calcs[2] == ' ':
            print("{}'s move failed!".format(firstmover.name))
    else:
            print("{} used {}!".format(firstmover.name, firstmover.moves[move - 1].name))

            # Skips if the move had no damage or if the move's damage calculated to 0
            if calcs[0] != ' ' and calcs[0] != 0:

                # Subtracts health from the victim
                secondmover.stats[0] -= calcs[0]

                # Sets victim's health to 0 if the victim faints (HP <= 0)
                if secondmover.stats[0] < 0: secondmover.stats[0] = 0
                print("{} took {} damage!".format(secondmover.name, floor(calcs[0])))
                print("{} is now at {}/{} HP!".format(secondmover.name, floor(secondmover.stats[0]),
                                                      secondmover.maxhp))
            # Skips if no status should be applied
            if calcs[1] != ' ':

                # Applies status to victim
                secondmover.status = calcs[1]
                print((statusget.get(calcs[1][0])).format(secondmover.name))

            # Skips if no weather changes should be made
            if calcs[2] != ' ':

                # Applies the new weather
                fieldweather = calcs[2]
                print(weatherhere.get(calcs[2][0]))

    # Skips the second set of calculations if the second moving Pokemon has already fainted
    # The rest of the code is the same as above, just the attacker and victim are swapped
    if secondmover.stats[0] != 0:
        move = moves[1]
        if order == 1: move = moves[0]
        calcs = BattleCalculator(secondmover, secondmover.moves[move - 1], firstmover)
        if calcs[0] == ' ' and calcs[1] == ' ' and calcs[2] == ' ':
            print("{}'s move failed!".format(secondmover.name))
        else:
            print("{} used {}!".format(secondmover.name, secondmover.moves[move - 1].name))
            if calcs[0] != ' ' and calcs[0] != 0:
                firstmover.stats[0] -= calcs[0]
                if firstmover.stats[0] < 0: firstmover.stats[0] = 0
                print("{} took {} damage!".format(firstmover.name, floor(calcs[0])))
                print("{} is now at {}/{} HP!".format(firstmover.name, floor(firstmover.stats[0]),
                                                      firstmover.maxhp))
            if calcs[1] != ' ':
                firstmover.status = calcs[1]
                print((statusget.get(calcs[1][0])).format(firstmover.name))
            if calcs[2] != ' ':
                fieldweather = calcs[2]
                print(weatherhere.get(calcs[2][0]))

    # Skips status damage if any Pokemon has fainted
    if firstmover.stats[0] != 0 and secondmover.stats[0] != 0:

        # Applies status damage to the first moving Pokemon, then the second
        for player in (firstmover, secondmover):
            if player.status[0] == 'burn':
                player.stats[0] -= player.maxhp * 1/16
                if player.stats[0] < 0: player.stats[0] = 0
                print("{} took damage from the burn!".format(player.name))
                print("{} took {} damage!".format(player.name, floor(player.maxhp * 1/16)))
                print("{} is now at {}/{} HP!".format(player.name, floor(player.stats[0]), player.maxhp))

                # If the first moving Pokemon faints to a status condition, the game will end without the second
                # taking damage
                if player.stats[0] == 0: break

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
player1.trainer = input("Player 1 name: ")
player1.name = input("Player 1 Pokemon name: ")
player2.trainer = input("Player 2 name: ")
player2.name = input("Player 2 Pokemon name: ")

    # Sets random seed
seed(time())

    # Game loop. Ends when any Pokemon faints
while player1.stats[0] > 0 and player2.stats[0] > 0:

    # Recieves moves selected
    moves = moveselect()
    speedmod1 = 1
    speedmod2 = 1

    # Halves speed if the player is paralyzed
    if player1.status[0] == 'paralyze': speedmod1 = 0.5
    if player2.status[0] == 'paralyze': speedmod2 = 0.5

    # Determines turn order based on the speed of player 1 and player 2
    if player1.stats[5] * speedmod1 > player2.stats[5] * speedmod2:
        turn(player1, player2, 0)
    elif player1.stats[5] * speedmod1 < player2.stats[5] * speedmod2:
        turn(player2, player1, 1)
    else:

        # Will be random if the speed is the same
        turn(player1, player2, 0) if randint(1, 2) == 1 else turn(player2, player1, 1)


    # Declaring the winner to whichever Pokemon is left standing
if player1.stats[0] <= 0:
    print("{} has won with their {}!".format(player2.trainer, player2.name))
elif player2.stats[0] <= 0:
    print("{} has won with their {}!".format(player1.trainer, player1.name))
else:
    print("ERROR: The game ended before any Pokemon fainted.")
