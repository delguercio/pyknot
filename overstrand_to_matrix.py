from array import *
import csv

#three_one = [2, 0, 1, 3]
#six_one = [2, 4, 0, 5, 1, 3]
#seven_four = [4, 5, 6, 1, 0, 3, 2, 7]
#seven_seven = [4, 3, 6, 5, 0, 1, 2, 7]
#eight_five = [3, 6, 0, 1, 7, 2, 4, 5]
#eight_ten = [6, 4, 5, 7, 2, 0, 3, 1]


def create_matrix(overstrand_list):
    """
        you know that the 0th crossing will have strands 0 and 1
        you can you know the third strand at the 0th crosssing will be 1
        (i.e. indexes (0,0),(0,1) (0,overstrand_list[0])
        the second crossing will have strands 1 and 2 and so on
        (i.e. indexes (1,1),(1,2) will get a 1)
        you can know the third strand at the nth crossing by checking
        what is at the nth position of the overstrand_list.
        If odd, an extra loop was added at the end of the overstrand_list
        so to compensate for that if the last index equals the last value
        that means there a loop that crosses over itself and it will always
        have the 0th strand and then itself twice. the last strand will 
        not cross itself unless you put in a loop.
        input: overstrand_list
        output: 2d list of lists where the rows represent a crossing. to
                find the DLN of a knot there must be an even number of 
                crossings, but if there originally was an odd number of
                that means the last crossing was a loop added 
                have 3 ones representing the three strands that meet at a
                different crossing
    """
    # list of positions in the matrix where we want a 1
    index_list = []

    # number of strands in the knot
    num_strand = len(overstrand_list)

    # starting matrix of all 0s
    knot_matrix = [[0]*num_strand for i in range(num_strand)]
    #print("STARTING MATRIX")
    #print(knot_matrix)

    # if we have six strands, the last column of the matrix will be labelled 5 by the computer
    last_index = num_strand-1

    # see if knot loops over itself (extra loop for odd # crossings)
    if last_index == overstrand_list[last_index]:
        # for each column, 
        for i in range(num_strand-1):
            index_list.append([(i,i),(i,i+1),(i,overstrand_list[i])])
        index_list.append([(last_index,0),(last_index,overstrand_list[last_index]),(last_index,overstrand_list[last_index])])
    else:
        for i in range(num_strand):
            index_list.append([(i,i%num_strand),(i,(i+1)%num_strand),(i,overstrand_list[i])])
    #print("INDEX LIST")
    #print(index_list)

    #print(knot_matrix[0])

    for row in index_list:
        #print("ROW")
        #print(row)
        for index in row:
            #print("INDEX")
            #print(index)
            #print(index[0])
            #print(index[1])
            #print(knot_matrix)
            #print(knot_matrix[index[0]][index[1]])
            #knot_matrix[0][1] = 1
            knot_matrix[index[0]][index[1]] += 1
            #print(knot_matrix[index[0]])
    return knot_matrix


#print(six_one)

#print('The dictionary for 6-1 '+str(create_matrix(six_one)))
#print('The dictionary for 3-1 '+str(create_matrix(three_one)))
#print('The dictionary for 7-4 '+str(create_matrix(seven_four)))
#print('The dictionary for 7-7  '+str(create_matrix(seven_seven)))
#print('The dictionary for 8-5  '+str(create_matrix(eight_five)))
#print('The dictionary for 8-10  '+str(create_matrix(eight_ten)))


# fields = [ 'Name', 'Overstrand List']

# newfields = [ 'Name', 'Coloring Matrix']

# filename = "name_overstrand1_3colorable.csv"

# line_count = 0

# rawfile = open(filename, 'r')

# reader = csv.reader(rawfile)

# new_LoL = []
 
# for row in reader:
#     if line_count == 0:
#         new_LoL.append(newfields)
#         line_count = line_count + 1
#     else:
#         strings = row[1][1:-1].split(",")
#         print(strings)
#         #list_of_lists = [ list(crossing.split(",")) for crossing in strings ]
#         #print(list_of_lists)
#         list_of_intlists = [int(n) for n in strings]
#         print(list_of_intlists)
#         new_LoL.append([row[0],create_matrix( list_of_intlists )])
#         line_count = line_count + 1

# rawfile.close()



# newfilename = "name_matrix1_3colorable.csv"

# newrawfile = open(newfilename, 'w')

# writer = csv.writer(newrawfile)

# for row in new_LoL:
#     writer.writerow(row)

# newrawfile.close()














