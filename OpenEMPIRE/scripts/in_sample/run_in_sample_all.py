from argparse import ArgumentParser
from pathlib import Path

from empire.core.config import EmpireConfiguration, read_config_file
from empire.core.model_runner import run_empire_model, setup_run_paths
from empire.logger import get_empire_logger

parser = ArgumentParser(description="A CLI script to run the Empire model.")

parser.add_argument(
    "-d",
    "--dataset",
    help="Specify the required dataset",
    default="europe_agg_v50",
)

parser.add_argument("-f", "--force", help="Force new run if old exist.", action="store_true")
parser.add_argument("-c", "--config-file", help="Path to config file.", default="config/aggrun.yaml")

# How many instances to solve to obtain mean and SD
parser.add_argument("-ni", "--num-instances", help="Number of instances", type=int, default=30)

args = parser.parse_args()
dataset=args.dataset

## Read config and setup folders ##
config = read_config_file(Path(args.config_file))
empire_config = EmpireConfiguration.from_dict(config=config)

num_instances = args.num_instances
routines = ["basic", "moment", "filter", "copula"]
tree_sizes = [10, 50, 100]

for ts in tree_sizes:
    for routine in routines: 
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
