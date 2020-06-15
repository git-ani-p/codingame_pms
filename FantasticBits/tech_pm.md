**Preface  
----------------------------------------   
  
Here I will only detail my final solution, it will not contain ideas or options to improve, it explains how to put forth the code for a genetic algorithm. It looks like a similar approach will be very useful in making a GA for Mean Max which has a very similar mechanic.  
  
As Magus explained most of the simulation, I will only focus on what is different. 
  
----------------------------------------   
  
Table of Contents:  
1) Spells 
2) Genetic Algorithm  
3) Evaluation Function  
4) Dummy AI
  
----------------------------------------   

**Spells  
----------------------------------------    
  
This is a new addition in fantastic bits and it can be divided into two categories:  
1) Force based : FLIPENDO and ACCIO.  
2) State based : OBLIVIATE and PETRIFICUS.  
  
FORCE BASED:  
Flipendo and accio are both force based actions, all I do is apply the given formula and divide by the mass of the entity. After this, it is exactly how I apply MOVE and THROW.  
  
STATE BASED:  
OBLIVIATE : I have a forbidden list in the bludgers which I append my wizards to.  
PETRIFICUS : set vx and vy to 0.  
  
----------------------------------------   
  
**GENETIC ALGORITHM  
----------------------------------------   
  
It was a necessity as explained in the postmortem, there are 2 ways to evolve a solution:  
1) Mutation : This is done by passing an amplitude to a mutation method. I create a random number between angle +- amplitude 
the amplitude was initially inversely proportional to the score so as to modify a bad solution more, but I went with what most people advice and mutated based on the generation number.  
2) Crossover : Take a pair of solution and for the child solution --> for each of the genomes, pick a random of the two solutions and select the gene from there.  
  
----------------------------------------   
  
**Evaluation function  
----------------------------------------   
  
This was something that I picked up in physics, to build a formula find the dependant parameters and multiply them by derived constants.  
  
Unfortunately my judjement of the game state is entirely qualitative, so after watching a couple of top replays I found that the following variables are the most important.  
1) How close am I to my closest Snaffle.  
2) Proximity of the snaffles to either goal.  
3) Having Magic.  
4) OBVIOUSLY scored snaffles.  
5) distance between my wizards so as to cover as much of the map as possible.  
  
----------------------------------------   
  
**Dummy AI  
----------------------------------------   
  
A reasonable approximation that can be made in coders strike back is that the opponent continues on his own trajectory, this will work out without much problems as We use a small depth and collisions are quite rare.  
  
But in Fantastic Bits, it is necessary to go to a high depth to evaluate spells, so the approximation becomes very off in these cases. Hence we need to have a reasonable but time efficient prediction of the enemy.  
  
As I started in Silver, I assumed that everyone moved exactly like the Bronze Boss --> Move to closest snaffle and throw at goal as hard as possible.  














