from random import choice, shuffle
import sys
import csv

Names = {}
xCords = []
yCords = []
Neglected = []

# Reconfigure main function to take HI, I, C, F, Partners, Names, and Dimensions as inputs. User-prompting functions
# are no longer needed with the flask/html GUI.
def seating_algorithm(Names, Height, Width, HI, I, C, F):

    Partners = False
    while True:
        inpt = input("Partnered desks? (y/n)\n").lower().strip()
        if inpt == "yes" or inpt == "y":
            Partners = True
            break
        elif inpt == "no" or inpt == "n":
            Partners = False
            break

    load_names()
    get_grid_dimensions(Partners)

    print("List HIGHLY INCOMPATIBLE students. You are limited to two pairs. Press ENTER when finished.")
    HI = get_pairs(2)

    print("List students who should not be beside eachother. Press ENTER when finished")
    I = get_pairs(None)

    print("List students that may be seated beside one another. Press ENTER when finished.")
    print("Note: You have specified that students will be seated at partnered desks. A student can thus only have one partner!") if Partners else print("Note: A student may have a maximum of TWO partners.")
    C = get_pairs(None)
    find_contradiction(HI, C, I)
    C = fix_compatibles(C, Partners, HI)

    limit = int(round(len(xCords) / 3))
    print(f"List students who should be near the front of the class. You are limited to {limit}. Press ENTER when finished.")
    F = get_fronts(limit)

    MCS = get_MCS(HI, C, F)
    HI_C_F = MCS["HI_C_F"]
    HI_C = MCS["HI_C"]
    HI_F = MCS["HI_F"]
    C_F = MCS["C_F"]

    
    while True:
        escape_loop = True
        # PHASE 1: Place HI pairs with their partners
        if len(HI) > 0:
            while True:
                P1 = phase_one(Partners, HI, HI_C_F, HI_C, HI_F, C, F, I)
                P1Assignments = P1["Assignments"]
                if I_check(P1Assignments, I) and F_check(P1Assignments, F) and C_check(P1Assignments, C):
                    print("Phase 1 was succesful")
                    C = P1["Edited_C"]
                    break
                else:
                    print("Phase 1 did not satisfy the checks. Retrying.")
        else:
            P1Assignments = []
            P1 = {"Removed": []}
        
        # PHASE 2: Place C_F with partners, then F
        P2Counter = 0
        if escape_loop:
            while True:
                P2Assignments = phase_two(Partners, C_F, F, C, P1Assignments)
                if I_check(P2Assignments, I) and F_check(P2Assignments, F) and C_check(P2Assignments, C):
                    print("Phase 2 was succesful")
                    break
                else:
                    print("Phase 2 did not satisfy the checks. Retrying.")
                    P2Counter += 1
                if P2Counter >= 2000:
                    escape_loop = False
                    break

        # PHASE 3: Place remaining C students with partners
        P3Counter = 0
        if escape_loop:
            while True:
                output = phase_three(Partners, C, P2Assignments)
                P3Assignments = output["Assignments"]
                ResetCheck = output["ResetCheck"]
                if ResetCheck:
                    escape_loop = False
                    break
                if I_check(P3Assignments, I) and F_check(P3Assignments, F) and C_check(P3Assignments, C):
                    print("Phase 3 was succesful")
                    break
                else:
                    print("Phase 3 did not satisfy the checks. Retrying.")
                    P3Counter += 1
                if P3Counter >= 2000:
                    escape_loop = False
                    break

        # PHASE 4: Place I pairs with sufficient distance
        P4counter = 0
        if escape_loop:
            while True:
                P4Assignments = phase_four(P3Assignments, I)
                if I_check(P4Assignments, I) and F_check(P4Assignments, F) and C_check(P4Assignments, C):
                    print("Phase 4 was succesful")
                    break
                else:
                    print("Phase 4 did not satisfy the checks. Retrying.")
                    P4counter += 1
                if P4counter >= 2000:
                    escape_loop == False
                    break

        if escape_loop:
            break

    # PHASE 5: Place all neutral students
    phase_five(P4Assignments)

    print()
    print(f"Compatible: {C}")
    print(f"Incompatible: {I}")
    print(f"Highly Incompatible: {HI}")
    print(f"Fronts: {F}")
    print()
    print(f"Phase 1 Assignments: {P1Assignments}")
    print(f"Phase 2 Assignments: {P2Assignments}")
    print(f"Phase 3 Assignments: {P3Assignments}")
    print(f"Phase 4 Assignments: {P4Assignments}")
    print(f"Final Assignments: {Names}")
    print(f"Removed due to string impossibility: {P1['Removed']}")

    print_spreadsheet()


