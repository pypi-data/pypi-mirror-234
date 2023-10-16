import pytest
from gwlandscape_python import GWLandscape, FileReference, FileReferenceList
from gwlandscape_python.dataset_type import Dataset
from gwlandscape_python.keyword_type import Keyword
from gwlandscape_python.model_type import Model
from gwlandscape_python.publication_type import Publication


@pytest.fixture
def setup_gwl_request(mocker):
    def mock_init(self, token, auth_endpoint, endpoint):
        pass

    mock_request = mocker.Mock()
    mocker.patch('gwlandscape_python.gwlandscape.GWDC.__init__', mock_init)
    mocker.patch('gwlandscape_python.gwlandscape.GWDC.request', mock_request)

    return GWLandscape(token='my_token'), mock_request


@pytest.fixture
def mock_keyword_data():
    def _mock_keyword_data(i=1):
        return {'tag': f'mock tag {i}'}
    return _mock_keyword_data


@pytest.fixture
def create_keyword(mock_keyword_data):
    def _create_keyword(client, i=1):
        return Keyword(client=client, id=f'mock_keyword_id{i}', **mock_keyword_data(i))
    return _create_keyword


@pytest.fixture
def query_keyword_return(mock_keyword_data):
    def _query_keyword_return(n_keywords, start_id=1):
        return {
            "keywords": {
                "edges": [
                    {
                        "node": {
                            "id": f'mock_keyword_id{i}',
                            **mock_keyword_data(i)
                        }
                    } for i in range(start_id, n_keywords+start_id)
                ]
            }
        }
    return _query_keyword_return


@pytest.fixture
def mock_publication_data(create_keyword):
    def _mock_publication_data(i=1, n_keywords=0):
        return {
            'author': f'mock author {i}',
            'published': bool(i % 2),
            'title': f'mock publication {i}',
            'year': 1234+i,
            'journal': f'mock journal {i}',
            'journal_doi': f'mock journal doi {i}',
            'dataset_doi': f'mock dataset doi {i}',
            'description': f'mock description {i}',
            'public': bool(i % 2),
            'download_link': f'mock download link {i}',
            'arxiv_id': f'mock arxiv id {i}',
            'keywords': [create_keyword(None, ik) for ik in range(1, n_keywords+1)]
        }
    return _mock_publication_data


@pytest.fixture
def create_publication(mock_publication_data):
    def _create_publication(client, i=1, n_keywords=0):
        return Publication(
            client=client,
            id=f'mock_publication_id{i}',
            creation_time='2022-06-20T02:12:59.459297+00:00',
            **mock_publication_data(i, n_keywords))
    return _create_publication


@pytest.fixture
def query_publication_return(mock_publication_data, query_keyword_return):
    def _query_publication_return(n_publications, n_keywords=2):
        return {
            'compas_publications': {
                'edges': [
                    {
                        'node': {
                            'id': f'mock_publication_id{i}',
                            'creation_time': '2022-06-20T02:12:59.459297+00:00',
                            # Don't look at this, it's disgusting
                            **{
                                **mock_publication_data(i),
                                **query_keyword_return(n_keywords)
                            }
                        }
                    }
                ] for i in range(1, n_publications+1)
            }
        }
    return _query_publication_return


@pytest.fixture
def mock_model_data():
    def _mock_model_data(i=1):
        return {
            'name': f'mock name {i}',
            'summary': f'mock summary {i}',
            'description': f'mock description {i}',
        }
    return _mock_model_data


@pytest.fixture
def create_model(mock_model_data):
    def _create_model(client, i=1):
        return Model(client=client, id=f'mock_model_id{i}', **mock_model_data(i))
    return _create_model


@pytest.fixture
def query_model_return(mock_model_data):
    def _query_model_return(n_models):
        return {
            'compas_models': {
                'edges': [
                    {
                        'node': {
                            'id': f'mock_model_id{i}',
                            **mock_model_data(i)
                        } for i in range(1, n_models+1)
                    }
                ]
            }
        }
    return _query_model_return


@pytest.fixture
def mock_dataset_data(create_publication, create_model):
    def _mock_dataset_data(client, i=1):
        return {
            'publication': create_publication(client, i, n_keywords=2),
            'model': create_model(client, i),
        }
    return _mock_dataset_data


@pytest.fixture
def create_dataset(mock_dataset_data):
    def _create_dataset(client, i=1):
        return Dataset(
            client=client,
            dataset_id=f'mock_dataset_id{i}',
            **mock_dataset_data(client, i)
        )
    return _create_dataset


@pytest.fixture
def query_dataset_return(query_publication_return, query_model_return):
    def _query_dataset_return(n_datasets):
        return {
            'compas_dataset_models': {
                'edges': [
                    {
                        'node': {
                            'id': f'mock_dataset_id{i}',
                            'compas_publication':
                                query_publication_return(i)['compas_publications']['edges'][0]['node'],
                            'compas_model': query_model_return(i)['compas_models']['edges'][0]['node'],
                        } for i in range(1, n_datasets+1)
                    }
                ]
            }
        }
    return _query_dataset_return


@pytest.fixture
def mock_dataset_file_data():
    def _mock_dataset_file_data(i=1):
        return {
            'path': f'path/to/test_{i}.h5',
            'file_size': f'{i}',
            'download_token': f'test_token_{i}',
        }
    return _mock_dataset_file_data


@pytest.fixture
def query_dataset_files_return(mock_dataset_file_data):
    def _query_dataset_files_return(n_files):
        return {
            'compas_dataset_model': {
                'files': [mock_dataset_file_data(i) for i in range(1, n_files+1)]
            }
        }
    return _query_dataset_files_return


@pytest.fixture
def create_dataset_files(mock_dataset_file_data):
    def _create_dataset_files(dataset, n_files):
        return FileReferenceList([
            FileReference(
                **mock_dataset_file_data(i),
                parent=dataset
            ) for i in range(1, n_files+1)
        ])
    return _create_dataset_files
