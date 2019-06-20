def ColourList(matrix):

    alphabet = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" ]
    number_rows = len(matrix)

    colours = []
    free_variables = []
    free_var_names = []

    alphabet = alphabet[0:len(matrix)]

    for i in range( len( alphabet ) ):
        vars()[alphabet[i]] = 0
        
    for i in range(number_rows):
        print( "we are on row number ", i+1 )
        print( matrix[i] )
        vars()["not_zero_things"+"_"+alphabet[i]] = []
        
        for j in range( len( matrix[i] ) ):
            
            pivot_location = 0
            if j == i :
                print( "the pivot value is", matrix[i][j] )
                pivot_location = j

                if matrix[i][j] == 0 :
                    free_variables.append ( i )

            if j > i and matrix[i][j] != 0:
                #print( "wow we have a thing here", matrix[i][j], " for variable", j )
                vars()["not_zero_things"+"_"+alphabet[i]].append( j )

    for k in range( len( free_variables ) ):
        print( alphabet[free_variables[k]], "=", k ) 
        vars()[alphabet[free_variables[k]]] = k 

    print( "our free variable(s)! ", free_var_names )
    
    for i in range(number_rows):
        if matrix[i][i] != 0:
            print( alphabet[i], "=", end = " " )
            
            for num in range( len( vars()["not_zero_things"+"_"+alphabet[i]] ) ):
                free_var = vars()["not_zero_things"+"_"+alphabet[i]][num]
                #print( "free var", free_var )
                #print( "subtracting", matrix[i][free_var], "*", alphabet[free_var] )
                vars()[alphabet[i]] -= matrix[i][free_var]*vars()[alphabet[free_var]]
            vars()[alphabet[i]] = vars()[alphabet[i]]  % 3
            print( vars()[alphabet[i]] )
                
    print()
    print()
    
    for let in range( len( alphabet ) ):
        print( alphabet[let], "=", vars()[alphabet[let]] )
        colours.append( vars()[alphabet[let]] )
    print( colours )
    
matrix = [[1, 0, 0, 0, 2, 0], [0, 1, 0, 0, 1, 1], [0, 0, 1, 0, 0, 2], [0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

colours = ColourList(matrix)
print(colours)
