# Provided table with run configurations
run_table = """
#run	Node	Metode	Scenarier	Instanser	Tidsbruk (dager)		Instans fra	Instans til
1	6-13	copula-filter-wind	100	10	1,7		1	10
2	6-14	copula-filter-wind	100	10	1,7		11	20
3	6-15	copula-filter-wind	100	10	1,7		21	30
4	6-16	copula-filter-solar	100	10	1,7		1	10
5	6-17	copula-filter-solar	100	10	1,7		11	20
6	6-18	copula-filter-solar	100	10	1,7		21	30
7	6-19	copula-filter-combo	100	10	1,7		1	10
8	6-20	copula-filter-combo	100	10	1,7		11	20
9	6-22	copula-filter-combo	100	10	1,7		21	30
"""

# Generate shell script files for each run
for line in run_table.split('\n')[1:]:
    if line.strip() == '':
        continue
    parts = line.split()
    try:
        run_id = int(parts[0])
        copula_type = parts[2].split("-")[2]
    except ValueError:
        continue  # Skip header and other non-integer lines
    node = parts[1]  # Extract node number
    # Create a shell script content for each run
    script_content = f"""\
#!/bin/bash

screen -S run-{copula_type}{run_id}
ssh compute-{node}

module load Python/3.11.5-GCCcore-13.2.0
module load gurobi
cd ../../storage/users/iogjorva/OpenEMPIRE
python -m scripts.remaining_runs.run_is_{copula_type}_{run_id}
"""
    # Write the content to a file
    with open(f"run_script_{run_id}.sh", "w") as f:
        f.write(script_content)

print("Script files generated successfully.")
