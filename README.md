# Seating50 - The Optimal Seating Plan Generator
----
## Video Demo:
https://www.youtube.com/watch?v=FfMmps0m7Tw

## Description:
For my CS50 final project, I have created a valuable tool for teachers with unruly students! Seating50 is a web application that uses four input fields to generate an optimal classroom seating plan. While proper order may be subjective to the teacher, I've found that all high-quality plans are generally based on three core conditions:

- Incompatible students are to be separated

- Compatible students can and should be placed in close proximity

- Some should be nearer the front of the classroom

While these conditions are simple in isolation, more chaotic classrooms make finding the right seating plan significantly more challenging. In fact, I was inspired to start this project when I encountered a former teacher of mine defeated with frustration due to this exact problem!

On the front end, the user may input as much information as possible regarding the conditions above. That is, compatible, incompatible, and front-bound students. They may also select up to two incompatible pairs to be deemed "Highly Incompatible." These student pairs are maximally separated. I focused much energy on making a user-friendly GUI, hoping to encourage the user to saturate the algorithm. More demanding inputs generally lead to more optimal final output.

## Usage:
Using Seating50 requires the installation of Python3 and Python's Flask framework. Otherwise, the Bootstrap files are fetched in the header of "layout.html" using a URL and all other features should be supported by your browser. Use the "flask run" command in your terminal to get started.

```bash
pip install flask
```

```bash
flask run
```

For a detailed tutorial and tour of the app, click the "Seating50 Tutorial" link in the navbar once you've generated and opened the URL. All steps should be displayed neatly by the HTML.

## How the Seating50 Algorithm Works

The sorting algorithm imagines the grid of desks as a cartesian plan, in which user-inputted constraints limit how individuals may be assigned coordinates. Essentially, students are repeatedly assigned random positions until a configuration satisfies all constraints. However, as inputs become more demanding, this approach alone becomes futile.

After initially attempting this relatively simple "pure-randomization" algorithm, I soon realized that regardless of speed, my computer could never sift through the 250 nonillion permutations of the average thirty-student classroom. I thus improved on this design by implementing methods to "guide" the randomness in the right direction. "Guided randomness" best describes this algorithm's core functionality.

The problem is broken into five phases, ordered according to the probability* of their events occurring by chance. In the first two phases, highly incompatible students are placed on the margins, and front-bound students in the first two rows. With a freshly empty coordinate plane, placing these otherwise highly restricted input categories is easy. Finishing these steps first thus prevents "bottlenecking" later on.

*I have not proven that any event is more probable than the next, but this order seemed most intuitive.

```python
# Typical "Phase" in seating_algorithm():
while True:
    # PHASE 1: Separate HI pairs with their partners
    P1 = phase_one(Partners, HI, HI_C_F, HI_C, HI_F, C, F, I, Width, yCords)
    Assignments = P1["Assignments"]
    P1Assignments = Assignments.copy()
    # Ensure assignments pass all constraints
    if I_check(Assignments, I) and F_check(Assignments, F) and C_check(Assignments, C, Partners):
        print("P1 successful")
        C = P1["Edited_C"]
        Removed3 = P1["Removed"]
        break
    if not I_check(Assignments, I):
        P1IFailCounter += 1
    print("Retrying P1 (Did not pass checks)")
    P1Counter += 1
    if P1Counter >= COMMON_REP_LIMIT:
        escape_loop = False
        break
```

In the third phase, all compatible student pairs are placed contiguously on the horizontal (Ie, side-by-side facing the front of the class). In a class without partnered desks, there are many logical impossibilities with this sort of placement that must be considered before this phase. (See "Logical Impossibilities"). One partner in each pair is placed randomly, while the other is forcibly located beside them if possible. This repeated neighboring becomes almost impossible by pure chance, so my approach yields significantly reduced running time while still allowing for a high degree of randomness.

Finally, the incompatible and uncategorized students are placed last in the fourth and fifth phases. The incompatible pairs are placed similarly to the compatibles in that only one of the students in each pair is placed randomly (if still unplaced). The other student takes a position that is sufficiently distant from their partner. If no such positions exist, then the whole process is partially or fully reset, depending on how many attempts have been made.

After every distinct complete student placement operation in the algorithm, a counter tracks how many unsuccessful attempts have been made. If this counter reaches its particular "Rep Limit" (a value I determined somewhat arbitrarily with some testing), the whole algorithm will be reset, and some user input may be neglected. Neglecting user input only occurs when demand is highly strenuous and may be nearing or completely impossible in order to de-stress the algorithm:

