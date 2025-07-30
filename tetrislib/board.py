# Set up the board.
# The board is represented as an array of arrays, with 10 rows and 10 columns.
board_size = { "x": 10, "y": 10 }
board = [[0] * board_size["x"] for _ in range(board_size["y"])]

# ─────────────────────────────── Display ───────────────────────────────
CHAR_MAP = {
    0: " ",   # empty
    1: "#",   # T
    2: "@",   # I
    3: "$",   # O
    4: "%",   # L
    5: "!",   # J
    6: "&",   # S
    7: "+",   # Z
}


# Draws the contents of the board with a border around it.
def draw_board():
    board_border = "".join(["*" for _ in range(board_size["x"] + 2)])
    print(board_border)
    for y in range(board_size["y"]):
        line = "|"
        for x in range(board_size["x"]):
            line += CHAR_MAP.get(board[y][x], "#") if board[y][x] else " "
        line += "|"
        print(line)
    print(board_border)


