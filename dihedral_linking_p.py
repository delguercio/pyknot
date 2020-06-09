overstrand_3_1 = [2, 0, 1, 3]
overstrand_4_1 = [2, 3, 0, 1]
overstrand_5_2 = [2, 4, 0, 1, 3, 5]
overstrand_6_1 = [2, 4, 0, 5, 1, 3]
overstrand_7_4 = [5, 4, 0, 6, 1, 2, 3, 7]
overstrand_7_7 = [4, 3, 6, 5, 0, 1, 2, 7]
overstrand_8_5 = [3, 6, 0, 1, 7, 2, 4, 5]
overstrand_9_35 = [6, 5, 7, 0, 8, 1, 3, 2, 4, 9]

color_3_1 = [1, 2, 3, 1]
color_4_1 = [4, 1, 5, 3] #5 coloring
color_5_2 = [2, 1, 5, 6, 3, 2] #7 coloring
color_6_1 = [3, 2, 1, 2, 3, 1]
color_7_4 = [1, 2, 3, 2, 1, 3, 3, 1]
color_7_7 = [1, 3, 2, 1, 2, 3, 3, 1]
color_8_5 = [4, 2, 5, 3, 1, 3, 7, 2] #7 coloring
color_9_35 = [3, 1, 2, 3, 3, 3, 2, 1, 3, 3]

sign_3_1 = [1, 1, 1, 1]
sign_6_1 = [1, -1, 1, 1, -1, 1]
sign_7_4 = [-1, -1, -1, -1, -1, -1, -1, 1]
sign_7_7 = [1, -1, 1, -1, 1, -1, 1, 1]
sign_9_35 = [-1, -1, -1, -1, -1, -1, -1, -1, -1, 1]




def reflect( current_universe , wall_color , p ):
    """
    input: current universe, color of the wall you are traveling
           through, p for number of colorings
    output:the universe on the other side of the wall
    """
    if (2*wall_color - current_universe)%p == 0:
        return p
    else:
        return (2*wall_color - current_universe)%p

def incoming_outgoing_list(color_list):
    """
    input: color list
    output: a list of lists or the index of the incoming understrand and outgoing understrand
    """
    incomingoutgoing = []
    for i in range(len(color_list)):
        incomingoutgoing.append([color_list[i],color_list[(i+1)%len(color_list)]])
    return incomingoutgoing



def reflect_list( wall_1side_list , inout_strands , inout_strands_index , p ):
    """
    this function works recursively by appending taking a list and appending
    the last element in the list reflected over the incoming or outgoing understrand
    alternating

    you initialize with inout_strands_index as either zero or one
    which indictes if you are reflecting over the incoming understrand 
    inout_strands[0] or the outgoing understrand inout_strands[1]

    helper functions: reflect(), incomingoutgoing_list()
    input: wall_1side_list inout_strands inout_strands_index p
    output: wall_1side_list
    """
    if len(wall_1side_list)==((p-1)/2)+1: # base case
        return wall_1side_list #return 
    else:
        if inout_strands_index == 0:
            wall_color = wall_1side_list[-1] # bottom universe at crossing
            wall_1side_list.append(reflect(wall_color,inout_strands[inout_strands_index],p))#,inout_strands, 1, p)
            return reflect_list( wall_1side_list, inout_strands , 1, p)
        else:
            wall_color = wall_1side_list[-1]
            wall_1side_list.append(reflect(wall_color,inout_strands[inout_strands_index],p))#,inout_strands, 1, p)
            return reflect_list( wall_1side_list, inout_strands , 0, p)


def wall_colors( overstrand_list , color_list , p ):
    """
    input: overstrand_list, color_list, p an odd number

    output: all of the walls in all crossings of the knot

    one of the lists will be [ [ [],[] ],[ [],[] ],...,[ [],[] ] ]
    [[[crossing 0 universe of the top on incoming understand, universe of the one below,...]
      [crossing 0 universe of the top on outgoing understand, universe of the one below,...]]
     [["      " 1 "                                        ", "                       ",...]]
     ...]
    """
    wall_color_lists = []
    incomingoutgoing_list = incoming_outgoing_list(color_list)
    for crossing in range(len(overstrand_list)):#if the color of the overstrand does not match the color of the incoming understrand
        if color_list[overstrand_list[crossing]] != color_list[crossing]: #heterogenous
            heterogenous_wall_list = []
            heterogenous_wall_list.append(reflect_list( [color_list[overstrand_list[crossing]]] , incomingoutgoing_list[crossing] , 0 , p ))
            heterogenous_wall_list.append(reflect_list( [color_list[overstrand_list[crossing]]] , incomingoutgoing_list[crossing] , 1 , p ))
            wall_color_lists.append(heterogenous_wall_list)
        else: #homogeneous crossing, just want to refect all the colors except the incoming understrand
            homogeneous_wall_list = []
            homogeneous_color = color_list[overstrand_list[crossing]]
            homog_index_list = []
            for i in range(1,int(((p+1)/2))):
                #print(i)
                if (homogeneous_color+i)%p == 0:
                    homog_index_list.append(p)
                else:
                    #print(i)
                    homog_index_list.append((homogeneous_color+i)%p)
            homogeneous_wall_list.append(homog_index_list)
            homogeneous_wall_list.append([reflect(color, homogeneous_color, p) for color in homog_index_list])
            wall_color_lists.append(homogeneous_wall_list)
    return wall_color_lists

