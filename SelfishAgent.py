from prison import Player
import numpy as np

class SelfishAgent(Player):
    """
    This is a selfish player who by default plays a Defect strategy.
    """
    #def __init__(self): # default constructor
    N_CONSISTENT_ROUNDS = 5; #take 5 rounds to determine whether handshake or not

    def studentID(self):
        return "300453668"
    def agentName(self):
        return "Selfish Player" 
    def play(self, myHistory, oppHistory1, oppHistory2):
        # base case 
        if (len(oppHistory1) == 0 and len(oppHistory2) == 0):
            # start with defecting
            return 1;
        strats = [];
        # 1st level strategy
        strats.append(self.firstStrat(myHistory, oppHistory1, oppHistory2));
        
        # 2nd level strategy
        strats.append(self.secondStrat(myHistory, oppHistory1, oppHistory2));

        # determine from all strats - by majority vote based on the mean
        action: int = round(np.mean(np.asarray(strats)));
        print(f"Selfish Agent takes {action}");
        return action;
    
	# Strategies set
    # If somebody's defect > coop, then we defect
    def firstStrat(self, myHistory, oppHistory1, oppHistory2):
        '''
        Strategy 1: If any opponent's defect > coop in history --> then we Defect.
        '''
        # predict if someone's gonna defect/coop 
        # with the mean of his history
        if (len(oppHistory1) > 0 and len(oppHistory2) > 0):
            # defect > coop: mean will be rounded to 1
            predOpp1:int = round(np.mean(np.asarray(oppHistory1)));
            predOpp2:int = round(np.mean(np.asarray(oppHistory2)));
            # return 0 if the mean tends to 0, otherwise return 1
            return max(predOpp1, predOpp2);
        else:
            # defect by default
            return 1;

    def secondStrat(self, myHistory, oppHistory1, oppHistory2):
        '''
        Strategy 2: If both opponents play consistently in n-th rounds cooperatively, then we coop, else Defect. 
        '''
        isCoop:bool = True;

        if (len(oppHistory1) < self.N_CONSISTENT_ROUNDS or len(oppHistory2) < self.N_CONSISTENT_ROUNDS):
            # we by default defect
            return 1;

        # considering opponent 1
        opp1_prevAction: int;
        for consideringRound in range(len(oppHistory1)-1, len(oppHistory1)-1 - self.N_CONSISTENT_ROUNDS, -1):
            if (consideringRound < len(oppHistory1) - 1):
                # the first prev round in consideration
                opp1_prevAction = oppHistory1[consideringRound+1];
            else:
                # we assume handshaking in the first round without further history stats
                continue;
            # current round's action = previous round's action
            isCoop = isCoop and opp1_prevAction == oppHistory1[consideringRound];
        
        # considering opponent 2
        opp2_prevAction: int;
        for consideringRound in range(len(oppHistory2)-1, len(oppHistory2)-1 - self.N_CONSISTENT_ROUNDS, -1):
            if (consideringRound < len(oppHistory2) - 1):
                # the first prev round in consideration
                opp2_prevAction = oppHistory2[consideringRound+1];
            else:
                continue;
            # current round's action = previous round's action
            isCoop = isCoop and opp2_prevAction == oppHistory2[consideringRound];
        
        # determine the action
        if (isCoop == True):
            return 0;
        else:
            return 1;