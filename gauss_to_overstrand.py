

#
# 
#


#
# I call the strand number for the overstrand list "strand #" 
# and numbering system for the Gauss code the "crossing index". 
#

#
# First creates a dictionary of the form 
#              {{strand #0: overcrossing index, ... , -undercrossing index} ,
#               {strand #1: overcrossing index, ... , -undercrossing index} ,
#               ... }


def create_dict(gauss_code_list):
    """
        input: gauss code list
        output:dictionary with the keys integer strand numbers between 0 and
               length of gauss code list divided by two. Each dictionary entry
               has value a list with at least one integer entry
               [overcrossing index, ... , -undercrossing index]
               which corresponds to that strand number 
        """
    strand_count = 0 # overstrand we are on
    knot_dict = {}   # intialize knot dictionary
    strand_indicies = [] # list of gauss code indicies that intersect a given overstrand
    for i in range(len(gauss_code_list)): # go through entire gauss code
        if gauss_code_list[i] < 0: # if we are at the understrand
            strand_indicies.append(gauss_code_list[i])  # add index to list
            knot_dict.update({strand_count:strand_indicies}) # update overstrand index dictionary
            strand_count += 1 # go to the next strand
            strand_indicies = [] # reset indicies
        else:
            strand_indicies.append(gauss_code_list[i]) # if we are an overstrand, add gauss code index
                                                       # and continue
    for i in reversed(range(len(gauss_code_list))):        
        if gauss_code_list[i]>0: #if the last ones are positive, it's a part of strand 0
            knot_dict[0].insert(0,gauss_code_list[i])
        else: #not a part of strand 0
            break
    return knot_dict

def create_overstrand_list(gauss_code_list):
    """
        Goes through the dictionary in strand # key order (0,1, ...)
        searches for the overcrossing index corresponding to the undercrossing
        index of the strand. Adds key of the overcrossing index to list. Repeat.
        Return list.
        input: gauss code dictinary from create_dict(gauss_code_list)
        output: overstrand list to be input to colorings.py file
    """
    gauss_code_dict = create_dict(gauss_code_list)
    print(gauss_code_dict)
    overstrand_list = []
    for key,val in gauss_code_dict.items():
        lookingfor = val[-1]
        #print("I'm looking for "+str(lookingfor)+" in the Gauss Code")
        keys = [key for key, value in gauss_code_dict.items() if (-1)*lookingfor in value]
        #print("The corresponding strand is "+str(keys))
        #print(gauss_code_dict.items())
        overstrand_list.append(keys[0])
    #if len(overstrand_list)%2 == 1: # if you wanted to add a loop to in overstrand
    #    overstrand_list.append(len(overstrand_list))
    return overstrand_list


three_one = [1, -2, 3, -1, 2, -3,4,-4]
four_one = [-1, 2, -3, 1, -4, 3, -2, 4]
six_one = [1,-2,3,-4,2,-1,5,-6,4,-3,6,-5]
seven_four = [-1, 2, -3, 4, -5, 6, -7, 3, -2, 1, -4, 7, -6, 5]
seven_seven = [1, -2, 3, -4, 5, -6, 4, -7, 2, -1, 7, -3, 6, -5]
eight_five = [1, -2, 3, -4, 5, -1, 2, -3, 6, -7, 8, -5, 4, -6, 7, -8]
eight_ten = [-1, 2, -3, 4, -5, 6, -7, 8, -4, 5, -6, 1, -2, 7, -8, 3]
eight_eleven = [1, -2, 3, -4, 5, -6, 7, -8, 2, -1, 8, -3, 6, -5, 4, -7]
eight_twenty =[1, -2, -3, 4, 5, -1, 2, -5, -6, 7, -8, 6, -4, 3, -7, 8]
eleven_n_one =[-1, 2, -3, 1, -4, 5, -6, 3, -2, 4, 7, -8, 9, 6, -5, -7, 10, -11, 8, -9, 11, -10]

#print(six_one)
"""
print('The overstrand list for 6-1 is '+str(create_overstrand_list(six_one)))#
print('The overstrand list for 3-1 is '+str(create_overstrand_list(three_one)))
print('The overstrand list for 7-4 is '+str(create_overstrand_list(seven_four)))
print('The overstrand list for 7-7 is '+str(create_overstrand_list(seven_seven)))
print('The overstrand list for 8-5 is '+str(create_overstrand_list(eight_five)))
print('The overstrand list for 8-10 is '+str(create_overstrand_list(eight_ten)))
print('The overstrand list for 11n-1 is '+str(create_overstrand_list(eleven_n_one)))
"""
print(create_overstrand_list(three_one))

fields = [ 'Name', 'Gauss Notation']

newfields = [ 'Name', 'Overstrand List']

filename = "name_gauss_3colorable.csv"

line_count = 0

rawfile = open(filename, 'r')

reader = csv.reader(rawfile)

new_LoL = []
 
for row in reader:
    if line_count == 0:
        new_LoL.append(newfields)
        line_count = line_count + 1
    else:
        strings = list(row[1][1:-1].split(","))
        list_of_ints = [ int(number) for number in strings ]
        signs = SignList( list_of_ints )
        if len(signs)%2 == 0:
            new_LoL.append([row[0],signs])
            line_count = line_count + 1
        else:
            pos_crossing = signs + [1]
            new_LoL.append([row[0],pos_crossing])
            line_count = line_count + 1            

rawfile.close()

newfilename = "name_overstrand_3colorable.csv"

newrawfile = open(newfilename, 'w')

writer = csv.writer(newrawfile)

for row in new_LoL:
    writer.writerow(row)

newrawfile.close()
