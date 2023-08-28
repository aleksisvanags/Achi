# AchiClient
# Aleksis Vanags
# 26/08/2023 - 27/08/2023

import socket
import threading
import json
import pygame

FORMAT = "utf-8"
PORT = 5050
# EDIT Change the 'SERVER' variable as approprate.
# See README.md for guidance.
SERVER = ""
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

WIDTH = 420
HEIGHT = 420
ROWS = 3
COLS = 3
SQUARE_SIZE = HEIGHT//ROWS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 90, 255)
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Achi")

grid = [[2, 2, 2],
        [2, 2, 2],
        [2, 2, 2],
        [2]]

def main():
    pygame.init()
    pygame.font.init()

    font = pygame.font.SysFont("Consolas", 32, False, False)
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    run = True
    win = False

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif (event.type == pygame.MOUSEBUTTONDOWN) and (not win):
                x, y = pygame.mouse.get_pos()
                MESSAGE = [x, y]
                Send(json.dumps(MESSAGE))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    Send(json.dumps("r"))

        DrawBoard(WIN)
        win = CheckWin()

        if win:
            turn = grid[3][0]

            if turn:
                winner = "Blue Wins!"
            else:
                winner = "Orange Wins!"

            winnerText = font.render(winner, True, WHITE, BLACK)
            resetText = font.render("Press 'r' to Reset", True, WHITE, BLACK)
            winnerTextRect = winnerText.get_rect()
            resetTextRect = resetText.get_rect()
            winnerTextRect.center = (WIDTH // 2, HEIGHT // 3)
            resetTextRect.center = (WIDTH // 2, HEIGHT // 2)
            winnerScreenFade = pygame.Surface((WIDTH, HEIGHT))

            winnerScreenFade.fill(BLACK)
            winnerScreenFade.set_alpha(160)
            winnerScreenFade.blit(winnerText, winnerTextRect)
            winnerScreenFade.blit(resetText, resetTextRect)
            WIN.blit(winnerScreenFade, (0, 0))

        pygame.display.update()

    pygame.quit()

def DrawBoard(win):
    win.fill(BLACK)

    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 0:
                pygame.draw.rect(win, ORANGE, (r * SQUARE_SIZE, c * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif grid[r][c] == 1:
                pygame.draw.rect(win, BLUE, (r * SQUARE_SIZE, c * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(win, WHITE, (r * SQUARE_SIZE, c * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            pygame.draw.rect(win, BLACK, ((r * SQUARE_SIZE) - 1, 0, 2, HEIGHT))
            pygame.draw.rect(win, BLACK, (0, (c * SQUARE_SIZE) - 1, WIDTH, 2))

def CheckWin():
    if grid[0][0] == grid[0][1] == grid[0][2] != 2:
        return True
    elif grid[1][0] == grid[1][1] == grid[1][2] != 2:
        return True
    elif grid[2][0] == grid[2][1] == grid[2][2] != 2:
        return True
    elif grid[0][0] == grid[1][0] == grid[2][0] != 2:
        return True
    elif grid[0][1] == grid[1][1] == grid[2][1] != 2:
        return True
    elif grid[0][2] == grid[1][2] == grid[2][2] != 2:
        return True
    elif grid[0][0] == grid[1][1] == grid[2][2] != 2:
        return True
    elif grid[0][2] == grid[1][1] == grid[2][0] != 2:
        return True
    else:
        return False

def Send(msg):
    client.send(msg.encode(FORMAT))

def RecieveBoard():
    while True:
        global grid

        msg = client.recv(368).decode(FORMAT)
        grid = json.loads(msg)

if __name__ == "__main__":
    thread = threading.Thread(target=RecieveBoard)
    thread.start()
    main()
