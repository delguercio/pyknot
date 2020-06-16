from color_overstrand_to_index2lists import *

def reflect(current_universe, wall_color, p):
    """
    input: current universe, color of the wall you are traveling
           through, p for number of colorings
    output:the universe on the other side of the wall
    """
    if (2*wall_color - current_universe)%p == 0:
        return p
    else:
        return (2*wall_color - current_universe)%p

def matrix_index1(overstrand_list, color_list, sign_list, wherelists, horizontalorder, verticalorder, p):
    n = len(color_list)
    num_index2 = (p-1)//2
    numCol=num_index2*n+1
    numRow = num_index2*n
    matrix=[[0]*numCol for i in range(numRow)] #Build zero matrix
    for i in range(n):
        a = horizontalorder[i][0] #update a,b,c,d at each crossing
        b = horizontalorder[i][1]
        c = verticalorder[i][0]
        d = verticalorder[i][1]
        print(a,b,c,d)
        print(color_list[overstrand_list[i]])
        print(wherelists[a-1][i])
        #Find all epsilons
        epsilon = sign_list[i]
        if color_list[overstrand_list[i]] == wherelists[a-1][i]:
            epsilon_a_two = 1
        else:
            epsilon_a_two = -1
        if reflect(wherelists[b-1][i], color_list[i], p) == color_list[(i+1)%n]:
            epsilon_b_two = 1
        else:
            epsilon_b_two = -1
        if  wherelists[c-1][overstrand_list[i]] == reflect(color_list[overstrand_list[i]], color_list[i], p):
            epsilon_c_one = 1
        else:
            epsilon_c_one = -1
        if  wherelists[d-1][overstrand_list[i]] == color_list[(i+1)%n]: 
            epsilon_d_one = 1
        else:
            epsilon_d_one = -1
        # Fill rows 0-3 with top equations 
        matrix[i][i+(a-1) * n] = 1
        matrix[i][i+(a-1) * n+1] = -1
        matrix[i][overstrand_list[i]+(c-1)*n] = epsilon_c_one * epsilon_a_two
        matrix[i][-1] = epsilon * epsilon_a_two
        # Fill rows 4-7 with bottom equations
        matrix[i+n][i+(b-1)*n] = 1
        matrix[i+n][i+(b-1)*n+1] = -1
        matrix[i+n][overstrand_list[i]+(c-1)*n]= epsilon_c_one * epsilon_b_two
        matrix[i+n][overstrand_list[i]+(d-1)*n]= epsilon_d_one * epsilon_b_two     
    return matrix
    
def main():
    Mat = matrix_index1([2,3,0,1], [3,5,4,2], [-1,1,-1,1], [[4,4,0,1], [1,2,2,4]],\
                        [[1,2],[2,1],[1,2],[2,1]], [[2,1],[1,2],[2,1],[1,2]], 5)
    print(Mat)
main() 
    

        
                
                
                

    
    
    
    

    
                
            
    





                            
                                  
                              
                





                               
