#!/usr/bin/env python
import json
import logging
import time
from argparse import ArgumentParser
from pathlib import Path

from empire.core.config import EmpireConfiguration, read_config_file
from empire.core.scenario_random import (check_scenarios_exist,
                                         generate_random_scenario)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = ArgumentParser(description="A CLI script to generate scenarios for the Empire model.")

parser.add_argument("-f", "--force", help="Force new scenarios even if old scenarios exist", action="store_true")

args = parser.parse_args()

version = "europe_v51"
config_path = Path("config/run.yaml")
config = read_config_file(config_path)
empire_config = EmpireConfiguration.from_dict(config=config)

scenario_data_path = Path.cwd() / f"Data handler/{version}/ScenarioData"

with open(Path.cwd() / "config/countries.json", "r", encoding="utf-8") as file:
    dict_countries = json.load(file)

empire_config.number_of_scenarios = 1
empire_config.n_tree_compare = 20
empire_config.copula_make = False
empire_config.copula_use = False
empire_config.copula_clusters_make = ["electricload"]

if not check_scenarios_exist(scenario_data_path=scenario_data_path) or args.force:
    logger.info("Generating scenarios.")

    start_time = time.time()
    generate_random_scenario(
        empire_config=empire_config,
        dict_countries=dict_countries,
        scenario_data_path=scenario_data_path,
        tab_file_path=scenario_data_path,
    )
    end_time = time.time()
    runtime = end_time - start_time
    print("Runtime:", runtime, "seconds")
else:
    logger.warning(
        "Stochastic scenarios already exist in the ScenarioData folder. "
        "Delete these if you want new scenarios or force this by using the '-f' argument."
    )