__In this readme I will detail my solution to the code vs Zombies challenge on codingame  
If you can read and understand this document, you will be able to make the modifications necessary to implement the solution in this folder.__  
  
__TABLE OF CONTENTS:  
    1) Mathematics involved (Movement of entities)  
    2) Simulation technique  
    3) Monte Carlo Search  
    4) Flow of code and linkage  
    5) Road forward__    
      
__CHAPTER 1 --> MATHEMATICS INVOLVED : MOVEMENT OF ENTITIES__    
  
Here, there was not much mathematics involved in the puzzle. But the majority of it was in the movement of the different entities.     
  
The movement of entities extremely rigid: it had a fixed distance that it can move and there were no side variables, but still it is not obvious how to limit its steps. So I decided that instead of the Cartesian Coordinates that were given, I would use Polar coordinates which involve distance and angle instead. This greatly simplifies the problem as Polar Coordinates are made for such computations
    
  
The movement function for the entities looks something like this  
      
    
 ```
float slope = (float) ( ( this.y - this.target.y ) / ( this.x - this.target.x ) );   
float theta = (float) Math.Atan(slope);  
this.x += (float)  Math.Cos(theta) * this.dist_per_turn;  
this.y += (float) Math.Sin(theta) * this.dist_per_turn;  
   ```
    
Polar coordinates use distance from origin and angle with x axis rather than x and y positions to depict a coordinate.  
  
So, I found the slope using the dy/dx method and after this the inverse tangent function of the Math module gives the angle with x axis. Now, we have the theta of a polar coordinate. The distance is easy as an entity can only move by a fixed amount of units per turn.   
After this, we convert back to cartesian and add to the respective components.  
  
  
__Chapter 2: Simulation techniques__    
  
So now that we know how an entity moves, it is quite simple to simulate a turn.   
The rules make it exceptionally easy to simulate a turn for the following reasons:  
    1) No collisions! Multiple entities of the same type are allowed to occupy the same point!  
    2) Ease of identifying target: Zombies work independantly, so identifying their targets needs little work    
    
Now, we will look at the simulation of an entire turn   
  
It is given in the turns that the ordering of events follows the following fixed pattern:  
    1) Zombies move towards their targets.  
    2) Ash moves towards his target.  
    3) Any zombie within a 2000 unit range around Ash is destroyed.  
    4) Zombies eat any human they share coordinates with.    
  
So following these events,  
The get_target method of the zombie class identifies the closest human. In this method, we use square distance as it is called quite often during a turn and the square root method involves a complex formula that involves a while loop and hence is considerably performance heavy. The significance of (&) performance will be discussed in the following chapter.  
    
    
The moveto_target moves 400 units towards the target in the manner discussed in the previous chapter.    

The (&&) movement of Ash is slightly more complex and will be discussed in the following chapter on Monte Carlo Tree Search, for now it is suffice to say that it recieves a parameter that gives it the target to move towards and again, in a similar way, the moveto method of Ash moves 1000 units towards the target.   
  
After this, any zombie that is in the 2000 unit radius of Ash is killed.  
The killing is done by turning the 'alive' flag in the entity method to false. after having done this, we simply add an if to all of the following for loops that checks the 'alive' flag before performing any action on the zombie.  
Again here, we use the square distance method to save performance. While the square of 2000 can be pre calculated, the * operator is quite fast so it really makes little difference.   
( If you want to know which operators are fast and which are slow, think of what logic the operator runs on, if it seems like a while loop is necessary--> it is performance heavy. By this logic, the / operator is also slow )  

Now, here in the kill_humans method of a zombie, there is an approximation used where we kill any zombie in the killing radius of a zombie( Here it is 400 Units ). This approximation aids in the (&&) scoring function which which will be discussed in the following chapter.  

Now the above methods will be executed in order for a single turn in the play() method of the Player class.  

__CHAPTER 3 : MONTE CARLO SEARCH__    
  
