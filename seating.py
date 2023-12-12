from random import choice, shuffle
import sys
import math

## Outputs "optimal" student placement as assigned coordinate pairs to be interpretted by frontend JS.
## See "README.md" for more details.

# C == Compatible Student Pairs
# I == Incompatible Student Pairs
# F == Students bound to front row. (Bounds student to first/second row with bias for the first row.)
# HI == Highly Incomptabile Student Pairs

# Some arbitrary settings that may be changed:
# F is limited to three students, and placement is biased.
# HI is limited to 2 pairs
# Maximum "comp string" length is "width - 4". (See "fix_compatibles()")
# Student placement functions are re-attempted 20 times before COMPLETE RESET.
# Left/Right margins are one quarter of class width. (See "phase_one()")

# Todo:
# Make README.md and talk about "fix_compatibes()" function

COMMON_REP_LIMIT = 20
MEDIUM_REP_LIMIT = 100
HIGH_REP_LIMIT = 500
def seating_algorithm(dirtyNames, Height, Width, HI, I, dirtyC, F, Partners):
    # Clear potential logical impossibilies in C
    SIwidthLimit = Width - 4
    SIwidthLimit2 = Width - 5
    output = fix_compatibles(dirtyC, Partners, HI, SIwidthLimit)
    C = output["C"]
    Removed1 = output["Removed1"]
    Removed2 = output["Removed2"]
    find_contradictions(HI, C, I)

    Names = load_names(dirtyNames)
    dims = get_grid_dimensions(Partners, Height, Width, Names)
    xCords = dims[0]
    yCords = dims[1]

    # Find and store students who exist in multiple categories.
    MCS = get_MCS(HI, C, F)
    HI_C_F = MCS["HI_C_F"]
    HI_C = MCS["HI_C"]
    HI_F = MCS["HI_F"]
    C_F = MCS["C_F"]

    P3FailCounter = 0
    Removed4 = []
    Removed5 = []
    # Five "phases" of student placement are repeated until permutation that satisfies all conditions is found.
    while True:
        # Fix C pairs after P3FailCounter gets sufficiently high
        shuffle(C)
        if P3FailCounter > HIGH_REP_LIMIT:
            output = fix_compatibles_2(C, C_F, SIwidthLimit2)
            C = output["C"]
            Removed4.append(output["Removed4"])
            P3FailCounter = 0

        escape_loop = True
        if len(HI) > 0:
            while True:
                # PHASE 1: Separate HI pairs with their partners
                P1 = phase_one(Partners, HI, HI_C_F, HI_C, HI_F, C, F, I, Width, yCords)
                P1Assignments = P1["Assignments"]
                if I_check(P1Assignments, I) and F_check(P1Assignments, F) and C_check(P1Assignments, C, Partners):
                    print("Phase 1 was succesful")
                    C = P1["Edited_C"]
                    break
                else:
                    print("Phase 1 did not satisfy the checks. Retrying.")
                print("loop1")
        else:
            P1Assignments = {}
            P1 = {"Removed": []}
        Removed3 = P1["Removed"]
        
        P2Counter = 0
        if escape_loop:
            while True:
                # PHASE 2: Place C_F with partners, then F
                output = phase_two(Partners, C_F, F, C, P1Assignments, xCords)
                P2Assignments = output["P2Assignments"]
                FullReset = output["FullReset"]
                if FullReset:
                    escape_loop = False
                    break
                if I_check(P2Assignments, I) and F_check(P2Assignments, F) and C_check(P2Assignments, C, Partners):
                    print("Phase 2 was succesful")
                    break
                else:
                    print("Phase 2 did not satisfy the checks. Retrying.")
                    P2Counter += 1
                if P2Counter >= COMMON_REP_LIMIT:
                    escape_loop = False
                    break

        P3Counter = 0
        if escape_loop:
            while True:
                # PHASE 3: Place remaining C students with partners
                output = phase_three(Partners, C, P2Assignments, xCords, yCords)
                P3Assignments = output["Assignments"]
                ResetCheck = output["ResetCheck"]
                if ResetCheck:
                    print("PHASE 3 FULL RESET")
                    P3FailCounter += 1
                    escape_loop = False
                    break
                if I_check(P3Assignments, I) and F_check(P3Assignments, F) and C_check(P3Assignments, C, Partners):
                    print("Phase 3 was succesful")
                    break
                else:
                    print("Phase 3 did not satisfy the checks. Retrying.")
                    P3Counter += 1
                if P3Counter >= COMMON_REP_LIMIT:
                    escape_loop = False
                    break

        P4counter = 0
        if escape_loop:
            while True:
                # PHASE 4: Place I pairs with sufficient distance between students.
                output = phase_four(P3Assignments, I, xCords, yCords)
                P4Assignments = output["Assignments"]
                ResetCheck = output["ResetCheck"]
                if ResetCheck:
                    print("PHASE 4 FULL RESET")
                    escape_loop = False
                    ToRemove = choice(I)
                    I.remove(ToRemove)
                    Removed5.append(ToRemove)
                    break
                if I_check(P4Assignments, I) and F_check(P4Assignments, F) and C_check(P4Assignments, C, Partners):
                    print("Phase 4 was succesful")
                    break
                else:
                    print("Phase 4 did not satisfy the checks. Retrying.")
                    P4counter += 1
                if P4counter >= COMMON_REP_LIMIT:
                    escape_loop = False
                    break

        if escape_loop:
            break

    # PHASE 5: Place remaining neutral students
    Names = phase_five(P4Assignments, xCords, yCords, Names)

    # Final details
    print(f"\n\nCompatible: {C}")
    print(f"Incompatible: {I}")
    print(f"Highly Incompatible: {HI}")
    print(f"Fronts: {F}\n")
    print(f"Phase 1 Assignments: {P1Assignments}\n")
    print(f"Phase 2 Assignments: {P2Assignments}\n")
    print(f"Phase 3 Assignments: {P3Assignments}\n")
    print(f"Phase 4 Assignments: {P4Assignments}\n\n")
    print(f"Final Assignments: {Names}\n")
    print(f"Removed due to 'HI: (a,b) C: (a, e) (b, e)' impossibility: {Removed1}")
    print(f"Removed due to loop/comp string overstretch: {Removed2}")
    print(f"Removed due to outer margin impossibility: {Removed3}")
    print(f"Removed due to constant P3 failure: {Removed4}")
    print(f"Removed due to constant P4 failure: {Removed5}")

    AllRemoved = Removed1 + Removed2 + Removed3 + Removed4 + Removed5
    return {
        "Ass": Names,
        "Removed": AllRemoved
    }

