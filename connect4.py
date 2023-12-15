import numpy as np
import pygame, math, sys, random

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
EMPTY = 0
PLAYER = 1
AI = 2
WINDOW_LENGTH = 4
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Connect4')

# Set up the screen
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
screen = pygame.display.set_mode(size)

# Fonts
font = pygame.font.Font("font/lunchds.ttf", 75)
font2 = pygame.font.Font("font/lunchds.ttf", 25)

# Functions

# Create empty array
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

# Place piece into selected column
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check if the selected column has any empty row
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# Return the lowest empty row in seleceted column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Print array
def print_board(board):
    print(np.flip(board, 0))

# Check if the player placed 4 connected pieces
def winning_move(board, piece):
    # Check horizontal
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
            if all(board[r][c+i] == piece for i in range(WINDOW_LENGTH)):
                return True

    # Check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - WINDOW_LENGTH + 1):
            if all(board[r+i][c] == piece for i in range(WINDOW_LENGTH)):
                return True

    # Check diagonal (down-right)
    for r in range(ROW_COUNT - WINDOW_LENGTH + 1):
        for c in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
            if all(board[r+i][c+i] == piece for i in range(WINDOW_LENGTH)):
                return True

    # Check diagonal (up-right)
    for r in range(WINDOW_LENGTH - 1, ROW_COUNT):
        for c in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
            if all(board[r-i][c+i] == piece for i in range(WINDOW_LENGTH)):
                return True

    return False

# Evaluate score for last piece placed
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER if piece == AI else AI

    count_piece = np.sum(window == piece)
    count_empty = np.sum(window == EMPTY)
    count_opp_piece = np.sum(window == opp_piece)

    if count_piece == 4:
        score += 100
    elif count_piece == 3 and count_empty == 1:
        score += 5
    elif count_piece == 2 and count_empty == 2:
        score += 2
    if count_opp_piece == 3 and count_empty == 1:
        score -= 4

    return score

# Evaluate entire game board
def score_position(board, piece):
    score = 0

    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # Check horizontal
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
            window = board[r, c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - WINDOW_LENGTH + 1):
            window = board[r:r+WINDOW_LENGTH, c]
            score += evaluate_window(window, piece)

    # Check diagonal (down-right)
    for r in range(ROW_COUNT - WINDOW_LENGTH + 1):
        for c in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Check diagonal (up-right)
    for r in range(WINDOW_LENGTH - 1, ROW_COUNT):
        for c in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
            window = [board[r-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# Check if the game is won by Player, AI or if the board is full
def is_terminal_node(board):
    return winning_move(board, PLAYER) or winning_move(board, AI) or len(get_valid_locations(board)) == 0

# Minimax algorithm
def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal: # If the game is over
            if winning_move(board, AI):
                return (None, 999999999999)
            elif winning_move(board, PLAYER):
                return (None, -999999999999)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI))

    # AI is trying to place 4 own pieces
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI)
            new_score = minimax(b_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else: # AI is trying to block player pieces
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER)
            new_score = minimax(b_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

# Find all empty locations for placing piece
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# Pick the best move based on the highest score
def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    best_score = 0
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

# Draw array as game board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, "SteelBlue", (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, "Black", (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER:
                pygame.draw.circle(screen, "Yellow", (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == AI:
                pygame.draw.circle(screen, "Red", (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    pygame.display.update()

# Main Game Loop
game_active = False
depth = 3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_active:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos_x, pos_y = event.pos
            if easy_button_rect.collidepoint(pos_x, pos_y):
                print("Easy difficulty selected!")
                depth = 2
                game_active = True
                turn = random.choice([PLAYER, AI])
                board = create_board()  # Restarting the game
            elif medium_button_rect.collidepoint(pos_x, pos_y):
                print("Medium difficulty selected!")
                depth = 3
                game_active = True
                turn = random.choice([PLAYER, AI])
                board = create_board()  # Restarting the game
            elif hard_button_rect.collidepoint(pos_x, pos_y):
                print("Hard difficulty selected!")
                depth = 4
                game_active = True
                turn = random.choice([PLAYER, AI])
                board = create_board()  # Restarting the game

        # Main menu
        screen.fill("SteelBlue")
        game_title = font.render("CONNECT4", False, "Red")
        game_title_rect = game_title.get_rect(center=(width / 2, 100))
        screen.blit(game_title, game_title_rect)
        game_author = font2.render("Patrik Halfar", False, "Red")
        game_author_rect = game_author.get_rect(center=(width / 2, 150))
        screen.blit(game_author, game_author_rect)
        game_difficulty = font2.render("SELECT GAME DIFFICULTY", False, "Black")
        game_difficulty_rect = game_difficulty.get_rect(center=(width / 2, 200))
        screen.blit(game_difficulty, game_difficulty_rect)

        easy_button_rect = pygame.Rect(width / 2 - 100, 250, 200, 50)
        pygame.draw.rect(screen, "Green", easy_button_rect)
        easy_text = font2.render("Easy", False, "White")
        easy_text_rect = easy_text.get_rect(center=easy_button_rect.center)
        screen.blit(easy_text, easy_text_rect)

        medium_button_rect = pygame.Rect(width / 2 - 100, 325, 200, 50)
        pygame.draw.rect(screen, "Orange", medium_button_rect)
        medium_text = font2.render("Medium", False, "White")
        medium_text_rect = medium_text.get_rect(center=medium_button_rect.center)
        screen.blit(medium_text, medium_text_rect)

        hard_button_rect = pygame.Rect(width / 2 - 100, 400, 200, 50)
        pygame.draw.rect(screen, "Red", hard_button_rect)
        hard_text = font2.render("Hard", False, "White")
        hard_text_rect = hard_text.get_rect(center=hard_button_rect.center)
        screen.blit(hard_text, hard_text_rect)

        pygame.display.update()

    if game_active:
        screen.fill("Black")
        pygame.time.wait(500)  # Fix for placing dot after selecting difficulty

    while game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board(board)

        if turn == PLAYER:
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, "Black", (0, 0, width, SQUARE_SIZE))
                pos_x = event.pos[0]
                pygame.draw.circle(screen, "Yellow", (pos_x, int(SQUARE_SIZE / 2)), RADIUS)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pygame.draw.rect(screen, "Black", (0, 0, width, SQUARE_SIZE))
                pos_x = event.pos[0]
                col = int(math.floor(pos_x / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER)

                    if winning_move(board, PLAYER):
                        label = font.render("Player wins!", False, "Yellow")
                        label_rect = label.get_rect(center=(width / 2, SQUARE_SIZE / 2))
                        screen.blit(label, label_rect)
                        game_active = False

                    turn = AI

                    print_board(board)
                    draw_board(board)

        elif turn == AI:
            col, minimax_score = minimax(board, depth, True)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI)

                if winning_move(board, AI):
                    pygame.time.wait(1000)
                    label = font.render("AI wins!", False, "Red")
                    label_rect = label.get_rect(center=(width / 2, SQUARE_SIZE / 2))
                    screen.blit(label, label_rect)
                    game_active = False

                print_board(board)
                draw_board(board)

                turn = PLAYER

        if game_active == False:
            pygame.time.wait(5000)  # Wait 5 seconds after the end of the game

        pygame.display.update()