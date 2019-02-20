import numpy as np 


def solved(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0:
                return False
    return True

def unable_to_solve(possibilities):
    for k in range(9):
        for j in range(9):
            sum = 0
            for i in range(9):
                sum += possibilities[i][j][k]
                if sum==0:
                    return True
    return False

def unique(sudoku, number, x, y):
    if sudoku[:][y].any() == number:
        return False
    if sudoku[x][:].any() == number:
        return False
    aux_x = x - x%3
    aux_y = y - y%3
    if sudoku[aux_x:aux_x+3][aux_y:aux_y+3].any() == number:
        return False
    
    return True

def make_possibilities(sudoku):
    possibilities = np.zeros(81*9).reshape(9,9,9)
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if unique(sudoku,i+1,j,k):
                    possibilities[i][j][k]=1

def delete(possibilities,num,x,y):
    for i in range(9):
        possibilities[num][x][i] = 0
        possibilities[num][i][y] = 0
        possibilities[i][x][y] = 0
    
    aux_x = x - (x%3)
    aux_y = y - (y%3)

    for i in range(aux_x,aux_x + 3):
        for j in range(aux_y,aux_y + 3):
            possibilities[num][i][j]=0
    
    return possibilities

def solver(sudoku,possibilities):

    if solved(sudoku):
        return sudoku
    
    if unable_to_solve(possibilities):
        return 0
    
    for i in range(9):
        for j in range(9):
            if(sudoku[i][j]==0):
                copy = sudoku.copy()
                for k in range(9):
                    if possibilities[k][i][j]==1:
                        copy[i][j] = k+1
                        copy_p = delete(possibilities.copy(),k,i,j)
                        result = solver(copy,copy_p)
                        if result != 0:
                            return result
