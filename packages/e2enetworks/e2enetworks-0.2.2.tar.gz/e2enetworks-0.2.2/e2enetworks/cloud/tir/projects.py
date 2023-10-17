import requests

from typing import Optional
from e2enetworks.constants import BASE_GPU_URL
from e2enetworks.cloud.tir import client
from e2enetworks.cloud.tir.utils import prepare_object


class Projects:
    def __init__(
            self,
            team: Optional[str] = ""
    ):
        client_not_ready = (
            "Client is not ready. Please initiate client by:"
            "\n- Using e2enetworks.cloud.tir.init(...)"
        )
        if not client.Default.ready():
            raise ValueError(client_not_ready)

        if team:
            client.Default.set_team(team)

    def create(self, project_name):
        payload = {
            "project_name": project_name,
        }
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/"
        req = requests.Request('POST', url, data=payload)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def get(self, project_id):

        if type(project_id) != int:
            raise ValueError(project_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{project_id}/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def list(self):

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete(self, project_id):
        if type(project_id) != int:
            raise ValueError(project_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{project_id}/"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    @staticmethod
    def help():
        print("Projects Class Help")
        print("\t\t===================")
        print("\t\tThis class provides functionalities to interact with projects.")
        print("\t\tAvailable methods:")
        print("\t\t1. __init__(team_id): Initializes a Projects instance with the specified team ID.")
        print("\t\t2. create(project_name): Creates a new project with the provided project name.")
        print("\t\t3. get(project_id): Retrieves information about a specific project using its ID.")
        print("\t\t4. list(): Lists all projects associated with the team.")
        print("\t\t5. delete(project_id): Deletes a project with the given ID.")
        print("\t\t8. help(): Displays this help message.")

        # Example usages
        print("\t\tExample usages:")
        print("\t\tprojects = Projects(123)")
        print("\t\tprojects.create('Project Name')")
        print("\t\tprojects.get(456)")
        print("\t\tprojects.list()")
        print("\t\tprojects.delete(456)")
