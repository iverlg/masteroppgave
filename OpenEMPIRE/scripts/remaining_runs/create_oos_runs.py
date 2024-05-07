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
1	6-23	copula-filter10	10	4	1.7		1	4
2	6-23	copula-filter10	10	4	1.7		5	8
3	6-24	copula-filter10	10	4	1.7		9	12
4	6-24	copula-filter10	10	4	1.7		13	16
5	6-25	copula-filter10	10	4	1.7		17	20
6	6-25	copula-filter10	10	4	1.7		21	24
7	6-26	copula-filter10	10	3	1.3		25	27
8	6-26	copula-filter10	10	3	1.3		28	30
9	6-27	copula-filter10	50	4	1.7		1	4
10	6-27	copula-filter10	50	4	1.7		5	8
11	6-28	copula-filter10	50	4	1.7		9	12
12	6-28	copula-filter10	50	4	1.7		13	16
13	6-29	copula-filter10	50	4	1.7		17	20
14	6-29	copula-filter10	50	4	1.7		21	24
15	6-30	copula-filter10	50	3	1.3		25	27
16	6-30	copula-filter10	50	3	1.3		28	30
17	6-31	copula-filter10	100	4	1.7		1	4
18	6-31	copula-filter10	100	4	1.7		5	8
19	6-32	copula-filter10	100	4	1.7		9	12
20	6-32	copula-filter10	100	4	1.7		13	16
21	6-33	copula-filter10	100	4	1.7		17	20
22	6-33	copula-filter10	100	4	1.7		21	24
23	6-34	copula-filter10	100	3	1.3		25	27
24	6-34	copula-filter10	100	3	1.3		28	30
25	6-35	copula-filter-wind10	100	4	1.7		1	4
26	6-35	copula-filter-wind10	100	4	1.7		5	8
27	6-36	copula-filter-wind10	100	4	1.7		9	12
28	6-36	copula-filter-wind10	100	4	1.7		13	16
29	6-37	copula-filter-wind10	100	4	1.7		17	20
30	6-37	copula-filter-wind10	100	4	1.7		21	24
31	6-38	copula-filter-wind10	100	3	1.3		25	27
32	6-38	copula-filter-wind10	100	3	1.3		28	30
33	6-39	copula-filter-solar10	100	4	1.7		1	4
34	6-39	copula-filter-solar10	100	4	1.7		5	8
35	6-40	copula-filter-solar10	100	4	1.7		9	12
36	6-40	copula-filter-solar10	100	4	1.7		13	16
37	6-41	copula-filter-solar10	100	4	1.7		17	20
38	6-41	copula-filter-solar10	100	4	1.7		21	24
39	6-42	copula-filter-solar10	100	3	1.3		25	27
40	6-42	copula-filter-solar10	100	3	1.3		28	30
41	6-43	copula-filter-combo10	100	4	1.7		1	4
42	6-43	copula-filter-combo10	100	4	1.7		5	8
43	6-44	copula-filter-combo10	100	4	1.7		9	12
44	6-44	copula-filter-combo10	100	4	1.7		13	16
45	6-45	copula-filter-combo10	100	4	1.7		17	20
46	6-45	copula-filter-combo10	100	4	1.7		21	24
47	6-46	copula-filter-combo10	100	3	1.3		25	27
48	6-46	copula-filter-combo10	100	3	1.3		28	30
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
    new_content = new_content.replace('method = "copula-filter10"', f'method = "{config["method"]}"')
    new_content = new_content.replace("num_scenarios = 10", f"num_scenarios = {config['num_scenarios']}")
    new_content = new_content.replace("start_instance = 1", f"start_instance = {config['start_instance']}")
    new_content = new_content.replace("num_instances = 5", f"num_instances = {config['num_instances']}")

    # Write the modified content to a new file
    output_file_path = os.path.join(output_directory, f"run_oos_{i}.py")
    with open(output_file_path, "w") as f:
        f.write(new_content)

    print(f"Generated script for run {i}: {output_file_path}")
