#Get a sudoku puzzle as input
og_horizontal = []
ii = 0
# get puzzle as a list of strings. Make sure those strings are 9 characters long
# and only contain "." and numbers 1 through 9
ok = ".123456789"
while ii < 9:
    print("type line", ii+1)
    puzzle = input("sudoku line: ")
    if len(puzzle) == 9 and all(c in ok for c in puzzle):
        og_horizontal.append(puzzle)
        ii += 1
    else:
        print("invalid line")
        continue


#turn list of strings into a list of lists
#with each '.' being a 0 and each element being an integer
#also here: I make a list of tuples containing the coordinates of empty_spaces.
#this allows the code to easily differentiate squares that need to be filled
#from squares that need to be left alone.
horizontal = []
row_count = -1
empty_spaces = []
count = 0
for string in og_horizontal:
    row_count +=1
    col_count = -1
    line = []
    for c in string:
        col_count += 1
        if c == ".":
            count += 1
            c = 0
            empty_spaces.append((row_count, col_count))
        line.append(int(c))
    horizontal.append(line)

#Create a list of lists representing the vertical lines
vertical = []
jj = 0
while jj < 9:
    vert_line = []
    for line in horizontal:
        if line[jj] != 0:
            vert_line.append(line[jj])
    vertical.append(vert_line)
    jj +=1


#Create a list of lists representing the boxes
box = []
def box_set(row_min, row_max, col_min, col_max):
    box_line = []
    for line in horizontal:
        for num in line:
            if num != 0:
                if (horizontal.index(line) >= row_min and
                horizontal.index(line) < row_max and
                line.index(num) >= col_min and
                line.index(num) < col_max):
                    box_line.append(num)
    box.append(box_line)
box_set(0, 3, 0, 3)
box_set(0, 3, 3, 6)
box_set(0, 3, 6, 9)
box_set(3, 6, 0, 3)
box_set(3, 6, 3, 6)
box_set(3, 6, 6, 9)
box_set(6, 9, 0, 3)
box_set(6, 9, 3, 6)
box_set(6, 9, 6, 9)

#This function returns a number representing a row in box_set.
#This in turn represents a box in the sudoku puzzle.
#So, for a given blank space (determined by its row and column), this function
#tells the program which box that blank space is in.
row_counts = 0
col_counts = 0
def box_row():
    if row_counts >= 0 and row_counts < 3 and col_counts >= 0 and col_counts < 3:
        return 0
    if row_counts >= 0 and row_counts < 3 and col_counts >= 3 and col_counts < 6:
        return 1
    if row_counts >= 0 and row_counts < 3 and col_counts >= 6 and col_counts < 9:
        return 2
    if row_counts >= 3 and row_counts < 6 and col_counts >= 0 and col_counts < 3:
        return 3
    if row_counts >= 3 and row_counts < 6 and col_counts >= 3 and col_counts < 6:
        return 4
    if row_counts >= 3 and row_counts < 6 and col_counts >= 6 and col_counts < 9:
        return 5
    if row_counts >= 6 and row_counts < 9 and col_counts >= 0 and col_counts < 3:
        return 6
    if row_counts >= 6 and row_counts < 9 and col_counts >= 3 and col_counts < 6:
        return 7
    if row_counts >= 6 and row_counts < 9 and col_counts >= 6 and col_counts < 9:
        return 8


#This function sends a targeted blank space (determined by solver) down a path
#for one of three possibilities: either (1) a number seems to work in that square,
#or (2) it doesn't work but there are more numbers to try, or (3) the number does
#not work and there are no more numbers to try.
def increment():
    #as long as the number hasn't rolled over to 10, keep trying
    #higher numbers
    global x
    global row_counts
    global col_counts
    #if the number in question (which is x+1) is in the range of 1 to 9, then
    #a test can be done to see if that number fits in the empty square
    if x < 9:
        #If there are no repeats of a number being tested horizontally, vertically,
        #or in the box, then the number (x +1) seems to work in this square.
        if (horizontal[row_counts].count(x + 1) == 0 and
        vertical[col_counts].count(x + 1) == 0 and
        box[box_row()].count(x + 1) == 0) :
            #Put the tested value in the square
            x += 1
            horizontal[row_counts][col_counts] = x
            #Put the tested value on record in this vertical column
            vertical[col_counts].append(x)
            #Put the tested value on record in this box
            box[box_row()].append(x)
            #Go back to the solver function.
            return

        #if there are any repeats of the tested number horizontally, vertially,
        #or in the box
        else:
            #Still increment, so that a number 1 higher is tried next time around
            x += 1
            horizontal[row_counts][col_counts] = x
            #go back to the beginning of the function
            increment()
    #if x raises to 9, that means every possible number has been tried, and none worked
    elif x == 9:
        #if this happens on the very first blank square, the puzzle is invalid
        # and the program ends
        global square_count
        if square_count == 0:
            print("invalid puzzle")
            quit()
        #On any other square, set that square equal to zero, ready to be returned to
        #later. Meanwhile, go back to the previous empty square, clear that value
        #from the vertical and box records, and go back to the top of the function.
        #Effectively, this will have that previous square start trying the numbers
        #higher than were found to work before.
        else:
            horizontal[row_counts][col_counts] = 0
            square_count -=1
            back_space = empty_spaces[square_count]
            row_counts = back_space[0]
            col_counts = back_space[1]
            x = horizontal[row_counts][col_counts]
            vertical[col_counts].remove(x)
            box[box_row()].remove(x)
            increment()

#The function that solves the sudoku puzzle. This chunk, before running the
#increment function defined above, iterates through every spot in the puzzle
#and checks to see whether that spot is fixed or not. If not, it runs the
#above function.
def solver():
    global row_counts
    row_counts = -1
    while row_counts < 9:
        row_counts += 1
        global col_counts
        col_counts = -1
        while col_counts < 9:
            col_counts +=1
            global coordinates
            y = (row_counts, col_counts)
            coordinates = y
            global square_count
            square_count = -1
            for i in empty_spaces:
                square_count += 1
                if coordinates == i:
                    global x
                    x = horizontal[row_counts][col_counts]
                    increment()

#Run the sudoku solver
solver()

#Printing the answer to the puzzle
for line in horizontal:
    print(line)
