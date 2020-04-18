def BraidToGauss(braid):
        # Creates a Gauss code from the braid notation.
        gauss = []
        i = 0
        currentstrand = 0

        crossings = {}
        for i in range(len(braid)):
                crossings[i] = 0
                
        count = 1
        i = 0
        while len(gauss) < 2*len(braid):
                index = i % len(braid)
                crossing = braid[index]
                if abs(crossing)== currentstrand or abs(crossing)== currentstrand + 1:
                        if crossings[index] == 0:
                                crossings[index] = count
                                count += 1
                
                if abs(crossing) == currentstrand:
                        currentstrand -= 1
                        if crossing > 0:
                                gauss.append(-crossings[index])
                        else:
                                gauss.append(crossings[index])
                elif abs(crossing) == currentstrand + 1:
                        currentstrand += 1
                        if crossing > 0:
                                gauss.append(crossings[index])
                        else:
                                gauss.append(-crossings[index])
                else:
                        move = False
                i += 1

        return gauss

def InitialSigns(braid):
        # Takes signs from braid notation: positive entry in braid notation = positive crossing
        signs = []

        for crossing in braid:
                if crossing < 0:
                        signs.append(1)
                else:
                        signs.append(-1)
        return signs

def GaussToSigns(initialsigns, gauss):
        # Reorders sign list based on Gauss code
        signs = []

        for i in range(len(gauss)):
                if gauss[i] < 0:
                    signs.append(initialsigns[abs(gauss[i])-1])

        return signs
        
def BraidToSigns(braid):
        initsigns = InitialSigns(braid)
        gauss = BraidToGauss(braid)
        signs = GaussToSigns(initsigns, gauss)

        return signs

