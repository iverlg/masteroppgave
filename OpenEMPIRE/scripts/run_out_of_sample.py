from argparse import ArgumentParser
from pathlib import Path

from empire.core.config import (EmpireConfiguration, EmpireRunConfiguration,
                                read_config_file)
from empire.core.model_runner import run_empire_model
from empire.logger import get_empire_logger
from empire.utils import get_name_of_last_folder_in_path, get_run_name

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
    default="run_in_sample",
)

parser.add_argument("-f", "--force", help="Force new run if old exist.", action="store_true")
parser.add_argument("-c", "--config-file", help="Path to config file.", default="config/run.yaml")

args = parser.parse_args()
dataset = args.dataset
results_dir = args.results_directory

## Read config and setup folders ##
if dataset == "test":
    config = read_config_file(Path("config/testrun.yaml"))
elif dataset == "europe_agg_v50":
    config = read_config_file(Path("config/aggrun.yaml"))
else:
    config = read_config_file(Path(args.config_file))

empire_config = EmpireConfiguration.from_dict(config=config)

# Modifications to config
empire_config.use_scenario_generation = False
empire_config.use_fixed_sample = True

# Get all runs
empire_path = Path.cwd()
results_path = empire_path / f"Results/{results_dir}/dataset_{dataset}"
all_run_paths = sorted([d for d in results_path.iterdir() if d.is_dir()])

out_of_sample_path = empire_path / f"OutOfSample/dataset_{dataset}"
out_of_sample_tree_paths = sorted([t for t in out_of_sample_path.iterdir() if t.is_dir()])

if len(all_run_paths) == 0:
    raise ValueError("Results directory is empty, try specifying another directory")

if len(out_of_sample_tree_paths) == 0:
    raise ValueError("Out of sample runs for directory is empty, generate using the script 'create_out_of_sample_trees.py'")

# Set up run config manually to avoid duplicate input files and easier output struct
run_name = get_run_name(empire_config=empire_config, version=dataset)

break_index = 0
for run_path in all_run_paths:
    if break_index == 2:
        break
    else:
        break_index += 1
    for tree_path in out_of_sample_tree_paths:
        sample_file_path = tree_path
        sample_tree = get_name_of_last_folder_in_path(tree_path)

        # Set up run config manually to avoid duplicate input files and easier output struct
        run_name = get_name_of_last_folder_in_path(run_path) + f"_out-of-sample_{sample_tree}"
        dataset_path = run_path / "Input" / "Xlsx"
        results_file_path = run_path / "Output"

        # Workaround to avoid manual copying scenario files
        tab_path = scenario_data_path = run_path / "Input" / "Tab"

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
        run_empire_model(
            empire_config=empire_config,
            run_config=run_config,
            data_managers=[],
            test_run=False,
            OUT_OF_SAMPLE=True,
            sample_file_path=sample_file_path
        )