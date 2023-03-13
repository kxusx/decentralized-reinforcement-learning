#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

def reroute_vehicle(vehicle_id):
    # Get the current route of the vehicle
    current_route = traci.vehicle.getRoute(vehicle_id)
    
    # Get the current position of the vehicle on the route
    current_edge = traci.vehicle.getRoadID(vehicle_id)
    current_position = traci.vehicle.getLanePosition(vehicle_id)
    current_route_index = current_route.index(current_edge)
    
    # Calculate the travel time for each possible new route
    possible_routes = traci.simulation.findRoute(current_edge, random.choice(traci.simulation.getNetwork().getEdges()),)
    travel_times = []
    for route in possible_routes:
        travel_time = traci.simulation.getTravelTime(route.edges)
        travel_times.append(travel_time)
    
    # Find the best new route based on travel time
    best_route_index = travel_times.index(min(travel_times))
    best_route = possible_routes[best_route_index].edges
    
    # Reroute the vehicle to the best new route
    traci.vehicle.rerouteTraveltime(vehicle_id, best_route)
    traci.vehicle.moveTo(vehicle_id, best_route[0], current_position)


# contains TraCI control loop
def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
        # Reroute a random vehicle at each intersection every 30 seconds
        if traci.simulation.getTime() % 30 == 0:
            reroute_vehicle(0)

    traci.close()
    sys.stdout.flush()
                
if __name__ == '__main__':
    options = get_options()
    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "demo.sumo.cfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()