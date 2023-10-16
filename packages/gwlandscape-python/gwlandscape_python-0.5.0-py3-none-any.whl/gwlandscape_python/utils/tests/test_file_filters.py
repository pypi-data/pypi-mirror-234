import pytest
from gwlandscape_python.dataset_type import Dataset
from gwlandscape_python.utils import file_filters
from gwlandscape_python import FileReference, FileReferenceList


@pytest.fixture
def data(mocker):
    dataset = Dataset(mocker.Mock(), 1, None, None)
    return FileReferenceList([
        FileReference(
            path='data/dir/test1.h5',
            file_size='1',
            download_token='test_token_1',
            parent=dataset
        ),
        FileReference(
            path='data/dir/test2.h5',
            file_size='1',
            download_token='test_token_2',
            parent=dataset
        ),
    ])


@pytest.fixture
def other(mocker):
    dataset = Dataset(mocker.Mock(), 1, None, None)
    return FileReferenceList([
        FileReference(
            path='result/dir/test1.png',
            file_size='1',
            download_token='test_token_3',
            parent=dataset
        ),
        FileReference(
            path='result/dir/test2.txt',
            file_size='1',
            download_token='test_token_4',
            parent=dataset
        ),
        FileReference(
            path='result/dir/h5.txt',
            file_size='1',
            download_token='test_token_5',
            parent=dataset
        ),
        FileReference(
            path='result/dir/h5',
            file_size='1',
            download_token='test_token_6',
            parent=dataset
        ),
    ])


@pytest.fixture
def full(data, other):
    return data + other


def test_data_file_filter(full, data):
    sub_list = file_filters.data_filter(full)
    assert file_filters.sort_file_list(sub_list) == file_filters.sort_file_list(data)
