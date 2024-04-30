import os
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
from empire.core.config import (EmpireConfiguration, EmpireRunConfiguration,
                                read_config_file)
from empire.core.model_runner import run_empire_model
from empire.logger import get_empire_logger
from empire.utils import get_name_of_last_folder_in_path

###############################################################################
# Before running this script, you should run these scripts for given dataset: #
#    1. scripts/in_sample/run_in_sample_new.py                                    #
#    2. scripts/out_of_sample/create_out_of_sample_trees.py                   #
###############################################################################

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

parser.add_argument(
    "-m",
    "--method",
    help="Specify the SGR method ('basic', 'moment20', 'filter10', 'copula20')",
)

parser.add_argument(
    "-ns",
    "--num_scenarios",
    help="Specify the number of scenarios for given SGR method",
)

parser.add_argument("-f", "--force", help="Force new run if old exist.", action="store_true")
parser.add_argument("-c", "--config-file", help="Path to config file.", default="config/aggrun.yaml")

args = parser.parse_args()
dataset = args.dataset
results_dir = args.results_directory
method = args.method
num_scenarios = args.num_scenarios

## Read config and setup folders ##
config = read_config_file(Path(args.config_file))
empire_config = EmpireConfiguration.from_dict(config=config)

# Modifications to config
empire_config.use_scenario_generation = False
empire_config.use_fixed_sample = True
empire_config.number_of_scenarios = 59

# Get all runs
empire_path = Path.cwd()
results_path = empire_path / f"Results/{results_dir}/dataset_{dataset}"
all_run_paths = sorted([d for d in results_path.iterdir() if d.is_dir()])

out_of_sample_path = empire_path / f"OutOfSample/dataset_{dataset}/tree"

if len(all_run_paths) == 0:
    raise ValueError("Results directory is empty, try specifying another directory")

for run_path in all_run_paths:
    run_details = get_name_of_last_folder_in_path(run_path)
    sgr_method = run_details.split("_")[0]
    ns = run_details.split("_")[1][3:]

    print(run_details)

    if sgr_method != method or num_scenarios != ns:
        continue

    # Part of run config setup
    dataset_path = run_path / "Input" / "Xlsx"
    results_file_path = run_path / "Output"

    # Workaround to avoid manual copying scenario files
    tab_path = scenario_data_path = run_path / "Input" / "Tab"

    # Save objective values in dataframe 
    df_out_of_sample = pd.DataFrame({"Sample tree": [], "Objective value": []})

    sample_file_path = out_of_sample_path
    sample_tree = get_name_of_last_folder_in_path(out_of_sample_path)

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
    
    """ # Calculate out of sample value as mean of objective value from all trees
    out_of_sample_value = df_out_of_sample["Objective value"].mean()
    df_final_row = pd.DataFrame({"Sample tree": ["Out-of-sample value"], "Objective value": [out_of_sample_value]})
    df_out_of_sample = pd.concat([df_out_of_sample, df_final_row], ignore_index = True)  """

    out_of_sample_results_path = empire_path / f"OutOfSample/dataset_{dataset}/new" / run_details

    if not os.path.exists(out_of_sample_results_path):
        os.makedirs(out_of_sample_results_path)

    df_out_of_sample.to_csv(out_of_sample_results_path / "out_of_sample_values.csv")