def load_names(dirtyNames):
    Names = {}
    for name in dirtyNames:
        Names[name.strip()] = "empty"
    return Names

def get_grid_dimensions(Partners, Height, Width, Names):
    xCords = []
    yCords = []
    if Height * Width < len(Names):
        print("Error: Not enough seats")
        sys.exit(1)
    if Height * Width < 15:
        print("Error: Class is too small!")
        sys.exit(1)
    if Height * Width > 96:
        print("Error: Class is too big!")
        sys.exit(1)
    if Partners and (Width % 2 == 1):
        print("Error: In a class with partnered desks, the width must be an even number!")
        sys.exit(1)
    for num in range(Width):
        xCords.append(num)
    for num in range(Height):
        yCords.append(num)
    return [xCords, yCords]

# Cleanse compatibles of logical impossibilities
def fix_compatibles(C, Partners, HI, SIwidthLimit):

    # Student partner count is limitied (IMPLEMENT IN JS)
    counts = {}
    problems = []
    for couple in C:
        for student in couple:
            if student in counts and Partners:
                print("Error: Each student can only have one partner!")
                sys.exit(2)
            elif student in counts and not Partners:
                counts[student] += 1
                if counts[student] > 2:
                    print("Error: Each student can only have two partners!")
                    sys.exit(2)
            else:
                counts[student] = 1

    # Remove "HI: (a,b) C: (a, e) (b, e)" impossibility
    Removed1 = []
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
                Removed1.append(rchoice)
            else:
                break

    # Account for loop impossibility and overstretched strings of compatible pairs.
    # Removes a problematic C pair (at random) in response to impossible placement. Repeats this until problem-free.
    Removed2 = []
    while True:
        ProblemFound = False
        shuffle(C)
        for pair in C:
            BaseStudent = pair[0]
            OtherS = pair[1]
            Counter = 0
            PreviousStudent = BaseStudent
            if loop_check(BaseStudent, OtherS, PreviousStudent, Counter, C, SIwidthLimit):
                ProblemFound = True
                PairToElim = pair
                break
            BaseStudent = pair[1]
            OtherS = pair[0]
            Counter = 0
            PreviousStudent = BaseStudent
            if loop_check(BaseStudent, OtherS, PreviousStudent, Counter, C, SIwidthLimit):
                ProblemFound = True
                PairToElim = pair
                break
        if ProblemFound:
            Removed2.append(PairToElim)
            C.remove(PairToElim)
        else:
            break

    return {
        "C": C,
        "Removed1": Removed1,
        "Removed2": Removed2
    }

