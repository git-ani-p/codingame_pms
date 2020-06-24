Here i will detail my thought processes and the way that I go about writing an AI for the codingame multiplayer challenges.  
I will refer a lot to the Fantastic bits postmortem that I had written some time bacck, so it will be better if you read that document before this one.  
  
It is somewhat a reference for myself, so that I can read this keeping my code on the side so that I can easily find logical errors, and perhaps spark new ideas on approaches to these interesting challenges.  
  
==================================================  
  
Language Choice. 
==================================================  
  
I find python to be favourite language to start the challenges, sure it can be slow... but it has so many in-built methods that you can get a very basic AI fully functional within half an hour. Another major advantage of python is its non-typed nature, so you can easily change between integers and strings without much problem. For example:  
```
n = 0
n = 'a'
``` 
This simple snippet will immediately return an error in most of the other languages,  but is allowed in python.  
One thing that is slightly messy in python is the versions, several prominent differences are there in between the second and third versions of python, and I prefer python2 as that is what I started with.  
so.  
It is good to add this piece of code to the beginning of your code to avoid version errors. 
```
from __future__ import print_function  
import sys  
if (sys.version_info.major > 2):  
    xrange = range  
    raw_input = input  
```
==================================================  
  
Starting the work
==================================================  
  
It is always better to start out with a throwaway code in these challenges as new rules are introduced as your AI gets stronger. I realized this in the Spring Challenge, where I immediately thought of a simple search but found it to be extremely ineffective due to the fog of war that was introduced later in the contest.  
  
As the code is a throwaway, it will not be that time intensive, so you can use whichever language you like the best, so python for me.  
  
After I rough out and submit this heuristic, I look at the game and try to break it down to its most basic components. In general, there are 3 such categories to look for.  
1) How do the entities move? --> This is an extremely important element which will affect your basic strategy a lot. Some of the things to consider here are: do they collide, do they move simultaneously, are their movements interrelated. etc.  
2) Do I really care about the opponent? --> This seems strange, as the objecctive is always to win... But winning does not always mean adopting agressive strategies. Consider Smash The Code, you only want to group your blocks as fast as possible, the enemy's action does not matter much.  
3) What is the distance function? --> This can have large impacts, I know several people who during the last challenge, mechanically implemented an Euclidean distance function rather that thinking about it. In general, if the entities move step by step, manhattan distance is more useful. Else Euclidean distance should be preffered.  
  
I keep these principles in mind as I make small touches to the basic AI till I reach Bronze where the rules are usually entirely revealed.  
  
==================================================  
  
Final approach. 
==================================================   
  
At the end of the previously mentioned process, I am in Bronze, and I can go about implementing the other rules and trying out a far more effective class of algorithms called search based algorithms.  
  
The essence of a search based algorithm is pretty simple, I keep generating random strategies for as long as possible, and at the end I use an evaluation function to choose the function which I think is the best.  
  
The reason why search based algorithms are so much better than the basic heuristic algorithms that can also be used is that there are no restrictions. For example, I would never consider using a flipendo spell to push a bludger into my partner wizard in Fantastic Bits, but some times it is useful as it may give him a speed boost to get to his target.  
  
In a search based Artificial Intelligence, there are only 2 components:
1) The move generation  
2) The evaluation function.  
  
In order to quantitatively analyze a move for the evaluation function, it is also necessary to have a simulation to interpret the end state.  
  
==================================================   
  
WRITING THE SIMULATION  
==================================================  
  
Most Sims here broadly have the same framework, but there are obviously some contest specific touches.  
  
The main components that I identified are :  
1) Movement of entities.  
2) Collisions of entities.  
3) Opponent prediction.  
  
1) Entities always move in this way:  
  
entity.x += entity.vx;  
entity.y += entity.vy;   
entity.vx += thrust * Math.Cos(entity.Angle);  
entity.vy += thrust * Math.Sin(entity.Angle);  
   
On occasion, like in Code vs Zombies, entities moved by a fixed amount every time. In this case, thrust = 0 and entity.vx = amount is enough to modify it properly.  
  
2) Collisions of entities.  
  
Magus's document explains how to simulate and play out collisions well enough, I will focus on other aspects of entity collisions.  
  
The main question in terms of collisions is whether or not to consider them. Earlier, I thought that if you spend more time on simulating / computing / playing out collisions, the more accurate your simulation is.  
  
But some benchmarking of performances in the online arena reveals that this is not correct. I added a elapsed_time print to the play(), bounce() and collision() and closest() methods. This revealed that, the closest() and collision() methods take more time considering that they are called a lot more times to see if collisions actually happen.  
  
So, collision time does not directly translate lot of accuracy. So it may still be enough to get a good rank. Check how it works in both cases and then decide.  
   
3) Opponent prediction.  
  
Avoiding opponent prediction gets less and less accurate as you increase the depth of the simulation.  
  
So you obviously need an AI to predict the movements, but there are different ways of deciding which AI to use. The ways to go about this are :   
a) A heuristic AI.  
b) Your own Search.  
  
Using the heuristic AI will be a lot slower as it takes approx 0.1ms per run, that wastes a lot of time, but when you are in lower leagues, it is far more accurate than the search as the opponents may not be that advanced.  
  
Normally using the search to work out the opponent's move means running the search assuming that you wait for about 10 -- 15% of the time and using those moves. This is highly accurate in legend, also it is very time efficient.  
   
Another idea that I have tried experimenting with running the AIs in alternate short intervals so as to get a much more accurate prediction. The idea behind this, is that it will converge to an ideal solution at infinity runs. But this looks like it runs a very high risk of specialization, so it probably better to use the first approach.  
  