```python
## Some logic for neglecting user input after "REP_LIMIT" attempts=
# Loop repetition limits
COMMON_REP_LIMIT = 20
MEDIUM_REP_LIMIT = 100
HIGH_REP_LIMIT = 1000
HIGHER_REP_LIMIT = 10000

# Fix C pairs after P3FailCounter gets sufficiently high
shuffle(OriginalC)
if P3FailCounter > HIGH_REP_LIMIT or P2CFailCounter > HIGHER_REP_LIMIT:
    output = fix_compatibles_2(C, C_F, SIwidthLimit2)
    C = output["C"]
    RemovedC = RemovedC + output["Removed4"]
    P3FailCounter, P2CFailCounter = 0, 0
# Overwhelming I pairs list occuring in P2 or P3. Neglect a pair.
if P1IFailCounter > MEDIUM_REP_LIMIT or P2IFailCounter > HIGHER_REP_LIMIT or P3IFailCounter > HIGHER_REP_LIMIT or P4IFailCounter > HIGH_REP_LIMIT:
    I_F_pair = find_IF(I, F)
    if I_F_pair and P2IFailCounter > HIGHER_REP_LIMIT:
        I.remove(I_F_pair)
        RemovedI.append(I_F_pair)
    else:
        Rand_I_Pair = choice(I)
        I.remove(Rand_I_Pair)
        RemovedI.append(Rand_I_Pair)
    P1IFailCounter, P2IFailCounter, P3IFailCounter, P4IFailCounter = 0, 0, 0, 0
```

## Challenges

- Multi-Category-Inputs: Some students can exist in several, if not ALL, categories. For example, student "A" could be front-bound, compatible with "B," incompatible with "C," and highly incompatible with "D." These students are sometimes treated differently in the algorithm due to their lower likelihood of being correctly located. Multi-Category students are stored as their individual lists separated by underscores in the code:

```python
# Find and store students who exist in multiple categories.
MCS = get_MCS(HI, C, F)
HI_C_F = MCS["HI_C_F"]
HI_C = MCS["HI_C"]
HI_F = MCS["HI_F"]
C_F = MCS["C_F"]
```

- Codebase Size: Admittedly, the logic for this algorithm could probably have been condensed and designed more optimally. There is slight redundancy in the algorithm's five phases, which could have been reduced, but I did my best to keep it at a minimum. Consequently, the program became quite large, and bugs became more challenging to locate and fix in the later stages. I conducted the heaviest testing when the frontend GUI had been fully developed; at this point, the codebase was nearing two thousand lines in aggregate. Thus, I uncovered the most bugs when fixing them was most strenuous! Frustratingly, the most painful bugs were simple logical errors I initially overlooked. These often involved indexing into empty lists, getting stuck in loops due to logical placement impossibilities, and slight errors in my reasoning in solving smaller-scope problems. In fact, after hours of painful searching, most of these could be solved with a simple "if" statement.

- JavaScript: Before starting this project, my knowledge of Javascript syntax and capabilities needed to be improved. Much research was required to begin the GUI, and I often found myself browsing the web for solutions to various problems while implementing it. The functionality was thus the most challenging part of the front end, as I already knew a sufficient amount of CSS, HTML, and Bootstrap.

## Logical Impossibilities

Among my encountered challenges were several logical impossibilities that were difficult to uncover and especially difficult to treat with code. The algorithm deals with these problems before any substantial student placement occurs.

- Compatible and Highly Incompatible Impossibility: If student "A" and "B" are highly incompatible, then student "C" cannot be compatible with BOTH "A" and "B." In this case, one of the compatible pairs is neglected.

- Outer Margin Impossibility: Compatible partners of students that belong in the "Highly Incompatible" category may cause problems. Since highly incompatible students must be placed on the margins, it may become impossible for their partners to be placed contiguous to them. Example: "A" + "B" are compatible, but so are "C" + "B". If B is stuck in the second column of the grid, then we could run into problems. If "E" + "A" and "F" + "C" are also compatible pairs, then placement of one of the former would be impossible. For this reason, these pairs are omitted for simplicity.

- Loop Impossibility / Comp String Overstretch: In a non-partnered classroom, the user can choose compatible pairs in a way that will form a "string" in the final plan. Example: If "A" + "B", &nbsp;"B" + "C", &nbsp;"C" + "D", &nbsp;and "D" + "E" are compatible pairs, then they will form a five-student-long string due to the logic in Phase 3 mentioned earlier. These "Comp Strings," as I call them, pose two problems:

    - Comp String Overstretch: The seating plan is only possible to generate if the Comp String length is within the width of the classroom, but shorter strings create problems of their own. Being larger blocks of definite structure, Comp Strings can reduce the number of total possible classroom permutations and, in many cases, will make the constraints wholly or nearly impossible to satisfy. From testing, I observed that this shrinking of possibilities becomes significantly more problematic as the Comp String amount and length are increased.

    - Loop Impossibility: A loop is formed whenever a Comp String starts and ends with the same student. The simplest version of this situation would be: "A" + "B",&nbsp; "B" + "C" and "C" + "A" compatible pairs. Since this algorithm places Comp pairs contiguously in the x-direction, placing these pairs would be logically impossible. At best, one of the pairs will always be separated.

    To account for these issues, the recursive "loop_check()" is called in "fix_compatibles()." This function essentially "travels" down these strings and counts the number of pairs therein. When this counter exceeds "Classwidth - 3" (an arbitrary limit stored in the SIwidthLimit variable), the middle pair of the Comp String is removed and neglected entirely. Later, if the compatible pairs continue to restrict the algorithm from finding a valid solution, "loop_check()" will be called again with a smaller Comp String length limit. This solution is another example of the algorithm "de-stressing" itself when necessary. The Loop Impossibility is also solved in "loop_check()" by a base case that checks if any students in the Comp String match the first inputted "Base" student.

