## What is Multi-agent system ??
A multi-agent system (MAS or "self-organized system") is a computerized system composed of multiple interacting intelligent agents

## what are the components of this project??
 1. Environment : Its a mXn grid.(In GUI its just a mXn buttons with text on it)
 2. Agent : Its an autonomous entity which acts, directing its activity towards achieving goals.

## how  multiple Agents was simulated ??
I have used mutithreading to simulate multiple agent(one thread for each agent) and avoid collisions i have used locks on grid.

## How agent decides the next move??
Agent have a sensor which tells the distance from the target .
Using this sensor agent goes to the path which takes agent toward the target.

## File descriptions

- a) In the  grid world of size m*n with no obstacles. there is  an environment and agent class. The agent has a position sensor that gives the (x,y) coordinates of the agent at any time. The agent is moved by the actions left, right, up and down. The goal coordinates are known in advance. 
- b) Goal coordinates are not known but there is a sensor that detects the distance to the goal.
- c) It simulates 10 agents like these concurrently. It ensures that agent do not collide. 
- d) In this  10% times the agent does not move, even though the action command is given.

## How to run the project??
Just the run the file you want by using following command -  

python fileName.py

## which libraries are used??
- tkinter
- time
- threading
- random
- time
