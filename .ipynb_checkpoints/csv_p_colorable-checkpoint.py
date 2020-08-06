
import csv


from colorings import *

from braid_to_gauss import *
from gauss_to_overstrand import *
from gauss_to_signlist import *
from matrix_to_rrematrix import *
from rrematrix_to_colourlist import *
from overstrand_to_matrix import *

from matrix_to_dln import *

import math



primes_used = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 313, 353]

"""
uc2 = "gauss"

for colorings in primes_used:

    ### Gauss to DLN

    fields = [ 'Name', 'Gauss Notation']

    newfields = [ 'Name', 'Dihedral Linking Numbers']
    
    filename = "./data/name_gaussfrom"+uc2+"_"+str(colorings)+"colorable.csv"

    line_count = 0

    rawfile = open(filename, 'r')

    reader = csv.reader(rawfile)

    gauss_code = []

    new_LoL = []
    
    for row in reader:
        if line_count == 0:
            new_LoL.append(newfields)
            line_count = line_count + 1
        else:
            strings = list(row[1][1:-1].split(","))
            gauss_code = [ int(number) for number in strings ]
            dln = gauss_to_dln( gauss_code , colorings )
            new_LoL.append([row[0], dln])
            line_count = line_count + 1 
            
    rawfile.close()

    newfilename = "./data/name_dlnfrom"+uc2+"_"+str(colorings)+"colorable.csv"

    newrawfile = open(newfilename, 'w')

    writer = csv.writer(newrawfile)

    for row in new_LoL:
        writer.writerow(row)

    newrawfile.close()    
"""

uc2 = "braid"

for colorings in primes_used:

    ### Gauss to DLN

    fields = [ 'Name', 'Gauss Notation']

    newfields = [ 'Name', 'Dihedral Linking Numbers']
    
    filename = "./data/name_braid_"+str(colorings)+"colorable.csv"

    line_count = 0

    rawfile = open(filename, 'r')

    reader = csv.reader(rawfile)

    braid = []

    new_LoL = []
    
    for row in reader:
        if line_count == 0:
            new_LoL.append(newfields)
            line_count = line_count + 1
        else:
            mult_braids = list(row[1][1:-1].split("},{"))
            for string in mult_braids:
                strings = list(string.split(","))
                braid = [ int(number) for number in strings ]
                dlns = braid_to_dln( braid , colorings )
            new_LoL.append([row[0], dln])
            line_count = line_count + 1 
            
    rawfile.close()

    newfilename = "./data/name_dlnfrom"+uc2+"_"+str(colorings)+"colorable.csv"

    newrawfile = open(newfilename, 'w')

    writer = csv.writer(newrawfile)

    for row in new_LoL:
        writer.writerow(row)

    newrawfile.close()    
    

""" 
    
    ##### gauss to overstrand no loop
    
    fields = [ 'Name', 'Gauss Notation']

    newfields = [ 'Name', 'Overstrand List']

    filename = "./data/name_gaussfrom"+uc2+"_"+str(colorings)+"colorable.csv"

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
            overstrands = create_overstrand_list( list_of_ints )
            new_LoL.append([row[0],overstrands])
            line_count = line_count + 1

    rawfile.close()

    newfilename = "./data/name_overstrandfrom"+uc2+"_"+str(colorings)+"colorable.csv"

    newrawfile = open(newfilename, 'w')

    writer = csv.writer(newrawfile)

    for row in new_LoL:
        writer.writerow(row)

    newrawfile.close()



    ##### overstrand to matrix

    fields = [ 'Name', 'Overstrand List']

    newfields = [ 'Name', 'Coloring Matrix']

    filename = "./data/name_overstrandfrom"+uc2+"_"+str(colorings)+"colorable.csv"

    

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
            #print(list_of_intlists)
            new_LoL.append([row[0],create_matrix( list_of_intlists ,int(colorings))])
            line_count = line_count + 1

    rawfile.close()

    newfilename = "./data/name_matrixfrom"+uc2+"_"+str(colorings)+"colorable.csv"

    newrawfile = open(newfilename, 'w')

    writer = csv.writer(newrawfile)

    for row in new_LoL:
        writer.writerow(row)

    newrawfile.close()


    #### matrix to RREM

    fields = [ 'Name', 'Coloring Matrix']

    newfields = [ 'Name', 'Row Reduced Coloring Matrix']

    filename = "./data/name_matrixfrom"+uc2+"_"+str(colorings)+"colorable.csv"

    newfilename = "./data/name_reducedmatrixfrom"+uc2+"_"+str(colorings)+"colorable.csv"

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
            #print(strings)
            list_of_lists = [ list(crossing.split(",")) for crossing in strings ]
            #print(list_of_lists)
            list_of_intlists = [ [int(n) for n in string] for string in list_of_lists ]
            rre_matrix = ToReducedRowEchelonForm( list_of_intlists , int(colorings))
            print(rre_matrix)
            new_LoL.append([row[0],rre_matrix ])
            line_count = line_count + 1

    rawfile.close()

    newrawfile = open(newfilename, 'w')

    writer = csv.writer(newrawfile)

    for row in new_LoL:
        writer.writerow(row)

    newrawfile.close() 

    ### RRE to colorlist

    fields = [ 'Name', 'Row Reduced Coloring Matrix']

    newfields = [ 'Name', 'Color List']

    filename = "./data/name_reducedmatrixfrom"+uc2+"_"+str(colorings)+"colorable.csv"

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
    #        print(strings)
            list_of_lists = [ list(crossing.split(",")) for crossing in strings ]
    #        print(list_of_lists)
            list_of_intlists = [ [int(n) for n in string] for string in list_of_lists ]
            list_of_colorlists = ColourList( list_of_intlists ,int(colorings) )
            if len(list_of_colorlists[0])%2 == 0:
                new_LoL.append([row[0],list_of_colorlists])
                line_count = line_count + 1
            else:
                for i in range(len(list_of_colorlists)):
                    zeroth_color = list_of_colorlists[i][0]
                    list_of_colorlists[i].append(zeroth_color)
                new_LoL.append([row[0],list_of_colorlists])
                line_count = line_count + 1            


    rawfile.close()


    newfilename = "./data/name_colorlistfrom"+uc2+"_"+str(colorings)+"colorable.csv"

    newrawfile = open(newfilename, 'w')

    writer = csv.writer(newrawfile)

    for row in new_LoL:
        writer.writerow(row)

    newrawfile.close()
"""



