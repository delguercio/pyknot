import dihedral_linking_five as dl5


def index(iterable, value):

    for i in range(len(iterable)):
        if iterable[i] == value:
            return i


def universe_lists(colourlist, overstrandlist, p):

    n = len(colourlist)
    universes = []

    for i in range(n):
        overstrand = overstrandlist[i]
        colour_in = colourlist[i]
        colour_out = colourlist[(i + 1) % n]
        colour_over = colourlist[overstrand]

        if colour_in == colour_out:

            universe_pairs = []

            for j in range((p - 1) // 2):

                current_universe = (colour_in + j + 1) % p
                if current_universe == 0:
                    current_universe = p
                universe_pairs.append(
                    [current_universe, dl5.reflect(current_universe,
                                                   colour_in, p)])

            universes.append(universe_pairs)

        else:

            universes_left = [colour_over]
            current_universe = colour_over

            for j in range((p - 1) // 2):

                if j % 2 == 0:
                    next_universe = dl5.reflect(current_universe, colour_in, p)
                else:
                    next_universe = dl5.reflect(current_universe,
                                                colour_out, p)

                current_universe = next_universe
                universes_left.append(current_universe)

            universes_right = [colour_over]

            current_universe = colour_over

            for k in range((p - 1) // 2):

                if k % 2 == 0:
                    next_universe = dl5.reflect(current_universe,
                                                colour_out, p)
                else:
                    next_universe = dl5.reflect(current_universe, colour_in, p)

                current_universe = next_universe
                universes_right.append(current_universe)

            universes.append([universes_left, universes_right])

    return universes


def where_lists(colourlist, overstrandlist, p):

    universes = universe_lists(colourlist, overstrandlist, p)
    where_lists = []

    for i in range((p - 1) // 2):
        current_universe = universes[0][i % 2][i]
        where_list = [current_universe]

        for j in range(len(colourlist)):

            overstrand = overstrandlist[j]
            over_colour = colourlist[overstrand]

            current_universe = dl5.reflect(current_universe, over_colour, p)
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
        order_list = [0 for x in range((p - 1) // 2)]

        if colour_in == colour_over:

            for j in range((p - 1) // 2):
                where = wheres[j][i]
                for k in range((p - 1) // 2):
                    if where in crossing_universes[k]:
                        order_list[k] = j + 1

            order_lists.append(order_list)

        else:
            left_universes = crossing_universes[0]
            right_universes = crossing_universes[1]

            for j in range((p - 1) // 2):

                where = wheres[j][i]
                pair = dl5.reflect(where, colour_in, p)

                if where in left_universes and pair in left_universes:
                    index1 = index(left_universes, where)
                    index2 = index(left_universes, pair)
                else:
                    index1 = index(right_universes, where)
                    index2 = index(right_universes, pair)

                level = min(index1, index2)
                order_list[level] = j + 1

            order_lists.append(order_list)

    return order_lists


def vertical_order(colourlist, overstrandlist, p):

    universes = universe_lists(colourlist, overstrandlist, p)
    horizontal = horizontal_order(colourlist, overstrandlist, p)

    order_lists = []

    for i in range(len(colourlist)):

        crossing_universes = universes[i]
        overstrand = overstrandlist[i]
        over_crossing = universes[overstrand]

        order_list = []

        for j in range((p - 1) // 2):

            if colourlist[i] == colourlist[overstrand]:
                uni1 = crossing_universes[j][0]
                uni2 = crossing_universes[j][1]

            else:

                left_universes = crossing_universes[0]
                right_universes = crossing_universes[1]
                uni1 = left_universes[j + 1]
                uni2 = right_universes[j + 1]

            if colourlist[overstrand] == colourlist[overstrandlist
                                                    [overstrand]]:
                for k in range((p - 1) // 2):

                    if uni1 in over_crossing[k]:
                        order_list.append(horizontal[overstrand][k])

            else:

                if uni1 in over_crossing[0] and uni2 in over_crossing[0]:
                    index1 = index(over_crossing[0], uni1)
                    index2 = index(over_crossing[0], uni2)
                else:
                    index1 = index(over_crossing[1], uni1)
                    index2 = index(over_crossing[1], uni2)

                order_list.append(horizontal[overstrand][min(index1, index2)])

        order_lists.append(order_list)

    return(order_lists)


# print(universe_lists([2, 3, 4, 5, 6, 7, 1, 2], [4, 5, 6, 0, 1, 2, 3, 7], 7))
# print(horizontal_order([2, 3, 4, 5, 6, 7, 1, 2], [4, 5, 6, 0, 1, 2, 3, 7], 7))
# print(vertical_order([2, 3, 4, 5, 6, 7, 1, 2], [4, 5, 6, 0, 1, 2, 3, 7], 7))