# Load inputted names into memory
def load_names():
    with open("names.txt") as inputF:
        for name in inputF:
            Names[name.strip()] = "empty"

# Cleanse compatibles of logical impossibilities
def fix_compatibles(C, Partners, HI):
    while True:
        counts = {}
        problems = []
        for couple in C:
            for student in couple:
                try:
                    counts[student] += 1
                    if Partners:
                        print("Error: Each student can only have one partner!")
                        sys.exit(1)
                    if counts[student] > 2:
                        print("Error: Each student can only have two partners!")
                        sys.exit(2)
                except KeyError:
                    counts[student] = 1
        # (a,b)(a,c)(b,c) triangle impossibility
        for student in counts:
            if counts[student] == 2:
                test = []
                for pair in C:
                    if pair[0] == student:
                        test.append(pair[1])
                    if pair[1] == student:
                        test.append(pair[0])
                revtest = [test[1], test[0]]
                if test in C:
                    problems.append(test)
                elif revtest in C:
                    problems.append(revtest)
        if problems:
            rchoice = choice(problems)
            C.remove(rchoice)
            print(f"Removed: {rchoice} ((a,b)(a,c)(b,c) Triangle impossibility)")
        else:
            break

    # HI: (a,b) C: (a, e) (b, e) impossibility
    for pair in HI:
        while True:
            LeftHIpartners = []
            RightHIpartners = []
            for couple in C:
                if pair[0] == couple[0]:
                    LeftHIpartners.append(couple[1])
                if pair[0] == couple[1]:
                    LeftHIpartners.append(couple[0])
                if pair[1] == couple[0]:
                    RightHIpartners.append(couple[1])
                if pair[1] == couple[1]:
                    RightHIpartners.append(couple[0])
            SamePartners = []
            for S in LeftHIpartners:
                if S in RightHIpartners:
                    SamePartners.append(S)
            problems = []
            for St in SamePartners:
                for couple in C:
                    if (St == couple[0] or St == couple[1]) and (pair[0] == couple[0] or pair[0] == couple[1] or pair[1] == couple[0] or pair[1] == couple[1]):
                        problems.append(couple)
            
            if problems:
                rchoice = choice(problems)
                C.remove(rchoice)
                print(f"Removed: {rchoice} (HI: (a,b) C: (a, e) (b, e) impossibility)")
            else:
                break       
    return C



# Function for prompting user for C, HI, or I student pairs
def get_pairs(Limit):
    # Get inputs
    drtyPairs = []
    pairs = []
    stop = False
    while True:
        if not Limit == None and len(drtyPairs) >= Limit:
            break
        while True:
            S = input("Student 1: ").strip().capitalize()
            if S in Names:
                S1 = S
                break
            elif S.lower() in Names:
                S1 = S.lower()
                break
            elif S.lower() == "":
                stop = True
                break
            else:
                print("Student not in list. Try again.")
        if stop == True:
            break
        while True:
            S = input("Student 2: ").strip().capitalize()
            if S in Names and not S == S1:
                S2 = S
                break
            elif S.lower() in Names and not S == S1:
                S2 = S.lower()
                break
            elif S.lower() == "":
                stop = True
                break
            elif S == S1:
                print("Cannot input the same student twice!")
            else:
                print("Student not in list. Try again.")
        if stop == True:
            break
        else:
            drtyPairs.append([S1, S2])
    # Rid dups
    for pair in drtyPairs:
        InversePair = [pair[1], pair[0]]
        if (not pair in pairs) and (not InversePair in pairs):
            pairs.append(pair)
    return pairs

