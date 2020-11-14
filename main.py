import random
import math

typeget = {
            'normal': 0, 'fire': 1, 'water': 2, 'electric': 3, 'grass': 4, 'ice': 5, 'fighting': 6, 'poison': 7,
            'ground': 8, 'flying': 9, 'psyhic': 10, 'bug': 11, 'rock': 12, 'ghost': 13, 'dragon': 14, 'dark': 15,
            'steel': 16, 'fairy': 17
        }

statusget = {
    'burn':"{} was burned!", 'paralyze':"{} was paralyzed!", 'sleep':"{} fell asleep!", 'freeze':"{} was frozen solid!",
    'poison':"{} was poisoned!", 'poison_bad':"{} was badly poisoned!"
}

weatherhere = {
    'sun': "Harsh sunlight appeared!", 'rain': "It started raining!", 'sandstorm': "A sandstorm has spawned!",
    'hail': "It started hailing!"
}

weathergone = {
    'sun': "The harsh sunlight has faded.", 'rain': "The rain has stopped.", 'sandstorm': "The sandstorm has subsided.",
    'hail': "The hail has stopped."
}

global fieldweather; fieldweather = [None]

class Pokemon:

    def __init__(self, info, move1=None, move2=None, move3=None, move4=None, status=' ', name=None):

        self.type = [typeget.get(info[0]), typeget.get(info[1])]
        self.stats = [info[2], info[3], info[4], info[5], info[6], info[7]]
        self.moves = [move1, move2, move3, move4]; self.status = status
        self.name = name; self.maxhp = self.stats[0]


class PokemonMove:

    def __init__(self, name, type, force=None, damage=None, accuracy=None, status=None, statusAccuracy=None,
                 weather=None):
        self.type = typeget.get(type); self.damage = damage; self.accuracy = accuracy; self.status = status
        self.statusAccuracy = statusAccuracy; self.weather = weather; self.force = force; self.name = name


Tackle = PokemonMove('Tackle', 'normal', 'physical', 40, 100)
Fire_Blast = PokemonMove('Fire Blast', 'fire', 'special', 110, 85, 'burn', 10)
Heavy_Slam = PokemonMove('Heavy Slam', 'normal', 'physical', 85, 100, 'paralyze', 30)
Sunny_Day = PokemonMove('Sunny Day', 'fire', weather='sun')
Will_O_Wisp = PokemonMove('Will O Wisp', 'fire', status='burn', statusAccuracy=85)

Tepig = ('fire', None, 125, 68, 50, 50, 50, 50)

player1 = Pokemon(Tepig, Tackle, Fire_Blast, Heavy_Slam, Sunny_Day)
player1.name = input("Player 1 name: ")
player2 = Pokemon(Tepig, Will_O_Wisp, Fire_Blast, Heavy_Slam, Sunny_Day)
player2.name = input("Player 2 name: ")


def moveselect():
    move1 = input("What is player 1's move? {} = 1, {} = 2, {} = 3, {} = 4\n".format(player1.moves[0].name,
    player1.moves[1].name, player1.moves[2].name, player1.moves[3].name))
    if 1 <= int(move1) <= 4:
        print("You selected {}!".format(player1.moves[int(move1) - 1].name))
    else: moveselect()
    move2 = input("What is player 2's move? {} = 1, {} = 2, {} = 3, {} = 4\n".format(player2.moves[0].name,
    player2.moves[1].name, player2.moves[2].name, player2.moves[3].name))
    if 1 <= int(move2) <= 4:
        print("You selected {}!".format(player2.moves[int(move2) - 1].name))
    else: moveselect()
    return int(move1), int(move2)

def typeAdvantage(user, move, victim):

    value = 1
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

    if user.type[0] == move.type or user.type[1] == move.type: value *= 1.5
    value *= row[move.type][victim.type[0]]
    if victim.type[1] != None: value *= row[move.type][victim.type[1]]
    return value

