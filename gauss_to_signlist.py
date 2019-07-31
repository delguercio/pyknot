# -----------------------------
#    Filename: signlist.py
#      Author: Jack Kendrick
# Last Update: 7/31/2019
# -----------------------------

import csv


def reverse_sect(values, start, end):

    """Reverses the section of the values list between the start and end points."""
    
    sect = values[start: end]
    for i in range(len(sect)):
        values.remove(sect[i])
    for i in range(len(sect)):
        values.insert(start, sect[i])

    return values
    

def kauffman(code):

    """Modifies the input Gauss code using Kauffman's algorithm."""

    if type(code) == str:
        code = code.split(", ")
    for i in range(len(code)):
        code[i] = int(code[i])

    for crossing in range(1, len(code)//2+1):
        for i in range(len(code)):
            if abs(code[i]) == crossing:
                pair = FindPair(code, i)
                code = reverse_sect(code, i+1, pair)
                
    return code

def FindPair(values, i):
    """Finds the position of the matching pair of indexed item in the input list."""

    value = int(values[i])

    for index in range(len(values)):
        if abs(values[index]) == abs(value) and index != i:
            pair = index
            break

    return pair

def Rank(code):

    """Determines whether each arc around a modified Gauss code is a maximum (above the code) or a minimum (below the code). Also builds arc dictionary describing the start and end points of each arc in the modified Gauss code. Returns list of maximums, minimums, and the arc dictionary."""

    max_list = [abs(code[0])]
    min_list = []
    found = [abs(code[0])]

    n = len(code)
    arcs = {}

    for i in range(n):
        if code[i] > 0:
            arc = code[i]
            start = i
            end = FindPair(code, i)
            if end < 0:
                end += n
            arcs[arc] = [min(start, end), max(start, end)]

    for arc in found:
        found_inside = []
        if arc in max_list:
            maximum = True
        else:
            maximum = False
        start = arcs[arc][0]
        end = arcs[arc][1]

        for value in code[start:end]:
            value = abs(value)
            if value not in found:
                if arcs[value][0] < start or arcs[value][1]> end:
                    if maximum:
                        min_list.append(value)
                    else:
                        max_list.append(value)

                    found.append(value)
                    found_inside.append(value)

        if len(found_inside) == 0 and found[-1] == arc and len(found)<n//2:
            declared = True
            while not declared:
                for value in code[start:end]:
                    value = abs(value)
                    if value not in found:
                        max_list.append(value)
                        declared = True

    return [max_list, min_list, arcs]
        
def CreatePath(gauss, arcs):

    """Builds a path through the modified Gauss code using the original Gauss code and arc dictionary."""

    path = []
    for code in gauss:
        path.append(arcs[abs(code)])

    for i in range(len(path)):
        if i == len(path) -1:
            break
        if abs((path[i+1])[0] - (path[i])[1]) != 1:
            path[i+1] = path[i+1][::-1]
            if abs((path[i+1])[0] - (path[i])[1]) != 1:
                path[i] = path[i][::-1]
                if abs((path[i+1])[0] - (path[i])[1]) != 1:
                    path[i+1]=path[i+1][::-1]
        
    if path[-1][1] != len(gauss)-1:
        path[-1] = path[-1][::-1]

    for i in range(len(path)-2,0,-1):
        if abs(path[i][1]-path[i+1][0]) != 1:
            path[i] = path[i][::-1]
                
    return path
    
def BuildCrossing(gauss, ranks):

    """Creates an ordered pair [a, b] for each crossing using the original Gauss code and the information returned by the Rank function. Returns the crossings dictionary."""

    max_list = ranks[0]
    min_list = ranks[1]
    arcs = ranks[2]
    crossings = {}

    for i in range(1, len(gauss)//2+1):
        crossings[i] = [0,0]

    path = CreatePath(gauss, arcs)

    for i in range(len(gauss)):
        if path[i][1] > path[i][0]:
            direction = 1
        else:
            direction = 2

        if gauss[i] < 0:
            position = 1
        else:
            position = 0

        crossings[abs(gauss[i])][position] = direction

    for i in range(len(path)):
        inside = False
        if i != len(path)-1:
            if min(path[i+1]) < path[i][1] < max(path[i+1]):
                inside = True

            if gauss[i+1] < 0:
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

    positive = [[-1,-2], [1,-1], [2,1], [-2,2]]
    negative = [[-2,-1], [-1,1], [1,2], [2,-2]]
    signs = []
    errors = []
    for crossing in crossings:
        if crossings[crossing] in negative:
            signs.append(-1)
        elif crossings[crossing] in positive:
            signs.append(1)
        else:
            errors.append(crossing)

    return [signs, errors]

def Reorder(signs, gauss):

    """Reorders sign list from being in the order of the Gauss code to being in the order needed for the DLN program"""
    
    new_signs = []
    crossing_map = {}

    strand = 0
    for code in gauss:
        if code < 0:
            crossing_map[strand] = abs(code)
            strand += 1

    for crossing in crossing_map:
        new_signs.append(signs[crossing_map[crossing]-1])

    return new_signs
        
   
def SignList(code):
    fixed_code = code.copy()
    arcs = kauffman(code)
    ranks = Rank(arcs)
    crossings = BuildCrossing(fixed_code, ranks)
    signs = Signs(crossings)[0]
    signs = Reorder(signs, fixed_code)
    return signs

def main():
    code = [-1, 2, -3, 4, -5, 1, -6, 7, -4, 3, -8, 9, -10, 11, -7, 5, -2, 8, -9, 10, -11, 6]
    signs = SignList(code)
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


