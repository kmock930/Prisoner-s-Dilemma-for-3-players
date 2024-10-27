from prison import Player
import numpy as np

class MyAgent(Player):
    """
    My agent

    Created on Oct 18, 2024

    @author: Kelvin
    """
    #def __init__(self): # default constructor
    N_ROUND_TO_FAKE_AFTER_HANDSHAKE = 3;
        
    def studentID(self):
        return "300453668"
    def agentName(self):
        return "My Agent"
    def play(self, myHistory, oppHistory1, oppHistory2):
        if (len(myHistory) == 0 or len(oppHistory1) == 0 or len(oppHistory2) == 0):
            # start by cooperating
            return 0;
        strats: list = [];
        # first-level strategy - based on numbr of defects / coops
        strats.append(self.firstStrat(myHistory, oppHistory1, oppHistory2));

        # second-level strategy - based on ML approach - Markov chains Predictions
        strats.append(self.secondStrat(myHistory, oppHistory1, oppHistory2));

        # third-level strategy - based on some particular patterns of actions from previous round
        strats.append(self.thirdStrat(myHistory, oppHistory1, oppHistory2));

        # fourth-level strategy - logic to backstab an ally's handshake
        strats.append(self.fourthStrat(myHistory, oppHistory1, oppHistory2));
    
        # determine from all strats - by majority vote based on the mean
        action: int = round(np.mean(np.asarray(strats)));
        print(f"My Own Agent takes {action}");
        return action;

    # Strategies set
    def firstStrat(self, myHistory, oppHistory1, oppHistory2):
        '''
        Strategy 1: determine based on both opponents past history (all possible history moves)
        If any player had more defects than coops, then we defect to selfishly get more utility,
        else we coop if both players had more coops than defects
        '''
        currRound: int = len(myHistory);
        finalAction: int = 0;
        if (currRound == 0):
            # start by coorporating
            return finalAction;
        numCoop_opp1: int = self.countFromOpp(oppHistory1, isDefect=False);
        numDefect_oop1: int = self.countFromOpp(oppHistory1, isDefect=True);
        numCoop_opp2: int = self.countFromOpp(oppHistory2, isDefect=False);
        numDefect_oop2: int = self.countFromOpp(oppHistory2, isDefect=True);
        if (numDefect_oop1 > numCoop_opp1 or numDefect_oop2 > numCoop_opp2):
            # Defect if either agent does not play as intended (i.e. defect to ruin the game)
            finalAction = 1;
        return finalAction;

    def secondStrat(self, myHistory, oppHistory1, oppHistory2):
        '''
        Startegy 2: Making an action based on a Machine Learning approach
        with Markov chains
        '''
        predNextMove_opp1 = self.markovPred(oppHistory1);
        predNextMove_opp2 = self.markovPred(oppHistory2);
        # Make decisions based on predictions from both players' history moves
        # if anyone coops, we still give a chance to coop again, otherwise we defect.
        action: int = predNextMove_opp1 and predNextMove_opp2;
        return action;
    
    def thirdStrat(self, myHistory, oppHistory1, oppHistory2):
        '''
        Strategy 3: Deciding whether to coop solely based on special combinations from 1-prev round of game.
        '''
        # define patterns to coop based on this paper:
        # https://www.tandfonline.com/doi/pdf/10.1080/00224545.1969.9922385?casa_token=uqkxPScI7vQAAAAA:3yFOWapSA8vGmsc4xoUdpBJJ_iiTM9gJuMEIAgE8yQe14-aeX5A8jIMzzwx8_Ahvd_y-DkNv6Oxd
        patterns = [
            (0, 0, 0),
            (1, 0, 0),
            (1, 1, 1)
        ];
        for pattern in patterns:
            # comparing my own previous action
            if (pattern[0] == myHistory[-1]):
                # comparing opp 1's previous action
                if (pattern[1] == oppHistory1[-1]):
                    # comparing opp 2's previous action
                    if (pattern[2] == oppHistory2[-1]):
                        # coop only if all conditions of a pattern are met
                        return 0;
        # if pattern does not match, then we defect.
        return 1;

    def fourthStrat(self, myHistory, oppHistory1, oppHistory2):
        '''
        Strategy 4: Deciding whether to backstab an ally after a certain number of rounds in the game, 
        to aim for the best utilities in both situations, i.e., when you coop and when you defect, respectively. 
        '''
        if (len(myHistory) == 0 or len(oppHistory1) == 0 or len(oppHistory2) == 0):
            # start by coop
            return 0;
    
        foundHandshake: bool = False;
        for handshakeStartInd in range(len(myHistory)):
            if (foundHandshake == True):
                break;
            if (oppHistory1[handshakeStartInd] == oppHistory2[handshakeStartInd] == 0):
                # handshake: means both coop
                foundHandshake = True;
        
        currRound: int = len(myHistory);
        if (foundHandshake == True):
            if (handshakeStartInd == currRound - 1 - self.N_ROUND_TO_FAKE_AFTER_HANDSHAKE):
                isAllHandshake = True;
                for i in range(handshakeStartInd, len(myHistory) - 1):
                    # check whether all consecutive rounds are also handshake
                    if (myHistory[i] == oppHistory1[i] == oppHistory2[i]):
                        continue;
                    else:
                        isAllHandshake = False;
                if (isAllHandshake == True):
                    # backstab ally by defecting
                    # benefit of backstab: reward = 8 (max)
                    # assume opponents (i.e. both allies) continue to coop = handshake
                    return 1;
                else: 
                    # situation: not all past actions from the first handshake till current round establish a handshake
                    # rely on strat 3 to determine whether we should give chance or not
                    return self.thirdStrat(myHistory, oppHistory1, oppHistory2);
            else:
                return 0;
        else: 
            # situation: when handshake is not found in past history from both players (i.e., not allies)
            # no handshake, then we rely on strat 3 to determine whether we should give chance or not
            return self.thirdStrat(myHistory, oppHistory1, oppHistory2);

    # util functions
    def countFromOpp(self, oppHistory, isDefect = True):
        '''
        Function that count the number of defects/coops from an opponent's history.
        '''
        countCond: int;
        if (isDefect == True):
            countCond = 1;
        else:
            countCond = 0;
        return sum([countCond for action in oppHistory if action == countCond])

		
    def markovPred(self, oppHistory):
        possibleTransitions = {
            (0, 0): 0,
            (0, 1): 0,
            (1, 0): 0,
            (1, 1): 0
        };
        
        # we can only predict moves having 2 rounds played in the past
        if (len(oppHistory) >= 2):
            for i in range(len(oppHistory) - 1):
                current_state = oppHistory[i];
                next_state = oppHistory[i + 1]; # avoid dividing by 0
                possibleTransitions[(current_state, next_state)] += 1;
            total_transitions_from_0 = possibleTransitions[(0, 0)] + possibleTransitions[(0, 1)] + 1e-5;
            total_transitions_from_1 = possibleTransitions[(1, 0)] + possibleTransitions[(1, 1)] + 1e-5;
            transition_matrix = {
                0: [possibleTransitions[(0, 0)] / total_transitions_from_0, possibleTransitions[(0, 1)] / total_transitions_from_0],
                1: [possibleTransitions[(1, 0)] / total_transitions_from_1, possibleTransitions[(1, 1)] / total_transitions_from_1]
            };

            # Ensure probabilities sum to 1 by normalization, handling zero row_sum case
            for state in transition_matrix:
                row_sum = sum(transition_matrix[state]);
                if row_sum == 0:
                    # If no transitions observed, assign equal probability to each transition
                    transition_matrix[state] = [0.5, 0.5];
                else:
                    # Otherwise, normalize as usual
                    transition_matrix[state] = [prob / row_sum for prob in transition_matrix[state]];
            
            def predict_next(current_state):
                prob_0, prob_1 = transition_matrix[current_state];
                return np.random.choice([0, 1], p=[prob_0, prob_1]); # predict based on probabilities from the past rounds
            current_state = oppHistory[-1];  # Last state in the sequence
            next_prediction = predict_next(current_state);
            return next_prediction;
        else:
            # by default, we coop
            return 0;