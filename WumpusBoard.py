from random import choice, random, seed
seed(1211)  # arbitrary seed for testing


class Board:
    def __init__(self, size=4, start=(0, 0), pit_rate=0.1, gold_loc=None, wumpus_loc=None, n_wumpus=1):
        """
        The board is represented as a list of lists.
        Most placings are either random or intended to be specified by the user.
        I wanted to also handle a non-square board, but did not get to implementing it.
        :param size: board size NXN matrix, default is 4.
        :param start: starting location. Default is 0,0, which is top left.
        :param pit_rate: likelihood of an unoccupied space to become a pit.
        :param gold_loc: the gold's starting location. Random if None.
        :param wumpus_loc: the Wumpus starting location. Random if None.
                            The Wumpus doesn't move in this implementation :(
        :param n_wumpus: theoretically, could have more than one wumpus.
        """
        self.size, self.start, self.agent_location, self.pit_rate, self.gold_loc,\
        self.wumpus_loc, self.n_wumpus = size, start, start, pit_rate,\
                                         gold_loc, wumpus_loc, n_wumpus
        self.board = self.generate_board(size, start, gold_loc)
        self.pit_locations = []
        self.generate_pits(pit_rate)
        self.add_wumpus(wumpus_loc)
        self.breezes = {}
        self.stenches = {}
        self.breezes_and_stench(self.pit_locations, self.wumpus_loc)
        return

    def generate_board(self, size, start, gold_loc):
        """ :returns a list of lists of size n
                empty locations are 0s, agent is A, and gold is g"""

        # create nXn matrix
        board = [[0 for i in range(size)] for j in range(size)]

        # gold appears at random location, or at a specified one.
        # this should handle errors, but for now left to rely on the user.
        # theoretically the gold could be in the starting square, but for ease of implementation, it isn't
        while gold_loc is None:
            x, y = choice(range(size)), choice(range(size))
            if [x, y] != start:
                gold_loc = (x, y)
        board[gold_loc[0]][gold_loc[1]] = "g"
        self.gold_loc = gold_loc

        # place the agent at the chosen start location
        board[start[0]][start[1]] = "A"

        return board

    def generate_pits(self, pit_rate):
        # for each unoccupied square, generate random floating point in range 0-1
        # if it is smaller than the pit-rate, the room becomes a pit.
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0 and random() <= pit_rate:
                    self.board[i][j] = "p"
                    self.pit_locations.append((i, j))
        return

    def add_wumpus(self, wumpus_loc):
        # randomize an unoccupied square, place wumpus, unless a location is specified
        # not currently implementing multiple wumpusi
        while wumpus_loc is None:
            x, y = choice(range(self.size)), choice(range(self.size))
            if self.board[x][y] == 0:
                wumpus_loc = (x, y)
        self.board[wumpus_loc[0]][wumpus_loc[1]] = "w"
        self.wumpus_loc = wumpus_loc
        return

    def breezes_and_stench(self, pit_locations, wumpus_loc):
        # will be used for perceiving stenches and breezes
        for pit in pit_locations:
            for room in self.adjacent(pit):
                self.breezes[room] = True
        for room in self.adjacent(wumpus_loc):
            self.stenches[room] = True
        return

    @staticmethod
    def adjacent(loc):
        """
        checks for adjacency of rooms. Does not care for the borders of the board, though.
        Decided to handle that in each call, although would make sense to do here instead.
        :param loc: the room to check for adjacency.
        :return: all adjacent rooms as a list of tuples [(X,Y),...]
        """
        return [(loc[0] + 1, loc[1]), (loc[0] - 1, loc[1]), (loc[0], loc[1] + 1), (loc[0], loc[1] - 1)]

