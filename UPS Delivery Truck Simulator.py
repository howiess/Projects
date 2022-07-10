"""
Copy your Package and Truck classes here
"""
class Package:

    def __init__(self, id):
        self.id = id
        self.address = ""
        self.office = ""
        self.ownerName = ""
        self.collected = False
        self.delivered = False

class Truck:

    def __init__(self, id, n, loc):
        self.id = id
        self.size = n
        self.location = loc
        self.packages = []         #{id: 'address'}
        self.mileage = 0
        self.delivered = []



    def collectPackage(self, pk):
        if len(self.packages) < self.size:
            if pk.collected == False and pk.delivered is False:
                if self.location == pk.office:
                    pk.collected = True
                    self.packages.append(pk) 
                
                    return 'Successfully collected the package.'
                else:
                    return 'The package is not at current location. '
            else:
                return 'The package has already been picked up.'
        else: 
            return "There is no enough space for the truck to pick up the package"

    def deliverPackage(self, pk):
        
            if self.location == pk.address:
            
                if pk in self.packages:
                    pk.delivered = True
                    self.delivered.append(pk)
                    self.packages.remove(pk)
                    
                    return 'Package has been successfully delivered.'
                else:
                    return "Error: The package is not in the truck."
            else:
                return 'Error: This is not the location for delivery.'
        

    def deliverPackages(self):
        

        num_packages = 0
        pk_to_deliver = []
        for pk in self.packages:
            if pk.address == self.location:
                pk_to_deliver.append(pk)  

         
        for pk in pk_to_deliver:
            self.deliverPackage(pk)
            num_packages += 1             
        if num_packages > 0:
            return 'All packages have been successfully delivered.'
        else:
            return 'Error: No packages are being sent to this location.'
        
    # Don't worry about checking whether the truck is at a post-service office.
    # The test cases will make sure of that.

    

    def removePackage(self, pk):
        if pk.collected is True:
            if pk.delivered is False:
                if pk in self.packages:
                    self.packages.remove(pk)
                    pk.collected = False  
                    pk.office = self.location              
                    return 'The package has been successfully returned to {}'.format(self.location)
                else: 
                    return "Error: The package is not in the truck."  
            
            else:
                return "Error: The package has been delivered"    
        else:
            return 'Error: The package has not been collected yet.'

    def driveTo(self, loc, dist):
        self.location = loc
        self.mileage += dist
        return 'Successfully reached the destination {}, distance covered in total is {} miles.'.format(self.location, self.mileage)

    def getPackagesIds(self):
        result = []
        for pk in self.packages:
            result.append(pk.id)
        return result




"""
deliveryService
"""

def createAdjacentList(map):
    """return the adjacent node list for the map"""
    graph = {}
    for edge in map:
        if edge[0] in graph:       # assume adjacent nodes of the edge is A and B, edge 0 is A and edge 1 is B, edge 2 is the distance in between
            graph[edge[0]].append((edge[1], edge[2]))
        else:
            graph[edge[0]] = [(edge[1], edge[2])]  # if A does not exist in graph, let's create it
        if edge[1] in graph:
            graph[edge[1]].append((edge[0], edge[2]))
        else:
            graph[edge[1]] = [(edge[0], edge[2])]
    return graph

def collectAllPackages(truck, pkTodo):   # check the truck size 
    """Return list of uncollected packages while collecting 
    packages at the location of the truck  
    Input: 
        pkTodo: list of packages that has to be collected 
    """
    uncollected = []
    for pk in pkTodo:
        if truck.size == len(truck.packages):
            break
        elif truck.location == pk.office:
            truck.collectPackage(pk)
            # print('DEBUG: collected')
        elif truck.location != pk.office:
            uncollected.append(pk)
    return (uncollected, {})

def deliverAllPackages(truck, undelivered):
    deliveredTo = {} 
    for pk in truck.packages:
        if truck.location == pk.address:
            deliveredTo[pk.id] = pk.address  # look at project instructions
            undelivered.remove(pk)
            # print('DEBUG: delivered')
    truck.deliverPackages()
    return (undelivered, deliveredTo)

def procressPackages(truck, pkTodo, mode): 
    """
    2 modes : 0 = collect packages mode, 1 = deliver packages mode for later use

    """

    if mode == 0:
        temp = collectAllPackages(truck, pkTodo)
    elif mode == 1:
        temp = deliverAllPackages(truck, pkTodo)
    return temp

