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
1	6-1	copula-filter	10	5	0,4		1	5
2	6-1	copula-filter	10	5	0,4		6	10
3	6-2	copula-filter	10	5	0,4		11	15
4	6-2	copula-filter	10	5	0,4		16	20
5	6-4	copula-filter	10	5	0,4		21	25
6	6-4	copula-filter	10	5	0,4		26	30
7	6-5	copula-filter	50	4	0,5		1	4
8	6-5	copula-filter	50	4	0,5		5	8
9	6-6	copula-filter	50	4	0,5		9	12
10	6-6	copula-filter	50	4	0,5		13	16
11	6-7	copula-filter	50	4	0,5		17	20
12	6-7	copula-filter	50	4	0,5		21	24
13	6-8	copula-filter	50	4	0,5		25	28
14	6-8	copula-filter	50	2	0,3		29	30
15	6-9	copula-filter	100	2	0,4		1	2
16	6-10	copula-filter	100	2	0,4		3	4
17	6-11	copula-filter	100	2	0,4		5	6
18	6-13	copula-filter	100	2	0,4		7	8
19	6-14	copula-filter	100	2	0,4		9	10
20	6-15	copula-filter	100	2	0,4		11	12
21	6-16	copula-filter	100	2	0,4		13	14
22	6-17	copula-filter	100	2	0,4		15	16
23	6-18	copula-filter	100	2	0,4		17	18
24	6-19	copula-filter	100	2	0,4		19	20
25	6-20	copula-filter	100	2	0,4		21	22
26	6-21	copula-filter	100	2	0,4		23	24
27	6-22	copula-filter	100	2	0,4		25	26
28	6-24	copula-filter	100	2	0,4		27	28
28	6-25	copula-filter	100	2	0,4		29	30
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
    run_configurations.append({"method": method, "num_scenarios": num_scenarios, "start_instance": start_instance, "num_instances": num_instances})

# Read the original file content
with open(original_file_path, "r") as f:
    original_content = f.read()

# Iterate over each run configuration
for i, config in enumerate(run_configurations, start=1):
    # Create a copy of the original content
    new_content = original_content

    # Replace the parameters with the values from the current configuration
    new_content = new_content.replace('routine = "copula-filter"', f'routine = "{config["method"]}"')
    new_content = new_content.replace("num_scenarios = 10", f"num_scenarios = {config['num_scenarios']}")
    new_content = new_content.replace("num_instances = 10", f"num_instances = {config['num_instances']}")
    new_content = new_content.replace("start_instance = 1", f"start_instance = {config['start_instance']}")

    # Write the modified content to a new file
    output_file_path = os.path.join(output_directory, f"run_in_sample_{i}.py")
    with open(output_file_path, "w") as f:
        f.write(new_content)

    print(f"Generated script for run {i}: {output_file_path}")
