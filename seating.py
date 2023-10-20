import random
import sys
import csv

HI_C_F = []
HI_C = []
HI_F = []
C_F = []
HI = []
C = []
F = []
I = []

Names = {}
xCords = []
yCords = []

Neglected = []

def main():
    load_names()
    
    Partners = False
    while True:
        inpt = input("Partnered desks? (y/n)\n").lower().strip()
        if inpt == "yes" or inpt == "y":
            Partners = True
            break
        elif inpt == "no" or inpt == "n":
            Partners = False
            break

    get_C(Partners)
    print(C)
    #get_I()
    #get_HI()
    #get_F()





def load_names():
    with open("Final-Project/names.txt") as inputF:
        for name in inputF:
            Names[name.strip()] = "empty"

def get_C(Partners):
    # Instructions
    print("List students that may be seated beside one another. Press ENTER when finished.")
    if Partners:
        print("Note: You have specified that students will be seated at partnered desks. A student can thus only have one partner!")
    else:
        print("Note: A student may have a maximum of TWO partners.")
    # Get inputs
    dirtyC = []
    stop = False
    while True:
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
            dirtyC.append([S1, S2])
    # Rid dups
    for pair in dirtyC:
        InversePair = [pair[1], pair[0]]
        if (not pair in C) and (not InversePair in C):
            C.append(pair)
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
        else:
            break


    
    
        
































main()