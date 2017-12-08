# 2048-Game-Play
### Abstract
2048 is a sliding puzzle game release in 2014, which was quite popular on mobile devices. This paper discussed the theory and applicability of Minimax, Expectimax, Monte-Carlo Tree Search (MCTS), and reinforcement learning techniques.  While Expectimax shows the best performance with strong domain knowledge, minimax follows with fewer domain knowledge. Currently MCTS and Reinforcement Learning has the worst performance with no domain knowledge provided. but they still have large possibility to improve.

###### Keywords: 2048 Game; Tree Search; Reinforcement Learning.


Have Game_Manager, and Logic

what Game_Manager do:

    - Game Init
    - Decide if game is end
    - Clear Board after each move, if can have "clear"

Logic:

    - Four Actions: Up, Down, Left, Right

### comparison of different algorithms

Movements for all algorithms
![Movements-for-all-algos](/outputs/images/Movements-for-all-algos.PNG)


Maxtile Count for All Algorithms
![Maxtile-Count-for-All-Algorithms](/outputs/images/Maxtile-Count-for-All-Algorithms.PNG)


Average and Best Score for All Algorithms
![Average-and-Best-Score-for-All-Algorithms](/outputs/images/Average-and-Best-Score-for-All-Algorithms.PNG)

run by gui:

- python3 -i manager.py
