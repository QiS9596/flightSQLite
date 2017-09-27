"""
for the purpose that if we search for a long time period, and the Best First Search algorithm may cost too much time,
we might use greedy approximation in the first phase of searching process and in the second phase use BFS to make sure
that the searching can lead to the exact destination. This modula provides a way of greedy approximation algorithm in
the initial phase.

randomwalk greedy algorithm maintains a group of K nodes, in each iteration expands these node. The node are generated
based on probability calculated by the mileage, and then select the K best nodes in the new generated nodes.

"""
import sql
import BFS
import datetime

class randomwalk:
    def __init__(self,flightDBManager,startDatetime):
        self.flightDBManager = flightDBManager
        self.startDatetime = startDatetime
        self.currentDatetime = startDatetime
        pass

    def walk(self):
        pass

