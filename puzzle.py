import heapq

class PuzzleNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = 0 if parent is None else parent.cost + 1

    def __lt__(self, other):
        return (self.cost + self.heuristic()) < (other.cost + other.heuristic())

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

    def __str__(self):
        return str(self.state)

    def get_blank_position(self):
        for i, row in enumerate(self.state):
            for j, tile in enumerate(row):
                if tile == 0:
                    return i, j

    def get_successors(self):
        successors = []
        i, j = self.get_blank_position()

        for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_i, new_j = i + move[0], j + move[1]

            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row[:] for row in self.state]
                new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
                successors.append(PuzzleNode(new_state, self, move))

        return successors

    def is_goal(self, goal_state):
        return self.state == goal_state

    def heuristic(self):
        # Manhattan distance heuristic
        total_distance = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0:
                    goal_i, goal_j = divmod(self.state[i][j] - 1, 3)
                    total_distance += abs(i - goal_i) + abs(j - goal_j)
        return total_distance
def solve_puzzle(initial_state, goal_state):
    initial_node = PuzzleNode(initial_state)
    goal_node = PuzzleNode(goal_state)

    open_set = [initial_node]
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.is_goal(goal_state):
            states = [current_node.state]
            while current_node.parent:
                current_node = current_node.parent
                states.append(current_node.state)
            return states[::-1]

        closed_set.add(current_node)

        successors = current_node.get_successors()
        for successor in successors:
            if successor not in closed_set and successor not in open_set:
                heapq.heappush(open_set, successor)

    return None  # No solution found

# Example usage:
initial_state = [[7,2,8], [5,4,6], [3,1,0]]
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

solution_states = solve_puzzle(initial_state, goal_state)

if solution_states:
    for state in solution_states:
        for row in state:
            print(row)
        print()
else:
    print("No solution found.")
