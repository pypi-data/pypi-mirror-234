import json

import requests

from typing import Optional
from e2enetworks.constants import BASE_GPU_URL, INSTANCE_TYPE, headers
from e2enetworks.cloud.tir import client
from e2enetworks.cloud.tir.utils import prepare_object


class Notebooks:
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

    def create(self, name, sku_id, image_id, instance_type, disk_size_in_gb=30, notebook_type="new", notebook_url=""):
        payload = json.dumps({
            "name": name,
            "image_id": image_id,
            "sku_id": sku_id,
            "auto_shutdown_timeout": None,
            "instance_type": instance_type,
            "dataset_id_list": [],
            "disk_size_in_gb": disk_size_in_gb,
            "notebook_type": notebook_type,
            "notebook_url": notebook_url
        })
        headers['Authorization'] = f'Bearer {client.Default.access_token()}'
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/?" \
              f"apikey={client.Default.api_key()}"
        response = requests.post(url=url, headers=headers, data=payload)
        return prepare_object(response)

    def get(self, notebook_id):

        if type(notebook_id) != int:
            raise ValueError(notebook_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/" \
              f"{notebook_id}/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def list(self):

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete(self, notebook_id):
        if type(notebook_id) != int:
            raise ValueError(notebook_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/" \
              f"{notebook_id}/"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def stop(self, notebook_id):
        if type(notebook_id) != int:
            raise ValueError(notebook_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/" \
              f"{notebook_id}/actions/?action=stop&"
        req = requests.Request('PUT', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def start(self, notebook_id):
        if type(notebook_id) != int:
            raise ValueError(notebook_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/" \
              f"{notebook_id}/actions/?action=start&"
        req = requests.Request('PUT', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def upgrade(self, notebook_id, size):
        if type(notebook_id) != int:
            raise ValueError(notebook_id)

        if type(size) != int:
            raise ValueError(notebook_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/notebooks/" \
              f"{notebook_id}/pvc/upgrade/"
        req = requests.Request('PUT', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    @staticmethod
    def help():
        print("\t\tNotebook Class Help")
        print("\t\t=================")
        help_text = f"""
                Notebooks class provides methods to interact with notebooks in a project.

                Available methods:
                1. create(name, sku_id, image_id, instance_type, disk_size_in_gb=30, notebook_type="new",
                 notebook_url=""): Create a new notebook.
                2. get(notebook_id): Get information about a notebook.
                3. list(): List all notebooks in the project.
                4. delete(notebook_id): Delete a notebook.
                5. stop(notebook_id): Stop a running notebook.
                6. start(notebook_id): Start a stopped notebook.
                7. upgrade(notebook_id, size): Upgrade the size of a notebook's PVC.

                Usage:
                notebooks = Notebooks(team_id, project_id)
                notebooks.create(name, sku_id, image_id, instance_type={INSTANCE_TYPE}, disk_size_in_gb=30,
                 notebook_type="new", notebook_url="")
                notebooks.get(notebook_id)
                notebooks.list()
                notebooks.delete(notebook_id)
                notebooks.stop(notebook_id)
                notebooks.start(notebook_id)
                notebooks.upgrade(notebook_id, size)
                """
        print(help_text)