```python
# Moves along "strings" of compatible partners and detects when these strings are too long, or impossible to place.
def loop_check(BaseStudent, OtherS, PreviousStudent, Counter, C, Limit, Removed, pair, PairToElim):
    Buddies = find_buddies(OtherS, C)
    Buddies.remove(PreviousStudent)
    if Counter > Limit:
        C.remove(PairToElim)
        print(f"C string too long. Removed: {PairToElim}")
        Removed.append(PairToElim)
        return True
        # String too long
    if Counter == round(Limit / 2):
        # Find "half-way" pair
        if [OtherS, PreviousStudent] in C:
            PairToElim = [OtherS, PreviousStudent]
        else:
            PairToElim = [PreviousStudent, OtherS]
    if not Buddies:
        return False
        # No partners, therefore no loop/ end of string
    if Buddies[0] == BaseStudent:
        C.remove(PairToElim)
        Removed.append(PairToElim)
        print(f"Comp loop found. Removed: {PairToElim}")
        return True
        # Loop found!
    Counter += 1
    PreviousStudent = OtherS
    OtherS = Buddies[0]
    return loop_check(BaseStudent, OtherS, PreviousStudent, Counter, C, Limit, Removed, pair, PairToElim)
```

## Important Files Involved

Using the CSS properties "display: hidden" and "display: block," I could store the main HTML into two documents. By consolidating all this code, I can minimize the amount of backend requests and thus allow for a more seamless user experience. "Index.html" stores the HTML for the classroom dimension selection and student name input area. Once the user inputs the names, "app.py" renders "compatibles.html," which stores the rest of the visuals. Whenever users need a tutorial, they may select the "Seating50 Tutorial" button in the navbar to render "tutorial.html."

```CSS
    /* Initial visibility of elements for first page */
    #titleOverall {display: block;}
    #dimensions {display: none;}
    #NameList {display: none;}

    /* Initial visibiliy of elements for second page */
    #InfoTitle {display:block;}
    #NextButton {display:none;height:40px;width:80px;}
    #compTables {display:block;}
    .FrontDesc {display:none;opacity:0;}
    #SecondNextButton {height:40px;width:80px;}
    #FinalTable {display:none;opacity:0;}
    #LoadingScreen {display:none;opacity:0;}
    #plan {display:none;}
    #PlanTables {display:none;}
    #ResetButtons {display:none;}
    #RemovedPairsDesc {display:none;}
    #Timeout {display: none;}
```

On the backend, "app.py" handles all server responses and stores user-chosen compatible and incompatible student pairs as session data. The usage of the session object allows the user to continue selecting pairs or regenerate their plan as much as needed. To generate the plan, "app.py" calls "seating_alorithm()" to process the user's demands.

Lastly, "script.js" stores the javascript code that allows for almost all the functionality on the front end. I kept all arbitrarily chosen constants in the global scope to make the code easily adjustable and to avoid magic numbers. The file is organized into sections that serve different key roles, such as page transitions, animations, AJAX request handling, and main functionality in each HTML document.

```javascript
// Some adjustable constants that exist in the global scope

const max_height = 6
const min_height = 3
const max_width = 8
const min_width = 3
const PrcntgeOfHeight = 95;
const PartnerModeDeskHeight = "60%";
const FullHeight = "100%";

const IncompBG = 'rgba(220, 20, 60, 0.1)';
const CompBG = 'rgba(34, 139, 34, 0.1)';
const DarkBG = 'rgb(80, 172, 203)';
const LightBG = 'rgb(173, 216, 230)';
const DBLclickBorder = '2px solid crimson';

const FrontLimit = 3;
const MaxIncompPairAreaDivisor = 2;
const MaxCompPairAreaDivisor = 1.5;
const NxtBtnDivisor = 2.5;
```

## Conclusion and Future Updates
Seating50 uses a "guided randomization" approach to create an optimal classroom seating plan. The quality of this plan depends on the volume of user input, which pertains to three code conditions. In implementing the algorithm, some logical impossibilities, along with general codebase size, made bug fixing an arduous task. In the end, the algorithm may not yet be perfect, but this approach is a step in the right direction for solving many similar organizations in the future.

In upcoming updates, I want to add tolerance for a larger variety of classroom layouts, perhaps larger tables in different formations. I am also looking to find ways to allow the algorithm to take in more input. At the moment, it accepts more input than I ever thought it would, but the algorithm always reaches a "wall" at a certain point. Sufficiently high demand will obviously become impossible to fulfill, but I have yet to reach the limit. Seating50 undoubtedly has room for improvement!