This chapter is the essential "BRAIN" of the program.   
The basic logic of the search is simple, create a random sequence of 9 moves and simulate the moves.   
  
Now, the creation of the moves is quite simple, but there are some subtleties that have a large impact. For now, we will focus on the logic and the syntax related information will be put in the following chapter.  
  
So, the only movement that we can choose is the movement of our player: Ash. So, we can use the following ways to define a move:  
    1) Using the previously discussed polar technique, we can generate a random angle from 0 to 360, and a random distance            from 0 to 1000 and have Ash move towards that point.  
    2) The simplest method: Select a random x and a random y and move towards that coordinate.  
    3) select an entity from the humans and zombies and move towards that entity.  
    
Out of these options, the first and second ones are too short-sighted and will not have much continuity in movement, which makes them poor choices. They also have a reasonable large sample space : 36000 potential results for 1) and over a million in 3). So it cannot be expected that the program will consistently be able to return the optimum given a large sample space and a limited number of tries.
  
So, I chose the 3rd option. Hence the random_move method in the move class, for technical reasons, I store the move as the x and y of the target rather than the entity itself as it has a variable type( Human or Zombie ). Now we have a random selection of type (0 for Human and 1 for Zombie) and a random selection from a list.  
  
Now, it is not sufficient to see a single move ahead due to the limited moving capacity of the characters, so we define a class Solution which simply contains a sequence of 9 moves. 9 is an arbitrary number and can be changed to whichever number you choose, but be careful to choose a smaller number so as to avoid an impact on your performance.  
      
So in the random solution we can populate an array with a random sequence of moves so as to create a random solution. After this we score the move based on the zombies killed and humans saved. you can add other parameters to strengthen this if you wish.  

In my evaluation function, I return -INFINITY if all humans die, +INFINITY if all zombies die, else I place a higher weightage on the humans that I save.  
  
I earlier mentioned that the approximation in the kill_humans function was useful, the reason for this is that, if a zombie wanders into a group of humans, it is quite different from it attacking a single human. So a higher weightage is placed on going to a group of humans over a single human to save them. This allows me to pass some of the tougher test cases.  
  
Now I will detail some technical errors that you should watch out for:  
    1) I pass a random object into the random move generator as creating a new Random object each time is firstly an attack on        performance. It also resets the seed( can be solved but is performance heavy ) which leads to the same move being              generated each time.  
    2) Be careful to make everything public.  
    3) Use structs instead of point if possible, I used classes as I wanted to go for inheritance. This is not necessary, You        can replace class Point with struct Point. This will boost your performance.  
    4) Minimize object creation to gain in performance.  

I have placed a very high emphasis on performance on code. It may not seem like an important factor to people who are not familiar with simulation, but there is a very large potential list of solutions. In order to get a 'good' solution, we must be able to generate and evaluate sufficient solutions to reach a good result. Hence the code is structured around minimizing the sample space( Hence the definition for what a move is ) and maximizing the number of simulations. So it is important to avoid the use of unnecessary elements to improve the code.
    
__CHAPTER 4 : FLOW OF CODE__  
  
This was only my second attempt at writing a search based bot in an object oriented programming language ( I normally use python for its in built methods ). So I favoured readability over gaining in performance. Because of this I used classes instead of structs so that I could implement inheritance.  
  
Inheritance allows for a more readable code as I can use methods more easily rather than continually referencing to its member objects.  
Eg : I can do zombie.distance(human) rather than zombie.location.distance(human.location)  
  
Another more important reason to use Inheritance is that, methods now can have a return type Entity so that I dont have conflicting types in any future modifications of random_move().
  
Now, to the sequence of the code: I dont know how to import a UML diagram onto github so I will try in another way.  
  
