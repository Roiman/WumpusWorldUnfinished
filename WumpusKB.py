from PriorityQueueLIFO import PriorityQueue

class kb:
    def __init__(self, board):
        """
        a class for keeping the information that is known to the agent
        separate from the full state of the board.
        The KB updates based on agent actions, and is used to
        confirm different results with the board.
        :param board: a board object.
        """
        self.board = board
        self.breezes, self.stenches, self.glitter, self.explored, self.safe_rooms, room_risks = {}, {}, {}, {}, {}, {}

        for row in range(board.size):
            for column in range(board.size):
                # assign no-risk to rooms as a starting point
                # risk will be a way to evaluate pits and wumpus
                # actually inferring a pit is really difficult,
                # even if we know how many there are, which we don't.
                # see notes.
                room_risks[(row, column)] = 0

        self.agent_location = board.agent_location

        self.room_risks = room_risks
        self.explored[board.start] = True
        self.frontier = PriorityQueue()
        return

    def increase_risk_adjacent(self, loc):
        for room in self.adjacent(loc):
            self.room_risks[room] += 1
        return


    @staticmethod
    def adjacent(loc):
        return [(loc[0] + 1, loc[1]), (loc[0] - 1, loc[1]), (loc[0], loc[1] + 1), (loc[0], loc[1] - 1)]

