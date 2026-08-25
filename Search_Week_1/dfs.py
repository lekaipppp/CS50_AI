# A = starting position
# B = goal
# # = wall
# space = open path


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

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):

        if self.empty():
            raise Exception("Empty frontier")

        # DFS: remove the LAST added node
        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]

        return node


class Maze:

    def __init__(self, filename):

        # Read maze file
        with open(filename) as f:
            contents = f.read()

        # Check that there is exactly one start
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point")

        # Check that there is exactly one goal
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal")

        contents = contents.splitlines()

        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []

        # Read every position in the maze
        for i in range(self.height):

            row = []

            for j in range(self.width):

                try:
                    character = contents[i][j]

                    if character == "A":
                        self.start = (i, j)
                        row.append(False)

                    elif character == "B":
                        self.goal = (i, j)
                        row.append(False)

                    elif character == " ":
                        row.append(False)

                    else:
                        # Anything else is treated as a wall
                        row.append(True)

                except IndexError:
                    row.append(False)

            self.walls.append(row)

        self.solution = None
        self.num_explored = 0

    def neighbors(self, state):

        row, col = state

        # All four possible moves
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []

        for action, (r, c) in candidates:

            # Check:
            # 1. position is inside maze
            # 2. position is not a wall
            if (
                0 <= r < self.height
                and 0 <= c < self.width
                and not self.walls[r][c]
            ):
                result.append((action, (r, c)))

        return result

    def solve(self):

        # Keep track of how many nodes we explored
        self.num_explored = 0

        # Create starting node
        start = Node(
            state=self.start,
            parent=None,
            action=None
        )

        # DFS uses StackFrontier
        frontier = StackFrontier()
        frontier.add(start)

        # States we have already explored
        explored = set()

        while True:

            # If frontier is empty, no solution exists
            if frontier.empty():
                raise Exception("No solution")

            # DFS removes the newest node
            node = frontier.remove()

            self.num_explored += 1

            # Check if we reached the goal
            if node.state == self.goal:

                actions = []
                cells = []

                # Follow parent pointers backwards
                while node.parent is not None:

                    actions.append(node.action)
                    cells.append(node.state)

                    node = node.parent

                # We built the path backwards,
                # so reverse it
                actions.reverse()
                cells.reverse()

                self.solution = (actions, cells)

                print("Found the goal!")
                print("Actions:", actions)
                print("Path:", cells)
                print("Explored:", self.num_explored)

                return

            # Mark current state as explored
            explored.add(node.state)

            # Look at all valid neighbors
            for action, state in self.neighbors(node.state):

                # Only add it if:
                # 1. it has not already been explored
                # 2. it is not already waiting in frontier
                if (
                    state not in explored
                    and not frontier.contains_state(state)
                ):

                    child = Node(
                        state=state,
                        parent=node,
                        action=action
                    )

                    frontier.add(child)


# -----------------------------
# Run the program
# -----------------------------

maze = Maze("maze1.txt")

maze.solve()