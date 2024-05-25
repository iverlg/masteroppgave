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

screen -S oos-run{run_id}
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
