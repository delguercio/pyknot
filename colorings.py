# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# A crossing is an ordered pair of integers.  
# The first is the sign of the crossing, which is +1 or -1
# The second is an integer between 0 and c-1 inclusive where c is the number of crossings.
# This second integer tells you the over-arc.
# Indexing starts at 0 so we label the crossings from 0 to c-1

from sympy import Matrix

import itertools



# A color is a number between 1 and 3.
# A coloring is a list of colors such that the ith crossing 
#is assigned to the ith color in the list.




# homog: Given a crossing i and a coloring check whether the colors at crossing i
# are all the same or all different, or neither

def homog(crossingindex,colorlist,numcrossings,overstrands):    
#    print('numcrossings is ',numcrossings)
#    print('crossingindex is ',crossingindex)
#    print('len(colorlist) is ', len(colorlist))
#    print('(crossingindex+1)%numcrossings is', (crossingindex+1)%numcrossings)
#    print('overstrands[crossingindex] is', overstrands[crossingindex])
    if (colorlist[crossingindex]!=colorlist[(crossingindex+1)%numcrossings]) and (colorlist[crossingindex]!=colorlist[overstrands[crossingindex]]) and (colorlist[(crossingindex+1)%numcrossings]!= colorlist[overstrands[crossingindex]]) :
        return 'd' #d for different (inhomogeneous)
    elif (colorlist[crossingindex]==colorlist[(crossingindex+1)%numcrossings]) and (colorlist[crossingindex]==colorlist[overstrands[crossingindex]]) and (colorlist[(crossingindex+1)%numcrossings]== colorlist[overstrands[crossingindex]]) :
        return 's' #s for same (homogeneous)
    else :
        return 'o' #o for other (invalid crossing)

# A coloring is valid if at each crossing all the colors are the same or all are different.
# valid: Check if a coloring is valid. Returns true if so, false otherwise

def valid(colorlist,numcrossings,overstrands):
    v='true'
    for index in range(0,numcrossings):
        #print('the current coloring is',colorlist)
        if (homog(index, colorlist,numcrossings,overstrands)=='o') :
            v='false'
    return v
            


# Look for all valid colorings and return a list of those colorings (list of lists)


#def findallcolorings(numcrossings,overstrands):
#    allcolorings=[]
#    for i in range(1,4):
#        for j in range(1,4):
#            for k in range(1,4):
#                for l in range(1,4):
#                    if valid([i,j,k,l],numcrossings,overstrands)=="true":
#                        allcolorings.append([i,j,k,l])
#    return allcolorings
    
def findallcolorings(numcrossings,overstrands):
    allcolorings=[]
    possibilities=list(itertools.product([1,2,3],repeat=numcrossings))
    total=len(possibilities)
    for i in range(0,total):
        #print('index in findallcolorings is', i)
        if valid(possibilities[i],numcrossings,overstrands)=='true':
            allcolorings.append(possibilities[i])
    return allcolorings
            
    


# WhereIsA2i tells you in which 3-cell you must stand so A_2i is right of A_3i
#when you stand on the degree 2 copy of the knot and face in the direction
#of its orientation
def WhereIsA2i(colorlist,overstrands,numcrossings):
    twist=[]
    #At crossing 0, we pick arbitrarily one of the two numbers which is not the color of xing 0.
    s=set()
    s.add(1)
    s.add(2)
    s.add(3)
    s.discard(colorlist[0])
    twist.append(s.pop())
# Now visit the crossings in order.
    for i in range(1,numcrossings):    
        #At each crossing check the overstrand's color.  If it is equal to the current
        # 3-cell number, then as you go through the crossing, that 3-cell is fixed.
        # Thus the 3-cell from which A_2i is on the right stays the same.
        if (twist[i-1]==colorlist[overstrands[(i-1)%numcrossings]]):
            twist.append(twist[i-1])
        # otherwise if the overstrand has color x and the current 3-cell is y, 
            # the 3-cell will change to z!=x,y after passing through the wall
        elif (twist[i-1]!=colorlist[overstrands[(i-1)%numcrossings]]):
            s=set()
            s.add(1)
            s.add(2)
            s.add(3)
            s.discard(twist[i-1])
            s.discard(colorlist[overstrands[(i-1)%numcrossings]])
            twist.append(s.pop())
    return twist




# x_i is the coefficient of A_2i-A_3i in the 2-chain A_11+...+A_1c+sum_i(x_i(A_2i-A3i))
# We compute the boundary of the above expression one crossing at a time.
# At crossing k the nonzero part of the boundary is a multiple of a_2i-a_3i and we 
# compute this multiple in terms of the x_i.  We record the coefficient of x_i
# at crossing k.

def computecoef(colorlist, numcrossings,overstrands, signs):
    n=numcrossings
    #The matrix A of coefficients in our system Ax=b
    coefmatrix= [[0 for x in range(n+1)] for x in range(n)] 
    for k in range(0,n):
        # Look at A_2k and A_3k                    
        #The contribution to the boundary is x_k(a_2-a_3) so we put a 1 in 
        #index k
        coefmatrix[k][k]+=1
        # Look at A_2(k+1) and A_3(k+1), where k+1 is taken mod c
        # The contribution is x_(k+1)(a_3-a_2) so we put -1 in 
        #index k+1 mod c
        coefmatrix[k][(k+1)%n]-=1
        # If the crossing k has 3 colors
        if (homog(k,colorlist,n,overstrands)=='d'):
            # print()
            # print("This crossing is heterogeneous")
            if (WhereIsA2i(colorlist,overstrands,n)[k]==colorlist[overstrands[k]]):
                # print("w(i) for i = ", k, " is ", WhereIsA2i(colorlist,overstrands,n)[k])
                # print("the overstrand is ", overstrands[k], " and its color is ", colorlist[overstrands[k]] )
                # print("w(i) is equal to color(overstrand)")
                #If the crossing is positive
                if (signs[k]==1):
                    # print("This crossing is positive")
                    # Look at A_2f(k) and A_3f(k)
                    # One contributes 0 and the other +/-(a_2-a_3)
                    # To determine sign, check whether the color of the incoming understrand
                    # (strand k) matches the number of the 3-cell from which A_2f(k)
                    # is on the right
                    #THIS IS EPSILON 1
                    if(WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]==colorlist[k]):
                        coefmatrix[k][overstrands[k]]-=1
                        # print("w(overstrand) equals color(i)")
                        
                    elif (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]!=colorlist[k]):
                        # print("w(overstrand) does not equal color(i)")
                        
                        coefmatrix[k][overstrands[k]]+=1           
                    #Look at A_1f(k)
                    
                    # print("the right side of the equation is negative 1")
                    coefmatrix[k][n]-=1
                elif (signs[k]==-1):
                    # print("this crossing is negative")
                    if(WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]==colorlist[k]):
                        coefmatrix[k][overstrands[k]]-=1    
                        # print("w(overstrand) equals color(i)")
                        
                    elif (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]!=colorlist[k]):
                        coefmatrix[k][overstrands[k]]+=1    
                    #     print("w(overstrand) does not equal color(i)")
                    
                    # print("the right side of the equation is positive 1")
                    coefmatrix[k][n]=1                  
                    
                    
            elif (WhereIsA2i(colorlist,overstrands,n)[k]!=colorlist[overstrands[k]]):
                # print("w(i) for i = ", k, " is ", WhereIsA2i(colorlist,overstrands,n)[k])
                # print("the overstrand is ", overstrands[k], " and its color is ", colorlist[overstrands[k]] )
                # print("w(i) is not equal to color(overstrand)")
                # Same as above but all signs switch
                if (signs[k]==1):
                    # print("This crossing is positive")
                    if(WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]==colorlist[k]):
                        # print("w(overstrand) equals color(i)")
                        coefmatrix[k][overstrands[k]]+=1                        
                    elif (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]!=colorlist[k]):
                        # print("w(overstrand) does not equal color(i)")
                        coefmatrix[k][overstrands[k]]-=1  
                    # print("the right side of the equation is positive 1")
                    coefmatrix[k][n]=1                    
                elif (signs[k]==-1):
                    # print("this crossing is negative")
                    if(WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]==colorlist[k]):
                        # print("w(overstrand) equals color(i)")
                        coefmatrix[k][overstrands[k]]+=1                        
                    elif (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]!=colorlist[k]):
                        # print("w(overstrand) does not equal color(i)")
                        coefmatrix[k][overstrands[k]]-=1  
                    # print("the right side of the equation is negative 1")
                    coefmatrix[k][n]-=1      
                    
            # print("the coefficient of x(overstrand) is ", coefmatrix[k][overstrands[k]])
            # print()
                    
                    
                    
                    
        elif (homog(k, colorlist,n,overstrands)=='s'):    
            #print('check homogeneous signs again')
            # The 2-cells A_2f(k) and -A_3f(k) contribute the same amount to the bdry
            # so we compute the contribution of A_2f(k) and multiply by 2
            # The 2-cell A_1f(k) contributes nothing
            if (signs[k]==1):
                #Check whether the 3-cells from which you can see A_2k and A_2f(k)
                #on the right are the same or different
                if (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]==WhereIsA2i(colorlist,overstrands,n)[k]):
                    coefmatrix[k][overstrands[k]]-=2                    
                elif (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]!=WhereIsA2i(colorlist,overstrands,n)[k]):
                    coefmatrix[k][overstrands[k]]+=2                    
            elif (signs[k]==-1):
                if (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]==WhereIsA2i(colorlist,overstrands,n)[k]):
                    coefmatrix[k][overstrands[k]]-=2                    
                elif (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]!=WhereIsA2i(colorlist,overstrands,n)[k]):
                    coefmatrix[k][overstrands[k]]+=2
    print("COEF MATRIX:")
    print( coefmatrix )                     
    return coefmatrix

