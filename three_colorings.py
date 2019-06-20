## 
##
##
##
## this is a program that creates a three coloring for a knot
## 
##
##
##
##

import re

def create_dict(overstrand_list):
    """
        you know that the first crossing will have strands 0 and 1
        the second crossing will have strands 1 and 2 and so on
        you can know the third strand at the nth crossing by checking
        what is at the nth position of the overstrand_list.
        If odd, an extra loop was added at the end of the overstrand_list
        so to compensate for that if the last index equals the last value
        that means there a loop that crosses over itself and it will always
        have the 0th strand and then itself twice. the last strand will 
        not cross itself unless you put in a loop.
        input: overstrand_list
        output: dictionary where the keys are the index of the 
                crossing and then the value is a list of the
                strand number and color of the strand at that
                crossing 
                {0:[[0,'z'],[1,'z'],[2,'z']],
                 1:[[0,'z'],[1,'z'],[2,'z']],
                 2:[[0,'z'],[1,'z'],[2,'z']],
                 3:[[0,'z'],[3,'z'],[3,'z']]}
    """
    knot_dict = {}
    # make raw dict that only has the adjacent crossings in it
    # :)
    num_strand = len(overstrand_list)
    last_index = num_strand-1
    if last_index == overstrand_list[last_index]:
        for i in range(num_strand-1):
            knot_dict.update({ i : [[i,'z'],[i+1,'z'], [overstrand_list[i],'z']] })
        knot_dict.update({ last_index : [[last_index,'z'],[last_index,'z'], [0,'z']] })
        return knot_dict
    else:
        for i in range(num_strand):
            knot_dict.update({ i : [[i%num_strand,'z'],[(i+1)%num_strand,'z'],[overstrand_list[i],'z']] })
        return knot_dict


def color_strand(knot_dict,strand,color):
    """
        this is a helper function for three_color it will take in
        a knot dictionary and then output a the same knot dictionary
        except the specified strand will be colored the specified
        color

        input: knot_dict, strand (an integer), color (a string)
        output: another knot dictionary with changed color of strand
    """
    for k,v in knot_dict.items():
        for i in range(len(v)):
            if strand in v[i]:
                knot_dict[k][i][1] = color
    return knot_dict


def uncolor(knot_dict):
    """
        takes any knot_dict and makes is all z's
    """
    for k,v in knot_dict.items():
        for i in range(len(v)):
            knot_dict[k][i][1] = 'z'
    return knot_dict


def isValid(knot_dict):
    """
        goes through entire knot and returns "True" if knot_dict
        contains no invalid crossings returns "False if knot_dict
        contains an invalid crossing
        creates a list of strings of all the color combinations
        in the knot and then if there are any combinations with
        two of one color that's not a z then it's False
    """
    color_list = []
    crossing_colors_str = ''
    for k,v in knot_dict.items():
        for i in range(len(v)):
            #print(knot_dict[k][i])
            crossing_colors_str += knot_dict[k][i][1]
        color_list.append(crossing_colors_str)
        crossing_colors_str = ''

    regex = re.compile('aa[b|c]|bb[a|c]|cc[a|b]|a[b|c]a|b[a|c]b|c[a|b]c|[b|c]aa|[a|c]bb|[a|b]cc')
    #'aa[b|c|z]|bb[a|c|z]|cc[a|b|z]|a[b|c|z]a|b[a|c|z]b|c[a|b|z]c|[b|c|z]aa|[a|c|z]bb|[a|b|z]cc'
    for crossing in color_list:
        matchedObj = re.match(regex, crossing)
        #print(matchedObj)
        if matchedObj != None:
            return False
    return True
    """


def isDone(knot_dict):
        if you pass isValid and you don't have any z's (uncolored strands)
        then you return True
        else return False

    if isValid(knot_dict) == True:
        for k,v in knot_dict.items():
            for i in range(len(v)):
                crossing_colors_str += knot_dict[k][i][1]
        if 'z' in crossing_colors_str:
            return False
        else:
    else:
        return False

    """

