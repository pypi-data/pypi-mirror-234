import tempfile
import tarfile
import h5py
import pytest
from gwlandscape_python.utils import mutually_exclusive, _get_args_dict, validate_dataset


@pytest.mark.parametrize("args,kwargs,args_dict", [
    ((1, 2), {'arg3': 3, 'arg4': 4}, {'arg1': 1, 'arg2': 2, 'arg3': 3, 'arg4': 4}),
    ((1, ), {'arg2': 2, 'arg3': 3, 'arg4': 4}, {'arg1': 1, 'arg2': 2, 'arg3': 3, 'arg4': 4}),
    ((), {'arg1': 1, 'arg2': 2, 'arg3': 3, 'arg4': 4}, {'arg1': 1, 'arg2': 2, 'arg3': 3, 'arg4': 4}),
    ((1, 2, 3, 4), {}, {'arg1': 1, 'arg2': 2, 'arg3': 3, 'arg4': 4}),
    ((1, 2, 3), {}, {'arg1': 1, 'arg2': 2, 'arg3': 3}),
    ((1, 2), {'arg4': 4}, {'arg1': 1, 'arg2': 2, 'arg4': 4}),
    ((1, 2), {}, {'arg1': 1, 'arg2': 2}),
])
def test_get_args_dict(args, kwargs, args_dict):
    def arbitrary_func(arg1, arg2, arg3=None, arg4=None):
        return True

    assert _get_args_dict(arbitrary_func, args, kwargs) == args_dict


@pytest.fixture
def get_mutex_func():
    def mutex_func(*mutex_args):
        @mutually_exclusive(*mutex_args)
        def arbitrary_func(arg1=None, arg2=None, arg3=None, arg4=None):
            return True

        return arbitrary_func
    return mutex_func


@pytest.mark.parametrize("mutex_args,args_dict", [
    (('arg1', 'arg2'), {'arg1': 1, 'arg2': 2}),
    (('arg1', 'arg2', 'arg3'), {'arg1': 1, 'arg2': 2}),
    (('arg1', 'arg2', 'arg3'), {'arg1': 1, 'arg3': 3}),
    (('arg1', 'arg2', 'arg3'), {'arg2': 2, 'arg3': 3}),
    (('arg1 | arg2', 'arg3'), {'arg1': 1, 'arg3': 3}),
    (('arg1 | arg2', 'arg3'), {'arg2': 2, 'arg3': 3}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg1': 1, 'arg3': 3}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg1': 1, 'arg4': 4}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg2': 2, 'arg3': 3}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg2': 2, 'arg4': 4}),
    (('arg1 | arg2 | arg3', 'arg4'), {'arg1': 1, 'arg4': 4}),
    (('arg1 | arg2 | arg3', 'arg4'), {'arg2': 2, 'arg4': 4}),
    (('arg1 | arg2 | arg3', 'arg4'), {'arg3': 3, 'arg4': 4}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg1': 1, 'arg2': 2}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg1': 1, 'arg3': 3}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg1': 1, 'arg4': 4}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg2': 2, 'arg3': 3}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg2': 2, 'arg4': 4}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg3': 3, 'arg4': 4}),
])
def test_mutually_exclusive_fail(get_mutex_func, mutex_args, args_dict):
    func = get_mutex_func(*mutex_args)
    with pytest.raises(SyntaxError):
        func(**args_dict)


@pytest.mark.parametrize("mutex_args,args_dict", [
    (('arg1', 'arg2'), {'arg1': 1}),
    (('arg1', 'arg2'), {'arg2': 2}),
    (('arg1', 'arg2'), {'arg3': 3}),
    (('arg1', 'arg2'), {'arg1': 1, 'arg3': 3}),
    (('arg1', 'arg2'), {'arg2': 2, 'arg3': 3}),
    (('arg1', 'arg2', 'arg3'), {'arg1': 1, 'arg4': 4}),
    (('arg1', 'arg2', 'arg3'), {'arg2': 2, 'arg4': 4}),
    (('arg1', 'arg2', 'arg3'), {'arg3': 3, 'arg4': 4}),
    (('arg1 | arg2', 'arg3'), {'arg1': 1, 'arg4': 4}),
    (('arg1 | arg2', 'arg3'), {'arg2': 2, 'arg4': 4}),
    (('arg1 | arg2', 'arg3'), {'arg3': 3, 'arg4': 4}),
    (('arg1 | arg2', 'arg3'), {'arg1': 1, 'arg2': 2}),
    (('arg1 | arg2', 'arg3'), {'arg1': 1, 'arg2': 2, 'arg4': 4}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg1': 1}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg2': 2}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg3': 3}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg4': 4}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg1': 1, 'arg2': 2}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg3': 3, 'arg4': 4}),
    (('arg1 | arg2 | arg3', 'arg4'), {'arg1': 1, 'arg2': 2}),
    (('arg1 | arg2 | arg3', 'arg4'), {'arg1': 1, 'arg3': 3}),
    (('arg1 | arg2 | arg3', 'arg4'), {'arg2': 2, 'arg3': 3}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg1': 1}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg2': 2}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg3': 3}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg4': 4}),
])
def test_mutually_exclusive_succeed(get_mutex_func, mutex_args, args_dict):
    func = get_mutex_func(*mutex_args)
    assert func(**args_dict)


def test_validate_dataset_h5():
    h5 = h5py.File(tempfile.NamedTemporaryFile(suffix='.h5').name, 'w')
    assert validate_dataset(h5.filename) is None


def test_validate_dataset_tar_with_h5():
    with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as f:
        with tarfile.open(fileobj=f, mode='w:gz') as tar:
            tar.add(h5py.File(tempfile.NamedTemporaryFile(suffix='.h5').name, 'w').filename)
    assert validate_dataset(tar.name) is None


def test_validate_dataset_tar_with_multiple_h5():
    with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as f:
        with tarfile.open(fileobj=f, mode='w:gz') as tar:
            tar.add(h5py.File(tempfile.NamedTemporaryFile(suffix='.h5').name, 'w').filename)
            tar.add(h5py.File(tempfile.NamedTemporaryFile(suffix='.h5').name, 'w').filename)

    with pytest.raises(Exception):
        validate_dataset(tar.name)


def test_validate_dataset_not_tar_or_h5():
    with pytest.raises(Exception):
        validate_dataset(tempfile.NamedTemporaryFile().name)
