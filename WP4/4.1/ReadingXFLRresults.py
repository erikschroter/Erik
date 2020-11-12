"""Function to read XFLR Results in a CSV Format which has as an output:
CL, yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord
If questions ask Christoph Pabsch"""

def ReadingXFLR(filename):
    """Input for function: filename
    Output of function: CL, yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord"""

    # Creating empty lists for all output columns
    yspan = []
    Chord = []
    Ai = []
    Cl = []
    ICd = []
    CmAirfquarterchord = []

    # Open Datafiles
    #Latin-1 encoding
    with open(filename, 'r', encoding='latin-1') as csv_file:

        lines = csv_file.readlines()

        # Delete the lines which are not needed
        del lines[:9]
        del lines[2:31]
        del lines[21:]

        # Read the lift coefficient value which is always in line 10
        pickedline = lines[0]
        pickedline = pickedline.split(',')
        CLintermediate = pickedline[1]
        NewCLlist = CLintermediate.split(' ')
        if '' in NewCLlist:
            NewCLlist.remove('')
        CLintermediate2 = NewCLlist[-1]
        NewCLlist = CLintermediate2.split('\n')
        if '\n' in NewCLlist:
            NewCLlist.remove('\n')
        if '' in NewCLlist:
            NewCLlist.remove('')
        CL = NewCLlist[-1]

        # Create split lists for each line in the table
        del lines[0]
        for i in range(20):
            line = []
            line.append(lines[i])
            pickedline = line[0]
            pickedline = pickedline.split(',')
            lines[i] = pickedline

        # Obtain the values for yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord as lists of floats
        del lines[0]
        for k in range(len(lines)):
            yspan.append(lines[k][0])
            Chord.append(lines[k][1])
            Ai.append(lines[k][2])
            Cl.append(lines[k][3])
            ICd.append(lines[k][5])
            CmAirfquarterchord.append(lines[k][7])
        for j in range(len(yspan)):
            value = yspan[j]
            value = value.split(' ')
            yspan[j] = float(value[-1])
        for j in range(len(Chord)):
            value = Chord[j]
            value = value.split(' ')
            Chord[j] = float(value[-1])
        for j in range(len(Ai)):
            value = Ai[j]
            value = value.split(' ')
            Ai[j] = float(value[-1])
        for j in range(len(Cl)):
            value = Cl[j]
            value = value.split(' ')
            Cl[j] = float(value[-1])
        for j in range(len(ICd)):
            value = ICd[j]
            value = value.split(' ')
            ICd[j] = float(value[-1])
        for j in range(len(CmAirfquarterchord)):
            value = CmAirfquarterchord[j]
            value = value.split(' ')
            CmAirfquarterchord[j] = float(value[-1])

    return [CL, yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord]


"""
USE THE FOLLOWING LINES TO TEST THE FUNTION
"""
CL, yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord = ReadingXFLR('MainWing_a0.00_v10.00ms.csv')

print(CL)
print(yspan)
print(Chord)
print(Ai)
print(Cl)
print(ICd)
print(CmAirfquarterchord)