# Get students who need to be placed in front
def get_fronts(limit):
    F = []
    stop = False
    count = 0
    while stop == False and count < limit:
        while True:
            S = input("Student: ").strip().capitalize()
            if S in Names and S not in F:
                F.append(S)
                count += 1
                break
            elif S.lower() in Names and S not in F:
                F.append(S.lower())
                count += 1
                break
            elif S.lower() == "":
                stop = True
                break
            elif S in F:
                print("No duplicate inputs!")
            else:
                print("Student not in list. Try again.")
    return F

# Find the "multi-category" students
def get_MCS(HI, C, F):
    C_list = []
    HI_list = []
    HI_C_F = []
    HI_C = []
    HI_F = []
    C_F = []
    for pair in C:
        for x in range(2):
            if pair[x] not in C_list:
                C_list.append(pair[x])
    for pair in HI:
        for x in range(2):
            if pair[x] not in HI_list:
                HI_list.append(pair[x])
    for S in HI_list:
        if (S in F and S in C_list) and S not in HI_C_F:
            HI_C_F.append(S)
        elif (S in F and S not in C_list) and S not in HI_F:
            HI_F.append(S)
        elif (S in C_list and S not in F) and S not in HI_C:
            HI_C.append(S)
    for S in C_list:
        if S in F and S not in C_F:
            C_F.append(S)
    return {"HI_C_F": HI_C_F,
            "HI_C": HI_C,
            "HI_F": HI_F,
            "C_F": C_F}

# Students cannot be I and C
def find_contradiction(HI, C, I):
    CR = []
    for pair in C:
        invpair = [pair[1], pair[0]]
        for x in [pair, invpair]:
            for y in [HI, I]:
                if (x in y):
                    print(f"\nYou inputted {x[0]} and {x[1]} as both COMPATIBLE and INCOMPATIBLE!\n")
                    while True:
                        answer = input(f"If you would like them to be COMPATIBLE, type 'C'\nFor INCOMPATIBLE, type 'I'\nTo remove this pair altogether, type 'R'\n").lower()
                        if answer == "c":
                            y.remove(x)
                            break
                        elif answer == "i":
                            CR.append(x)
                            break
                        elif answer == "r":
                            y.remove(x)
                            CR.append(x)
                            break
                        else:
                            print("Invalid input.")
    for pair in CR:
        try:
            C.remove(pair)
        except ValueError:
            C.remove([pair[1], pair[0]])

# Get dimensions of classroom
def get_grid_dimensions(Partners):
    while True:
        try:
            width = int(input("Class width: "))
            break
        except ValueError:
            print("Input must be an integer")
    while True:
        try:
            height = int(input("Class height: "))
            break
        except ValueError:
            print("Input must be an integer")
    if height * width < len(Names):
        print("Error: Not enough seats")
        sys.exit(3)
    if height * width < 15:
        print("Error: Class is too small!")
        sys.exit(3)
    if height * width > 50:
        print("Error: Class is too big!")
        sys.exit(3)
    if Partners and (width % 2 == 1):
        print("Error: In a class with partnered desks, the width must be an even number!")
        sys.exit(4)
    for num in range(width):
        xCords.append(num)
    for num in range(height):
        yCords.append(num)

