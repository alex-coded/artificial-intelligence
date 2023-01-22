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
queue = []

visited_hill = {}
solution_hill = -1
path_hill = {}
queue_hill = []

visited_a_star = {}
solution_a_star = -1
path_a_star = {}
queue_a_star = []


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


def print_path_a_star(state):
    if (state[1][1], state[2][1]) in path_a_star:
        print_path_a_star(path_a_star[(state[1][1], state[2][1])])


def breadth_first_search(state):
    """

    :param state: the state passed as parameter
    :return:
    """
    global visited_bfs
    global solution_bfs
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


def heuristic(state):
    return (abs(state[1][1] - state[0])) * (abs(state[2][1] - state[0]))


def heuristic2(state):
    return (abs(state[1][1] - state[0])) * (1 / state[1][0]) + (abs(state[2][1] - state[0])) * (1 / state[2][0])


def improvement_func(state):
    return abs(1 - (abs(state[0] - state[1][1]) + abs(state[0] - state[2][1])) / state[0])


def check_if_transition_successful_hill(is_successful, new_state):
    global visited_hill
    if is_successful:
        if ((new_state[1][1], new_state[2][1]) not in visited_hill):
            return True
        elif visited_hill[(new_state[1][1], new_state[2][1])] < 6:
            return True
    return False


def hill_climbing(state):
    """

    :param state: the state passed as parameter
    :return:
    """
    global visited_hill
    global solution_hill
    global queue_hill
    global path_hill

    if ((state[1][1], state[2][1]) not in visited_hill):
        visited_hill[(state[1][1], state[2][1])] = 1
    else:
        visited_hill[(state[1][1], state[2][1])] += 1

    if solution_hill == -1:
        for jug_index in range(1, 3):
            # fill transition
            is_successful, new_state = fill_transition(state, jug_index)
            if check_if_transition_successful_hill(is_successful, new_state):
                queue_hill.append(new_state)
                if (new_state[1][1], new_state[2][1]) not in path_hill:
                    path_hill[(new_state[1][1], new_state[2][1])] = state
                    if is_final_state(new_state):
                        solution_hill = new_state
                        print_path(new_state)
                        exit()

            # pour transition
            is_successful, new_state = pour_transition(state, jug_index)
            if check_if_transition_successful_hill(is_successful, new_state):
                queue_hill.append(new_state)
                if (new_state[1][1], new_state[2][1]) not in path_hill:
                    path_hill[(new_state[1][1], new_state[2][1])] = state
                    if is_final_state(new_state):
                        solution_hill = new_state
                        print_path(new_state)
                        exit()

            # empty transition
            is_successful, new_state = empty_transition(state, jug_index)
            if check_if_transition_successful_hill(is_successful, new_state):
                queue_hill.append(new_state)
                if (new_state[1][1], new_state[2][1]) not in path_hill:
                    path_hill[(new_state[1][1], new_state[2][1])] = state
                    if is_final_state(new_state):
                        solution_hill = new_state
                        print_path(new_state)
                        exit()

        # print("path", path)gf
        queue_hill.pop(0)
        if len(queue_hill) > 0:
            queue_hill.sort(key=heuristic2)
            print('Test:')
            print(state)
            print(heuristic2(state), heuristic2(queue_hill[0]))
            if heuristic2(state) >= heuristic2(queue_hill[0]):
                future_state = queue_hill[0]
                queue_hill.clear()
                hill_climbing(future_state)
        else:
            print("No solution")


def check_if_transition_successful_a_star(is_successful, new_state):
    global visited_a_star
    if is_successful and ((new_state[1][1], new_state[2][1]) not in visited_a_star):
        visited_a_star[(new_state[1][1], new_state[2][1])] = 1
        return True
    return False


def a_star(state):
    """
    :param state: the state passed as parameter
    :return:
    """
    global visited_a_star
    global solution_a_star
    global queue
    global path_a_star

    if state not in queue:
        queue.append(state)

    if solution_a_star == -1:
        for jug_index in range(1, 3):
            # fill transition
            is_successful, new_state = fill_transition(state, jug_index)
            if check_if_transition_successful_a_star(is_successful, new_state):
                queue.append(new_state)
                if (new_state[1][1], new_state[2][1]) not in path_a_star:
                    path_a_star[(new_state[1][1], new_state[2][1])] = state
                    if is_final_state(new_state):
                        solution_a_star = new_state
                        print_path_a_star(new_state)
                        exit()

            # pour transition
            is_successful, new_state = pour_transition(state, jug_index)
            if check_if_transition_successful_a_star(is_successful, new_state):
                queue.append(new_state)
                if (new_state[1][1], new_state[2][1]) not in path_a_star:
                    path_a_star[(new_state[1][1], new_state[2][1])] = state
                    if is_final_state(new_state):
                        solution_a_star = new_state
                        print_path_a_star(new_state)
                        exit()

            # empty transition
            is_successful, new_state = empty_transition(state, jug_index)
            if check_if_transition_successful_a_star(is_successful, new_state):
                queue.append(new_state)
                if (new_state[1][1], new_state[2][1]) not in path_a_star:
                    path_a_star[(new_state[1][1], new_state[2][1])] = state
                    if is_final_state(new_state):
                        solution_a_star = new_state
                        print_path_a_star(new_state)
                        exit()
        queue.pop(0)
        if len(queue) > 0:
            queue.sort(key=heuristic)
            a_star(queue[0])
        else:
            print("no solution")


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

    # print('BFS')
    # visited_bfs[(0, 0)] = 1
    # breadth_first_search(state)

    print('hill_climbing')
    visited_hill[(0, 0)] = 1
    hill_climbing(state)
    if solution_hill == -1:
        print('Euristica s-a blocat intr-un maxim local, dar exista o solutie')

    # print('A star')
    # visited_a_star[(0, 0)] = 1
    # a_star(state)


if __name__ == '__main__':
    water_jug_problem(4, 3, 5)
