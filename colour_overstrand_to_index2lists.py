def index(l, v):

    for i in range(len(l)):
        if l[i] == v:
            return i

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


def universe_lists(colourlist, overstrandlist, p):

    n = len(colourlist)
    universes = []

    for i in range(n):
        
        overstrand = overstrandlist[i]
        colour_in = colourlist[i]
        colour_out = colourlist[(i+1)%n]
        colour_over = colourlist[overstrand]

        if colour_in == colour_out:

            universe_pairs = []

            for j in range((p-1)//2):

                current_universe = (colour_in + j +1)%p
                universe_pairs.append([current_universe, reflect(current_universe, colour_in,p)])

            universes.append(universe_pairs)
            
        else:

            universes_left = [colour_over]
            
            current_universe = colour_over
            
            for j in range((p-1)//2):

                if j%2 == 0:
                    next_universe = reflect(current_universe, colour_in, p)
                else:
                    next_universe = reflect(current_universe, colour_out, p)

                current_universe = next_universe
                universes_left.append(current_universe)

            universes_right = [colour_over]

            current_universe = colour_over
            
            for k in range((p-1)//2):

                if k%2 == 0:
                    next_universe = reflect(current_universe, colour_out, p)
                else:
                    next_universe = reflect(current_universe, colour_in, p)

                current_universe = next_universe
                universes_right.append(current_universe)

            universes.append([universes_left, universes_right])

    return universes

def where_lists(colourlist, overstrandlist,p):

    universes = universe_lists(colourlist, overstrandlist,p)

    strandcolour = colourlist[0]
    where_lists = []

    for i in range((p-1)//2):

        if i == 0%2:
            current_universe = universes[0][0][i]
        else:
            current_universe = universes[0][1][i]

        where_list=[current_universe]

        for j in range(len(colourlist)):

            overstrand = overstrandlist[j]
            over_colour = colourlist[overstrand]
            
            current_universe = reflect(current_universe, over_colour, p)
            where_list.append(current_universe)

        where_lists.append(where_list)

    return where_lists
        
def horizontal_order(colourlist, overstrandlist, p):

    universes = universe_lists(colourlist, overstrandlist, p)
    wheres = where_lists(colourlist, overstrandlist, p)

    order_lists = []

    for i in range(len(colourlist)):

        colour_in = colourlist[i]
        colour_over = colourlist[overstrandlist[i]]
        crossing_universes = universes[i]
        order_list = [0 for x in range((p-1)//2)]

        if colour_in == colour_over:

            for j in range((p-1)//2):
                where = wheres[j][i]

                for k in range((p-1)//2):
                    if where in crossing_universes[k]:
                        order_list[k]= j+1

            order_lists.append(order_list)
                

        else:
            left_universes = crossing_universes[0]
            right_universes = crossing_universes[1]

            for j in range((p-1)//2):

                where = wheres[j][i]
                pair = reflect(where, colour_in, p)

                if where in left_universes and pair in left_universes:
                    index1 = index(left_universes, where)
                    index2 = index(left_universes, pair)
                else:
                    index1 = index(right_universes, where)
                    index2 = index(right_universes, pair)

                level = min(index1, index2)
                order_list[level] = j+1

            order_lists.append(order_list)

    return order_lists

def vertical_order(colourlist, overstrandlist, p):

    universes = universe_lists(colourlist, overstrandlist, p)
    wheres = where_lists(colourlist, overstrandlist, p)
    horizontal = horizontal_order(colourlist, overstrandlist, p)

    order_lists = []

    for i in range(len(colourlist)):

        if colourlist[i] == colourlist[overstrandlist[i]]:

            order_list = horizontal[i]

        else:

            crossing_universes = universes[i]
            left_universes = crossing_universes[0]
            right_universes = crossing_universes[1]
            overstrand = overstrandlist[i]
            over_crossing = universes[overstrand]
                
            order_list = []
            
            for j in range((p-1)//2):

                universe1 = left_universes[j+1]
                universe2 = right_universes[j+1]

                if colourlist[overstrand] == colourlist[overstrandlist[overstrand]]:
                    for k in range((p-1)//2):

                        if universe1 in over_crossing[k]:
                            order_list.append(horizontal[overstrand][k])

                else:

                    if universe1 in over_crossing[0] and universe2 in over_crossing[0]:
                        index1 = index(over_crossing[0], universe1)
                        index2 = index(over_crossing[0], universe2)
                    else:
                        index1 = index(over_crossing[1], universe1)
                        index2 = index(over_crossing[1], universe2)

                    order_list.append(horizontal[overstrand][min(index1, index2)])

        order_lists.append(order_list)

    return(order_lists)

            














        
