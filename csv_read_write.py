


import csv


from colorings import *


from gauss_to_overstrand import *
from gauss_to_signlist import *
from matrix_to_rrematrix import *
from rrematrix_to_colourlist import *
from overstrand_to_matrix import *

#
# Goal is just a streamline csv reading and writing.
# only need to specify:
#           file you are reading
#           the function you are applying
#           file you are writing
#

import math

def menu():
    """ 
    """
    print("(0) ")
    print("(1) csv read and write")
    print("(2) ")
    print("(3) ")
    print("(4) ")
    print("(5) ")
    print("(6) ")
    print("(7) ")
    print("(9) Quit")
    print(" ")    
    print("Enter your choice:")

def main():
    """ the main user-interaction loop 
    """

    while True:     # the user-interaction loop
        menu()
        uc = input( "Choose an option: " )

        if uc == 9: #
            break

        elif uc == 0:  #
            #L = input("Enter a new list: ")

        elif uc == 1:  #
            csv_read_write()

        elif uc == 2: # 
            print(" ")

        elif uc == 3: # 
            print(" ")

        elif uc == 4:
            print(" ")

        elif uc == 5:
            print(" ")

        elif uc == 6:
            print(" ")

        elif uc == 7:
            print(" ")

        else:
            print "That's not on the menu!"

    print(" ")
    print(" ")
    print(" exiting ")
    print("         .")
    print("           . ")
    print("             . ")
    print(" ")
    print(" ")


def 

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
        #print(strings)
        list_of_lists = [ list(crossing.split(",")) for crossing in strings ]
        #print(list_of_lists)
        list_of_intlists = [ [int(n) for n in string] for string in list_of_lists ]
        new_LoL.append([row[0],ToReducedRowEchelonForm( list_of_intlists )])
        line_count = line_count + 1

rawfile.close()



newfilename = "name_reducedmatrix_3colorable.csv"

newrawfile = open(newfilename, 'w')

writer = csv.writer(newrawfile)

for row in new_LoL:
    writer.writerow(row)

newrawfile.close()

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

