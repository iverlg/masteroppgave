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
python -m scripts.remaining_runs.run_in_sample_{run_id}
"""
    # Write the content to a file
    with open(f"run_script_{run_id}.sh", "w") as f:
        f.write(script_content)

print("Script files generated successfully.")
