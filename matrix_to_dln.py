import colour_overstrand_to_index2lists as i2l
import dihedral_linking_five as dln5
import braid_to_gauss
import matrix
import gauss_to_overstrand
import rrematrix_to_colourlist


def rrematrix_to_dict(rre_matrix, p, k):
    matrix = rre_matrix[0]
    pivots = list(rre_matrix[1])
    # print(pivots)

    n = len(matrix.col(0))
    num_crossings = n // ((p - 1) // 2)
    # print("n = ", num_crossings)
    coeff_dict = {}

    for i in range(n):
        if k == 0:
            coeff_dict[(0, i % num_crossings)] = 1
        else:
            coeff_dict[(0, i % num_crossings)] = 0

    for i in range(n):
        coeff_dict[((i // num_crossings + 1), i % num_crossings)] = 0

    for i in range(len(pivots)):
        row = matrix.row(i)
        coeff_dict[((pivots[i] // num_crossings) + 1, pivots[i] % num_crossings)] = row[-1]

    return coeff_dict


def matrix_to_dln(colourlist, overstrandlist, signlist, coeff_dict, p, k):

    universes_list = i2l.universe_lists(colourlist, overstrandlist, p)
    wheres = i2l.where_lists(colourlist, overstrandlist, p)
    vert_order = i2l.vertical_order(colourlist, overstrandlist, p)
    dlns = []

    dln = 0
    # print('K = ', k)

    # Linking number of Index 1 knot with surface
    if k == 0:      # Linking number of knot with itself?
        dln = "x"
    else:
        for i in range(len(colourlist)):
            if colourlist[i] == colourlist[overstrandlist[i]]:
                # print("homogeneous => no change. DLN = ", dln)
                dln += 0
            else:
                over_index = vert_order[i][-1]      # Need bottom overstrand
                where_over = wheres[over_index - 1][overstrandlist[i]]

                if where_over == colourlist[i]:
                    epsilon1 = 1
                else:
                    epsilon1 = -1

                if signlist[i] * epsilon1 == 1:
                    # Walk through R wall
                    dln += signlist[i] * coeff_dict[(over_index, overstrandlist[i])]

                else:
                    # Walk through L wall
                    dln -= signlist[i] * coeff_dict[(over_index, overstrandlist[i])]
                    if k == over_index:
                        dln += signlist[i]

    dlns.append(dln)

    # Linking numbers of Index 2 knots with surface
    for j in range(len(wheres)):        # Go through each of the index 2 knots

        if k == j + 1:      # Linking number of knot with itself?
            dln = "x"
        else:
            where_list = wheres[j]
            dln = 0

            for i in range(len(where_list) - 1):        # Go through each crossing
                where_under = where_list[i]
                universes = universes_list[i]
                # print("crossing:", i)

                if colourlist[i] == colourlist[overstrandlist[i]]:
                    for x in range(len(universes)):     # list of pairs of universes
                        if where_under in universes[x]:
                            over_index = vert_order[i][x]

                else:
                    if where_under in universes[0] and where_under in universes[1]:
                        # Must be on the top level, so a(j) = 0
                        over_index = 0
                    else:
                        if where_under in universes[0]:
                            level = i2l.index(universes[0], where_under)
                        else:
                            level = i2l.index(universes[1], where_under)

                        over_index = vert_order[i][level - 1]

                if over_index == 0:
                    where_over = colourlist[overstrandlist[i]]
                    # print("adding index 1 wall")
                    dln += signlist[i] * coeff_dict[(0, overstrandlist[i])]
                    # print(dln)
                else:
                    where_over = wheres[over_index - 1][overstrandlist[i]]

                    # print(where_under, where_over)

                    reflections = [dln5.reflect(where_over, colourlist[i], p),
                                   dln5.reflect(where_over, colourlist[overstrandlist[i]], p)]
                    if where_under in reflections:
                        epsilon1 = 1
                    else:
                        epsilon1 = -1
                    # print("adding wall", (over_index, overstrandlist[i]))
                    # if epsilon1 * signlist[i] == -1:
                        # print("right")
                    # else:
                        # print("left")
                    dln -= epsilon1 * coeff_dict[(over_index, overstrandlist[i])]

                    if k == over_index:
                        dln += (signlist[i] + epsilon1) // 2
            # print("Final DLN:", dln)
        dlns.append(dln)

    return dlns


def errors(complete_dln):

    error_list = []
    for i in range(len(complete_dln)):
        dln_mat = complete_dln[i]
        n = len(dln_mat)

        for j in range(n):
            for k in range(n):
                if dln_mat[j][k] != dln_mat[k][j]:
                    error_list.append([j, k])

    return error_list


def braid_to_dln(braid, p):
    gauss = braid_to_gauss.BraidToGauss(braid)

    signlist = braid_to_gauss.BraidToSigns(braid)
    overstrandlist = gauss_to_overstrand.create_overstrand_list(gauss)
    colourlists = rrematrix_to_colourlist.overstrand_to_colourlist(overstrandlist, p)

    complete_dln = []
    for i in range(len(colourlists)):
        colourlist = colourlists[i]

        if len(signlist) % 2 == 1:
            signlist.append(1)
            overstrandlist.append(len(overstrandlist))
            colourlist.append(colourlist[0])
        # print(signlist, overstrandlist, colourlist)
        dln_mat = []

        for k in range(((p - 1) // 2) + 1):
            mat = matrix.create_matrix(overstrandlist, colourlist, signlist, p, k)
            coeffs = rrematrix_to_dict(mat, p, k)
            # print("Coefficients: k = ", k)
            # print(coeffs)
            # print()

            dlns = matrix_to_dln(colourlist, overstrandlist, signlist, coeffs, p, k)
            dln_mat.append(dlns)
        complete_dln.append(dln_mat)

    error_list = errors(complete_dln)

    if error_list == []:
        return complete_dln

    else:
        return ["Error:", error_list]


# complete_dln = braid_to_dln([1, 1, 2, -1, -3, 2, -3], 3)
# for dln in complete_dln:
#     print(dln)
