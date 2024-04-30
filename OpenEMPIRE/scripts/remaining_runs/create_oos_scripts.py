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

# Generate shell script files for each run
for line in run_table.split('\n')[1:]:
    if line.strip() == '':
        continue
    parts = line.split()
    try:
        run_id = int(parts[0])
    except ValueError:
        continue  # Skip header and other non-integer lines
    node = parts[1]  # Extract node number
    # Create a shell script content for each run
    script_content = f"""\
#!/bin/bash

screen -S new-run{run_id}
ssh compute-{node}

module load Python/3.11.5-GCCcore-13.2.0
module load gurobi
cd ../../storage/users/iogjorva/OpenEMPIRE
python -m scripts.remaining_runs.run_oos_{run_id}
"""
    # Write the content to a file
    with open(f"run_script_{run_id}.sh", "w") as f:
        f.write(script_content)

print("Script files generated successfully.")
