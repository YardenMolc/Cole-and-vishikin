# Distributed Algorithm - Cole and vishikin- alg

I searched everywere on the web implemetion of cole and vishiking Distributed Algorithm for graph coloring but I couldnt find any, so I decided to make one by myself

Because I have only one computer I made a simulate file which return me a graph where each node in the graph is a computer 

one more thing, we have a master file whice contorl the rounds , each vertex listinening on the UDP port to the master and can send a message to the master that he (vertex) want to continue to next round, when all vertex completed the round, the master sending the number of the next round 

the nodes in the graph can communicate only with theirs childerns/parents and thet are sending/listening on TCP port.

In the end of the run time , we are getting txt file with the id of the vertex which contain is final color, and we are getting an output log file so we can see the process , what and to where each vertrex send her new color.


<h4> Starting the simultation </h4>  

First run simlate.py and enter the number of vertex in the graph
Secondly , run the master.py and enter the exact same number of vertex

<h3> for ploting the final graph (by color) run plot.py (Thank you Itzik for the helps in ploting the graph) </h3>

