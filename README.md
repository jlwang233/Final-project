# Title: Finding Seats in Library

## Team Member(s):
Jialu Wang, Qi Qi

# Monte Carlo Simulation Scenario & Purpose:
During final month, it is difficult to get a seat in the library.

We want to find how long people will wait until they find a seat in a library. 

We observe two types of study units in a library:

1. individual student (1)
2. study group (2-6)

We observe three types of seat:
1. study desk (1)
2. study table (6)
3. study room (up tp 6)

### Hypothesis before running the simulation:
1. indiv will first choose desk then table with vacancy.
2. group will first choose room then table available amount of seats.
3. a room can only seat a single group; a desk can only seat a single individual; table can seat both groups and individuals as long as there are enough seats
4. seatID 1-75 are study desks; 76-100 are study rooms; 101-150 are study tables.
5. average incoming study unit rate is 5 min/unit.
6. FIFO. Study unit should wait in queue until there are enought seats for them.

### Simulation's variables of uncertainty
1. size of incoming study unit
2. stay time of existing study unit

## Instructions on how to use the program:
- input: the number of study unit -including individual and group; the number of simulations.
- output: total and average waiting time for all the study unit in line; tasks remaining (the number of study unit still wait in line); the last study unit has to wait.
- main structure: 4 classes- studyUnit, seat, table, tableUnit; 1 main function - schedule() 

## Sources Used:
