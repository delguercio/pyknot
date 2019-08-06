# -----------------------------
#    Filename: gauss_to_signlist.py
#      Author: Jack Kendrick
# Last Update: 8/5/2019
# -----------------------------

import csv

def reverse_sect(values, start, end):

    """Reverses the section of the values list between the start and end points."""
   
    sect = values[start: end]                   # Create a copy of the section that needs to be reversed
    for i in range(len(sect)):                  # Removes values from the list
        values.remove(sect[i])                  
    for i in range(len(sect)):
        values.insert(start, sect[i])           # Places each value in the section at the start point, meaning the specified section is reversed

    return values
    

def kauffman(code):

    """Modifies the input Gauss code using Kauffman's algorithm."""
    
    # To reconstruct a knot from its Gauss code, we follow the process described by Kauffman (1999).

    if type(code) == str:                                   # If the Gauss code isn't already a list, this turns it into one
        code = code.split(", ")
    for i in range(len(code)):
        code[i] = int(code[i])

    for crossing in range(1, len(code)//2+1):               # Reverses the section of code between two elements in the Gauss code
        for i in range(len(code)):                          # that have the same value, as outlined by Kauffman
            if abs(code[i]) == crossing:                    
                pair = FindPair(code, i)
                code = reverse_sect(code, i+1, pair)
                
    return code                                             # This code will be referred to as the modified Gauss code.

def FindPair(values, i):
    """
        input: Gauss code (values), and an index i
        output: the matching index where values[i] == values[index] but i != index
        
        Finds the position of the matching pair of indexed item in the input list.
    """

    value = int(values[i])

    for index in range(len(values)):
        if abs(values[index]) == abs(value) and index != i:
            pair = index
            break

    return pair

def Rank(code):

    """ Determines whether each arc around a modified Gauss code is a maximum (above the code)
        or a minimum (below the code). Also builds arc dictionary describing the start and end 
        points of each arc in the modified Gauss code. Returns list of maximums, minimums, and 
        the arc dictionary.
        Calls on FindPair(values, i), kauffman(code), and reverse_sect(values, start, end).
        
        input: g
        
        output: one list the number of the arc that is above, one list the number of the arc that
                are below, and the arc dictionary
    """

    # When reconstructing a knot from the Gauss code by hand, non-intersecting arcs are drawn 
    # between entries in the modified Gauss code with the same absolute value. Some of these arcs 
    # are drawn above the modified Gauss code (maximums) and some are drawn below the
    # code (minimums), and whether a particular arc is a maximum or a minimum is important when 
    # determining the sign of the crossing onsaid arc.
    
    max_list = [abs(code[0])]                                       # The first entry in the code is made a maximum arbitrarily.
    min_list = []                                                   # Whether the first entry is made a maximum or a minimum
    found = [abs(code[0])]                                          # determines whether the sign list is found for the knot or its
                                                                    # mirror image. As this choice is currently arbitrary, the sign list
    n = len(code)                                                   # could be for either the knot or its mirror image, meaning the
    arcs = {}                                                       # dihedral linking number is currently found up to absolute value.   

    for i in range(n):
        if code[i] > 0:                                             # Creates a dictionary of the arc number with its corresponding start
            arc = code[i]                                           # and end point for use later.
            start = i
            end = FindPair(code, i)
            if end < 0:
                end += n
            arcs[arc] = [min(start, end), max(start, end)]          # Start point is smaller by convention.

    for arc in found:
        found_inside = []
        if arc in max_list:
            maximum = True
        else:
            maximum = False
        start = arcs[arc][0]
        end = arcs[arc][1]

        for value in code[start:end]:                                   # Goes through the code inside the current arc.
            value = abs(value)
            if value not in found:
                if arcs[value][0] < start or arcs[value][1]> end:       # If one end of the inner arc is outside the current arcs,
                    if maximum:                                         # it is a minimum if the current arc is a maximum and a
                        min_list.append(value)                          # maximum if the current arc is a minimum.
                    else:
                        max_list.append(value)

                    found.append(value)
                    found_inside.append(value)

        if len(found_inside) == 0 and found[-1] == arc and len(found)<n//2:  # If not all of the arcs have been classified as maximums
            declared = True                                                  # or minimums but the program has already run through all of
            while not declared:                                              # the found arcs, the next unclassified arc is made a maximum
                for value in code[start:end]:                                # arbitrarily.
                    value = abs(value)
                    if value not in found:
                        max_list.append(value)
                        declared = True

    return [max_list, min_list, arcs]
        
def CreatePath(gauss, arcs):

    """  
        Builds a path through the modified Gauss code using the original Gauss code and arc dictionary.
        output: indicies you must go to in order on the Kauffman(gauss_code)
    """

    # In order to reconstruct the knot from the modified Gauss code, a closed loop needs to be made through the modified Gauss code,
    # with the only crossings in the knot being on the previously found arcs (i.e. there is a crossing on the arc between 1 and -1, 2
    # and -2, etc.) In order to ensure that the only crossings are those in the original knot, this function uses the arc dictionary
    # created in the Rank function to build a path through the modified Gauss code.
    
    path = []
    for code in gauss:                                                  # For each entry in the Gauss code, the start and end points
        path.append(arcs[abs(code)])                                    # of the relevant arc are added to the path. The path is then
                                                                        # a list of pairs.
    for i in range(len(path)):
        if i == len(path) -1:
            break
        if abs((path[i+1])[0] - (path[i])[1]) != 1:                     # If the end point of the arc is not adjacent to the start point
            path[i+1] = path[i+1][::-1]                                 # of the next arc, the end points of the next arc are reversed
            if abs((path[i+1])[0] - (path[i])[1]) != 1:                 # If the start and end points are still not adjacent, the first
                path[i] = path[i][::-1]                                 # arc is reversed.
                if abs((path[i+1])[0] - (path[i])[1]) != 1:             # It is important that the end point of one arc is adjacent to
                    path[i+1]=path[i+1][::-1]                           # the start point of the next arc as this ensures that there are  
                                                                        # no extra crossings being added to the knot.
                            
    if path[-1][1] != len(gauss)-1:                                     # This ensures that the last arc's end point is at the end of the
        path[-1] = path[-1][::-1]                                       # list.

    for i in range(len(path)-2,0,-1):                                   # Go through the list backwards and ensure that all of the start/
        if abs(path[i][1]-path[i+1][0]) != 1:                           # end points of the arcs are next to each other. This just double
            path[i] = path[i][::-1]                                     # checks that the program works how it should.
                
    return path
    
def BuildCrossing(gauss, ranks):

    """ 
        Creates an ordered pair [a, b] for each crossing using the original Gauss code and the information 
        returned by the Rank function. Returns the crossings dictionary.
    """
    
    # This function creates a dictionary that encodes all the necessary information to determine the sign of each crossing. Each entry
    # in dictionary is formatted as [overstrand, understrand] where each value in the pair is ±1 or ±2. Each entry in the crossing can
    # be thought of like a vector with ±1 pointing to the right and ±2 pointing to the left. Positive values point downwards in each 
    # direction and negative values point upwards.
    
    max_list = ranks[0]
    min_list = ranks[1]
    arcs = ranks[2]
    crossings = {}

    for i in range(1, len(gauss)//2+1):             
        crossings[i] = [0,0]

    path = CreatePath(gauss, arcs)

    for i in range(len(gauss)):
        if path[i][1] > path[i][0]:         # By determining whether the next entry in the path is bigger or smaller than than the current
            direction = 1                   # entry you can determine whether you travel left or right along the current arc. Direction 1
        else:                               # is to the right and direction 2 is to the left.
            direction = 2

        if gauss[i] < 0:                    # If the entry in the Gauss code is negative, the current strand is the understrand at the crossing
            position = 1                    # so the second entry in the crossing is currently being altered. Else, the strand is the overstrand
        else:                               # and the first entry in the crossing is being changed.
            position = 0

        crossings[abs(gauss[i])][position] = direction

    for i in range(len(path)):              # After the direction of each strand at the crossing is found, it can be determined whether
        inside = False                      # the direction should be positive or negative.
        if i != len(path)-1:
            if min(path[i+1]) < path[i][1] < max(path[i+1]):    # The end of an arc is either inside or outside of the next arc. This,
                inside = True                                   # along with whether the next arc is a minimum or a maximum, determines
                                                                # whether the direction of the next strand is positive or negative.
            if gauss[i+1] < 0:                                  # This is easier to see when doing an example by hand.
                position = 1
            else:
                position = 0

            if abs(gauss[i+1]) in max_list:
                if inside:
                    crossings[abs(gauss[i+1])][position] = -crossings[abs(gauss[i+1])][position]
            if abs(gauss[i+1]) in min_list:
                if not inside:
                    crossings[abs(gauss[i+1])][position] = -crossings[abs(gauss[i+1])][position]                                                

    return crossings

def Signs(crossings):

    """Determines the sign of each crossing in the input dictionary by comparing to the known positive and negative crossings. Returns the sign list."""

    positive = [[-1,-2], [1,-1], [2,1], [-2,2]]         # These are the only possible positive and negative crossings and thus each
    negative = [[-2,-1], [-1,1], [1,2], [2,-2]]         # crossing in the crossing dictionary must be of one of these forms.
    signs = []
    errors = []
    for crossing in crossings:
        if crossings[crossing] in negative:
            signs.append(-1)
        elif crossings[crossing] in positive:
            signs.append(1)
        else:
            errors.append(crossing)                     # The error list is mostly used for trouble shooting and should have zero entries.

    return [signs, errors]

def Reorder(signs, gauss):

    """Reorders sign list from being in the order of the Gauss code to being in the order needed for the DLN program"""
    
    # The Gauss code crossing labels can be pretty arbitrary, whereas for the DLN program the crossings must be in order such that the
    # zeroth crossing is at the end of the zeroth strand, etc. This function reorders the sign list so that the signs are in order
    # for the DLN program and not according to the labels used in the Gauss code.
    
    new_signs = []
    crossing_map = {}

    strand = 0
    for code in gauss:
        if code < 0:                                # If a crossing in the Gauss code is negative, the current strand i is the understrand
            crossing_map[strand] = abs(code)        # at the crossing, thus it is the ith crossing.
            strand += 1

    for crossing in crossing_map:
        new_signs.append(signs[crossing_map[crossing]-1])   # signs[crossing_map[crossing]-1] because Gauss code labels start from 1 and
                                                            # not 0.
    return new_signs
        
   
def SignList(code):                                         # This pieces the previous functions together to return the sign list.
    fixed_code = code.copy()
    arcs = kauffman(code)
    ranks = Rank(arcs)
    crossings = BuildCrossing(fixed_code, ranks)
    signs = Signs(crossings)[0]
    signs = Reorder(signs, fixed_code)
    return signs

def main():
    code = [-1, 2, -3, 4, -5, 1, -6, 7, -4, 3, -8, 9, -10, 11, -7, 5, -2, 8, -9, 10, -11, 6] # Change this to any Gauss code to find the
    signs = SignList(code)                                                                   # sign list for a specific knot.
    print(signs)

#if __name__ == "__main__":
#    main()


fields = [ 'Name', 'Gauss Notation']

newfields = [ 'Name', 'Sign List']

filename = "name_gauss_3colorable.csv"

line_count = 0

rawfile = open(filename, 'r')

reader = csv.reader(rawfile)

new_LoL = []
 
for row in reader:
    if line_count == 0:
        new_LoL.append(newfields)
        line_count = line_count + 1
    else:
        strings = list(row[1][1:-1].split(","))
        list_of_ints = [ int(number) for number in strings ]
        signs = SignList( list_of_ints )
        if len(signs)%2 == 0:
            new_LoL.append([row[0],signs])
            line_count = line_count + 1
        else:
            pos_crossing = signs + [1]
            new_LoL.append([row[0],pos_crossing])
            line_count = line_count + 1            

rawfile.close()



newfilename = "name_sign_3colorable.csv"

newrawfile = open(newfilename, 'w')

writer = csv.writer(newrawfile)

for row in new_LoL:
    writer.writerow(row)

newrawfile.close()


# -----------------------------
# REFERENCES:
# LH Kauffman, Virtual Knot Theory, European Journal of Combinatorics, 20 (1999), 663-691
# -----------------------------
