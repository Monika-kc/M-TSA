import numpy as np
import matplotlib.pyplot as plt

# Define constants
NUM_VEHICLES = 10
NUM_EDGE_NODES = 5
NUM_TASKS = 20
TIME_SLOTS = 10

# Define M-TSA algorithm
def m_tsa_algorithm(task_size, urgency, edge_capacities, edge_latencies, epsilon=1.125):
    """Apply M-TSA algorithm for task offloading."""
    scores = []
    for i in range(NUM_EDGE_NODES):
        latency_score = edge_latencies[i]
        capacity_score = edge_capacities[i] - task_size
        
        # Normalize scores
        latency_score = latency_score / max(edge_latencies)
        capacity_score = capacity_score / max(edge_capacities)
        
        # Calculate overall score based on epsilon
        overall_score = (epsilon * capacity_score) - latency_score
        scores.append(overall_score)
    
    # Select the edge node with the highest score
    best_edge_node = np.argmax(scores)
    return best_edge_node

# Simulate other algorithms (placeholders)
def simulated_annealing(task_size, edge_capacities, edge_latencies):
    return np.random.randint(0, NUM_EDGE_NODES)

def random_migration(task_size, edge_capacities, edge_latencies):
    return np.random.randint(0, NUM_EDGE_NODES)

def snms_migration(task_size, edge_capacities, edge_latencies):
    return np.random.randint(0, NUM_EDGE_NODES)

def simulate_algorithm(algorithm, num_vehicles, num_tasks):
    """Simulate performance of different algorithms."""
    load_balances = []
    delays = []
    energy_consumptions = []

    for _ in range(TIME_SLOTS):
        # Randomly initialize task sizes and edge node attributes
        task_sizes = np.random.randint(10, 50, size=num_tasks)
        urgencies = np.random.uniform(0, 1, size=num_tasks)
        edge_capacities = np.random.randint(50, 100, size=NUM_EDGE_NODES)
        edge_latencies = np.random.uniform(1, 5, size=NUM_EDGE_NODES)
        
        offloading_results = []
        for size, urgency in zip(task_sizes, urgencies):
            if algorithm == 'M-TSA':
                edge_node = m_tsa_algorithm(size, urgency, edge_capacities, edge_latencies)
            elif algorithm == 'SA':
                edge_node = simulated_annealing(size, edge_capacities, edge_latencies)
            elif algorithm == 'Random':
                edge_node = random_migration(size, edge_capacities, edge_latencies)
            elif algorithm == 'SNMS':
                edge_node = snms_migration(size, edge_capacities, edge_latencies)
            offloading_results.append(edge_node)
        
        # Compute metrics
        load_balance = np.mean([edge_capacities[edge] - size for edge, size in zip(offloading_results, task_sizes)])
        average_delay = np.mean([edge_latencies[edge] for edge in offloading_results])
        energy_consumption = np.mean([np.random.uniform(5, 15) for _ in range(num_tasks)])  # Example energy consumption
        
        load_balances.append(load_balance)
        delays.append(average_delay)
        energy_consumptions.append(energy_consumption)
    
    return np.mean(load_balances), np.mean(delays), np.mean(energy_consumptions)

def plot_results(results):
    """Plot performance comparison results."""
    algorithms, load_balances, delays, energy_consumptions = zip(*results)

    plt.figure(figsize=(18, 6))

    # Plot load balance comparison
    plt.subplot(1, 3, 1)
    plt.bar(algorithms, load_balances, color='b', alpha=0.7)
    plt.xlabel('Algorithm')
    plt.ylabel('Average Load Balance')
    plt.title('Load Balance Comparison')

    # Plot average delay comparison
    plt.subplot(1, 3, 2)
    plt.bar(algorithms, delays, color='r', alpha=0.7)
    plt.xlabel('Algorithm')
    plt.ylabel('Average Delay')
    plt.title('Average Delay Comparison')

    # Plot energy consumption comparison
    plt.subplot(1, 3, 3)
    plt.bar(algorithms, energy_consumptions, color='g', alpha=0.7)
    plt.xlabel('Algorithm')
    plt.ylabel('Average Energy Consumption')
    plt.title('Energy Consumption Comparison')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    algorithms = ['M-TSA', 'SA', 'Random', 'SNMS']
    results = []

    for algo in algorithms:
        load_balance, delay, energy_consumption = simulate_algorithm(algo, NUM_VEHICLES, NUM_TASKS)
        results.append((algo, load_balance, delay, energy_consumption))

    plot_results(results)
    
    # Performance comparison
    m_tsa_load_balance, m_tsa_delay, m_tsa_energy = [result[1:] for result in results if result[0] == 'M-TSA'][0]
    sa_load_balance, sa_delay, sa_energy = [result[1:] for result in results if result[0] == 'SA'][0]
    random_load_balance, random_delay, random_energy = [result[1:] for result in results if result[0] == 'Random'][0]
    snms_load_balance, snms_delay, snms_energy = [result[1:] for result in results if result[0] == 'SNMS'][0]

    # Calculate performance improvements
    tcm_vs_sa_load = (sa_load_balance - m_tsa_load_balance) / sa_load_balance * 100
    tcm_vs_random_load = (random_load_balance - m_tsa_load_balance) / random_load_balance * 100
    tcm_vs_snms_load = (snms_load_balance - m_tsa_load_balance) / snms_load_balance * 100

    tcm_vs_sa_delay = (m_tsa_delay - sa_delay) / sa_delay * 100
    tcm_vs_random_delay = (m_tsa_delay - random_delay) / random_delay * 100
    tcm_vs_snms_delay = (m_tsa_delay - snms_delay) / snms_delay * 100

    tcm_vs_sa_energy = (m_tsa_energy - sa_energy) / sa_energy * 100
    tcm_vs_random_energy = (m_tsa_energy - random_energy) / random_energy * 100
    tcm_vs_snms_energy = (m_tsa_energy - snms_energy) / snms_energy * 100

    print(f"TCM vs SA - Load Balance Improvement: {tcm_vs_sa_load:.2f}%")
    print(f"TCM vs Random - Load Balance Improvement: {tcm_vs_random_load:.2f}%")
    print(f"TCM vs SNMS - Load Balance Improvement: {tcm_vs_snms_load:.2f}%")
    print(f"TCM vs SA - Latency Reduction: {tcm_vs_sa_delay:.2f}%")
    print(f"TCM vs Random - Latency Reduction: {tcm_vs_random_delay:.2f}%")
    print(f"TCM vs SNMS - Latency Increase: {tcm_vs_snms_delay:.2f}%")
    print(f"TCM vs SA - Energy Consumption Reduction: {tcm_vs_sa_energy:.2f}%")
    print(f"TCM vs Random - Energy Consumption Reduction: {tcm_vs_random_energy:.2f}%")
    print(f"TCM vs SNMS - Energy Consumption Reduction: {tcm_vs_snms_energy:.2f}%")
