import json
import logging
from argparse import ArgumentParser
from pathlib import Path

from empire.core.config import EmpireConfiguration, read_config_file
from empire.core.scenario_random import generate_random_scenario

parser = ArgumentParser(description="A CLI script to run the Empire model.")

parser.add_argument(
    "-d",
    "--dataset",
    help="Specify the required dataset",
    default="europe_agg_v50",
)

parser.add_argument("-c", "--config-file", help="Path to config file.", default="config/run.yaml")

# Tree size
parser.add_argument("-n", "--num-trees", help="Number of out of sample trees", type=int, required=True)

# User inputs
args = parser.parse_args()
dataset = args.dataset
num_trees = args.num_trees

## Read config and setup folders ##
if dataset == "test":
    config = read_config_file(Path("config/testrun.yaml"))
elif dataset == "europe_agg_v50":
    config = read_config_file(Path("config/aggrun.yaml"))
else:
    config = read_config_file(Path(args.config_file))

empire_config = EmpireConfiguration.from_dict(config=config)

# Modifications to config
empire_config.use_scenario_generation = True
empire_config.number_of_scenarios = 1
empire_config.moment_matching = False
empire_config.filter_make = False
empire_config.filter_use = False

# Paths for scenario generation
empire_path = Path.cwd()
with open(empire_path / "config/countries.json", "r", encoding="utf-8") as file:
        dict_countries = json.load(file)

scenario_data_path = empire_path / f"Data handler/{dataset}/ScenarioData"

logging.info(f"Generating out of sample trees for {dataset} ...")
for n in range(1, num_trees+1):
    tab_file_path = empire_path / f"OutOfSample/{dataset}/tree{str(n)}"
    generate_random_scenario(
                empire_config=empire_config,
                dict_countries=dict_countries,
                scenario_data_path=scenario_data_path,
                tab_file_path=tab_file_path,
            )
    logging.info(f"Done with tree number: {n}")