def traverseMapGraph(mapGraph, truck, mode, pkTodo):
    """Traverse all the location in the mapGraph while collecting 
    or delivering packages
    Input: 
        mapGraph: the map in adjacent node list form (see above adjacentlist function)
        mode: when it is 0, collect packages, when it is 1, 
            deliver packages
    """
    deliveredTo = {} # The packages that have been delivered
    origin = truck.location # The original location
    stops = [] # Places where the truck stops
    path = [] # Path of the places where the truck stops, each element in this list is a tuple of (location, distance)
    visitedLoc = [origin] # All the locations that have been visited, no repetition of the same locaiton

    connectedLoc = mapGraph[origin] # Setup the connected locations of the origin
    
    temp = procressPackages(truck, pkTodo, mode)  # temp is a tuple, return (collectAllPackages() or DeliverAllPackages()) depends on mode
    pkTodo = temp[0]  # either undelivered or uncollected package
    deliveredTo.update(temp[1])  # update the dictionary 

    # Visit different location until all the locations have been visited
    while len(visitedLoc) != len(mapGraph) and pkTodo and (truck.size > len(truck.packages) or mode == 1):

        # check if all connected locations of this location have been visited, if so then go back 
        if all(x[0] in visitedLoc for x in connectedLoc):
            # print("DEBUG: Now going backwards")
            savedPath = path.copy()    #prevent path repetation 
            savedPath.reverse()
            i = 0
            for loc in savedPath[1:]:
                truck.driveTo(loc[0], savedPath[i][1])
                # print("DEBUG: Now going backwards to", loc[0])
                stops.append(loc[0])
                path.append(loc)
                connectedLoc = mapGraph[loc[0]]
                i += 1
                if not all(x[0] in visitedLoc for x in connectedLoc):
                    break
    
        # go to the next location that's never visited
        for loc in connectedLoc:
            # print("DEBUG: Checking Location ", loc[0])
            if loc[0] not in visitedLoc:
                truck.driveTo(loc[0], loc[1])
                # print("DEBUG: Now driving to", loc[0])
                stops.append(loc[0])
                path.append(loc)
                visitedLoc.append(loc[0])
                connectedLoc = mapGraph[loc[0]]

                temp = procressPackages(truck, pkTodo, mode)
                pkTodo = temp[0]
                deliveredTo.update(temp[1])
                break

    # print("DEBUG: VistedLoc =", len(visitedLoc))
    return (deliveredTo, stops)


def deliveryService(map, truck, packages):
    deliveredTo = {}
    stops = [truck.location]
    mapGraph = createAdjacentList(map)
    pkTodo = packages.copy()

    # print("DEBUG: Starting location is", truck.location)
    # print('DEBUG: Truck size is', truck.size)
    while len(deliveredTo) < len(packages):
        temp = traverseMapGraph(mapGraph, truck, 0, pkTodo) 
        deliveredTo.update(temp[0])
        stops += temp[1]
        
        temp = traverseMapGraph(mapGraph, truck, 1, pkTodo)
        deliveredTo.update(temp[0])
        stops += temp[1]

    return (deliveredTo, stops)


"""
testing
"""
from csv import *

def readMap():
    map = []    
    with open('map2.txt') as csvfile:        
        r = reader(csvfile, delimiter=',')        
        for row in r:            
            map.append((row[0], row[1], int(row[2])))    
    return map

def readPk():
    packages = []    
    with open('packages2.txt') as csvfile:        
        r = reader(csvfile, delimiter=',')        
        for row in r:            
            pk = Package(row[0])            
            pk.office = row[1]            
            pk.address = row[2]            
            packages.append(pk)    
    return packages

def test():
    map1 = readMap()
    pk1 = readPk()
    truck = Truck(100, 5, 'UPS1')
    result = deliveryService(map1, truck, pk1)
    delivereda = 0
    for pk in pk1:
        if pk.delivered == True:
            delivereda += 1
    for i in range(1, len(result[1])):            
        if result[1][i-1] == result[1][i]:                
            print("DEBUG:", result[1][i-1], result[1][i])
    print("DEBUG: delivered =", delivereda, "pk =", len(pk1))
    return result
