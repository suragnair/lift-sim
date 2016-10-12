# lift-sim
## Simulator for Elevator Control

A simplified elevator simulator that follows the rules specified in the problem statement [here](http://www.cse.iitd.ac.in/~mausam/courses/col333/autumn2016/)
This simulator has been created for Assignment 4 of the fall 2016 course COL333 (Artificial Intelligence) at IIT-Delhi. Before solving your MDP, don't forget that honesty is the best policy.

## Usage Instructions

Your executable should take the arguments ```N, K, p, q, r, t_u``` as specified in the problem statement.

To run the simulator:
```bash 
python sim.py <run.sh> <N> <K> <p> <q> <r> <t_u>
```

run.sh should be a bash script which runs your code.

Optional arguments:  
-ep \<ep>     : Number of episodes to play out (Default: 1000)  
-mode \<mode> : 'CUI' for a command line visualisation, 'None' for no visualisation (Default: 'CUI')
-log \<log>   : Name of output log file (Default: simulation.txt)

You should read/write updates/actions from stdin/to stdout respectively. Debug messages can be written to stderr. On running your executable for the first time, you should send a '0' when ready. You may have a look at SimpleAgent.py and run.sh for an example agent.
