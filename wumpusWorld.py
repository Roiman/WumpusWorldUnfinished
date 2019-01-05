from WumpusBoard import Board
from WumpusKB import kb


class agent:
    def __init__(self, kb):
        """
        a class for the agent to perform actions.
        Relies on the KB and the board.
        :param kb: a kb object
        """
        self.kb = kb
        return

    def perceive(self, location):
        no_stench = False
        no_breeze = False

        # check for game-over
        try:
            if (location in self.kb.board.pit_locations)\
                    or (location == self.kb.board.wumpus_loc):
                return "GAME OVER"
        except KeyError:
            pass

        # check for stench
        try:
            if self.kb.board.stenches[location]:
                self.kb.breezes[location] = True
                self.kb.increase_risk_adjacent(location)
        except KeyError:
            no_stench = True

        # check for breeze
        try:
            if self.kb.board.breezes[location]:
                self.kb.breezes[location] = True
                self.kb.increase_risk_adjacent(location)
        except KeyError:
            no_breeze = True

        # if neither stench nor breeze, make adjacent squares "safe"
        if no_breeze and no_stench:
            for room in kb.adjacent(location):
                if room not in kb.explored:
                    if (0 <= room[0] <= self.kb.board.size) and (0 <= room[1] <= self.kb.board.size):
                        kb.frontier.push(room, 0)  # TODO: safe rooms should always be selected for exploration
                        kb.safe_rooms[room] = True

        # check for glitter
        try:
            if self.kb.board.gold_loc == location:
                self.kb.glitter[location] = True
        except KeyError:
            pass

        return

    # adds the adjacent locations to the frontier
    def add_to_frontier(self, loc):
        for room in kb.adjacent(loc):
            if room not in kb.explored:
                # only adds rooms that have not been explored, and inside the board
                if (0 <= room[0] <= self.kb.board.size) and (0 <= room[1] <= self.kb.board.size):
                    self.kb.frontier.push(room, self.kb.room_risks[room])
                    # since frontier is a priority que, the order to explore will be by risk level
                    # need to adjust so we explore from the last added, not the first
        return

    def find_route(self, target_room, allowed_rooms):
        # this would have used the A* search
        """
        finds the shortest path to a room using A* search
        only explores within the list of visited rooms
        :param target_room: room as (X, Y)
        :param allowed_rooms: list of rooms (X, Y)
        :return: ordered list of rooms to pass.
                    allowed rooms are either
                    rooms we visited or deemed safe
        """
        return

    def move(self):
        """
        the 'move' function was intended to move the agent
        to the safest nearest space, through the shortest route.
        If the gold was found, it would either grab it and move
        to the exit, or move to the gold's room and then grab
        it and move back to the exist.
        :return:
        """
        try:
            if kb.glitter != {}:
                # do we have gold? go to exit.
                # no gold? are we at the gold location? grab, go to exit
                # not at gold location? go to gold location.
                return

        except:
            target_room = self.kb.frontier.pop(0)

            # move to least risky square through shortest path of explored rooms
            #    in case of tie on risk: randomize
            #    check for precepts in new location, update the exploration frontier
            # self.perceive(loc)
            # self.add_to_frontier(loc)
            return


board = Board()
kb = kb(board)
agent = agent(kb)

