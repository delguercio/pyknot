



def reflect( current_universe , wall_color ):
    """

    """
    return (2*wall_color - current_universe)%5 

print("should be 1")
print("i got "+str(reflect(4,0)))
print("should be 2")
print("i got "+str(reflect(1,4)))
print("should be 3")
print("i got "+str(reflect(3,3)))



def where( overstrand_list , color_list ):
    """


    """
    num_crossings = len(overstrand_list)
    where_list_1 = []
    where_list_2 = []
    colors = [0,1,2,3,4]
    for i in range(len(overstrand_list)):
        print("We are on strand ", i)
        if i ==0- 0:
            where_list.append(color_list[overstrand_list[0]])
            #print("We initialized the first strand: ", where_list)
        elif i == 1:
            where_list.append(color_list[overstrand_list[0]])
            #print("We initialized the second strand: ", where_list)
        else:
            color_of_overstrand = color_list[overstrand_list[i-1]]
            color_of_overstrand = color_list[overstrand_list[(i-1)%num_crossings]]
            universe_of_incoming_understrand = where_list[i-1]
            #print('COLOR OF OVERSTRAND')
            #print(color_of_overstrand)
                #print(colors)
                where_list.append(colors[0])
                #print(where_list)

                colors = [1,2,3]
    return where_list




