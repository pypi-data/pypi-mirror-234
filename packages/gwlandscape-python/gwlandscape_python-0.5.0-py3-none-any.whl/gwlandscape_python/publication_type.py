from dataclasses import dataclass, field

import gwlandscape_python


@dataclass
class Publication:
    client: gwlandscape_python.gwlandscape.GWLandscape = field(compare=False)
    id: str
    author: str
    published: bool
    title: str
    year: int
    journal: str
    journal_doi: str
    dataset_doi: str
    description: str
    public: bool
    download_link: str
    arxiv_id: str
    creation_time: str
    keywords: list

    def __repr__(self):
        return f'Publication("{self.title}")'

    def update(
        self,
        author=None,
        title=None,
        arxiv_id=None,
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
        Update this Publication in the GWLandscape database

        Parameters
        ----------
        author : str, optional
            The author of the publication, by default None
        title : str, optional
            The title of the publication, by default None
        arxiv_id : str, optional
            The arxiv id of the publication, by default None
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
            Updated Publication
        """
        inputs = {key: val for key, val in locals().items() if ((val is not None) and (key != 'self'))}

        mutation = """
            mutation UpdatePublicationMutation($input: UpdatePublicationMutationInput!) {
                updatePublication(input: $input) {
                    result
                }
            }
        """

        # Handle keywords
        if keywords:
            keywords = [
                self.client.get_keywords(exact=keyword)[0] if isinstance(keyword, str) else keyword
                for keyword in keywords
            ]
            inputs['keywords'] = [keyword.id for keyword in keywords]

        params = {
            'input': {
                'id': self.id,
                **inputs
            }
        }

        result = self.client.request(mutation, params)

        if result['update_publication']['result']:
            for key, val in inputs.items():
                setattr(self, key, val)

            if keywords:
                self.keywords = keywords

    def delete(self):
        """
        Remove this Publication from the GWLandscape database
        """

        mutation = """
            mutation DeletePublicationMutation($input: DeletePublicationMutationInput!) {
                deletePublication(input: $input) {
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

        assert result['delete_publication']['result']