# computecoef2 computes the coefficients x_i of the 2-cells A_2i of the 2-chain bounding the
#degree 2 curve.  The 2-cells may also appear in this 2-chain.  If the coefficient of 
# A_3i is called y_i then x_i+y_i=1, so we need only the x_i.
def computecoef2(colorlist, numcrossings,overstrands, signs):
    n=numcrossings
    print("computecoef2 is being used")
    #The matrix A of coefficients in our system Ax=b
    coefmatrix= [[0 for x in range(n+1)] for x in range(n)] 
    for k in range(0,n):
        
        coefmatrix[k][k]+=1
       
        coefmatrix[k][(k+1)%n]-=1
       #PRETTY SURE THIS IS EPSILON 2
        if (homog(k,colorlist,n,overstrands)=='d'):
            if (WhereIsA2i(colorlist,overstrands,n)[k]==colorlist[overstrands[k]]):                
                if (signs[k]==1):                  
                    if(WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]==colorlist[k]):
                        coefmatrix[k][overstrands[k]]-=1
                        coefmatrix[k][n]+=1
                    elif (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]!=colorlist[k]):
                        coefmatrix[k][overstrands[k]]+=1   
                        coefmatrix[k][n]+=0
                elif (signs[k]==-1):
                    if(WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]==colorlist[k]):
                        coefmatrix[k][overstrands[k]]-=1
                        coefmatrix[k][n]-=0                        
                    elif (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]!=colorlist[k]):
                        coefmatrix[k][overstrands[k]]+=1
                        coefmatrix[k][n]-=1                        
            elif (WhereIsA2i(colorlist,overstrands,n)[k]!=colorlist[overstrands[k]]):                  
                if (signs[k]==1):
                    if(WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]==colorlist[k]):
                        coefmatrix[k][overstrands[k]]+=1     
                        coefmatrix[k][n]-=1
                    elif (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]!=colorlist[k]):
                        coefmatrix[k][overstrands[k]]-=1    
                        coefmatrix[k][n]+=0
                elif (signs[k]==-1):
                    if(WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]==colorlist[k]):
                        coefmatrix[k][overstrands[k]]+=1  
                        coefmatrix[k][n]+=0
                    elif (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]!=colorlist[k]):
                        coefmatrix[k][overstrands[k]]-=1  
                        coefmatrix[k][n]+=1
                        
                    
        elif (homog(k, colorlist,n,overstrands)=='s'):    
           
            if (signs[k]==1):
                
                if (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]==WhereIsA2i(colorlist,overstrands,n)[k]):
                    coefmatrix[k][overstrands[k]]-=2
                    coefmatrix[k][n]+=1
                elif (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]!=WhereIsA2i(colorlist,overstrands,n)[k]):
                    coefmatrix[k][overstrands[k]]+=2 
                    coefmatrix[k][n]-=1
            elif (signs[k]==-1):
                if (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]==WhereIsA2i(colorlist,overstrands,n)[k]):
                    coefmatrix[k][overstrands[k]]-=2   
                    coefmatrix[k][n]+=1
                elif (WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]!=WhereIsA2i(colorlist,overstrands,n)[k]):
                    coefmatrix[k][overstrands[k]]+=2  
                    coefmatrix[k][n]-=1
    return coefmatrix

#Solve for the x_i.  Pick a solution where all free variables are zero.

def solvefor2chain(matrixofcoefs, numcrossings):
    M=Matrix(matrixofcoefs)
    #print(M)
    pivots=M.rref()[1]
    #print(M.rref())
    numpivots=len(pivots)
    RR=M.rref()[0]    
    #initialize a column vector x
    x=[0 for j in range(numcrossings)]
    #if there is no solution then the last column is a pivot
    if numcrossings in pivots:
        return 'False'
    #let x be - the last column of the reduced row echelon form
    else:    
        for i in range(0,numpivots):
            x[pivots[i]]=-RR[i,numcrossings]  
        #Let all the free variables (non pivots) be zero
        return x
   
