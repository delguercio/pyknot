

#
#
#  Program to calculate the Dihedral Linking Numbers for
#  three colored knots
#
#

import sympy
import math


def where(overstrand_list,color_list):
    """
        this function outputs the universe your head is in if
        your right hand is in A_(i,2) and you are walking in
        the direction the knot is oriented

        you travel along the strands from 0->1->2->...->n-1

        at the 0th crossing
        you initialize where(0th strand) to be the same
        universe as the color of the overstrand

        this means that where(1st strand) = same universe
        as the color of the overstrand

        now you approach the 1st crossing
        if where(1st strand) = color of the overstrand at 1st crossing
            then where(2nd strand) = color of the overstrand at 2nd crossing
        else where(1st strand) != color of the overstrand at 2nd crossing
            then where(2nd strand) = the third color 
    """
    where_list = []
    colors = [1,2,0]
    for i in range(len(overstrand_list)):
        #print("We are on strand ", i)
        if i == 0:
            where_list.append(color_list[overstrand_list[0]])
            #print("We initialized the first strand: ", where_list)
        elif i == 1:
            where_list.append(color_list[overstrand_list[0]])
            #print("We initialized the second strand: ", where_list)
        
        else:
            color_of_overstrand = color_list[overstrand_list[i-1]]
            universe_of_incoming_understrand = where_list[i-1]
            #print('COLOR OF OVERSTRAND')
            #print(color_of_overstrand)
            #print('UNIVERSE OF INCOMING UNDERSTRAND')
            #print(universe_of_incoming_understrand)
            
            if universe_of_incoming_understrand == color_of_overstrand:
                where_list.append(color_of_overstrand)
                #print(where_list)
            else:
                colors.remove(color_of_overstrand)
                colors.remove(universe_of_incoming_understrand)
                #print(colors)
                where_list.append(colors[0])
                #print(where_list)
                colors = [1,2,0]
    return where_list

def initialize_matrix(overstrand_list,color_list,where_list,sign_list):
   #how big does the matrix need to be?
   #we have number of columns = number of strands, number of rows = number of crossings.... hm

   x_matrix = [[0]*(len(overstrand_list)+1) for i in range(len(overstrand_list))]
   #print("STARTING MATRIX")
   #print(x_matrix)
   epsilon_one = 0
   epsilon_two = 0
   #Great! now find epsilon signs. :)
   #need a loop for each of the crossings

   for i in range(len(overstrand_list)):
      #initialize epsilon_three so we can see if a crossing is inhomogeneous or not easily
      #epsilon_one = 0
      #epsilon_two = 0
      epsilon_three = 0
      '''print('for equation '+str(i))
      print('epsilon_one')
      print(epsilon_one)
      print('epsilon_two')
      print(epsilon_two)
      print('epsilon_three')
      print(epsilon_three)'''
      
      #epsilon one is positive if the color of i is not equal to the where of the overstrand.
      
      if(color_list[i] == where_list[overstrand_list[i]]):
         epsilon_one = -1
      else:
         epsilon_one = 1


      #epsilon two is positive if the color of the overstrand is equal to the where of
         
      if(color_list[overstrand_list[i]] == where_list[i]):
         epsilon_two = 1
      else:
         epsilon_two = -1

      '''print('for equation'+str(i))
      print('epsilon_one')
      print(epsilon_one)
      print('epsilon_two')
      print(epsilon_two)
      print('epsilon_three')
      print(epsilon_three)'''

      #see if we have an epsilon three. this would happen if all three strands are the same color (homogeneous crossing)

      if(color_list[i]==color_list[(i+1)%len(overstrand_list)]==color_list[overstrand_list[i]]):
         #print("HOMOGENOUS CROSSING!")
         if(where_list[i] == where_list[overstrand_list[i]]):
            epsilon_three = -1
         else:
            epsilon_three = 1
         #print("epsilon three: ", epsilon_three )


      #now we need to add the equation information to this row of the matrix.
      x_matrix[i][i]+=1
      x_matrix[i][(i+1)%len(overstrand_list)]-=1
      #print("NEW MATRIX")
      #print(x_matrix)
      
      if epsilon_three == 0:
         #print('this')
         #print(x_matrix[i][overstrand_list[i]])
         #CHANGED THIS 
         x_matrix[i][overstrand_list[i]] += (epsilon_one*epsilon_two)
         #print('changed to')
         #print(x_matrix[i][overstrand_list[i]])
         #ALSO CHANGED THIS ON THE SIGN STUFF TO SEE NOW IT IS THE SAME AS PATRICIAS CODE
         x_matrix[i][len(overstrand_list)] -= sign_list[i]*epsilon_two

         #print("NEW MATRIX")
         #print(x_matrix)

      else:
         x_matrix[i][overstrand_list[i]] += 2*epsilon_three

      #print("NEW MATRIX")
      #print(x_matrix)

   #print("FINISHED MATRIX")
   #print(sympy.Matrix(x_matrix).rref()[0])
   return sympy.Matrix(x_matrix).rref()[0]

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

