from prison import Player

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
        return "Mean Player"
    def play(self, myHistory, oppHistory1, oppHistory2):
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
        print(f"Current Round: {currRound}; And final action: {finalAction}")
        return finalAction;

    def countFromOpp(self, oppHistory, isDefect = True):
        countCond: int;
        if (isDefect == True):
            countCond = 1;
        else:
            countCond = 0;
        return sum([countCond for action in oppHistory if action == countCond])

		
