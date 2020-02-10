
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

def side( list_of_lists ):
    """
    input:
    output:
    """
    return

def tier():
    """
    input:
    output:
    """
    return

# print("should be 1")
# print("i got "+str(reflect(4,0)))
# print("should be 2")
# print("i got "+str(reflect(1,4)))
# print("should be 3")
# print("i got "+str(reflect(3,3)))


def reflect_list( wall_1side_list , inout_strands , inout_strands_index , p ):
    if len(wall_1side_list)==((p-1)/2)+1: # base case 
        #print("inside base case")
        #print(wall_1side_list)
        return wall_1side_list
    else:
        if inout_strands_index == 0:
            #print("inside outgoing understrand color case")
            wall_color = wall_1side_list[-1]
            #print("wall_color")
            #print(wall_color)
            #print("wall_1side_list")
            #print(wall_1side_list)
            #print("reflected color")
            #print(reflect(wall_color,inout_strands[inout_strands_index],p))
            wall_1side_list.append(reflect(wall_color,inout_strands[inout_strands_index],p))#,inout_strands, 1, p)
            #print(wall_1side_list)
            return reflect_list( wall_1side_list, inout_strands , 1, p)
        else:
            wall_color = wall_1side_list[-1]
            wall_1side_list.append(reflect(wall_color,inout_strands[inout_strands_index],p))#,inout_strands, 1, p)
            return reflect_list( wall_1side_list, inout_strands , 0, p)

# print(reflect_list([0], [1,2], 0, 3))
# print(reflect_list([0], [1,2], 1, 3))
# print(reflect_list([1], [2,0], 0, 3))
# print(reflect_list([1], [2,0], 1, 3))
# print(reflect_list([2], [0,1], 0, 3))
# print(reflect_list([2], [0,1], 1, 3))
# print(reflect_list([4], [3,0], 0, 5)) #front
# print(reflect_list([4], [3,0], 1, 5)) #back
# print(reflect_list([2], [0,4], 0, 5)) #front
# print(reflect_list([2], [0,4], 1, 5)) #back
# print(reflect_list([2], [0,1], 0, 5))
# print(reflect_list([2], [0,1], 1, 5))


#want to turn colorlist [3, 0, 4, 2] into
#incomingoutgoing = [[3,0],[0,4],[4,2],[2,3]]
def incoming_outgoing_list(color_list):
    incomingoutgoing = []
    for i in range(len(color_list)):
        incomingoutgoing.append([color_list[i],color_list[(i+1)%len(color_list)]])
    return incomingoutgoing

#print(incoming_outgoing_list(color_4_1))

def wall_colors( overstrand_list , color_list , p ):
    """ co
    we want input to be

    overstrand_list, color_list, p an odd number

    and then the output will be TWO lists of numbers

    one of the lists will be [[[],[]],[[],[]],...,[[],[]]]
    [[[crossing 0 universe of the top on incoming understand, universe of the one below,...]
      [crossing 0 universe of the top on outgoing understand, universe of the one below,...]]
     [["      " 1 "                                        ", "                       ",...]]
     ...]
    """
    wall_color_lists = []
    incomingoutgoing_list = incoming_outgoing_list(color_list)
    for crossing in range(len(overstrand_list)):
        if crossing+1 != len(overstrand_list):
            wall_color_lists.append([reflect_list( [color_list[overstrand_list[crossing]]] , incomingoutgoing_list[crossing] , 0 , p ), reflect_list( [color_list[overstrand_list[crossing]]] , incomingoutgoing_list[crossing] , 1 , p )])
        else: #homogeneous crossing
            wall_color_lists.append

    return wall_color_lists

print(wall_colors(overstrand_5_2,color_5_2,7))

#
#
#wall_colors_8_5 = [[[2,4,5,1], [2, 7, 6, 3]]]#, [[6, 3, 5, 4], [6, 2, 7, 1]], [[3, 5, 6, 2], [3, 1, 7, 4]], [[1, 3, 4, 7], [1, 6, 5, 2]], [[1, 6, 5, 2], [1, 3, 4, 7]], [[4, 0, 5, 6], [4, 1, 3, 2]], [[7, 5, 4, 1], [7, 2, 3, 6]], [[2, 7, 6, 3], [2, 4, 5, 1]]]
#where_list_8_5 =  [[[1,0,0,1],[0,1,0,0]]]
#print(wall_colors(overstrand_8_5,color_8_5,7))
#[[2,4,5,1],[2,0,6,3]] [[1,0,0,1],[0,1,0,0]]

def pass_through(where_list):
    pass_where_list = []
    pass_where_list.append(where_list[1])
    pass_where_list.append(where_list[0])
    return pass_where_list

def colors_out(where_list,wall_colors):
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




