




primes_used = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 313, 353]

for uc2 in primes_used:
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