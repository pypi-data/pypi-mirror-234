from functools import wraps
from pathlib import Path
import tarfile
import h5py


# Taken from https://stackoverflow.com/a/40363565
# Needed to be able to identify the names of arguments provided,
# whether or not they were positional or keywords
def _get_args_dict(fn, args, kwargs):
    args_names = fn.__code__.co_varnames[:fn.__code__.co_argcount]
    return {**dict(zip(args_names, args)), **kwargs}


# Heavily adapted from https://stackoverflow.com/a/54487188
def mutually_exclusive(*keywords):
    if len(keywords) < 2:
        raise SyntaxError('mutually_exclusive decorator does nothing without at least two arguments')

    # Split OR groups, and then count how many of the mutually exclusive keywords appear in the the kwargs
    keyword_sets = [keyword.replace(' ', '').split('|') for keyword in keywords]

    error_msg = 'You must specify at most one of {}'.format(', '.join(keywords))

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            arg_list = _get_args_dict(func, args, kwargs)

            n_mutex_keywords = sum(any(k in arg_list for k in keyword_set) for keyword_set in keyword_sets)

            # If there is more than one of the mutually exclusive arguments, we have a problem
            if n_mutex_keywords > 1:
                raise SyntaxError(error_msg)

            return func(*args, **kwargs)
        return inner
    return wrapper


def validate_dataset(file_path):
    if h5py.is_hdf5(file_path):
        return None

    if not tarfile.is_tarfile(file_path):
        raise Exception('Upload is neither a tarfile nor a hdf5 file')

    with tarfile.open(file_path) as f:
        if sum(Path(name).suffix in ['.h5', '.hdf5'] for name in f.getnames()) != 1:
            raise Exception('Tarfile must contain exactly one hdf5 file')
