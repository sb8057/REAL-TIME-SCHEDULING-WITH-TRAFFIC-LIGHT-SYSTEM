#include <stdio.h>
#include <stdlib.h>

// Structure to represent a traffic signal
typedef struct {
    int id;          // Signal ID
    int duration;    // Duration for which the signal stays green
} TrafficSignal;

// Structure to represent a lane
typedef struct {
    int id;            // Lane ID
    int signalId;      // Signal controlling the lane
    int vehicles;      // Number of vehicles in the lane
} Lane;

// Structure to represent a vehicle
typedef struct {
    int id;            // Vehicle ID
    int laneId;        // Lane the vehicle is in
} Vehicle;

// Function to initialize a lane
Lane initLane(int id, int signalId) {
    Lane lane;
    lane.id = id;
    lane.signalId = signalId;
    lane.vehicles = 0;
    return lane;
}

// Function to initialize a vehicle
Vehicle initVehicle(int id, int laneId) {
    Vehicle vehicle;
    vehicle.id = id;
    vehicle.laneId = laneId;
    return vehicle;
}

// Function to implement round-robin scheduling
void roundRobin(TrafficSignal signals[], int numSignals, Lane lanes[], int numLanes, int totalTime) {
    int i, j, k;
    for (i = 0; i < totalTime; i++) {
        // Update signals and lanes
        for (j = 0; j < numSignals; j++) {
            signals[j].duration--;
            if (signals[j].duration == 0) {
                // Change signal to the next one in round-robin
                signals[j].duration = lanes[j].vehicles * 2;  // Adjust duration based on the number of vehicles
                lanes[j].signalId = (lanes[j].signalId + 1) % numSignals;
            }
        }

        // Simulate vehicles entering the system
        for (k = 0; k < numLanes; k++) {
            if (rand() % 2 == 0) {  // 50% chance of a vehicle entering the lane
                lanes[k].vehicles++;
                printf("Vehicle %d entered Lane %d\n", lanes[k].vehicles, lanes[k].id);
            }
        }

        // Simulate vehicles leaving the system
        for (k = 0; k < numLanes; k++) {
            if (lanes[k].vehicles > 0 && lanes[k].signalId == k) {
                lanes[k].vehicles--;
                printf("Vehicle leaving Lane %d\n", lanes[k].id);
            }
        }
    }
}

int main() {
    // Example signals
    TrafficSignal signals[] = {
        {1, 10},
        {2, 8},
        {3, 12},
    };

    int numSignals = sizeof(signals) / sizeof(signals[0]);

    // Example lanes
    Lane lanes[] = {
        initLane(1, 0),
        initLane(2, 1),
        initLane(3, 2),
    };

    int numLanes = sizeof(lanes) / sizeof(lanes[0]);
    int totalTime = 30; // Total simulation time in seconds

    // Run the round-robin scheduling
    roundRobin(signals, numSignals, lanes, numLanes, totalTime);

    return 0;
}
