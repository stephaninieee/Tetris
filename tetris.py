#!/usr/bin/env python

from tetrislib import *
import time, threading, random

prepare_terminal()

# ─────────────────────────────── Shapes ────────────────────────────────
# Every shape is defined inside its own 4×4 bounding box.
SHAPES = {
    1: [(0, 1), (1, 0), (1, 1), (1, 2)],      # T
    2: [(0, 0), (0, 1), (0, 2), (0, 3)],      # I
    3: [(0, 0), (0, 1), (1, 0), (1, 1)],      # O
    4: [(0, 2), (1, 0), (1, 1), (1, 2)],      # L
    5: [(0, 0), (1, 0), (1, 1), (1, 2)],      # J
    6: [(0, 1), (0, 2), (1, 0), (1, 1)],      # S
    7: [(0, 0), (0, 1), (1, 1), (1, 2)],      # Z
}


def place_block(block, val):
    for y, x in block:
        board[y][x] = val

def move_block(block, dir):
    dx, dy  = 0, 0
    if dir == "left":
        dx -=1
    elif dir == "right":
        dx +=1
    elif dir == "down":
        dy +=1
    
    new_pos = [(y + dy, x + dx) for y, x in block]
    if valid_move(new_pos):
        return new_pos
    else:
        return block

def valid_move(block):
    """
    Collision detection (with sides of game board and other pieces)
    """
    for y, x in block:
        if y < 0 or y >= board_size["y"] or x < 0 or x >= board_size["x"]:
            return False
        if board[y][x] != 0:
            return False
    return True

def stick_block(block, val):
    """
    place block to the board 
    """
    place_block(block, val)
    clear_line()

def clear_line():
    for row in range(board_size["y"]):
        if all(cell != 0 for cell in board[row]):
            for r in range(row, 0, -1):
                board[r] = board[r-1]
            board[0] = [0 for _ in range(board_size["x"])]

    
def new_block():
    """Return a random (piece_coords, pid) pair."""
    pid   = random.randint(1, 7)
    shape = SHAPES[pid]
    off_x = board_size["x"] // 2 - 2
    return [(y, x + off_x) for y, x in shape], pid


def rotate(block):
    min_x = min(x for x, y in block)
    max_x = max(x for x, y in block)
    diff_x = max_x - min_x
    min_y = min(y for x, y in block)
    max_y = max(y for x, y in block)
    diff_y = max_y - min_y 
    size = max(diff_x, diff_y)
    rotated = []
    for x, y in block:
        new_y = (min_x + size) - (y-min_y)
        new_x = min_y + (x - min_x)
        rotated.append((new_y, new_x))

    if valid_move(rotated):
        return rotated
    else:
        return block

t_piece, t_pid = new_block()
place_block(t_piece, t_pid)
draw_board()

drop_intervals = 0.5 
lock = threading.Lock()
running = True

# Thread 1: Auto Drop 
def auto_drop():
    global t_piece, t_pid, running
    last_drop = time.time()
    while running:
        time.sleep(0.05)
        with lock:
            if time.time() - last_drop < drop_intervals:
                continue
            place_block(t_piece, 0)      
            new_pos = move_block(t_piece, "down")
            if new_pos == t_piece:
                stick_block(t_piece, t_pid)
                t_piece, t_pid = new_block()
                if not valid_move(t_piece):
                        running = False
                        print("Game Over")
                        draw_board()
                        break
            else:
                t_piece = new_pos
            place_block(t_piece, t_pid)
            draw_board()
            last_drop = time.time() 


# This code waits for input until the user hits a keystroke.
# get_input() returns one of "left", "up", "right", "down", "exit", or None
# (for all other keys).
# # Thread 2 : handle input
def handle_input():
    global t_piece, t_pid, running
    while running:
        key = get_input()
        with lock:
            place_block(t_piece, 0)
        if key == "left":
            t_piece = move_block(t_piece, "left")
        if key == "right":
            t_piece  = move_block(t_piece,"right")
        if key == "down":
            new_pos = move_block(t_piece,"down") 
            if new_pos == t_piece:
                stick_block(t_piece, t_pid)
                t_piece, t_pid = new_block()
                if not valid_move(t_piece):
                    print("Game Over")
                    draw_board()
                    return False
            else:
                t_piece = new_pos
        if key == "up":
            t_piece = rotate(t_piece) 
        
        elif key == "exit":
            break

        place_block(t_piece, t_pid)
        draw_board()

if __name__ == "__main__":
    t1 = threading.Thread(target=auto_drop,   name="AutoDrop")
    t2 = threading.Thread(target=handle_input, name="Input")
    t1.start(); t2.start()
    t1.join();  t2.join()





