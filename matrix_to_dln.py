import colour_overstrand_to_index2lists as i2l
import dihedral_linking_five as dln5
import braid_to_gauss
import matrix
import gauss_to_overstrand
import rrematrix_to_colourlist
import gauss_to_signlist


def rrematrix_to_dict(rre_matrix, p, k):
    matrix = rre_matrix[0]
    pivots = list(rre_matrix[1])
    # print(pivots)

    if len(matrix.row(0)) - 1 in pivots:
        return "X"

    else:
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
    if coeff_dict == "X":       # No DLN Exists
        for i in range(((p - 1) // 2) + 1):
            dlns.append("x")

    else:
        # Linking number of Index 1 knot with surface
        zero_2chain = rrematrix_to_dict(matrix.create_matrix(overstrandlist, colourlist, signlist, p, 0), p, 0)
        if zero_2chain == "X":
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

            where_list = wheres[j]
            dln = 0

            j_2chain = rrematrix_to_dict(matrix.create_matrix(overstrandlist, colourlist, signlist, p, j + 1), p, j + 1)
            if j_2chain == "X":
                dln = "x"
            else:
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


def errors(complete_dln, p):

    error_list = []
    for i in range(len(complete_dln)):
        dln_mat = complete_dln[i]
        n = len(dln_mat)

        for j in range(n):
            for k in range(n):
                if dln_mat[j][k] != dln_mat[k][j]:
                    if str(k) + ", " + str(j) + " not equal to " + str(j) + ", " + str(k) not in error_list:
                        error_message = str(j) + ", " + str(k) + " not equal to " + str(k) + ", " + str(j)
                        error_list.append(error_message)

                # if j != 0 and k != 0 and k != j:
                #     if "x" not in [dln_mat[j][k], dln_mat[0][j], dln_mat[0][k]]:
                #         if dln_mat[j][k] != (dln_mat[0][min(j + k, p - j - k)] + dln_mat[0][abs(j - k)]) / 2:
                #             if str(k) + ", " + str(j) + " not equal to (0, " + str(k) + " + 0, " + str(j) + ")/ 2" not in error_list:
                #                 error_message = str(j) + ", " + str(k) + " not equal to (0, " + str(j) + " + 0, " + str(k) + ")/ 2"
                #                 error_list.append(error_message)

    return error_list


def braid_to_dln(braid, p):
    gauss = braid_to_gauss.BraidToGauss(braid)

    signlist = braid_to_gauss.BraidToSigns(braid)
    overstrandlist = gauss_to_overstrand.create_overstrand_list(gauss)
    colourlists = rrematrix_to_colourlist.overstrand_to_colourlist(overstrandlist, p)

    complete_dln = []
    for i in range(len(colourlists)):
        colourlist = colourlists[i]

        if len(colourlist) % 2 == 1:
            colourlist.append(colourlist[0])
            if i == 0:
                signlist.append(1)
                overstrandlist.append(len(overstrandlist))
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

    error_list = errors(complete_dln, p)

    if error_list == []:
        return complete_dln

    else:
        return ["Error:", error_list]


def gauss_to_dln(gauss, p):

    signlist = gauss_to_signlist.SignList(gauss)
    overstrandlist = gauss_to_overstrand.create_overstrand_list(gauss)
    colourlists = rrematrix_to_colourlist.overstrand_to_colourlist(overstrandlist, p)

    complete_dln = []
    for i in range(len(colourlists)):
        colourlist = colourlists[i]

        if len(colourlist) % 2 == 1:
            colourlist.append(colourlist[0])
            if i == 0:
                signlist.append(1)
                overstrandlist.append(len(overstrandlist))
        # print(signlist, overstrandlist, colourlist)
        dln_mat = []

        for k in range(((p - 1) // 2) + 1):
            # print(k)
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


complete_dln = braid_to_dln([1, 1, 1, 2, -1, 2], 7)
for dln in complete_dln:
    print(dln)