# Moves along "strings" of compatible partners and detects when these strings are too long, or impossible to place.
def loop_check(BaseStudent, OtherS, PreviousStudent, Counter, C, Limit):
    Buddies = find_buddies(OtherS, C)
    Buddies.remove(PreviousStudent)
    # DIVISOR IS ARBITRARY. ADJUST "width - 4" AS NEEDED!
    if Counter > Limit:
        print("String too long!")
        return True
        # String too long
    if not Buddies:
        return False
        # No partners, therefore no loop.
    if Buddies[0] == BaseStudent:
        return True
        # Loop found!
    Counter += 1
    PreviousStudent = OtherS
    OtherS = Buddies[0]
    return loop_check(BaseStudent, OtherS, PreviousStudent, Counter, C, Limit)

# Finds students who are compatible partners of a given student.
def find_buddies(OtherS, C):
    Buddies = []
    for pair in C:
        if pair[0] == OtherS:
            Buddies.append(pair[1])
        if pair[1] == OtherS:
            Buddies.append(pair[0])
    return Buddies

# If P3 fails enough times, remove a random C pair that exists in a COMP string
def fix_compatibles_2(C, C_F, SIwidthLimit2):
    # Seperate C pairs to BIAS F students
    Removed4 = None
    ProblemFound = False
    shuffle(C)
    C_Fpairs = []
    nonC_Fpairs = []
    for pair in C:
        if pair[0] in C_F or pair[1] in C_F:
            C_Fpairs.append(pair)
        else:
            nonC_Fpairs.append(pair)
    # Iterate through C pairs and remove a pair that belongs to a string
    while True:
        for list in [C_Fpairs, nonC_Fpairs]:
            for pair in list:
                BaseStudent = pair[0]
                OtherS = pair[1]
                Counter = 0
                PreviousStudent = BaseStudent
                if loop_check(BaseStudent, OtherS, PreviousStudent, Counter, C, SIwidthLimit2):
                    ProblemFound = True
                    PairToElim = pair
                if not ProblemFound:
                    BaseStudent = pair[1]
                    OtherS = pair[0]
                    Counter = 0
                    PreviousStudent = BaseStudent
                    if loop_check(BaseStudent, OtherS, PreviousStudent, Counter, C, SIwidthLimit2):
                        ProblemFound = True
                        PairToElim = pair
                if ProblemFound:
                    Removed4 = PairToElim
                    C.remove(PairToElim)
                    break
            if ProblemFound:
                break
        if not ProblemFound and SIwidthLimit2 > 0:
            SIwidthLimit2 -= 1
        else:
            break
    return {
        "C": C,
        "Removed4": Removed4
        } 

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

# Students cannot be C and I
# This is precautionary as these inputs are prevented in the front end.
def find_contradictions(HI, C, I):
    for pair in C:
        invpair = [pair[1], pair[0]]
        for x in [pair, invpair]:
            for y in [HI, I]:
                if (x in y):
                    print(f"\nYou inputted {x[0]} and {x[1]} as both COMPATIBLE and INCOMPATIBLE!\n")
                    sys.exit("9")

