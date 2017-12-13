# AI player for Game 2048

### Introduction
This project explored theory and applicability of Minimax, Expectimax, Monte-Carlo Tree Search (MCTS), and reinforcement learning techniques.  While Expectimax shows the best performance with strong domain knowledge, minimax follows with fewer domain knowledge. 

Currently MCTS and Reinforcement Learning has the worst performance with no domain knowledge provided. but they still have large possibility to improve.

what Game_Manager do:

    - Game Init
    - Decide if game is end
    - Clear Board after each move, if can have "clear"

Logic:

    - Four Actions: Up, Down, Left, Right
 
run game 2048 by gui:

	- python3 -i manager.py

### Problem Formulation
2048 is a single-player, nondeterministic sliding block puzzle game developed by Gabriele Cirulli in 2014 The goal of this game is to reach 2048 or a higher number.
![game](https://github.com/kaito4213/2048-Game-Player/blob/master/outputs/images/problem.png)

* STATE: 2048 game board is 4 X 4 grid where the value of each cell is a power of 2.
* ACTION: Swipe to any direction from {UP, DOWN, LEFT, RIGHT}
* RULES:
1. Any two adjacent cells with the same value along merge direction will be merged and add up
2. After each move, the board will randomly generate 1 new cell with value 2 or 4 in available space.
3. Score is calculated when two cells merge together

![rule1](https://github.com/kaito4213/2048-Game-Player/blob/master/outputs/images/move1.png) ![rule1](https://github.com/kaito4213/2048-Game-Player/blob/master/outputs/images/move2.png) ![rule1](https://github.com/kaito4213/2048-Game-Player/blob/master/outputs/images/move3.png)
 
 
### Experiment and Result

We solve the game by using following methodologies:
* Minimax, Expectimax with doman knowledge
* Monte Carlo, Q-learning without doman knowledge

(Note: Minimax, Expectimax, Monte Carlo are also called tree search algorithm)

This is [demo](https://www.youtube.com/watch?v=VYg8peT_-dY) showing the performance of Minimax 

This is [demo](https://www.youtube.com/watch?v=tNzmeJS-h18) showing the performance of Expectimax 

This is [demo](https://www.youtube.com/watch?v=DFlbKxX9g1I) showing the performance of Q Learning 


For minimax and expectimax, the game are dominated by domain knowledge. The AI will have better performance if the depth of search is deeper. Although the system can reach a satisfying result though the carefully designed heuristic function, it is hard to generalize such algorithm because the heuristic in different field are quite different. 
![tree](https://github.com/kaito4213/2048-Game-Player/blob/master/outputs/images/tree1.png)

Comparing all methods, the expectimax shows the best performance while the reinforcement learning has the worst performance, which might because we simplify the reinforcement learning algorithm to reduce the computational complexity and the lack of training times. The performance of Qlearning is expected to be better as the training time increases.
![all](https://github.com/kaito4213/2048-Game-Player/blob/master/outputs/images/rl.png)