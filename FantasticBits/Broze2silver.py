import sys
import math
import random
import time

# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

flipendo_cooldown = 0
accio_cooldown = 0



class vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance2(self, new):
        return (self.x - new.x) ** 2 + (self.y - new.y) ** 2
        
    def distance(self, new):
        return math.sqrt( (self.x - new.x) ** 2 + (self.y - new.y) ** 2 )
    
        
    def will_reach(self, entity_to_hit, target, target_type = 'GOAL'):
        if target_type == 'GOAL':
            if target.x_position == 0:
                if entity_to_hit.location.x > self.x:
                    return False
            elif target.x_position == 16000:
                if entity_to_hit.location.x < self.x:
                    return False
            target_x = target.x_position
            delta_x = entity_to_hit.location.x - self.x
            delta_y = entity_to_hit.location.y - self.y
            slope = delta_y / delta_x
            y_intercept = entity_to_hit.location.y - slope * entity_to_hit.location.x
            #Now have all elements of y = mx + c, apply to target x and get y, then check is in range
            y_at_target_x = target_x * slope + y_intercept
            if target.contains(y_at_target_x):
                return True
            else:
                return False
        
            
                
                


class entity:
    def __init__(self, id, owner, location, speed, state, mass, friction):
        self.id = id
        self.owner = owner
        self.location = location
        self.speed = speed
        self.state = state
        self.mass = mass
        self.friction = friction
        self.future_position = vector(self.location.x + self.speed.x, self.location.y + self.speed.y)
    
    def distance2(self, target, target_type = 'ENTITY'):
        if target_type == 'ENTITY':
            return self.location.distance2(target.location)
        else:
            return self.location.distance2(target)
    def distance(self, target, target_type = 'ENTITY'):
        if target_type == 'ENTITY':
            return self.location.distance(target.location)
        else:
            return self.location.distance(target)

    def contains(self, point):
        return self.location.distance2(point) < self.radius ** 2
            
    def update(self, location, speed, state):
        self.location = location
        self.speed = speed
        self.state = state
    
            
class wizard(entity):
    
    def __init__(self, id, owner, location, speed, state, magic):
        entity.__init__(self, id, owner, location, speed, state, 1.0, 0.75)
        self.magic = magic
        
        self.has_snaffle = ( self.state == 1 )
        
        if self.owner == "ME":
            self.my_goal = my_goal
            self.opp_goal = opp_goal
        else:
            self.my_goal = opp_goal
            self.opp_goal = my_goal
    
    def get_partner(self):
        print('CHECKING FOR PARTNER', file = sys.stderr)
        for wiz in wizards:
            if wiz.owner == self.owner and wiz.id != self.id:
                self.partner = wiz
                print(wiz.id, file = sys.stderr)
                
    def my_min_dist(self, target):
        return min(self.distance(target), self.partner.distance(target))
        
    def opp_min_dist(self, target):
        opp1, opp2 = [wiz for wiz in wizards if wiz.owner != self.owner]
        return min(opp1.distance(target), opp2.distance(target))
    
    def check_obliviate(self):
        if self.magic > 10:
            for blu in bludgers:
                if self.distance(blu) < 100 and self.distance(min(snaffles, key = lambda x:self.distance2(x))) < 1000:
                    return 'OBLIVIATE {}'.format(blu.id)
        
        
    
    def check_petrificus(self):
        if self.magic >= 10:
            for snaf in sorted(snaffles, key = lambda x: self.my_goal.distance(x.location)):
                if snaf.reaches_goal(self.my_goal):
                    snaf.targetted = True
                    return 'PETRIFICUS {}'.format(snaf.id)
            return None
        return None
        
    
    
    def check_flipendo(self):
        self.sorted_snaffles = sorted(snaffles, key = lambda x: self.distance(x))
        if self.magic >= 20 and flipendo_cooldown == 0:
            for i in self.sorted_snaffles[::-1]:
                if self.location.will_reach(i, opp_goal) and i.targetted == False and self.my_min_dist(i) > self.opp_min_dist(i) and not i.reaches_goal(self.opp_goal):
                    i.targetted = True
                    return 'FLIPENDO {}'.format(i.id)
                    
            return None
        else:
            return None
    
    def check_accio(self):
        if self.magic >= 40:
            to_accio = None
            sort_snaffles = sorted(snaffles, key = lambda x: self.my_goal.distance(x.location))
            for i in sort_snaffles:
                if self.my_min_dist(i) > self.opp_min_dist(i):
                    return 'ACCIO {}'.format(i.id)
            else:
                return None
        else:
            return None
            
    def goto_closest(self):
        for i in self.sorted_snaffles:
            if i.targetted == False:
                i.targetted = True
                return 'MOVE {} {} {}'.format(i.future_position.x, i.future_position.y, 150)
        target = snaffles[0]
        return 'MOVE {} {} {}'.format(target.future_position.x, target.future_position.y, 150)
        
    def throw_at_goal(self):
        for snaf in snaffles:
            if self.distance(snaf) <= 400:
                self.my_snaffle = snaf
        return 'THROW {} {} {}'.format(self.opp_goal.centre.x - self.my_snaffle.speed.x, self.opp_goal.centre.y - self.my_snaffle.speed.y, 500)
        
    def calc_move(self):
        self.get_partner()
        if self.has_snaffle:
            return self.throw_at_goal()
        else:
            
            a = self.check_flipendo()
            b = self.check_accio()
            c = self.goto_closest()
            d = self.check_obliviate()
            first = self.check_petrificus()
            if a:
                return a
            elif first:
                return first
            elif b:
                return b
            elif d:
                return d
            else:
                return c
    
        
        