# HI students are placed on the margins beside their partners.
def phase_one(Partners, HI, HI_C_F, HI_C, HI_F, C, F, I, Width, yCords):

    Assignments = {}
    LeftMargin = []
    RightMargin = []

    # Left/RIght margin is a quarter of the width. Adjust as necessary.
    for x in range(int(math.ceil(Width / 4))):
        LeftMargin.append(x)
        RightMargin.append((Width - 1) - x)
    print(f"Left Margin: {LeftMargin}")
    print(f"Right Margin {RightMargin}")

    # Count students in HI to determine phase 1 path.
    counts = {}
    path = "nodups"
    for pair in HI:
        for S in pair:
            if S in counts:
                counts[S] += 1
            else:
                counts[S] = 1
    for key in counts:
        if counts[key] == 2:
            dupStudent = key
            path = "dups"

    ## (A,B);(A,C) path. Ie: If one student is HI with two others.
    if path == "dups":
        # Place "A" on left/right margin
        margins = [LeftMargin, RightMargin]
        shuffle(margins)
        assigns = place_on_margin(Partners, dupStudent, margins[0], HI_C_F, HI_F, HI_C, C, F, Width, yCords)
        for student in assigns:
            Assignments[student] = assigns[student]

        # Create/shuffle list of "B and C"
        otherS = []
        for S in counts:
            if counts[S] == 1:
                otherS.append(S)
        shuffle(otherS)

        # The placement of multi-category students is restricted, and thus should be done first.
        if otherS[0] in HI_C_F or otherS[0] in HI_F:
            otherSf = [otherS[0], otherS[1]]
        if otherS[1] in HI_C_F or otherS[1] in HI_F:
            otherSf = [otherS[1], otherS[0]]
        else:
            otherSf = otherS
        for S in otherSf:
            while True:
                assigns = place_on_margin(Partners, S, margins[1], HI_C_F, HI_F, HI_C, C, F, Width, yCords)
                repeats = False
                for student in assigns:
                    if assigns[student] in Assignments.values():
                        repeats = True
                if not repeats:
                    for student in assigns:
                        Assignments[student] = assigns[student]
                    break
    
    ## (A,B);(C,D) path. Ie: If there are two DISTINCT HI pairs.
    if path == "nodups":
        shuffle(HI)
    
        # Place (A,B)
        pair = HI[0]
        margins = [LeftMargin, RightMargin]
        shuffle(margins)
        for n in range(2):
            assigns = place_on_margin(Partners, pair[n], margins[n], HI_C_F, HI_F, HI_C, C, F, Width, yCords)
            for student in assigns:
                Assignments[student] = assigns[student]
            # Get list of all HI students:
            HI_list = []
            for duo in HI:
                HI_list.append(duo[0])
                HI_list.append(duo[1])
        
        # Place (C,D) IF needed
        if len(HI) == 2:
            pair = HI[1]
            shuffle(pair)

            for n in range(2):
                # Place them if they haven't already been placed.
                if pair[n] not in Assignments:
                    while True:
                        print("loop1")
                        break_loop = True
                        assigns = place_on_margin(Partners, pair[n], margins[n], HI_C_F, HI_F, HI_C, C, F, Width, yCords)
                        for student in assigns:
                            if assigns[student] in Assignments.values():
                                break_loop = False
                        if break_loop:
                            for student in assigns:
                                Assignments[student] = assigns[student]
                            break
                # This path is possible because HI student(s) can be Compatible with other HI students!
                elif pair[n] in Assignments:
                    xcord = Assignments[pair[n]][0]
                    ycord = Assignments[pair[n]][1]
                    Stdnt = pair[n]
                    # Find and Place Compatible partner
                    partner = None
                    for cple in C:
                        if cple[0] == Stdnt and cple[1] not in HI_list:
                            partner = cple[1]
                        if cple[1] == Stdnt and cple[0] not in HI_list:
                            partner = cple[0]
                    if partner:
                        if ([xcord + 1, ycord] not in Assignments.values()) and xcord + 1 < Width:
                            Assignments[partner] = [xcord + 1, ycord]
                        elif ([xcord - 1, ycord] not in Assignments.values()) and xcord - 1 >= 0:
                            Assignments[partner] = [xcord - 1, ycord]
                        else:
                            print(f"ERROR: {Stdnt} and {partner} C pair is IMPOSSIBLE")
        if len(HI) > 2:
            print("ERROR: 'phase_one' has not been implemented with support for >2 HI pairs!")
            sys.exit(3)
    
    print(f"Assignments: {Assignments}")
    print(f"Compatible: {C}")
    print(f"Highly Incompatible: {HI}")
    print(f"Fronts: {F}")
    print(f"Incompatible: {I}")
    
    # To account for "Outer Margin" impossibility, neglect any C pairs that exist past the margins
    ToRemove = []
    merged = HI_C + HI_C_F
    for S in merged:
        FoundLeftP = False
        FoundRightP = False
        HISxCord = Assignments[S][0]
        if HISxCord < Width / 2:
            for student in Assignments:
                if Assignments[student][0] == (HISxCord - 1) and Assignments[student][1] == Assignments[S][1]:
                    LeftP = student
                    FoundLeftP = True
            if FoundLeftP:
                for pair in C:
                    if (pair[0] == LeftP and not pair[1] == S) or (pair[1] == LeftP and not pair[0] == S):
                        ToRemove.append(pair)
                LeftP = None
        if HISxCord > Width / 2:
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

