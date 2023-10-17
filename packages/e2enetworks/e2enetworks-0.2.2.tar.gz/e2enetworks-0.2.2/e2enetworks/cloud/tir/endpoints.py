import json

import requests

from typing import Optional
from e2enetworks.constants import BASE_GPU_URL, headers
from e2enetworks.cloud.tir import client
from e2enetworks.cloud.tir.utils import prepare_object


class EndPoints:
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

    def create(self, name, sku_id, prefix, replica, model_id):
        payload = json.dumps({
            "name": name,
            "sku_id": sku_id,
            "prefix": prefix,
            "replica": replica,
            "model_id": model_id
        })
        headers['Authorization'] = f'Bearer {client.Default.access_token()}'
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/inference/?" \
              f"apikey={client.Default.api_key()}"
        response = requests.post(url=url, headers=headers, data=payload)
        return prepare_object(response)

    def get(self, endpoint_id):

        if type(endpoint_id) != int:
            raise ValueError(endpoint_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/inference/" \
              f"{endpoint_id}/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def list(self):

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/inference/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete(self, endpoint_id):
        if type(endpoint_id) != int:
            raise ValueError(endpoint_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/inference/" \
              f"{endpoint_id}/"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    @staticmethod
    def help():
        print("EndPoint Class Help")
        print("\t\t=================")
        print("\t\tThis class provides functionalities to interact with EndPoint.")
        print("\t\tAvailable methods:")
        print("\t\t1. __init__(team_id, project_id): Initializes an EndPoints instance with the specified team and "
              "project IDs.")
        print("\t\t2. create(name, sku_id, prefix, replica, model_id): Creates an endpoint with the provided details.")
        print("\t\t3. get(endpoint_id): Retrieves information about a specific endpoint using its ID.")
        print("\t\t4. list(): Lists all endpoints associated with the team and project.")
        print("\t\t5. delete(endpoint_id): Deletes an endpoint with the given ID.")
        print("\t\t8. help(): Displays this help message.")

        # Example usages
        print("\t\tExample usages:")
        print("\t\tendpoints = EndPoints(123, 456)")
        print("\t\tendpoints.create('Name', sku_id, 'Prefix', replica, model_id)")
        print("\t\tendpoints.get(789)")
        print("\t\tendpoints.list()")
        print("\t\tendpoints.delete(789)")