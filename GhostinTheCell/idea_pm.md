TODO : ADD tech_pm, FINISH this.  
As in Fantastic Bits, I will be splitting this into two post mortems, this one will contain ideas that I considered, used, discarded and those that can be used in the future.  
  
__Table of Contents__  
1) Introduction.  
2) To Bronze.  
3) Deciding the approach.  
4) What Worked.  
5) What did not.  
6) How to Move ahead.    
  
==================================================  
  
Introduction.  
==================================================  
  
Ghost in the cell is a different contest from those that I normally enjoy(Physics based) but I enjoyed making an AI for it nevertheless. Here I will detail the AI evolutions only in terms of ideas, the code and technical details will be given in the technical Post Mortem.  
  
==================================================  
  
To Bronze  
==================================================  
  
This was unlike the other contests as I really struggled on my way to Bronze. This can be seen from the bloat in my Wood12Bronze code. It was more from misunderstanding the rules than anything else, I thought that the link start and end points were fixed, this kept me in the top of Wood2 for over an hour, until a minor modification got me through.  
What was earler this,  
  
```
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    links.append(link(factory_1, factory_2, distance))
```  
   
Became this.  
```
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    links.append(link(factory_1, factory_2, distance))
    links.append(link(factory_2, factory_1, distance))
```   
The reason this had such a large impact is that, the code would only consider a link to a factory if I am the start point, as I thought that start and end where relevant. It was actually a two sided link with the lower number factory given first.  
  
For this reason, I was completely unable to attack lower numbered factories as my code thought that there was no path to them.  
  
The basic logic that I applied to get till bronze was completely intuitive.   
1) If there are neutral factories, attack them.   
2) If I want to attack the opponent, take his factories in ascending order of strength, for each of his factories, I consider all of my factories. I look at the distance between my factory and his, multiply the distance by production to get his final strength, if I can send more than that... I send that many.  
  
This was probably enough to get till bronze without the previously mentioned error, but I added bombs thinking that they were what was holding me back.  
  
The bomb logic is simply looking at all secure factories and seeing if they have production and cyborgs above a threshold.  
  
==================================================   
  
Deciding the approach  
==================================================   
  
After getting to bronze we find the latest updates, these are bombs and increasing.  
  
Now, the general approach in such contests is a Search Based AI. So I started thinking about a Search immediately.  
  
On the surface, the game is absurdly easy to simulate, the rules are very well defined and simple subtraction takes care of troop movements. The evaluation function will also be equally simple, the factories and troops are the only important data, so this is the way that we can go about it.  
```
∑(factory * factory_value) + ∑Troops - ∑(opp_factory * opp_factory_value) - opp_bomb_count
```  
So the only thing left to do is to define a solution...  
This proved to be the most frustrating part of the AI, what is a solution??   
   
coding abilities like INCREASE and BOMB can be done using the genome pairing technique that I used in Fantastic Bits, have a single genome for moving troops and another for abilities.  
  
But what is a moving genome? Some of the methods that I considered were :  
1) Each factory has a tuple as a Move, WAIT means moving 0 of its troops.
   This is not a good Solution for an important reason --> Factory collaboration becomes very difficult, I may want to send 10 cyborgs from Factory 1 to take over Factory 2, after this, 5 cyborgs from Factory 1 and 3 cyborgs from Factory 3 to take over Factory 4.  
   But, according to the genome, a single factory can only move 1 set of troops to one factory. Hence this idea was discarded.
   
  2) Every one of my cyborgs that is not already on the move has a factory target, targeting its own factory translates to a wait.  
  This seems reasonable but for one problem, you are playing to win, so by the end of the match it is not uncommon to have over 300 troops.  
  Let us derive the sample space for this search.  
  ```
  Let the number of stationary troops be 'T'
  Let the number of factories be 'N'
  Each troop can move to all of the N factories( including its own for a WAIT )
  ==> A troop has N potential actions.
  ==> For all the  troops, the potential actions is :
  N * N * N... (T times)
  ==> N ** T
  ```
  So there are N ** T potential actions. There are on an average 5 -- 7 factories and to win, you may need upto 400 Troops.  
  Assuming that 80% remain in their factories, there are 320 Considered troops.  
  ==> the size of the search space if you want to win, is 5 ** 320. It is not possible to search a reasonable amount of this in    50 ms even with Genetic improvements. At its most optimized state, it may not cross a local maxima(as you will mutate to reach local maxima and plateau there). Worst case, you have purely random movements.  
   
