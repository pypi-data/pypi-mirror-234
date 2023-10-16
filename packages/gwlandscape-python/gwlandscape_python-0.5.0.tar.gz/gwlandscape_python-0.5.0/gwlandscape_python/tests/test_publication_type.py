from gwlandscape_python.tests.utils import compare_graphql_query


def test_update_publication_success(setup_gwl_request, create_publication, mock_publication_data):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "update_publication": {
            "result": True
        }
    }

    publication = create_publication(gwl, i=1)
    updated_data = mock_publication_data(i=2)

    publication.update(**updated_data)

    mock_request.assert_called_with(
        """
            mutation UpdatePublicationMutation($input: UpdatePublicationMutationInput!) {
                updatePublication(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': publication.id,
                **updated_data
            }
        }
    )

    for key, val in updated_data.items():
        assert getattr(publication, key) == val


def test_update_publication_string_keywords(
    setup_gwl_request,
    create_publication,
    create_keyword,
    query_keyword_return
):
    gwl, mock_request = setup_gwl_request

    mock_request.side_effect = [
        *[query_keyword_return(1, start_id=i) for i in range(100, 103)],
        {
            "update_publication": {
                "result": True
            }
        }
    ]

    publication = create_publication(gwl)
    new_keywords = [create_keyword(gwl, i=i) for i in range(100, 103)]

    publication.update(keywords=[keyword.tag for keyword in new_keywords])

    for i, j in enumerate(range(100, 103)):
        assert compare_graphql_query(
            mock_request.mock_calls[i].kwargs['query'],
            """
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
        )

        assert mock_request.mock_calls[i].kwargs['variables'] == {
            'exact': f'mock tag {j}',
            'contains': None,
            'id': None
        }

    assert compare_graphql_query(
        mock_request.mock_calls[3].args[0],
        """
            mutation UpdatePublicationMutation($input: UpdatePublicationMutationInput!) {
                updatePublication(input: $input) {
                    result
                }
            }
        """
    )

    assert mock_request.mock_calls[3].args[1] == {
        'input': {
            'id': publication.id,
            'keywords': [keyword.id for keyword in new_keywords]
        }
    }


def test_update_publication_failure(setup_gwl_request, create_publication, mock_publication_data):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "update_publication": {
            "result": False
        }
    }

    publication = create_publication(gwl, i=1)
    initial_data = mock_publication_data(i=1)
    updated_data = mock_publication_data(i=2)

    publication.update(**updated_data)

    for key, val in initial_data.items():
        assert getattr(publication, key) == val


def test_delete_publication(setup_gwl_request, create_publication):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "delete_publication": {
            "result": True
        }
    }

    publication = create_publication(gwl, i=1)

    publication.delete()

    mock_request.assert_called_with(
        """
            mutation DeletePublicationMutation($input: DeletePublicationMutationInput!) {
                deletePublication(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': publication.id
            }
        }
    )
