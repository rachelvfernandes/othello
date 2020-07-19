import math
import sys
import numpy as np

#Player tokens
B = 0 #black
W = 1 #white
E = 2 #empty
winners = {0: "Black", 1: "White", 2: "Tie"}
opponents = {W: B, B: W}

#Directions on the board
directions = np.array([[0, -1], [0, +1], [-1, 0], [+1, 0], [-1, -1], [+1, -1], [-1, +1], [+1, +1]])

#Board
current_board = np.array([
[E, E, E, E, E, E, E, E],
[E, E, E, E, E, E, E, E],
[E, E, E, E, E, E, E, E],
[E, E, E, W, B, E, E, E],
[E, E, E, B, W, E, E, E],
[E, E, E, E, E, E, E, E],
[E, E, E, E, E, E, E, E],
[E, E, E, E, E, E, E, E],
])

#Weighting of spaces on the board
weighting = np.array([
[4, -3, 2, 2, 2, 2, -3, 4],
[-3, -4, -1, -1, -1, -1, -4, -3],
[2, -1, 1, 0, 0, 1, -1, 2],
[2, -1, 0, 1, 1, 0, -1, 2],
[2, -1, 0, 1, 1, 0, -1, 2],
[2, -1, 1, 0, 0, 1, -1, 2],
[-3, -4, -1, -1, -1, -1, -4, -3],
[4, -3, 2, 2, 2, 2, -3, 4],
])

current_player = B


def possible_moves(board, player):
    # This method finds instances of pieces and checks for empty spaces. Finding empty spaces and checking for instances of pieces might be better
    opponent = opponents[player]
    moves = set()
    player_instances = np.where(board == player)
    for player_instance in list(zip(player_instances[0], player_instances[1])):
        for direction in directions:
            dist = 1
            x = direction[0] * dist + player_instance[0]
            y = direction[1] * dist + player_instance[1]
            while -1 < x < 8 and -1 < y < 8 and board[x][y] == opponent:
                dist += 1
                x = direction[0] * dist + player_instance[0]
                y = direction[1] * dist + player_instance[1]
            if dist > 1 and -1 < x < 8 and -1 < y < 8 and board[x][y] == E:
                moves.add((direction[0] * dist + player_instance[0], direction[1] * dist + player_instance[1]))
    return list(moves)

def get_next_player(board, player):
    opponent = opponents[player]
    if len(possible_moves(board, opponent)):
        return opponent
    if len(possible_moves(board, player)):
        return player
    return None

def make_move(board, player, move):
    opponent = opponents[player]
    board[move[0]][move[1]] = player
    for direction in directions:
        dist = 1
        x = direction[0] * dist + move[0]
        y = direction[1] * dist + move[1]
        while -1 < x < 8 and -1 < y < 8 and board[x][y] == opponent:
            dist += 1
            x = direction[0] * dist + move[0]
            y = direction[1] * dist + move[1]
        if dist > 1 and -1 < x < 8 and -1 < y < 8 and board[x][y] == player:
            for c in range(1, dist):
                board[direction[0] * c + move[0]][direction[1] * c + move[1]] = player
    return board

def minimax(board, player, depth, alpha, beta):
    opponent = opponents[player]
    best = {W: min, B: max}
    if depth == 0:
        score = score_board(board)
        return None, score
    possibles = []
    for move in possible_moves(board, player):
        new_board = make_move(board.copy(), player, move) #use a copy unless you want it to edit the original board!
        next_player = get_next_player(new_board, player)
        if next_player is None:
            if len(np.where(board == B)[0]) == len(np.where(board == W)[0]):
                score = 0
            elif player == B:
                score = math.inf
            elif player == W:
                score = -math.inf
        else:
            score = minimax(new_board, next_player, depth - 1, alpha, beta)[1]
        possibles.append((move, score))
        if player == B:
            if score > alpha:
                alpha = score
        elif player == W:
            if score < beta:
                beta = score
        if alpha >= beta:
            break
    if len(possibles) > 0:
        return best[player](possibles, key=lambda x: x[1])
    else:
        return -1, -1

def best_move(board, player):
    #   If corner taken, dont weight adjacent pieces negatively.
    depth = 3
    move = minimax(board, player, depth, -math.inf, math.inf)[0]
    print(move)
    return make_move(board.copy(), player, move)

def edge_build(edge, player):
    num_other_player_in_between = 0
    for space in edge:
        if space == E:
            return num_other_player_in_between
        elif space == player:
            num_other_player_in_between += 1
    return num_other_player_in_between

def score_board(board):
    black_tokens = np.where(board == B)
    black_tokens = list(zip(black_tokens[0], black_tokens[1]))
    white_tokens = np.where(board == W)
    white_tokens = list(zip(white_tokens[0], white_tokens[1]))
    spaces_filled = len(black_tokens) + len(white_tokens)
    spaces_left = 64 - spaces_filled
    tokens_acquired = len(black_tokens) - len(white_tokens)
    black_moves = possible_moves(board, B)
    white_moves = possible_moves(board, W)
    mobility = len(black_moves) - len(white_moves)
    weighted_tokens = 0
    for tok in black_tokens:
        weighted_tokens += weighting[tok[0]][tok[1]]
    for tok in white_tokens:
        weighted_tokens -= weighting[tok[0]][tok[1]]
    weighted_moves = 0
    for move in black_moves:
        weighted_moves += weighting[move[0]][move[1]]
    for move in white_moves:
        weighted_moves -= weighting[move[0]][move[1]]
    return spaces_left*weighted_tokens + spaces_filled*tokens_acquired + 0.9*spaces_left*weighted_moves + 0.2*spaces_filled*mobility


# Play the game until the board is full or no one can move
while current_player is not None:
    current_board = best_move(current_board, current_player)
    print(current_board)
    current_player = get_next_player(current_board, current_player)

#Score the board
black_score = len(np.where(current_board == B)[0])
white_score = len(np.where(current_board == W)[0])
if black_score > white_score:
    winner = B
elif white_score < black_score:
    winner = W
else:
    winner = E #tie
print(winners[winner])

