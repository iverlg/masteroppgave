from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
from empire.core.config import (EmpireConfiguration, EmpireRunConfiguration,
                                read_config_file)
from empire.core.model_runner import run_empire_model, setup_run_paths
from empire.logger import get_empire_logger
from empire.utils import get_name_of_last_folder_in_path

parser = ArgumentParser(description="A CLI script to run the Empire model.")

parser.add_argument(
    "-d",
    "--dataset",
    help="Specify the required dataset",
    default="europe_agg_v50",
)

parser.add_argument(
    "-rdir",
    "--results-directory",
    help="Specify the results directory for in sample runs",
    default="run_in_sample_new",
)

# SGR: 'basic', 'filter', 'moment', 'copula'
parser.add_argument("-r", "--routine", help="Scenario generation routine ('basic', 'filter', 'moment', 'copula')", required=True)

parser.add_argument("-f", "--force", help="Force new run if old exist.", action="store_true")
parser.add_argument("-c", "--config-file", help="Path to config file.", default="config/aggrun.yaml")

# How many instances to solve to obtain mean and SD
parser.add_argument("-ni", "--num-instances", help="Number of instances", type=int, default=30)

args = parser.parse_args()
dataset=args.dataset
results_dir = args.results_directory
routine = args.routine

## Read config and setup folders ##
config = read_config_file(Path(args.config_file))
empire_config = EmpireConfiguration.from_dict(config=config)

num_instances = args.num_instances
tree_sizes = [1]

for ts in tree_sizes:
    num_scenarios = ts

    # For SGR routines add extra detail to output-folder / name
    routine_detail = ""
    if routine == "moment":
        routine_detail = f"moment{empire_config.n_tree_compare}"
    elif routine == "filter":
        routine_detail = f"filter{empire_config.n_cluster}"
    elif routine == "copula":
        routine_detail = f"copula{empire_config.n_tree_compare}"
    else:
        routine_detail = "basic"

    # Modifications to config
    empire_config.use_scenario_generation = True
    empire_config.use_fixed_sample = False
    empire_config.filter_make = False
    empire_config.number_of_scenarios = num_scenarios

    if routine == "filter":
        empire_config.moment_matching = False
        empire_config.filter_use = True
        empire_config.copula_use = False
    elif routine == "moment":
        empire_config.moment_matching = True
        empire_config.filter_use = False
        empire_config.copula_use = False
    elif routine == "copula":
        empire_config.moment_matching = False
        empire_config.filter_use = False
        empire_config.copula_use = True
    else: 
        empire_config.moment_matching = False
        empire_config.filter_use = False
        empire_config.copula_use = False
        
    # Run script
    for i in range(1, num_instances + 1):
         if i==1 and (routine == "filter" or routine == "copula"):
            empire_config.copula_make = True
            empire_config.filter_make = True
        else:
            empire_config.copula_make = False
            empire_config.filter_make = False
        run_path = Path.cwd() / "Results/run_in_sample_new/dataset_{ds}/{r}_sce{ns}_{i}".format(
            ds=dataset,
            r=routine_detail,
            ns=num_scenarios,
            i=i
        )

        if (run_path / "Output/results_objective.csv").exists() and not args.force:
            raise ValueError("There already exists results for this analysis run.")

        run_config = setup_run_paths(version=dataset, empire_config=empire_config, run_path=run_path)
        logger = get_empire_logger(run_config=run_config)
        logger.info("Running EMPIRE Model")

        ## Run empire model
        run_empire_model(
            empire_config=empire_config, run_config=run_config, data_managers=[], test_run=False
        )

# Modifications to config
empire_config.use_scenario_generation = False
empire_config.use_fixed_sample = True
empire_config.number_of_scenarios = 100

# Get all runs
empire_path = Path.cwd()
results_path = empire_path / f"Results/{results_dir}/dataset_{dataset}"
all_run_paths = sorted([d for d in results_path.iterdir() if d.is_dir()])

out_of_sample_path = empire_path / f"OutOfSample/dataset_{dataset}/new"
out_of_sample_tree_paths = sorted([t for t in out_of_sample_path.iterdir() if t.is_dir()])

if len(all_run_paths) == 0:
    raise ValueError("Results directory is empty, try specifying another directory")

if len(out_of_sample_tree_paths) == 0:
    raise ValueError("Out of sample runs for directory is empty, generate using the script 'create_out_of_sample_trees.py'")

for run_path in all_run_paths:
    # Part of run config setup
    dataset_path = run_path / "Input" / "Xlsx"
    results_file_path = run_path / "Output"

    # Workaround to avoid manual copying scenario files
    tab_path = scenario_data_path = run_path / "Input" / "Tab"

    # Save objective values in dataframe 
    df_out_of_sample = pd.DataFrame({"Sample tree": [], "Objective value": []})

    for tree_path in out_of_sample_tree_paths:
        sample_file_path = tree_path
        sample_tree = get_name_of_last_folder_in_path(tree_path)

        # Set up run config manually to avoid duplicate input files and easier output struct
        run_name = get_name_of_last_folder_in_path(run_path) + f"_out-of-sample_{sample_tree}"
        run_config = EmpireRunConfiguration(
                        run_name=run_name,
                        dataset_path=dataset_path,
                        tab_path=tab_path,
                        scenario_data_path=scenario_data_path,
                        results_path=results_file_path,
                        empire_path=empire_path
                    )

        logger = get_empire_logger(run_config=run_config)
        logger.info("Running EMPIRE Model")

        ## Run empire model
        obj_value = run_empire_model(
            empire_config=empire_config,
            run_config=run_config,
            data_managers=[],
            test_run=False,
            OUT_OF_SAMPLE=True,
            sample_file_path=sample_file_path
        )

        # Append objective value to df for current out-of-sample tree
        df_row = pd.DataFrame({"Sample tree": [sample_tree], "Objective value": [obj_value]})
        df_out_of_sample = pd.concat([df_out_of_sample, df_row], ignore_index = True)
    
    # Calculate out of sample value as mean of objective value from all trees
    out_of_sample_value = df_out_of_sample["Objective value"].mean()
    df_final_row = pd.DataFrame({"Sample tree": ["Out-of-sample value"], "Objective value": [out_of_sample_value]})
    df_out_of_sample = pd.concat([df_out_of_sample, df_final_row], ignore_index = True) 
    df_out_of_sample.to_csv(results_file_path / "OutOfSample" / "out_of_sample_values.csv")







