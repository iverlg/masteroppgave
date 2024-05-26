import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import wasserstein_distance

AGGR = True

df_onshr_wind = pd.read_csv(f"CopulaTesting/scenario_data{'_agg' if AGGR else ''}/windonshore.csv")
df_load = pd.read_csv(f"CopulaTesting/scenario_data{'_agg' if AGGR else ''}/electricload.csv")
df_solar = pd.read_csv(f"CopulaTesting/scenario_data{'_agg' if AGGR else ''}/solar.csv")
df_offshr_wind = pd.read_csv(f"CopulaTesting/scenario_data{'_agg' if AGGR else ''}/windoffshore.csv")
df_hydro_ror = pd.read_csv(f"CopulaTesting/scenario_data{'_agg' if AGGR else ''}/hydroror.csv")
df_hydro_seasonal = pd.read_csv(f"CopulaTesting/scenario_data{'_agg' if AGGR else ''}/hydroseasonal.csv")

MAPPING = dict({
    "onshore_wind": df_onshr_wind,
    "load": df_load,
    "solar": df_solar,
    "offshore_wind": df_offshr_wind,
    "hydro_ror": df_hydro_ror,
    "hydro_seasonal": df_hydro_seasonal
})

LOCATION_X = "North"
LOCATION_Y = "East"
DF_X = "load"
DF_Y = "load"
N_SCENARIOS = 50

def scale_to_integers(x, y, scale_factor):
    # Scale the real numbers to integers within a suitable range
    scaled_x = int(x * scale_factor)
    scaled_y = int(y * scale_factor)
    return scaled_x, scaled_y

def cantor_pairing_function(x, y):
    # Apply the Cantor pairing function to integer inputs; 2D -> 1D
    return ((x + y) * (x + y + 1)) // 2 + y

def map_to_1d_distribution(x_values, y_values, scale_factor):
    mapped_values = []
    for x, y in zip(x_values, y_values):
        scaled_x, scaled_y = scale_to_integers(x, y, scale_factor)
        mapped_value = cantor_pairing_function(scaled_x, scaled_y)
        mapped_values.append(mapped_value)
    return mapped_values

def remove_time_and_filter_location(df: pd.DataFrame, location: str) -> pd.DataFrame:
    _df = df.copy()
    _df = _df.drop(columns=["time"])
    _df = _df[[location]]
    return _df

TEXT_MAPPING = {
    "load": "Load",
    "solar": "Solar PV", 
    "onshore_wind": "Wind onshore"
}

def plot_copula(df: pd.DataFrame, loc_x: str, loc_y: str, xx: str, yy: str, scenario = None, distance: float = None) -> None:
    _df = df.copy()
    x = _df["rank_value_x"]
    y = _df["rank_value_y"]

    plt.rcParams.update({'font.size': 20})
    plt.figure(figsize=(10,6))
    plt.scatter(x, y, color="blue", s=0.5)

    plt.xlabel(f"{TEXT_MAPPING[xx]} {loc_x}")
    plt.ylabel(f"{TEXT_MAPPING[yy]} {loc_y}")

    title = "Original copula"
    if distance != None:
        title = f"Sampled copula. Distance = {distance:.1E}"

    plt.title(title)
    plt.savefig(f"CopulaTesting/original_copula_figs/{xx}-{yy}_{loc_x}-{loc_y}{'_scenario-' + str(scenario + 1) if scenario != None else ''}", bbox_inches="tight")
    plt.close()

def generate_random_scenario() -> list[int]:
    # Pick random year (1-5)
    sampling_year = np.random.randint(1, 6) #1-5

    # Filter to hours for given year
    sampling_year_indexes = range(8760*(sampling_year-1), 8760*sampling_year)

    # Pick random start hours within given year
    sampling_hours_start = sorted(np.random.randint(sampling_year_indexes[0], sampling_year_indexes[-1], size=6))

    # Make sure non-overlapping intervals
    redo_sampling = True
    while redo_sampling:
        solution_good = True
        for i in range(0, len(sampling_hours_start)-1):
            if sampling_hours_start[i] - sampling_hours_start[i+1] > -168:
                sampling_hours_start = sorted(np.random.randint(sampling_year_indexes[0], sampling_year_indexes[-1], size=6))
                solution_good = False
        redo_sampling = False if solution_good else True

    # Generate sample data (168 hours x 4 seasons + 2 peaks x 24 hours)
    sampling_hours = []
    for j in range(0, len(sampling_hours_start)):
        hour = sampling_hours_start[j]
        interval_length = 168 if j < 4 else 24
        for _h in range(hour, hour+interval_length):
            sampling_hours.append(_h)

    return sampling_hours

