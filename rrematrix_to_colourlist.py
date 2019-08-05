import csv

#Makes a list of color lists that are valid for the knot, given the row reduced matrix for the strands. 
def ColourList(matrix):
    #get number of rows as a variable and initialize lists for later. 
    number_rows = len(matrix)

    colourlists = []
    colours = []
    pivots = []
    free_variables = []
    free_var_names = []

    #Loop through each of the rows
    for i in range(number_rows):
        #set a flag for when a pivot is in the row. 
        pivot_found = False
        
        #Loop through each of the columns within the row
        for j in range( len( matrix[i] ) ):
            #If we haven't found a pivot yet, keep going further right
            if pivot_found == False:
                #If the value of this entry isn't 0, it's the pivot!
                if matrix[i][j] > 0:
                    #Add the location of the entry to our list pivots. 
                    pivot_location = j
                    pivots.append(pivot_location)
                    pivot_found = True
                    
                    
    #Go through each of the variables (rows). 
    #If the variable doesn't have a pivot, it is a free variable. Add to the list of free variables.
    for i in range(number_rows):
        if i not in pivots:
            free_variables.append(i)
    #jack do this :(   
    #<|(:3)
    colour_dict ={}
    for k in range( len( free_variables ) ):
        colour_dict[free_variables[k]] = k%3
    
    for i in range(len(pivots)):
        colour = 0
        row = matrix[i]
        for column in range(len(row)):
            if column not in pivots:
                colour -= row[column]*colour_dict[column]
        colour = colour%3
        colour_dict[pivots[i]] = colour
        
    for i in range(len(matrix)):
        colours.append(colour_dict[i]+1)

    colourlists.append(colours)
    
    if len(free_variables) == 3:
        free_colours = [[0,0,1],[0,1,0],[1,0,0]]

        for i in range(3):
            colour_dict ={}
            colours = []
            combination = free_colours[i]
            for j in range(3):
                colour_dict[free_variables[j]] = combination[j]

            for i in range(len(pivots)):
                colour = 0
                row = matrix[i]
                for column in range(len(row)):
                    if column not in pivots:
                        colour -= row[column]*colour_dict[column]
                colour = colour%3
                colour_dict[pivots[i]] = colour
                
            for i in range(len(matrix)):
                colours.append(colour_dict[i]+1)

            colourlists.append(colours)    
        
    return colourlists

#testing
#print( ColourList([[1, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 1, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 1, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 1, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 1, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 1, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))


#Edit csv files. 
fields = [ 'Name', 'Row Reduced Coloring Matrix']

newfields = [ 'Name', 'Color List']

filename = "name_reducedmatrix1_3colorable.csv"

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
        new_LoL.append([row[0],ColourList( list_of_intlists )])
        line_count = line_count + 1

rawfile.close()



newfilename = "name_colorlist_3colorable.csv"

newrawfile = open(newfilename, 'w')

writer = csv.writer(newrawfile)

for row in new_LoL:
    writer.writerow(row)

newrawfile.close()
