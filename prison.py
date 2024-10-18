'''
This Python module models the three-player Prisoner's Dilemma game.
We use the integer "0" to represent cooperation, and "1" to represent 
defection. 

Recall that in the 2-players dilemma, U(DC) > U(CC) > U(DD) > U(CD), where
we give the payoff for the first player in the list. We want the three-player game 
to resemble the 2-player game whenever one player's response is fixed, and we
also want symmetry, so U(CCD) = U(CDC) etc. This gives the unique ordering

U(DCC) > U(CCC) > U(DDC) > U(CDC) > U(DDD) > U(CDD)

The payoffs for player 1 are given by the following matrix:

@author: akhtsang
Created on Feb 9, 2017
'''

import random
import math
#import runTournament as island

PAYOFF = [[[6, 3], [3, 0]], [[8, 5], [5, 2]]]

"""
So payoff[i][j][k] represents the payoff to player 1 when the first
player's action is i, the second player's action is j, and the
third player's action is k.

In this simulation, triples of players will play each other repeatedly in a
'match'. A match consists of about 100 rounds, and your score from that match
is the average of the payoffs from each round of that match. For each round, your
strategy is given a list of the previous plays (so you can remember what your 
opponent did) and must compute the next action.
 """


class Player(object):
    """
    This defines an interface for a player of the 3-player.  Inherit and modify this class
    by declaring the following:
    
    class SecretStrategyPlayer(Player)
        # code goes here
        # make sure you implement the play(...) function
    
    Attributes:
    While you are not prohibited from adding attributes.  You should not need 
    to implement do so.  The parameters to play(...) contain all information 
    available about the current state of play. 
    """

    def studentID(self):
        """ Returns the creator's numeric studentID """
        raise NotImplementedError("studentID not implemented")

    def agentName(self):
        """ Returns a creative name for the agent """
        return self.__class__.__name__

    def play(self, myHistory, oppHistory1, oppHistory2):
        """ 
        Given a history of play, computes and returns your next move
        ( 0 = cooperate; 1 = defect )
        myHistory = list of int representing your past plays
        oppHisotry1 = list of int representing opponent 1's past plays
        oppHisotry2 = list of int representing opponent 2's past plays
        NB: use len(myHistory) to find the number of games played
        """
        raise NotImplementedError("play not implemented")


class NicePlayer(Player):
    """
    The nicePlayer always cooperates (plays 0).
    """

    def studentID(self):
        return "42"

    def agentName(self):
        return "Nice Player"

    def play(self, myHistory, oppHistory1, oppHistory2):
        return 0


class MeanPlayer(Player):
    """
    The meanPlayer always defects (plays 1).
    """

    def studentID(self):
        return "42"

    def agentName(self):
        return "Mean Player"

    def play(self, myHistory, oppHistory1, oppHistory2):
        return 1


class RandomPlayer(Player):
    """
    The randomPlayer chooses an action randomly.
    """

    def studentID(self):
        return "42"

    def agentName(self):
        return "Random Player"

    def play(self, myHistory, oppHistory1, oppHistory2):
        return random.randint(0, 1)


if __name__ == "__main__":
    """
    Replace one or two of these with your player!
    """
    from runTournament import scoreGame
    
    p1 = NicePlayer()
    p2 = NicePlayer()
    p3 = NicePlayer()
    NROUNDS = 200
    [s1, s2, s3] = scoreGame(p1, p2, p3, NROUNDS)
    print("========== 3PD Results ==========")
    print(p1.agentName(), " (", p1.studentID(), ") :", s1)
    print(p2.agentName(), " (", p2.studentID(), ") :", s2)
    print(p3.agentName(), " (", p3.studentID(), ") :", s3)
    if p1.studentID() == "42" and p2.studentID() == "42" and p3.studentID() == "42":
        raise AssertionError("DANGER WILL ROBINSON: Make sure you replace one or two of the players with your agent!")
    