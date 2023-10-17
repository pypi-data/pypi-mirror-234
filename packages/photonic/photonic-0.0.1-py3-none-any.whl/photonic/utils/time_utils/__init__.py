from time import perf_counter


def print_run_time(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        func(args, kwargs)
        end = perf_counter()

        print(f"Function '{func.__name__}' took {end - start:.6f} seconds to run.")

    return wrapper
