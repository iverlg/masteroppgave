import os

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Path to the original file
original_file_name = "run_oos_1.py"
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
1	6-25	copula-filter5	100	3	1.3		1	3
2	6-25	copula-filter5	100	3	1.3		4	6
3	6-14	copula-filter5	100	3	1.3		7	9
4	6-14	copula-filter5	100	3	1.3		10	12
5	6-15	copula-filter5	100	3	1.3		13	15
6	6-15	copula-filter5	100	3	1.3		16	18
7	6-16	copula-filter5	100	3	1.3		19	21
8	6-16	copula-filter5	100	3	1.3		22	24
9	6-19	copula-filter5	100	3	1.3		25	27
10	6-19	copula-filter5	100	3	1.3		28	30
11	6-20	copula-filter25	100	3	1.3		1	3
12	6-20	copula-filter25	100	3	1.3		4	6
13	6-21	copula-filter25	100	3	1.3		7	9
14	6-21	copula-filter25	100	3	1.3		10	12
15	6-22	copula-filter25	100	3	1.3		13	15
16	6-22	copula-filter25	100	3	1.3		16	18
17	6-23	copula-filter25	100	3	1.3		19	21
18	6-23	copula-filter25	100	3	1.3		22	24
19	6-24	copula-filter25	100	3	1.3		25	27
20	6-24	copula-filter25	100	3	1.3		28	30
"""

# Split the table into rows
rows = run_table.strip().split("\n")

# Extract run configurations from each row
run_configurations = []
for row in rows[1:]:  # Skip the header row
    columns = row.split()
    method = columns[2]
    num_scenarios = int(columns[3])
    start_instance = int(columns[6])
    end_instance = int(columns[7])
    num_instances = end_instance - start_instance + 1
    n_clusters = method[-2:] if len(method) == 15 else method[-1:]
    run_configurations.append({"method": method, "num_scenarios": num_scenarios, "start_instance": start_instance, "num_instances": num_instances, "n_clusters": n_clusters})

# Read the original file content
with open(original_file_path, "r") as f:
    original_content = f.read()

# Iterate over each run configuration
for i, config in enumerate(run_configurations, start=1):
    # Create a copy of the original content
    new_content = original_content

    # Replace the parameters with the values from the current configuration
    new_content = new_content.replace('method = "copula-filter5"', f'method = "{config["method"]}"')
    new_content = new_content.replace("num_scenarios = 100", f"num_scenarios = {config['num_scenarios']}")
    new_content = new_content.replace("start_instance = 1", f"start_instance = {config['start_instance']}")
    new_content = new_content.replace("num_instances = 3", f"num_instances = {config['num_instances']}")
    new_content = new_content.replace("empire_config.n_cluster = 25", f"empire_config.n_cluster = {config['n_clusters']}")


    # Write the modified content to a new file
    output_file_path = os.path.join(output_directory, f"run_oos_{i}.py")
    with open(output_file_path, "w") as f:
        f.write(new_content)

    print(f"Generated script for run {i}: {output_file_path}")
