

#
#
#  Program to calculate the Dihedral Linking Numbers for
#  three colored knots
#
#

import sympy
import math

# reference lists for testing
overstrand_3_1 = [2, 0, 1, 3]
overstrand_6_1 = [2, 4, 0, 5, 1, 3]
overstrand_7_4 = [5, 4, 0, 6, 1, 2, 3, 7]
overstrand_7_7 = [4, 3, 6, 5, 0, 1, 2, 7]
overstrand_9_35 = [6, 5, 7, 0, 8, 1, 3, 2, 4, 9]

color_3_1 = [1, 2, 3, 1]
color_6_1 = [3, 2, 1, 2, 3, 1]
color_7_4 = [1, 2, 3, 2, 1, 3, 3, 1]
color_7_7 = [1, 3, 2, 1, 2, 3, 3, 1]
color_9_35 = [3, 1, 2, 3, 3, 3, 2, 1, 3, 3]

sign_3_1 = [1, 1, 1, 1]
sign_6_1 = [1, -1, 1, 1, -1, 1]
sign_7_4 = [-1, -1, -1, -1, -1, -1, -1, 1]
sign_7_7 = [1, -1, 1, -1, 1, -1, 1, 1]
sign_9_35 = [-1, -1, -1, -1, -1, -1, -1, -1, -1, 1]



#This function tells you which 3-cell your head is in if you stand on the strand i with A(i,2) on your right.
#Input the overstrand list and color list. 
def where(overstrand_list,color_list):
    #First make a variable for the number of crossings for convenience and initialize the list to be returned.
    num_crossings = len(overstrand_list)
    where_list = []
    
    #Using the set colorSet makes it easier for us to eliminate the wrong colors. colorSet starts with all 3 colors.
    colorSet = set()
    colorSet.add(1)
    colorSet.add(2)
    colorSet.add(3)
    
    #We discard the color of strand 0, since it is impossible for your head to be in the 3-cell of the color of the same strand you're on. 
    colorSet.discard(color_list[0])
    
    #Choose one of the other colors left behind arbitrarily to be your starting 3-cell
    #If the color chosen is the color of the overstrand you are standing upright. If it is the other color, you are upside down on strand 0. 
    where_list.append(colorSet.pop())
    
    #Go through each of the crossings, not counting crossing 0. 
    for i in range(1,num_crossings):
        #If you were standing upright on your last strand, you will be standing upright again on this strand in the same 3-cell.
        #The top part of the diagram should be within the 3-cell corresponding to the color of the overstrand.
        #So if you're standing upright in the top, you will be in the overstrand color 3-cell regardless of which strand you're on.
        if( where_list[i-1] == color_list[overstrand_list[(i-1)%num_crossings]]):
            where_list.append(where_list[i-1])
        
        #If you were standing upside down on the last strand, you will be standing upside down in a different 3-cell.
        elif( where_list[i-1] != color_list[overstrand_list[(i-1)%num_crossings]]):
            #Using colorSet, we can eliminate the 3-cell of the last strand and the 3-cell of the overstrand.
            #The remaining 3-cell will correspond to this strand.
            colorSet = set()
            colorSet.add(1)
            colorSet.add(2)
            colorSet.add(3)
            colorSet.discard(where_list[i-1])
            colorSet.discard(color_list[overstrand_list[(i-1)%num_crossings]])
            where_list.append(colorSet.pop())
        
    return where_list

#testing print statements
where_3_1 = where( overstrand_3_1 , color_3_1 )
where_6_1 = where( overstrand_6_1 , color_6_1 )
where_7_4 = where( overstrand_7_4 , color_7_4 )
where_7_7 = where( overstrand_7_7 , color_7_7 )
where_9_35 = where( overstrand_9_35  , color_9_35 )