# print("3_1 two chain")
twochain_3_1 = solvefor2chain([[1, -1, -1, 0, -1], [1, 1, -1, 0, 1], [0, 1, 1, -1, -1], [-1, 0, 0, -1, 0]],4)
# print("6_1")
twochain_6_1 = solvefor2chain([[1, -1, -1, 0, 0, 0, -1], [0, 1, -1, 0, 1, 0, -1], [-1, 0, 1, -1, 0, 0, 1], [0, 0, 0, 1, -1, -1, -1], [0, 1, 0, 0, 1, -1, -1], [-1, 0, 0, -1, 0, 1, 1]],6)
# print("7_4")
twochain_7_4 = solvefor2chain([[1, -1, 0, 0, 0, 1, 0, 0, 1], [0, 1, -1, 0, 1, 0, 0, 0, -1], [-1, 0, 1, -1, 0, 0, 0, 0, -1], [0, 0, 0, 1, -1, 0, 1, 0, 1], [0, 1, 0, 0, 1, -1, 0, 0, -1], [0, 0, 2, 0, 0, 1, -1, 0, 0], [0, 0, 0, 1, 0, 0, 1, -1, 1], [-1, 0, 0, 0, 0, 0, 0, -1, 0]],8)
# print("7_7")
twochain_7_7 = solvefor2chain([[1, -1, 0, 0, -1, 0, 0, 0, -1], [0, 1, -1, -1, 0, 0, 0, 0, -1], [0, 0, 1, -1, 0, 0, -1, 0, -1], [0, 0, 0, 1, -1, -1, 0, 0, 1], [-1, 0, 0, 0, 1, -1, 0, 0, 1], [0, -2, 0, 0, 0, 1, -1, 0, 0], [0, 0, -1, 0, 0, 0, 1, -1, 1], [-1, 0, 0, 0, 0, 0, 0, -1, 0]],8)
# print("9_35")
twochain_9_35 = solvefor2chain([[1, -1, 0, 0, 0, 0, -2, 0, 0, 0, 0], [0, 1, -1, 0, 0, -2, 0, 0, 0, 0, 0], [0, 0, 1, -1, 0, 0, 0, 1, 0, 0, -1], [1, 0, 0, 1, -1, 0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 1, -1, 0, 0, 1, 0, -1], [0, -2, 0, 0, 0, 1, -1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 1, -1, 0, 0, -1], [0, 0, 1, 0, 0, 0, 0, 1, -1, 0, -1], [0, 0, 0, 0, 1, 0, 0, 0, 1, -1, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0]],10)
#Compute the intersection of the degree 2 curve with the 2 cells A_1k and x_k(A_2k-A3k)
#crossing by crossing

