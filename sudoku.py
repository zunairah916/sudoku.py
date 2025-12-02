import pygame
import random
import copy

WINDOW_WIDTH, WINDOW_HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

pygame.init()
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku Generator & Solver")
FONT = pygame.font.SysFont("comicsans", 40)
SMALL_FONT = pygame.font.SysFont("comicsans", 20)

def print_board(board):
    for row in board:
        print(row)
    print()

def is_valid(board, row, col, num):
    for i in range(GRID_SIZE):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def find_empty_mrv(board):
    min_options = 10
    target_cell = None
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                options = sum(is_valid(board, i, j, n) for n in range(1, 10))
                if options < min_options:
                    min_options = options
                    target_cell = (i, j)
    return target_cell

def solve(board):
    empty = find_empty_mrv(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0
    return False

def count_solutions(board):
    empty = find_empty_mrv(board)
    if not empty:
        return 1
    row, col = empty
    total = 0
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            total += count_solutions(board)
            if total > 1:
                board[row][col] = 0
                return total
            board[row][col] = 0
    return total

def fill_board(board):
    nums = list(range(1, 10))
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if fill_board(board):
                            return True
                        board[i][j] = 0
                return False
    return True

def generate_puzzle():
    board = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    fill_board(board)
    puzzle = copy.deepcopy(board)
    cells = [(i,j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)]
    random.shuffle(cells)
    for row, col in cells:
        removed = puzzle[row][col]
        puzzle[row][col] = 0
        temp_board = copy.deepcopy(puzzle)
        if count_solutions(temp_board) != 1:
            puzzle[row][col] = removed
    return puzzle

def draw_board(board, selected=None):
    WIN.fill(WHITE)
    # Draw cells
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x, y = j * CELL_SIZE, i * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            if selected == (i, j):
                pygame.draw.rect(WIN, LIGHT_BLUE, rect)
            pygame.draw.rect(WIN, BLACK, rect, 1)
            if board[i][j] != 0:
                text = FONT.render(str(board[i][j]), True, BLACK)
                WIN.blit(text, (x + CELL_SIZE//2 - text.get_width()//2, y + CELL_SIZE//2 - text.get_height()//2))
    for i in range(0, GRID_SIZE+1, 3):
        pygame.draw.line(WIN, BLACK, (0, i*CELL_SIZE), (WINDOW_WIDTH, i*CELL_SIZE), 3)
        pygame.draw.line(WIN, BLACK, (i*CELL_SIZE, 0), (i*CELL_SIZE, WINDOW_WIDTH), 3)

def animate_solve(board):
    empty_cells = [(i,j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j]==0]
    def _solve_animate():
        empty = find_empty_mrv(board)
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if is_valid(board, row, col, num):
                board[row][col] = num
                draw_board(board, selected=(row, col))
                pygame.display.update()
                pygame.time.delay(30)
                if _solve_animate():
                    return True
                board[row][col] = 0
                draw_board(board, selected=(row, col))
                pygame.display.update()
                pygame.time.delay(30)
        return False
    _solve_animate()

def main():
    puzzle = generate_puzzle()
    board = copy.deepcopy(puzzle)
    selected = None
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        draw_board(board, selected)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    animate_solve(board)
                if event.key == pygame.K_r: 
                    board = copy.deepcopy(puzzle)
    pygame.quit()

if __name__ == "__main__":
    main()
