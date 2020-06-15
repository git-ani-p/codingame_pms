Table of Contents:  
  
1) Preface  
2) Introduction.  
3) Heuristics to start.  
4) Basics.  
5) What is different from CSB.  
6) What I considered.  
7) What I chose to do.  
8) How to move forward.  
9) Conclusion.  
  
  
**PREFACE  
----------------------------------------  

Fantastic bits was similar to CSB in several ways, so I will not explain what Magus explained in his document, rather I will focus on the basics which will lead up to Magus's document, then I will move onto what is different and other such characterestics of the game.  
  
Feel free to consult my code, dont try cheating as you will definitely be caught. This postmortem mostly discusses the approach that I took and how I could improve on it. I will be adding a second post mortem which will be a lot more technical to this repository.  
   
=========================================  
  
**Introduction  
----------------------------------------  
  
Fantastic bits had a highly complex game to simulate and even after the simulation is built, it is quite difficult to optimize, I still have not perfected the simulation engine yet. For this reason, I managed to get reasonably far (Top Silver) using pure heuristics. For this reason, I will explain my heuristic methods as well so that it gives a good base of how I approached the game.  
  
----------------------------------------  
  
**Heuristics to start with  
----------------------------------------  
  
Heuristics is basically an if/else approach with some sorting and searching. So here I implement basic logic to get as far as possible.   
  
As if-else logic is very fast, I did not need to use Object Oriented Languages. For this reason python suited my needs perfectly as a lot of the in built functions were perfect for what I wanted to do.  
  
Till Bronze:  
I move to the closest snaffle at highest power, and throw it at the goal with max power if I am holding a snaffle.  
  
Including Spells:  
The game gets a bit more complex at this point, to start with I chose to ignore the opponent entirely until I get the basic parts ready. For this, referring to the code that I attached and Bob's be lazy and keep things simple will make it perfectly clear.  
  
----------------------------------------   
  
   
**Basic stuff.  
----------------------------------------  
  
While Heuristics is a very useful way of determining your actions, search algorithms(when properly used) can be a lot more useful.  
  
The basis for a search algorithm is that we generate a random strategy, evaluate how good it is and at the end of a given time period, print out the best plan that we found.  
  
Here, 100 milliseconds is a considerable amount of time for a program to run, so search algorithms seem to be ideal. Now that we have decided on the ideal strategy, we can further split it into what we want to do.  
  
1) What is a strategy?  
2) How do we evaluate a strategy?  
  
I struggled with the first part, so I will explain it in detail in the following chapters, for now I will explain how I judged a strategy.  
  
As we cannot apply judgement and look at how good a strategy is, Our program should be able to evaluate the strategy quantitatively rather than qualitatively. So we need to break down the strategy into a bunch of numbers.  
  
The best way to do this is look at the game state that following this strategy leads to. After this we extract information from this game state and use this data in our scoring of a strategy.  
  
In order to learn how to build a simulation, the physics and mathematics of the simulation are surely explained better in Magus's CSB document http://files.magusgeek.com/csb/csb_en.html.  
  
----------------------------------------  
   
     
**What is different from CSB  
----------------------------------------  
  
CSB is Coders Strike Back, it is the most basic bot programming to start with as it is extremely easy to simulate.  
Even though almost all of the simulation is identical to that of CSB, it is a lot more difficult to manage the simulation engine for Fantastic Bits.  
1) Closed map : The closed map adds another type of collisions to the list.  
2) A lot more entities : There are several extra entities to consider so the simulation gets a lot slower.  
  
While game information is given turn by turn, the game essentially moves collision by collision. This is due to the fact that collisions basically change the characterestics of the entities and can lead to different gamestates. Because of the added entities and the closed map, there are a lot more collisions so the collision by collision movement is VERY slow.  
  
----------------------------------------   
  
**What I considered:  
----------------------------------------   
  
I am new to the search algorithm process for any project and the only other thing that I have been able to produce is a highly bugged Monte Carlo Search for Coders Strike Back.  
  
As it was my first attempt, I tried to start at the most basic level possible-->  A purely random search hat did not simulate collisions or spells.  
  
While this may produce a reasonable AI, I doubted whether it was enough to make it to Gold without spells. So spells were an absolute neccessity.  
  
Now I hit a roadblock... How to encode a spell into a genome( A move/plan )??? While this may seem trivial to the top coders on the website, it was quite tough for me. I considered a number of approaches and all of them seemed deeply flawed.  
  