def where(overstrand_list, color_list, p):
    """

    """
    all_walls = wall_colors(overstrand_list,color_list, p)
    print(all_walls)
    first_wall = all_walls[0]
    side = 0
    where_lists = []
    for tier in range(len(first_wall[0])-1):
        where_lists.append([first_wall[side%2][tier]])
        side+=1
    for where_list in where_lists:
        for i in range(len(overstrand_list)-1):
            if where_list[i] == color_list[overstrand_list[i+1]]:
                where_list.append(color_list[overstrand_list[i+1]])
            else:                
                where_list.append(reflect(where_list[i],color_list[overstrand_list[i+1]],p))
    return where_lists


#This function outputs the matrix containing x_i, x_i+1, x_f(i) and a constant. This relies on using epsilon rules. 
def initialize_matrix(overstrand_list,color_list,where_list,sign_list,p):
    #Make a starting matrix of all 0s
    num_index2 = int((p-1)/2)
    x_matrix = [[0]*(num_index2*len(overstrand_list)+1) for i in range(num_index2*len(overstrand_list))]
    epsilon_a_two = 0
    epsilon_b_two = 0
    epsilon_c_one = 0
    epsilon_d_one = 0

    #Now we need to find the signs of the first two epsilons.
    #Loop through each of the crossings
    for i in range(num_index2*len(overstrand_list)):
        #initialize epsilon_three so we can see if a crossing is inhomogeneous or not easily
        epsilon_a_two = 0
        epsilon_b_two = 0
        epsilon_c_one = 0
        epsilon_d_one = 0

        epsilon_three = 0
        
        for i in range(len(overstrand_list)):
            if color_list[i]==color_list[(i+1)%len(overstrand_list)]==color_list[overstrand_list[i]]:
            #IF HOMOGENEOUS CROSSING
                continue
            else:
                #now we need to add the equation information to this row of the matrix.
                x_matrix[i][i] +=1
                x_matrix[i][(i+1)%len(overstrand_list)] -=1
                if color_list[overstrand_list[i]] == where_list[overstrand_list[i]]:
                    epsilon_a_two = 1
                    #epsilon two is positive if the color of the overstrand is equal to the where of i. 
                    if reflect(where_lists[][]color_list[overstrand_list[i]] == where_list[i]:
                        epsilon_two = 1
                    elif color_list[overstrand_list[i]] != where_list[i]:
                        epsilon_two = -1
                elif color_list[overstrand_list[i]] != where_list[overstrand_list[i]]:
                    epsilon_a_two = -1
                    #epsilon two is positive if the color of the overstrand is equal to the where of i. 
                    if color_list[overstrand_list[i]] == where_list[i]:
                        epsilon_two = 1
                    elif color_list[overstrand_list[i]] != where_list[i]:
                        epsilon_two = -1



        #see if we have an epsilon three. this would happen if all three strands are the same color (homogeneous crossing)

            #epsilon 3 is negative if where of i is the same as where of the overstrand.
 #           if(where_list[i] == where_list[overstrand_list[i]]):
 #               epsilon_three = -1
 #           else:
 #               epsilon_three = 1


      
        #edits as a heterogenous crossing
 #       if epsilon_three == 0:
            #edit the overstrand coefficient
            #x_matrix[i][overstrand_list[i]] += (epsilon_one*epsilon_two)
            #edit the constant on the LEFT side of the equation (the equation will be set equal to 0?)
            #x_matrix[i][len(overstrand_list)] += -(sign_list[i]*epsilon_two)
 #           continue 
      #edits as a homogenous crossing
 #       else:
            #edit overstrand coefficient. constant is 0. 
 #           x_matrix[i][overstrand_list[i]] += 2*epsilon_three


    #print("MATRIX")
    #print(x_matrix)

    #return row reduced version of matrix
    return sympy.Matrix(x_matrix).rref()[0] #x_matrix #


print(where(overstrand_8_5,color_8_5,7))



##def index(l, v):
##
##    for i in range(len(l)):
##        if l[i] == v:
##            return i
##
##def universe_lists(colourlist, overstrandlist, p):
##
##    n = len(colourlist)
##    universes = []
##
##    for i in range(n):
##        
##        overstrand = overstrandlist[i]
##        colour_in = colourlist[i]
##        colour_out = colourlist[(i+1)%n]
##        colour_over = colourlist[overstrand]
##
##        if colour_in == colour_out:
##
##            universe_pairs = []
##
##            for j in range((p-1)//2):
##
##                current_universe = (colour_in + j +1)%p
##                universe_pairs.append([current_universe, reflect(current_universe, colour_in,p)])
##
##            universes.append(universe_pairs)
##            
##        else:
##
##            universes_left = [colour_over]
##            
##            current_universe = colour_over
##            
##            for j in range((p-1)//2):
##
##                if j%2 == 0:
##                    next_universe = reflect(current_universe, colour_in, p)
##                else:
##                    next_universe = reflect(current_universe, colour_out, p)
##
##                current_universe = next_universe
##                universes_left.append(current_universe)
##
##            universes_right = [colour_over]
##
##            current_universe = colour_over
##            
##            for k in range((p-1)//2):
##
##                if k%2 == 0:
##                    next_universe = reflect(current_universe, colour_out, p)
##                else:
##                    next_universe = reflect(current_universe, colour_in, p)
##
##                current_universe = next_universe
##                universes_right.append(current_universe)
##
##            universes.append([universes_left, universes_right])
##
##    return universes
##
##def where_lists(colourlist, overstrandlist,p):
##
##    universes = universe_lists(colourlist, overstrandlist,p)
##
##    strandcolour = colourlist[0]
##    where_lists = []
##
##    for i in range((p-1)//2):
##
##        if i == 0%2:
##            current_universe = universes[0][0][i]
##        else:
##            current_universe = universes[0][1][i]
##
##        where_list=[current_universe]
##
##        for j in range(len(colourlist)):
##
##            overstrand = overstrandlist[j]
##            over_colour = colourlist[overstrand]
##            
##            current_universe = reflect(current_universe, over_colour, p)
##            where_list.append(current_universe)
##
##        where_lists.append(where_list)
##
##    return where_lists
##        
##def horizontal_order(colourlist, overstrandlist, p):
##
##    universes = universe_lists(colourlist, overstrandlist, p)
##    wheres = where_lists(colourlist, overstrandlist, p)
##
##    order_lists = []
##
##    for i in range(len(colourlist)):
##
##        colour_in = colourlist[i]
##        colour_over = colourlist[overstrandlist[i]]
##        crossing_universes = universes[i]
##        order_list = [0 for x in range((p-1)//2)]
##
##        if colour_in == colour_over:
##
##            for j in range((p-1)//2):
##                where = wheres[j][i]
##
##                for k in range((p-1)//2):
##                    if where in crossing_universes[k]:
##                        order_list[k]= j+1
##
##            order_lists.append(order_list)
##                
##
##        else:
##            left_universes = crossing_universes[0]
##            right_universes = crossing_universes[1]
##
##            for j in range((p-1)//2):
##
##                where = wheres[j][i]
##                pair = reflect(where, colour_in, p)
##
##                if where in left_universes and pair in left_universes:
##                    index1 = index(left_universes, where)
##                    index2 = index(left_universes, pair)
##                else:
##                    index1 = index(right_universes, where)
##                    index2 = index(right_universes, pair)
##
##                level = min(index1, index2)
##                order_list[level] = j+1
##
##            order_lists.append(order_list)
##
##    return order_lists
##
##def vertical_order(colourlist, overstrandlist, p):
##
##    universes = universe_lists(colourlist, overstrandlist, p)
##    wheres = where_lists(colourlist, overstrandlist, p)
##    horizontal = horizontal_order(colourlist, overstrandlist, p)
##
##    order_lists = []
##
##    for i in range(len(colourlist)):
##
##        if colourlist[i] == colourlist[overstrandlist[i]]:
##
##            order_list = horizontal[i]
##
##        else:
##
##            crossing_universes = universes[i]
##            left_universes = crossing_universes[0]
##            right_universes = crossing_universes[1]
##            overstrand = overstrandlist[i]
##            over_crossing = universes[overstrand]
##                
##            order_list = []
##            
##            for j in range((p-1)//2):
##
##                universe1 = left_universes[j+1]
##                universe2 = right_universes[j+1]
##
##                if colourlist[overstrand] == colourlist[overstrandlist[overstrand]]:
##                    for k in range((p-1)//2):
##
##                        if universe1 in over_crossing[k]:
##                            order_list.append(horizontal[overstrand][k])
##
##                else:
##
##                    if universe1 in over_crossing[0] and universe2 in over_crossing[0]:
##                        index1 = index(over_crossing[0], universe1)
##                        index2 = index(over_crossing[0], universe2)
##                    else:
##                        index1 = index(over_crossing[1], universe1)
##                        index2 = index(over_crossing[1], universe2)
##
##                    order_list.append(horizontal[overstrand][min(index1, index2)])
##
##        order_lists.append(order_list)
##
##    return(order_lists)


















                               
