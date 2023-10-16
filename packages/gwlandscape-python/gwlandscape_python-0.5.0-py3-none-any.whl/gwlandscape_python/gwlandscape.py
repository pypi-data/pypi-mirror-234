from pathlib import Path

from gwdc_python import GWDC
from gwdc_python.files import FileReference, FileReferenceList
from gwdc_python.logger import create_logger

import gwlandscape_python
from gwlandscape_python.utils import mutually_exclusive, validate_dataset
from gwlandscape_python.utils.file_download import _download_files, _get_file_map_fn, _save_file_map_fn
from gwlandscape_python.settings import GWLANDSCAPE_ENDPOINT, GWLANDSCAPE_AUTH_ENDPOINT

logger = create_logger(__name__)


class GWLandscape:
    """
    GWLandscape class provides an API for interacting with COMPAS, allowing jobs to be submitted and acquired.

    Parameters
    ----------
    token : str
        API token for a GWDC user
    endpoint : str, optional
        URL to which we send the queries, by default GWLANDSCAPE_ENDPOINT

    Attributes
    ----------
    client : GWDC
        Handles a lot of the underlying logic surrounding the queries
    """

    def __init__(self, token="", auth_endpoint=GWLANDSCAPE_AUTH_ENDPOINT, endpoint=GWLANDSCAPE_ENDPOINT):
        self.client = GWDC(
            token=token,
            auth_endpoint=auth_endpoint,
            endpoint=endpoint,
        )

        self.request = self.client.request  # Setting shorthand for simplicity

    def create_keyword(self, tag):
        """
        Creates a new keyword object with the specified tag.

        Parameters
        ----------
        tag : str
            The tag of the keyword to be created

        Returns
        -------
        Keyword
            Created Keyword
        """
        mutation = """
            mutation AddKeywordMutation($input: AddKeywordMutationInput!) {
                addKeyword(input: $input) {
                    id
                }
            }
        """

        params = {
            'input': {
                'tag': tag
            }
        }

        result = self.request(mutation, params)

        assert 'id' in result['add_keyword']

        return self.get_keywords(_id=result['add_keyword']['id'])[0]

    @mutually_exclusive('exact', 'contains', '_id')
    def get_keywords(self, exact=None, contains=None, _id=None):
        """
        Fetch all keywords matching exactly the provided parameter, any keywords with tags containing the term in
        the contains parameter, or the keyword with the specified id.

        At most, only one of exact, contains, or _id must be provided. If neither the exact, contains, or _id
        parameter is supplied, then all keywords are returned.

        Parameters
        ----------
        exact : str, optional
            Match keywords with this exact tag (case-insensitive), by default None
        contains : str, optional
            Match keywords containing this text (case-insensitive)), by default None
        _id : str, optional
            Match keyword by the provided ID, by default None

        Returns
        -------
        list
            A list of :class:`.Keyword` instances
        """

        query = """
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

        variables = {
            'exact': exact,
            'contains': contains,
            'id': _id
        }

        result = self.request(query=query, variables=variables)

        return [
            gwlandscape_python.Keyword(client=self, **kw['node'])
            for kw in result['keywords']['edges']
        ]

    def create_publication(
        self,
        author,
        title,
        arxiv_id,
        published=None,
        year=None,
        journal=None,
        journal_doi=None,
        dataset_doi=None,
        description=None,
        public=None,
        download_link=None,
        keywords=None
    ):
        """
        Creates a new keyword object with the specified tag.

        Parameters
        ----------
        author : str
            The author of the publication
        title : str
            The title of the publication
        arxiv_id : str
            The arxiv id of the publication
        published : bool, optional
            If the publication was published in a journal/arXiv, by default None
        year : int, optional
            The year of the publication, by default None
        journal : str, optional
            The name of the journal, by default None
        journal_doi : str, optional
            The DOI of the publication, by default None
        dataset_doi : str, optional
            The DOI of the dataset, by default None
        description : str, optional
            A description of the publication, by default None
        public : bool, optional
            If the publication has been made public (visible to the public), by default None
        download_link : str, optional
            A link to download the publication/dataset, by default None
        keywords : list, optional
            A list of str or :class:`~.Keyword` objects for the publication, by default None

        Returns
        -------
        Publication
            Created Publication
        """
        inputs = {key: val for key, val in locals().items() if ((val is not None) and (key != 'self'))}

        mutation = """
            mutation AddPublicationMutation($input: AddPublicationMutationInput!) {
                addPublication(input: $input) {
                    id
                }
            }
        """

        # Handle keywords
        if isinstance(keywords, list):
            inputs['keywords'] = [
                self.get_keywords(exact=keyword)[0].id if isinstance(keyword, str) else keyword.id
                for keyword in keywords
            ]
            inputs['keywords'] = [keyword.id for keyword in keywords]

        params = {
            'input': {
                **inputs
            }
        }

        result = self.request(mutation, params)

        assert 'id' in result['add_publication']

        return self.get_publications(_id=result['add_publication']['id'])[0]

    @mutually_exclusive('author | title', '_id')
    def get_publications(self, author=None, title=None, _id=None):
        """
        Fetch all publications with author/title/arxiv id containing the values specified.
        Also allows fetching publication by the provided ID

        At most, only one of (author, title) or _id must be provided. If no parameter is provided, all
        publications are returned.

        Parameters
        ----------
        author : str, optional
            Match publication author contains this value (case-insensitive), by default None
        title : str, optional
            Match publication arxiv id exactly equals this value (case-insensitive), by default None
        _id : str, optional
            Match publication by the provided ID, by default None

        Returns
        -------
        list
            A list of :class:`.Publication` instances
        """

        query = """
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

        variables = {
            'author': author,
            'title': title,
            'id': _id
        }

        result = self.request(query=query, variables=variables)

        # Handle keywords
        for pub in result['compas_publications']['edges']:
            pub['node']['keywords'] = [
                gwlandscape_python.Keyword(client=self, **kw['node']) for kw in pub['node']['keywords']['edges']
            ]

        return [
            gwlandscape_python.Publication(client=self, **kw['node'])
            for kw in result['compas_publications']['edges']
        ]

    def create_model(self, name, summary=None, description=None):
        """
        Creates a new model object with the specified parameters.

        Parameters
        ----------
        name : str
            The name of the model to be created
        summary : str, optional
            The summary of the model to be created, by default None
        description : str, optional
            The description of the model to be created, by default None

        Returns
        -------
        Model
            Created Model
        """
        inputs = {key: val for key, val in locals().items() if ((val is not None) and (key != 'self'))}

        mutation = """
            mutation AddCompasModelMutation($input: AddCompasModelMutationInput!) {
                addCompasModel(input: $input) {
                    id
                }
            }
        """

        params = {
            'input': {
                **inputs
            }
        }

        result = self.request(mutation, params)

        assert 'id' in result['add_compas_model']

        return self.get_models(_id=result['add_compas_model']['id'])[0]

    @mutually_exclusive('name | summary | description', '_id')
    def get_models(self, name=None, summary=None, description=None, _id=None):
        """
        Fetch all models with name/summary/description containing the values specified.
        Also allows fetching models by the provided ID

        At most, only one of (name, summary, description) or _id must be provided. If no parameter is provided, all
        models are returned.

        Parameters
        ----------
        name : str, optional
            Match model name containing this value (case-insensitive), by default None
        summary : str, optional
            Match model summary contains this value (case-insensitive), by default None
        description : str, optional
            Match model description contains this value (case-insensitive), by default None
        _id : str, optional
            Match model by the provided ID, by default None

        Returns
        -------
        list
            A list of :class:`.Model` instances
        """

        query = """
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

        variables = {
            'name': name,
            'summary': summary,
            'description': description,
            'id': _id
        }

        result = self.request(query=query, variables=variables)

        return [
            gwlandscape_python.Model(client=self, **kw['node'])
            for kw in result['compas_models']['edges']
        ]

    def create_dataset(self, publication, model, datafile):
        """
        Creates a new dataset object with the specified publication and model.
        Datasets must contain exactly one hdf5 file, and should either be a hdf5 file
        or a tarfile containing the hdf5 file.

        Parameters
        ----------
        publication : Publication
            The Publication this dataset is for
        model : Model
            The model this dataset is for
        datafile : str or Path
            Local path to the COMPAS h5 file or tarfile

        Returns
        -------
        Dataset
            Created Dataset
        """
        query = """
            mutation UploadCompasDatasetModelMutation($input: UploadCompasDatasetModelMutationInput!) {
                uploadCompasDatasetModel(input: $input) {
                    id
                }
            }
        """
        file_path = Path(datafile)
        validate_dataset(file_path)

        with Path(datafile).open('rb') as f:
            variables = {
                'input': {
                    "uploadToken": self._generate_compas_dataset_model_upload_token(),
                    'compas_publication': publication.id,
                    'compas_model': model.id,
                    'jobFile': f
                }
            }

            result = self.request(query=query, variables=variables, authorize=False)

        assert 'id' in result['upload_compas_dataset_model']

        return self.get_datasets(_id=result['upload_compas_dataset_model']['id'])[0]

    @mutually_exclusive('publication | model', '_id')
    def get_datasets(self, publication=None, model=None, _id=None):
        """
        Fetch all dataset models with publication/model matching the provided parameters.
        Also allows fetching models by the provided ID

        At most, only one of (publication, model) or _id must be provided. If no parameter is provided, all
        dataset models are returned.

        Parameters
        ----------
        publication : Publication, optional
            Match all dataset models with this publication, by default None
        model : Model, optional
            Match all dataset models with this publication, by default None
        _id : str, optional
            Match model by the provided ID, by default None

        Returns
        -------
        list
            A list of Dataset instances
        """

        query = """
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

        variables = {
            'publication': publication.id if publication else None,
            'model': model.id if model else None,
            'id': _id
        }

        result = self.request(query=query, variables=variables)

        # Handle publication and model objects
        for dataset in result['compas_dataset_models']['edges']:
            # Handle publication keywords
            dataset['node']['compas_publication']['keywords'] = [
                gwlandscape_python.Keyword(client=self, **kw['node'])
                for kw in dataset['node']['compas_publication']['keywords']['edges']
            ]

            dataset['node']['publication'] = gwlandscape_python.Publication(
                client=self,
                **dataset['node']['compas_publication']
            )
            dataset['node']['model'] = gwlandscape_python.Model(client=self, **dataset['node']['compas_model'])

            # Delete the compas_ fields - we don't need them anymore
            del dataset['node']['compas_publication']
            del dataset['node']['compas_model']

            dataset['node']['dataset_id'] = dataset['node'].pop('id')

        return [
            gwlandscape_python.dataset_type.Dataset(client=self, **kw['node'])
            for kw in result['compas_dataset_models']['edges']
        ]

    def _generate_compas_dataset_model_upload_token(self):
        """Creates a new long lived upload token for use uploading compas publications

        Returns
        -------
        str
            The upload token
        """
        query = """
            query GenerateCompasDatasetModelUploadToken {
                generateCompasDatasetModelUploadToken {
                  token
                }
            }
        """

        data = self.request(query=query)
        return data['generate_compas_dataset_model_upload_token']['token']

    def _get_files_by_dataset(self, dataset):
        query = """
            query ($id: ID!) {
                compasDatasetModel (id: $id) {
                    files {
                        path
                        fileSize
                        downloadToken
                    }
                }
            }
        """

        variables = {
            "id": dataset.id
        }

        data = self.request(query=query, variables=variables)

        file_list = FileReferenceList()
        for file_data in data['compas_dataset_model']['files']:
            file_list.append(
                FileReference(
                    **file_data,
                    parent=dataset
                ),
            )

        return file_list

    def get_files_by_reference(self, file_references):
        """Obtains file data when provided a :class:`~gwdc_python.files.file_reference.FileReferenceList`

        Parameters
        ----------
        file_references : ~gwdc_python.files.file_reference.FileReferenceList
            Contains the :class:`~gwdc_python.files.file_reference.FileReference` objects for which
            to download the contents

        Returns
        -------
        list
            List of tuples containing the file path and file contents as a byte string
        """
        files = _download_files(_get_file_map_fn, file_references)

        logger.info(f'All {len(file_references)} files downloaded!')

        return files

    def save_files_by_reference(self, file_references, root_path):
        """Save files when provided a :class:`~gwdc_python.files.file_reference.FileReferenceList` and a root path

        Parameters
        ----------
        file_references : ~gwdc_python.files.file_reference.FileReferenceList
            Contains the :class:`~gwdc_python.files.file_reference.FileReference` objects for which
            to save the associated files
        root_path : str or ~pathlib.Path
            Directory into which to save the files
        preserve_directory_structure : bool, optional
            Remove any directory structure for the downloaded files, by default True
        """
        _download_files(_save_file_map_fn, file_references, root_path)

        logger.info(f'All {len(file_references)} files saved!')
