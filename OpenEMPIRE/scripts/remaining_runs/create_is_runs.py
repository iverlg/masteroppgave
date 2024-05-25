import os

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Path to the original file
original_file_name = "run_in_sample_1.py"
original_file_path = os.path.join(current_directory, original_file_name)

# Directory to store the modified files
output_directory = current_directory

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Read the original file content
with open(original_file_path, "r") as f:
    original_content = f.read()

# Provided table with run configurations
run_table = """
#run	Node	Metode	Scenarier	Instanser	Tidsbruk (dager)		Instans fra	Instans til
1	4-57	copula-filter5	100	5	0.8		1	5
2	4-58	copula-filter5	100	5	0.8		6	10
3	6-16	copula-filter5	100	5	0.8		11	15
4	6-18	copula-filter5	100	5	0.8		16	20
5	6-25	copula-filter5	100	5	0.8		21	25
6	6-26	copula-filter5	100	5	0.8		26	30
7	6-27	copula-filter25	100	5	0.8		1	5
8	6-28	copula-filter25	100	5	0.8		6	10
9	6-34	copula-filter25	100	5	0.8		11	15
10	6-35	copula-filter25	100	5	0.8		16	20
11	6-40	copula-filter25	100	5	0.8		21	25
12	6-45	copula-filter25	100	5	0.8		26	30
"""

# Split the table into rows
rows = run_table.strip().split("\n")

# Extract run configurations from each row
run_configurations = []
for row in rows[1:]:  # Skip the header row
    columns = row.split()
    method = columns[2]
    n_clusters = method[-2:] if len(method) == 15 else method[-1:]
    num_scenarios = int(columns[3])
    start_instance = int(columns[6])
    end_instance = int(columns[7])
    num_instances = end_instance - start_instance + 1
    run_configurations.append({"method": method, "num_scenarios": num_scenarios, "start_instance": start_instance, "num_instances": num_instances, "n_clusters": n_clusters})

# Read the original file content
with open(original_file_path, "r") as f:
    original_content = f.read()

# Iterate over each run configuration
for i, config in enumerate(run_configurations, start=1):
    # Create a copy of the original content
    new_content = original_content

    # Replace the parameters with the values from the current configuration
    new_content = new_content.replace('routine = "copula-filter5"', f'routine = "{config["method"]}"')
    new_content = new_content.replace("num_scenarios = 100", f"num_scenarios = {config['num_scenarios']}")
    new_content = new_content.replace("num_instances = 5", f"num_instances = {config['num_instances']}")
    new_content = new_content.replace("start_instance = 1", f"start_instance = {config['start_instance']}")
    new_content = new_content.replace("empire_config.n_cluster = 5", f"empire_config.n_cluster = {config['n_clusters']}")
    new_content = new_content.replace('elif routine == "copula-filter":', f"elif routine == 'copula-filter{config['n_clusters']}':")


    # Write the modified content to a new file
    output_file_path = os.path.join(output_directory, f"run_in_sample_{i}.py")
    with open(output_file_path, "w") as f:
        f.write(new_content)

    print(f"Generated script for run {i}: {output_file_path}")
