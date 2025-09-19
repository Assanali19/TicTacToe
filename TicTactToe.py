import pygame
import sys
import random

size = 4
win = 3
cell_size = 100
margin = 5
width = height = cell_size * size + margin * (size + 1)
FPS = 60
ANIM_SPEED = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 255, 0, 120)

board = [[' ']*size for _ in range(size)]
animations = []

def check_win_line(board, player):
    for i in range(size):
        for j in range(size - win + 1):
            if all (board[i][j+k] == player for k in range(win)):
                return [(i,j+k) for k in range(win)]
            if all(board[j+k][i] == player for k in range(win)):
                return [(j+k,i) for k in range(win)]
    for i in range(size - win + 1):
        for j in range(size - win + 1):
            if all(board[i+k][j+k] == player for k in range(win)):
                return [(i+k,j+k) for k in range(win)]
            if all (board[i+win-1-k][j+k] == player for k in range(win)):
                return [(i+win-1-k,j+k) for k in range(win)]
    return None

def get_empty(board):
    return [(i, j) for i in range(size) for j in range(size) if board[i][j] == ' ']

def ai_move(board, ai='X', human='O'):
    for i, j in get_empty(board):
        board[i][j] = ai
        if check_win_line(board, ai):
            return (i, j)
        board[i][j] = ' '
    for i, j in get_empty(board):
        board[i][j] = human
        if check_win_line(board, human):
            board[i][j] = ai
            return (i, j)
        board[i][j] = ' '
    center = size // 2
    if board[center][center] == ' ':
        return (center, center)
    for i, j in [(0,0), (0, size-1), (size-1,0), (size-1, size-1)]:
        if board[i][j] == ' ':
            return (i, j)
    return random.choice(get_empty(board))

def draw_board (screen, board, animations, win_line=None):
    screen.fill(BLACK)
    for i in range(size):
        for j in range(size):
            x = margin + j*(cell_size+margin)
            y = margin + i*(cell_size+margin)
            pygame.draw.rect(screen, WHITE, (x, y, cell_size, cell_size))
    for i in range(size):
        for j in range(size):
            for anim in animations:
                if anim[0]==i and anim[1]==j:
                    progress = anim[3]
                    text_size = int(cell_size * progress)
                    font_anim = pygame.font.SysFont(None, text_size)
                    color = RED if anim[2]=='O' else BLUE
                    text = font_anim. render(anim[2], True, color)
                    x = margin + j*(cell_size+margin) + cell_size//2
                    y = margin + i*(cell_size+margin) + cell_size//2
                    rect = text.get_rect(center=(x,y))
                    screen.blit(text, rect)
    if win_line:
        for i,j in win_line:
            x = margin + j*(cell_size+margin)
            y = margin + i*(cell_size+margin)
            s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            s.fill(LIGHT_GREEN)
            screen.blit(s, (x,y))
    pygame.display.flip()

def choose_first():
    global turn
    first_choice = True
    while first_choice:
        screen.fill((0,0,0))
        font = pygame.font.SysFont(None,36)
        text1 = font.render("Presss O, if player goes first", True, (255,255,255))
        text2 = font.render("Presss X, if AI plays first", True, (255,255,255))
        screen.blit(text1, (20, height//2 - 40))
        screen.blit(text2, (20,height//2 + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    turn = "O"
                    first_choice = False
                elif event.key == pygame.K_x:
                    turn = "X"
                    first_choice = False

pygame.init()
screen = pygame.display.set_mode((width, width))
pygame.display.set_caption("Crests and captions 4x4 with light")
clock = pygame.time.Clock()
turn = None
choose_first()
game_over = False
winner = ''
win_line = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and turn == 'O':
            mx, my = event.pos
            j = mx // (cell_size + margin)
            i = my // (cell_size + margin)
            if i < size and j < size and board[i][j] == ' ':
                board[i][j] = 'O'
                animations.append([i, j, 'O', 0])
                win_line = check_win_line(board, 'O')
                if win_line:
                    game_over = True
                    winner = 'You won!'
                elif not get_empty(board):
                    game_over = True
                    winner = 'Draw!'
                else:
                    turn = 'X'
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                board = [[' ']*size for _ in range(size)]
                animations = []
                turn = None
                game_over = False
                winner = ''
                win_line = None
                choose_first()
    
    if turn == 'X' and not game_over:
        i, j = ai_move (board)
        board[i][j] = 'X'
        animations.append([i, j, 'X', 0])
        win_line = check_win_line(board, 'X')
        if win_line:
            game_over = True
            winner = 'I won!'
        elif not get_empty(board):
            game_over = True
            winner = 'Not enough!'
        else:
            turn = 'O'

    for anim in animations:
        if anim[3] < 1:
            anim[3] += 0.1
            if anim[3]> 1:
                anim[3]=1
    
    draw_board(screen, board, animations, win_line)
    
    if game_over:
        font = pygame.font.SysFont(None, 48)
        text = font.render(winner, True, GREEN)
        rect = text.get_rect(center=(width/2, height/2))
        screen.blit(text, rect)

        font_small = pygame.font.SysFont(None,28)
        text_restart = font_small.render("Press R to restart the game", True, GREEN)
        rect_restart = text_restart.get_rect(center=(width/2,height-30))
        screen.blit(text_restart,rect_restart)

        pygame.display.flip()
    clock.tick(FPS)