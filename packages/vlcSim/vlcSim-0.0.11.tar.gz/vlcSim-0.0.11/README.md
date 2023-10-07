VLCSim is an Event-Oriented simulator package for Visible Light Communication.

# Features

- Dynamic Environment with in/out connections 
- Flexible resource allocation algorithm 
- Flexible VLC/room parameters

# Events

The simulator has 5 Type of events:

* **ARRIVE**: Every time when a connection arrives to the system
* **RESUME**: When a connection begin the transmission
* **PAUSE**: When a Connection PAUSES the transmission
* **DEPARTURE**: When a connectin ends its transmission
* **RETRYING**: WHen a connection is not allocated, and uses a WAIT status, it makes a new attepmt to connect.

# Code example

Next example could be used to start coding with the package:

```python
from vlcsim import *


def alloc(receiver, connection, scenario: Scenario, controller: Controller):
    vleds = scenario.vleds
    snrFromVleds = []
    for vled in vleds:
        snrFromVleds.append(scenario.snrVled(receiver, vled))
    posBestSNR = snrFromVleds.index(max(snrFromVleds))
    if controller.numberOfActiveConnections(posBestSNR) > 2:
        return Controller.status.WAIT, connection
    else:
        connection.AP = vleds[posBestSNR]
    return Controller.status.ALLOCATED, connection


if __name__ == "__main__":
    # Simulator Constructor: size of the room, with the numbrer of grids and the rho parameter

    sim = Simulator(5.0, 5.0, 2.15, 10, 0.8)

    # Adding Vleds to the room
    vled = VLed(-1.25, -1.25, 2.15, 60, 60, 20, 70)
    vled.sliceTime = 2
    sim.scenario.addVLed(vled)
    vled = VLed(-1.25, 1.25, 2.15, 60, 60, 20, 70)
    vled.sliceTime = 2
    sim.scenario.addVLed(vled)
    vled = VLed(1.25, -1.25, 2.15, 60, 60, 20, 70)
    vled.sliceTime = 2
    sim.scenario.addVLed(vled)
    vled = VLed(1.25, 1.25, 2.15, 60, 60, 20, 70)
    vled.sliceTime = 2
    sim.scenario.addVLed(vled)

    # Adding rf
    rf = RF(0, 0, 0.85)
    rf.sliceTime = 2
    sim.scenario.addRF(rf)

    # setting algorithm and number of connections
    sim.set_allocation_algorithm(alloc)
    sim.goalConnections = 100

    # changing Dynamic
    sim.lambdaS = 1
    sim.mu = 10

    # changing random wait limits
    sim.upper_random_wait = 20
    sim.lower_random_wait = 2

    # initialize and run
    sim.init()
    sim.run()


```


