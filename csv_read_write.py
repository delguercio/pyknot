


import csv


#
#   read csv in 
#   for line in csv run program
#   


#
# this didn't work so i just put the functions in :/
#

from gauss_to_overstrand import *

def ToReducedRowEchelonForm( M):
    if not M: return M
    lead = 0 # col index
    rowCount = len(M) # num rows in M
    columnCount = len(M[0]) # num col in M
    for r in range(lead, rowCount): #r is row index
        if lead >= columnCount:  #if col index reaches end, return column
            return M
        i = r #
        while M[i][lead] == 0: #if the value is already 0, move to the next row
            i += 1
            if i == rowCount: #we reached the last row
                i = r
                lead += 1
                if columnCount == lead: #we reached the last column
                    return M
        #print("r is"+str(r))
        #print("i is"+str(i))
        #print("lead is"+str(lead))
        #print("M is"+str(M))
        M[i],M[r] = M[r],M[i] #swap two different rows (reassigning two vars at once)
        #print("M is swapped"+str(M))
        lv = M[r][lead] 
        if lv == 2: #if the lead value is two, double the row and take mod 3
        #print("lead value is"+str(lv))
            M[r] = [ (mrx*2)%3 for mrx in M[r]]
       # print("M row r is divided by lv"+str(M))
        for i in range(rowCount):
            if i != r: #everything below the lead value will be taken care of in the step
                lv = M[i][lead]
                #print("lv is"+str(lv))
               # print("you take"+str(M[i])+"and subtract"+str(M[r])+"times lv")
                M[i] = [ (iv - lv*rv)%3 for rv,iv in zip(M[r],M[i])]
              #  print("M is "+str(M))
        lead += 1
    return M
"""

fields = [ 'Name', 'Coloring Matrix']

newfields = [ 'Name', 'Row Reduced Coloring Matrix']

filename = "name_matrix1_3colorable.csv"

line_count = 0

rawfile = open(filename, 'r')

reader = csv.reader(rawfile)

new_LoL = []
 
for row in reader:
    if line_count == 0:
        new_LoL.append(newfields)
        line_count = line_count + 1
    else:
        strings = row[1][2:-2].split("], [")
        print(strings)
        list_of_lists = [ list(crossing.split(",")) for crossing in strings ]
        print(list_of_lists)
        list_of_intlists = [ [int(n) for n in string] for string in list_of_lists ]
        new_LoL.append([row[0],ToReducedRowEchelonForm( list_of_intlists )])
        line_count = line_count + 1

rawfile.close()



newfilename = "name_reducedmatrix1_3colorable.csv"

newrawfile = open(newfilename, 'w')

writer = csv.writer(newrawfile)

for row in new_LoL:
    writer.writerow(row)

newrawfile.close()

def create_dict(gauss_code_list):

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

    gauss_code_dict = create_dict(gauss_code_list)
    #print(gauss_code_dict)
    overstrand_list = []
    for key,val in gauss_code_dict.items():
        lookingfor = val[-1]
        #print("I'm looking for "+str(lookingfor)+" in the Gauss Code")
        keys = [key for key, value in gauss_code_dict.items() if (-1)*lookingfor in value]
        #print("The corresponding strand is "+str(keys))
        #print(gauss_code_dict.items())
        overstrand_list.append(keys[0])
    if len(overstrand_list)%2 == 1:
        overstrand_list.append(len(overstrand_list))
    return overstrand_list
"""

fields = [ 'Name', 'Gauss Code']

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
        strings = row[1][1:-1].split(",")
        #print(strings)
        #list_of_lists = [ list(crossing.split(",")) for crossing in strings ]
        #print(list_of_lists)
        list_of_intlists = [int(n) for n in strings]
        print(list_of_intlists)
        new_LoL.append([row[0],create_overstrand_list( list_of_intlists )])
        line_count = line_count + 1

rawfile.close()



newfilename = "name_overstrand_3colorable.csv"

newrawfile = open(newfilename, 'w')

writer = csv.writer(newrawfile)

for row in new_LoL:
    writer.writerow(row)

newrawfile.close()

