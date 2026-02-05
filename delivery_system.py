import json
from collections import defaultdict

with open("data.json", "r") as file:
    data = json.load(file)


# Extract data

warehouses = data['warehouses']
agents = data['agents']
packages = data['packages']
# Function to calculate Euclidean distance

def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5
# Assign packages to the nearest agent based on distance from agent to warehouse

agent_packages = defaultdict(list)
for package in packages:
    w = package['warehouse']
    w_pos = warehouses[w]

    min_dist = float('inf')
    assigned_agent = None

    for agent, agent_pos in agents.items():
        d = distance(agent_pos, w_pos)
        if d < min_dist:
            min_dist = d
            assigned_agent = agent

    agent_packages[assigned_agent].append(package)

 # Simulate delivery and calculate total distance and efficiency
report = {}
min_efficiency = float('inf')
best_agent = None
for agent, packs in agent_packages.items():
    total_distance = 0

    for p in packs:
        w_pos = warehouses[p['warehouse']]
        a_pos = agents[agent]
        dest = p['destination']

        total_distance += distance(a_pos, w_pos) + distance(w_pos, dest)

    packages_delivered = len(packs)
    efficiency = total_distance / packages_delivered if packages_delivered > 0 else 0
    report[agent] = {
        "packages_delivered": packages_delivered,
        "total_distance": round(total_distance, 2),
        "efficiency": round(efficiency, 2)
    }

    if efficiency < min_efficiency:
        min_efficiency = efficiency
        best_agent = agent
report["best_agent"] = best_agent

# Save the report to report.json
with open('report.json', 'w') as f:
    json.dump(report, f, indent=4)
#Print the report for verification
print(json.dumps(report, indent=4))
