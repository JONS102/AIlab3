#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system

HUMAN = -1
COMP = +1
SIZE = 10  # Kích thước bảng
WIN_CONDITION = 5  # Số ô liên tiếp để thắng
board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

def evaluate(state):
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0
    return score

def wins(state, player):
    # Kiểm tra hàng ngang
    for row in range(SIZE):
        for col in range(SIZE - WIN_CONDITION + 1):
            if all(state[row][col + i] == player for i in range(WIN_CONDITION)):
                return True

    # Kiểm tra hàng dọc
    for col in range(SIZE):
        for row in range(SIZE - WIN_CONDITION + 1):
            if all(state[row + i][col] == player for i in range(WIN_CONDITION)):
                return True

    # Kiểm tra đường chéo chính
    for row in range(SIZE - WIN_CONDITION + 1):
        for col in range(SIZE - WIN_CONDITION + 1):
            if all(state[row + i][col + i] == player for i in range(WIN_CONDITION)):
                return True

    # Kiểm tra đường chéo phụ
    for row in range(WIN_CONDITION - 1, SIZE):
        for col in range(SIZE - WIN_CONDITION + 1):
            if all(state[row - i][col + i] == player for i in range(WIN_CONDITION)):
                return True

    return False

def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)

def empty_cells(state):
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells

def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False

def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False

def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best

def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

def render(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '-' * (SIZE * 4 + 1)

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} ', end='')
        print('|\n' + str_line)

def ai_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Lượt của máy [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == SIZE * SIZE:
        x = choice(range(SIZE))
        y = choice(range(SIZE))
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)

def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    moves = {i + 1: [i // SIZE, i % SIZE] for i in range(SIZE * SIZE)}

    clean()
    print(f'Lượt của người chơi [{h_choice}]')
    render(board, c_choice, h_choice)

    move = -1
    while move < 1 or move > SIZE * SIZE:
        try:
            move = int(input(f'Sử dụng bàn phím số (1..{SIZE * SIZE}): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Nước đi không hợp lệ')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Tạm biệt')
            exit()
        except (KeyError, ValueError):
            print('Lựa chọn không hợp lệ')

def input_initial_state():
    print(f"Nhập trạng thái ban đầu của bảng (lưới {SIZE}x{SIZE}). Sử dụng 0 cho ô trống, -1 cho người chơi, và 1 cho máy tính:")
    for i in range(SIZE):
        row = input(f"Hàng {i + 1} (các giá trị cách nhau bằng dấu phẩy): ")
        board[i] = [int(x) for x in row.split(",")]

def main():
    clean()
    h_choice = ''
    c_choice = ''
    first = ''

    input_initial_state()

    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Chọn X hoặc O\nĐã chọn: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Tạm biệt')
            exit()
        except (KeyError, ValueError):
            print('Lựa chọn không hợp lệ')

    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('Bắt đầu trước?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Tạm biệt')
            exit()
        except (KeyError, ValueError):
            print('Lựa chọn không hợp lệ')

    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    if wins(board, HUMAN):
        clean()
        print(f'Lượt của người chơi [{h_choice}]')
        render(board, c_choice, h_choice)
        print('BẠN THẮNG!')
    elif wins(board, COMP):
        clean()
        print(f'Lượt của máy [{c_choice}]')
        render(board, c_choice, h_choice)
        print('BẠN THUA!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('HÒA!')

    exit()

if __name__ == '__main__':
    main()