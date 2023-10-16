from gwdc_python.objects.base import GWDCObjectBase
from gwdc_python.files.constants import GWDCObjectType

from gwlandscape_python.utils import file_filters


class Dataset(GWDCObjectBase):
    """
    Dataset class is useful for interacting with the Datasets returned from a call to the GWCloud API.
    It is primarily used to update the parameters and obtain files related to the dataset.

    Parameters
    ----------
    client : ~gwlandscape_python.gwlandscape.GWLandscape
        A reference to the GWLandscape object instance from which the Dataset was created
    dataset_id : str
        The id of the Dataset, required to obtain the files associated with it
    publication : ~gwlandscape_python.publication_type.Publication
        The publication with which the dataset is associated
    model : ~gwlandscape_python.model_type.Model
        The model with which the dataset is associated
    """
    FILE_LIST_FILTERS = {
        'data': file_filters.data_filter
    }

    def __init__(self, client, dataset_id, publication, model):
        super().__init__(client, dataset_id, GWDCObjectType.UPLOADED)
        self.publication = publication
        self.model = model

    def __repr__(self):
        return f'Dataset({self.publication} - {self.model})'

    def update(self, publication=None, model=None):
        """
        Update a Dataset in the GWLandscape database

        Parameters
        ----------
        publication : Publication, optional
            The new Publication, by default None
        model : Model, optional
            The new Model, by default None

        Returns
        -------
        Dataset
            Updated Dataset
        """
        inputs = {key: val for key, val in locals().items() if ((val is not None) and (key != 'self'))}

        mutation = """
            mutation UpdateCompasDatasetModelMutation($input: UpdateCompasDatasetModelMutationInput!) {
                updateCompasDatasetModel(input: $input) {
                    result
                }
            }
        """

        params = {
            'input': {
                'id': self.id,
                **{f'compas_{key}': val.id for key, val in inputs.items()}
            }
        }

        result = self.client.request(mutation, params)

        if result['update_compas_dataset_model']['result']:
            for key, val in inputs.items():
                setattr(self, key, val)

    def delete(self):
        """
        Remove this Dataset from the GWLandscape database
        """

        mutation = """
            mutation DeleteCompasDatasetModelMutation($input: DeleteCompasDatasetModelMutationInput!) {
                deleteCompasDatasetModel(input: $input) {
                    result
                }
            }
        """

        params = {
            'input': {
                'id': self.id
            }
        }

        result = self.client.request(mutation, params)

        assert result['delete_compas_dataset_model']['result']
