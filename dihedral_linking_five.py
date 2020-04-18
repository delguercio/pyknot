
overstrand_3_1 = [2, 0, 1, 3]
overstrand_4_1 = [2, 3, 0, 1]
overstrand_5_2 = [2, 4, 0, 1, 3, 5]
overstrand_6_1 = [2, 4, 0, 5, 1, 3]
overstrand_7_4 = [5, 4, 0, 6, 1, 2, 3, 7]
overstrand_7_7 = [4, 3, 6, 5, 0, 1, 2, 7]
overstrand_8_5 = [3, 6, 0, 1, 7, 2, 4, 5]
overstrand_9_35 = [6, 5, 7, 0, 8, 1, 3, 2, 4, 9]

color_3_1 = [1, 2, 3, 1]
color_4_1 = [3, 0, 4, 2] #5 coloring
color_5_2 = [2, 1, 5, 6, 3, 2] #7 coloring
color_6_1 = [3, 2, 1, 2, 3, 1]
color_7_4 = [1, 2, 3, 2, 1, 3, 3, 1]
color_7_7 = [1, 3, 2, 1, 2, 3, 3, 1]
color_8_5 = [3, 1, 4, 2, 0, 2, 6, 1] #7 coloring
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
    return (2*wall_color - current_universe)%p 


def reflect_list( wall_1side_list , inout_strands , inout_strands_index , p ):
    """
    this function works by appending 

    you initialize with inout_strands_index as either zero or one

    helper functions: reflect
    input: wall_1side_list inout_strands inout_strands_index p
    output: wall_1side_list
    """
    if len(wall_1side_list)==((p-1)/2)+1: # base case
        return wall_1side_list #return 
    else:
        if inout_strands_index == 0:
            wall_color = wall_1side_list[-1] # bottom universe at crossing
            print("wall color is")
            print(wall_color)
            wall_1side_list.append(reflect(wall_color,inout_strands[inout_strands_index],p))#,inout_strands, 1, p)
            return reflect_list( wall_1side_list, inout_strands , 1, p)
        else:
            wall_color = wall_1side_list[-1]
            wall_1side_list.append(reflect(wall_color,inout_strands[inout_strands_index],p))#,inout_strands, 1, p)
            return reflect_list( wall_1side_list, inout_strands , 0, p)

def incoming_outgoing_list(color_list):
    """
    input:
    output:
    """
    incomingoutgoing = []
    for i in range(len(color_list)):
        incomingoutgoing.append([color_list[i],color_list[(i+1)%len(color_list)]])
    return incomingoutgoing


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
            colors = range(0,p).remove(homogeneous_color)
            homogeneous_wall_list.append(colors)
            homogeneous_wall_list.append([reflect(color, homogeneous_color, p) for color in colors])
            wall_color_lists.append(homogeneous_wall_list)
    return wall_color_lists

#print(wall_colors(overstrand_5_2,color_5_2,7))

# homogeneous_wall_list = []
# p = 7
# homogeneous_color = 2
# colors = range(0,p)
# colors.remove(homogeneous_color)
# print(colors)
# homogeneous_wall_list.append(colors)
# homogeneous_wall_list.append([reflect(color, homogeneous_color, p) for color in colors])
# print(homogeneous_wall_list)

#wall_colors_8_5 = [[[2,4,5,1], [2, 7, 6, 3]]]#, [[6, 3, 5, 4], [6, 2, 7, 1]], [[3, 5, 6, 2], [3, 1, 7, 4]], [[1, 3, 4, 7], [1, 6, 5, 2]], [[1, 6, 5, 2], [1, 3, 4, 7]], [[4, 0, 5, 6], [4, 1, 3, 2]], [[7, 5, 4, 1], [7, 2, 3, 6]], [[2, 7, 6, 3], [2, 4, 5, 1]]]
#where_list_8_5 =  [[[1,0,0,2],[0,3,0,0]]]
#print(wall_colors(overstrand_8_5,color_8_5,7))
#[[2,4,5,1],[2,0,6,3]] [[1,0,0,1],[0,1,0,0]]

def pass_through(where_list):
    """
    if you intialize with a list of lists where_lists where a 1-3 represents
    the location of the numbered men
    this list "passes the men through to the other side
    but in reality it just switches the order of the two lists returns a new
    list with the desired order
    input:
    output:
    """
    pass_where_list = []
    pass_where_list.append(where_list[1])
    pass_where_list.append(where_list[0])
    return pass_where_list

#print(pass_through(where_list_8_5))

def colors_out(where_list,wall_colors):
    """
    input:
    output:
    """
    colors_out_listoflists = []
    for k in range(len(wall_colors[0])):
        print(where_list[0][k])
        colors_out_list = [a*b for a,b in zip(where_list[0][k],wall_colors[0][k])]
        colors_out_listoflists.append(colors_out_list)
        colors_out_list = []
    return colors_out_listoflists

#print(pass_through(where_list_8_5))
#print(colors_out(where_list_8_5, wall_colors_8_5))
#print(wall_colors_8_5[0][1].index()))
#print(wall_colors(overstrand_4_1,color_4_1,5))


# def where( overstrand_list , color_list ):
#     """


#     """
#     num_crossings = len(overstrand_list)
#     where_list_1 = []
#     where_list_2 = []
#     colors = [0,1,2,3,4]
#     for i in range(len(overstrand_list)):
#         print("We are on strand ", i)
#         if i ==0- 0:
#             where_list.append(color_list[overstrand_list[0]])
#             #print("We initialized the first strand: ", where_list)
#         elif i == 1:
#             where_list.append(color_list[overstrand_list[0]])
#             #print("We initialized the second strand: ", where_list)
#         else:
#             color_of_overstrand = color_list[overstrand_list[i-1]]
#             color_of_overstrand = color_list[overstrand_list[(i-1)%num_crossings]]
#             universe_of_incoming_understrand = where_list[i-1]
#             #print('COLOR OF OVERSTRAND')
#             #print(color_of_overstrand)
#                 #print(colors)
#                 where_list.append(colors[0])
#                 #print(where_list)

#                 colors = [1,2,3]
#     return where_list