# print(where_3_1)
# print(where_6_1)
# print(where_7_4)
# print(where_7_7)
# print(where_9_35)
    
    
#This function outputs the matrix containing x_i, x_i+1, x_f(i) and a constant. This relies on using epsilon rules. 
def initialize_matrix(overstrand_list,color_list,where_list,sign_list):
   #Make a starting matrix of all 0s. (I think the initialization of epsilons one and two is doing nothing. Remove later?).
   x_matrix = [[0]*(len(overstrand_list)+1) for i in range(len(overstrand_list))]
   epsilon_one = 0
   epsilon_two = 0
    
   #Now we need to find the signs of the first two epsilons.
   #Loop through each of the crossings
   for i in range(len(overstrand_list)):
      #initialize epsilon_three so we can see if a crossing is inhomogeneous or not easily
      epsilon_one = 0
      epsilon_two = 0
      epsilon_three = 0
      
      #epsilon one is positive if the color of i is not equal to the where of the overstrand.
      #standing upside down on 
      if(color_list[i] == where_list[overstrand_list[i]]):
         epsilon_one = 1
      else:
         epsilon_one = -1


      #epsilon two is positive if the color of the overstrand is equal to the where of i. 
      if(color_list[overstrand_list[i]] == where_list[i]):
         epsilon_two = 1
      else:
         epsilon_two = -1

      #see if we have an epsilon three. this would happen if all three strands are the same color (homogeneous crossing)
      if(color_list[i]==color_list[(i+1)%len(overstrand_list)]==color_list[overstrand_list[i]]):
         #epsilon 3 is negative if where of i is the same as where of the overstrand.
         if(where_list[i] == where_list[overstrand_list[i]]):
            epsilon_three = -1
         else:
            epsilon_three = 1

      #now we need to add the equation information to this row of the matrix.
      x_matrix[i][i] +=1
      x_matrix[i][(i+1)%len(overstrand_list)] -=1
      
      #edits as a heterogenous crossing
      if epsilon_three == 0:
         #edit the overstrand coefficient
         x_matrix[i][overstrand_list[i]] += (epsilon_one*epsilon_two)
         #edit the constant on the LEFT side of the equation (the equation will be set equal to 0?)
         x_matrix[i][len(overstrand_list)] += -(sign_list[i]*epsilon_two)
             
      #edits as a homogenous crossing
      else:
         #edit overstrand coefficient. constant is 0. 
         x_matrix[i][overstrand_list[i]] += 2*epsilon_three


   #print("MATRIX")
   #print(x_matrix)
   
   #return row reduced version of matrix
   return sympy.Matrix(x_matrix).rref()[0] #x_matrix #

#testing
matrix_3_1 = initialize_matrix(overstrand_3_1, color_3_1, where_3_1, sign_3_1 )
matrix_6_1 = initialize_matrix(overstrand_6_1, color_6_1, where_6_1 ,sign_6_1 )
matrix_7_4 = initialize_matrix(overstrand_7_4, color_7_4, where_7_4 ,sign_7_4 )
matrix_7_7 = initialize_matrix(overstrand_7_7, color_7_7, where_7_7 ,sign_7_7 )
matrix_9_35 = initialize_matrix(overstrand_9_35, color_9_35, where_9_35 , sign_9_35 )

# print(matrix_3_1)
# print(matrix_6_1)
# print(matrix_7_4)
# print(matrix_7_7)
# print(matrix_9_35)

def solve_2chain(rref_matrix):
    #print("RREF MATRIX:")
    #print(rref_matrix)
    number_rows = int(math.sqrt(len(rref_matrix)))
    number_cols = int(len(rref_matrix)/number_rows)-1
    x_values = []
    for i in range(number_cols):
        x_values.append(0)
        
    #print("X VALUES START ", x_values)
    for i in range(number_rows):
        #print("on row ",i, " out of ", number_rows)
        #print("check for ", (number_rows*i)+i, " through ", (number_rows*i)+i+number_cols)
        for j in range(number_cols):
            #print("on col ", j, " out of ", number_cols)
            value = rref_matrix[(number_rows*i)+i+j]
            if value != 0:
                x_values[j] = rref_matrix[(number_rows*i)+i+number_cols]
                break
    #print("ummmm x values now: ", x_values)
    
    for x in range(len(x_values)):
        x_values[x] = -x_values[x]
        
    return x_values

