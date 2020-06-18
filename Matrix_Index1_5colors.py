import colour_overstrand_to_index2lists as i2l
import dihedral_linking_five as dl5
from sympy import Matrix


def matrix_index1(overstrand_list, color_list, sign_list, p):

    wherelists = i2l.where_lists(color_list, overstrand_list, p)
    horizontalorder = i2l.horizontal_order(color_list, overstrand_list, p)
    verticalorder = i2l.vertical_order(color_list, overstrand_list, p)

    n = len(color_list)
    num_index2 = (p - 1) // 2
    numCol = num_index2 * n + 1
    numRow = num_index2 * n
    coeff_matrix = [[0] * numCol for i in range(numRow)]  # Build zero matrix
    for i in range(n):
        a = horizontalorder[i][0]  # update a,b,c,d at each crossing
        b = horizontalorder[i][1]
        c = verticalorder[i][0]
        d = verticalorder[i][1]

        # Find all epsilons
        epsilon = sign_list[i]
        if color_list[overstrand_list[i]] == wherelists[a - 1][i]:
            epsilon_a_two = 1
        else:
            epsilon_a_two = -1

        if dl5.reflect(wherelists[b - 1][i], color_list[i], p) == color_list[
                (i + 1) % n]:
            epsilon_b_two = 1
        else:
            epsilon_b_two = -1

        if wherelists[c - 1][overstrand_list[i]] == dl5.reflect(
                color_list[overstrand_list[i]], color_list[i], p):
            epsilon_c_one = 1
        else:
            epsilon_c_one = -1

        if wherelists[d - 1][overstrand_list[i]] == color_list[(i + 1) % n]:
            epsilon_d_one = 1
        else:
            epsilon_d_one = -1

        # Fill rows 0-3 with top equations
        coeff_matrix[i][i + (a - 1) * n] = 1
        coeff_matrix[i][(i + 1) % n + (a - 1) * n] = -1
        coeff_matrix[i][overstrand_list[i] + (c - 1) * n] = epsilon_c_one * epsilon_a_two
        coeff_matrix[i][-1] = epsilon * epsilon_a_two
        # Fill rows 4-7 with bottom equations
        coeff_matrix[i + n][i + (b - 1) * n] = 1
        coeff_matrix[i + n][(i + 1) % n + (b - 1) * n] = -1
        coeff_matrix[i + n][overstrand_list[i] + (c - 1) * n] = epsilon_c_one * epsilon_b_two
        coeff_matrix[i + n][overstrand_list[i] + (d - 1) * n] = epsilon_d_one * epsilon_b_two

    return Matrix(coeff_matrix).rref()


# def main():
#     Mat = matrix_index1([2, 3, 0, 1], [3, 5, 4, 2], [-1, 1, -1, 1], 5)
#     print(Mat)
# main()

print(matrix_index1([2, 3, 0, 1], [3, 5, 4, 2], [-1, 1, -1, 1], 5))
