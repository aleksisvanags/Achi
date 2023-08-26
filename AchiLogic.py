# AchiLogic
# Aleksis Vanags
# 26/08/2023

import json
import AchiCommonVariables
from math import sqrt

def Process(move):
    move = json.loads(move)

    if move == "r":
        AchiCommonVariables.oPieces = 4
        AchiCommonVariables.bPieces = 4
        AchiCommonVariables.grid = [[2, 2, 2],
                [2, 2, 2],
                [2, 2, 2],
                [2]]
        AchiCommonVariables.turn = True
    else:
        x = move[0]
        y = move[1]

        if (AchiCommonVariables.turn and (AchiCommonVariables.oPieces > 0)) or ((not AchiCommonVariables.turn) and (AchiCommonVariables.bPieces > 0)):
            Placement(x, y)
        else:
            Move(move)

def Placement(x, y):
    r = x // (AchiCommonVariables.WIDTH // AchiCommonVariables.ROWS)
    c = y // (AchiCommonVariables.HEIGHT // AchiCommonVariables.COLS)

    if AchiCommonVariables.grid[r][c] == 2:
        if AchiCommonVariables.turn:
            AchiCommonVariables.grid[r][c] = 0
            AchiCommonVariables.oPieces -= 1
        else:
            AchiCommonVariables.grid[r][c] = 1
            AchiCommonVariables.bPieces -= 1
    
        AchiCommonVariables.turn = not AchiCommonVariables.turn
        AchiCommonVariables.grid[3][0] = AchiCommonVariables.turn

def Move(clickPos):
    emptySquare = [-1, -1]
    r = clickPos[0] // (AchiCommonVariables.WIDTH // AchiCommonVariables.ROWS)
    c = clickPos[1] // (AchiCommonVariables.HEIGHT // AchiCommonVariables.COLS)

    for row in range(AchiCommonVariables.ROWS):
            for col in range(AchiCommonVariables.COLS):
                if AchiCommonVariables.grid[row][col] == 2:
                    emptySquare = [row, col]

    if AchiCommonVariables.turn and (AchiCommonVariables.grid[r][c] == 0):
        if (emptySquare == [1, 1]) or (r == c == 1) or (sqrt(((r - emptySquare[0]) ** 2) + ((c - emptySquare[1]) ** 2)) == 1):
            AchiCommonVariables.grid[emptySquare[0]][emptySquare[1]] = 0
            AchiCommonVariables.grid[r][c] = 2
            AchiCommonVariables.turn = not AchiCommonVariables.turn
    elif (not AchiCommonVariables.turn) and (AchiCommonVariables.grid[r][c] == 1):
        if (emptySquare == [1, 1]) or (r == c == 1) or (sqrt(((r - emptySquare[0]) ** 2) + ((c - emptySquare[1]) ** 2)) == 1):
            AchiCommonVariables.grid[emptySquare[0]][emptySquare[1]] = 1
            AchiCommonVariables.grid[r][c] = 2
            AchiCommonVariables.turn = not AchiCommonVariables.turn
    else:
        pass

    AchiCommonVariables.grid[3][0] = AchiCommonVariables.turn