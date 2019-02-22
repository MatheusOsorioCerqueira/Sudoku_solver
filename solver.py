import numpy as np 
#0 0 6 0 3 0 0 0 0 0 0 5 0 0 0 0 0 3 0 0 0 0 4 9 2 0 7 7 0 0 0 0 0 0 3 0 0 9 0 2 0 0 7 0 0 0 0 0 0 0 3 0 9 0 0 0 4 0 0 0 0 0 0 0 6 0 1 0 0 4 0 0 0 0 0 0 0 0 5 6 1
#0 0 0 0 0 5 4 0 9 4 5 1 0 0 2 3 0 0 9 8 2 0 0 0 5 6 1 6 0 7 0 0 0 9 8 0 0 0 3 4 6 0 0 0 0 5 0 0 2 8 7 0 1 0 0 4 0 0 7 0 0 9 6 3 0 0 0 0 0 7 0 0 0 0 5 9 4 6 8 0 2


#status: tested
def make_sudoku():#going to be here shortly, just used to create a sudoku game that i can test for functionality
    sudoku = list(input("type sudoku: "))#recieves input
    sudoku = list(filter(lambda x: x!=' ',sudoku))#filters for spaces between numbers
    return np.array(sudoku).reshape(9,9).astype(np.int)#transforms into an np.array, also transforms the type to be an integer

#status: tested
def is_possible(sudoku,n,x,y):#checks if a given number is already on the square, line or column of the sudoku
    for i in range(9):
        if sudoku[x][i]==n or sudoku[i][y]==n:#checks line and column
            return False
    
    aux_x = x - (x%3)
    aux_y = y - (y%3)

    for i in range(aux_x,(aux_x+3)):#checks square
        for j in range(aux_y,(aux_y+3)):
            if sudoku[i][j]==n:
                return False
    
    return True

def test_possibilities(sudoku,n,x,y):
    for i in range(9):
        if sudoku[x][i]==1 or sudoku[i][y]==1:#checks line and column
            return False    
    aux_x = x - (x%3)
    aux_y = y - (y%3)

    for i in range(aux_x,(aux_x+3)):#checks square
        for j in range(aux_y,(aux_y+3)):
            if sudoku[i][j]==1:
                return False
        
    return True

#status: tested
def make_helper(sudoku):#returns a 9x9x9 matrix cube with all the possibilities for each single square in the current sudoku
    helper = np.zeros(81*9).reshape(9,9,9).astype(np.int)#creates a 9x9x9 matrix cube with zeros
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0:
                for k in range(9):
                    if is_possible(sudoku,k+1,i,j):
                        helper[k][i][j]=1
    
    return helper

def delete(helper,number,x,y):
    for i in range(9):
        helper[number][i][y]=0
        helper[number][x][i]=0


    aux_x = x - (x%3)
    aux_y = y - (y%3)
    for i in range(aux_x,(aux_x+3)):
        for j in range(aux_y,(aux_y+3)):
            helper[number][i][j]=0
    return helper

def  unable_to_solve(sudoku, helper):
    for i in range(9):
        for j in range(9):
            sum = 0
            if sudoku[i][j]==0:
                for k in range(9):
                    if helper[k][i][j] != 0: sum+=1
                if sum==0:
                    return True
    return False

def only_possibility(sudoku,helper):
    value = False
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0:
                sum = 0
                place = 0
                for k in range(9):
                    if helper[k][i][j]==1: 
                        sum+=1
                        place = k
                if sum ==1:
                    value = True
                    sudoku[i][j]= place+1
                    delete(helper,place,i,j)
                    sum==0
                for k in range(9):
                    if helper[k][i][j]==1:
                        helper[k][i][j]=0
                        if test_possibilities(helper[k],k,i,j):
                            sudoku[i][j]=k+1
                            helper = delete(helper,k,i,j) 
                        else:
                            helper[k][i][j]=1

    if value:
        return only_possibility(sudoku,helper)
    return sudoku,helper


def solved(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0:
                return False
    return True

def solve(sudoku, helper,n):
    result = 0
    aux_s = 0
    aux_h = 0
    if solved(sudoku):
        return sudoku
    if unable_to_solve(sudoku,helper):
        return 0
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                for k in range(9):
                    if helper[k][i][j]==1:
                        aux_s = sudoku.copy()
                        aux_h = helper.copy()
                        aux_s[i][j] = k+1
                        aux_h = delete(aux_h,k,i,j)
                        aux_s,aux_h = only_possibility(aux_s,aux_h)
                        print(n)
                        result = solve(aux_s,aux_h,n+1)
                        if type(result)!= int:
                            return result
    return 0



sudoku = make_sudoku()
helper = make_helper(sudoku)
print(solve(sudoku,helper,0))
        
    