def phase_one(Partners, HI, HI_C_F, HI_C, HI_F, C, F, I):
    
    # Define width and assignments
    width = len(xCords)
    Assignments = {}

    # Get margins
    LeftMargin = []
    RightMargin = []
    for x in range(int(round(width / 4))):
        LeftMargin.append(x)
        RightMargin.append((width - 1) - x)
    print(f"Left Margin: {LeftMargin}")
    print(f"Right Margin {RightMargin}")

    # Count students in HI to determine phase 1 path
    counts = {}
    path = "nodups"
    for pair in HI:
        for x in range(2):
            try:
               counts[pair[x]] += 1
               dupStudent = pair[x]
               path = "dups"
            except KeyError: 
                counts[pair[x]] = 1
            
    # Phase one "dups" path
    if path == "dups":
        # Place duplicated student on left/right margin
        margins = [LeftMargin, RightMargin]
        shuffle(margins)
        assigns = place_on_margin(Partners, dupStudent, margins[0], HI_C_F, HI_F, HI_C, C, F)
        for student in assigns:
            Assignments[student] = assigns[student]

        # Create/shuffle list of other students in HI
        otherS = []
        for S in counts:
            if counts[S] == 1:
                otherS.append(S)
        shuffle(otherS)

        # NEW LINE
        # Prioritize HI_F and HI_C_F students
        if otherS[0] in HI_C_F or otherS[0] in HI_F:
            otherSf = [otherS[0], otherS[1]]
        if otherS[1] in HI_C_F or otherS[1] in HI_F:
            otherSf = [otherS[1], otherS[0]]
        else:
            otherSf = otherS

        # Place other students in other margin
        for S in otherSf:
            while True:
                assigns = place_on_margin(Partners, S, margins[1], HI_C_F, HI_F, HI_C, C, F)
                repeats = False
                for student in assigns:
                    if assigns[student] in Assignments.values():
                        repeats = True
                if not repeats:
                    for student in assigns:
                        Assignments[student] = assigns[student]
                    break
    
    # Phase one "nodups" path
    if path == "nodups":
        shuffle(HI)
    
        # PLace the first HI pair with partners
        pair = HI[0]
        margins = [LeftMargin, RightMargin]
        shuffle(margins)
        for n in range(2):
            assigns = place_on_margin(Partners, pair[n], margins[n], HI_C_F, HI_F, HI_C, C, F)
            for student in assigns:
                Assignments[student] = assigns[student]

            # Get list of all HI students:
            HI_list = []
            for duo in HI:
                HI_list.append(duo[0])
                HI_list.append(duo[1])
        
        # Place second pair if len(HI) is 2
        if len(HI) == 2:
            pair = HI[1]
            shuffle(pair)

            # Place students on margins if not placed. Otherwise, ensure that all partners are placed.
            for n in range(2):
                if pair[n] not in Assignments:
                    while True:
                        break_loop = True
                        assigns = place_on_margin(Partners, pair[n], margins[n], HI_C_F, HI_F, HI_C, C, F)
                        for student in assigns:
                            if assigns[student] in Assignments.values():
                                break_loop = False
                        if break_loop:
                            for student in assigns:
                                Assignments[student] = assigns[student]
                            break
                elif pair[n] in Assignments:
                    xcord = Assignments[pair[n]][0]
                    ycord = Assignments[pair[n]][1]
                    Stdnt = pair[n]
                    # If this student is pre-placed, that is because they are C with another HI.
                    # Find non-HI partner
                    partner = None
                    for cple in C:
                        if cple[0] == Stdnt and cple[1] not in HI_list:
                            partner = cple[1]
                        if cple[1] == Stdnt and cple[0] not in HI_list:
                            partner = cple[0]
                    # Place non-HI partner
                    if partner:
                        if ([xcord + 1, ycord] not in Assignments.values()) and xcord + 1 < width:
                            Assignments[partner] = [xcord + 1, ycord]
                        elif ([xcord - 1, ycord] not in Assignments.values()) and xcord - 1 >= 0:
                            Assignments[partner] = [xcord - 1, ycord]
                        else:
                            print(f"ERROR: {Stdnt} and {partner} C pair is IMPOSSIBLE")
        if len(HI) > 2:
            print("ERROR: 'phase_one' has not been implemented with support for >2 HI pairs!")
            sys.exit(5)
    
    print(f"Assignments: {Assignments}")
    print(f"Compatible: {C}")
    print(f"Highly Incompatible: {HI}")
    print(f"Fronts: {F}")
    print(f"Incompatible: {I}")
    
    # To account for "string impossibility", neglect any C pairs that exist past the margins
    ToRemove = []
    merged = HI_C + HI_C_F
    for S in merged:
        FoundLeftP = False
        FoundRightP = False
        HISxCord = Assignments[S][0]
        if HISxCord < width / 2:
            for student in Assignments:
                if Assignments[student][0] == (HISxCord - 1) and Assignments[student][1] == Assignments[S][1]:
                    LeftP = student
                    FoundLeftP = True
            if FoundLeftP:
                for pair in C:
                    if (pair[0] == LeftP and not pair[1] == S) or (pair[1] == LeftP and not pair[0] == S):
                        ToRemove.append(pair)
                LeftP = None
        if HISxCord > width / 2:
            for student in Assignments:
                if Assignments[student][0] == (HISxCord + 1) and Assignments[student][1] == Assignments[S][1]:
                    RightP = student
                    FoundRightP = True
            if FoundRightP:
                for pair in C:
                    if (pair[0] == RightP and not pair[1] == S) or (pair[1] == RightP and not pair[0] == S):
                        ToRemove.append(pair)
                RightP = None
    for pair in ToRemove:
        C.remove(pair)
    
    return {"Assignments": Assignments,
            "Edited_C": C,
            "Removed": ToRemove}

