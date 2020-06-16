from colour_overstrand_to_index2lists import *


def rrematrix_to_dict(matrix):
    n = len(matrix)
    num_crossings = n//2
    coeff_dict = {}

    for i in range(n):
        coeff_dict[((i//num_crossings)+1, i % num_crossings)] = 0

    pivots = []

    # Loop through each of the rows
    for i in range(n):
        # set a flag for when a pivot is in the row.
        pivot_found = False

        # Loop through each of the columns within the row
        for j in range(len(matrix[i])):
            # If we haven't found a pivot yet, keep going further right
            if not pivot_found:
                # If the value of this entry isn't 0, it's the pivot!
                if matrix[i][j] != 0:
                    # Add the location of the entry to our list pivots.
                    pivot_location = j
                    pivots.append(pivot_location)
                    pivot_found = True

    for i in range(len(pivots)):
        row = matrix[i]
        for column in range(len(row)):
            if column in pivots:
                coeff_dict[((column//num_crossings)+1, column % num_crossings)] = row[-1]

    return coeff_dict


def matrix_to_dln(colourlist, overstrandlist, signlist, p):

    universes_list = universe_lists(colourlist, overstrandlist, p)
    wheres = where_lists(colourlist, overstrandlist, p)
    vert_order = vertical_order(colourlist, overstrandlist, p)
    coeff_dict = {(1, 1): 1,
                  (1, 3): -1,
                  (1, 0): 0,
                  (1, 2): 0,
                  (2, 0): 0,
                  (2, 1): 0,
                  (2, 2): 0,
                  (2, 3): 0}
    dlns = []

    for i in range(len(wheres)):  # Go through each of the where lists

        dln = 0
        where_list = wheres[i]

        for j in range(len(universes_list)):  # Go through each of the crossings
            where = where_list[j]
            universes = universes_list[j]

            for k in range(len(universes)):
                if where in universes[k]:
                    level = index(universes[k], where)
                    break

            # index 1 is only the zeroth level at inhomogeneous crossings
            if level == 0 and colourlist[j] != colourlist[overstrandlist[j]]:
                coeff = 1
            else:
                knot = vert_order[j][level-1]
                coeff = coeff_dict[(knot, overstrandlist[j])]

                vertical_where = wheres[knot-1][overstrandlist[j]]
                if where == vertical_where or where == reflect(vertical_where, colourlist[j], p):
                    e = 1
                else:
                    e = -1

                coeff = coeff*e*signlist[j]

            dln += coeff*signlist[j]

        dlns.append(dln)

    return dlns


print(matrix_to_dln([3, 5, 4, 2], [2, 3, 0, 1], [-1, 1, -1, 1], 5))
