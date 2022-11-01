from collections import deque
import random
from re import M
from turtle import back
from copy import deepcopy

visited = {}
solution = -1
path_bck = []

visited_bfs = {}
solution_bfs = -1
path_bfs = {}
queue = deque()


def get_initial_state(k, capacity1, capacity2):
    return k, [capacity1, 0], [capacity2, 0]


def gcd(x, y):
    if y == 0:
        return x
    return gcd(y, x % y)


def is_solvable(x, y, k):
    if k % gcd(x, y) == 0 and (x + y) > k:
        return True
    return False


def is_final_state(state):
    if state[1][1] == state[0] or state[2][1] == state[0] or ((state[1][1] + state[2][1]) == state[0]):
        return True
    return False


def validate_fill_transition(state, jug):
    return state[jug][0] != state[jug][1]


def validate_pour_transition(state, jug, jug2):
    if state[jug][1] != state[jug][0] and state[jug2][0] != 0:
        return True
    return False


def validate_empty_transition(state, jug):
    if state[jug][1] != 0:
        return True
    return False


def fill_transition(state, jug):
    """

    :param state: current state
    :param jug: the jug to be filled
    :return: is_successful, new_state
    """
    new_state = deepcopy(state)
    if validate_fill_transition(new_state, jug):
        new_state[jug][1] = new_state[jug][0]
        return 1, new_state
    else:
        return -1, new_state


def pour_transition(state, jug):
    """
    pour water from one jug to another
    :param state: current state
    :param jug: jug to which we pour water
    :return: is_successful, new_state
    """
    jug2 = 1
    if jug == 1:
        jug2 = 2
    new_state = deepcopy(state)
    if validate_pour_transition(new_state, jug, jug2):
        quantity_to_pour = min(new_state[jug2][1], new_state[jug][0] - new_state[jug][1])
        new_state[jug][1] += quantity_to_pour
        new_state[jug2][1] -= quantity_to_pour
        return 1, new_state
    else:
        return -1, new_state


def empty_transition(state, jug):
    new_state = deepcopy(state)
    if validate_empty_transition(new_state, jug):
        new_state[jug][1] = 0
        return 1, new_state
    else:
        return -1, new_state


def backtracking(state):
    global visited
    global solution
    global path_bck
    if is_final_state(state):
        solution = state
        for i in path_bck:
            print(i)
    if solution == -1:
        for operation in range(0, 3):
            for jug_index in range(1, 3):
                if operation == 0:
                    is_successful, new_state = fill_transition(state, jug_index)
                elif operation == 1:
                    is_successful, new_state = pour_transition(state, jug_index)
                else:
                    is_successful, new_state = empty_transition(state, jug_index)

                if is_successful and (new_state[1][1], new_state[2][1]) not in visited:
                    visited[(new_state[1][1], new_state[2][1])] = 1
                    path_bck.append(state)
                    backtracking(new_state)
                    path_bck.pop()


def check_if_transition_successful_bfs(is_successful, new_state):
    global visited_bfs
    if is_successful and ((new_state[1][1], new_state[2][1]) not in visited_bfs):
        visited_bfs[(new_state[1][1], new_state[2][1])] = 1
        return True
    return False


def print_path(state):
    if (state[1][1], state[2][1]) in path_bfs:
        print_path(path_bfs[(state[1][1], state[2][1])])
        print(state)


def breadth_first_search(state):
    """

    :param state: the state passed as parameter
    :return:
    """
    global visited_bfs
    global solution_bfs
    global path
    global queue
    global path_bfs

    if state not in queue:
        queue.append(state)

    if solution_bfs == -1:
        for jug_index in range(1, 3):
            # fill transition
            is_successful, new_state = fill_transition(state, jug_index)
            if check_if_transition_successful_bfs(is_successful, new_state):
                queue.append(new_state)
                if (new_state[1][1], new_state[2][1]) not in path_bfs:
                    path_bfs[(new_state[1][1], new_state[2][1])] = state
                    if is_final_state(new_state):
                        solution_bfs = new_state
                        print_path(new_state)
                        exit()

            # pour transition
            is_successful, new_state = pour_transition(state, jug_index)
            if check_if_transition_successful_bfs(is_successful, new_state):
                queue.append(new_state)
                if (new_state[1][1], new_state[2][1]) not in path_bfs:
                    path_bfs[(new_state[1][1], new_state[2][1])] = state
                    if is_final_state(new_state):
                        solution_bfs = new_state
                        print_path(new_state)
                        exit()

            # empty transition
            is_successful, new_state = empty_transition(state, jug_index)
            if check_if_transition_successful_bfs(is_successful, new_state):
                queue.append(new_state)
                if (new_state[1][1], new_state[2][1]) not in path_bfs:
                    path_bfs[(new_state[1][1], new_state[2][1])] = state
                    if is_final_state(new_state):
                        solution_bfs = new_state
                        print_path(new_state)
                        exit()

        # print("path", path)gf
        queue.popleft()
        if len(queue) > 0:
            breadth_first_search(queue[0])
        else:
            print("no solution")


def improvement_func(state):
    return 1 - (abs(state[0] - state[1][1]) + abs(state[0] - state[2][1])) / state[0]

global heur_state

def hill_climbing(state):
    arr_solutions = list()
    while True:
        operation = random.randint(0, 9)
        for jug_index in range(1, 3):
            if operation == 0:
                is_successful, new_state = fill_transition(state, jug_index)
                if is_successful:
                    arr_solutions.append(new_state)

            elif operation == 1:
                is_successful, new_state = pour_transition(state, jug_index)
                if is_successful:
                    arr_solutions.append(new_state)
            else:
                is_successful, new_state = empty_transition(state, jug_index)
                if is_successful:
                    arr_solutions.append(new_state)

        best_fit = -1
        best_state = state
        heuristic_results = list()
        for elm in arr_solutions:
            # print(elm)
            # heuristic_results[tuple(elm)] = improvement_func(elm)
            # heuristic_results[tuple(elm)] = improvement_func(elm)
            # best
            heuristic_results.append(tuple((elm[1][1], elm[2][1])))

        for key, value in heuristic_results:
            if value < best_fit:
                best_fit = value
                best_state = key

        state = best_state
        print(state)
        # print(best_fit)


def water_jug_problem(k, capacity1, capacity2):
    global path_bck
    if not is_solvable(capacity1, capacity2, k):
        print("It's not solvable")
        exit()
    state = get_initial_state(k, capacity1, capacity2)

    # print('Backtracking')
    # visited[(0, 0)] = 1
    # backtracking(state)
    # print(solution)
    #
    # print('BFS')
    # visited_bfs[(0, 0)] = 1
    # breadth_first_search(state)

    hill_climbing(state)


if __name__ == '__main__':
    water_jug_problem(4, 3, 5)
