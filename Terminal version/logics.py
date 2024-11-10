import random

def initialize():
    #initializes the game by making the starting grid and printing instruction

    mat = []
    for i in range(4): #adding 4 completely empty lists to get a 4x4 grid
        mat.append([0] * 4)

    # printing controls for user
    print("Commands are as follows : ")
    print("'W' or 'w' : Move Up")
    print("'S' or 's' : Move Down")
    print("'A' or 'a' : Move Left")
    print("'D' or 'd' : Move Right")

    add_new_value(mat)
    return mat

def add_new_value(mat):

    row = random.randint(0, 3)
    column = random.randint(0, 3)

    while mat[row][column] != 0:
        row = random.randint(0, 3)
        column = random.randint(0, 3)

    #todo: once the highest value reaches a certain point, start with 4 and 8 as well
    mat[row][column] = 2

def check_game_state(mat):

    for row in range(4): #checks winning condition
        for col in range(4):
            if (mat[row][col] == 2048):
                return "Win"

    #todo see if you can optimise this

    for row in range(3): #check each value and it's right and bottom value, does not check last row or col because of out of range
        for col in range(3):
            if (mat[row][col] == mat[row][col + 1]) or (mat[row][col] == mat[row + 1][col]):
                return "Continue"

    for row in range(3): #check values of last column
        if (mat[row][3] == mat[row + 1][3]):
            return "Continue"

    for col in range(3): #check values of last row
        if (mat[3][col] == mat[3][col + 1]):
            return "Continue"

    #if the above conditions failed, game is lost
    return "lost"

def compress(mat):
    new_mat = []
    changed = False #to see if this function changed any values or not

    for _ in range(4):
        new_mat.append([0] * 4)

    for row in range(4):
        pos = 0 #to get the value to leftmost empty cell

        for col in range(4):
            if mat[row][col] != 0: #if the cell is not empty, we try to change it
                new_mat[row][pos] = mat[row][col] #set the filled cell's value to leftmost empty cell in new matrix

                if(col != pos): #if the value was already at leftmost cell, no change happened
                    changed = True #if change actually happened aka value was actually shifted, make it true
                pos += 1 #go to right cell in same row

    return new_mat, changed #todo why are we returning changed

def merge(mat):

    changed = False

    for row in range(4): #to check all rows
        for col in range(3): #to check current rows' column, and it's next column's value
            if (mat[row][col] != 0) and (mat[row][col] == mat[row][col + 1]):
                mat[row][col] = (mat[row][col]) * 2
                mat[row][col + 1] = 0
                changed = True #if change actually happened aka values were merged, make it true

    return mat, changed

def reverse(mat):
    new_mat = []

    for row in range(4):
        new_mat.append([]) #for each row, append empty list to input values
        for col in range(4):
            new_mat[row].append(mat[row][3-col]) #this puts 4th value(3rd index) to first value(0 index)

    return new_mat

def transpose(mat):
    new_mat = []

    for row in range(4):
        new_mat.append([]) #for each row append empty list to input values
        for col in range(4):
            new_mat[row].append(mat[col][row])

    return  new_mat

#main moving function
#compress acts like moving the matrix to left, merge then merges the values if same values blocks are added together and then we compress it again
#using this and reverse(for right) or transposing(for up and down) we changed the values, compress and merge them, and then change them again(reverse or transpose) to get desired result
#do a try run of move_right() and move_up() to understand the logic easily

def move_left(mat):
    new_mat, changedG = compress(mat) #assign compressed matrix to new_mat

    new_mat, changedM = merge(new_mat) #merge new_mat and assign it to itself

    changed = changedM or changedG #if either value is true, it means matrix was changed

    new_mat, changedF = compress(new_mat) #compress the merged new_mat

    return new_mat, changedF #returns the compressed and merged new matrix and whether it was changed or not

def move_right(mat):
    reverse_mat = reverse(mat) #reverse the matrix

    new_mat, changedF = move_left(reverse_mat) #compress the reversed matrix

    final_mat = reverse(new_mat) #now, reverse the compressed matrix to make it seem like values shifted to right

    return final_mat, changedF

def move_up(mat):
    transpose_mat = transpose(mat) #transpose the given matrix

    new_mat,changedF = move_left(transpose_mat) #merge and compress the transposed matrix

    final_mat = transpose(new_mat) #transpose the compressed matrix to make it seem like values moved up

    return final_mat, changedF

def move_down(mat):
    transpose_mat = transpose(mat) #transpose the given matrix

    new_mat, changedF = move_right(transpose_mat) #merge and compress the transposed matrix

    final_mat = transpose(new_mat) #transpose the compressed matrix to make it seem like values moved down

    return final_mat, changedF