# Used in both phase one paths to place a student on a certain margin (left or right).
def place_on_margin(Partners, Student, Margin, HI_C_F, HI_F, HI_C, C, F, Width, yCords):
    assigns = {}
    while True:
        break_loop = True

        # Place Student on margin. If front-bound, place in front.
        x = choice(Margin)
        if Student in HI_F or Student in HI_C_F:
            y = choice([0, 0, 0, 0, 1])
        elif front_partner_check(Student, F, C):
            y = choice([0, 0, 0, 0, 1])
        else:
            y = choice(yCords)
        assigns[Student] = [x, y]

        # If Student has partners, place partners beside them. If impossible, restart.
        if Student in HI_C_F or Student in HI_C:
            xLS = x - 1
            xRS = x + 1
            Seats = [xLS, xRS]
            if xLS < 0 or xLS > (Width - 1):
                Seats.remove(xLS)
            if xRS < 0 or xRS > (Width - 1):
                Seats.remove(xRS)
            for pair in C:
                if not Seats and (pair[1] == Student or pair[0] == Student):
                    break_loop = False
                    break
                elif Seats:
                    Seat = choice(Seats)
                    if Seats and pair[0] == Student:
                        assigns[pair[1]] = [Seat, y]
                        Seats.remove(Seat)
                    if Seats and pair[1] == Student:
                        assigns[pair[0]] = [Seat, y]
                        Seats.remove(Seat)
                    if Partners:
                        if (x % 2 == 0 and Seat == xLS) or (x % 2 == 1 and Seat == xRS):
                            break_loop = False
                            break
        if break_loop:
            break
        else:
            assigns.clear()
    return assigns

# Returns true if any C partners are in F
def front_partner_check(Student, F, C):
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

# Ensures all I students are sufficiently separated after EVERY PHASE
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

# Ensures all F students are in the front rows after EVERY PHASE
def F_check(Assignments, F):
    for S in Assignments:
        if S in F and Assignments[S][1] > 1:
            print("F_check failed")
            return False
    return True

# Ensures all C students are placed together after EVERY PHASE
def C_check(Assignments, C, Partners):
    Existing = []
    for pair in C:
        if pair[0] in Assignments and pair[1] in Assignments:
            Existing.append(pair)
    for pair in Existing:
        if (abs(Assignments[pair[0]][0] - Assignments[pair[1]][0]) > 1) or (abs(Assignments[pair[0]][1] - Assignments[pair[1]][1]) > 0):
            print("C_check failed")
            return False
        if Partners and (Assignments[pair[0]][0] % 2 == 1) and (Assignments[pair[1]][0] == Assignments[pair[0]][0] + 1):
            return False
        if Partners and (Assignments[pair[0]][0] % 2 == 0) and (Assignments[pair[1]][0] == Assignments[pair[0]][0] - 1):
            return False
    return True

# Place C_F students, then place F students.
def phase_two(Partners, C_F, F, C, Assignments, xCords):
    counter = 0
    FullReset = False
    # C_F
    while True:
        print("loop3")
        escape = True
        P2Assignments = {}
        shuffle(C_F)
        for S in C_F:
            if (S not in Assignments) and (S not in P2Assignments):
                # Assign coordinates to student if this has not been done
                # Bias to front row (yCord==0) in chosing yCord
                while True:
                    xCord = choice(xCords)
                    yCord = choice([0, 0, 0, 0, 1])
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
                # A and B have been used to condense this section. A: 1->0 ; B: 0->1 to avoid cpy+paste of several lines.
                # Place this student's partners beside them.
                for pair in C:
                    b = 1
                    for a in range(2):
                        if pair[b] == S and (pair[a] not in Assignments) and (pair[a] not in P2Assignments):
                            if (LeftRight[0] not in Assignments.values()) and (LeftRight[0] not in P2Assignments.values()):
                                P2Assignments[pair[a]] = LeftRight[0]
                            elif len(LeftRight) > 1 and (LeftRight[1] not in Assignments.values()) and (LeftRight[1] not in P2Assignments.values()):
                                P2Assignments[pair[a]] = LeftRight[1]
                            else:
                                escape = False
                                print("Impossible placement of C_F partner. Resetting")
                            if Partners and escape and (P2Assignments[S][0] % 2 == 0) and (P2Assignments[pair[a]][0] == P2Assignments[S][0] - 1):
                                escape = False
                                print("partner fail")
                            if Partners and escape and (P2Assignments[S][0] % 2 == 1) and (P2Assignments[pair[a]][0] == P2Assignments[S][0] + 1):
                                escape = False
                                print("partner fail")
                        b -= 1
                    if not escape:
                        counter += 1
                        break
                if not escape:
                    break
        if (not escape) and (counter >= COMMON_REP_LIMIT):
            FullReset = True
            escape = True
        if escape:
            break
    
    # F
    shuffle(F)
    FrontLoopCount = 0
    for S in F:
        if (S not in Assignments) and (S not in P2Assignments):
            while True:
                xCord = choice(xCords)
                yCord = choice([0, 0, 0, 0, 1])
                if ([xCord, yCord] not in Assignments.values()) and ([xCord, yCord] not in P2Assignments.values()):
                    P2Assignments[S] = [xCord, yCord]
                    break
                FrontLoopCount += 1
                print("P2R")
                if FrontLoopCount >= 50:
                    FullReset = True
                    break
                print("P2R")
    
    # Combine and return assignment dictionaries
    Combined = Combine_Dictionaries(Assignments, P2Assignments)
    return {"FullReset": FullReset,
            "P2Assignments": Combined}

