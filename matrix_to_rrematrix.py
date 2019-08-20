
#
# This program is edited from https://rosettacode.org/wiki/Reduced_row_echelon_form#Python
# The difference is that our row reduction works in mod p, if we are working to p-color a knot
# where p is a prime number. It doesn't work for all odd... yet.
#
# Edited by Jack to include inverses and mod 
#


def ToReducedRowEchelonForm(M, p):
    """
        input: matrix from overstrand_to_matrix.py
        output: reduced row eschelon matrix mod p
    """
    inverses = {}
    for i in range(p):
        for inverse in range(p):
            if (i*inverse)%p == 1:
                inverses[i] = inverse
            
    if not M: return
    lead = 0 # col index
    rowCount = len(M) # num rows in M
    columnCount = len(M[0]) # num col in M
    for r in range(lead, rowCount): #r is row index
        if lead >= columnCount:  #if col index reaches end, return column
            return
        i = r #
        while M[i][lead] == 0: #if the value is already 0, move to the next row
            i += 1
            if i == rowCount: #we reached the last row
                i = r
                lead += 1
                if columnCount == lead: #we reached the last column
                    return

        M[i],M[r] = M[r],M[i] #swap two different rows (reassigning two vars at once)
        lv = M[r][lead] 
        if lv != 1: #if the lead value isn't one, multiply the row by lv inverse and take mod n    
            M[r] = [ (mrx*inverses[lv])%p for mrx in M[r] ]
        for i in range(rowCount):
            if i != r: #everything below the lead value will be taken care of in the step
                lv = M[i][lead]
                M[i] = [ (iv - lv*rv)%p for rv,iv in zip(M[r],M[i]) ]
        lead += 1
 
 
#mtx4_1 = [[1,1,0,1],[0,1,1,1],[1,1,1,0],[1,0,1,1]]
#mtx = [[1,0,1,1,0],[1,1,0,1,0],[0,1,0,1,1],[0,1,1,0,1],[1,0,1,0,1]]
 
#ToReducedRowEchelonForm(mtx, 3)

#print(mtx)







