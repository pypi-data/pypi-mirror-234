import uuid
from tempfile import NamedTemporaryFile
import h5py

import pytest

from gwlandscape_python import FileReference
from gwlandscape_python.tests.utils import compare_graphql_query


@pytest.fixture
def create_keyword_request(setup_gwl_request, query_keyword_return):
    response_data = [
        {
            "add_keyword": {
                "id": "mock_keyword_id1"
            }
        },
        query_keyword_return(n_keywords=1)
    ]

    gwl, mr = setup_gwl_request

    def mock_request(*args, **kwargs):
        return response_data.pop(0)

    mr.side_effect = mock_request

    return gwl, mr


@pytest.fixture
def get_keywords_query():
    return """
        query ($exact: String, $contains: String, $id: ID) {
            keywords (tag: $exact, tag_Icontains: $contains, id: $id) {
                edges {
                    node {
                        id
                        tag
                    }
                }
            }
        }
    """


@pytest.fixture
def create_publication_request(setup_gwl_request, query_publication_return):
    response_data = [
        {
            "add_publication": {
                "id": "mock_publication_id1"
            }
        },
        query_publication_return(n_publications=1)
    ]

    gwl, mr = setup_gwl_request

    def mock_request(*args, **kwargs):
        return response_data.pop(0)

    mr.side_effect = mock_request

    return gwl, mr


@pytest.fixture
def get_publications_query():
    return """
        query ($author: String, $title: String, $id: ID) {
            compasPublications (
                author_Icontains: $author,
                title_Icontains: $title,
                id: $id
            ) {
                edges {
                    node {
                        id
                        author
                        published
                        title
                        year
                        journal
                        journalDoi
                        datasetDoi
                        creationTime
                        description
                        public
                        downloadLink
                        arxivId
                        keywords {
                            edges {
                                node {
                                    id
                                    tag
                                }
                            }
                        }
                    }
                }
            }
        }
    """


@pytest.fixture
def create_model_request(setup_gwl_request, query_model_return):
    response_data = [
        {
            "add_compas_model": {
                "id": "mock_model_id1"
            }
        },
        query_model_return(n_models=1)
    ]

    gwl, mr = setup_gwl_request

    def mock_request(*args, **kwargs):
        return response_data.pop(0)

    mr.side_effect = mock_request

    return gwl, mr


@pytest.fixture
def get_models_query():
    return """
        query ($name: String, $summary: String, $description: String, $id: ID) {
            compasModels (
                name_Icontains: $name,
                summary_Icontains: $summary,
                description_Icontains: $description,
                id: $id
            ) {
                edges {
                    node {
                        id
                        name
                        summary
                        description
                    }
                }
            }
        }
    """


@pytest.fixture
def create_dataset_request(setup_gwl_request, query_dataset_return):
    response_data = [
        {
            "generate_compas_dataset_model_upload_token": {
                "token": str(uuid.uuid4())
            }
        },
        {
            "upload_compas_dataset_model": {
                "id": "mock_dataset_id1"
            }
        },
        query_dataset_return(n_datasets=1)
    ]

    gwl, mr = setup_gwl_request

    def mock_request(*args, **kwargs):
        return response_data.pop(0)

    mr.side_effect = mock_request

    return gwl, mr


@pytest.fixture
def get_datasets_query():
    return """
        query ($publication: ID, $model: ID, $id: ID) {
            compasDatasetModels (compasPublication: $publication, compasModel: $model, id: $id) {
                edges {
                    node {
                        id
                        compasPublication {
                            id
                            author
                            published
                            title
                            year
                            journal
                            journalDoi
                            datasetDoi
                            creationTime
                            description
                            public
                            downloadLink
                            arxivId
                            keywords {
                                edges {
                                    node {
                                        id
                                        tag
                                    }
                                }
                            }
                        }
                        compasModel {
                            id
                            name
                            summary
                            description
                        }
                    }
                }
            }
        }
    """


