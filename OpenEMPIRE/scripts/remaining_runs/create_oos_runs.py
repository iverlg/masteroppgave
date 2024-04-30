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
1	6-4	Copula	10	1	0,4		16	16
2	6-4	Copula	10	1	0,4		17	17
3	6-5	Copula	10	1	0,4		18	18
4	6-5	Copula	10	1	0,4		19	19
5	6-6	Copula	10	1	0,4		20	20
6	6-6	Copula	50	1	0,4		11	11
7	6-7	Copula	50	1	0,4		12	12
8	6-7	Copula	50	1	0,4		13	13
9	6-8	Copula	50	1	0,4		14	14
10	6-8	Copula	50	1	0,4		15	15
11	6-9	Copula	50	1	0,4		16	16
12	6-9	Copula	50	1	0,4		17	17
13	6-10	Copula	50	1	0,4		18	18
14	6-10	Copula	50	1	0,4		19	19
15	6-11	Copula	50	1	0,4		20	20
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
    run_configurations.append({"method": method, "num_scenarios": num_scenarios, "start_instance": start_instance})

# Read the original file content
with open(original_file_path, "r") as f:
    original_content = f.read()

# Iterate over each run configuration
for i, config in enumerate(run_configurations, start=1):
    # Create a copy of the original content
    new_content = original_content

    # Replace the parameters with the values from the current configuration
    new_content = new_content.replace('method = "basic"', f'method = "{config["method"]}"')
    new_content = new_content.replace("num_scenarios = 10", f"num_scenarios = {config['num_scenarios']}")
    new_content = new_content.replace("start_instance = 1", f"start_instance = {config['start_instance']}")

    # Write the modified content to a new file
    output_file_path = os.path.join(output_directory, f"run_oos_{i}.py")
    with open(output_file_path, "w") as f:
        f.write(new_content)

    print(f"Generated script for run {i}: {output_file_path}")