# Place remaining C partners with their partners. If ever impossible, restart.
def phase_three(Partners, C, P2Assignments, xCords, yCords):
    counter = 0
    fullreset = False
    while True:
        print("loop5")
        P3Assignments = {}
        restart = False
        shuffle(C)
        for pair in C:
            # If ONLY student A is assigned OR Student B right is assigned
            # Again used Z and N to reduce redundancy.
            b = 1
            for a in range(2) :
                if (pair[a] in P2Assignments or pair[a] in P3Assignments) and (pair[b] not in P2Assignments and pair[b] not in P3Assignments):
                    if pair[a] in P2Assignments:
                        xPcord = P2Assignments[pair[a]][0]
                        yPcord = P2Assignments[pair[a]][1]
                    if pair[a] in P3Assignments:
                        xPcord = P3Assignments[pair[a]][0]
                        yPcord = P3Assignments[pair[a]][1]
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
                b -= 1

            # If no one has been assigned
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
            
            # Reset Conditions
            if counter >= COMMON_REP_LIMIT:
                fullreset = True
                restart = False
                break
            if restart:
                print("Reached impossibility in Phase 3 C Assignments\nRetrying...")
                counter += 1
                break
        if not restart:
            break

    # Combine dictionaries
    Combined = Combine_Dictionaries(P2Assignments, P3Assignments)
    return {"Assignments": Combined,
            "ResetCheck": fullreset}

# Place the incompatible pairs semi-randomly.
def phase_four(P3Assignments, I, xCords, yCords):
    counter = 0
    fullreset = False
    while True:
        # Define available coordinates
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
            # If both students unassigned
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
                    if not AsubT:
                        escape = False
                        break
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

            # If ONLY left is assigned OR ONLY right is assigned
            # Uses A and B to reduce redundancy
            b = 1
            for a in range(2):
                if ((S[a] in P3Assignments) or (S[a] in P4Assignments)) and ((S[b] not in P3Assignments) and (S[b] not in P4Assignments)):
                    if S[a] in P3Assignments:
                        RC = P3Assignments[S[a]]
                    if S[a] in P4Assignments:
                        RC = P4Assignments[S[a]]
                    AsubT = []
                    while True:
                        for c in Available:
                            if c not in tried:
                                AsubT.append(c)
                        if not AsubT:
                            escape = False
                            break
                        RC2 = choice(AsubT)
                        if ((abs(RC[0] - RC2[0]) > 1) or (abs(RC[1] - RC2[1]) > 1)) and (RC2 not in P3Assignments.values()) and (RC2 not in P4Assignments.values()):
                            break
                        else:
                            tried.append(RC2)
                        if len(tried) == len(Available):
                            escape = False
                            break
                    if escape:
                        P4Assignments[S[b]] = RC2
                        Available.remove(RC2)
                b -= 1

            # Both assigned
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
            print(f"Impossibility reached in Phase 4. Retrying. (Counter: {counter})")
            counter += 1
        if counter >= MEDIUM_REP_LIMIT:
            fullreset = True
            break
    
    # Combine dictionaries
    Combined = Combine_Dictionaries(P3Assignments, P4Assignments)
    return {"Assignments": Combined,
            "ResetCheck": fullreset}

# Randomly assign coordinates to remaining students
def phase_five(P4Assignments, xCords, yCords, Names):
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
    return Names

def Combine_Dictionaries(Dict1, Dict2):
    copy1 = Dict1.copy()
    copy2 = Dict2.copy()
    copy1.update(copy2)
    return copy1