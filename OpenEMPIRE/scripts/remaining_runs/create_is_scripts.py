# Provided table with run configurations
run_table = """
#run	Node	Metode	Scenarier	Instanser	Tidsbruk (dager)		Instans fra	Instans til
1	4-57	copula-filter5	100	5	0.8		1	5
2	4-58	copula-filter5	100	5	0.8		6	10
3	6-16	copula-filter5	100	5	0.8		11	15
4	6-22	copula-filter5	100	5	0.8		16	20
5	6-23	copula-filter5	100	5	0.8		21	25
6	6-19	copula-filter5	100	5	0.8		26	30
7	6-27	copula-filter25	100	5	0.8		1	5
8	6-28	copula-filter25	100	5	0.8		6	10
9	6-34	copula-filter25	100	5	0.8		11	15
10	6-35	copula-filter25	100	5	0.8		16	20
11	6-40	copula-filter25	100	5	0.8		21	25
12	6-45	copula-filter25	100	5	0.8		26	30
"""

# Generate shell script files for each run
for line in run_table.split('\n')[1:]:
    if line.strip() == '':
        continue
    parts = line.split()
    try:
        run_id = int(parts[0])
        copula_type = parts[2]
    except ValueError:
        continue  # Skip header and other non-integer lines
    node = parts[1]  # Extract node number
    # Create a shell script content for each run
    script_content = f"""\
#!/bin/bash

screen -S run-{copula_type}-{run_id}
ssh compute-{node}

module load Python/3.11.5-GCCcore-13.2.0
module load gurobi
cd ../../storage/users/iogjorva/OpenEMPIRE
python -m scripts.remaining_runs.run_in_sample_{run_id}
"""
    # Write the content to a file
    with open(f"run_script_{run_id}.sh", "w") as f:
        f.write(script_content)

print("Script files generated successfully.")
