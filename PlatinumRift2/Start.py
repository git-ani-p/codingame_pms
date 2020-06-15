import sys
import math
import random as r
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# player_count: the amount of players (always 2)
# my_id: my player ID (0 or 1)
# zone_count: the amount of zones on the map
# link_count: the amount of links between all zones
player_count, my_id, zone_count, link_count = [int(i) for i in input().split()]


class zone:
    def __init__(self, id, owner, pods0, pods1, platinum):
        self.id = id
        self.owner = owner
        self.pods = [pods0, pods1]
        self.platinum = platinum
        self.my_pods = self.pods[my_id]
        
    def update(self, owner, pods0, pods1, visibility, platinum):
        self.owner = owner
        self.pods = [pods0, pods1]
        self.my_pods = self.pods[my_id]
        if visibility == 1:
            self.platinum = platinum
        
    def calc_move_towards(self):
        connected_zone_ids = [lin.start for lin in links_to_opponent]
        my_links = [lin.end for lin in links if lin.start == self.id]
        target = None
        target_object = None
        for lin in connected_zone_ids:
            if lin in my_links:
                target = lin
                target_object = ''
                for zon in zones:
                    if zon.id == target:
                        target_object = zon
                if target_object.owner != my_id:
                    break
                
        if target_object:
            
            print('MOVING TOWARDS OPPONENT', file = sys.stderr)
            return '{} {} {}'.format(self.my_pods, self.id, target)
            
            
        else:
            
            print('MOVING RANDOMLY', file = sys.stderr)
            target = r.choice(my_links)
            return '{} {} {}'.format(self.my_pods, self.id, target)
            
    def calc_move_at(self):
        print('ATTACKING OPPONENTS', file = sys.stderr)
        return '{} {} {}'.format(self.my_pods, self.id, opp_HQ.id)
            
    def get_move(self):
        connected_zone_ids = [lin.start for lin in links_to_opponent]
        if self.id in connected_zone_ids:
            return self.calc_move_at()
        else:
            return self.calc_move_towards()
            
        
        
class link:
    def __init__(self, zone1, zone2):
        self.start = zone1
        self.end = zone2



zones = []

for i in range(zone_count):
    # zone_id: this zone's ID (between 0 and zoneCount-1)
    # platinum_source: Because of the fog, will always be 0
    zone_id, platinum_source = [int(j) for j in input().split()]
    tmp = zone(zone_id, 0, 0, 0, 0)
    zones.append(tmp)
    
    
turn_number = 1    
opp_id = 1 - my_id
my_HQ = ''
opp_HQ = ''
my_pos = ''
links_to_opponent = []
links = []

for i in range(link_count):
    zone_1, zone_2 = [int(j) for j in input().split()]
    tmp = link(zone_1, zone_2)
    links.append(tmp)
    tmp = link(zone_2, zone_1)
    links.append(tmp)
    
# game loop
while True:
    my_platinum = int(input())  # your available Platinum
    for i in range(zone_count):
        # z_id: this zone's ID
        # owner_id: the player who owns this zone (-1 otherwise)
        # pods_p0: player 0's PODs on this zone
        # pods_p1: player 1's PODs on this zone
        # visible: 1 if one of your units can see this tile, else 0
        # platinum: the amount of Platinum this zone can provide (0 if hidden by fog)
        z_id, owner_id, pods_p0, pods_p1, visible, platinum = [int(j) for j in input().split()]
        pods = [pods_p0, pods_p1]
        if turn_number == 1:
            if pods[my_id] > 0:
                my_HQ = zone(z_id, owner_id, pods_p0, pods_p1, platinum)
            if pods[opp_id] > 0:
                opp_HQ = zone(z_id, owner_id, pods_p0, pods_p1, platinum)
                links_to_opponent = [lin for lin in links if lin.end == opp_HQ.id]
        
        for zon in zones:
            if zon.id == z_id:
                zon.update(owner_id, pods_p0, pods_p1, visible, platinum)
        
        
    my_zones = [zon for zon in zones if zon.owner == my_id]
    a = ''
    for zon in my_zones:
        a += zon.get_move()
        a += ' '

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    
    if a == '':
        print('WAIT')
    else:
        print(a.rstrip())
    
    
    print('WAIT')
    
    turn_number += 1
    
    
