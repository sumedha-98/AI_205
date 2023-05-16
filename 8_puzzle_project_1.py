import heapq
import copy
import time

trivial = [[1, 2, 3],
           [4, 5, 6],
           [7, 8, 0]]
veryEasy = [[1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]]
easy = [[1, 2, 0],
        [4, 5, 3],
        [7, 8, 6]]
medium = [[0, 1, 2],
          [4, 5, 3],
          [7, 8, 6]]
hard = [[8, 7, 1],
        [6, 0, 2],
        [5, 4, 3]]
goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

def isValid(i,j, size):
    if i >= 0 and j >= 0 and i < size and j < size:
        return True
    else:
        return False
    
def blank(state, size): #function to find the location of the blank
    for i in range(size):
        for j in range(size):
            if state[i][j] == 0:
                return i, j #returns the row number and column number of the blank

def swap(state, nx, ny, row, col): #swaps current node with neighbour node
    state[row][col], state[nx][ny] = state[nx][ny], state[row][col]
    return state

def heuristic_misplaced(state, size): #Calculates the number of tiles that are misplaced tiles in current state as compared to goal state
    count = 0
    for i in range(size):
        for j in range(size):
            if state[i][j] != goal_state[i][j] and state[i][j] != 0:
                count += 1
    return count

def heuristic_manhattan(state, size): #Calculates the total sum of distances of misplaced tiles in current state as compared to goal state
    value = 0
    goal_state_map = {}
    for i in range(size):
        for j in range(size):
            goal_state_map[goal_state[i][j]] = [i, j]
    for i in range(size):
        for j in range(size):
            if (state[i][j] == goal_state[i][j]):
                continue   
            if (state[i][j] == 0):
                continue
            value = value + abs(goal_state_map[state[i][j]][0] - i) + abs(goal_state_map[state[i][j]][1] - j)
    return value


def general_search(initial_state, heuristic, size):

    start = time.time()
    h = 0 #adds the heuristic value.
    distance = {} #Calculates depth with heuristic value
    depth = {} #Calculates depth of goal state
    nodes_expanded = 0 #Keeps a track of the nodes explored
    distance[tuple(tuple(i) for i in initial_state)] = 0
    depth[tuple(tuple(i) for i in initial_state)] = 0
    visited = set() #Keeps a track of the visited nodes
    nodes = [(0,initial_state)]
    nodes_length = 1
    neighbour_list = [(0,-1),(0,1),(-1,0),(1,0)] #to move the blank tile left, right, up and down
    while nodes:
        if heuristic == 0: #Uniform cost search
            node = nodes.pop(0)
        else: #A* with Misplaced Tile or Manhattan Distance heuristic
            node = heapq.heappop(nodes)
        if node[1] == goal_state: #Goal state reached
            end = time.time()
            print("Goal state reached!")
            print ("Depth of the solution:",depth[tuple(tuple(i) for i in goal_state)])
            print("Nodes expanded:",nodes_expanded)
            print("Maximum queue size:", nodes_length)
            print("Time taken: %.3f" %(end - start))  
            return
        node_tuple = tuple(tuple(i) for i in node[1])
        visited.add(node_tuple) #add current node to visited
        nodes_expanded += 1
        row_no, column_no = blank(node[1], size) #get the row and column of blank
        for x in neighbour_list:
            nx = row_no + x[0] #neighbour to left and right
            ny = column_no + x[1] #neighbour above and below
            neighbour = copy.deepcopy(node[1]) #stores neighbour
            if isValid(nx, ny, size):
                    neighbour = swap(neighbour, nx, ny, row_no, column_no) # neighbour node
                    neighbour_tuple = tuple(tuple(i) for i in neighbour)
                    if neighbour_tuple not in visited:
                        if heuristic == 1: #A* with misplaced tile heuristic
                            h = heuristic_misplaced(neighbour, size)
                        if heuristic == 2: #A* with Manhattan Distance heuristic
                            h = heuristic_manhattan(neighbour, size)
                        distance[neighbour_tuple] = depth[node_tuple] + 1 + h
                        depth[neighbour_tuple] = depth[node_tuple] + 1
                        if heuristic == 0: #Uniform cost search
                            nodes.append((depth[neighbour_tuple], neighbour)) #add depth and neighbour to nodes
                            visited.add(neighbour_tuple) 
                        else: 
                            heapq.heappush(nodes, (distance[neighbour_tuple], neighbour)) #add depth and neighbour to nodes
                        nodes_length = max(nodes_length,len(nodes))
    print("FAILURE!")   #Goal state not reached

size = 3 #The size can be changed accordingly for 15-puzzle or 25-puzzle

print("Welcome to 8-puzzle!")
print("Enter 1 to select a pre-set board or Enter 2 to build your own")
n = int(input())
if n == 1:
    print("Choose your level of difficulty: \n 1. Trival \n 2. Very Easy \n 3. Easy \n 4. Medium \n 5. Hard")
    x = int(input())
    if x == 1:
        board = trivial
    elif x == 2:
        board = veryEasy
    elif x == 3:
        board = easy
    elif x == 4:
        board = medium
    elif x == 5:
        board = hard
    else:
        print("Invalid choice")

    print("Choose the search algorithm which you would like to use: \n 0: Uniform Cost Search \n 1: A* with Misplaced tile \n 2: A* with Manhattan Distance")
    y = int(input())
    if y == 0:
        heuristic = 0
    elif y == 1:
        heuristic = 1
    elif y == 2:
        heuristic = 2
    else:
        print("Invalid Choice")

elif n == 2:
    print("Input your values in a single line by giving a single space between each value. Remember the blank tile is represented as 0!")
    string = input().split()
    board = [[int(string[0]), int(string[1]), int(string[2])],
             [int(string[3]), int(string[4]), int(string[5])],
             [int(string[6]), int(string[7]), int(string[8])]]

    print("Choose the search algorithm which you would like to use: \n 0: Uniform Cost Search \n 1: A* with Misplaced tile \n 2: A* with Manhattan Distance")
    y = int(input())
    if y == 0:
        heuristic = 0
    elif y == 1:
        heuristic = 1
    elif y == 2:
        heuristic = 2
    else:
        print("Invalid Choice")

general_search(board, heuristic, size) 


