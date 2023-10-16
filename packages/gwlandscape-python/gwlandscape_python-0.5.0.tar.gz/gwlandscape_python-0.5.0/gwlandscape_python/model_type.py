from dataclasses import dataclass, field

import gwlandscape_python


@dataclass
class Model:
    client: gwlandscape_python.gwlandscape.GWLandscape = field(compare=False)
    id: str
    name: str
    summary: str
    description: str

    def __repr__(self):
        return f'Model("{self.name}")'

    def update(self, name=None, summary=None, description=None):
        """
        Update this Model in the GWLandscape database

        Parameters
        ----------
        name : str, optional
            The new name, by default None
        summary : str, optional
            The new summary, by default None
        description : str, optional
            The new description, by default None
        """
        inputs = {key: val for key, val in locals().items() if ((val is not None) and (key != 'self'))}

        mutation = """
            mutation UpdateCompasModelMutation($input: UpdateCompasModelMutationInput!) {
                updateCompasModel(input: $input) {
                    result
                }
            }
        """

        params = {
            'input': {
                'id': self.id,
                **inputs
            }
        }

        result = self.client.request(mutation, params)

        if result['update_compas_model']['result']:
            for key, val in inputs.items():
                setattr(self, key, val)

    def delete(self):
        """
        Remove this Model from the GWLandscape database
        """

        mutation = """
            mutation DeleteCompasModelMutation($input: DeleteCompasModelMutationInput!) {
                deleteCompasModel(input: $input) {
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

        assert result['delete_compas_model']['result']
