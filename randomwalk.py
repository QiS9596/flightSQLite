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
import util
import random

DEFAULT_GROUP_SIZE = 20
class randomwalk:
    def __init__(self,startDatetime,endDatetime,start_city,flightDBManager = sql.FlightTestingDBManager(), group_size = DEFAULT_GROUP_SIZE):
        """

        :param flightDBManager: sql.FlightTestingDBManager object instance
        :param startDatetime: start searching datetime, datetime object instance
        :param endDatetime: end date time of the randomwalk process. note this is the datetime of trans phase, not the final arrival
        :param start_city: BFS.city object instance
        :param group_size: group size that the algorithm maintains
        """
        self.flightDBManager = flightDBManager
        self.startDatetime = startDatetime
        self.currentDatetime = startDatetime
        self.endDatetime = startDatetime
        self.start_city = start_city
        self.groupe_size = group_size

    def walk(self):
        """
        the body of the searching algorithm.
        should be called to envoke the random searching algorithm
        :return: a list of BFS.node
        """
        initial = BFS.node(currentairport= self.start_city)
        initial.currentDatetime = self.currentDatetime
        group = self.step(initial)
        while not self.decided_stop_searching(group):
            group = self.step(group)
        return group




    def step(self, startnode):
        """
        a step of random walk.
        start from BFS.node instance startnode, randomly select it's son nodes based on the mileage
        :param startnode: the node where we start our journey
        :return: a list of BFS.node instance of size self.groupe_size
        """
        currentcity = startnode.currentairport
        avil_flight_list = currentcity.getDepartureFlight()
        selectedFlight = []
        prob = []
        for flight in avil_flight_list:
            prob.append(flight.Mileage)
        while selectedFlight.__len__ <  self.groupe_size:
            selectedFlight.append(util.select_on_prob(avil_flight_list,prob))
        if not selectedFlight.__len__ == self.groupe_size:
            raise Exception('randomwalk modula: randomwalk class: step func: selectedFlight generating error')
        result = []
        for flight in selectedFlight:
            newnode = BFS.node(history=startnode,flight=flight)
            result.append(newnode)
        return result

    def decided_stop_searching(self,group):
        """
        decide if we should end random searching process and start Best First Searching process
        based on a random check on if some node exceeds the end date time
        :param group: the current group, a list of BFS.node instance of size = self.group_size
        :return: bool value of if we should stop the random waik process
        """
        test_times = int(0.1*self.groupe_size) + 1
        for i in range(0,test_times):
            test_index = random.randint(0,self.groupe_size-1)
            test_target = group[test_index]
            current = test_target.currentDatetime
            if not BFS.earlyTo(current,self.endDatetime):
                return True
        return False