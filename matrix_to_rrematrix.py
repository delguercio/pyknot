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
        #for row in M:
        #    print(row)

        #print()
 
 
mtx4_1 = [[1,1,0,1],[0,1,1,1],[1,1,1,0],[1,0,1,1]]
mtx = [[1,0,1,1,0],[1,1,0,1,0],[0,1,0,1,1],[0,1,1,0,1],[1,0,1,0,1]]
 
print(ToReducedRowEchelonForm( mtx ))


#print(mtx)
#for row in mtx:
#    print(row)





