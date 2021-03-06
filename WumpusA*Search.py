from collections import deque
import itertools
from heapq import heappop, heappush


class PriorityQueue:
    def __init__(self):
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.REMOVED = '<removed-task>'  # placeholder for a removed task
        self.counter = itertools.count()  # unique sequence count

    def push(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    def __len__(self):
        return len(self.entry_finder)


# answer for (1)
class PuzzleNode:
    def __init__(self, location, parent, max_frontier_size, steps, goal_distance, size):
        """
        :param state: 2D list representing the board
        :param parent: other puzzle node, None for starting_node
        :param steps: number of steps to reach this node
        :param max_frontier_size: the easiest way to map frontier
                sizes to nodes is to store them here.
                Gives the max at time of exploration
        :param goal_distance: a heuristic applied on current state
        """
        self.location, self.parent, self.max_frontier_size, self.steps, self.goal_distance, self.size = \
            location, parent, max_frontier_size, steps, goal_distance, size
        return


# answer to (3).(b)
def misplacedTiles(state):
    """
    counts the number of tiles in their place.
    the use of deque here brings us down from O(n^2) or even O(2n^2)
    to O(n)
    """
    n = len(state)  # since we know the state is valid
    lst = deque([x for x in range(n * n)])  # que with all expected elements
    count = 0
    # iterates over the grid and adds 1 for each displaced tile
    for row in state:
        for tile in row:
            if tile != lst.popleft():  # pops each tested tile from the que
                count += 1
    return count


# answer to (3).(b)
def manhattanDistance(state):
    """
    finds the distance of each tile from its intended location
    returns a sum of all these distances
    """
    ans = 0
    n = len(state)  # since we know the state is valid
    for i, row in enumerate(state):
        # enumerate provides us with an index as well as a value
        for j, tile in enumerate(row):
            if tile != i * n + j:
                """
                if a tile is misplaced, we need to -
                1. figure out where it should have been
                2. find out how far it is from where it is
                3. add this manhattan distance to ans

                tile//n provides a truncated result: intended row
                tile%n provides a modulo: intended column
                taking the absolute value of the difference
                from the intended and the current is the manhattan distance 
                """
                ans += abs(i - tile // n) + abs(j - tile % n)
    return ans


def deep_clone(state):
    """
    :param state: takes a game state
    :return: output the same game state
                without modifying the original
    """
    new_state = []
    for row in state:
        new_state.append(row[:])
    return new_state


def explore_next(parent, heuristic, explored_set, allowed_set):
    """
    checks all states that can be reached from the current state
    according to the rules that only the 0 can move on y/x axis
    this is equivalent to moving any tile adjacent
        to the empty tile.
    :param parent: puzzle node to be expanded,
                    used for generating a new puzzle node
    :param heuristic: a goal-distance heuristic
    :param explored_set: all previously observed states
    :return: returns all nodes that can be reached from the parent
                excluding any previously observed states.
    """
    ignored_set = {}
    new_nodes = []
    # a list of possible "moves" in a 2D array
    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for i, j in parent.location:
        for ni, nj in moves:
            """
            we know len(state) is n,
            because we validated before starting.
            avoids out of range by checking i and j after
            each addition/subtraction.
            the new state is then generated by switching
            the 0 with another adjacent tile.
            we then test if the new state is in the
            previously explored set. We do this with a test
            node before applying the heuristic, since
            applying the heuristic to a previously explored
            state is a redundant process.
            """
            if 0 <= i + ni < parent.size and 0 <= j + nj < parent.size:
                new_room = (i + ni, j + nj)
                if new_room in allowed_set:
                    a = b
                else:
                    ignored_set[new_room] = True
                explored_state = deep_clone(parent.state)  # copy the array
                explored_state[i][j] = explored_state[i + ni][j + nj]
                explored_state[i + ni][j + nj] = 0
                test_node = PuzzleNode(explored_state, parent, parent.max_frontier_size, parent.steps + 1, -1)
                """
                doing this to save heuristic runs, it's expensive, man.
                max_frontier_size will update when explored
                answer to (3).(c) – avoiding repeated states
                for "It should also check if a better path to a
                previously-visited state has been found at any
                search step and modify the frontier" – A* with
                consistent heuristics assumes that a node is
                always reached optimally. So this is not needed.
                """
                test_state = str(test_node)

                if test_state in explored_set:
                    if explored_set[test_state].steps > test_node.steps:
                        test_node.goal_distance = explored_set[test_state].goal_distance
                        explored_set[test_state] = test_node
                        new_nodes.append(test_node)
                if test_state not in explored_set:
                    test_node.goal_distance = heuristic(explored_state)
                    new_nodes.append(test_node)
        break
    return new_nodes


# answer for (3)
def a_star(start_room, heuristic, explored, safe):
    """
    takes a starting state, lists all substates reachable from it,
    which are in the explored or safe states,
    adds them to frontier. The next state with the lowest cost
    evaluated by adding the heuristic distance and the number of
    steps is then selected for exploration.
    States previously explored are not added to the frontier,
    since we operate with the assumption that they were previously
    reached optimally.

    The goal state is achieved when heuristic(state) == 0.
    Each expansion adds 1 to the steps because of the game rules.
    Heap-Queue is used because it lets us keep the lowest-cost node
    at the start of the data structure for expansion.
    To make this work, nodes are stored in a tuple with this value.

    Since heapq doesn't deal well with our node structure,
    I added a dictionary mapping each state to a node,
    this allows us to retrieve nodes at O(1) for other uses.
    It also serves as the 'list' of explored states.
    """
    node_dict = {}
    start_node = PuzzleNode(start_room, None, 1, 0, heuristic(start_room))
    node_dict[start_room] = start_node
    frontier = PriorityQueue()
    frontier.push(start_room, start_node.steps + start_node.goal_distance)
    max_frontier = len(frontier)

    solution = []

    while frontier:
        # keep going till all nodes are explored, or a goal state is reached
        cur = frontier.pop()
        node_dict[cur].max_frontier_size = max(len(frontier), max_frontier)
        cur = node_dict[cur]  # pull the node from the dict
        if cur.goal_distance == 0:
            """
            this is the only termination condition except for
            unreachable solution. It works even if the start node
            is an end state.
            It then adds all nodes to the list 'solution' in reverse
            so solution[-1] is the start node.
            """
            while cur is not None:
                solution.append(cur)
                cur = cur.parent
            break
        for next_node in explore_next(cur, heuristic, node_dict):
            """
            explores the next node in the frontier using
            explore_next. Adds each new node to the dict
            then adds to the frontier, which arranges itself as heap 
            """
            key = str(next_node)
            node_dict[key] = next_node
            frontier.push(key, cur.steps + start_node.goal_distance)
        max_frontier = max(len(frontier), max_frontier)
        # not expecting this to be different from len(frontier)
        # in most cases, but it could happen.
    return solution, max_frontier  # solution is empty if there isn't one



# list of heuristics
heuristics = [misplacedTiles, manhattanDistance]
test_cases = [[2,2],
              [[0,0,0],[1,2,3,4]],
              [[5,7,7],[2,4,3],[8,1,0]],
              [[5,7,6],[2,4,3.2],[8,1,0]],
              [[5,7,6],[2,4,3.2],["8",1,0]],
              [[5,7,6],[2,4,3.2],[[8],1,0]],
              [[5,7,6],[2,4,3],[8,1,0]],
              [[7,0,8],[4,6,1],[5,3,2]],
              [[2,3,7],[1,8,0],[6,5,4]],
              [[0,1,2],[3,4,5],[6,7,8]]]

n = 3
prnt = False
for heuristic in heuristics:
    for test_case in test_cases:
        steps, frontierSize, err = solvePuzzle(n, test_case, heuristic, prnt)
        print(steps, frontierSize, err)