def place_on_margin(Partners, Student, Margin, HI_C_F, HI_F, HI_C, C, F):
    Assignments = {}
    width = len(xCords)
    while True:
            break_loop = True

            # Place Student on margin. If front, place in front.
            x = choice(Margin)
            if Student in HI_F or Student in HI_C_F:
                y = choice([0, 1])
            elif front_partner_check(Student, F, C):
                y = choice([0, 1])
            else:
                y = choice(yCords)
            Assignments[Student] = [x, y]

            # If Student has partners, place partners beside him. If impossible, restart.
            if Student in HI_C_F or Student in HI_C:
                xLS = x - 1
                xRS = x + 1
                Seats = [xLS, xRS]
                if xLS < 0 or xLS > (width - 1):
                    Seats.remove(xLS)
                if xRS < 0 or xRS > (width - 1):
                    Seats.remove(xRS)
                for pair in C:
                    if not Seats and (pair[1] == Student or pair[0] == Student):
                        break_loop = False
                        break
                    elif Seats:
                        Seat = choice(Seats)
                        if Seats and pair[0] == Student:
                            Assignments[pair[1]] = [Seat, y]
                            Seats.remove(Seat)
                        if Seats and pair[1] == Student:
                            Assignments[pair[0]] = [Seat, y]
                            Seats.remove(Seat)
                        if Partners:
                            if (x % 2 == 0 and Seat == xLS) or (x % 2 == 1 and Seat == xRS):
                                break_loop = False
                                break
            if break_loop:
                break
            else:
                Assignments.clear()
    return Assignments

def front_partner_check(Student, F, C):
    # Find all C partners
    partners = []
    for pair in C:
        if pair[0] == Student:
            partners.append(pair[1])
        if pair[1] == Student:
            partners.append(pair[0])
    for S in partners:
        if S in F:
            return True
    return False

def I_check(Assignments, I):
    Existing = []
    for pair in I:
        if pair[0] in Assignments and pair[1] in Assignments:
            Existing.append(pair)
    for pair in Existing:
        if (abs(Assignments[pair[0]][0] - Assignments[pair[1]][0]) < 2) and (abs(Assignments[pair[0]][1] - Assignments[pair[1]][1]) < 2):
            print("I_check failed")
            return False
    return True

def F_check(Assignments, F):
    for S in Assignments:
        if S in F and Assignments[S][1] > 1:
            print("F_check failed")
            return False
    return True

def C_check(Assignments, C):
    Existing = []
    for pair in C:
        if pair[0] in Assignments and pair[1] in Assignments:
            Existing.append(pair)
    for pair in Existing:
        if (abs(Assignments[pair[0]][0] - Assignments[pair[1]][0]) > 1) or (abs(Assignments[pair[0]][1] - Assignments[pair[1]][1]) > 0):
            print("C_check failed")
            return False
    return True

