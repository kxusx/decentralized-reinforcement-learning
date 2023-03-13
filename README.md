1) For creating demo.trips.xml file : python3 /usr/local/opt/sumo/share/sumo/tools/randomTrips.py -n demo.net.xml -e 50000 -o demo.trips.xml

2) For Creating the rou.xml file :duarouter -n demo.net.xml --route-files demo.trips.xml -o demo.rou.xml --ignore-errors