import csv
from itertools import *
from overstrand_to_matrix import *
from matrix_to_rrematrix import *

#Makes a list of color lists that are valid for the knot, given the row reduced matrix for the strands. 
def ColourList(matrix,p):
    #get number of rows as a variable and initialize lists for later. 
    number_rows = len(matrix)

    possible_colours = []
    for i in range(p):
        possible_colours.append(i)
    
    colourlists = []
    colours = []
    pivots = []
    free_variables = []


    #Loop through each of the rows
    for i in range(number_rows):
        #set a flag for when a pivot is in the row. 
        pivot_found = False
        
        #Loop through each of the columns within the row
        for j in range( len( matrix[i] ) ):
            #If we haven't found a pivot yet, keep going further right
            if pivot_found == False:
                #If the value of this entry isn't 0, it's the pivot!
                if matrix[i][j] > 0:
                    #Add the location of the entry to our list pivots. 
                    pivot_location = j
                    pivots.append(pivot_location)
                    pivot_found = True
                    
                    
    #Go through each of the variables (rows). 
    #If the variable doesn't have a pivot, it is a free variable. Add to the list of free variables.
    for i in range(number_rows):
        if i not in pivots:
            free_variables.append(i)
    
    # All possible assignments of colours to the free variables
    free = list(product(possible_colours, repeat = len(free_variables)))

    free_colours=[]

    for colours in free:
        colours = list(colours)
        free_colours.append(colours)

    # Get rid of rotations of each colour list
    for colourlist in free_colours:
        colourlist = list(colourlist)
        for i in range(p):
            new_list = []
            for colour in colourlist:
                new_colour=(colour+i+1) %p
                new_list.append(new_colour)

            if new_list != colourlist and new_list in free_colours:
                free_colours.remove(new_list)

    # Get rid of reflections of each colour list
    for colourlist in free_colours:
        colourlist = list(colourlist)
        new_list = []
        for colour in colourlist:
            new_colour = (p-colour) %p
            new_list.append(new_colour)
        if new_list != colourlist and new_list in free_colours:
            free_colours.remove(new_list)

    trivial_colouring = []
    for i in range(len(free_variables)):
        trivial_colouring.append(0)

    free_colours.remove(trivial_colouring)

    for permutation in free_colours:

        colour_dict={}

        colours = []

        for i in range(len(permutation)):
            colour = list(permutation)[i]
            colour_dict[free_variables[i]] = colour

        for i in range(len(pivots)):
                colour = 0
                row = matrix[i]
                for column in range(len(row)):
                    if column not in pivots:
                        colour -= row[column]*colour_dict[column]
                colour = colour%p
                colour_dict[pivots[i]] = colour
     
        for i in range(len(matrix)):
                colours.append(colour_dict[i])

        colourlists.append(colours)


    for colourlist in colourlists:
        for i in range(len(colourlist)):
            if colourlist[i] ==0:
                colourlist[i] = p  
        
    return colourlists

def overstrand_to_colourlist(overstrand, p):
    matrix = create_matrix(overstrand, p)
    rrematrix = ToReducedRowEchelonForm(matrix, p)
    colourlists = ColourList(rrematrix, p)

    return colourlists

print(overstrand_to_colourlist([3,6,8,2,12,9,3,0,10,4,6,9,10,2], 3))
