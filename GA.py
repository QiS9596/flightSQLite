import BFS
import sql
class Node:
    """
    Node class for Genetic Algorithm,
    generate a table for each day
    Each table contains an entity for each flight and a bool value representing wether to take it
    """
    def __init__(self, startDate, endDate):
        pass

    def eval(self):
        pass

    class table:

        def __init__(self):
            pass
        def getStartCity(self):
            pass
        def getFinalCity(self):
            pass
        def getFirstDepatureTime(self):
            pass
        def getLastDepatureTime(self):
            pass

        class tableElement:
            flight = None
            taken = False
            def __init__(self, flight, taken):
                self.flight = flight
                self.taken = taken