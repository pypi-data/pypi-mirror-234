import json

import requests

from typing import Optional
from e2enetworks.constants import BASE_GPU_URL, BUCKET_TYPES, headers
from e2enetworks.cloud.tir import client
from e2enetworks.cloud.tir.utils import prepare_object


class Datasets:
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

    def create(self, name=None, bucket_name=None, bucket_type=None, description=""):
        payload = json.dumps({
            "type": bucket_type,
            "name": name,
            "bucket_name": bucket_name,
            "description": description,
        })
        headers['Authorization'] = f'Bearer {client.Default.access_token()}'
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/datasets/?" \
              f"apikey={client.Default.api_key()}"
        response = requests.post(url=url, headers=headers, data=payload)
        return prepare_object(response)

    def get(self, dataset_id):

        if type(dataset_id) != int:
            raise ValueError(dataset_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/datasets/" \
              f"{dataset_id}/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def list(self):

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/datasets/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete(self, dataset_id):
        if type(dataset_id) != int:
            raise ValueError(dataset_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/datasets/" \
              f"{dataset_id}/"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    @staticmethod
    def help():
        print("Datasets Class Help")
        print("\t\t=================")
        print("\t\tThis class provides functionalities to interact with Datasets.")
        print("\t\tAvailable methods:")
        print(
            "\t\t1. __init__(team_id, project_id): Initializes a Datasets instance with the specified team and "
            "project IDs.")
        print(f"\t\t2. create(name, bucket_name=, bucket_type, description): Creates a new dataset with the provided"
              f"name, bucket name, bucket type and description\n Bucket Name is not required in case of"
              f" bucket_type='managed'")
        print("\t\t3. get(bucket_name): Retrieves information about a specific dataset using its bucket name.")
        print("\t\t4. list(): Lists all datasets associated with the team and project.")
        print("\t\t5. delete(bucket_name): Deletes a dataset with the given bucket name.")
        print("\t\t6. clear_values(): Resets the team and project IDs to None.")
        print("\t\t7. validate(): Checks if the team and project IDs are of integer type.")
        print("\t\t8. help(): Displays this help message.")

        # Example usages
        print("\t\tExample usages:")
        print("\t\tdatasets = Datasets(123, 456)")
        print(f"\t\tdatasets.create(name='Test Dataset', bucket_name='dataset-bucket', bucket_type={BUCKET_TYPES},"
              f" description='Test Dataset')")
        print("\t\tdatasets.get('Bucket Name')")
        print("\t\tdatasets.list()")
        print("\t\tdatasets.delete('Bucket Name')")