class bludger(entity):
    def __init__(self, id, location, speed, state):
        entity.__init__(self, id, None, location, speed, state, 8.0, 0.90)
        self.target = min(wizards, key = lambda x: self.distance2(x))
        self.dist_to_target = self.distance(self.target)
        
    
class snaffle(entity):
    def __init__(self, id, location, speed, state):
        entity.__init__(self, id, None, location, speed, state, 0.5, 0.75)
        self.is_grabbed = ( self.state == 1 )
        self.targetted = False
        
    def set_target(self):
        for i in snaffles:
            if i.id == snaf.id:
                i.targetted = True
                
    def reaches_goal(self, target_goal):
        
        current_x = self.location.x
        current_y = self.location.y
        current_vx = self.speed.x
        current_vy = self.speed.y
        for i in range(3):
            current_x += current_vx
            current_y += current_vy
            current_vx *= 0.75
            current_vy *= 0.75
        final_x = current_x
        final_y = current_y
        if target_goal.x_position == 0:
            if final_x <= target_goal.x_position:
                return target_goal.contains(final_y)
            return False
        else:
            if final_x >= target_goal.x_position:
                return target_goal.contains(final_y)
            return False

class goal:
    def __init__(self, x_position):
        self.x_position = x_position
        self.y_start = 2300
        self.y_end = 5100
        self.centre = vector(self.x_position, 3750)
        
    def contains(self, y_coordinate):
        if self.y_start < y_coordinate and y_coordinate < self.y_end:
            return True
        else:
            return False
    def contains_point(self, point):
        if self.x_position == 0 and point.x <= 0:
            return self.contains(point.y)
        if self.x_position == 16000 and point.x >- 16000:
            return self.contains(point.y)
        return False
        
            
    def distance(self, point):
        return self.centre.distance(point)
    





my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
if my_team_id == 0:
    my_goal = goal(0)
    opp_goal = goal(16000)
else:
    my_goal = goal(16000)
    opp_goal = goal(0)

wizards = []
bludgers = []
snaffles = []

# game loop
while True:
    start_time = time.time() * 1000
    wizards = []
    bludgers = []
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
        location = vector(x, y)
        speed = vector(vx, vy)
        if entity_type == "WIZARD":
            temp = wizard(entity_id, "ME", location, speed, state, my_magic)
            wizards.append(temp)
        elif entity_type == 'OPPONENT_WIZARD':
            temp = wizard(entity_id, "OPPONENT", location, speed, state, opponent_magic)
            wizards.append(temp)
        elif entity_type == 'SNAFFLE':
            temp = snaffle(entity_id, location, speed, state)
            snaffles.append(temp)
        elif entity_type == 'BLUDGER':
            temp = bludger(entity_id, location, speed, state)
            bludgers.append(temp)
    
    for i in wizards:
        if i.owner == 'ME':
            move = i.calc_move()
            if 'FLIPENDO' in move:
                flipendo_cooldown = 3
                for wiz in wizards:
                    if wiz.owner == 'ME':
                        wiz.magic -= 20
            if 'ACCIO' in move:
                accio_cooldown = 6
                for wiz in wizards:
                    if wiz.owner == 'ME':
                        wiz.magic -= 15
                        
            if 'PETRIFICUS' in move:
                for wiz in wizards:
                    if wiz.owner == 'ME':
                        wiz.magic -= 10
            
            if 'OBLIVIATE' in move:
                for wiz in wizards:
                    if wiz.owner == 'ME':
                        wiz.magic -= 5
            end_time = time.time() * 1000
            print(move, str(int(end_time - start_time)) + 'ms')
    if flipendo_cooldown > 0:
        flipendo_cooldown -= 1
    if accio_cooldown > 0:
        accio_cooldown -= 1
