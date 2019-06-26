

#
#
#  Program to calculate the Dihedral Linking Numbers for
#  three colored knots
#
#


def where_list(overstrand_list,color_list):
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
    colors = [0,1,2]
    for i in range(len(overstrand_list)):
        if i == 0:
            where_list.append(color_list[0])
            #print(where_list)
        color_of_overstrand = color_list[overstrand_list[i]]
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
            colors = [0,1,2]
    return where_list

def initialize_matrix(overstrand_list,color_list,where_list,sign_list):
   #how big does the matrix need to be?
   #we have number of columns = number of strands, number of rows = number of crossings.... hm

   x_matrix = [[0]*(len(overstrand_list)+1) for i in range(len(overstrand_list))]
   print("STARTING MATRIX")
   print(x_matrix)

   #Great! now find epsilon signs. :)
   #need a loop for each of the crossings

   for i in range(len(overstrand_list)):
      #initialize epsilon_three so we can see if a crossing is inhomogeneous or not easily
      epsilon_three = 0

      
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


      #see if we have an epsilon three. this would happen if all three strands are the same color (homogeneous crossing)

      if(color_list[i]==color_list[(i+1)%len(overstrand_list)]==color_list[overstrand_list[i]]):
         print("HOMOGENOUS CROSSING!")
         if(where_list[i] == where_list[overstrand_list[i]]):
            epsilon_three = -1
         else:
            epsilon_three = 1


      #now we need to add the equation information to this row of the matrix.
      x_matrix[i][i]+=1
      x_matrix[i][(i+1)%len(overstrand_list)]+=1

      
      if epsilon_three == 0:
         x_matrix[i][overstrand_list[i]]+= (epsilon_one*epsilon_two)
         x_matrix[i][len(overstrand_list)] -= sign_list[i]*epsilon_one

      else:
         x_matrix[i][overstrand_list[i]] += 2*epsilon_three

      print("NEW MATRIX")
      print(x_matrix)
      
print('trefoil '+str(where_list([2, 0, 1, 3],[1, 2, 0, 1])))
where_list_trefoil = where_list([2, 0, 1, 3],[1, 2, 0, 1])
initialize_matrix([2, 0, 1, 3],[1, 2, 0, 1],where_list_trefoil,[1, 1, 1, 1])
#print('6_1 '+str(where_list([2, 4, 0, 5, 1, 3],[0, 2, 1, 2, 0, 1])))