def phase_two(Partners, C_F, F, C, Assignments):
    # Remember to clear P2Assignments and restart if impossibilities are detected

    # Place the C_F students

    while True:
        escape = True
        P2Assignments = {}
        shuffle(C_F)
        for S in C_F:
            if (S not in Assignments) and (S not in P2Assignments):
                while True:
                    xCord = choice(xCords)
                    yCord = choice([0, 1])
                    LS = [(xCord - 1), yCord]
                    RS = [(xCord + 1), yCord]
                    LeftRight = [LS, RS]
                    if LS[0] < 0:
                        LeftRight.remove(LS)
                    if RS[0] > (len(xCords) - 1):
                        LeftRight.remove(RS)
                    shuffle(LeftRight)
                    if [xCord, yCord] not in Assignments.values():
                        P2Assignments[S] = [xCord, yCord]
                        break

                for pair in C:
                    if pair[0] == S and (pair[1] not in Assignments) and (pair[1] not in P2Assignments):
                        if (LeftRight[0] not in Assignments.values()) and (LeftRight[0] not in P2Assignments.values()):
                            P2Assignments[pair[1]] = LeftRight[0]
                        elif len(LeftRight) > 1 and (LeftRight[1] not in Assignments.values()) and (LeftRight[1] not in P2Assignments.values()):
                            P2Assignments[pair[1]] = LeftRight[1]
                        else:
                            escape = False
                            print("Impossible placement of C_F partner. Resetting")
                        if Partners and (P2Assignments[S][0] % 2 == 0) and (P2Assignments[pair[1]][0] == P2Assignments[S][0] - 1):
                            escape = False
                            print("partner fail")
                        if Partners and (P2Assignments[S][0] % 2 == 1) and (P2Assignments[pair[1]][0] == P2Assignments[S][0] + 1):
                            escape = False
                            print("partner fail")
                    if pair[1] == S and (pair[0] not in Assignments) and (pair[0] not in P2Assignments):
                        if (LeftRight[0] not in Assignments.values()) and (LeftRight[0] not in P2Assignments.values()):
                            P2Assignments[pair[0]] = LeftRight[0]
                        elif len(LeftRight) > 1 and (LeftRight[1] not in Assignments.values()) and (LeftRight[1] not in P2Assignments.values()):
                            P2Assignments[pair[0]] = LeftRight[1]
                        else:
                            escape = False
                            print("Impossible placement of C_F partner. Resetting")
                        if Partners and (P2Assignments[S][0] % 2 == 0) and (P2Assignments[pair[0]][0] == P2Assignments[S][0] - 1):
                            escape = False
                            print("partner fail")
                        if Partners and (P2Assignments[S][0] % 2 == 1) and (P2Assignments[pair[0]][0] == P2Assignments[S][0] + 1):
                            escape = False
                            print("partner fail")
                    if not escape:
                        break
                if not escape:
                    break
        if escape:
            break
    
    shuffle(F)
    for S in F:
        if (S not in Assignments) and (S not in P2Assignments):
            while True:
                xCord = choice(xCords)
                yCord = choice([0, 1])
                if ([xCord, yCord] not in Assignments.values()) and ([xCord, yCord] not in P2Assignments.values()):
                    P2Assignments[S] = [xCord, yCord]
                    break
                print("P2R")
    
    Combined = {}
    for S in P2Assignments:
        Combined[S] = P2Assignments[S]
    for S in Assignments:
        Combined[S] = Assignments[S]
    
    return Combined