@pytest.fixture
def setup_mock_download_fns(mocker, create_dataset_files):
    def _setup_mock_download_fns(dataset):
        mock_files = mocker.Mock(
            return_value=[(f.path, NamedTemporaryFile()) for f in create_dataset_files(dataset, 3)]
        )

        return (
            mocker.patch('gwlandscape_python.gwlandscape._download_files', mock_files),
            mocker.patch('gwlandscape_python.gwlandscape._get_file_map_fn'),
            mocker.patch('gwlandscape_python.gwlandscape._save_file_map_fn'),
        )
    return _setup_mock_download_fns


def test_create_keyword(create_keyword_request, mock_keyword_data, get_keywords_query):
    gwl, mock_request = create_keyword_request

    keyword_data = mock_keyword_data(i=1)
    keyword_id = 'mock_keyword_id1'

    keyword = gwl.create_keyword(**keyword_data)

    assert keyword.id == keyword_id
    assert keyword.tag == keyword_data['tag']

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            mutation AddKeywordMutation($input: AddKeywordMutationInput!) {
                addKeyword(input: $input) {
                    id
                }
            }
        """
    )

    assert mock_request.mock_calls[0].args[1] == {'input': keyword_data}

    assert compare_graphql_query(
        mock_request.mock_calls[1].kwargs['query'],
        get_keywords_query
    )

    assert mock_request.mock_calls[1].kwargs['variables'] == {
        'exact': None,
        'contains': None,
        'id': keyword_id
    }


@pytest.mark.parametrize('exact', [True, False])
@pytest.mark.parametrize('contains', [True, False])
@pytest.mark.parametrize('_id', [True, False])
def test_get_keyword_exact(
    setup_gwl_request,
    query_keyword_return,
    mock_keyword_data,
    get_keywords_query,
    exact,
    contains,
    _id
):
    gwl, mock_request = setup_gwl_request

    keyword_data = mock_keyword_data(i=1)
    keyword_id = 'mock_keyword_id1'

    input_pairs = [('exact', exact), ('contains', contains)]
    inputs = {key: keyword_data['tag'] for key, val in input_pairs if val}
    if _id:
        inputs['_id'] = keyword_id

    if len(inputs) > 1:
        with pytest.raises(SyntaxError):
            gwl.get_keywords(**inputs)
        return

    mock_request.return_value = query_keyword_return(n_keywords=1)

    kws = gwl.get_keywords(**inputs)
    assert len(kws) == 1

    keyword = kws[0]
    assert keyword.id == keyword_id
    assert keyword.tag == keyword_data['tag']

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_keywords_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'exact': None,
        'contains': None,
        'id': inputs.pop('_id', None),
        **inputs
    }


def test_get_keyword_multi(setup_gwl_request, query_keyword_return, mock_keyword_data, get_keywords_query):
    gwl, mock_request = setup_gwl_request

    keywords_data = [mock_keyword_data(i+1) for i in range(2)]

    mock_request.return_value = query_keyword_return(n_keywords=2)

    kws = gwl.get_keywords()
    assert len(kws) == 2

    for i, keyword_data in enumerate(keywords_data):
        assert kws[i].id == f'mock_keyword_id{i+1}'
        assert kws[i].tag == keyword_data['tag']

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_keywords_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'exact': None,
        'contains': None,
        'id': None
    }


def test_create_publication(create_publication_request, mock_publication_data, get_publications_query):
    gwl, mock_request = create_publication_request

    publication_data = mock_publication_data(i=1, n_keywords=2)
    publication_id = 'mock_publication_id1'

    publication = gwl.create_publication(**publication_data)

    assert publication.id == publication_id
    for key, val in publication_data.items():
        assert getattr(publication, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            mutation AddPublicationMutation($input: AddPublicationMutationInput!) {
                addPublication(input: $input) {
                    id
                }
            }
        """
    )

    publication_data['keywords'] = [keyword.id for keyword in publication_data['keywords']]
    assert mock_request.mock_calls[0].args[1] == {'input': publication_data}

    assert compare_graphql_query(
        mock_request.mock_calls[1].kwargs['query'],
        get_publications_query
    )

    assert mock_request.mock_calls[1].kwargs['variables'] == {
        'author': None,
        'title': None,
        'id': publication_id
    }


