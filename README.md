# TrustMeNot Agent
This agent is designed to leverage both cooperative and self-serving strategies to maximize cumulative utility across multiple rounds.
## Core Strategy Set
1. This strategy decides each move by comparing the cumulative history of defections and cooperations from both opponents.
2. A Markov Chain-based strategy, which is a Machine Learning based approach, predicts future moves by analyzing each opponent’s historical patterns from the history of each opponent respectively.
3. A strategy decides whether to cooperate solely based on some special combinations [1] from the most recent round of the game.
- This implementation adapts the combinations to a 3-player game.
- Specifically, we do not apply one combination to TrustMeNot: it cooperates in the previous round; and is being betrayed by either opponent; causing it to “forgive” that one opponent by cooperating again. This setup prevents counterproductive forgiveness scenarios. [2]
4. Strategy 4: Since the agent relies on a technique which handshakes with 2 other agents, it decides whether to backstab an ally after 3 handshaking rounds, to aim for the best utilities in both situations, i.e., when you coop and when you defect, respectively.
- Interestingly, the best situation when you defect is when other players cooperate. This outcome yields a utility of 8, however, it is nearly impossible. [2]
- The only way to achieve this is to “fake a handshake”, which suggests firstly establishing trust with players, and then defecting suddenly after 3 handshaking rounds. In such way, the supposed “allies” will not adapt to the agent’s backstabbing quickly and thus, it gets a chance to attain the maximum possible utility in the game in this 1 round. 
## Selfish Strategy Set
These strategies prioritize maximizing the agent’s own profit without considering cumulative group benefits.
1. In any opponent’s history, if the number of defects is played more than the number of coops, then the agent defects.
2. This strategy is played conditionally. Under the condition when the agent identified any opponent to be an enemy in a handshaking technique, If any opponent’s history reveals inconsistent cooperation over 5 rounds, the agent defects.
## Handshake
Using the mathematical approach suggested by “AgentCipher,” I implemented a handshaking algorithm based on Elliptic-curve Cryptography (ECC), a key-based encryption method commonly used in secure communications. [3] ECC prevents other parties from predicting the resulting value, enhancing the security of communication. [4] Additionally, scalar-based matrix multiplication simplifies the handshaking algorithm, as complex encryption is not the agent’s main focus. [5]. Allies communicate through a specific 5-round action pattern, with each action encrypted and sent to an ally each round. Internally, the agent decrypts the codeword and checks for a pattern match. If matched, the opponent is identified as an ally; otherwise, TrustMeNot activates its second selfish strategy to protect its rewards. 
# References
[1] James T. Tedeschi, Douglas S. Hiester & James P. Gahagan, "Trust and the Prisoner's Dilemma Game," pp. 43-50, 30 06 2010.
[2] K. Mock, "The Incentive to Cooperate with other agents," 23 10 2024. [Online]. Available: https://brightspace.carleton.ca/d2l/le/292860/discussions/threads/653279/View.
[3] "vmware by Boradcom," [Online]. Available: https://www.vmware.com/topics/elliptic-curve-cryptography. [Accessed 28 10 2024].
[4] A. Menezes, P. v. Oorschot and S. Vanstone, Handbook of Applied Cryptography (5th ed.), CRC Press. ISBN 0-8493-8523-7., 1997.