def intersectionnumberDeg2withDeg1Surface(boundarycoefs, colorlist, overstrands, signs, numcrossings):
    """ actual main linking number program
        it basically goes though each crossing after you use the matrix to find
        all coefficients and then 
    """
    n=numcrossings
    intersection=0
    #print('boundary coefs')
    #print(boundarycoefs)
    #push the degree 2 knot into the 3-cell from which A_2k can be seen from the right.
    for k in range(0,n):    
        if homog(k, colorlist,n,overstrands)=='d':
            #If the crossing is not homogeneous, the push-off will either intersect 
            #A_1f(k) or A_2f(k) or A_3f(k)
            #If the 3-cell from which A_2k can be seen from the right is the same as the 3-cell
            #adjacent to A_1f(k), the knot will intersect A_1f(k), which always appears in our 2-chain
            #with coefficient 1
            if WhereIsA2i(colorlist,overstrands,n)[k]==colorlist[overstrands[k]]:
                if signs[k]==1:
                    # print("add 1")
                    # print("case A_1")
                    intersection+=1
                    # print('case zero')
                    # print('f(k)=', overstrands[k], '-x_f(k)=', -boundarycoefs[overstrands[k]])
                    # print(intersection)
                elif signs[k]==-1:
                    # print("subtract 1")
                    # print("case A_1 neg")
                    intersection-=1
                    # print('case 1')
                    # print('f(k)=', overstrands[k], '-x_f(k)=', -boundarycoefs[overstrands[k]])
                    # print(intersection)
            #Otherwise the push-off will intersect A_2f(k)or A_3f(k),
            #but we only count it if x_i is nonzero.  Note that the knot intersects only
            #one of these, x_i times 
            #If it intersects A_3f(k) rather than A_2f(k) need to multiply by -1
            elif WhereIsA2i(colorlist,overstrands,n)[k]!=colorlist[overstrands[k]]:
                #Check whether the knot intersects A_2f(k) or A_3f(k) by checking
                #if the color of the incoming understrand matches the 2-cell in which
                #A_2 is on the right and looking at the sign of the crossing?
                            
                if colorlist[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    if signs[k]==1:
                        #in this case the knot intersects A_3f(k) so the contribution
                        #is -x[k]
                        intersection-=boundarycoefs[overstrands[k]]
                        # print("subtract ", boundarycoefs[overstrands[k]])
                        # print('case a')
                        # print('f(k)=', overstrands[k], '-x_f(k)=', -boundarycoefs[overstrands[k]])
                        # print(intersection)
                    elif signs[k]==-1:
                        intersection-=boundarycoefs[overstrands[k]]
                        # print("subtract ", boundarycoefs[overstrands[k]])
                        # print('case b')
                        # print('f(k)=', overstrands[k], '+-x_f(k)=', -boundarycoefs[overstrands[k]])
                        # print(intersection)        
                elif colorlist[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    if signs[k]==1:
                        intersection+=boundarycoefs[overstrands[k]]
                        # print("add ", boundarycoefs[overstrands[k]])
                        # print('case c')
                        # print('f(k)=', overstrands[k], 'x_f(k)=', boundarycoefs[overstrands[k]])
                        # print(intersection)
                    elif signs[k]==-1:
                        intersection+=boundarycoefs[overstrands[k]]
                        # print("add ", boundarycoefs[overstrands[k]])
                        # print('case d')
                        # print('f(k)=', overstrands[k], 'x_f(k)=', boundarycoefs[overstrands[k]])
                        # print(intersection)
        elif homog(k, colorlist,n,overstrands)=='s':
            #The push-off will either intersect A_2f(k) or A_3f(k)
            if signs[k]==1:            
                if WhereIsA2i(colorlist,overstrands,n)[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    intersection+=boundarycoefs[overstrands[k]]
                    # print("add ", boundarycoefs[overstrands[k]])
                    # print('case e')
                    # print('f(k)=', overstrands[k], 'x_f(k)=', boundarycoefs[overstrands[k]])
                    # print(intersection)
                elif WhereIsA2i(colorlist,overstrands,n)[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    intersection-=boundarycoefs[overstrands[k]]
                    # print("subtract ", boundarycoefs[overstrands[k]])
                    # print('case f')
                    # print('f(k)=', overstrands[k], '-x_f(k)=', -boundarycoefs[overstrands[k]])
                    # print(intersection)
            elif signs[k]==-1:
                if WhereIsA2i(colorlist,overstrands,n)[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    intersection+=boundarycoefs[overstrands[k]]
                    # print("add ", boundarycoefs[overstrands[k]])
                    # print('case g')
                    # print('f(k)=', overstrands[k], 'x_f(k)=', boundarycoefs[overstrands[k]])
                    # print(intersection)
                elif WhereIsA2i(colorlist,overstrands,n)[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    intersection-=boundarycoefs[overstrands[k]]
                    # print("subtract ", boundarycoefs[overstrands[k]])
                    # print('case h')
                    # print('f(k)=', overstrands[k], '-x_f(k)=', -boundarycoefs[overstrands[k]])
                    # print(intersection)
    return intersection





print('3_1')
print(intersectionnumberDeg2withDeg1Surface(twochain_3_1, [1, 2, 0, 1], [2, 0, 1, 3], [1, 1, 1, 1], 4))
print('6_1')
print(intersectionnumberDeg2withDeg1Surface(twochain_6_1, [0, 2, 1, 2, 0, 1], [2, 4, 0, 5, 1, 3] , [1, -1, 1, 1, -1, 1] ,6) )
print('7_4')
print(intersectionnumberDeg2withDeg1Surface(twochain_7_4, [1, 2, 0, 2, 1, 0, 0, 1], [5, 4, 0, 6, 1, 2, 3, 7] , [-1, -1, -1, -1, -1, -1, -1, 1] , 8))
print('7_7')
print(intersectionnumberDeg2withDeg1Surface(twochain_7_7, [1, 0, 2, 1, 2, 0, 0, 1], [4, 3, 6, 5, 0, 1, 2, 7] , [1, -1, 1, -1, 1, -1, 1, 1] , 8))
print('9_35')
print(intersectionnumberDeg2withDeg1Surface(twochain_9_35, [2, 2, 2, 1, 0, 2, 2, 0, 1, 2], [6, 5, 7, 0, 8, 1, 3, 2, 4, 9],[-1, -1, -1, -1, -1, -1, -1, -1, -1, 1],10))


def intersectionnumberDeg1withDeg2Surface(boundarycoefs, colorlist, overstrands, signs, numcrossings):
    n=numcrossings
    intersection=0
    #push the degree 2 knot into the 3-cell from which A_2k can be seen from the right.
    for k in range(0,n):    
        if homog(k, colorlist,n,overstrands)=='d':
            if colorlist[overstrands[k]]==WhereIsA2i(colorlist,overstrands,n)[k]:
                if colorlist[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    if signs[k]==1:                    
                        intersection+=boundarycoefs[overstrands[k]]
                        #print("At crossing ", k, "Add ",boundarycoefs[overstrands[k]])
                    elif signs[k]==-1:
                        intersection-=1-boundarycoefs[overstrands[k]] 
                        #print("At crossing ", k, "Subtract 1-",boundarycoefs[overstrands[k]])
                elif colorlist[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    if signs[k]==1:
                        intersection+=1-boundarycoefs[overstrands[k]]
                        #print("At crossing ", k, "Add 1-",boundarycoefs[overstrands[k]])
                    elif signs[k]==-1:
                        intersection-=boundarycoefs[overstrands[k]]
                        #print("At crossing ", k, "Subtract ",boundarycoefs[overstrands[k]])
            elif colorlist[overstrands[k]]!=WhereIsA2i(colorlist,overstrands,n)[k]:
                if colorlist[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    if signs[k]==1:
                        intersection+=boundarycoefs[overstrands[k]]
                        #print("At crossing ", k, "Add ",boundarycoefs[overstrands[k]])
                    elif signs[k]==-1:
                        intersection-=1-boundarycoefs[overstrands[k]]
                        #print("At crossing ", k, "Subtract 1-",boundarycoefs[overstrands[k]])
                elif colorlist[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    if signs[k]==1:
                        intersection+=1-boundarycoefs[overstrands[k]]
                        #print("At crossing ", k, "Add 1-",boundarycoefs[overstrands[k]])
                    elif signs[k]==-1:
                        intersection-= boundarycoefs[overstrands[k]]
                        #print("At crossing ", k, "Subtract ",boundarycoefs[overstrands[k]])
        elif homog(k, colorlist,n,overstrands)=='s':
            #The push-off will either intersect A_2f(k) or A_3f(k)
            if signs[k]==1:            
                if WhereIsA2i(colorlist,overstrands,n)[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    intersection+=0
#                    print('case e')
#                    print('f(k)=', overstrands[k], 'add', 1)
                elif WhereIsA2i(colorlist,overstrands,n)[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    intersection+=0
#                    print('case f')
#                    print('f(k)=', overstrands[k], 'add', 1)
            elif signs[k]==-1:
                if WhereIsA2i(colorlist,overstrands,n)[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    intersection-=0
#                    print('case g')
#                    print('f(k)=', overstrands[k], 'add', -1)
                elif WhereIsA2i(colorlist,overstrands,n)[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    intersection-=0
#                    print('case h')
#                    print('f(k)=', overstrands[k], 'add', -1)
    return intersection

def selflinkingnumberDeg1(boundarycoefs, colorlist, overstrands, signs, numcrossings):
    n=numcrossings
    selflinking=0
    #push the degree 1 knot into the 3-cell from which A_2k can be seen from the right.
    for k in range(0,n):    
        if homog(k, colorlist,n,overstrands)=='d':
            if colorlist[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                if signs[k]==1:
                    #in this case the knot intersects A_3f(k) so the contribution
                    #is -x[k]
                    selflinking+=boundarycoefs[overstrands[k]]
#                    print('case a')
#                    print('f(k)=', overstrands[k], '+x_f(k)=', -boundarycoefs[overstrands[k]])
                elif signs[k]==-1:
                    selflinking+=boundarycoefs[overstrands[k]]
#                    print('case b')
#                    print('f(k)=', overstrands[k], 'x_f(k)=', boundarycoefs[overstrands[k]])
                
            elif colorlist[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                if signs[k]==1:
                    selflinking-=boundarycoefs[overstrands[k]]
#                    print('case c')
#                    print('f(k)=', overstrands[k], '-x_f(k)=', boundarycoefs[overstrands[k]])
                elif signs[k]==-1:
                    selflinking-=boundarycoefs[overstrands[k]]
#                    print('case d')
#                    print('f(k)=', overstrands[k], '-x_f(k)=', -boundarycoefs[overstrands[k]])
        elif homog(k, colorlist,n,overstrands)=='s':
            #The push-off will either intersect A_2f(k) or A_3f(k)
            if signs[k]==1:            
                if WhereIsA2i(colorlist,overstrands,n)[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    selflinking+=1
#                    print('case e')
#                    print('f(k)=', overstrands[k], 'add', 1)
                elif WhereIsA2i(colorlist,overstrands,n)[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    selflinking+=1
#                    print('case f')
#                    print('f(k)=', overstrands[k], 'add', 1)
            elif signs[k]==-1:
                if WhereIsA2i(colorlist,overstrands,n)[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    selflinking-=1
#                    print('case g')
#                    print('f(k)=', overstrands[k], 'add', -1)
                elif WhereIsA2i(colorlist,overstrands,n)[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    selflinking-=1
#                    print('case h')
#                    print('f(k)=', overstrands[k], 'add', -1)
    return selflinking


def selflinkingnumberDeg2(boundarycoefs, colorlist, overstrands, signs, numcrossings):
    n=numcrossings
    selflinking=0
    #push the degree 2 knot into the 3-cell from which A_2k can be seen from the right.
    for k in range(0,n):    
        if homog(k, colorlist,n,overstrands)=='d':
            if colorlist[overstrands[k]]==WhereIsA2i(colorlist,overstrands,n)[k]:
                if colorlist[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    if signs[k]==1:                    
                        selflinking+=0
                        #print("At crossing ", k, "Add 0")
                    elif signs[k]==-1:
                        selflinking+=0   
                        #print("At crossing ", k, "Add 0")
                elif colorlist[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    if signs[k]==1:
                        selflinking-=0
                        #print("At crossing ", k, "Add 0")
                    elif signs[k]==-1:
                        selflinking-=0
                        #print("At crossing ", k, "Add 0")
            elif colorlist[overstrands[k]]!=WhereIsA2i(colorlist,overstrands,n)[k]:
                if colorlist[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    if signs[k]==1:
                        selflinking+=1-boundarycoefs[overstrands[k]]
                        #print("At crossing ", k, "Add 1-",boundarycoefs[overstrands[k]])
                    elif signs[k]==-1:
                        selflinking-=boundarycoefs[overstrands[k]]
                        #print("At crossing ", k, "Subtract ",boundarycoefs[overstrands[k]])
                elif colorlist[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    if signs[k]==1:
                        selflinking+=boundarycoefs[overstrands[k]]
                        #print("At crossing ", k, "Add ",boundarycoefs[overstrands[k]])
                    elif signs[k]==-1:
                        selflinking-=1-boundarycoefs[overstrands[k]]
                        #print("At crossing ", k, "Subtract 1-",boundarycoefs[overstrands[k]])
        elif homog(k, colorlist,n,overstrands)=='s':
            #The push-off will either intersect A_2f(k) or A_3f(k)
            if signs[k]==1:            
                if WhereIsA2i(colorlist,overstrands,n)[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    # if w(strand) = w(overstrand)
                    selflinking+=boundarycoefs[overstrands[k]]
                    # then the linking number gets added
                    #print("At crossing ", k, "Add ",boundarycoefs[overstrands[k]])
#                    print('case e')
#                    print('f(k)=', overstrands[k], 'add', 1)
                elif WhereIsA2i(colorlist,overstrands,n)[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    selflinking+=1-boundarycoefs[overstrands[k]]
                    #print("At crossing ", k, "Add 1-",boundarycoefs[overstrands[k]])
#                    print('case f')
#                    print('f(k)=', overstrands[k], 'add', 1)
            elif signs[k]==-1:
                if WhereIsA2i(colorlist,overstrands,n)[k]==WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    selflinking-=1-boundarycoefs[overstrands[k]]
                    #print("At crossing ", k, "Subtract 1-",boundarycoefs[overstrands[k]])
#                    print('case g')
#                    print('f(k)=', overstrands[k], 'add', -1)
                elif WhereIsA2i(colorlist,overstrands,n)[k]!=WhereIsA2i(colorlist,overstrands,n)[overstrands[k]]:
                    selflinking-=boundarycoefs[overstrands[k]]
                    #print("At crossing ", k, "Subtract ",boundarycoefs[overstrands[k]])
#                    print('case h')
#                    print('f(k)=', overstrands[k], 'add', -1)
    return selflinking


def linkinginvariantcollectionDeg1(numcrossings, overstrands, signs):
    allinvariants=[]
    validcoloringlist=findallcolorings(numcrossings,overstrands)
    for i in range(0, len(validcoloringlist)):
        currentM=computecoef(validcoloringlist[i],numcrossings,overstrands,signs)
        if solvefor2chain(currentM, numcrossings)!='False':        
            allinvariants.append(intersectionnumberDeg2withDeg1Surface(solvefor2chain(currentM,numcrossings),validcoloringlist[i],overstrands, signs, numcrossings))
        else:
            allinvariants.append('undefined')
    return allinvariants
    
def linkinginvariantcollectionDeg2(numcrossings, overstrands, signs):
    allinvariants=[]
    validcoloringlist=findallcolorings(numcrossings,overstrands)
    for i in range(0, len(validcoloringlist)):
        currentM=computecoef2(validcoloringlist[i],numcrossings,overstrands,signs)
        if solvefor2chain(currentM, numcrossings)!='False':        
            allinvariants.append(intersectionnumberDeg1withDeg2Surface(solvefor2chain(currentM,numcrossings),validcoloringlist[i],overstrands, signs, numcrossings))
        else:
            allinvariants.append('undefined')
    return allinvariants
    
def selflinkinginvariantcollectionDeg1(numcrossings, overstrands, signs):
    
    allselflinking=[]
    validcoloringlist=findallcolorings(numcrossings,overstrands)
    for i in range(0, len(validcoloringlist)):
        currentM=computecoef(validcoloringlist[i],numcrossings,overstrands,signs)
        if solvefor2chain(currentM, numcrossings)!='False':        
            
            allselflinking.append(selflinkingnumberDeg1(solvefor2chain(currentM,numcrossings),validcoloringlist[i],overstrands, signs, numcrossings))
        else:
            allselflinking.append('undefined')
    return allselflinking
    
def selflinkinginvariantcollectionDeg2(numcrossings, overstrands, signs):
    
    allselflinking=[]
    validcoloringlist=findallcolorings(numcrossings,overstrands)
    for i in range(0, len(validcoloringlist)):
        currentM=computecoef2(validcoloringlist[i],numcrossings,overstrands,signs)
        if solvefor2chain(currentM, numcrossings)!='False':        
            
            allselflinking.append(selflinkingnumberDeg2(solvefor2chain(currentM,numcrossings),validcoloringlist[i],overstrands, signs, numcrossings))
        else:
            allselflinking.append('undefined')
    return allselflinking
    
def slice2bridgeType1(a,b):
    n=4+4*a+4*b
    signs=[0 for x in range(n)]
    overstrands=[0 for x in range(n)]
    coloring=[0 for x in range(n)]
    # Box 1
    for k in range(0,a):
        signs[k]=1
        overstrands[k]=(1+4*a+3*b-k)%n
        coloring[k]=(-k)%3 +1
    for k in range(2+3*a+3*b,1+4*a+3*b+1):
        signs[k]=1
        overstrands[k]=(4*a+3*b+1-k)%n
        coloring[k]=1+((k-1)%3)
    # Box 2
    signs[1+3*a+3*b]=-1
    overstrands[1+3*a+3*b]=(2+4*a+3*b)%n
    coloring[1+3*a+3*b]=1
    signs[2+4*a+3*b]=-1
    overstrands[2+4*a+3*b]=(1+3*a+3*b)%n
    coloring[2+4*a+3*b]=3
    # Box 3
    for k in range(a, a+b-1+1):
        signs[k]=1
        overstrands[k]=(4*a+3*b-k)%n
        coloring[k]=(1+k)%3+1
    for k in range(3*a+2*b+1,3*a+3*b+1):
        signs[k]=1
        overstrands[k]=(4*a+3*b-k)%n
        coloring[k]=((1+-k)%3)+1
    # Box 4
    signs[3*a+2*b]=1
    overstrands[3*a+2*b]=(4+4*a+3*b)%n
    coloring[3*a+2*b]=2
    signs[3+4*a+3*b]=1
    overstrands[3+4*a+3*b]=(1+3*a+2*b)%n
    coloring[3+4*a+3*b]=2
    # Box 5
    for k in range(a+b,2*a+b-1+1):
        signs[k]=-1
        overstrands[k]=(4*a+3*b-k)%n
        coloring[k]=(-k-1)%3+1
    for k in range(2*a+2*b,3*a+2*b-1+1):
        signs[k]=-1
        overstrands[k]=(4*a+3*b-k)%n
        coloring[k]=(k-1)%3+1
    
    # Box 6
    for k in range(2*a+b,2*a+2*b-1+1):
        signs[k]=-1
        overstrands[k]=(3+6*a+5*b-k)%n
        coloring[k]=1+(k-1)%3
    for k in range(4+4*a+3*b,3+4*a+4*b+1):
        signs[k]=-1
        overstrands[k]=(6*a+5*b+3-k)%n
        coloring[k]=1+((-k)%3)
    return signs, overstrands, coloring

def twobridge(a,b,c,d,e,f):
    n=2*(a+b+c+d+e+f)
    signs=[0 for x in range(n)]
    overstrands=[0 for x in range(n)]
    coloring=[0 for x in range(n)]
    # Box 1
    for k in range(0,a):
        signs[k]=1
        overstrands[k]=(9+2*(a-1)+(b-1)+2*(c-1)+2*(e-1)+(f-1)+(d-1)-k)%n
        coloring[k]=(k)%3 +1
    for k in range(8+a-1+b-1+2*(c-1)+2*(e-1)+f-1+d-1,8+2*(a-1)+b-1+2*(c-1)+2*(e-1)+f-1+d-1+1):
        signs[k]=1
        overstrands[k]=(9+2*(a-1)+(b-1)+2*(c-1)+2*(e-1)+(f-1)+(d-1)-k)%n
        coloring[k]=1+((-k-1)%3)
    # Box 2
    for k in range(9+2*(a-1)+b-1+2*(c-1)+2*(e-1)+f-1+d-1,9+2*(a-1)+2*(b-1)+2*(c-1)+2*(e-1)+f-1+d-1+1):
        signs[k]=-1
        overstrands[k]=(17+3*(a-1)+2*(b-1)+4*(c-1)+4*(e-1)+2*(f-1)+2*(d-1)-k)%n
        coloring[k]=(k-1)%3+1
    for k in range(7+a-1+2*(c-1)+2*(e-1)+f-1+d-1,7+a-1+2*(c-1)+2*(e-1)+f-1+d-1+b-1+1):
        signs[k]=-1
        overstrands[k]=(17+3*(a-1)+2*(b-1)+4*(c-1)+4*(e-1)+2*(f-1)+2*(d-1)-k)%n
        coloring[k]=(-k-1)%3+1    
    # Box 3
    for k in range(a, a+c-1+1):
        signs[k]=1
        overstrands[k]=(8+2*(a-1)+2*(c-1)+2*(e-1)+f-1+d-1-k)%n
        coloring[k]=(1-k)%3+1
    for k in range(6+a-1+c-1+2*(e-1)+f-1+d-1,6+a-1+2*(c-1)+2*(e-1)+f-1+d-1+1):
        signs[k]=1
        overstrands[k]=(8+2*(a-1)+2*(c-1)+2*(e-1)+f-1+d-1-k)%n
        coloring[k]=((1+k)%3)+1
    # Box 4
    for k in range(10+2*(a-1)+2*(b-1)+2*(c-1)+d-1+2*(e-1)+f-1,10+2*(a-1)+2*(b-1)+2*(c-1)+2*(d-1)+2*(e-1)+f-1 +1):
        signs[k]=1
        overstrands[k]=15+3*(a-1)+2*(b-1)+3*(c-1)+2*(d-1)+4*(e-1)+2*(f-1)-k
        coloring[k]=2
    for k in range(5+a-1+c-1+2*(e-1)+f-1,5+a-1+c-1+2*(e-1)+f-1+d-1+1 ):
        overstrands[k]=15+3*(a-1)+2*(b-1)+3*(c-1)+2*(d-1)+4*(e-1)+2*(f-1)-k
        coloring[k]=2
        signs[k]=1
    # Box 5
    for k in range(2+a-1+c-1,2+a-1+c-1+e-1+1):
        signs[k]=-1
        overstrands[k]=(6+2*(a-1)+2*(c-1)+2*(e-1)+f-1-k)%n
        coloring[k]=(k-1)%3+1
    for k in range(4+a-1+c-1+e-1+f-1,4+a-1+c-1+2*(e-1)+f-1+1):
        signs[k]=-1
        overstrands[k]=(6+2*(a-1)+2*(c-1)+2*(e-1)+f-1-k)%n
        coloring[k]=(-k-1)%3+1
    
    # Box 6
    for k in range(3+a-1+c-1+e-1,3+a-1+c-1+e-1+f-1+1):
        signs[k]=-1
        overstrands[k]=(15+3*(a-1)+2*(b-1)+3*(c-1)+3*(e-1)+2*(d-1)+2*(f-1)-k)%n
        coloring[k]=1+(-k-1)%3
    for k in range(11+2*(a-1)+2*(b-1)+2*(c-1)+2*(d-1)+2*(e-1)+(f-1),11+2*(a-1)+2*(b-1)+2*(c-1)+2*(d-1)+2*(e-1)+2*(f-1)+1):
        signs[k]=-1
        overstrands[k]=(15+3*(a-1)+2*(b-1)+3*(c-1)+3*(e-1)+2*(d-1)+2*(f-1)-k)%n
        coloring[k]=1+((k)%3)
    return signs, overstrands, coloring

## Find one coloring of a slice 2 bridge knot of type 1 by assinging different
##colors to the first two strands and then continuing brute force
#
#def slice2bridgeType1coloring(a,b):
#    n=12+4*(a-1)+4*(b-1)
#    coloring=[0 for x in range(n)]   
#    coloring[0]=1
#    coloring[1]=2
#    signs=slice2bridgeType1(a,b)[0]
#    overstrands=slice2bridge[Type1(a,b)[1]]
#    for k in range(0,n):
#        if (coloring[k]!=0) and (coloring[(k+1)%n]!=0):
#            s=set()
#            s.add(1)
#            s.add(2)
#            s.add(3)
#            s.discard(col)
#            s.discard(colorlist[overstrands[(i-1)%numcrossings]])
#            twist.append(s.pop())
#           coloring[overstrands[k]] 

def display(signs,overstrands,name,coloring): #,detail
    c=len(signs)
    #print('**********************************************************')
    #print('The knot is: ', name)
    #print()
    #print('The list of signs is: ', signs)
    #print()
    #print('The list of overcrossings is: ', overstrands)
    #print()
#    print('The number of valid colorings is: ',len(findallcolorings(c,overstrands)))
    #print()
#    print(findallcolorings(c,overstrands))
#    print()
    #print('Consider in detail the coloring ' , coloring)
    #print()
    #print("The list of 3-cells from which A_2k is seen from the right is:")
    #print()
    #print(WhereIsA2i(coloring,overstrands,c))
    #print()
    M=computecoef(coloring,c,overstrands, signs)
#    print('The matrix of coefficients x_i of A_2i-A_3i, with inhomogeneous part in the last column, is')
#    print()
#    print(M)
#    print()
#    print('The reduced row eschelon form and pivots are:')
#    print(Matrix(M).rref())
    #print()
    #if solvefor2chain(M,c)!='False':
    #    print('The coefficients of the 2-cell corresponding to the deg 1 curve are')
    #    print()
    #    print(solvefor2chain(M,c))
    #    print()
    #    print('The linking number, computed with the surface bounded by the deg 1 curve, is ', intersectionnumberDeg2withDeg1Surface(solvefor2chain(M,c),coloring,overstrands,signs,c),'.')
    #    print()
    #    print('The self-linking number of the degree 1 curve is ', selflinkingnumberDeg1(solvefor2chain(M,c),coloring,overstrands,signs,c),'.')
    #    print()
    #else:
    #    print('There is no bounding 2-chain for the degree 1 curve.')
    #    print()
############### OLIVIA CHANGED    M2=computecoef2(coloring,c,overstrands, signs)
#    print('The matrix of coefficients x_i of A_2i (and 1-x_i of A_3i), with inhomogeneous part in the last column, is')
#    print()
#    print(M2)
#    print()
#    print('The reduced row eschelon form and pivots are:')
#    print(Matrix(M2).rref())
#    print()
 ############## OLIVIA CHANGED   if solvefor2chain(M2,c)!='False':
        #print('The coefficients of 2-cell corresponding to the deg 2 curve are')
        #print()
        #print(solvefor2chain(M2,c))
        #print()
        #print('The linking number, computed with the surface bounded by the deg 2 curve, is ', intersectionnumberDeg1withDeg2Surface(solvefor2chain(M2,c),coloring,overstrands,signs,c),'.')
        #print()
    return intersectionnumberDeg2withDeg1Surface(solvefor2chain(M,c),coloring,overstrands,signs,c)#intersectionnumberDeg1withDeg2Surface(solvefor2chain(M2,c),coloring,overstrands,signs,c)#,intersectionnumberDeg2withDeg1Surface(solvefor2chain(M,c),coloring,overstrands,signs,c)]
        #print('The self-linking number of the degree 2 curve is ', selflinkingnumberDeg2(solvefor2chain(M2,c),coloring,overstrands,signs,c),'.')
 ##############   else:
 ##############       return "No Dihedral Linking Number Exists"
    #if detail=='yes':

    #    print('The collection of linking invariants for ', name, ' computed by intersecting the degree 2 curve with a surface whose boundary is the degree 1 curve, is:')
    #    print()
    #    print(set(linkinginvariantcollectionDeg1(c,overstrands, signs)))
    #    print()
    #    print('The collection of linking invariants for ', name, ' computed by intersecting the degree 1 curve with a surface whose boundary is the degree 2 curve, is:')
    #    print(set(linkinginvariantcollectionDeg2(c,overstrands, signs)))
    #    print()
    #    print('The collection of self-linking numbers of the degree 1 curve for ', name, 'is:')
    #    print()
    #    print(set(selflinkinginvariantcollectionDeg1(c,overstrands,signs)))
    #    print()
    #    print('The collection of self-linking numbers of the degree 2 curve for ', name, 'is:')
    #    print()
    #    print(set(selflinkinginvariantcollectionDeg2(c,overstrands,signs)))
    #    print()
    #elif detail=='no':
    #    print('For collections of invariants let detail= yes')
"""





print('trefoil')
print('patricia got '+str(display([1, 1, 1, 1],[2, 0, 1, 3],'3_1',[1, 2, 0, 1])))
#print('we got')
print('6_1')
print('patricia got'+str(display([1, -1, 1, 1, -1, 1] ,[2, 4, 0, 5, 1, 3] , '6_1' ,[0, 2, 1, 2, 0, 1])))
#print('patricia got -2')
print('7_4')
print('patricia got '+str(display( [-1, -1, -1, -1, -1, -1, -1, 1] ,[5, 4, 0, 6, 1, 2, 3, 7] ,'7_4',[1, 2, 0, 2, 1, 0, 0, 1])))
#print('patricia got 2')
print('7_7')
print('patricia got '+str(display([1, -1, 1, -1, 1, -1, 1, 1] ,[4, 3, 6, 5, 0, 1, 2, 7] ,  '7_7',[1, 0, 2, 1, 2, 0, 0, 1])))
#print('patricia got -2')
"""

# 0 6 -8 4



def slicedisplayType1(aRange,bRange):
    for k in range(0,aRange):
        for l in range(0,bRange):
            a=1+3*k
            b=1+3*l
            print("The paramaters (a,b): ",a, ', ',b)
            signs=slice2bridgeType1(a,b)[0]
            overstrands=slice2bridgeType1(a,b)[1]
            coloring=slice2bridgeType1(a,b)[2]
            n=len(signs)
            if valid(coloring,n,overstrands)=='true':
                M=computecoef(coloring,n,overstrands, signs)
                if solvefor2chain(M,n)!='False':
                    slkdeg1=selflinkingnumberDeg1(solvefor2chain(M,n),coloring,overstrands,signs,n)
                    lk1=intersectionnumberDeg2withDeg1Surface(solvefor2chain(M,n),coloring,overstrands,signs,n)
       
                else:
                   slkdeg1='undefined'
                   lk1='undefined'
                M2=computecoef2(coloring,n,overstrands,signs)
                if solvefor2chain(M2,n)!='False':
                    slkdeg2=selflinkingnumberDeg2(solvefor2chain(M2,n),coloring,overstrands,signs,n)
                    lk2=intersectionnumberDeg1withDeg2Surface(solvefor2chain(M2,n),coloring,overstrands,signs,n)
                else:
                    slkdeg2='undefined'
                    lk2='undefined'
                print('Self-linking of degree 1 curve: ',slkdeg1)
                print('Self-linking of degree 2 curve: ',slkdeg2)
                print('Linking of branch curves computed in two ways: ', lk1, ', ', lk2)
            else:
                print('invalid coloring')
            print('________________________________________________')
            print()
            
def twobridgedisplay(a,b,c,d,e,f):
    
    print("The paramaters (a,b,c,d,e,f): ",a, ', ',b, ', ', c, ', ', d, ', ', e, ', ',f)
    signs=twobridge(a,b,c,d,e,f)[0]
    overstrands=twobridge(a,b,c,d,e,f)[1]
    coloring=twobridge(a,b,c,d,e,f)[2]
    n=len(signs)
    if valid(coloring,n,overstrands)=='true':
        M=computecoef(coloring,n,overstrands, signs)
        if solvefor2chain(M,n)!='False':
            slkdeg1=selflinkingnumberDeg1(solvefor2chain(M,n),coloring,overstrands,signs,n)
            lk1=intersectionnumberDeg2withDeg1Surface(solvefor2chain(M,n),coloring,overstrands,signs,n)
   
        else:
           slkdeg1='undefined'
           lk1='undefined'
        M2=computecoef2(coloring,n,overstrands,signs)
        if solvefor2chain(M2,n)!='False':
            slkdeg2=selflinkingnumberDeg2(solvefor2chain(M2,n),coloring,overstrands,signs,n)
            lk2=intersectionnumberDeg1withDeg2Surface(solvefor2chain(M2,n),coloring,overstrands,signs,n)
        else:
            slkdeg2='undefined'
            lk2='undefined'
        print('Self-linking of degree 1 curve: ',slkdeg1)
        print('Self-linking of degree 2 curve: ',slkdeg2)
        print('Linking of branch curves computed in two ways: ', lk1, ', ', lk2)
    else:
        print('invalid coloring')
    print('________________________________________________')
    print()
    
def twobridgedatatable(arange,brange,crange,drange,erange,frange):
    for i in range(0,arange):
        for j in range(0,brange):
            for k in range(0, crange):
                for l in range(0, drange):
                    for m in range(0, erange):
                        for n in range(0, frange):
                            twobridgedisplay(2*(3*i+1),2*(3*j+1),2*(3*k+1),2*(3*l+1),2*(3*m+1),2*(3*n+1))

import csv

#           0            1                  2              3             4            5
"""
fields = [ 'Name','Gauss Notation', 'Overstrand List', 'Sign List', 'Color List', 'Dihedral Linking Number' ]

newfields = [ 'Name', 'Dihedral Linking Number' ]

filename = "allfields_3colorable.csv"

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
        color_list_listoflists = [ list(crossing.split(",")) for crossing in color_list_listofstrings ]
        color_lists = [ [int(n) for n in string] for string in color_list_listoflists ]
        #print("COLOR LISTS")
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
        
        new_LoL.append([row[0],dihedral_linking_numbers])
        dihedral_linking_numbers = []
        
        line_count = line_count + 1

rawfile.close()



newfilename = "name_DLN_3colorable.csv"

newrawfile = open(newfilename, 'w')

writer = csv.writer(newrawfile)

for row in new_LoL:
    writer.writerow(row)

newrawfile.close()
"""

#print(display([-1,-1,1,1,1,1],[3,5,4,0,2,1],'6-1',[2,1,2,0,1,0]))
#print(display([-1,-1,1,1,1,1],[3,5,4,0,2,1],'6-1',[3,2,3,1,2,1]))
#display([1,1,1,1,1,1,1,1],[4,5,0,7,2,1,6,3],'6-1',[2,2,1,3,2,3,1,1],'no')
#print(display([-1,1,-1,1,-1,1,-1,1],[4,3,6,7,0,6,2,1],'7-7',[3,1,3,2,2,1,1,2]))

print(display([1,1,1,1],[2,0,1,3],'3-1',[1,2,3,1]))
print(display([1, -1, 1, 1, -1, 1],[2, 4, 0, 5, 1, 3],'6-1',[0, 2, 1, 2, 0, 1]))






#print(display([-1,1,-1,1,1,1,1,1,1,1,-1,1],[2,4,5,6,1,9,3,5,10,6,8,11],'11n-1',[1,2,3,3,1,3,2,1,2,1,3,1,1]))
#Lo_Knot_Ls_31 = [[[3,0,2,1],[1,1,1,-1],[1,2,3,3]],[[2,0,1,3],[1,1,1,-1],[1,2,3,1]],[[2,0,3,1],[1,1,-1,1],[1,2,3,3]],[[3,2,0,1],[1,1,-1,1],[1,2,2,3]],[[1,3,2,0],[1,-1,1,1],[1,2,2,3]]]


#for i in range(len(Lo_Knot_Ls_31)):
#    print(display(Lo_Knot_Ls_31[i][0],Lo_Knot_Ls_31[i][1],'knotzzzz',Lo_Knot_Ls_31[i][2],'no'))


#display([1,1,1,-1,1,1,1,-1],[6,4,5,7,2,0,1,3],'8-5',[3,1,2,3,3,1,2,3],'no')
#print(findallcolorings(6,[3,5,4,0,2,1]))

#display([1,-1,-1,1,-1,-1],[3,5,4,0,2,1],'the 6-1 knot',[1,2,1,3,2,3] )

#print(findallcolorings(8,[2,5,4,6,0,1,3,7]))

#display([-1,1,-1,1,-1,1,1,1],[2,5,4,6,0,1,3,7],'the 7-7 knot', [1,2,3,2,1,1,3,1])

#M=Matrix(computecoef2([1,2,3,2,1,1,3,1],8,[2,5,4,6,0,1,3,7],[-1,1,-1,1,-1,1,1,1]))
#print("the matrix of coefficients x_i of A_2i and 1-x_i of A_3i for the 2-chain bounding the degree 2 curve") 
#print(M)
#print(solvefor2chain(computecoef2([1,2,3,2,1,1,3,1],8,[2,5,4,6,0,1,3,7],[-1,1,-1,1,-1,1,1,1]),8))
#print('The reduced row eschelon form and pivots are:')
#print(Matrix(M).rref())
#coefs2=solvefor2chain(computecoef2([1,2,3,2,1,1,3,1],8,[2,5,4,6,0,1,3,7],[-1,1,-1,1,-1,1,1,1]),8)
#print(selflinkingnumberDeg2(coefs2,[1,2,3,2,1,1,3,1],[2,5,4,6,0,1,3,7],[-1,1,-1,1,-1,1,1,1],8))

#print(findallcolorings(8,[5,7,0,6,1,3,4,2]))

#display([-1,1,1,1,-1,1,1,1],[5,7,0,6,1,3,4,2],'the 8-5 knot', [1,1,2,3,1,1,2,3])


#display([1,1,1,-1,1,-1,-1,1],[4,7,0,6,1,3,5,2],'the 8-10 knot', [1,1,2,3,1,1,2,3])

#print(findallcolorings(8,[3,5,6,0,1,7,2,4]))

#display([-1,-1,1,-1,-1,-1,1,-1],[3,5,6,0,1,7,2,4], 'the 8-11 knot', [1,2,2,3,2,2,1,3])
#print(findallcolorings(10,[2,5,6,7,8,1,3,9,4,9]))

#display([-1,1,-1,-1,1,1,-1,-1,1,1],[2,5,6,7,8,1,3,9,4,9],'the 9-17 knot', [1,2,3,3,3,1,3,3,2,1])


#display([1,1,-1,-1,1,1,1,-1,1,1,-1,-1],[4,5,6,9,1,8,10,2,0,7,3,0],'the 11-171 knot', [3,1,2,1,2,3,3,1,3,3,2,3])
#display([1,1,-1,-1,1,1,1,-1,1,1,-1,-1],[4,5,6,9,1,8,10,2,0,7,3,0],'the 11-171 knot', [1,1,1,2,1,1,3,3,2,3,3,1])

#display([1,1,-1,-1,-1,1,1,-1,1,-1,1,-1],[9,7,4,0,2,10,2,10,1,8,5,4],'the simple slice 2-bridge knot', [1, 2, 1, 2, 3, 2, 2, 3, 1, 3, 2, 2],'no')
#print(findallcolorings(12,[9,7,4,0,2,10,2,10,1,8,5,4] ))
#print(findallcolorings(24, [18,17,16,15,13,7,0,5,22,21,20,19,5,19,4,3,2,1,14,11,10,9,8,7]))
#display([1,1,1,1,1,-1,-1,-1,1,1,1,1,1,-1,1,1,1,1,-1,1,1,1,1,-1],[18,17,16,15,13,7,0,5,22,21,20,19,5,19,4,3,2,1,14,11,10,9,8,7],'the next simplest slice 2-bridge knot', [1,2,3,1,2,1,2,3,2,2,2,2,2,3,1,3,2,1,3,2,2,2,2,2],'no')
#print(slice2bridgeType1(4,4))
#print(valid(slice2bridgeType1(4,4)[2],len(slice2bridgeType1(4,4)[1]),slice2bridgeType1(4,4)[1]))
#display(slice2bridgeType1(4,4)[0],slice2bridgeType1(4,4)[1],'the slice 2-bridge knot of type (4,4)',slice2bridgeType1(4,4)[2],'no')
#display(slice2bridgeType1(7,4)[0],slice2bridgeType1(7,4)[1],'the slice 2-bridge knot of type (7,4)',slice2bridgeType1(7,4)[2],'no')
#print(valid(slice2bridgeType1(7,4)[2],len(slice2bridgeType1(7,4)[1]),slice2bridgeType1(7,4)[1]))
#slicedisplayType1(5,4)
#print(twobridge(8,2,2,2,2,2))
#print(valid(twobridge(8,2,2,2,2,2)[2],len(twobridge(8,2,2,2,2,2)[2]),twobridge(8,2,2,2,2,2)[1]))
#twobridgedisplay(8,2,2,2,2,2)
#twobridgedatatable(2,2,2,2,2,2)
#twobridgedatatable(6,1,1,1,1,1)

#display([1,1,1,1,1,1],[5,3,4,2,0,1],'connected sum of two trefoils',[1,2,1,3,2,3],'yes')
#print(findallcolorings(6,[5,3,4,2,0,1]))
#display([1,1,1,1,1,1],[5,3,4,2,0,1],'connected sum of two trefoils',[1,1,2,3,1,1],'yes')
#display([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[3,7,1,18,16,13,10,1,10,7,8,13,6,11,19,5,18,4,16,14],'HF mutant knot 1', [1,1,1,1,1,1,2,1,1,2,3,2,1,3,1,1,1,1,1,1],'no')
#display([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[3,7,1,19,15,13,10,1,10,7,8,16,6,15,5,13,11,19,4,17],'HF mutant knot 2', [2,2,2,2,1,1,1,2,2,1,3,1,1,1,1,1,1,1,2,3],'no')
#display([-1,-1,-1,-1,-1,-1,-1,-1,-1],[5,6,7,8,0,1,2,3,4],'(2,9)',[3,1,2,3,1,2,3,1,2],'no')
#display([-1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,1],[2,6,0,18,15,2,12,21,18,17,16,21,20,6,5,11,10,9,5,6,12,15,18],'mystery knot',[2,3,1,3,2,3,2,2,2,3,1,2,2,2,2,1,3,2,1,2,2,2,3],'no')