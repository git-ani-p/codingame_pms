Since the last contest, I did a considerable amount of practice and I was ready to try out everything that I knew. And I am very happy with the result! 44th and Python!!  
  
__TABLE OF CONTENTS__  
1) Starting out.  
2) First attempts.  
3) Final attempt.  
4) Language changing.  
5) Final approach.  
6) Conclustion.  
  
  
=========================================================   
  
Starting Out  
=========================================================  
  
This contest focussed on an old multi, so I already had a bot (albeit a bad one) in the arena. It was a very basic heuristic wherein I would only look at the known factories.  
  
After looking at the known factories, I gave priority to poorly defended factories( opponent factories with less than 3 pods ). If there were no such factories, move to any neutral. Else WAIT.  
  
That was it to begin with, it brought me till #900. But when I restarted the multi as a contest, I discarded most of the earlier code and kept only the classes and some of the methods.  
You can see this heuristic in the Platinum Rift 2 folder of this repository.  
  
=========================================================   
  
First Attempts  
=========================================================   
  
Usually, search based bots are the ideal techniques for CodinGame contests, I planned to attempt a simulation and search as my final approach. So to start with, I looked at what matters most in this game, aside from having pods and zones.  
  
1) Exploring a lot of the map.  
2) Attacking the opponent's base.  
3) Defending my base when necessary.  
4) Keeping close to the action.  
  
So this was the basis for my first version, which managed a good #150 rank.  
  
The way that I implemented this was:  
A Floyd Warshall with edge weights as 1 when the map was given on the first turn.  
Turn by Turn:  
  
1) Start with a defensive evaluation --> Look at all of the __Current__ inputted zones which are in the control of the opponent, If I think that they are strong enough and close enough to pose a threat to my base, I use the distance matrix to find my closest Zone, use a BFS to find a path, and send all of my pods to the Base.   
  
2) Now an offensive evaluation, I consider each of my zones, if they are close enough to the opponent's base to take it over, assuming that the opponent does not move pods from his base, I apply a BFS and send all of the pods in that direction.  
  
3) Now, I look at each of my zones, and evaluate the adjacent zones based on Criteria (1), (2), (4) that I gave earlier:  
``` 
    def eval_zone(zone_id):
      result = 0
      result += zones[zone_id].platinum * 100000       # Platinum is the most important factor
      result -= 100 * distances[zone_id][opp_base]  # I want to stay in attacking range of the opponent's base.
      result -= 100 * sum(distances[zone_id][zon] for zon in zones if zon.platinum == 0) # If platinum is 0, it is unexplored, and I want to explore it  
      
      result -= distances[zone][centre] # Moving towards edges for the map, keeps you far from the action
      
      return result
```   
  
So I evaluated the adjacent zones like so, and moved to them.  
  
This was written in python and took only an hour to get functional as a bulk of the code was copy-pasted from my Ghost in the Cell bot.  
  
As you can see, the code was quite bloated, and I often ran into timeouts, so when I translated the code to C++, it moved into the top 100.  
  
So far, it was simple enough as the bot did not take any more that 500 lines in python and 800 lines in C++, so I left it in the arena, and I started to focus on a search.  
  
=========================================================   
  
I started off with the naive assumption that I could implement the previously described evaluation function into the search. But this proved to be impossible due to the Fog of War.  
  
I was still confident in the search based bot idea, so I tried to find a way to work around this.  
   
As the fog of war was the main problem, I saw 3 ways to overcome it:  
1) Ignore the opponent pods, so that I can ignore pods death.   
2) Ignore Platinum --> I discarded this immediately.  
3) Explore the map in the early turns, and use the previously described evaluation function.  
  
So I settled on (3) + (1) and went for it,  
  
After a few days, I got the search bug free and tried it against my previous AI in the arena.  
  
I found that I was consistently losing before I finished exploring... This was due to the fact that I completely ignored defense, and the opponent rushed my base and won immediately.  
  
It should have been obvious, but in the excitement of a reasonable approach, I did not consider it thoroughly before implementing it.  
  
=========================================================    
  
Final Version  
=========================================================   
  
I had only 3 days left after the mess up with a search, so rather than a full rewrite, I went back to the previous C++ version and looked for ways to improve.  
  
Small tweaks to the evaluation function allowed me to keep my rank in the top 100, for example: rather than sum(distances), I changed it to 10000 * zones explored - sum(distances) so that I placed a higher weightage on the explored zones, rather than the distance to them. 
  
I made an attempt to assume the maps are symmetric as [CG]SaiksyApo mentioned in the Feedback thread, and found that it became too weak in the occasional paired asymmetric maps that the battles generated.  
  
The best addition that I made was the "Chess" addition:  
  
In Chess, you only make exchanges if you are equal or ahead in the game, so it is not a good idea to attack the opponent's zones, if you are weak. But, I started running into wierd bugs in the C++ version, so I ported back to python and spent a full day optimizing it.  
https://www.techbeamers.com/python-code-optimization-tips-tricks/ is especially useful.  
  
The final submit pushed me to #63 and the repeated submits of others moved me all the way to the top 50.  
  
  
=========================================================   
  
Conclusion  
=========================================================   
  
This contest had an interesting twist of no leagues. Because of this, I could not sit idle with a lucky submit as the submits of very strong AIs like @Siman's pulled me down a lot. Normally, it would be top gold, and the submissions of Legend Level AIs would nt affect me. But this kept my interest up and had a good effect on my motivation.  
  
As for my work, I am happy with my final result but quite disappointed in the time that I wasted trying obviously wrong implementations of the search, Im sure that the top players had better ways of using the search, but I was not able to make it work.  
  

  


    





