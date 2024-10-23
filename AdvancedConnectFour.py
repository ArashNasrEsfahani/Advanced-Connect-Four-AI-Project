import numpy as np
import random
import pygame
import sys
import math

def initialize_board():
	board = np.zeros((M, N))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_loc(board, col):
	return board[M-1][col] == 0

def next_available_row(board, col):
	for i in range(M):
		if (board[i][col] == 0):
			return i

def print_board(board):
	print(np.flip(board, 0))

def is_end_node(board):
	return win_check(board, RED_PIECE) or win_check(board, BLUE_PIECE) or len(get_valid_location(board)) == 0

def get_valid_location(board):
	validLoc = []
	for col in range(N):
		if is_valid_loc(board, col):
			validLoc.append(col)
	return validLoc

def draw_board(board):
	for j in range(N):
		for i in range(M):     
			pygame.draw.circle(screen, WHITE, (int(j*windowSize + windowSize/2), int(i*windowSize + windowSize + windowSize/2)), radius)
	
	for j in range(N):
		for i in range(M):		
			if board[i][j] == RED_PIECE:
				pygame.draw.circle(screen, RED, (int(j*windowSize + windowSize/2), height-int(i*windowSize + windowSize/2)), radius)
			elif board[i][j] == BLUE_PIECE: 
				pygame.draw.circle(screen, BLUE, (int(j*windowSize + windowSize/2), height-int(i*windowSize + windowSize/2)), radius)
	pygame.display.update()