These are the following classes, their member variables and methods  
    1) class Point :  
        Variables -- > float x, float y ( floats are used to avoid implicit type casting in order to gain in performance )  
        Methods --> float distance2( Point p )    ( distance2 is used in cases where relative distance is required )  
                    float distance( Point p )  
    2) class Entity : Point ( Inherits from Point, for ease of use in distance functions ):  
        Variables --> int id, int dist_per_turn, int range ( These are constants but are stored in case I put methods in the                                                                entity class itself )  
                      bool alive ( Checks whether the entity was killed on simulation )  
        Constants --> float start_x, start_y ( An entity must be reset to its initial position after simulation )   
        Methods --> void reset() : resets the object to its initial x and y for the next simulation   
    3) class Human : Entity ( Inherits from Entity )   
        No variables of its own, range and dist_per_turn are 0   
    4) class Zombie : Entity ( Inherits from Entity )  
        range and dist_per_turn are 400  
        Variables --> Entity target ( target is of type entity as it can be Ash as well )  
        Methods --> void get_target() : Find the nearest human including Ash to move towards  
                    void moveto_target() : move 400 steps towards target  
    5) class Ash : Entity ( Inherits from Entity )  
        range and dist_per_turn are 1000 and 2000 respectively  
        Variables --> Entity target ( it is an Entity type as Ash can move towards a human as well )   
        Methods --> void moveto_target(Move move) ( Moves towards the x and y of move )  
                    void output(Move move) (print the move that is going to be executed  
    6) class Move :  
        Variables --> float x, float y  
        Methods --> Move random_move(Random r) ( Generates a random move )   
    7) class Solution :  
        Variables --> Move[] moves  
        Methods --> Solution random_solution(Random r) ( Generates a random solution )  
                    int score() ( Scores the solution )  
    8) class Player : The driver class  
        Variables --> int humanCount, int zombieCount, Human[] humans, Zombie[] zombies, Ash ash  
        Methods --> static void main() ( Runs the code )  
                    static void play(Solution solution) ( Play out a solution. is static to avoid unnecessary objects)  
  
The driver method main() in Player is the method that runs the code.  
The basic logic of this method is that it takes and stores the input and then while there is time left, it generates new solution and sets that as the best solution if it has a higher score that the previous solution. At the end of the 92 milliseconds, the program uses the Ash.output() method to print the first move of the best solution.  
  
int gens is simply a counter that tells me how many simulations I am able to do at a certain depth, it aids in benchmarking of performance  
   
__CHAPTER 5 : THE ROAD FORWARD.__    
  
Reading this, you will realize that there are several ways to improve. The foremost amongst these ways is to switch over from Monte Carlo to a Simulated Anealling.  
  
A Simulated Anealling functions similar to a Monte Carlo except that there is an extent of similarity between the previous and new solution. So if you are planning to modify to a simulated anealling, pass an amplitude to a function that modifies / mutates a solution so as to control the extent of change. The larger the amplitude --> the more change. So, the amplitude will preferably be inversely proportional to the score of the solution so as to not modify a good solution too much. You can start out with 1 / solution.score() as the amplitude and see how that works.  
  
There are smaller ways to work on this program. These are:  
      1) Vary the depth( number of moves per solution ) and check how it works out.    
      2) Add different parameters and coefficients to the evaluation function.  
      3) Experiment with your own definitions for what a 'Move' is.  
      4) Improve continuity between turns, so after the first turn, instead of randomly generating a new solution. Pop the              first Move of the previous solution and add a random move at the end. It is actually quite easy to do, keep shifting          forward and add the Move.random_move() function to the end.

If you are starting out, this is not an advisable solution for you. You can start out with a Heuristic bot in which you can implement the following strategies :   
    1) Move towards the closest Zombie : This will pass 70% of the test cases.  
    2) Move towards the closest Human : This will pass 95% of the test cases.  
    3) Move towards a human that it will take less time than a zombie to reach and stay there : Passes all test cases but with        a poor score.  
      
Happy coding!! :)



