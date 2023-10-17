import inspect
import warnings
import re
from collections import namedtuple
import makefun
import hashlib
import cloudpickle as pickle
import pandas as pd

from . import xsettings
from scriptine import path


CachePlan = namedtuple("CachePlan", ['from_cache', 'cache_hash'])
_GET_CACHE_PLAN = False


def x_cached(name='', hash_key=None, also_parquet=False, outer_level=1, static=False, hash_args=True):
    def decorator(func):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        calling_name = calframe[outer_level][3]
        if calling_name == '<module>':
            calling_name = path(calframe[outer_level][1]).namebase

        f_src = inspect.getsource(func)
        short_name = name or func.__name__
        f_name = f"{calling_name}__{func.__name__}"
        if name:
            f_name = f"{f_name}__{name}"

        @makefun.wraps(func)
        def _cached(*args, **kwargs):
            actually_static = static
            cache_folder = None

            if actually_static:
                if not xsettings.STATIC_CATH_PATH:
                    warnings.warn('xsettings.STATIC_CATH_PATH is not set: setting static=False')
                    actually_static = False
                else:
                    cache_folder = xsettings.STATIC_CATH_PATH

            if not actually_static:
                assert xsettings.CACHE_PATH is not None, "must set xsettings.CACHE_PATH"
                cache_folder = xsettings.CACHE_PATH

            assert cache_folder, "Problem with cache_folder"

            cache_folder = path(cache_folder)
            cache_folder = cache_folder.joinpath(f_name)

            code_text = f_src + f_name + name + str(hash_key)
            if hash_args:
                for v in args:
                    if callable(v):
                        code_text += f"; {inspect.getsource(v)}"
                    else:
                        code_text += f"; {v}"

                for k,v in kwargs.items():
                    if callable(v):
                        code_text += f"; {k}={inspect.getsource(v)}"
                    else:
                        code_text += f"; {k}={v}"

            assert re.search(r" at 0x[0-9a-f]{12}>", code_text) is None, "x_cached: found a reference to memory, should probably fix"

            code_hash = hashlib.md5(code_text.encode('utf-8')).hexdigest()

            cache_subfolder = cache_folder.joinpath(code_hash)
            cache_subfolder.ensure_dir()
            cache_file = cache_subfolder.joinpath(f"{short_name}.pickle")

            def create_cache_plan(from_cache=None):
                res = CachePlan(from_cache=from_cache, cache_hash=code_hash)
                return res

            if cache_file.exists():
                if _GET_CACHE_PLAN:
                    return create_cache_plan(from_cache=True)
                else:
                    with open(cache_file, 'rb') as f:
                        results = pickle.load(f)
                        return results

            else:
                if _GET_CACHE_PLAN:
                    return create_cache_plan(from_cache=False)
                else:
                    results = func(*args, **kwargs)

                with open(cache_file, 'wb') as f:
                    pickle.dump(results, f)

                if also_parquet:
                    assert isinstance(results, pd.DataFrame), "need DataFrame to save as parquet"
                    parquet_path = cache_subfolder.joinpath(f"{short_name}.parquet")
                    results.to_parquet(parquet_path, use_deprecated_int96_timestamps=True)

            return results
        return _cached

    return decorator


def x_cached_call(func, *args, name='', hash_key=None, hash_args=True, also_parquet=False, static=False, cached=True, **kwargs):
    if cached:
        dec = x_cached(name=name, hash_key=hash_key, hash_args=hash_args, also_parquet=also_parquet, outer_level=2, static=static)
        return dec(func)(*args, **kwargs)

    return func(*args, **kwargs)


def x_cached_call_list(funcs):
    global _GET_CACHE_PLAN

    first_call_idx = len(funcs) - 1
    return
