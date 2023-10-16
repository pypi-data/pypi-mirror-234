import pytest
from pathlib import Path
from gwlandscape_python.utils import identifiers


@pytest.fixture
def setup_paths():
    return {
        'data': Path('test.h5'),
        'dir_data': Path('this/is/a/test.h5'),

        'no_suffix': Path('this/is/a/test'),
        'h5_dir': Path('this/is/not/a/h5'),

        'txt': Path('this/is/not/a/text.txt'),
    }


@pytest.fixture
def setup_identifiers():
    return [
        (
            identifiers.data_file,
            ['data', 'dir_data']
        ),
    ]


@pytest.fixture
def check_identifier(setup_paths):
    def _check_identifier(identifier, true_path_keys):
        true_paths = [value for key, value in setup_paths.items() if key in true_path_keys]
        false_paths = [value for key, value in setup_paths.items() if key not in true_path_keys]
        for path in true_paths:
            assert identifier(path) is True

        for path in false_paths:
            assert identifier(path) is False

    return _check_identifier


def test_identifiers(setup_identifiers, check_identifier):
    for identifier, true_path_keys in setup_identifiers:
        check_identifier(identifier, true_path_keys)
