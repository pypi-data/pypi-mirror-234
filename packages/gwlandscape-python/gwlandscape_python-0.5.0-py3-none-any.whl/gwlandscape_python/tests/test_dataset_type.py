def test_update_dataset(setup_gwl_request, create_dataset, mock_dataset_data):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "update_compas_dataset_model": {
            "result": True
        }
    }

    dataset = create_dataset(client=gwl, i=1)
    updated_data = mock_dataset_data(gwl, i=2)

    dataset.update(**updated_data)

    mock_request.assert_called_with(
        """
            mutation UpdateCompasDatasetModelMutation($input: UpdateCompasDatasetModelMutationInput!) {
                updateCompasDatasetModel(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': dataset.id,
                'compas_publication': updated_data['publication'].id,
                'compas_model': updated_data['model'].id,
            }
        }
    )

    for key, val in updated_data.items():
        assert getattr(dataset, key) == val


def test_update_dataset_failure(setup_gwl_request, create_dataset, mock_dataset_data):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "update_compas_dataset_model": {
            "result": False
        }
    }

    dataset = create_dataset(client=gwl, i=1)
    initial_data = mock_dataset_data(gwl, i=1)
    updated_data = mock_dataset_data(gwl, i=2)

    dataset.update(**updated_data)

    mock_request.assert_called_with(
        """
            mutation UpdateCompasDatasetModelMutation($input: UpdateCompasDatasetModelMutationInput!) {
                updateCompasDatasetModel(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': dataset.id,
                'compas_publication': updated_data['publication'].id,
                'compas_model': updated_data['model'].id,
            }
        }
    )

    for key, val in initial_data.items():
        assert getattr(dataset, key) == val


def test_delete_dataset(setup_gwl_request, create_dataset):
    gwl, mock_request = setup_gwl_request

    mock_request.return_value = {
        "delete_compas_dataset_model": {
            "result": True
        }
    }

    dataset = create_dataset(client=gwl)

    dataset.delete()

    mock_request.assert_called_with(
        """
            mutation DeleteCompasDatasetModelMutation($input: DeleteCompasDatasetModelMutationInput!) {
                deleteCompasDatasetModel(input: $input) {
                    result
                }
            }
        """,
        {
            'input': {
                'id': dataset.id
            }
        }
    )
