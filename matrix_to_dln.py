import colour_overstrand_to_index2lists as i2l
import dihedral_linking_five as dl5
from sympy import Matrix


def rrematrix_to_dict(rre_matrix):
    matrix = rre_matrix[0]
    pivots = list(rre_matrix[1])

    n = len(matrix.col(0))
    num_crossings = n // 2
    coeff_dict = {}

    for i in range(n):
        coeff_dict[((i // num_crossings) + 1, i % num_crossings)] = 0

    for i in range(len(pivots)):
        row = matrix.row(i)
        coeff_dict[((pivots[i] // num_crossings) + 1, pivots[i] % num_crossings)] = row[-1]

    return coeff_dict


def matrix_to_dln(colourlist, overstrandlist, signlist, coeff_dict, p):

    universes_list = i2l.universe_lists(colourlist, overstrandlist, p)
    wheres = i2l.where_lists(colourlist, overstrandlist, p)
    vert_order = i2l.vertical_order(colourlist, overstrandlist, p)
    dlns = []

    for i in range(len(wheres)):  # Go through each of the where lists

        dln = 0
        where_list = wheres[i]

        for j in range(len(universes_list)):  # Go through each crossing
            where = where_list[j]
            universes = universes_list[j]

            for k in range(len(universes)):
                if where in universes[k]:
                    level = i2l.index(universes[k], where)
                    break

            # index 1 is only the zeroth level at inhomogeneous crossings
            if level == 0 and colourlist[j] != colourlist[overstrandlist[j]]:
                coeff = 1
            else:
                knot = vert_order[j][level - 1]
                coeff = coeff_dict[(knot, overstrandlist[j])]

                vertical_where = wheres[knot - 1][overstrandlist[j]]
                if where == vertical_where or where == dl5.reflect(
                        vertical_where,
                        colourlist[j], p):
                    e = 1
                else:
                    e = -1

                coeff = coeff * e * signlist[j]

            dln += coeff * signlist[j]

        dlns.append(dln)

    return dlns


coeffs = rrematrix_to_dict((Matrix([[1, 0, 0, 0, 1, 0, 1, -1, 0],
                                    [0, 1, 0, 0, 1, 0, 0, -1, 1],
                                    [0, 0, 1, 0, 1, -1, 1, 0, 0],
                                    [0, 0, 0, 1, 0, -1, 1, 0, -1],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]), (0, 1, 2, 3)))

print(matrix_to_dln([3, 5, 4, 2], [2, 3, 0, 1], [-1, 1, -1, 1], coeffs, 5))
