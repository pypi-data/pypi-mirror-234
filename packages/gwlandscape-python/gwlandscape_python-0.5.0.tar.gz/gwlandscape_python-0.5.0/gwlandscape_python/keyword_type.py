from dataclasses import dataclass, field

import gwlandscape_python


@dataclass
class Keyword:
    client: gwlandscape_python.gwlandscape.GWLandscape = field(compare=False)
    id: str
    tag: str

    def __repr__(self):
        return f'Keyword("{self.tag}")'

    def update(self, tag=None):
        """
        Update this Keyword in the GWLandscape database

        Parameters
        ----------
        tag : str, optional
            The new tag, by default None

        Returns
        -------
        Keyword
            Updated Keyword
        """

        mutation = """
            mutation UpdateKeywordMutation($input: UpdateKeywordMutationInput!) {
                updateKeyword(input: $input) {
                    result
                }
            }
        """

        params = {
            'input': {
                'id': self.id,
                'tag': tag
            }
        }

        result = self.client.request(mutation, params)

        if result['update_keyword']['result']:
            self.tag = tag if tag is not None else self.tag

    def delete(self):
        """
        Remove this Keyword from the GWLandscape database
        """

        mutation = """
            mutation DeleteKeywordMutation($input: DeleteKeywordMutationInput!) {
                deleteKeyword(input: $input) {
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

        assert result['delete_keyword']['result']