def _calculate_rank_values(df: pd.DataFrame, sampling_hours: list[int] = None) -> pd.DataFrame:
    _df = df.copy()
    if sampling_hours != None:
        _df = _df.filter(items=sampling_hours, axis=0)

    _df["rank"] = _df.rank(method="first")
    # Sample and reindex to get random order if tie
    #_df["rank"] = _df.sample(frac=1).rank(method='first').reindex_like(_df)
    _df["rank_value"] = _df["rank"] / len(_df)
    return _df

def generate_copula(df_x: pd.DataFrame, df_y: pd.DataFrame, sampling_hours: list[int] = None) -> pd.DataFrame:
    _df_x = _calculate_rank_values(df_x, sampling_hours)
    _df_y = _calculate_rank_values(df_y, sampling_hours)
    df_copula = pd.DataFrame(index=range(0, len(_df_x)) if sampling_hours == None else sampling_hours)
    df_copula["rank_value_x"] = df_copula.join(_df_x)[["rank_value"]]
    df_copula["rank_value_y"] = df_copula.join(_df_y)[["rank_value"]]
    return df_copula

def calculate_distance(df_copula: pd.DataFrame, df_copula_sample: pd.DataFrame) -> float:
    _df_copula = df_copula.copy()
    _df_copula_sample = df_copula_sample.copy()

    copula_1d = map_to_1d_distribution(_df_copula["rank_value_x"], _df_copula["rank_value_y"], 10000)
    copula_sample_1d = map_to_1d_distribution(_df_copula_sample["rank_value_x"], _df_copula_sample["rank_value_y"], 10000)
    ws_dist = wasserstein_distance(copula_1d, copula_sample_1d)
    return ws_dist

""" def calculate_distance(df_copula: pd.DataFrame, df_copula_sample: pd.DataFrame) -> float:
    _df_copula = df_copula.copy()
    _df_copula_sample = df_copula_sample.copy()

    distance = 0
    for _, row in _df_copula_sample.iterrows():
        sample_x = row["rank_value_x"]
        sample_y = row["rank_value_y"]

        # Based on rank_value_x
        closest_original_row = _df_copula.iloc[(_df_copula['rank_value_x']-sample_x).abs().argsort()[:1]]

        # Calculate abs distance between sample point and 'closest' point (along x-axis) on original copula
        distance += (abs(closest_original_row["rank_value_x"].values[0]-sample_x) + \
                     abs(closest_original_row["rank_value_y"].values[0]-sample_y))

    return distance """

def main():
    considered_combos = []
    unique_nodes = ["East", "North", "West"]
    for i in range(len(unique_nodes)):
        for j in range(i, len(unique_nodes)):
            loc_x = unique_nodes[i]
            loc_y = unique_nodes[j]
            for xx in TEXT_MAPPING.keys():
                for yy in TEXT_MAPPING.keys():
                    if loc_x==loc_y and xx==yy: 
                        continue

                    considered = sorted([loc_x, loc_y, xx, yy])
                    if considered in considered_combos:
                        continue
                    else:
                        considered_combos.append(considered)
                    df_x = remove_time_and_filter_location(MAPPING[xx], location=loc_x)
                    df_y = remove_time_and_filter_location(MAPPING[yy], location=loc_y)

                    df_copula_original = generate_copula(df_x, df_y)
                    plot_copula(df_copula_original, loc_x, loc_y, xx, yy, scenario=None, distance=None)

    
    """ 
    min_distance = np.inf
    best_copula: pd.DataFrame = None

    for n in range(N_SCENARIOS):
        sampling_hours = generate_random_scenario()
        df_copula_sample = generate_copula(df_x, df_y, sampling_hours=sampling_hours)
        sample_distance = calculate_distance(df_copula_original, df_copula_sample)
        print(f"Sample distance for scenario {n}: {sample_distance}")
        plot_copula(df_copula_sample, loc_x, loc_y, scenario=n, distance=sample_distance)
        if sample_distance < min_distance:
            best_copula = df_copula_sample
            min_distance = sample_distance
    plot_copula(best_copula, loc_x, loc_y, scenario='best', distance=min_distance) """

if __name__ == "__main__":
    main()