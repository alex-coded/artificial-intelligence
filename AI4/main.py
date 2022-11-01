player1_moves = []
player2_moves = []
player1_matrix = []
player2_matrix = []
player1_dominant_strategy_matrix = []
player2_dominant_strategy_matrix = []


#  Liniile reprezinta mutarile playerului 1
#  Coloanele reprezinta mutarile playerului 2

def read_data():
    global player1_matrix
    global player2_matrix
    global player1_moves
    global player2_moves

    file = open('date.txt', 'r')
    lines = file.readlines()

    # Stim ca avem 2 playeri

    player1_moves = lines[0].split('\t')
    player1_moves = player1_moves[1:]
    player2_moves = lines[1].split('\t')
    player2_moves = player2_moves[1:]

    player1_matrix = [[0 for _ in range(len(player2_moves))] for _ in range(len(player1_moves))]
    player2_matrix = [[0 for _ in range(len(player2_moves))] for _ in range(len(player1_moves))]

    for index in range(2, len(lines)):
        values = lines[index].split('\t')
        values[len(values) - 1] = values[len(values) - 1][:-1]

        for index2 in range(len(values)):
            x, y = values[index2].split('/')
            player1_matrix[index - 2][index2] = int(x)
            player2_matrix[index - 2][index2] = int(y)


def dominant_strategy_player1():
    global player1_matrix
    global player2_matrix
    global player1_moves
    global player2_moves
    global player1_dominant_strategy_matrix
    global player2_dominant_strategy_matrix
    player1_dominant_strategy_matrix = [[0 for _ in range(len(player2_moves))] for _ in range(len(player1_moves))]

    for index_player2_moves in range(len(player2_moves)):
        maximum_gain = -1
        for index_player1_moves in range(len(player1_moves)):
            maximum_gain = max(maximum_gain, player1_matrix[index_player1_moves][index_player2_moves])
        for index_player1_moves in range(len(player1_moves)):
            if player1_matrix[index_player1_moves][index_player2_moves] == maximum_gain:
                player1_dominant_strategy_matrix[index_player1_moves][index_player2_moves] = 1

    for index_player1_moves in range(len(player1_moves)):
        dominant_strategy = True
        for index_player2_moves in range(len(player2_moves)):
            if player1_dominant_strategy_matrix[index_player1_moves][index_player2_moves] == 0:
                dominant_strategy = False
                break
        if dominant_strategy:
            print('Una din strategiile dominante ale player ului 1 este: ' + player1_moves[index_player1_moves])
            return 1
    print('Playerul 1 nu are strategii dominante')
    return -1


def dominant_strategy_player2():
    global player1_matrix
    global player2_matrix
    global player1_moves
    global player2_moves
    global player1_dominant_strategy_matrix
    global player2_dominant_strategy_matrix
    player2_dominant_strategy_matrix = [[0 for _ in range(len(player2_moves))] for _ in range(len(player1_moves))]

    for index_player1_moves in range(len(player1_moves)):
        maximum_gain = -1
        for index_player2_moves in range(len(player2_moves)):
            maximum_gain = max(maximum_gain, player2_matrix[index_player1_moves][index_player2_moves])
        for index_player2_moves in range(len(player2_moves)):
            if player2_matrix[index_player1_moves][index_player2_moves] == maximum_gain:
                player2_dominant_strategy_matrix[index_player1_moves][index_player2_moves] = 1

    for index_player2_moves in range(len(player2_moves)):
        dominant_strategy = True
        for index_player1_moves in range(len(player1_moves)):
            if player2_dominant_strategy_matrix[index_player1_moves][index_player2_moves] == 0:
                dominant_strategy = False
                break
        if dominant_strategy:
            print('Una din strategiile dominante ale player ului 2 este: ' + player2_moves[index_player2_moves])
            return 1
    print('Playerul 2 nu are strategii dominante')
    return -1


def dominant_strategy():
    dominant_strategy_player1()
    dominant_strategy_player2()


def nash_equilibrium():
    global player1_dominant_strategy_matrix
    global player2_dominant_strategy_matrix
    for index_player1_moves in range(len(player1_moves)):
        for index_player2_moves in range(len(player2_moves)):
            if player1_dominant_strategy_matrix[index_player1_moves][index_player2_moves] + \
                    player2_dominant_strategy_matrix[index_player1_moves][index_player2_moves] == 2:
                print('Exista exchilibru Nash\nplayer1: ' + player1_moves[index_player1_moves] + '\nplayer2: ' +
                      player2_moves[index_player2_moves])
                return 1
    print('Nu exista echilibru Nash')
    return -1


if __name__ == '__main__':
    read_data()
    # Testing
    print(player1_matrix)
    print(player2_matrix)
    dominant_strategy()
    nash_equilibrium()



