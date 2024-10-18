'''
Created on Feb 24, 2017

@author: Alan
'''
from prison import PAYOFF
from prison import NicePlayer
from prison import MeanPlayer
from prison import RandomPlayer
import random
import math
import time
import sys
import numpy

from SampleAgent_007 import MyAgent as Agent1
from AnotherSampleAgent import SampleAgent as MeanAgent

NPLAYERS = 3

# RandomPlayer = __import__("RandomPlayer").RandomPlayer
# NicePlayer = __import__("NicePlayer").NicePlayer
# MeanPlayer = __import__("MeanPlayer").MeanPlayer

noiseFactor = 0.02  # Chance that a player will do the opposite action than they had intended.
phoneBook = {
        0: Agent1(),
        1: Agent1(),
        2: NicePlayer(),
        3: MeanPlayer(),
        4: RandomPlayer()
    }

def playRound(player1, player2, player3, history1, history2, history3):
    """
    Computes one round of play between 3 players (give players and their 
    histories.  Returns a list containing their actions.
    """
    a1 = player1.play(history1, history2, history3)
    if random.uniform(0, 1) < noiseFactor: a1 = 1 - a1
    a2 = player2.play(history2, history3, history1)
    if random.uniform(0, 1) < noiseFactor: a2 = 1 - a2
    a3 = player3.play(history3, history1, history2)
    if random.uniform(0, 1) < noiseFactor: a3 = 1 - a3
    return [a1, a2, a3]


def scoreRound(action1, action2, action3):
    """
    Given actions for three players, returns a list containing their
    respective scores 
    """
    s1 = PAYOFF[action1][action2][action3]
    s2 = PAYOFF[action2][action3][action1]
    s3 = PAYOFF[action3][action1][action2]
    return [s1, s2, s3]


def scoreGame(player1, player2, player3, nRounds):
    """
    Given three players, allow them to play the iterated game for nRounds 
    number of rounds.  Return their scores.
    """
    history1 = []
    history2 = []
    history3 = []
    score1 = 0
    score2 = 0
    score3 = 0

    #numRounds = int(random.normalvariate(100, 10))
    #while 80 > numRounds > 200:
    #    numRounds = int(random.normalvariate(100, 10))
    
    for i in range(nRounds):
        [a1, a2, a3] = playRound(player1, player2, player3, history1, history2, history3)
        history1.append(a1)
        history2.append(a2)
        history3.append(a3)
        [s1, s2, s3] = scoreRound(a1, a2, a3)
        score1 += s1
        score2 += s2
        score3 += s3
    return [score1, score2, score3]


def getPlayer(i):
    """ This function organizes all participating players in a 0+ natural number
    index, and returns an instance of a given player given an index
    """
    if i < 0 or i >= len(phoneBook):
        raise IndexError("getPlayer() index out of bounds")
    return phoneBook[i]


def scheduleGamesForPlayer_Subset(nPlayers, pIndex):
    """ Given the total number of players (nPlayers), and the index of the current
    player (pIndex), returns a list of games scheduled against the player such that 
    pIndex will play against each player (including herself) at least once, at 
    most twice, in the least number of games possible, with no game containing two 
    opponents of the same type.  These games occur in randomized order (and opponent
    pairs are also randomized).
    
    Games are returned as a 2D list of player indices, 
        result = scheduleGamesForPlayer(...)  
    result[0] is the first game to be played
    result[0][0] is always pIndex
    result[0][1] and result[0][2] are the opponents
    
    Example usage:
    > scheduleGamesForPlayer(10, 1)
    produces 5 games as follows:  
    > [[1, 0, 4], [1, 5, 9], [1, 3, 7], [1, 8, 2], [1, 1, 6]]
    """
    playerList = numpy.random.permutation(nPlayers)
    nBasicGames = math.floor(nPlayers / 2)
    schedule = []
    for i in range(nBasicGames):
        schedule.append([pIndex, playerList[i * 2], playerList[i * 2 + 1]])
    # If number of players is odd, we schedule one extra game with the remaining 
    # opponent and a randomly selected player.  The additional opponent cannot be 
    # the same as this last outstanding opponent.
    if nPlayers % 2 == 1:
        r = random.randint(0, nPlayers - 2)
        if r == playerList[-1]:
            r += 1
        schedule.append([pIndex, playerList[-1], r])
    return schedule


def scheduleGamesForPlayer(nPlayers, pIndex):
    """ Given the total number of players (nPlayers), and the index of the current
    player (pIndex), returns a list of games scheduled against the player such that 
    pIndex will play against each player (including herself) at least once, at 
    most twice, in the least number of games possible, with no game containing two 
    opponents of the same type.  These games occur in randomized order (and opponent
    pairs are also randomized).
    
    Games are returned as a 2D list of player indices, 
        result = scheduleGamesForPlayer(...)  
    result[0] is the first game to be played
    result[0][0] is always pIndex
    result[0][1] and result[0][2] are the opponents
    
    Example usage:
    > scheduleGamesForPlayer(10, 1)
    produces 5 games as follows:  
    > [[1, 0, 4], [1, 5, 9], [1, 3, 7], [1, 8, 2], [1, 1, 6]]
    """
    schedule = []
    for i in range(nPlayers):
        for j in range(nPlayers):
            schedule.append([pIndex, i, j])
    return schedule


def scheduleGamesForPlayer_Special(nPlayers, pIndex):
    schedule = [[117, 1, 2]]
    return schedule


def runTournament(nPlayers):
    """
    Runs a tournament for the specified number of players, returning a list containing
    their average performance for their ceil(nPlayers/2) games.
    NB: nPlayers should correspond to the number of players specified in the 
    getPlayers(...) function
    """
    NROUNDS = round(random.normalvariate(100, 10)); # Actual value will be determined randomly
    
    tournamentResults = []
    for p in range(nPlayers):
        startime = time.time()
        # print("Generating Schedule")
        sys.stdout.flush()
        #schedule = scheduleGamesForPlayer_Subset(nPlayers, p)
        schedule = scheduleGamesForPlayer(nPlayers, p)
        pTally = 0
        pGames = 0
        for s in schedule:
            print("Game: ", s)
            [s1, s2, s3] = scoreGame(getPlayer(s[0]), getPlayer(s[1]), getPlayer(s[2]), NROUNDS)
            pTally += s1
            pGames += 1
        tournamentResults.append(pTally / pGames)
        endtime = time.time()
        print(len(tournamentResults), " of ", nPlayers, ": seconds taken=", endtime - startime)
        sys.stdout.flush()
    return tournamentResults

print("Starting...")
results = runTournament(NPLAYERS)
print(results)