def intersecting_cells(overstrand_list,color_list,where_list,sign_list):
  """
      goes through all the crossings
      at crossing i the color of the overstrand[i] is the same as where[i]
        then the lift passes through the cell A_(1,i)
      otherwise overstrand[i] is not the same as where[i]
      thus the lift passes through the cell A_(2,i) or A_(3,i)
        if positive crossing
            if where[overstrand[i]] == color[i]
                then the lift passes through A_(2,i)
            else
                then the lift passes through A_(3,i)
        else negative crossing
            if where[overstrand[i]] == color[i]
                then the lift passes through A_(3,i)           
            else
                then the lift passes through A_(2,i)
  """
  num_crossings = len(overstrand_list)
  intersect_list = [0]*(num_crossings*2)

  
  for i in range(num_crossings):
    #see if the crossing is homog or heterog
    if color_list[i] == color_list[int((i+1)%num_crossings)] and color_list[i] == color_list[overstrand_list[i]] and color_list[int((i+1)%num_crossings)] == color_list[overstrand_list[i]]:
        #print("homogeneous crossing")
        if sign_list[i] == 1:
            if where_list[overstrand_list[i]] == where_list[i]:
                intersect_list[i+num_crossings] += 1
            elif where_list[overstrand_list[i]] != where_list[i]:
                intersect_list[i+num_crossings] -= 1
        elif sign_list[i] == -1:
            if where_list[overstrand_list[i]] == where_list[i]:
                intersect_list[i+num_crossings] += 1
            elif where_list[overstrand_list[i]] != where_list[i]:
                intersect_list[i+num_crossings] -= 1
        
    else:
        #print("heterogeneous crossing")
        if color_list[overstrand_list[i]] == where_list[i]:
          intersect_list[i] += 1
        elif color_list[overstrand_list[i]] != where_list[i]:
          if sign_list[i] == 1:
            if where_list[overstrand_list[i]] == color_list[i]:
              intersect_list[i+num_crossings] += 1
            elif where_list[overstrand_list[i]] != color_list[i]:
              intersect_list[i+num_crossings] -= 1
          else:
            if where_list[overstrand_list[i]] == color_list[i]:
              intersect_list[i+num_crossings] -= 1
            elif where_list[overstrand_list[i]] != color_list[i]:
              intersect_list[i+num_crossings] += 1
        
  return intersect_list

def Degree1Surface(overstrand_list, sign_list, color_list):
  """ 

  """
  # first call on all helper functions
  where_list = where(overstrand_list,color_list)
  #print(where_list)
  rref_matrix = initialize_matrix(overstrand_list,color_list,where_list,sign_list)
  print("rref_matrix")
  print(rref_matrix)
  two_chain = solve_2chain(rref_matrix)
  print("two_chain")
  print(two_chain)
  intersect_list = intersecting_cells(overstrand_list,color_list,where_list,sign_list)
  #print(intersect_list)
  num_crossings = len(overstrand_list)

  linking_number = 0

  for i in range(len(intersect_list)):
    #if it's an A_(1,i) surface
    if i < num_crossings: 
      print("overstrand ", overstrand_list[i])
      print("sign", sign_list[i])
      linking_number += intersect_list[i]*sign_list[i]
      print("add ", intersect_list[i]*sign_list[i])
    #if it's a A_(2 or 3, i) with two_chain[i] numbers of crossings
    elif i >= num_crossings: 
      print("overstrand ", overstrand_list[i-num_crossings])
      print("sign", sign_list[i-num_crossings])
      linking_number += intersect_list[i]*two_chain[i-num_crossings]*sign_list[i-num_crossings]
      print("add ", intersect_list[i]*two_chain[i-num_crossings]*sign_list[i-num_crossings])
  return linking_number



#print('trefoil where_list'+str(where([2, 0, 1, 3],[1, 2, 3, 1])))
#where_list_trefoil = where([2, 0, 1, 3],[1, 2, 3, 1])
#rref_matrix_trefoil = initialize_matrix([2, 0, 1, 3],[1, 2, 3, 1],where_list_trefoil,[1, 1, 1, 1])
#twochain_trefoil = solve_2chain(rref_matrix_trefoil)
#intersect_list_trefoil = intersecting_cells([2, 0, 1, 3],[1, 2, 3, 1],where_list_trefoil,[1, 1, 1, 1])
print('trefoil')
print('we got '+str(Degree1Surface([2, 0, 1, 3],[1, 1, 1, 1],[1, 2, 0, 1])))
print('patricia got 2')
print('6_1')
print('we got '+str(Degree1Surface([2, 4, 0, 5, 1, 3] , [1, -1, 1, 1, -1, 1] , [0, 2, 1, 2, 0, 1])))
print('patricia got -2')
print('7_4')
print('we got '+str(Degree1Surface([5, 4, 0, 6, 1, 2, 3, 7] , [-1, -1, -1, -1, -1, -1, -1, 1] , [1, 2, 0, 2, 1, 0, 0, 1])))
print('patricia got 2')
print('7_7')
print('we got '+str(Degree1Surface([4, 3, 6, 5, 0, 1, 2, 7] , [1, -1, 1, -1, 1, -1, 1, 1] , [1, 0, 2, 1, 2, 0, 0, 1])))
print('patricia got -2')
#where_list_6_1 = where_list([2, 4, 0, 5, 1, 3],[3, 2, 1, 2, 3, 1])
#print('6_1 knot ' + str(where_list_6_1))
#rref_matrix_6_1 = initialize_matrix([2, 4, 0, 5, 1, 3],[3, 2, 1, 2, 3, 1],where_list_6_1,[1, -1, 1, 1, -1, 1])
#solve_2chain(rref_matrix_6_1)
