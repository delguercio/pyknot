# import colour_overstrand_to_index2lists as i2l
import dihedral_linking_five as dln5
import colour_overstrand_to_index2lists as i2l
from sympy import Matrix


def create_matrix(overstrandlist, colorlist, signlist, p, k):
    # k = number of the surface. k = 0 => index 1 surface, k = 1 => 1st index 2, etc.

    wherelists = i2l.where_lists(colorlist, overstrandlist, p)
    horizontalorder = i2l.horizontal_order(colorlist, overstrandlist, p)
    verticalorder = i2l.vertical_order(colorlist, overstrandlist, p)
    # print(verticalorder)

    n = len(colorlist)
    num_index2 = (p - 1) // 2
    numCol = num_index2 * n + 1
    numRow = num_index2 * n
    coeff_matrix = [[0] * numCol for i in range(numRow)]  # Build zero matrix

    for i in range(n):

        for j in range(num_index2):
            # print(j)
            h = horizontalorder[i][j]
            where_under = wherelists[h - 1][i]
            # edit matrix so that x^h_i = 1, x^h_(i+1) = -1
            coeff_matrix[i + j * n][i + (h - 1) * n] = 1
            coeff_matrix[i + j * n][(i + 1) % n + (h - 1) * n] = -1

            # a = index of overstrand above understrand, b = index of overstrand below understrand
            # (for homogeneous crossing, a = b)
            # We have 8 cases in total to consider:
            # 1. if i is inhomogeneous, j = 0 and k = 0
            # 2. if i is inhomogeneous, j = 0 and k = b
            # 3. if i is inhomogeneous, j = 0 and k != 0, b
            # 4. if i is inhomogeneous, j != 0 and k != a, b
            # 5. if i is inhomogeneous, j != 0, k = a
            # 6. if i is inhomogeneous, j != 0, k = b
            # 7. if i is homogeneous, k != a
            # 8. if i is homogeneous, k = a

            if colorlist[i] == colorlist[overstrandlist[i]]:
                # homogeneous crossing
                # find a
                a = verticalorder[i][j]

                # find where of understrand and overstrand
                # look at a^th index 2 when overstrand is the understrand
                where_over = wherelists[a - 1][overstrandlist[i]]
                # find epsilon1
                if where_under == where_over:
                    epsilon1 = -1
                else:
                    epsilon1 = 1

                coeff_matrix[i + j * n][overstrandlist[i] + (a - 1) * n] += 2 * epsilon1

                if k == a:      # (Case 8)
                    # x^h_i - x^h_{i+1} + 2epsilon4 x^a_{f(i)} = epsilon4
                    coeff_matrix[i + j * n][-1] = epsilon1
            else:
                # inhomogeneous crossing
                b = verticalorder[i][j]
                # epsilon_b = 1 if where functions are next to each other, -1 otherwise
                where_over = wherelists[b - 1][overstrandlist[i]]

                reflections = [dln5.reflect(where_under, colorlist[i], p),
                               dln5.reflect(where_under, colorlist[overstrandlist[i]], p)]

                if where_over in reflections:
                    epsilon1 = 1
                else:
                    epsilon1 = -1

                coeff_matrix[i + j * n][overstrandlist[i] + (b - 1) * n] = epsilon1  # (Case 1, 2, 3, 4, 5, 6)
                if k == b:
                    if where_over in [where_under, dln5.reflect(where_under, colorlist[i], p)]:
                        epsilon2 = 1
                    else:
                        epsilon2 = -1
                    if signlist[i] * epsilon2 == -1:
                        coeff_matrix[i + j * n][-1] = epsilon1   # (Case 2, Case 6)

                if j == 0 and k == 0:  # (Case 1)
                    # find epsilon0 (previously epsilon_a_2)
                    if where_under == colorlist[overstrandlist[i]]:
                        epsilon0 = 1
                    else:
                        epsilon0 = -1
                    # constant in matrix = signlist[i] * epsilon0
                    coeff_matrix[i + j * n][-1] = epsilon0 * signlist[i]

                if j != 0:
                    a = verticalorder[i][j - 1]
                    # epsilon1 = 1 if where functions are next to each other, -1 otherwise
                    where_over = wherelists[a - 1][overstrandlist[i]]

                    reflections = [dln5.reflect(where_under, colorlist[i], p),
                                   dln5.reflect(where_under, colorlist[overstrandlist[i]], p)]

                    if where_over in reflections:
                        epsilon1 = 1
                    else:
                        epsilon1 = -1

                    coeff_matrix[i + j * n][overstrandlist[i] + (a - 1) * n] = epsilon1  # (Case 4, 5, 6)

                    if k == a:
                        if where_over in [where_under, dln5.reflect(where_under, colorlist[i], p)]:
                            epsilon2 = 1
                        else:
                            epsilon2 = -1
                        if signlist[i] * epsilon2 == -1:
                            coeff_matrix[i + j * n][-1] = epsilon1  # (Case 5)

    # print(coeff_matrix)
    return Matrix(coeff_matrix).rref()


# print(create_matrix([3, 6, 5, 0, 1, 2, 6, 4], [5, 4, 3, 2, 3, 5, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], 5, 0))
# print(create_matrix([2, 0, 1, 3], [2, 3, 1, 2], [-1, -1, -1, 1], 3, 0))
# print(create_matrix([3, 0, 1, 2], [4, 3, 5, 1], [1, -1, 1, -1], 5, 2))
