# lift-sim
## Simulator for Elevator Control

A simplified elevator simulator that follows the rules specified in the problem statement [here](http://www.cse.iitd.ac.in/~mausam/courses/col333/autumn2016/A4/A4.pdf).

This simulator has been created for Assignment 4 of the Fall 2016 course COL333 (Artificial Intelligence) at IIT-Delhi. Before solving your MDP, don't forget that honesty is the best policy.

## Usage Instructions

To run the simulator:
```bash 
python sim.py run.sh <N> <K> <p> <q> <r> <t_u>
```

run.sh should be a bash script which runs your code. It should take the arguments ```N, K, p, q, r, t_u``` as specified in the problem statement.

Optional arguments:  
-ep \<ep> : Number of episodes to play out (Default: 1000)  
-log \<log> : Name of output log file (Default: 'simulation.txt')  
-mode \<mode> : 'CUI' for a command line visualisation, 'None' for no visualisation (Default: 'CUI')

You should read subsequent updates from stdin and write actions to stdout. Debug messages can be written to stderr. On running your executable for the first time, you should send a '0' when ready. The initial state has all elevators on the first floor with no buttons pressed.

You may have a look at SimpleAgent.py and run.sh for an example agent and script.

<b>Note</b>: To create an agent in C++, write a program that:
 - reads from stdin (cin) the buttons pressed in the form of a single string. Note that the state of individual buttons is delimited by spaces. For example, if in a time step, a person shows up on the 4th floor and decides to go up, the update received would be 'BU4'. If along with this, a person enters the 2nd elevator and presses the button for the 3rd floor, the update would be 'BU4 B32'. Hence every message in the state received will be either of the form B&lt;D/U&gt;&lt;floor number&gt; or B&lt;destination&gt;&lt;elevator number&gt;. 

 The state of a button will only be sent if it's not already pressed.

 - writes actions to stdout (cout) in the form of a string, with one action per elevator separated by spaces. For example, read the actions outputted by simpleAgent inside simpleAgent.py.


## Sample Print Trace:

![alt tag](https://raw.githubusercontent.com/suragnair/lift-sim/master/sample_trace.png)

- Actions taken : action taken by the controller based on the previous state. Based on these actions, a simulation is performed and printed below.
- People Waiting Up/Down : number of people waiting to go up and down on each floor (note that this is not explicitly available to the agent).
- Floor Up/Down Buttons : In the above Episode, the BD is pressed for floors 3 and 5, and BU is pressed for floor 1.
- Elevators : A dot shows which floor the elevator is on. If it is open, then a gap is shown with the direction of the light.
- Elevator Buttons : Buttons pressed inside each elevator are shown with 'o's. For Elevator 1, button for the 5th floor is pressed while the button for the 1st floor is pressed for Elevator 2.
- Update sent : The additional updates that transpired in the last time step. In this case, the button 'BD3' was pressed since someone arrived at floor 3. If no one arrives (or presses an already pressed floor button), a '0' is sent, followed by new lift buttons pressed (if any).

## Log to PDF

To convert a .txt log to a pdf for easier viewing:

```bash
python convertToPDF.py <simulation.txt> <simulation.pdf>
```

Note: reportlab is a prerequisite and can be installed using pip:

```bash
pip install reportlab
```
