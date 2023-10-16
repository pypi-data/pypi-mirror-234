import pickle
import os
import hashlib
import inspect
import yaml
from dotenv import load_dotenv


def get_cache_dir():
    load_dotenv()

    try:
        if os.environ.get("SECD") == "PRODUCTION":
            with open("secd.yml", "r") as f:
                run_meta = yaml.load(f)
                if "cache_dir" in run_meta and "mount_path" in run_meta:
                    return os.path.join(run_meta["mount_path"], "cache")
    except:
        return "cache"
    return "cache"


CACHE_DIR = get_cache_dir()


def generate_cache_key(func, args, kwargs):
    # Create a unique cache key based on the function name, args, kwargs, and source code
    source_code = inspect.getsource(func)
    key = f"{func.__name__}:{args}:{kwargs}:{hashlib.md5(source_code.encode()).hexdigest()}"
    return hashlib.md5(key.encode()).hexdigest()


def cache(func):
    def wrapper(*args, **kwargs):
        # Ensure the cache directory exists; create it if not
        os.makedirs(CACHE_DIR, exist_ok=True)

        # Generate a cache key based on function name, args, kwargs, and source code hash
        cache_key = generate_cache_key(func, args, kwargs)
        cache_path = os.path.join(CACHE_DIR, cache_key)

        # Initialize computed_source_code_hash to None
        computed_source_code_hash = hashlib.md5(
            inspect.getsource(func).encode()).hexdigest()

        if os.path.exists(cache_path):
            # Load the cached result and source code hash
            with open(cache_path, "rb") as cache_file:
                cached_source_code_hash, result = pickle.load(cache_file)

            if computed_source_code_hash == cached_source_code_hash:
                print(f"Using cached result for {func.__name__}")
                return result
            else:
                print(
                    f"Function code has changed; recomputing {func.__name__}")
        else:
            print(f"Cache not found; recomputing {func.__name__}")

        # Execute the function and save the result and source code hash to the cache
        result = func(*args, **kwargs)
        with open(cache_path, "wb") as cache_file:
            pickle.dump((computed_source_code_hash, result), cache_file)
        return result

    return wrapper


def get_output_path():
    env_path = os.environ.get('OUTPUT_PATH')
    if env_path:
        os.makedirs(env_path, exist_ok=True)
        return env_path
    else:
        os.makedirs('output', exist_ok=True)
        return 'output'
