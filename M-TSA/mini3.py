import numpy as np

# Define constants
NUM_VEHICLES = 10
NUM_EDGE_NODES = 5
CLOUD_CAPACITY = 100  # Example capacity

# Simulated task attributes for each vehicle
tasks = np.random.randint(10, 50, size=(NUM_VEHICLES, 2))  # [task_size, urgency]

# Simulated edge node capacities
edge_capacities = np.random.randint(20, 50, size=NUM_EDGE_NODES)

# Simulated edge node latencies
edge_latencies = np.random.uniform(1, 5, size=NUM_EDGE_NODES)

def m_tsa_algorithm(task_size, urgency):
    # Define weights for the multi-objective optimization
    weight_latency = 0.7
    weight_capacity = 0.3
    
    scores = []
    for i in range(NUM_EDGE_NODES):
        latency_score = edge_latencies[i]
        capacity_score = edge_capacities[i] - task_size
        
        # Normalize scores
        latency_score = latency_score / max(edge_latencies)
        capacity_score = capacity_score / max(edge_capacities)
        
        # Calculate overall score based on weights
        overall_score = (weight_latency * latency_score) + (weight_capacity * capacity_score)
        scores.append(overall_score)
    
    # Select the edge node with the highest score
    best_edge_node = np.argmax(scores)
    return best_edge_node

def offload_tasks(tasks):
    offloaded_tasks = {}
    for vehicle_id, (task_size, urgency) in enumerate(tasks):
        if task_size <= CLOUD_CAPACITY:
            # Offload to cloud if task size is within capacity
            print(f"Task {vehicle_id} offloaded to cloud")
        else:
            # Use M-TSA algorithm to determine the best edge node
            best_edge_node = m_tsa_algorithm(task_size, urgency)
            offloaded_tasks[vehicle_id] = best_edge_node
            print(f"Task {vehicle_id} offloaded to edge node {best_edge_node}")

    return offloaded_tasks

if __name__ == "__main__":
    offloaded_tasks = offload_tasks(tasks)
    print("Offloading results:", offloaded_tasks)
