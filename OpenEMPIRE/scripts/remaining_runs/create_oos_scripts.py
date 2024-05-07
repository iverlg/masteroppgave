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