#seven_four = {0:[[0,'c'],[3,'c'],[4,'z']],
#              1:[[0,'z'],[1,'z'],[3,'z']],
#              2:[[1,'z'],[4,'z'],[5,'z']],
#              3:[[1,'z'],[2,'z'],[6,'z']],
#              4:[[2,'z'],[5,'z'],[6,'z']],
#              5:[[2,'z'],[3,'z'],[5,'z']],
#              6:[[0,'z'],[4,'z'],[6,'z']] }

#print(isValid(seven_four))

def needs_color(strands):
    """
        tnhe list of list of the strands and
        outputs the color that's missing if it has [color, color, uncolored]
        outputs nothing if it's missing more than one color
    """
    crossing_colors_str = ''
    for strand in strands:
        crossing_colors_str += strand[1]
    if 'z' in crossing_colors_str:
        if 'a' in crossing_colors_str:
            if 'b' in crossing_colors_str:
                return ('c',crossing_colors_str.index('z'))
            elif 'c' in crossing_colors_str:
                return ('b',crossing_colors_str.index('z'))
            else:
                return ('a',crossing_colors_str.index('z'))
        elif 'b' in crossing_colors_str:
            if 'a' in crossing_colors_str:
                return ('c',crossing_colors_str.index('z'))
            elif 'c' in crossing_colors_str:
                return ('a',crossing_colors_str.index('z'))
            else:
                return ('b',crossing_colors_str.index('z'))            
        elif 'c' in crossing_colors_str:
            if 'a' in crossing_colors_str:
                return ('b',crossing_colors_str.index('z'))
            elif 'b' in crossing_colors_str:
                return ('a',crossing_colors_str.index('z'))
            else:
                return ('c',crossing_colors_str.index('z'))
        else:
            return ('z',-1)
    else:
        return ('z',-1)

#print(needs_color([[0,'c'],[4,'b'],[5,'b']]))
#print(needs_color([[0,'z'],[4,'z'],[5,'b']]))
#print(needs_color([[0,'c'],[4,'c'],[5,'z']]))

def threecolor_crossing(knot_dict,strands,crossing_index,coloring_type):
    """
        make a string of all of the colors in the crossing
        then if it's all z's color it ['a','b','c']
        if it contains two z's needs_color(strands)[1] = -1
        otherwise 0 <= needs_color(strands)[1] <= 2 in which case you color it

    """
    crossing_colors_str = ''
    for strand in strands:
        crossing_colors_str += strand[1]

    if crossing_colors_str == 'zzz': #it's not colored at all so color it
        colors = ['a','b','c']
        for strand in enumerate(strands):
            color_strand(knot_dict,strand[1][0],colors[strand[0]])
        return knot_dict
    elif needs_color(strands)[1] >= 0: # it's z so fill it in
        color_needed = needs_color(strands)[0]
        index_of_strand_on_strands = needs_color(strands)[1]
        color_strand(knot_dict, strands[index_of_strand_on_strands][0], color_needed)
        return knot_dict
    else: #it's 'zz' so don't do anything
        return knot_dict

def threecolor_crossing_alt_init(knot_dict,strands):
    """
        make a string of all of the colors in the crossing
        then if it's all z's color it ['a','a','a']
        if it contains two z's needs_color(strands)[1] = -1
        otherwise 0 <= needs_color(strands)[1] <= 2 in which case you color it

    """
    crossing_colors_str = ''
    for strand in strands:
        crossing_colors_str += strand[1]

    if crossing_colors_str == 'zzz': #it's not colored at all so color it
        colors = ['a','a','a']
        for strand in enumerate(strands):
            color_strand(knot_dict,strand[1][0],colors[strand[0]])
        return knot_dict
    elif needs_color(strands)[1] >= 0: # it's z so fill it in
        color_needed = needs_color(strands)[0]
        index_of_strand_on_strands = needs_color(strands)[1]
        color_strand(knot_dict, strands[index_of_strand_on_strands][0], color_needed)
        return knot_dict
    else: #it's 'zz' so don't do anything
        return knot_dict

