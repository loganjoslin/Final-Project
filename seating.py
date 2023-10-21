import random
import sys
import csv

Names = {}
xCords = []
yCords = []
Neglected = []

def main():

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

    print("List students that may be seated beside one another. Press ENTER when finished.")
    print("Note: You have specified that students will be seated at partnered desks. A student can thus only have one partner!") if Partners else print("Note: A student may have a maximum of TWO partners.")
    C = get_pairs(None)
    C = fix_compatibles(C, Partners)

    print("List students who should not be beside eachother. Press ENTER when finished")
    I = get_pairs(None)

    limit = int(round(len(xCords) / 3))
    print(f"List students who should not be near the front of the class. You are limited to {limit}. Press ENTER when finished.")
    F = get_fronts(limit)

    find_contradiction(HI, C, I)

    MCS = get_MCS(HI, C, F)
    HI_C_F = MCS["HI_C_F"]
    HI_C = MCS["HI_C"]
    HI_F = MCS["HI_F"]
    C_F = MCS["C_F"]

    print(Names)
    print(C)
    print(I)
    print(HI)
    print(HI_C_F)
    print(HI_C)
    print(HI_F)
    print(C_F)




def load_names():
    with open("Final-Project/names.txt") as inputF:
        for name in inputF:
            Names[name.strip()] = "empty"

def fix_compatibles(C, Partners):
    # Cleanse compatibles of logical impossibilities
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
        # (a,b)(a,c)(b,c) impossibiltiy
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
            choice = random.choice(problems)
            C.remove(choice)
            Neglected.append(choice)
        else:
            break
    return C

def get_pairs(Limit):
    # Get inputs
    drtyPairs = []
    pairs = []
    stop = False
    while True:
        if not Limit == None and len(drtyPairs) >= Limit:
            break
        while True:
            S1 = input("Student 1: ").strip().capitalize()
            if S1 in Names or S1.lower() in Names:
                break
            elif S1.lower() == "":
                stop = True
                break
            else:
                print("Student not in list. Try again.")
        if stop == True:
            break
        while True:
            S2 = input("Student 2: ").strip().capitalize()
            if (S2 in Names or S2.lower() in Names) and not S2 == S1:
                break
            elif S2.lower() == "":
                stop = True
                break
            elif S2 == S1:
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

def get_fronts(limit):
    F = []
    stop = False
    count = 0
    while True:
        while True:
            S = input("Student: ").strip().capitalize()
            if (S in Names or S.lower() in Names or S.capitalize() in Names) and S not in F:
                count += 1
                break
            elif S.lower() == "":
                stop = True
                break
            elif S in F:
                print("No duplicate inputs!")
            else:
                print("Student not in list. Try again.")
        if stop == True or count == limit:
            if not S == "":
                F.append(S)
            break
        else:
            F.append(S)
    return F

def get_MCS(HI, C, F):
    C_list = []
    HI_list = []
    HI_C_F = []
    HI_C = []
    HI_F = []
    C_F = []
    for pair in C:
        for x in range(1):
            if pair[x] not in C_list:
                C_list.append(pair[x])
    for pair in HI:
        for x in range(1):
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

def find_contradiction(HI, C, I):
    for pair in C:
        invpair = [pair[1], pair[0]]
        for x in [pair, invpair]:
            for y in [HI, I]:
                if (x in y):
                    print(f"\nYou inputted {x[0]} and {x[1]} as both COMPATIBLE and INCOMPATIBLE!\n")
                    answer = input(f"If you would like them to be COMPATIBLE, type 'C'\nFor INCOMPATIBLE, type 'I'\nTo remove this pair altogether, type 'R'\n").lower()
                    while True:
                        if answer == "c":
                            y.remove(x)
                            break
                        elif answer == "i":
                            C.remove(x)
                            break
                        elif answer == "r":
                            y.remove(x)
                            C.remove(x)
                            break
                        else:
                            print("Invalid input.")

def get_grid_dimensions(Partners):
    width = int(input("Class width: "))
    height = int(input("Class height: "))
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


    




    
    
        
































main()