3) Have a group value of an amount to reduce the sample space by that factor. This is an interesting approach but it fails in the end.  
  
To apply this, you have to find the delicate balance between sending the "Just enough" amount of troops in certain cases, but also reduce the search space to a reasonable amount.  
```
Now, we modify the formula, T --> T / K where K is the number of cyborgs per group.  
==> Formula becomes N ** (T / K).  
Taking the mean winning case, 5 ** (320 / K).  

As the simulation is very simple, it is by extension very fast. The most optimized version of Coders Strike Back can run 20 thousand simulations at a depth 7.  

Extrapolating this, we can probably achieve 50 thousand simulations at a depth 7. This translates to 70K at depth 5.
I experimentally found that with mutations, searching 10 -- 12% of the sample space is required to get a reasonable search.
so if 70K is 10 %, the search space needs to be 700K at the maximum.

Taking log of 700K to the base 5(mean number of factories), we get 8.3624447455.
So T / K needs to be 8.36, and substituting the mean value of T,
320 / K = 8.36
==> K = 320 / 8.36 = 39
This is too large a value of a group, you rarely send more than 15 cyborgs to a single factory, hence this approach is mathematically wrong.
```  
  
For these reasons, I think that a search based bot is impractical and would not be that much better than a random one, so a heuristic bot is required.  
  
==================================================   
  
What worked  
==================================================   
  
Reading Agade's post mortem gave me a couple of ideas, the one that I used effectively is the Floyd Warshall algorithm.  
  
I will not explain the algorithm here, geeksforgeeks does that better, I used it to calculate paths to factories that are not linked, as well as calculating alternate paths through linked factories.  
  
This has the advantage of changing your mind in the middle, like if a factory suddenly gets reinforced, there is no point in foolishly going ahead with your plan to attack that factory. This allows you to attack unlinked factories as well.  It allowed me to move till mid - Silver.  
  
The next change was simulating turns to see what the best move would be, I simulated turns exactly as I described it in the earlier chapters.  
  
This allowed me to predict the gamestate, and it obliterated the Silver Boss and I made it till bottom gold.  
  
In terms of the BOMB, I simply bombed "Above Average" factories, i.e the factories that had above the mean number of cyborgs and above the mean production amount.  
   
==================================================   
  
What did not work  
==================================================   
  
I made some attempts that really messed up the code and even after debugging did not improve the rank at all.  
1) Storing the previous moves and applying them on the next turn. It seemed like a good idea at the time, but I eventally realized that it just ruined the effects of the Floyd Warshall algorithm. The main point of the Floyd Warshall algorithm was to allow me to change my mind in the middle of moves, but if I store my previous, moves, this prevents that from happening. Instead, if a move is still the best move, mt AI will find it anyway on the next turn.  
   
2) Bomb troop thresholds. I thought that having a bomb troop threshold should be a lot more effective than randomly bombing, but I ended up bombing obvious targets and they ran away, it was not at all effective, attacking above average factories worked a lot better.  
   
==================================================   
  
Ideas to move ahead.  
==================================================   
  
At the moment, my factories do not collaborate too well. My factories essentially battle one vs one. In the sense that, I attack one factory from only one factory. So I cannot group actions together. This will probably be the key to get to Legend.    
Other than that, I have not at all implemented INCREASE, probably will be a good idea to increase only when the opponent does not have bombs, this will ensure that my INCREASED factories cannot be taken easily.  










