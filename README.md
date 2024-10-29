# TrustMeNot Agent
This agent is a strategic agent maximizing cumulative rewards through a combination of cooperative and self-serving tactics. It takes an action proposed by a majority vote. TrustMeNot colludes with “AgentCipher” and “Monkey” to explore collusion possibilities.
## Packages and Dependencies
- Install numpy with `pip install numpy`
## Core Strategy Set
1. **History Comparison**: This strategy evaluates each opponent’s past defections and cooperations, deciding the current move based on the overall history.
2. **Markov Chain Predictions**: This strategy leverages a Markov Chain-based machine learning model to predict future opponent moves, by analyzing patterns in each opponent’s history for tailored response predictions.
3. **Special Combinations**: This strategy decides whether to cooperate solely based on some special combinations [1] from the most recent round of the game. The approach adapts to this 3-player game. Interestingly, TrustMeNot avoids forgiving an opponent if betrayed in the previous round, preventing unintended cooperations that could lead to exploitation. [2]
4. **Backstabbing an Ally**: TrustMeNot enjoys the best utilities in both situations, when you coop and when you defect, respectively.
- Interestingly, the best situation when you defect is when other players cooperate. This outcome yields a utility of 8, however, it is nearly impossible. [2]
- The only way to achieve this is to “fake a handshake”, which suggests firstly establishing trust with players, and then defecting suddenly after 3 handshaking rounds. In such way, the supposed “allies” will not adapt to the agent’s backstabbing quickly and thus, it gets a chance to attain the maximum possible utility in the game in this 1 round, while as well consistently enjoying a utility of 6 through handshaking. 
## Selfish Strategy Set
These strategies prioritize maximizing TrustMeNot’s own profit without considering cumulative group benefits.
1. **Defection based on Opponent History**: If any opponent’s history contains more defections than cooperations, TrustMeNot will defect.
2. **Conditional Detection**: If an opponent shows inconsistent cooperation over a five-round period, or if identified as untrustworthy through the handshake process, TrustMeNot will defect to secure its own rewards.
## Handshake
What defines a “handshake” is when all players play coop successfully in a round. 

Inspired by the mathematical approach developed by Abdullah Mostafa in "AgentCipher" [3], I implemented a handshaking algorithm using Error Correcting Code (ECC). ECC is a cryptographic method that detects and minimizes errors during data transmission, enhancing security by preventing external parties from predicting handshake values. This method is widely used in telecommunications to ensure data accuracy, making it well-suited for establishing secure communication between colluding agents.

Our colluding agents have been tested and compromised a 5-bit code encoded with ECC, allowing the system to recognize ally patterns even in noisy environments. For simplicity, scalar-based matrix multiplication is applied, as complex encryption isn’t the primary focus. Allies use a 5-round pattern of actions, each encrypted and checked internally by each agent for a match. By comparing bits with the compromised code, we allow errors in at most 2 bits. If a match is identified, the opponent is considered an ally; otherwise, TrustMeNot takes its selfish strategy to maximize individual rewards.
# References
[1] James T. Tedeschi, Douglas S. Hiester & James P. Gahagan, "Trust and the Prisoner's Dilemma Game," pp. 43-50, 30 06 2010.

[2] K. Mock, "The Incentive to Cooperate with other agents," 23 10 2024. [Online]. Available: https://brightspace.carleton.ca/d2l/le/292860/discussions/threads/653279/View.

[3] A. Mostafa, "Encoded handshakes for a fairly robust collusion strategy," 28 10 2024. [Online]. Available: https://brightspace.carleton.ca/d2l/le/292860/discussions/threads/655392/View.