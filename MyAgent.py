from prison import Player
import numpy as np

class MyAgent(Player):
    """
    My agent

    Created on Oct 18, 2024

    @author: Kelvin
    """
    #def __init__(self): # default constructor
        
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