def win_check(board, piece):
	for c in range(N - 3):
		for r in range(M):
			if (board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece):
				return True

	for c in range(N):
		for r in range(M-3):
			if (board[r][c] == piece and board[r + 1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece):
				return True

	for c in range(N - 3):
		for r in range(M-3):
			if (board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece):
				return True

	for c in range(N - 3):
		for r in range(3, M):
			if (board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece):
				return True

def cut_score(cut, piece):

	score = 0
	enemyPiece = RED_PIECE
	if piece == RED_PIECE:
		enemyPiece = BLUE_PIECE

	if (cut.count(piece) == 4):
		score += 225
	elif (cut.count(piece) == 3 and cut.count(0) == 1):
		score += 22
	elif (cut.count(piece) == 2 and cut.count(0) == 2):
		score += 16
	if (cut.count(enemyPiece) == 3 and cut.count(0) == 1):
		score -= 20

	return score

def evaluate_score(board, piece):
	score = 0

	center_array = [int(i) for i in list(board[:, N//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	for r in range(M):
		tempRow = [int(i) for i in list(board[r,:])]
		for c in range(N - 3):
			cut = tempRow[c: c + 4]
			score += cut_score(cut, piece)

	for c in range(N):
		tempCol = [int(i) for i in list(board[:,c])]
		for r in range(M - 3):
			cut = tempCol[r: r + 4]
			score += cut_score(cut, piece)

	for r in range(M - 3):
		for c in range(N - 3):
			cut = [board[r + i][c + i] for i in range(4)]
			score += cut_score(cut, piece)

	for r in range(M-3):
		for c in range(N - 3):
			cut = [board[r + 3 -i][c + i] for i in range(4)]
			score += cut_score(cut, piece)

	return score

def minimax(board, depth, a, b, maximizing):

	validLoc = get_valid_location(board)
	isEnd = is_end_node(board)

	if depth == 0 or isEnd:
		if isEnd:
			if win_check(board, BLUE_PIECE):
				return (None, 999999999)
			elif win_check(board, RED_PIECE):
				return (None, -999999999)
			else: 
				return (None, 0)

		else: 
			return (None, evaluate_score(board, BLUE_PIECE))

	if maximizing:
		value = -math.inf
		column = random.choice(validLoc)

		for col in validLoc:
			row = next_available_row(board, col)
			boardCopy = board.copy()
			drop_piece(boardCopy, row, col, BLUE_PIECE)
			newScore = minimax(boardCopy, depth-1, a, b, False)[1]
            
			if newScore > value:
				value = newScore
				column = col
			a = max(a, value)
			if a >= b:
				break
		return column, value

	else:
		value = math.inf
		column = random.choice(validLoc)

		for col in validLoc:
			row = next_available_row(board, col)
			boardCopy = board.copy()
			drop_piece(boardCopy, row, col, RED_PIECE)
			newScore = minimax(boardCopy, depth - 1, a, b, True)[1]
			if newScore < value:
				value = newScore
				column = col
			b = min(b, value)
			if a >= b:
				break
		return column, value




############"Gobal Parameters"##############
print("Choose M and N Seperated by Space:")
temp = input().split()
M = int(temp[0])
N = int(temp[1])
RED_PIECE = 1
BLUE_PIECE = 2
WHITE = (224,224,224)
RED = (255,0,0)
BLUE = (0,0,255)
###########################################

if __name__ == '__main__':

    #Choosing Game Mode
    while True:
        print("Choose Game Mode:\n 1- Human VS Human \n 2- Human VS AI \n 3- AI vs AI")
        gameMode = int(input())
        if (gameMode == 1):
            P1 = 0
            P2 = 1
            break        
        elif (gameMode == 2):
            P1 = 0
            AI1 = 1
            break
        elif (gameMode == 3):
            AI1 = 0
            AI2 = 1
            break
        else:
            print("I'm sorry. We only have three modes and you have to choose one of them. Try Again!")

    #Initializing some basic paramneters and the board      
    board = initialize_board()
    print_board(board)
    pygame.init()

    gameOver = False
    windowSize = 70
    width = N * windowSize
    height = (M + 1) * windowSize
    size = (width, height)
    radius = int(windowSize/2 - 4)
    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()
    gameFont = pygame.font.SysFont("Comic Sans", 38)

    turn = random.randint(0,1)

    if (gameMode == 1): #Human VS. Human Mode

        while not gameOver:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    sys.exit()
        
                if (event.type == pygame.MOUSEMOTION):
                    pygame.draw.rect(screen, WHITE, (0,0, width, windowSize))
                    dropPosition = event.pos[0]
                    if (turn == 0):
                        pygame.draw.circle(screen, RED, (dropPosition, int(windowSize/2)), radius)
                    else: 
                        pygame.draw.circle(screen, BLUE, (dropPosition, int(windowSize/2)), radius)
                pygame.display.update()
        
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    pygame.draw.rect(screen, WHITE, (0,0, width, windowSize))
                    
                    if (turn == 0):
                        dropPosition = event.pos[0]
                        col = int(math.floor(dropPosition/windowSize))

                        if is_valid_loc(board, col):
                            row = next_available_row(board, col)
                            drop_piece(board, row, col, 1)
                        
                            if win_check(board, 1):
                                label = gameFont.render("Player 1 Won!", 1, RED)
                                screen.blit(label, (10,10))
                                gameOver = True

                    else:         
                        dropPosition = event.pos[0]
                        col = int(math.floor(dropPosition/windowSize))
        
                        if is_valid_loc(board, col):
                            row = next_available_row(board, col)
                            drop_piece(board, row, col, 2)
                            
                            if win_check(board, 2):
                                label = gameFont.render("Player 2 Won!", 1, BLUE)
                                screen.blit(label, (40,10))
                                gameOver = True

                    print_board(board)
                    draw_board(board)
        
                    turn += 1
                    turn = turn % 2
        
                    if gameOver:
                        pygame.time.wait(2500)  

    elif (gameMode == 2):#Human VS. AI Mode

        while not gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, WHITE, (0,0, width, windowSize))
                    dropPosition = event.pos[0]
                    if turn == P1:
                        pygame.draw.circle(screen, RED, (dropPosition, int(windowSize/2)), radius)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, WHITE, (0,0, width, windowSize))

                    if turn == P1:
                        dropPosition = event.pos[0]
                        col = int(math.floor(dropPosition/windowSize))

                        if is_valid_loc(board, col):
                            row = next_available_row(board, col)
                            drop_piece(board, row, col, RED_PIECE)

                            if win_check(board, RED_PIECE):
                                label = gameFont.render("You Won!", 1, RED)
                                screen.blit(label, (40,10))
                                gameOver = True

                            turn += 1
                            turn = turn % 2

                            print_board(board)
                            draw_board(board)
                        
            if (turn == AI1 and not gameOver):	

                col, useless_score = minimax(board, 5, -math.inf, math.inf, True)

                if is_valid_loc(board, col):
                    row = next_available_row(board, col)
                    drop_piece(board, row, col, BLUE_PIECE)

                    if win_check(board, BLUE_PIECE):
                        label = gameFont.render("AI Won :(", 1, BLUE)
                        screen.blit(label, (40,10))
                        gameOver = True

                    print_board(board)
                    draw_board(board)
                    turn += 1
                    turn = turn % 2

            if gameOver:
                pygame.time.wait(2500)


    elif (gameMode == 3): #AI VS. AI Mode

        while not gameOver:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    sys.exit()
            
            if (turn == AI1 and not gameOver):				
                col, useless_score = minimax(board, 5, -math.inf, math.inf, True)

                if is_valid_loc(board, col):
                    row = next_available_row(board, col)
                    drop_piece(board, row, col, BLUE_PIECE)

                    if win_check(board, BLUE_PIECE):
                        label = gameFont.render("AI 1 Won!", 1, BLUE)
                        screen.blit(label, (40,10))
                        gameOver = True
                    print_board(board)
                    draw_board(board)
                    turn += 1
                    turn = turn % 2
                    pygame.time.wait(500)
        
            if (turn == AI2 and not gameOver):				
                col, useless_score = minimax(board, 5, -math.inf, math.inf, True)

                if is_valid_loc(board, col):
                    row = next_available_row(board, col)
                    drop_piece(board, row, col, RED_PIECE)

                    if win_check(board, RED_PIECE):
                        label = gameFont.render("AI 2 Won!", 1, RED)
                        screen.blit(label, (40,10))
                        gameOver = True
                    
                    print_board(board)
                    draw_board(board)
                    turn += 1
                    turn = turn % 2
                    pygame.time.wait(500)

            if gameOver:
                pygame.time.wait(2500)
                