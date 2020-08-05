 # inhomogeneous crossing
import colour_overstrand_to_index2lists as i2l
import dihedral_linking_five as dl5
from sympy import Matrix
        def matrix_p(overstrand_list, color_list, sign_list, p, k):
            wherelists = i2l.where_lists(color_list, overstrand_list, p)
            horizontalorder = i2l.horizontal_order(color_list, overstrand_list, p)
            verticalorder = i2l.vertical_order(color_list, overstrand_list, p)
            n = len(color_list)
            num_index2 = (p - 1) // 2
            numCol = num_index2 * n + 1
            numRow = num_index2 * n
            coeff_matrix = [[0] * numCol for i in range(numRow)]  # Build zero matrix
            for i in range(n):
                epsilon = signlist[i]
                for j in range(num_index2):
                    coeff_matrix[i + j * n][i + (h - 1) * n] = 1
                    coeff_matrix[i + j * n][(i + 1) % n + (h - 1) * n] = -1
                    b = verticalorder[i][j]
                    if wherelists[h-1][i] == dl5.reflect(wherelists[b - 1][overstrand_list[i]], color_list[i], p]) or
                     wherelists[h-1][i] == dl5.reflect(wherelists[b - 1][overstrand_list[i]], color_list[overstrand_list[i]], p]):
                        epsilon_b = 1
                    else:
                        epsilon_b = -1
                    coeff_matrix[i + j * n][overstrandlist[i] + (b - 1) * n] = epsilon_b
                    if k == b:
                        if wherelists[h-1][i] == wherelists[b-1][overstrand_list[i]] or
                        wherelists[b-1][overstrand_list[i]] == dl5.reflect(wherelists[h - 1][i], color_list[i], p]):
                            epsilon_2 = 1
                        else:
                            epsilon_2 = -1
                        if epsilon_2 * epsilon == -1:
                            coeff_matrix[i][-1] = epsilon_b
                    if j == 0 and k == 0:
                       if wherelists[h-1][i] == color[overstrand[i]]:
                           epsilon_0 = 1
                       else:
                           epsilon_0 = -1
                       coeff_matrix[i][-1] = signlist[i] * epsilon_0
                    if j!= 0:
                        a = verticalorder[i][j-1]
                        if wherelists[h-1][i]== dl5.reflect(wherelists[a - 1][overstrand_list[i]], color_list[i], p]) or
                        wherelists[h-1][i]== dl5.reflect(wherelists[a - 1][overstrand_list[i]], color_list[overstrand_list[i]], p]):
                            epsilon_a = 1
                        else:
                            epsilon_a = -1
                        coeff_matrix[i + j* n][overstrandlist[i] + (a - 1) * n] = epsilon_a
                        if k == a:
                            if wherelists[h-1][i] == wherelists[a-1][overstrand_list[i]] or
                            wherelists[a-1][overstrand_list[i]] == dl5.reflect(wherelists[h - 1][i], color_list[i], p]):
                                epsilon_2 = 1
                            else:
                                epsilon_2 = -1
                            if epsilon_2 * epsilon == -1:
                                coeff_matrix[i][-1] = epsilon_2
            return Matrix(coeff_matrix).rref()
                        
