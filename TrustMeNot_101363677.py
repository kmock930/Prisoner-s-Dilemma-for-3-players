from prison import Player
import numpy as np

class TrustMeNot(Player):
    """
    My agent - named "TrustMeNot"

    Created on Oct 18, 2024

    @author: Kelvin
    """
    N_ROUND_TO_FAKE_AFTER_HANDSHAKE = 3;
    N_CONSISTENT_ROUNDS = 5; #take 5 rounds to determine whether handshake or not

    def __init__(self): # default constructor
        self.code = [0,0,0,0,0];
        self.handshake = self.ECC();
        self.encoded_code = self.handshake.encode(self.code);
        self.flip = 0; # Used to remember last move
        self.send_bits = [];
        self.mode = 0;
        
    def studentID(self):
        return "101363677"
    def agentName(self):
        return "TrustMeNot"
    def play(self, myHistory, oppHistory1, oppHistory2):
        if (len(myHistory) == 0 or len(oppHistory1) == 0 or len(oppHistory2) == 0):
            # start by cooperating
            self.send_bits.append(0);
            return 0;
        if (len(myHistory) >= 5):
            # update previous move from handshake
            self.flip = myHistory[-1];
            data_bits = oppHistory1[-5:];
            encoded = self.handshake.encode(data_bits);
            decoded = self.handshake.decode(encoded);
            if (all(codeword == 0 for codeword in decoded)):
                # opp 1 is an ally
                pass;
            else:
                self.mode = -1; # attack mode
            data_bits = oppHistory2[-5:];
            encoded = self.handshake.encode(data_bits);
            decoded = self.handshake.decode(encoded);
            if (all(codeword == 0 for codeword in decoded)):
                # opp 2 is an ally
                pass;
            else:
                self.mode = -1; # attack mode

        strats: list = [];
        # first-level strategy - based on numbr of defects / coops
        strats.append(self.firstStrat(myHistory, oppHistory1, oppHistory2));

        # second-level strategy - based on ML approach - Markov chains Predictions
        strats.append(self.secondStrat(myHistory, oppHistory1, oppHistory2));

        # third-level strategy - based on some particular patterns of actions from previous round
        strats.append(self.thirdStrat(myHistory, oppHistory1, oppHistory2));

        # fourth-level strategy - logic to backstab an ally's handshake
        strats.append(self.fourthStrat(myHistory, oppHistory1, oppHistory2));

        # selfish strategy 1: If somebody's defect > coop, then we defect
        strats.append(self.firstSelfishStrat(myHistory, oppHistory1, oppHistory2));

        # selfish strategy 2: Defect to gurantee self utilities if any of the opponents is not an ally
        if (self.mode < 0):
            # defect by default, unless they establish handshake coincidently in n-th rounds
            strats.append(self.secondSelfishStrat(myHistory, oppHistory1, oppHistory2));
    
        # determine from all strats - by majority vote based on the mean
        action: int = round(np.mean(np.asarray(strats)));
        print(f"My Own Agent takes {action}");
        self.send_bits.append(action);
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

    # Selfish strategies
    # If somebody's defect > coop, then we defect
    def firstSelfishStrat(self, myHistory, oppHistory1, oppHistory2):
        '''
        Selfish Strategy 1: If any opponent's defect > coop in history --> then we Defect.
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

    def secondSelfishStrat(self, myHistory, oppHistory1, oppHistory2):
        '''
        Selfish Strategy 2: If both opponents play consistently in n-th rounds cooperatively, then we coop, else Defect. 
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

    # handshaking logic
    class ECC:
        '''
        Implemented by one of the classmates mainly whom I am colluding with.

        @author AgentCipher
        '''
        codeword_dict: dict;
        G: np.ndarray;
        
        # Constructor method
        def __init__(self):
            # Define the generator matrix G (5x15)
            self.G = np.empty((5, 15));

            # Initialize an empty dictionary for codeword lookup
            self.codeword_dict = {};

            # Precompute all valid codewords
            self.precompute_codewords();

        def precompute_codewords(self):
            '''
            Precompute all valid codewords
            '''
            # loop through all possible 5-bit data combinations (0 to 31):
            for num in range(0, 32): # in decimals
                    # Convert integer to 5-bit binary
                    data_bits = '{0:05b}'.format(num);
                    # Encode the 5 bits using the encode method
                    codeword = self.encode(data_bits);

                    if (type(codeword) == list):
                        codeword_str = "";
                        for digit in codeword:
                            codeword_str += str(digit);
                        codeword = codeword_str;
                    # Store the codeword and corresponding data bits in dictionary
                    self.codeword_dict.update({codeword: data_bits});
        
        def hamming_distance(self, cw1: str, cw2: str):
            '''
            Compute Hamming distance between two codewords
            '''
            # Initialize distance counter
            distance = 0;

            prevBit: str = cw1[0];
            # Compare each bit of cw1 and cw2
            for digit_cw1 in cw1:
                if (digit_cw1 != prevBit):
                    distance += 1;
                # update current bit in loop
                prevBit = digit_cw1;
            
            prevBit: str = cw2[0];
            for digit_cw2 in cw2:
                if (digit_cw2 != prevBit):
                    distance += 1;
                # update current bit in loop
                prevBit = digit_cw2;
            
            return distance;
        
        def encode(self, data_bits):
            '''
            Encode 5 bits of data into 15-bit codeword
            '''
            # Validate data_bits length and contents
            if (type(data_bits) == str):
                data_bits_list = [];
                for bit in data_bits:
                    data_bits_list.append(bit);
                    data_bits = data_bits_list;
            if (len(data_bits) != 5 or any(str(b) not in ['0', '1'] for b in data_bits)):
                raise ValueError("Data must be a list of 5 bits.");

            # Multiply data_bits with the generator matrix G to get codeword
            data_vector = np.array(data_bits, dtype=int).reshape(1, -1);
            codeword = ((data_vector @ self.G) % 2).flatten().astype(int).tolist();

            return codeword;

        def decode(self, received_codeword):
            # Step 1: Check if the received codeword matches a precomputed codeword
            if tuple(received_codeword) in self.codeword_dict:
                return self.codeword_dict[tuple(received_codeword)];
            
            # Step 2: If an exact match isn't found, find the closest valid codeword
            min_distance = float('inf');
            closest_data_bits = None;

            # Loop through all precomputed codewords to find the closest match
            for codeword, data_bits in self.codeword_dict.items():
                # Compute the Hamming distance between received_codeword and this codeword
                distance = self.hamming_distance(received_codeword, codeword);
                # Update the closest match if this codeword has a smaller distance
                if distance < min_distance:
                    min_distance = distance;
                    closest_data_bits = data_bits;
            
            # Step 3: Return the closest data_bits
            return closest_data_bits;
        
        def check_early_mismatch(original: str, received: str):
            '''
            Check early mismatch between two sequences
            '''
            # Count differing bits
            diff_count = 0;
            
            # loop through original and received bits
            prevBit = original[0];
            for digit_original in original:
                if (digit_original != prevBit):
                    diff_count += 1;
                prevBit = original[digit_original];
            
            prevBit = received[0];
            for digit_received in received:
                if (digit_received != prevBit):
                    diff_count += 1;
                prevBit = received[digit_received];
            
            # Return true if more than 2 differences
            return diff_count > 2;