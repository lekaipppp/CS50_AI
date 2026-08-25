#Notice in maze1, the A is the starting position, and B is the goal


class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier:

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    #Checks if the array is empty or not
    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty Froniter")

        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():

    def __init__(self, filename):

        '''When the code executes the open(filename), 
        It sends request to your OS asking for permission to
        access the file at the given path
        '''
        with open(filename) as f:
            #When we read the file, it atually starts as just one big, continuous string.
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point")

        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one end point")

        contents = contents.splitlines()

        self.height = len(contents)
        self.width = len(contents[0])

        self.walls = []

        for i in range(self.height):

            row = []

            for y in range(self.width):

                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)

                    elif contents[i][j] == "B":
                        self.end = (i, j)
                        row.append(False)

                    elif contents[i][j] == "#":
                        row.append(True)

                    elif contents[i][j] == " ":
                        row.append(False)
                except IndexError:
                    row.append(False)

            self.walls.append(row)        

    def neighbors(self, state):
        row, col = state

        candidates = [
            ("up", (row-1, col)),
            ("down", (row+1, col)),
            ("left", (row, col - 1)),
            ("rgiht", (row, col+1))
        ]

        result = []

        for action, (r, c) in candidates:
            if (
                0 <= r < self.height
                and 0 <= c < self.width
                and not self.walls[r][c]
            ):
                result.append((action, (r, c)))
        return result

    def solve(self):

        self.num_explored = 0

        start = Node(state=self.start, parent=None, action=None)

        frontier = StackFrontier()
        frontier.add(start)

        #Create a explored list:
        explored_list = set()

        while True:

            if frontier.empty():
                raise Exception("No solution")

            node = frontier.remove()

            if node.state == self.goal:
                print("Found the goal")
                return

            #if it is not the goal, we add it into the explored_set

            explored_list.add(node.state)

            #checks its neighbors
            for action, state in self.neighbors(node,state):

                if (
                    state not in explored_list
                    and not frontier.contains_state(state)
                ):
                    child = Node(
                        state = state,
                        parent=node,
                        action=action
                    )

                    frontier.add(child)