@pytest.mark.parametrize('author', [True, False])
@pytest.mark.parametrize('title', [True, False])
@pytest.mark.parametrize('_id', [True, False])
def test_get_publication_author_title(
    setup_gwl_request,
    query_publication_return,
    mock_publication_data,
    get_publications_query,
    author,
    title,
    _id
):
    gwl, mock_request = setup_gwl_request

    publication_data = mock_publication_data(1, n_keywords=2)
    publication_data['_id'] = 'mock_publication_id1'

    input_pairs = [('author', author), ('title', title), ('_id', _id)]
    inputs = {key: publication_data[key] for key, val in input_pairs if val}

    publication_id = publication_data.pop('_id')

    if _id and len(inputs) > 1:
        with pytest.raises(SyntaxError):
            gwl.get_publications(**inputs)
        return

    mock_request.return_value = query_publication_return(n_publications=1)

    publications = gwl.get_publications(**inputs)
    assert len(publications) == 1

    publication = publications[0]

    assert publication.id == publication_id
    for key, val in publication_data.items():
        assert getattr(publication, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_publications_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'author': None,
        'title': None,
        'id': inputs.pop('_id', None),
        **inputs
    }


def test_create_model(create_model_request, mock_model_data, get_models_query):
    gwl, mock_request = create_model_request

    model_data = mock_model_data(i=1)
    model_id = 'mock_model_id1'

    model = gwl.create_model(**model_data)

    assert model.id == model_id
    for key, val in model_data.items():
        assert getattr(model, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].args[0],
        """
            mutation AddCompasModelMutation($input: AddCompasModelMutationInput!) {
                addCompasModel(input: $input) {
                    id
                }
            }
        """
    )

    assert mock_request.mock_calls[0].args[1] == {'input': model_data}

    assert compare_graphql_query(
        mock_request.mock_calls[1].kwargs['query'],
        get_models_query
    )

    assert mock_request.mock_calls[1].kwargs['variables'] == {
        'name': None,
        'summary': None,
        'description': None,
        'id': model_id
    }


@pytest.mark.parametrize('name', [True, False])
@pytest.mark.parametrize('description', [True, False])
@pytest.mark.parametrize('summary', [True, False])
@pytest.mark.parametrize('_id', [True, False])
def test_get_models(
    setup_gwl_request,
    query_model_return,
    mock_model_data,
    get_models_query,
    name,
    description,
    summary,
    _id
):
    gwl, mock_request = setup_gwl_request

    model_data = mock_model_data(i=1)
    model_data['_id'] = 'mock_model_id1'

    input_pairs = [('name', name), ('summary', summary), ('description', description), ('_id', _id)]
    inputs = {key: model_data[key] for key, val in input_pairs if val}

    model_id = model_data.pop('_id')

    if _id and len(inputs) > 1:
        with pytest.raises(SyntaxError):
            gwl.get_models(**inputs)
        return

    mock_request.return_value = query_model_return(1)

    models = gwl.get_models(**inputs)
    assert len(models) == 1

    model = models[0]

    assert model.id == model_id
    for key, val in model_data.items():
        assert getattr(model, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_models_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'name': None,
        'summary': None,
        'description': None,
        'id': inputs.pop('_id', None),
        **inputs,
    }


def test_create_dataset(create_dataset_request, mock_dataset_data, get_datasets_query):
    gwl, mock_request = create_dataset_request

    dataset_data = mock_dataset_data(gwl, i=1)
    dataset_id = 'mock_dataset_id1'

    with NamedTemporaryFile(suffix='.h5') as tf:
        h5_file = h5py.File(tf.name, 'w')
        dataset = gwl.create_dataset(dataset_data['publication'], dataset_data['model'], h5_file.filename)

    assert dataset.id == dataset_id

    publication, model = dataset.publication, dataset.model

    for key, val in publication.__dict__.items():
        assert getattr(dataset.publication, key) == val

    for key, val in model.__dict__.items():
        assert getattr(dataset.model, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        """
            query GenerateCompasDatasetModelUploadToken {
                generateCompasDatasetModelUploadToken {
                  token
                }
            }
        """
    )

    assert compare_graphql_query(
        mock_request.mock_calls[1].kwargs['query'],
        """
            mutation UploadCompasDatasetModelMutation($input: UploadCompasDatasetModelMutationInput!) {
                uploadCompasDatasetModel(input: $input) {
                    id
                }
            }
        """
    )

    assert mock_request.mock_calls[1].kwargs['variables']['input']['compas_publication'] == publication.id
    assert mock_request.mock_calls[1].kwargs['variables']['input']['compas_model'] == model.id
    assert 'jobFile' in mock_request.mock_calls[1].kwargs['variables']['input']

    assert compare_graphql_query(
        mock_request.mock_calls[2].kwargs['query'],
        get_datasets_query
    )

    assert mock_request.mock_calls[2].kwargs['variables'] == {
        'publication': None,
        'model': None,
        'id': dataset_id
    }


