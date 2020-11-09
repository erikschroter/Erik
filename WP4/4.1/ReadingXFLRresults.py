def marsinit(filename):

    # Creating empty lists for all output columns
    yspan = []
    Chord = []
    Ai = []
    Cl = []
    ICd = []
    CmAirfquarterchord = []

    # Open Datafiles
    with open(filename, 'r') as csv_file:

        lines = csv_file.readlines()

        # Delete the lines which are not needed
        del lines[:9]
        del lines[2:12]
        del lines[40:]

        # Read the lift coefficient value which is always in line 10
        linefur = lines[0]
        linefur = linefur.split(',')
        CLintermediate = linefur[1]
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
        for i in range(39):
            line = []
            line.append(lines[i])
            linefur = line[0]
            linefur = linefur.split(',')
            lines[i] = linefur

        # Obtain the values for yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord
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
            yspan[j] = value[-1]
        for j in range(len(Chord)):
            value = Chord[j]
            value = value.split(' ')
            Chord[j] = value[-1]
        for j in range(len(Ai)):
            value = Ai[j]
            value = value.split(' ')
            Ai[j] = value[-1]
        for j in range(len(Cl)):
            value = Cl[j]
            value = value.split(' ')
            Cl[j] = value[-1]
        for j in range(len(ICd)):
            value = ICd[j]
            value = value.split(' ')
            ICd[j] = value[-1]
        for j in range(len(CmAirfquarterchord)):
            value = CmAirfquarterchord[j]
            value = value.split(' ')
            CmAirfquarterchord[j] = value[-1]

    return [CL, yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord]


"""CL, yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord = marsinit('MainWing_a0.00_v10.00ms.csv')

print(CL)
print(yspan)
print(Chord)
print(Ai)
print(Cl)
print(ICd)
print(CmAirfquarterchord)"""