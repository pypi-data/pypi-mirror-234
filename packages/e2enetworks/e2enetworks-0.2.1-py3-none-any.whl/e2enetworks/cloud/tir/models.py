import json

import requests

from typing import Optional
from e2enetworks.constants import BASE_GPU_URL, BUCKET_TYPES, MODEL_TYPES, headers
from e2enetworks.cloud.tir import client
from e2enetworks.cloud.tir.utils import prepare_object


class Models:
    def __init__(
            self,
            project: Optional[str] = "",
            team: Optional[str] = ""
    ):
        client_not_ready = (
            "Client is not ready. Please initiate client by:"
            "\n- Using e2enetworks.cloud.tir.init(...)"
        )
        if not client.Default.ready():
            raise ValueError(client_not_ready)

        if project:
            client.Default.set_project(project)

        if team:
            client.Default.set_team(team)

    def create(self, name, model_type, bucket_name, storage_type):
        payload = json.dumps({
            "name": name,
            "model_type": model_type,
            "bucket_name": bucket_name,
            "storage_type": storage_type
        })
        headers['Authorization'] = f'Bearer {client.Default.access_token()}'
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/model/?" \
              f"apikey={client.Default.api_key()}"
        response = requests.post(url=url, headers=headers, data=payload)
        return prepare_object(response)

    def get(self, model_id):

        if type(model_id) != int:
            raise ValueError(model_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/model/" \
              f"{model_id}/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def list(self):

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/model/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete(self, model_id):
        if type(model_id) != int:
            raise ValueError(model_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/model/" \
              f"{model_id}/"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    @staticmethod
    def help():
        print("Models Class Help")
        print("\t\t=================")
        print("\t\tThis class provides functionalities to interact with models.")
        print("\t\tAvailable methods:")
        print(
            "\t\t1. __init__(team_id, project_id): Initializes a Models instance with the specified team and project "
            "IDs.")
        print("\t\t2. create(name, storage_type, bucket_name, model_type): Creates a new model with the provided "
              "details.")
        print("\t\t3. get(model_id): Retrieves information about a specific model using its ID.")
        print("\t\t4. list(): Lists all models associated with the team and project.")
        print("\t\t5. delete(model_id): Deletes a model with the given ID.")
        print("\t\t6. clear_values(): Resets the team and project IDs to None.")
        print("\t\t7. validate(): Checks if the team and project IDs are of integer type.")
        print("\t\t8. help(): Displays this help message.")

        # Example usages
        print("\t\tExample usages:")
        print("\t\tmodels = Models(123, 456)")
        print(f"\t\tmodels.create(name='Test Dataset', bucket_name='dataset-bucket', storage_type={BUCKET_TYPES},"
              f" model_type={MODEL_TYPES})")
        print("\t\tmodels.get(789)")
        print("\t\tmodels.list()")
        print("\t\tmodels.delete(789)")