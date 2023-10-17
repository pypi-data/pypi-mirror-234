=====================================
Mind Foundry Analyze — Python Client
=====================================

Mind Foundry Analyze is a Data Science workbench developed by Mind Foundry.

This Python client makes it easier to interact with the API and integrate with other Python libraries.

Quick start::

    from mindfoundry.client.analyze import create_project_api_client

    client = create_project_api_client(YOUR_INSTANCE_URL, YOUR_CLIENT_ID, YOUR_CLIENT_SECRET)
    with open('./your-training-data.csv', 'rb') as data:
        data_set_id = client.create_file_data_set(data, 'Your Data Set Name', 'Your description')

    model_id = client.create_classification_model('Your Model Name', data_set_id, 'Target Column')

    with open('./your-prediction-data.csv', 'rb') as other_data:
        other_data_set_id = client.create_file_data_set(other_data, 'Prediction Data')

    prediction_id = client.create_prediction(model_id, other_data_set_id, 'Your Prediction Name')

    client.download_prediction_as_csv(prediction_id, './your-output-file.csv')


You can also create a data set from a Pandas DataFrame, or an array of dicts, or an array of arrays::

    data_dicts = [{'a': 1, 'b': 2}, {'a': 3}, {'b': 4}]
    client.create_file_data_set(data_dicts, 'Array of dicts')

    df = pd.DataFrame(data_dicts)
    client.create_file_data_set(df, 'Pandas DataFrame')

    data_arrays = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    client.create_file_data_set(data_arrays, 'Array of arrays')

