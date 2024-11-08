import numpy as np
import matplotlib.pyplot as plt

# Define the number of tasks and resources
num_tasks = 10
num_cloud_resources = 2
num_edge_resources = 3
num_end_devices = 5

# Generate random tasks with computation and data requirements
def generate_tasks(num_tasks):
    tasks = []
    for i in range(num_tasks):
        computation = np.random.randint(1, 100)  # Task computation requirement
        data = np.random.randint(1, 50)         # Task data requirement
        tasks.append((computation, data))
    return tasks

# Generate random resources with computation and bandwidth capabilities
def generate_resources(num_cloud, num_edge, num_end):
    resources = {
        'cloud': [(np.random.randint(100, 200), np.random.randint(10, 30)) for _ in range(num_cloud)],
        'edge': [(np.random.randint(50, 100), np.random.randint(20, 50)) for _ in range(num_edge)],
        'end': [(np.random.randint(10, 50), np.random.randint(30, 60)) for _ in range(num_end)]
    }
    return resources

# Simple M-TSA Algorithm for task offloading
def m_tsa_algorithm(tasks, resources):
    cloud_resources = resources['cloud']
    edge_resources = resources['edge']
    end_resources = resources['end']
    
    task_assignments = {
        'cloud': [],
        'edge': [],
        'end': []
    }
    
    for task in tasks:
        comp_req, data_req = task
        best_resource = None
        best_resource_type = None
        min_time = float('inf')
        
        # Evaluate Cloud Resources
        for i, (comp_cap, bandwidth) in enumerate(cloud_resources):
            if comp_req <= comp_cap and data_req <= bandwidth:
                time = comp_req / comp_cap  # Simplified time calculation
                if time < min_time:
                    min_time = time
                    best_resource = i
                    best_resource_type = 'cloud'
        
        # Evaluate Edge Resources
        for i, (comp_cap, bandwidth) in enumerate(edge_resources):
            if comp_req <= comp_cap and data_req <= bandwidth:
                time = comp_req / comp_cap
                if time < min_time:
                    min_time = time
                    best_resource = i
                    best_resource_type = 'edge'
        
        # Evaluate End Resources
        for i, (comp_cap, bandwidth) in enumerate(end_resources):
            if comp_req <= comp_cap and data_req <= bandwidth:
                time = comp_req / comp_cap
                if time < min_time:
                    min_time = time
                    best_resource = i
                    best_resource_type = 'end'
        
        if best_resource_type:
            task_assignments[best_resource_type].append(min_time)
    
    return task_assignments

# Generate tasks and resources
tasks = generate_tasks(num_tasks)
resources = generate_resources(num_cloud_resources, num_edge_resources, num_end_devices)

# Perform task offloading using M-TSA
assignments = m_tsa_algorithm(tasks, resources)

# Calculate average task completion time for each type of resource
def calculate_average_completion_time(assignments):
    avg_times = {
        'cloud': np.mean(assignments['cloud']) if assignments['cloud'] else 0,
        'edge': np.mean(assignments['edge']) if assignments['edge'] else 0,
        'end': np.mean(assignments['end']) if assignments['end'] else 0
    }
    return avg_times

avg_times = calculate_average_completion_time(assignments)

# Plotting the results
def plot_results(avg_times):
    resource_types = list(avg_times.keys())
    avg_completion_times = list(avg_times.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(resource_types, avg_completion_times, color=['skyblue', 'lightgreen', 'salmon'])
    plt.xlabel('Resource Type')
    plt.ylabel('Average Task Completion Time')
    plt.title('Average Task Completion Time for Each Resource Type')
    plt.grid(axis='y')
    
    # Save the plot to a file
    plt.savefig('task_completion_times.png')
    plt.show()

# Display and plot results
plot_results(avg_times)
