import itertools as iter
import overstrand_to_matrix as o2m
import matrix_to_rrematrix as m2rre
from sympy import Matrix


def rotations_reflections(perms, p):

    for perm in perms:
        for i in range(p):
            new_perm = []
            for value in perm:
                new_value = (value + i + 1) % p
                new_perm.append(new_value)

            if new_perm != perm and new_perm in perms:
                perms.remove(new_perm)

    for perm in perms:
        new_perm = []
        for value in perm:
            new_value = (p - value) % p
            new_perm.append(new_value)
        if new_perm != perm and new_perm in perms:
            perms.remove(new_perm)

    return perms


def ColourList(matrix, p):

    matrix = Matrix(matrix).rref()
    pivots = list(matrix[1])
    matrix = matrix[0]
    # get number of rows as a variable and initialize lists for later.
    number_rows = len(matrix.col(0))
    possible_colours = [i for i in range(p)]

    colourlists = []
    free_variables = []

    for i in range(number_rows):
        if i not in pivots:
            free_variables.append(i)

    # All possible assignments of colours to the free variables
    free_colours = list(iter.product(possible_colours, repeat=len(free_variables)))

    for i in range(len(free_colours)):
        free_colours[i] = list(free_colours[i])

    free_colours = rotations_reflections(free_colours, p)

    trivial_colouring = [0 for i in range(len(free_variables))]
    free_colours.remove(trivial_colouring)

    reorderings = list(iter.permutations(possible_colours))
    for i in range(len(reorderings)):
        reorderings[i] = list(reorderings[i])

    reorderings = rotations_reflections(reorderings, p)

    for permutation in free_colours:
        covered_colourings = []
        for reordering in reorderings:
            colouring = []
            for i in permutation:
                colouring.append(reordering[i])
            covered_colourings.append(colouring)

        test_covered = []
        for i in range(1, len(free_colours)):
            test_permutation = free_colours[i]
            test_covered = []
            for reordering in reorderings:
                colouring = []
                for i in test_permutation:
                    colouring.append(reordering[i])
                test_covered.append(colouring)

        if test_covered == covered_colourings and test_permutation != permutation:
            free_colours.remove(test_permutation)

    for permutation in free_colours:

        colour_dict = {}
        colours = []

        for i in range(len(permutation)):
            colour = list(permutation)[i]
            colour_dict[free_variables[i]] = colour

        for i in range(len(pivots)):
            colour = 0
            row = matrix.row(i)
            for column in range(len(row)):
                if column not in pivots:
                    colour -= row[column] * colour_dict[column]
            colour = colour % p
            colour_dict[pivots[i]] = colour

        for i in range(number_rows):
            colours.append(colour_dict[i])

        colourlists.append(colours)

    for colourlist in colourlists:
        for i in range(len(colourlist)):
            if colourlist[i] == 0:
                colourlist[i] = p

    return colourlists


def overstrand_to_colourlist(overstrand, p):
    matrix = o2m.create_matrix(overstrand, p)
    rrematrix = m2rre.ToReducedRowEchelonForm(matrix, p)
    colourlists = ColourList(rrematrix, p)

    return colourlists


# print(overstrand_to_colourlist([7, 0, 8, 7, 9, 11, 1, 3, 10, 4, 0, 5], 3))
# print(len(overstrand_to_colourlist([7, 0, 8, 7, 9, 11, 1, 3, 10, 4, 0, 5], 3)))

# print(overstrand_to_colourlist([2, 0, 1], 3))
