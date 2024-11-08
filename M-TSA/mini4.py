import numpy as np
import matplotlib.pyplot as plt

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
    offloaded_tasks = {i: None for i in range(NUM_VEHICLES)}
    edge_usage = np.zeros(NUM_EDGE_NODES)
    
    for vehicle_id, (task_size, urgency) in enumerate(tasks):
        if task_size <= CLOUD_CAPACITY:
            # Offload to cloud if task size is within capacity
            offloaded_tasks[vehicle_id] = 'Cloud'
        else:
            # Use M-TSA algorithm to determine the best edge node
            best_edge_node = m_tsa_algorithm(task_size, urgency)
            offloaded_tasks[vehicle_id] = best_edge_node
            edge_usage[best_edge_node] += task_size

    return offloaded_tasks, edge_usage

def plot_results(offloaded_tasks, edge_usage):
    # Plot task offloading results
    plt.figure(figsize=(12, 6))

    # Plot edge node usage
    plt.subplot(1, 2, 1)
    plt.bar(range(NUM_EDGE_NODES), edge_usage, color='b', alpha=0.7)
    plt.xlabel('Edge Node ID')
    plt.ylabel('Total Task Size Offloaded')
    plt.title('Edge Node Usage')

    # Plot task allocation
    plt.subplot(1, 2, 2)
    vehicles = list(offloaded_tasks.keys())
    allocations = [offloaded_tasks[v] for v in vehicles]
    plt.scatter(vehicles, [1] * len(vehicles), c=[allocations[v] if isinstance(allocations[v], int) else -1 for v in vehicles], cmap='viridis', s=100)
    plt.yticks([])
    plt.xlabel('Vehicle ID')
    plt.title('Task Allocation')
    plt.colorbar(label='Edge Node ID or Cloud')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    offloaded_tasks, edge_usage = offload_tasks(tasks)
    plot_results(offloaded_tasks, edge_usage)
