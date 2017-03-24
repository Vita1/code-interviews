import json
import math
from pprint import pprint

def calculateDistance(origin, destination):
    '''
    calculateDistance

    Calculate the great circle distance between the origin and the destination.
    It does not matter which location is origin and which is destination.

    Arguments:
        origin, destination (tuples): [0] is latitude, [1] is longitude

    Return values:
        (float): distance in kilometers

    '''
    # origin[0] is latitude, origin[1] is longitude
    # similar for destination
    angle = math.acos(math.sin(origin[0]) * math.sin(destination[0]) + \
        math.cos(origin[0]) * math.cos(destination[0]) * \
        math.cos(abs(origin[1] - destination[1])))
    # 6371 is the radius of the earth in kilometers
    return 6371 * math.radians(angle) 


def getNearbyCustomers(file, distance):

    '''
    getNearbyCustomers

    Get a list of customers located within a certain distance of the intercom office
    and print their user_ids and names, sorted by user_id in asc order.

    Arguments:
        file(string): the path to the file with the customers information
            customer informations are in JSON, with each customer on a different line
            should include the following fields: latitude, longitude, user_id, name

        distance(float): the distance, in kilometers from the office

    Return value:
        None
        But a list of customers is printed to the stdout in asc order by their user_id

    '''

    nearby_customers = []
    intercom = (53.3381985, -6.2592576)

    for line in open(file, 'r'):
        customer = json.loads(line)
        customer_location = (float(customer['latitude']), float(customer['longitude']))
        distance_to_customer = calculateDistance(intercom, customer_location)
        if distance_to_customer <= distance:
            nearby_customers.append({'id': customer['user_id'], 'name': customer['name']})
    
    nearby_customers.sort()

    pprint(nearby_customers)

getNearbyCustomers('customers.txt', 100.0)