def phase_three(Partners, C, P2Assignments):
    # Place remaining C partners with their partners. If ever impossible, restart.
    # Place remaining unplaced students randomly
    # Perform final I, F, C, and HI checks
    while True:
        P3Assignments = {}
        restart = False
        shuffle(C)
        counter = 0
        fullreset = False
        for pair in C:

            if (pair[1] in P2Assignments or pair[1] in P3Assignments) and (pair[0] not in P2Assignments and pair[0] not in P3Assignments):
                if pair[1] in P2Assignments:
                    xPcord = P2Assignments[pair[1]][0]
                    yPcord = P2Assignments[pair[1]][1]
                if pair[1] in P3Assignments:
                    xPcord = P3Assignments[pair[1]][0]
                    yPcord = P3Assignments[pair[1]][1]
                LS = [xPcord - 1, yPcord]
                RS = [xPcord + 1, yPcord]
                LsideRside = [LS, RS]
                if xPcord - 1 < 0 or LS in P2Assignments.values() or LS in P3Assignments.values():
                    LsideRside.remove(LS)
                if xPcord + 1 > (len(xCords) - 1) or RS in P2Assignments.values() or RS in P3Assignments.values():
                    LsideRside.remove(RS)
                if Partners and xPcord % 2 == 0 and LS in LsideRside:
                    LsideRside.remove(LS)
                if Partners and xPcord % 2 == 1 and RS in LsideRside:
                    LsideRside.remove(RS)
                if not LsideRside:
                    restart = True
                else:
                    P3Assignments[pair[0]] = choice(LsideRside)
                
            if (pair[0] in P2Assignments or pair[0] in P3Assignments) and (pair[1] not in P2Assignments and pair[1] not in P3Assignments):
                if pair[0] in P2Assignments:
                    xPcord = P2Assignments[pair[0]][0]
                    yPcord = P2Assignments[pair[0]][1]
                if pair[0] in P3Assignments:
                    xPcord = P3Assignments[pair[0]][0]
                    yPcord = P3Assignments[pair[0]][1]
                LS = [xPcord - 1, yPcord]
                RS = [xPcord + 1, yPcord]
                LsideRside = [LS, RS]
                if xPcord - 1 < 0 or LS in P2Assignments.values() or LS in P3Assignments.values():
                    LsideRside.remove(LS)
                if xPcord + 1 > (len(xCords) - 1) or RS in P2Assignments.values() or RS in P3Assignments.values():
                    LsideRside.remove(RS)
                if Partners and xPcord % 2 == 0 and LS in LsideRside:
                    LsideRside.remove(LS)
                if Partners and xPcord % 2 == 1 and RS in LsideRside:
                    LsideRside.remove(RS)
                if not LsideRside:
                    restart = True
                else:
                    P3Assignments[pair[1]] = choice(LsideRside)

            if (pair[0] not in P2Assignments) and (pair[1] not in P2Assignments) and (pair[0] not in P3Assignments) and (pair[1] not in P3Assignments):
                while True: 
                    RandomCoords = [choice(xCords), choice(yCords)]
                    if RandomCoords not in P2Assignments.values() and RandomCoords not in P3Assignments.values():
                        break
                Students = [pair[0], pair[1]]
                shuffle(Students)
                P3Assignments[Students[0]] = RandomCoords
                LS = [RandomCoords[0] - 1, RandomCoords[1]]
                RS = [RandomCoords[0] + 1, RandomCoords[1]]
                LsideRside = [LS, RS]
                if RandomCoords[0] - 1 < 0 or LS in P2Assignments.values() or LS in P3Assignments.values():
                    LsideRside.remove(LS)
                if RandomCoords[0] + 1 > (len(xCords) - 1) or RS in P2Assignments.values() or RS in P3Assignments.values():
                    LsideRside.remove(RS)
                if Partners and RandomCoords[0] % 2 == 0 and LS in LsideRside:
                    LsideRside.remove(LS)
                if Partners and RandomCoords[0] % 2 == 1 and RS in LsideRside:
                    LsideRside.remove(RS)
                if not LsideRside:
                    restart = True
                else:
                    P3Assignments[Students[1]] = choice(LsideRside)
            
            if restart:
                print("Reached impossibility in Phase 3 C Assignments\nRetrying...")
                counter += 1
                break
            if counter >= 2000:
                fullreset = True
                restart = False
                break

        if not restart:
            break

    Combined = {}
    for S in P3Assignments:
        Combined[S] = P3Assignments[S]
    for S in P2Assignments:
        Combined[S] = P2Assignments[S]

    return {"Assignments": Combined,
            "ResetCheck": fullreset}

