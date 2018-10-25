from dask import array as da


def bootstrap(df, *args, f, bootstrapping_parameters=None, **kwargs):
    if not bootstrapping_parameters:
        bootstrapping_parameters = {}

    chunks = bootstrapping_parameters.get("chunks", 1000)
    number_of_draws = bootstrapping_parameters.get("number_of_draws", 250)

    # First, draw <number_of_draws> times randomly from the full dataset
    # to simulate different measurements
    random_draws = da.random.choice(df, chunks=chunks, size=(number_of_draws, len(df)), replace=True)

    # Then, apply the function f on all the measurements
    measurement_results = f.call_on_dask_array(random_draws, *args, **kwargs)

    return measurement_results