# print("3_1 two chain")
# print(solve_2chain(sympy.Matrix([[1, -1, -1, 0, -1], [1, 1, -1, 0, 1], [0, 1, 1, -1, -1], [-1, 0, 0, -1, 0]]).rref()[0]))
# print("6_1")
# print(solve_2chain(sympy.Matrix([[1, -1, -1, 0, 0, 0, -1], [0, 1, -1, 0, 1, 0, -1], [-1, 0, 1, -1, 0, 0, 1], [0, 0, 0, 1, -1, -1, -1], [0, 1, 0, 0, 1, -1, -1], [-1, 0, 0, -1, 0, 1, 1]]).rref()[0]))
# print("7_4")
# print(solve_2chain(sympy.Matrix([[1, -1, 0, 0, 0, 1, 0, 0, 1], [0, 1, -1, 0, 1, 0, 0, 0, -1], [-1, 0, 1, -1, 0, 0, 0, 0, -1], [0, 0, 0, 1, -1, 0, 1, 0, 1], [0, 1, 0, 0, 1, -1, 0, 0, -1], [0, 0, 2, 0, 0, 1, -1, 0, 0], [0, 0, 0, 1, 0, 0, 1, -1, 1], [-1, 0, 0, 0, 0, 0, 0, -1, 0]]).rref()[0]))
# print("7_7")
# print(solve_2chain(sympy.Matrix([[1, -1, 0, 0, -1, 0, 0, 0, -1], [0, 1, -1, -1, 0, 0, 0, 0, -1], [0, 0, 1, -1, 0, 0, -1, 0, -1], [0, 0, 0, 1, -1, -1, 0, 0, 1], [-1, 0, 0, 0, 1, -1, 0, 0, 1], [0, -2, 0, 0, 0, 1, -1, 0, 0], [0, 0, -1, 0, 0, 0, 1, -1, 1], [-1, 0, 0, 0, 0, 0, 0, -1, 0]]).rref()[0]))
# print("9_35")
# print(solve_2chain(sympy.Matrix([[1, -1, 0, 0, 0, 0, -2, 0, 0, 0, 0], [0, 1, -1, 0, 0, -2, 0, 0, 0, 0, 0], [0, 0, 1, -1, 0, 0, 0, 1, 0, 0, -1], [1, 0, 0, 1, -1, 0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 1, -1, 0, 0, 1, 0, -1], [0, -2, 0, 0, 0, 1, -1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 1, -1, 0, 0, -1], [0, 0, 1, 0, 0, 0, 0, 1, -1, 0, -1], [0, 0, 0, 0, 1, 0, 0, 0, 1, -1, -1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0]]).rref()[0]))


def intersecting_cells(overstrand_list,color_list,where_list,sign_list):
  """
      goes through all the crossings
      at crossing i the color of the overstrand[i] is the same as where[i]
        then the lift passes through the cell A_(1,i)
      otherwise overstrand[i] is not the same as where[i]
      thus the lift passes through the cell A_(2,i) or A_(3,i)
        if positive crossing
            if where[overstrand[i]] == color[i]
                then the lift passes through A_(3,i)
            else
                then the lift passes through A_(2,i)
        else negative crossing
            if where[overstrand[i]] == color[i]
                then the lift passes through A_(2,i)           
            else
                then the lift passes through A_(3,i)
  """
  num_crossings = len(overstrand_list)
  intersect_list = [0]*(num_crossings*2)

  
  for i in range(num_crossings):
    #see if the crossing is homog or heterog
    if color_list[i] == color_list[int((i+1)%num_crossings)] and color_list[i] == color_list[overstrand_list[i]] and color_list[int((i+1)%num_crossings)] == color_list[overstrand_list[i]]:
        #print("homogeneous crossing")
        if where_list[overstrand_list[i]] == where_list[i]:
            intersect_list[i+num_crossings] -= 1
        elif where_list[overstrand_list[i]] != where_list[i]:
            intersect_list[i+num_crossings] += 1
        
    else:
        #print("heterogeneous crossing")
        if color_list[overstrand_list[i]] == where_list[i]:
          intersect_list[i] += 1
        elif color_list[overstrand_list[i]] != where_list[i]:
          if sign_list[i] == 1:
            if where_list[overstrand_list[i]] == color_list[i]:
              intersect_list[i+num_crossings] -= 1
            elif where_list[overstrand_list[i]] != color_list[i]:
              intersect_list[i+num_crossings] += 1
          else:
            if where_list[overstrand_list[i]] == color_list[i]:
              intersect_list[i+num_crossings] += 1
            elif where_list[overstrand_list[i]] != color_list[i]:
              intersect_list[i+num_crossings] -= 1
  return intersect_list





