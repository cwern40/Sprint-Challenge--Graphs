from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from copy import deepcopy

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# Important functions: player.current_room.id, player.current_room.get_exits() and player.travel(direction)
# Example visited code:
# {
#   0: {'n': '?', 's': 5, 'w': '?', 'e': '?'},
#   5: {'n': 0, 's': '?', 'e': '?'}
# }
traversal_path = []
visited_rooms = {}
proceed = True
finished = False
visited_rooms[player.current_room.id] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}

while proceed is True:
    available_directions = []
    if 'n' in visited_rooms[player.current_room.id] and visited_rooms[player.current_room.id]['n'] == '?':
        available_directions.append('n')
    if 's' in visited_rooms[player.current_room.id] and visited_rooms[player.current_room.id]['s'] == '?':
        available_directions.append('s')
    if 'w' in visited_rooms[player.current_room.id] and visited_rooms[player.current_room.id]['w'] == '?':
        available_directions.append('w')
    if 'e' in visited_rooms[player.current_room.id] and visited_rooms[player.current_room.id]['e'] == '?':
        available_directions.append('e')
    
    if len(available_directions) > 0:
        previous_room = player.current_room.id
        travel = random.choice(available_directions)
        player.travel(travel)
        traversal_path.append(travel)
        visited_rooms[previous_room][travel] = player.current_room.id
        if player.current_room.id in visited_rooms:
            if travel == 'n':
                visited_rooms[player.current_room.id]['s'] = previous_room
            if travel == 's':
                visited_rooms[player.current_room.id]['n'] = previous_room
            if travel == 'w':
                visited_rooms[player.current_room.id]['e'] = previous_room
            if travel == 'e':
                visited_rooms[player.current_room.id]['w'] = previous_room
        else:
            visited_rooms[player.current_room.id] = {}
            for room in player.current_room.get_exits():
                visited_rooms[player.current_room.id][room] = '?'
            if travel == 'n':
                visited_rooms[player.current_room.id]['s'] = previous_room
            if travel == 's':
                visited_rooms[player.current_room.id]['n'] = previous_room
            if travel == 'w':
                visited_rooms[player.current_room.id]['e'] = previous_room
            if travel == 'e':
                visited_rooms[player.current_room.id]['w'] = previous_room
    else:
        proceed = False
        finished = False
    
    while proceed is False and finished is False:
        plan_to_visit = Queue()
        bfs_visited = set()
        current_path =  ([player.current_room.id], [])
        plan_to_visit.enqueue(current_path)
        stop = False

        while stop is False:
            current_path = plan_to_visit.dequeue()

            if current_path[0][-1] not in bfs_visited:

                bfs_visited.add(current_path[0][-1])

                if 'n' in visited_rooms[current_path[0][-1]] and visited_rooms[current_path[0][-1]]['n'] == '?':
                    
                    for direction in current_path[1]:
                        player.travel(direction)
                        traversal_path.append(direction)
                        
                    proceed = True
                    stop = True
                elif 's' in visited_rooms[current_path[0][-1]] and visited_rooms[current_path[0][-1]]['s'] == '?':
                    
                    for direction in current_path[1]:
                        player.travel(direction)
                        traversal_path.append(direction)
                        
                    proceed = True
                    stop = True
                elif 'w' in visited_rooms[current_path[0][-1]] and visited_rooms[current_path[0][-1]]['w'] == '?':
                    
                    for direction in current_path[1]:
                        player.travel(direction)
                        traversal_path.append(direction)
                        
                    proceed = True
                    stop = True
                elif 'e' in visited_rooms[current_path[0][-1]] and visited_rooms[current_path[0][-1]]['e'] == '?':
                    
                    for direction in current_path[1]:
                        player.travel(direction)
                        traversal_path.append(direction)
                        
                    proceed = True
                    stop = True
                else:
                    for key, value in visited_rooms[current_path[0][-1]].items():
                        next_path = deepcopy(current_path)
                        next_path[0].append(value)
                        next_path[1].append(key)
                        plan_to_visit.enqueue(next_path)
            if plan_to_visit.size() is 0:
                stop = True
        if plan_to_visit.size() is 0:
            finished = True
            


# print("test")
# print(player.current_room.id)
# travel = player.current_room.get_exits()
# print(travel)
# print(travel[1])
# player.travel(travel[1])
# print(player.current_room.id)
# print("test")

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
