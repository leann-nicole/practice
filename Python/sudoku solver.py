size = 9

def print_board(board):
    for row in board:
        for num in row:
            print(num, end = ' ')
        print()
        
def by_three(n):
    while n < 9:
        yield n
        n += 3
        
def board_valid(board):
    #check subgrids
    for Row in by_three(0):
        for Col in by_three(0):
            freq = [0] * (size + 1)
            for row in range(Row, Row + 3):
                for col in range(Col, Col + 3):
                    if board[row][col] != 0:
                        freq[board[row][col]] += 1
                        if freq[board[row][col]] > 1: return False
                        
    #check rows
    for row in range(size):
        freq = [0] * (size + 1)
        for col in range(size):
            if board[row][col] != 0:
                freq[board[row][col]] += 1
                if freq[board[row][col]] > 1: return False

    #check columns
    for col in range(size):
        freq = [0] * (size + 1)
        for row in range(size):
            if board[row][col] != 0:
                freq[board[row][col]] += 1
                if freq[board[row][col]] > 1: return False
                
    #if all iterations completed
    return True

def sudoku_solve(board, row, col):
    
    if not board_valid(board): return False

    if row == size: return True
    
    if board[row][col] != 0:
        if col != size - 1:
            return sudoku_solve(board, row, col + 1)
        elif col == size - 1:
            return sudoku_solve(board, row + 1, 0)
    else:
        for num in range(size):
            board_copy = board
            board_copy[row][col] = num + 1
            
            if col != size - 1:
                if sudoku_solve(board_copy, row, col + 1):
                    board = board_copy
                    return True
            elif col == size - 1:
                if sudoku_solve(board_copy, row + 1, 0):
                    board = board_copy
                    return True 
        return False
    
def main():
    
    sudoku_board = [[0,0,0,8,0,0,0,0,0],  
                    [4,0,0,0,1,5,0,3,0],
                    [0,2,9,0,4,0,5,1,8],
                    [0,4,0,0,0,0,1,2,0],
                    [0,0,0,6,0,2,0,0,0],
                    [0,3,2,0,0,0,0,9,0],
                    [6,9,3,0,5,0,8,7,0],
                    [0,5,0,4,8,0,0,0,1],
                    [0,0,0,0,0,3,0,0,0]]
    
    print("ORIGINAL BOARD")
    print_board(sudoku_board)
    if sudoku_solve(sudoku_board, 0, 0):
        print("FINAL BOARD")
        
    else: print("BOARD UNSOLVABLE")
    print_board(sudoku_board)
    
main()