from asyncio import PriorityQueue
import datetime
import sql
import util
from SendData2mySQL import mySQLFlightManager
startDatetime = None  #the start date time set by user
endDatetime = None   #the arrival deadline set by user
TIME_END_FLAG = 10000 #some big constant used in eval()
DESTINATION_FLAG = 100000  #some big constant
MAXIMUM_CYCLE_LIMIT = 10000 #a big constant used to limit the iteration loop number
destination = None  #global variable holds the destination
flightDBManager = mySQLFlightManager()
    #sql.FlightTestingDBManager()

def earlyTo(datetime1,datetime2):
    sec = (datetime1-datetime2).total_seconds()
    if sec < 0:
        return True
    else: return False

class flight:
    """
    flight class that holds the information of a single flight
    this class get %H:%M and a datetime object as date input,
    and set the flight's departure and arrival time with them
    """
    arrivalTime = None #
    departureTime = None
    flightNO = None
    Mileage = None
    destination = None
    departureCity = None
    def __init__(self, departure_time_str, arrival_time_str, flightNO, Mileage, destination, departureCity, current_date):
        self.flightNO = flightNO
        self.Mileage = Mileage
        self.destination = destination
        self.departureCity = departureCity
        year = current_date.year
        month = current_date.month
        day = current_date.day
        self.departureTime = sql.DateStringGenerator.toDateObject(departure_time_str, year, month, day)
        self.arrivalTime = sql.DateStringGenerator.toDateObject(arrival_time_str,year,month,day)
        if sql.DateStringGenerator.earlyThan(arrival_time_str, departure_time_str):
            self.arrivalTime= self.arrivalTime + datetime.timedelta(days = 1)

class city:
    city_name = None
    def __init__(self,city_name):
        self.city_name = city_name
    def getDepartureFlight(self, current_date):
        flightList = list(flightDBManager.getAvaliableFlightList(self.city_name))
        result = []
        for f in flightList:
            current_flight = flight(f[2],f[3],f[5],f[4],f[1],f[0],current_date)
            if earlyTo(current_date, current_flight.departureTime):
                result.append(current_flight)
        return result

class node:
  """
    node class used to store the information of a plan
    flightNO is the history of all flight the user should take
    val is the estimation of the current plan
  """
  flightHistory = []
  val = 0
  currentairport = None
  currentDatetime = startDatetime

  def __init__(self,currentairport = None,history = None,flight = None):
    if not currentairport == None:
        self.currentairport = currentairport
        return
    if earlyTo(history.currentDatetime,flight.departureTime):
        self.flightHistory = history.flightHistory[:]
        self.flightHistory.append(flight)
        self.val += flight.Mileage
        self.currentDatetime = flight.arrivalTime
        self.currentairport = city(flight.destination)
  def __lt__(self, other):
      if self.eval()<other.eval():
          return True
      return False
  def __eq__(self, other):
    if not self.flightHistory.__len__() == other.flightHistory.__len__():
        return False
    if not self.eval() == other.eval():
        return False
    if not self.currentairport.city_name == other.currentairport.city_name:
        return False
    if not self.currentDatetime == other.currentDatetime:
        return False
    return True

  def eval(self):
    if self.flightHistory.__len__() == 0:
        return 0
    a = self.val
    self.currentDatetime = self.flightHistory[self.flightHistory.__len__()-1].arrivalTime
    if self.currentairport.city_name == destination.city_name:
      a += DESTINATION_FLAG
    if not earlyTo(self.currentDatetime, endDatetime):
      a -= TIME_END_FLAG
    return a

def BFS(StartCity,EndCity):
  """
    Input the start city and destination city.
    Returns the node object, in which we can find the entire flight plan
    Should set start datetime and end datetime before calling
  """
  pq = PriorityQueue()#priority queue is a builtin lower first priority queue that handle tuples like (priority, object)
  global destination
  destination = EndCity
  startNode = node(currentairport=StartCity)
  startNode.currentDatetime = startDatetime
  pq.put_nowait((-startNode.eval(),startNode))#put the starting city into the queue
  count = 0
  last = 0
  result = []#candidates for result, containing local maximum and global maximum
  while (not pq.empty()) and (count < MAXIMUM_CYCLE_LIMIT):
    print(count)
    #in each iteration we get the node with best estimation
    #and explore every avaliable flight
    current = pq.get_nowait()[1]
    if current.currentairport.city_name == destination.city_name  :
        #pq.put_nowait((-current.eval(),current))
        if 0<= (endDatetime - current.currentDatetime).days < 1:
            return current
    last = current.eval()
    resultflag = True
    todayAndTomorrow = current.currentairport.getDepartureFlight(current.currentDatetime)
    tomorrow = util.getTomorrowDatetime(current.currentDatetime)
    todayAndTomorrow+=(current.currentairport.getDepartureFlight(tomorrow))
    for flight in todayAndTomorrow:
      if earlyTo(current.currentDatetime,flight.departureTime):
        newNode = node(history=current,flight=flight)
        if newNode.eval() > last: #if some value of the desendents of current node is greater than current, it won't be a maximum
          resultflag = False
        a = -newNode.eval()
        pq.put_nowait((a, newNode))
    if resultflag:#otherwise it's a local maximum or global maximum
      result.append(current)
    count += 1

  for a in result:#get all of these maximum value together and return the one with maximum value
    pq.put_nowait((-a.eval(),a))
  return pq.get_nowait()[1]

#start_city = city("miyazaki")
#end_city = city("okinawa")
#startDatetime = datetime.datetime.now()
#endDatetime = startDatetime + datetime.timedelta(days=20)


def search(start_city,end_city,startdate,enddate):
    start_city = city(start_city)
    end_city = city(end_city)
    global startDatetime,endDatetime
    startDatetime = startdate
    endDatetime = enddate
    history = BFS(start_city,end_city).flightHistory
    return history

def check(history, start_city, end_city, startdate, enddate):
    pass

# history = search("miyazaki","okinawa",datetime.datetime.now(),datetime.datetime.now() + datetime.timedelta(days=20))
# for ticket in history:
#     print(ticket.departureTime)
#     print(ticket.arrivalTime)
#     print(ticket.flightNO)
