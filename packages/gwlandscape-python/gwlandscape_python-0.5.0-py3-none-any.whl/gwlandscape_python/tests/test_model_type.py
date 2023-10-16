def test_update_model(setup_gwl_request, create_model, mock_model_data):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "update_compas_model": {
            "result": True
        }
    }

    model = create_model(gwl, i=1)
    updated_data = mock_model_data(i=2)

    model.update(**updated_data)

    mock_request.assert_called_with(
        """
            mutation UpdateCompasModelMutation($input: UpdateCompasModelMutationInput!) {
                updateCompasModel(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': model.id,
                **updated_data
            }
        }
    )

    for key, val in updated_data.items():
        assert getattr(model, key) == val


def test_update_model_failure(setup_gwl_request, create_model, mock_model_data):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "update_compas_model": {
            "result": False
        }
    }

    model = create_model(gwl, i=1)
    initial_data = mock_model_data(i=1)
    updated_data = mock_model_data(i=2)

    model.update(**updated_data)

    mock_request.assert_called_with(
        """
            mutation UpdateCompasModelMutation($input: UpdateCompasModelMutationInput!) {
                updateCompasModel(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': model.id,
                **updated_data
            }
        }
    )

    for key, val in initial_data.items():
        assert getattr(model, key) == val


def test_delete_model(setup_gwl_request, create_model):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "delete_compas_model": {
            "result": True
        }
    }

    model = create_model(gwl)

    model.delete()

    mock_request.assert_called_with(
        """
            mutation DeleteCompasModelMutation($input: DeleteCompasModelMutationInput!) {
                deleteCompasModel(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': model.id
            }
        }
    )
