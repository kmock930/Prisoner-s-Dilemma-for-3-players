from prison import Player

class SampleAgent(Player):
    """
    This is an example player
    """
    #def __init__(self): # default constructor
        
    def studentID(self):
        return "000"
    def agentName(self):
        return "Mean Player"
    def play(self, myHistory, oppHistory1, oppHistory2):
        return 1;
		
