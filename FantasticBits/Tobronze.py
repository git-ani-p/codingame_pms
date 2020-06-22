  
import sys
import math
import random as r

# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.
my_wizards = []
snaffles = []
opp_wizard = []
others = []
class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, new_point):
        return math.sqrt( (self.x - new_point.x) ** 2 + (self.y - new_point.y) ** 2)


my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
if my_team_id == 0:
    my_goal = []
    p = point(0, 3750)
    my_goal.append(p)
    opp_goal = []
    p = point(16000, 3750)
    opp_goal.append(p)
    
else:
    opp_goal = []
    p = point(0, 3750)
    opp_goal.append(p)
    my_goal = []
    p = point(16000, 3750)
    my_goal.append(p)




class snaffle:
    def __init__(self, position, vx, vy, state):
        self.position = position
        self.vx = vx
        self.vy = vy
        self.state = state
        
class wizard:
    def __init__(self, position, vx, vy, state, mygoal, oppgoal):
        self.position = position
        self.vx = vx
        self.vy = vy
        self.state = state
        self.my_goal = mygoal
        self.opp_goal = oppgoal
    def closest_snaffle(self):
        relative_positions = []
        if len(snaffles)>0:
            for snaf in [x for x in snaffles if x.state == 0 and x not in others]:
                distance = self.position.distance(snaf.position)
                relative_positions.append([snaf, distance])
            if relative_positions:
                closest_array = min(relative_positions, key = lambda x: x[1])
                return [closest_array[0], 'SNAFFLE']
            else:
                return [my_goal[0], 'GOAL']
        else:
            return None
            
    def move(self, target):
        target = target[0]
        if self.state == 1:
            scorer = self.opp_goal[0]
            print('THROW ' + '{} {} {}'.format(scorer.x, scorer.y, 500))
            
        else:
            print('MOVE ' + '{} {} {}'.format(target.position.x, target.position.y, 150))
    def return_to_goal(self):
        print('MOVE ' + '{} {} {}'.format(self.my_goal[0].x, self.my_goal[0].y, 150))
        
            
            
# game loop
while True:
    my_wizards = []
    opp_wizards = []
    snaffles = []
    my_score, my_magic = [int(i) for i in input().split()]
    opponent_score, opponent_magic = [int(i) for i in input().split()]
    entities = int(input())  # number of entities still in game
    for i in range(entities):
        # entity_id: entity identifier
        # entity_type: "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        # x: position
        # y: position
        # vx: velocity
        # vy: velocity
        # state: 1 if the wizard is holding a Snaffle, 0 otherwise
        entity_id, entity_type, x, y, vx, vy, state = input().split()
        entity_id = int(entity_id)
        x = int(x)
        y = int(y)
        vx = int(vx)
        vy = int(vy)
        state = int(state)
        position = point(x, y)
        if entity_type == 'WIZARD':
            temp = wizard(position, vx, vy, state, my_goal, opp_goal)
            my_wizards.append(temp)
        elif entity_type == 'OPPONENT_WIZARD':
            temp = wizard(position, vx, vy, state, opp_goal, my_goal)
            opp_wizards.append(temp)
        elif entity_type == 'SNAFFLE':
            temp = snaffle(position, vx, vy, state)
            snaffles.append(temp)
        
        
        
        others = []
    for i in my_wizards:
        target = i.closest_snaffle()
        if target[1] == 'SNAFFLE':
            others.append(target)
            i.move(target)
        elif target[1] == 'GOAL':
            i.return_to_goal()
        
        
        
