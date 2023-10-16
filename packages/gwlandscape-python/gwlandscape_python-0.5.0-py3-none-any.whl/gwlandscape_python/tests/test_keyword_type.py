def test_update_keyword(setup_gwl_request, create_keyword, mock_keyword_data):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "update_keyword": {
            "result": True
        }
    }

    keyword = create_keyword(client=gwl, i=1)
    updated_data = mock_keyword_data(i=2)

    keyword.update(**updated_data)

    mock_request.assert_called_with(
        """
            mutation UpdateKeywordMutation($input: UpdateKeywordMutationInput!) {
                updateKeyword(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': keyword.id,
                **updated_data
            }
        }
    )

    assert keyword.tag == updated_data['tag']


def test_update_keyword_failure(setup_gwl_request, create_keyword, mock_keyword_data):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "update_keyword": {
            "result": False
        }
    }

    keyword = create_keyword(client=gwl, i=1)
    original_data = mock_keyword_data(i=1)
    updated_data = mock_keyword_data(i=2)

    keyword.update(**updated_data)

    mock_request.assert_called_with(
        """
            mutation UpdateKeywordMutation($input: UpdateKeywordMutationInput!) {
                updateKeyword(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': keyword.id,
                **updated_data
            }
        }
    )

    assert keyword.tag == original_data['tag']


def test_delete_keyword(setup_gwl_request, create_keyword):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "delete_keyword": {
            "result": True
        }
    }

    keyword = create_keyword(client=gwl, )

    keyword.delete()

    mock_request.assert_called_with(
        """
            mutation DeleteKeywordMutation($input: DeleteKeywordMutationInput!) {
                deleteKeyword(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': keyword.id
            }
        }
    )
