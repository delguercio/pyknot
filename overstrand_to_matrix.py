

###############################################################
## overstrand_to_matrix.py                                   ##
##                                                           ##
## Created by: Olivia Del Guercio (delgur@gmail.com)         ##
##                 & Hana Sambora                            ##
## First Created: 6/30/19                                    ##
## Last Modified: 8/5/19                                     ##
###############################################################

#
#
# This program goes from the output of gauss_to_overstrand.py (i.e. the overstrand list)
# to a matrix that represents the strands at each crossing of the knot that will then
# be row reduced mod three to find all of the valid crossings.
#
# If you want to know more about this you can look at the Section 3.3 (3-colourings) of
# http://www.math.ucsd.edu/~justin/Roberts-Knotes-Jan2015.pdf
#
# In the end the matrix will have the columns represent the strands and the rows represent
# crossings. At a given crossing, we will add one to each column with a strand there.
# So the trefoil for example:
#
#                   [[1,1,1,0],
#       [2,0,1,3] -> [1,1,1,0],
#                    [0,1,1,1],
#                    [1,0,0,2]]
#
#

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
        first makes a list of lists of tuples that
        specify where we want to add the 1's later in the program
        at the ith crossing (that is not a loop) the three strands represented are
            [(i,i),(i,i+1),(i,overstrand[i])]
        at the ith crossing (that IS a loop) the three strands represented are
            [(i,i),(i,i+1),(i,overstrand[i])]
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

    # initialize matrix
    knot_matrix = [[0]*num_strand for i in range(num_strand)]
    #print("STARTING MATRIX")
    #print(knot_matrix)

    last_index = num_strand-1 

    # if knot contains a loops at the end
    if last_index == overstrand_list[last_index]:
        for i in range(num_strand-1): # do not go to the last index
            index_list.append([(i,i),(i,i+1),(i,overstrand_list[i])])
        # if the last index of the loop is guarenteed to have the 0th strand, and then the last strand twice
        index_list.append([(last_index,0),(last_index,overstrand_list[last_index]),(last_index,overstrand_list[last_index])])
    else:
    #if the knot does not contain a loop at the end
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
            knot_matrix[index[0]][index[1]] += 1
    return knot_matrix

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













