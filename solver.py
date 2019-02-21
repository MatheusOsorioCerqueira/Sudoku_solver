import numpy as np 
#0 0 6 0 3 0 0 0 0 0 0 5 0 0 0 0 0 3 0 0 0 0 4 9 2 0 7 7 0 0 0 0 0 0 3 0 0 9 0 2 0 0 7 0 0 0 0 0 0 0 3 0 9 0 0 0 4 0 0 0 0 0 0 0 6 0 1 0 0 4 0 0 0 0 0 0 0 0 5 6 1



def make_sudoku():
    sudoku = list(input("type sudoku: "))
    sudoku = list(filter(lambda n: n!=' ',sudoku))
    return np.array(sudoku).reshape(9,9).astype(np.int)


def solved(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0:
                return False
    return True


def unable_to_solve(sudoku,possibilities):
    for k in range(9):
        for j in range(9):
            sum = 0
            if sudoku[j][k]==0:
                for i in range(9):
                    sum += possibilities[i][j][k]
                if sum==0:
                    return True
    return False


def unique(sudoku, number, x, y):
    if np.any(sudoku[:][y]==number):
        return False
    if np.any(sudoku[x][:] == number):
        return False
    aux_x = x - x%3
    aux_y = y - y%3
    if np.any(sudoku[aux_x:aux_x+3][aux_y:aux_y+3] == number):
        return False
    
    return True


def make_possibilities(sudoku):
    possibilities = np.zeros(81*9).reshape(9,9,9).astype(np.int)
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if unique(sudoku,i+1,j,k) and sudoku[j][k]==0:
                    possibilities[i][j][k]=1
    return possibilities


def only_possibility(sudoku,possibilities):
    value = False
    for i in range(9):
        for j in range(9):
            sum=0
            for k in range(9):
              sum+= possibilities[k][i][j]
            if sum==1:
                for k in range(9):
                    if possibilities[k][i][j]==1:
                        sudoku[i][j]=k+1
                        possibilities = make_possibilities(sudoku)
                        value = True
                        break
    if value:
        print("safado")
        return only_possibility(sudoku,possibilities)
    return sudoku


def delete(possibilities,num,x,y):
    for i in range(9):
        possibilities[num][x][i] = 0
        possibilities[num][i][y] = 0
        possibilities[i][x][y] = 0
    
    aux_x = x - (x%3)
    aux_y = y - (y%3)

    for i in range(aux_x,(aux_x + 3)):
        for j in range(aux_y,(aux_y + 3)):
            possibilities[num][i][j]=0
    
    return possibilities


def solver(sudoku,possibilities,n):
    print(n)
    if solved(sudoku):
        return sudoku
    
    if unable_to_solve(sudoku,possibilities):
        return 0
    
    for i in range(9):
        for j in range(9):
            if(sudoku[i][j]==0):
                for k in range(9):
                    #print("({},{}): {}".format(i,j,k))
                    if possibilities[k][i][j]==1:
                        copy = sudoku.copy()
                        copy[i][j]=k+1
                        copy_p = make_possibilities(copy)
                        sudoku = only_possibility(copy,copy_p)
                        result = solver(copy,copy_p,n+1)
                        if type(result) != int:
                            return result
    return 0


sudoku = make_sudoku()
helper = make_possibilities(sudoku)
print(solver(sudoku,helper,0))