# Place the incompatible pairs semi-randomly. Rerun if impossibility is found.
# HI pairs are being replaced!!!!!!!!
def phase_four(P3Assignments, I):

    while True:

        Available = []
        for x in xCords:
            for y in yCords:
                Available.append([x,y])
        for pair in P3Assignments.values():
            if pair in Available:
                Available.remove(pair)

        escape = True
        P4Assignments = {}

        for S in I:
            tried = []
            if ((S[0] not in P3Assignments) and (S[0] not in P4Assignments)) and ((S[1] not in P3Assignments) and (S[1] not in P4Assignments)):
                shuffle(S)
                RC = choice(Available)
                P4Assignments[S[0]] = RC
                Available.remove(RC)

                AsubT = []
                while True:
                    for c in Available:
                        if c not in tried:
                            AsubT.append(c)
                    RC2 = choice(AsubT)
                    if (abs(RC[0] - RC2[0]) > 1) or (abs(RC[1] - RC2[1]) > 1) and (RC2 not in P3Assignments.values()) and (RC2 not in P4Assignments.values()):
                        break
                    else:
                        tried.append(RC2)
                    if len(tried) == len(Available):
                        escape = False
                        break
                if escape:
                    P4Assignments[S[1]] = RC2
                    Available.remove(RC2)      

            if ((S[0] in P3Assignments) or (S[0] in P4Assignments)) and ((S[1] not in P3Assignments) and (S[1] not in P4Assignments)):
                if S[0] in P3Assignments:
                    RC = P3Assignments[S[0]]
                if S[0] in P4Assignments:
                    RC = P4Assignments[S[0]]
                AsubT = []
                while True:
                    for c in Available:
                        if c not in tried:
                            AsubT.append(c)
                    RC2 = choice(AsubT)
                    if ((abs(RC[0] - RC2[0]) > 1) or (abs(RC[1] - RC2[1]) > 1)) and (RC2 not in P3Assignments.values()) and (RC2 not in P4Assignments.values()):
                        break
                    else:
                        tried.append(RC2)
                    if len(tried) == len(Available):
                        escape = False
                        break
                if escape:
                    P4Assignments[S[1]] = RC2
                    Available.remove(RC2)   

            if ((S[1] in P3Assignments) or (S[1] in P4Assignments)) and ((S[0] not in P3Assignments) and (S[0] not in P4Assignments)):
                if S[1] in P3Assignments:
                    RC = P3Assignments[S[1]]
                if S[1] in P4Assignments:
                    RC = P4Assignments[S[1]]
                AsubT = []
                while True:
                    for c in Available:
                        if c not in tried:
                            AsubT.append(c)
                    RC2 = choice(AsubT)
                    if (abs(RC[0] - RC2[0]) > 1) or (abs(RC[1] - RC2[1]) > 1) and (RC2 not in P3Assignments.values()) and (RC2 not in P4Assignments.values()):
                        break
                    else:
                        tried.append(RC2)
                    if len(tried) == len(Available):
                        escape = False
                        break
                if escape:
                    P4Assignments[S[0]] = RC2
                    Available.remove(RC2)   

            if ((S[0] in P3Assignments) or (S[0] in P4Assignments)) and ((S[1] in P3Assignments) or (S[1] in P4Assignments)):
                if S[0] in P3Assignments:
                    x0 = P3Assignments[S[0]][0]
                    y0 = P3Assignments[S[0]][1]
                if S[0] in P4Assignments:
                    x0 = P4Assignments[S[0]][0]
                    y0 = P4Assignments[S[0]][1]
                if S[1] in P3Assignments:
                    x1 = P3Assignments[S[1]][0]
                    y1 = P3Assignments[S[1]][1]
                if S[1] in P4Assignments:
                    x1 = P4Assignments[S[1]][0]
                    y1 = P4Assignments[S[1]][1]
                if not ((abs(x1 - x0) > 1) or (abs(y1 - y0) > 1)):
                    escape = False
        
        if escape:
            break
        else:
            print("Impossibility reached in Phase 4. Retrying.")
    
    Combined = {}
    for S in P3Assignments:
        Combined[S] = P3Assignments[S]
    for S in P4Assignments:
        Combined[S] = P4Assignments[S]

    return Combined

def phase_five(P4Assignments):
    AvailableCoords = []
    for x in xCords:
        for y in yCords:
            AvailableCoords.append([x,y])
    for pair in P4Assignments.values():
        if pair in AvailableCoords:
            AvailableCoords.remove(pair)
    for S in P4Assignments:
        Names[S] = P4Assignments[S]
    for S in Names:
        if Names[S] == "empty":
            Names[S] = choice(AvailableCoords)
            AvailableCoords.remove(Names[S])

def print_spreadsheet():
    Longest = 4
    for name in Names:
        if len(name) > Longest:
            Longest = len(name)
    CellWidth = Longest + 1
    with open("output.csv", "w") as outputF:
        CSVoutput = csv.writer(outputF, delimiter="|")
        for y in yCords:
            row = []
            for x in xCords:
                exist = False
                for name in Names:
                    if Names[name][0] == x and Names[name][1] == y:
                        SpaceCount = CellWidth - len(name)
                        ReformattedName = name + (" " * SpaceCount)
                        row.append(ReformattedName)
                        exist = True
                        break
                if exist == False:
                    row.append("none" + (" " * (CellWidth - 4)))
            CSVoutput.writerow(row)

if __name__ == "__main__":
    seating_algorithm()