The main issue with this is the fact that you may not be allowed to cast the spell that you want to...  
  
1) Massive penalty for negative magic --> I have a large weight on the magic aspect of the evaluation function, I thought taht this would ensure that using magic that I dont have would be so harshly penalized that it could not possible be a good move. This was an idea that I discarded quickly as it may make the AI too conservative in its spell casting, may as well not code spells....  
  
2) if-else in the simulation --> I generate the spells in the Solution, but I dont perform them if they are not allowed.
                                 On the surface, it seems like a good idea, but if you think about it, it will produce pretty                                  random movements, I will waste too much time trying out moves that make no sense, like        flipendo without magic etc. and if I increase the probability of selecting "NO SPELL" it is back to Square 1.  
      
3) The "CSB" approach --> Like how Magus applied SHIELD in CSB, I would have a probability of each spell. This was not at all an improvement over option (2), I discarded it immediately.  
  
What I finally did was have 4 genomes rather than 2, a pair of genomes for each Wizard. Genome 1 is a move, Genome 2 is a spell. They are evaluated seperately and the better between the two takes priority.  
   
The next thing that I got stuck with was collisions : As I said earlier, the game essentially advances collision by collision rather than turn by turn. So if I evaluate 8 turns into the future, it may become 16+ "COLLISION TURNS". Given that I am not familiar with fast languages like C/C++ and only learn Java in school, it would be extremely heavy on performance.  
  
  
----------------------------------------   
  
**What I finally did:  
----------------------------------------   
  
Those two problems kept me occupied for a long time. So I eventually decided that a simple Monte Carlo wasnt going to cut it this time, it was going to have to become "evolutionary".  
  
Evolution is an excellent way of improving your search, what it does is that it allows you to converge to a good plan faster than a pure random.  
  
I will detail the evolution in my technical postmortem, here I will only give the bare essentials.  
  
What evolution does is that it only makes modifications to the previous solution to form a child solution rather than the following solution being generated at pure random. so a good solution is more likely to be improved rather than a new terrible solution like shooting at your own goal being evaluated.  
  
Why Evaluation?? I have a suboptimal language choice of Java which I hoped to convert to C# but was not able to change some of the features that I used, so with a lower amount of simulations, I was able to improve on a solution and hence required less simulations to reach a viable plan. This accounted for the poor performance to a certain extent.  
  
This accounted for the poor performance and the genome pairing advanced my spell usage.  
    
----------------------------------------   
  
**How to move ahead  
----------------------------------------   
  
As I mentioned earlier, there are very few components of a search based algorithm : Its move generation and its evaluation function.  
  
By virtue of the problem statement, the code is further divided into the following categories:  
1) Simulation Engine.  
2) Opponent Prediction.  
3) Evaluation Function.  

THE SIMULATION ENGINE:  
  
I am extremely unhappy with the simulation engine that I used; It is practically all bloat and I got frustrated while writing it so it is very inefficient.  
   
I learnt while trying a similar approach in Coders Strike Back, that the number of simulations that you perform is not as important as the number of IMPROVED simulations. Hence I have not bothered checking the number of moves generated and only looked at the number of improvements.  
   
This is usually around 45 -- 65, which I believe is too low for it to be effective.  
   
In order to fix this, the following things need to be done.  
1) Precompute as many values as possible.  
2) Optimize division.  
3) MOST IMPORTANT : Translate to C#/C/C++, these languages have inlining and hence are much faster.  
  
OPPONENT PREDICTION  
   
I have detailed the dummy class and its usage in the technical post mortem.  
  
I believe that the way that the dummy class has been coded is terrible... From my understanding, it is a terrible idea to have a deterministic( no random element ) dummy AI. I think that this will lead to specialization, while this may not affect in Bronze and Silver where everyone practically uses the same approach, it should wreak havoc in gold and legend where the approaches are more varied.  
  
It is recommended to run the search for your opponent for 10% of the time and use that as the dummy. I do not do this as my simulation engine is slow and 10ms will result in a random move most of the time.  
  
EVALUATION FUNCTION  
  
This part of the code is where the least improvement can be done. I have detailed the evaluation function and my reasoning behind it in my technical postmortem.  
  
I think that this may be good enough provided that the rest of the code is fixed.  
  
  
----------------------------------------   
  
**CONCLUSION  
----------------------------------------   

The code is rather bloated and inefficient as I got frustrated with the implementation. While there are several ways that this can be improved, I am still glad to have made my first bug-free Search Based Artificial Intelligence.  
  
   
  
  


