def linking_number(overstrand_list, sign_list, color_list):
  """ 

  """
  # first call on all helper functions
  where_list = where(overstrand_list,color_list)
  #print(where_list)
  rref_matrix = initialize_matrix(overstrand_list,color_list,where_list,sign_list)
  #print("rref_matrix")
  #print(rref_matrix)
  two_chain = solve_2chain(rref_matrix)
  #print("two_chain")
  #print(two_chain)
  intersect_list = intersecting_cells(overstrand_list,color_list,where_list,sign_list)
  #print(intersect_list)
  num_crossings = len(overstrand_list)

  linking_number = 0

  for i in range(len(intersect_list)):
    #if it's an A_(1,i) surface
    if i < num_crossings: 
      #print("overstrand ", overstrand_list[i])
      #print("sign", sign_list[i])
      linking_number += intersect_list[i]*sign_list[i]
      #print("add ", intersect_list[i]*sign_list[i])
    #if it's a A_(2 or 3, i) with two_chain[i] numbers of crossings
    elif i >= num_crossings: 
      #print("overstrand ", overstrand_list[i-num_crossings])
      #print("sign", sign_list[i-num_crossings])
      linking_number += intersect_list[i]*two_chain[i-num_crossings]*sign_list[i-num_crossings]
      #print("add ", intersect_list[i]*two_chain[i-num_crossings]*sign_list[i-num_crossings])
  return linking_number


print('trefoil')
print(linking_number(overstrand_3_1, sign_3_1, color_3_1))
print('6_1')
print(linking_number(overstrand_6_1, sign_6_1 , color_6_1))
print('7_4')
print(linking_number(overstrand_7_4, sign_7_4 , color_7_4))
print('7_7')
print(linking_number(overstrand_7_7, sign_7_7 , color_7_7))
print('9_35')
print(linking_number(overstrand_9_35, sign_9_35 , color_9_35))



 





#print('trefoil where_list'+str(where([2, 0, 1, 3],[1, 2, 3, 1])))
#where_list_trefoil = where([2, 0, 1, 3],[1, 2, 3, 1])
#rref_matrix_trefoil = initialize_matrix([2, 0, 1, 3],[1, 2, 3, 1],where_list_trefoil,[1, 1, 1, 1])
#twochain_trefoil = solve_2chain(rref_matrix_trefoil)
#intersect_list_trefoil = intersecting_cells([2, 0, 1, 3],[1, 2, 3, 1],where_list_trefoil,[1, 1, 1, 1])
# print('trefoil')
# print('we got '+str(linking_number([2, 0, 1, 3],[1, 1, 1, 1],[1, 2, 0, 1])))
# print()
# print('patricia got 2')
# print('6_1')
# print('we got '+str(linking_number([2, 4, 0, 5, 1, 3] , [1, -1, 1, 1, -1, 1] , [0, 2, 1, 2, 0, 1])))
# print()
# print('patricia got -2')
# print('7_4')
# print('we got '+str(linking_number([5, 4, 0, 6, 1, 2, 3, 7] , [-1, -1, -1, -1, -1, -1, -1, 1] , [1, 2, 0, 2, 1, 0, 0, 1])))
# print()
# print('patricia got 2')
# print('7_7')
# print('we got '+str(linking_number([4, 3, 6, 5, 0, 1, 2, 7] , [1, -1, 1, -1, 1, -1, 1, 1] , [1, 0, 2, 1, 2, 0, 0, 1])))
# #print()
# print('patricia got -2')
# print('9_35')
# print(linking_number([6, 5, 7, 0, 8, 1, 3, 2, 4, 9],[-1, -1, -1, -1, -1, -1, -1, -1, -1, 1],[2, 2, 2, 1, 0, 2, 2, 0, 1, 2]))
#where_list_6_1 = where_list([2, 4, 0, 5, 1, 3],[3, 2, 1, 2, 3, 1])
#print('6_1 knot ' + str(where_list_6_1))
#rref_matrix_6_1 = initialize_matrix([2, 4, 0, 5, 1, 3],[3, 2, 1, 2, 3, 1],where_list_6_1,[1, -1, 1, 1, -1, 1])
#solve_2chain(rref_matrix_6_1)