def three_color(knot_dict):
    """
        go to first crossing, color each strand in it
    """ 




 
        #for strand in enumerate(strands): #strand[0] is index strand[1] is item
        #    for color in colors:
        #        if isValid(color_strand(knot_dict,strand[1][0],color)):
        #            knot_dict = color_strand(knot_dict,strand,color)
        #            print("I'm here first"+str(strand)+"and color"+color)
        #            print(knot_dict)
        #            continue
        #        else:
        #            print("I'm on strand"+str(strand)+"and color"+color)
        #            continue


            #for color in colors:
            #    color_strand(knot_dict,strand[0],color)
            #    print(color_strand(knot_dict,strand[0],color))
                                          # change the secon
        #color_strand(strand,crossing,knot_dict)
        #print("Done!")
    


three_one = {0:[[0,'z'],[1,'z'],[2,'z']],
             1:[[0,'z'],[1,'z'],[2,'z']],
             2:[[0,'z'],[1,'z'],[2,'z']]}

six_one = {0:[[0,'z'],[4,'z'],[5,'z']],
           1:[[0,'z'],[1,'z'],[4,'z']],
           2:[[1,'z'],[3,'z'],[4,'z']],
           3:[[1,'z'],[2,'z'],[3,'z']],
           4:[[0,'z'],[2,'z'],[5,'z']],
           5:[[2,'z'],[3,'z'],[5,'z']] }

seven_four = {0:[[0,'z'],[3,'z'],[4,'z']],
              1:[[0,'z'],[1,'z'],[3,'z']],
              2:[[1,'z'],[4,'z'],[5,'z']],
              3:[[1,'z'],[2,'z'],[6,'z']],
              4:[[2,'z'],[5,'z'],[6,'z']],
              5:[[2,'z'],[3,'z'],[5,'z']],
              6:[[0,'z'],[4,'z'],[6,'z']] }
#seven_seven = 

#print(three_color(three_one))
#print(three_color(six_one))

#print(three_color(seven_four))

"""
    # go to first crossing, color each strand in it

    for crossing,strands in knot_dict.items():
        if isValid(knot_dict) == False:
            uncolor(knot_dict) 
        #print("crossing is "+str(crossing))
        #print("strands are "+str(strands))
        threecolor_crossing(knot_dict,strands)
        #print(knot_dict)
        if isValid(knot_dict) == False:
            uncolor(knot_dict)
            threecolor_crossing_alt_init(knot_dict,knot_dict[0])
            if isValid(knot_dict) == False:
                uncolor(knot_dict)
                threecolor_crossing_alt_init(knot_dict,knot_dict[0])
                for crossing,strands in knot_dict.items(): 
                    #print("crossing is "+str(crossing))
                    #print("strands are "+str(strands))
                    threecolor_crossing(knot_dict,strands)
                    #print(knot_dict)
                    break
                return knot_dict
    return knot_dict

"""

#def make_it_work(crossing):#like [[0,'z'],[4,'z'],[5,'z']]
"""
        as a mathematian, not a computer scientist, i feel like my
        code can be kind of silly and not super efficient
        in the words of Tim Gunn s/o my parents this function makes
        a crossing work
        if it's full of z's just make it 'a' 'b' 'c' 
        if it just needs one more, fill her in
        otherwise: do nothing! it's not your concern at this point
        you're just trying to make it work
"""

"""    existing_colors = ''
    made_it_work = []
    color = 'abc' # need regex :,)
    for strand in crossing:
        existing_colors = existing_colors+strand[1]
    if 'zzz' in existing_colors:
        for strand in enumerate(crossing):
            made_it_work = made_it_work + [[strand[1][0],color[strand[0]]]]
        return made_it_work
    elif 'zz' in existing_colors and 'zzz' not in existing_colors:

    elif 'z' in existing_colors:
        if 'a' in existing_colors:
    else:

    return made_it_work #,existing_colors[]]

"""