@pytest.mark.parametrize('publication', [True, False])
@pytest.mark.parametrize('model', [True, False])
@pytest.mark.parametrize('_id', [True, False])
def test_get_datasets(
    setup_gwl_request,
    query_dataset_return,
    mock_dataset_data,
    get_datasets_query,
    publication,
    model,
    _id
):
    gwl, mock_request = setup_gwl_request

    dataset_data = mock_dataset_data(gwl, i=1)
    dataset_data['_id'] = 'mock_dataset_id1'

    input_pairs = [('publication', publication), ('model', model), ('_id', _id)]
    inputs = {key: dataset_data[key] for key, val in input_pairs if val}

    dataset_id = dataset_data.pop('_id')

    if _id and len(inputs) > 1:
        with pytest.raises(SyntaxError):
            gwl.get_datasets(**inputs)
        return

    mock_request.return_value = query_dataset_return(1)

    datasets = gwl.get_datasets(**inputs)
    assert len(datasets) == 1

    dataset = datasets[0]

    assert dataset.id == dataset_id
    for key, val in dataset_data.items():
        assert getattr(dataset, key) == val

    assert compare_graphql_query(
        mock_request.mock_calls[0].kwargs['query'],
        get_datasets_query
    )

    assert mock_request.mock_calls[0].kwargs['variables'] == {
        'publication': inputs['publication'].id if 'publication' in inputs else None,
        'model': inputs['model'].id if 'model' in inputs else None,
        'id': inputs.get('_id', None),
    }


def test_gwlandscape_files_by_dataset(
    setup_gwl_request,
    query_dataset_files_return,
    mock_dataset_file_data,
    create_dataset
):
    gwl, mr = setup_gwl_request

    mr.return_value = query_dataset_files_return(n_files=3)

    dataset = create_dataset(gwl)

    file_list = gwl._get_files_by_dataset(dataset)

    for i, ref in enumerate(file_list):
        assert ref == FileReference(
            **mock_dataset_file_data(i+1),
            parent=dataset
        )


def test_gwlandscape_get_files_by_reference(
    setup_gwl_request,
    setup_mock_download_fns,
    create_dataset,
    create_dataset_files
):
    gwl, _ = setup_gwl_request
    test_dataset = create_dataset(gwl)

    mock_download_files, mock_get_fn, _ = setup_mock_download_fns(test_dataset)

    test_files = create_dataset_files(test_dataset, n_files=3)

    files = gwl.get_files_by_reference(test_files)

    assert [f[0] for f in files] == test_files.get_paths()

    mock_download_files.assert_called_once_with(
        mock_get_fn,
        test_files
    )


def test_gwlandscape_save_files_by_reference(
    setup_gwl_request,
    setup_mock_download_fns,
    create_dataset,
    create_dataset_files
):
    gwl, _ = setup_gwl_request
    test_dataset = create_dataset(gwl)

    mock_download_files, _, mock_save_fn = setup_mock_download_fns(test_dataset)

    mock_root_path = 'test_dir'

    test_files = create_dataset_files(test_dataset, n_files=3)

    gwl.save_files_by_reference(test_files, mock_root_path)

    mock_download_files.assert_called_once_with(
        mock_save_fn,
        test_files,
        mock_root_path
    )
