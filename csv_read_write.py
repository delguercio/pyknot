


import csv


from colorings import *

from braid_to_gauss import *
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
    print("")
    print("(1) braid -> sign list")
    print("(2) braid -> gauss")
    print("(3) gauss -> sign list")
    print("(4) gauss -> overstrand list")
    print("(5) overstrand list -> matrix")
    print("(6) matrix -> rre matrix")
    print("(7) rre matrix -> color list")
    print("(8) generate all_fields")
    print("(9) dihedral linking number")
    print("(10) exit")    
    print("Enter your choice:")

def submenu():
    """
    """
    print("")
    print("(1) add a loop when there is an odd number of crossings")
    print("(2) do not add a loop")

def main():
    """ the main user-interaction loop 
    """
    uc2 = str(input("Type braid or gauss depending on what you're doing:  "))
    colorings = str(input("How many colors are we working with?"))
    while True:     # the user-interaction loop
        menu()
        uc = int(input( "Choose an option: "))

        if uc == 1: # Braid to signlist

            fields = [ 'Name', 'Braid Notation']

            newfields = [ 'Name', 'Sign List']

            filename = "./data/name_braid_"+colorings+"colorable.csv"

            line_count = 0

            rawfile = open(filename, 'r')

            reader = csv.reader(rawfile)

            new_LoL = []
             
            for row in reader:
                if line_count == 0:
                    new_LoL.append(newfields)
                    line_count = line_count + 1
                else:
                    #print(line_count)
                    #print(row[0])
                    strings = list(row[1][1:-1].split(","))
                    #print(strings)
                    list_of_ints = [ int(number) for number in strings ]
                    signs = BraidToSigns( list_of_ints )
                    if len(signs)%2 == 0:
                        new_LoL.append([row[0],signs])
                        line_count = line_count + 1
                    else:
                        pos_crossing = signs + [1]
                        new_LoL.append([row[0],pos_crossing])
                        line_count = line_count + 1   

            rawfile.close()

            newfilename = "./data/name_signfrom"+uc2+"_"+colorings+"colorable.csv"

            newrawfile = open(newfilename, 'w')

            writer = csv.writer(newrawfile)

            for i in range(len(new_LoL)):
                writer.writerow(new_LoL[i])

            newrawfile.close()


        elif uc == 2: # Braid to Gauss

            fields = [ 'Name', 'Braid Notation']

            newfields = [ 'Name', 'Gauss Notation']

            filename = "./data/name_braid_"+colorings+"colorable.csv"

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
                    #print(strings)
                    list_of_ints = [ int(number) for number in strings ]
                    gauss = BraidToGauss( list_of_ints )
                    new_LoL.append([row[0],gauss])
                    line_count = line_count + 1 

            rawfile.close()

            newfilename = "./data/name_gaussfrom"+uc2+"_"+colorings+"colorable.csv"

            newrawfile = open(newfilename, 'w')

            writer = csv.writer(newrawfile)

            for row in new_LoL:
                writer.writerow(row)


            newrawfile.close()


        elif uc == 3:  # gauss -> sign list
            fields = [ 'Name', 'Gauss Notation']

            newfields = [ 'Name', 'Sign List']

            filename = "./data/name_gaussfrom"+uc2+"_"+colorings+"colorable.csv"

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


            newfilename = "./data/name_signfrom"+uc2+"_"+colorings+"colorable.csv"

            newrawfile = open(newfilename, 'w')

            writer = csv.writer(newrawfile)

            for row in new_LoL:
                writer.writerow(row)

            newrawfile.close()



        elif uc == 4: # gauss -> overstrand list
                submenu()
                subuc = int(input( "Choose an option: "))

                if subuc == 1: #

                    fields = [ 'Name', 'Gauss Notation']

                    newfields = [ 'Name', 'Overstrand List']

                    filename = "./data/name_gaussfrom"+uc2+"_"+colorings+"colorable.csv"

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
                            last_index = len(overstrands)
                            if len(overstrands)%2 == 0:
                                new_LoL.append([row[0],overstrands])
                                line_count = line_count + 1
                            else:
                                pos_crossing = overstrands + [last_index]
                                new_LoL.append([row[0],pos_crossing])
                                line_count = line_count + 1   

                    rawfile.close()

                    newfilename = "./data/name_overstrandfrom"+uc2+"_"+colorings+"colorable.csv"

                    newrawfile = open(newfilename, 'w')

                    writer = csv.writer(newrawfile)

                    for row in new_LoL:
                        writer.writerow(row)

                    newrawfile.close()

                elif subuc == 2: # do not add loop

                    fields = [ 'Name', 'Gauss Notation']

                    newfields = [ 'Name', 'Overstrand List']

                    filename = "./data/name_gaussfrom"+uc2+"_"+colorings+"colorable.csv"

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

                    newfilename = "./data/name_overstrandfrom"+uc2+"_"+colorings+"colorable.csv"

                    newrawfile = open(newfilename, 'w')

                    writer = csv.writer(newrawfile)

                    for row in new_LoL:
                        writer.writerow(row)

                    newrawfile.close()

                else:
                    print("not an option")
                    break



        elif uc == 5: # overstrand -> matrix
            fields = [ 'Name', 'Overstrand List']

            newfields = [ 'Name', 'Coloring Matrix']

            filename = "./data/name_overstrandfrom"+uc2+"_"+colorings+"colorable.csv"

            

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

            newfilename = "./data/name_matrixfrom"+uc2+"_"+colorings+"colorable.csv"

            newrawfile = open(newfilename, 'w')

            writer = csv.writer(newrawfile)

            for row in new_LoL:
                writer.writerow(row)

            newrawfile.close()

        elif uc == 6:  #  matrix -> rre matrix
            
            fields = [ 'Name', 'Coloring Matrix']

            newfields = [ 'Name', 'Row Reduced Coloring Matrix']

            filename = "./data/name_matrixfrom"+uc2+"_"+colorings+"colorable.csv"

            newfilename = "./data/name_reducedmatrixfrom"+uc2+"_"+colorings+"colorable.csv"

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


        elif uc == 7: # rre matrix -> color list
            fields = [ 'Name', 'Row Reduced Coloring Matrix']

            newfields = [ 'Name', 'Color List']

            filename = "./data/name_reducedmatrixfrom"+uc2+"_"+colorings+"colorable.csv"

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


            newfilename = "./data/name_colorlistfrom"+uc2+"_"+colorings+"colorable.csv"

            newrawfile = open(newfilename, 'w')

            writer = csv.writer(newrawfile)

            for row in new_LoL:
                writer.writerow(row)

            newrawfile.close()

        elif uc == 8: # generate all_fields


             #             0            1                  2              3             4            5

            newfields = [ 'Name','Gauss Notation', 'Overstrand List', 'Sign List', 'Color List', 'Dihedral Linking Number' ]



            # 0-1
            gauss_fields = [ 'Name', 'Gauss Notation']

            gauss_filename = "./data/name_gaussfrom"+uc2+"_"+colorings+"colorable.csv"

            gauss_rawfile = open(gauss_filename, 'r')

            gauss_reader = csv.reader(gauss_rawfile)

            # 2
            overstrand_fields = [ 'Name', 'Overstrand List']

            overstrand_filename = "./data/name_overstrandfrom"+uc2+"_"+colorings+"colorable.csv"

            overstrand_rawfile = open(overstrand_filename, 'r')

            overstrand_reader = csv.reader(overstrand_rawfile)

            # 3
            sign_fields = [ 'Name', 'Sign List']

            sign_filename = "./data/name_signfrom"+uc2+"_"+colorings+"colorable.csv"

            sign_rawfile = open(sign_filename, 'r')

            sign_reader = csv.reader(sign_rawfile)


            # 4
            colorlist_fields = [ 'Name', 'Color List']

            colorlist_filename = "./data/name_colorlistfrom"+uc2+"_"+colorings+"colorable.csv"

            colorlist_rawfile = open(colorlist_filename, 'r')

            colorlist_reader = csv.reader(colorlist_rawfile)



            line_count = 0

            new_LoL = []

            for row in gauss_reader:
                if line_count == 0:
                    new_LoL.append(newfields)
                    line_count = line_count + 1
                else:
                    new_LoL.append(row)
                    line_count = line_count + 1
                    
            gauss_rawfile.close()
            
            line_count = 0
            for row in overstrand_reader:
                if line_count == 0:
                    line_count += 1
                    continue
                else:
                    overstrand_list_listofstrings = row[1][1:-1].split(",")
                    overstrand_list = [ int(string) for string in overstrand_list_listofstrings ]
                    new_LoL[line_count].append(overstrand_list)
                    line_count = line_count + 1

            overstrand_rawfile.close()
            
            
            line_count = 0
            for row in sign_reader:
                if line_count == 0:
                    line_count += 1
                    continue
                else:
                    sign_list_listofstrings = row[1][1:-1].split(",")
                    sign_list = [ int(string) for string in sign_list_listofstrings ]
                    new_LoL[line_count].append(sign_list)
                    line_count = line_count + 1                  

            sign_rawfile.close()

            line_count = 0
            for row in colorlist_reader:
                if line_count == 0:
                    line_count += 1
                    continue
                else:
                    color_list_listofstrings = row[1][2:-2].split("], [")
                    color_list_listoflists = [ list(crossing.split(", ")) for crossing in color_list_listofstrings ]
                    color_lists = [ [int(n) for n in string] for string in color_list_listoflists ]
                    #print("COLOR LIST")
                    new_LoL[line_count].append(color_lists)
                    line_count = line_count + 1 

            colorlist_rawfile.close()


            newfilename = "./data/allfieldsfrom"+uc2+"_"+colorings+"colorable.csv"

            newrawfile = open(newfilename, 'w')

            writer = csv.writer(newrawfile)

            for row in new_LoL:
                writer.writerow(row)

            newrawfile.close()

        elif uc == 9: # dihedral linking number
            #            0            1                  2              3             4            5

            fields = [ 'Name','Gauss Notation', 'Overstrand List', 'Sign List', 'Color List', 'Dihedral Linking Number' ]

            newfields = [ 'Name', 'Dihedral Linking Number' ]

            filename = "./data/allfieldsfrom"+uc2+"_"+colorings+"colorable.csv"

            line_count = 0

            

            rawfile = open(filename, 'r')

            reader = csv.reader(rawfile)

            dihedral_linking_numbers = []

            new_LoL = []
             
            for row in reader:
                if line_count == 0:
                    new_LoL.append(newfields)
                    line_count = line_count + 1
                else:
                    color_list_listofstrings = row[4][2:-2].split("], [")
                    color_list_listoflists = [ list(crossing.split(", ")) for crossing in color_list_listofstrings ]
                    color_lists = [ [int(n) for n in string] for string in color_list_listoflists ]
                    #print("COLOR LIST")
                    #print(color_lists)
                    
                    overstrand_list_listofstrings = row[2][1:-1].split(",")
                    overstrand_list = [ int(string) for string in overstrand_list_listofstrings ]
                    #print("OVERSTRAND LIST")
                    #print(overstrand_list)


                    sign_list_listofstrings = row[3][1:-1].split(",")
                    sign_list = [ int(string) for string in sign_list_listofstrings ]
                    #print("SIGN LIST")
                    #print(sign_list)      

                    for i in range(len(color_lists)):
                        dihedral_linking_numbers.append(display( sign_list, overstrand_list, row[0], color_lists[i] ))
                    
                    #print(new_LoL)
                    new_LoL.append([row[0],dihedral_linking_numbers])
                    dihedral_linking_numbers = []
                    
                    line_count = line_count + 1

            rawfile.close()

            newfilename = "./data/name_DLNfrom"+uc2+"_"+colorings+"colorable.csv"

            newrawfile = open(newfilename, 'w')

            writer = csv.writer(newrawfile)

            for row in new_LoL:
                writer.writerow(row)

            newrawfile.close()

        elif uc == 10:
            break

        else:
            print("That's not on the menu!")

    print(" ")
    print(" ")
    print(" exiting ")
    print("         .")
    print("           . ")
    print("             . ")
    print(" ")
    print(" ")

main()