def BattleCalculator(attacker, move, victim):
    statusMiss = False
    damage = ''
    status = ''
    weather = ''

    typeadvantage = typeAdvantage(attacker, move, victim)

    if attacker.status[0] == 'paralyze':
        hit = random.randint(1, 4)
        if hit == 1:
            print("{} is paralyzed!".format(attacker.name))
            return '','',''

    if attacker.status[0] == 'freeze' or attacker.status[0] == 'sleep':
        if attacker.status[1] != 0:
            attacker.status[1] -= 1
            if attacker.status[0] == 'freeze': print("{} is frozen!".format(attacker.name))
            if attacker.status[0] == 'sleep': print("{} is asleep.".format(attacker.name))
            return '','',''
        else:
            if attacker.status[0] == 'freeze': print("{} thawed out!".format(attacker.name))
            if attacker.status[0] == 'sleep': print("{} woke up!".format(attacker.name))
            attacker.status = None

    if move.damage is not None:
        if move.accuracy is not None:
            hit = random.randint(1, 100)
            if move.accuracy < hit:
                print("{}'s attack missed!".format(attacker.name))
                return '','',''
        weatherboost = 1
        if fieldweather[0] == 'sun' and move.type == typeget.get('fire'): weatherboost = 1.5
        if fieldweather[0] == 'rain' and move.type == typeget.get('water'): weatherboost = 1.5
        if fieldweather[0] == 'sun' and move.type == typeget.get('water'): weatherboost = 0.5
        if fieldweather[0] == 'rain' and move.type == typeget.get('fire'): weatherboost = 0.5
        burn = 1
        if attacker.status[0] == 'burn' and move.force == 'physical': burn = 0.5
        crit = random.randint(1, 24)
        if crit == 1: crit = 1.5
        else: crit = 1
        if crit == 1.5: print("Critical hit!")
        rand = random.uniform(0.85, 1)
        damage = (((22 * move.damage * (attacker.stats[1] if move.force == 'physical' else attacker.stats[3]) /
              (victim.stats[2] if move.force == 'physical' else victim.stats[4]))/50 + 2) * typeadvantage * rand * crit
              * weatherboost * burn)

    if move.status != None:
        if move.statusAccuracy != None:
            hit = random.randint(1, 100)
            if move.statusAccuracy < hit:
                if damage == 0: print("{}'s attack missed!".format(attacker.name))
                statusMiss = True
        if statusMiss is False and typeadvantage != 0 and victim.status == ' ':
            status = [move.status]

    if move.weather != None:
        weather = [move.weather, 5]

    return damage, status, weather

def turn(firstmover, secondmover, order):
    move = moves[0]
    if order == 1: move = moves[1]
    global fieldweather
    calcs = BattleCalculator(firstmover, firstmover.moves[move - 1], secondmover)
    if calcs[0] == '' and calcs[1] == '' and calcs[2] == '':
            print("{}'s move failed!".format(firstmover.name))
    else:
            print("{} used {}!".format(firstmover.name, firstmover.moves[move - 1].name))
            if calcs[0] != '' and calcs[0] > 0:
                secondmover.stats[0] -= calcs[0]
                if secondmover.stats[0] < 0: secondmover.stats[0] = 0
                print("{} took {} damage!".format(secondmover.name, math.floor(calcs[0])))
                print("{} is now at {}/{} HP!".format(secondmover.name, math.floor(secondmover.stats[0]),
                                                      secondmover.maxhp))
            if calcs[1] != '':
                secondmover.status = calcs[1]
                print((statusget.get(calcs[1][0])).format(secondmover.name))
            if calcs[2] != '':
                fieldweather = calcs[2]
                print(weatherhere.get(calcs[2][0]))

    if secondmover.stats[0] != 0:
        move = moves[1]
        if order == 1: move = moves[0]
        calcs = BattleCalculator(secondmover, secondmover.moves[move - 1], firstmover)
        if calcs[0] == '' and calcs[1] == '' and calcs[2] == '':
            print("{}'s move failed!".format(secondmover.name))
        else:
            print("{} used {}!".format(secondmover.name, secondmover.moves[move - 1].name))
            if calcs[0] != '' and calcs[0] > 0:
                firstmover.stats[0] -= calcs[0]
                if firstmover.stats[0] < 0: firstmover.stats[0] = 0
                print("{} took {} damage!".format(firstmover.name, math.floor(calcs[0])))
                print("{} is now at {}/{} HP!".format(firstmover.name, math.floor(firstmover.stats[0]),
                                                      firstmover.maxhp))
            if calcs[1] != '':
                firstmover.status = calcs[1]
                print((statusget.get(calcs[1][0])).format(firstmover.name))
            if calcs[2] != '':
                fieldweather = calcs[2]
                print(weatherhere.get(calcs[2][0]))

    for player in (firstmover, secondmover):
        if player.status[0] == 'burn':
            player.stats[0] -= player.maxhp * 1/16
            if player.stats[0] < 0: player.stats[0] = 0
            print("{} took damage from the burn!".format(player.name))
            print("{} took {} damage!".format(player.name, math.floor(player.maxhp * 1/16)))
            print("{} is now at {}/{} HP!".format(player.name, math.floor(player.stats[0]), player.maxhp))
            if player.stats[0] == 0: break

    if fieldweather[0] is not None:
        if fieldweather[1] == 0:
            print(weathergone.get(fieldweather[0]))
            fieldweather = None
        else: fieldweather[1] -= 1

while player1.stats[0] > 0 and player2.stats[0] > 0:
    moves = moveselect()
    speedmod1 = 1
    speedmod2 = 1
    if player1.status[0] == 'paralyze': speedmod1 = 0.5
    if player2.status[0] == 'paralyze': speedmod2 = 0.5
    if player1.stats[5] * speedmod1 > player2.stats[5] * speedmod2:
        turn(player1, player2, 0)
    elif player1.stats[5] * speedmod1 < player2.stats[5] * speedmod2:
        turn(player2, player1, 1)
    else:
        turn(player1, player2, 0) if random.randint(1, 2) == 1 else turn(player2, player1, 1)


if player1.stats[0] <= 0:
    print("Player 2 has won with their trusty {}!".format(player2.name))
elif player2.stats[0] <= 0:
    print("Player 1 has won with their trusty {}!".format(player1.name))
else:
    print("ERROR: The game ended before any Pokemon fainted.")
