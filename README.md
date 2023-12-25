# Seating50
----
## Video Demo: 
## Description:

For my CS50 final project, I have created a useful tool for teachers with unruly students! Seating50 is a web application that uses four input fields to generate an optimal classroom seating plan. While proper order may be subjective to the teacher, I've found that all high quality plans are generally based on three core conditions:

1. Incompatible students are to be seperated
2. Compatible students can and should be placed in close proximity
3. Some should be nearer the front of the classroom

While these conditions are simple in isolation, more chaotic classrooms make the right seating plan significantly harder to find. In fact, I was inspired to start this project when I encountered a former teacher of mine defeated with frustration due to this exact problem!

On the frontend, the user may input as much information as possible that pertains to the aforementioned conditions. That is, compatible, incompatible and front-bound students. They may also select up to two of their incompatible pairs to be deemed "Highly Incompatible." These student pairs are maximally separated. I focused much energy into making a user-friendly GUI, hoping to encourage the user the saturate the algorithm. More demanding inputs generally lead to more optimal final output.

## How It Works

The sorting algorithm imagines the grid of desks as a cartesian plan, in which user-inputted constraints limit how individuals may be assigned coordinates therein. Essentially, students are repeatedly assigned random positions until a configuration is found that satisfies all constraints. However, as inputs become more demanding, this approach alone becomes futile.

After attempting this relatively simple "pure-randomization" algorithm, I soon realised that my computer, regardless of speed, could never sift through the 250 nonillion permutations of the average thirty student classroom. I thus improved on this design by implementing methods by which to "guide" the randomness in the right direction. "Guided randomness" is the best description of this algorithm's core functionality.

The problem is broken into five phases, ordered according to the probability* of their events occuring by chance. In the first two phases, highly incompatible students are placed on the margins, and front-bound students in the first two rows. With a freshly empty cordinate plane, it is easy to place these otherwise highly restricted categories of input. Finishing these steps first thus prevents "bottlenecking" later on.

In the third phase, all compatible student pairs are placed contiguously on the horizontal (Ie: side-by-side facing the front of the class). In a class without partnered desks, there are many logical impossibilties attributed to this sort of placement that must be considered before this phase. (See "Challenges Encountered"). One partner in each pair is placed randomly, while the other is forcibly located beside them if possible. This repeated neighbooring becomes almost impossible by pure chance, so my approach yields significantly reduced running time while still allowing for a high degree of randomness.

Finally, in the fourth and fifth phases, the incompatible and uncategorized students are placed last. The incompatible pairs are placed similarly to the compatibles, in that only one of the students in each pair is placed randomly (if still unplaced). The other student takes a position that is suffiently distant from their partner. If no such positions exist, then the whole process is partilly or fully resetted, depending on how many attempts have been made.

After every distinct complete student placement operation in the algorithm, there is a counter that tracks how many unsuccesful attemps have been made. If this counter reaches its particular "Rep Limit" (a value I determined somewhat arbitrarily with some testing), then the whole algorithm will be resetted and/or some user input may be neglected. Neglecting user input only occurs when demand is highly strenuous and may be nearing or completely impossible so as to de-stress the algorithm.

*I have not proven that any event is more probable than the next, but this order seemed most intuitive.

## Challenges

-Multi-Category-Inputs: It is possible for some students to exist several, if not ALL categories. For example, student "A" could be front-bound, compatible with "B", incompatible with "C" and highly incompatible with "D." These students are sometimes treated differently in the algortihm due to their lower likelihood of being properly located.

-Logical Impossibilities:

-Code-Base Size:

-JavaScript: 

## Logical Impossibilities

Among my encountered challenges were several logical impossibilities that were difficult uncover, and especially difficult to treat with code. The algorithm deals with these problems before any substantial student placement occurs.

Compatible and Highly Incompatible Impossibility: If student "A" and "B" are highly incomptible, then student "C" cannot be compatible with BOTH of "A" and "B". In this case, one of the compatible pairs is neglected.

Outer Margin Impossibility: Compatible partners of students that belong in the "Highly Incompatible" category may cause problems. Since highly incompatible students must be placed on the margins, it may become impossible for their partners to be placed contiguous to them. Example: "A" and "B" are compatible, but so are "C" and "B". If B is stuck in the second column of the grid, then we could run into problems. If "E", "A" and "F", "C" are also compatible pairs, then placement of one of the former would be impossible. For this reason, these pairs are totally omitted for simplicity.

Loop Impossibility / Comp String Overstretch: In a non-partnered classroom, you can chose compatible pairs in a way that will form a "string" in the final plan. Example: If "A" + "B", "B" + "C", "C" + "D", and "D" + "E" are compatible pairs, then they will form a five student long string due to the logic in Phase 3 mentioned earlier. These "Comp Strings", as I call them, pose two problems.

    1. Comp String Overstretch: The seating plan is obviously impossible to generate if the Comp String length exceeds the width of the classroom, but shorter strings create problems of their own. Being larger blocks of definite structure, Comp Strings can reduce the number of total possible classroom permutations and in many cases will make the constraints nearly or completely impossible to satisfy. From testing, I observed that this shrinking of possibilities becomes significantly more problematic as Comp String amount and/or length is increased.

    2. Loop Impossibility: The simplest version of this situation would be: "A" + "B", "B" + "C" and "C" + "A" compatible pairs. Given that this algorithm places Comp pairs contiguously in the x-direction, placing these pairs would be logically impossible. At best, one of the pairs will always be separated.

To account for these issues, the recursive "loop_check()" is called in "fix_compatibles()". This function essentially "travels" down these strings and counts how many pairs exist therein. When this counter exceeds "Classwidth - 3" (an arbitrary limit stored in the SIwidthLimit varible), the middle pair of the Comp String is removed and neglected entirely. Later on, if the compatible pairs continue to restrict the algorithm from finding a valid solution, "loop_check()" will be called again with a smaller Comp String length limit. This solution is another example of the algorithm "de-stressing" itself when necessary. The loop impossibility is solved in the same function ..........




