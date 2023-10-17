import requests 

from typing import Optional, Dict
from e2enetworks.cloud.tir import client, utils
from .utils import prepare_response, prepare_object
from e2enetworks.cloud.tir.constants import ARGUMENT_IS_MANDATORY


class PipelineClient:
    def __init__(
        self,
        project: Optional[str] = None,
    ):  
        client_not_ready = (
            "Client is not ready. Please initiate client by:"
            "\n- Using e2enetworks.cloud.tir.init(...)"
        )
        if not client.Default.ready():
            raise ValueError(client_not_ready)
        
        if project:
            client.Default.set_project(project)

    def create_pipeline(
        self,
        name,
        description,
        file_path,
        page_token: str = '',
        page_size: int = 10,
        sort_by: str = '',
        filter: Optional[str] = None
    ):
        if not name or not file_path:
            raise ValueError(f"name and file {ARGUMENT_IS_MANDATORY}")
        file = open(file_path, 'rb')
        files = [
            ('uploadfile',
             (file.name, file, 'application/octet-stream'))
        ]
        url = f"{client.Default.gpu_projects_path()}/pipelines/upload/?name={name}&description={description}&"
        req = requests.Request('POST', url, files=files)
        response = client.Default.make_request(req)
        return prepare_object(response)
    
    def list_pipelines(
        self,
        page_token: str = '',
        page_size: int = 10,
        sort_by: str = '',
        filter: Optional[str] = None
    ):
        url = "{project_path}/pipelines/".format(project_path=client.Default.gpu_projects_path())
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def get_pipeline(
        self,
        pipeline_id: str = '',
        page_token: str = '',
        page_size: int = 10,
        sort_by: str = '',
        filter: Optional[str] = None
    ):
        if not pipeline_id:
            raise ValueError(f"PIPELINE_ID {ARGUMENT_IS_MANDATORY}")
        url = f"{client.Default.gpu_projects_path()}/pipelines/{pipeline_id}/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete_pipeline(
        self,
        pipeline_id: str = '',
        page_token: str = '',
        page_size: int = 10,
        sort_by: str = '',
        filter: Optional[str] = None
    ):
        if not pipeline_id:
            raise ValueError(f"PIPELINE_ID {ARGUMENT_IS_MANDATORY}")
        url = f"{client.Default.gpu_projects_path()}/pipelines/{pipeline_id}/"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def create_experiment(
        self,
        name: str,
        description: Optional[str] = None,
    ):
        request_params = {
            'name': name,
            'description': description,
        }
        url = "{project_path}/pipelines/experiments/".format(project_path=client.Default.gpu_projects_path())
        req = requests.Request('POST', url, data=request_params)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def list_experiments(
        self,
        page_token: str = '',
        page_size: int = 10,
        sort_by: str = '',
        filter: Optional[str] = None
    ):
        url = "{project_path}/pipelines/experiments/".format(project_path=client.Default.gpu_projects_path())
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def get_experiment(
        self,
        experiment_id: str = '',
        page_token: str = '',
        page_size: int = 10,
        sort_by: str = '',
        filter: Optional[str] = None
    ):
        if not experiment_id:
            raise ValueError(f"EXPERIMENT_ID {ARGUMENT_IS_MANDATORY}")
        url = f"{client.Default.gpu_projects_path()}/pipelines/experiment/{experiment_id}/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete_experiment(
        self,
        experiment_id: str = '',
        page_token: str = '',
        page_size: int = 10,
        sort_by: str = '',
        filter: Optional[str] = None
    ):

        if not experiment_id:
            raise ValueError(f"EXPERIMENT_ID {ARGUMENT_IS_MANDATORY}")

        url = f"{client.Default.gpu_projects_path()}/pipelines/experiment/{experiment_id}/"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def create_run(
        self,
        name: str = '',
        description: str = '',
        experiment_id: str = '',
        pipeline_version_id: str = '',
        service_account: str = '',
        page_token: str = '',
        page_size: int = 10,
        sort_by: str = '',
        filter: Optional[str] = None
    ):
        if not name or not experiment_id or not pipeline_version_id:
            raise ValueError(f"name, experiment_id, pipeline_version_id {ARGUMENT_IS_MANDATORY}")
        payloads = {"name": name,
                    "description": description,
                    "experiment_id": experiment_id,
                    "pipeline_version_id": pipeline_version_id}
        url = "{project_path}/pipelines/runs/".format(project_path=client.Default.gpu_projects_path())
        req = requests.Request(method='POST', url=url, data=payloads)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def list_runs(
        self,
        page_token: str = '',
        page_size: int = 10,
        sort_by: str = '',
        filter: Optional[str] = None
    ):
        url = "{project_path}/pipelines/runs/".format(project_path=client.Default.gpu_projects_path())
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def get_run(
            self,
            run_id: str = '',
            page_token: str = '',
            page_size: int = 10,
            sort_by: str = '',
            filter: Optional[str] = None
    ):
        if not run_id:
            raise ValueError(f"RUN_ID {ARGUMENT_IS_MANDATORY}")
        url = f"{client.Default.gpu_projects_path()}/pipelines/run/{run_id}/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete_run(
            self,
            run_id: str = '',
            page_token: str = '',
            page_size: int = 10,
            sort_by: str = '',
            filter: Optional[str] = None
    ):

        if not run_id:
            raise ValueError(f"RUN_ID {ARGUMENT_IS_MANDATORY}")

        url = f"{client.Default.gpu_projects_path()}/pipelines/run/{run_id}/"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def list_jobs(
        self,
        page_token: str = '',
        page_size: int = 10,
        sort_by: str = '',
        filter: Optional[str] = None
    ):
        url = "{project_path}/pipelines/jobs/".format(project_path=client.Default.gpu_projects_path())
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def get_job(
            self,
            job_id: str = '',
            page_token: str = '',
            page_size: int = 10,
            sort_by: str = '',
            filter: Optional[str] = None
    ):
        if not job_id:
            raise ValueError(f"JOB_ID {ARGUMENT_IS_MANDATORY}")
        url = f"{client.Default.gpu_projects_path()}/pipelines/job/{job_id}/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete_job(
            self,
            job_id: str = '',
            page_token: str = '',
            page_size: int = 10,
            sort_by: str = '',
            filter: Optional[str] = None
    ):

        if not job_id:
            raise ValueError(f"JOB_ID {ARGUMENT_IS_MANDATORY}")

        url = f"{client.Default.gpu_projects_path()}/pipelines/job/{job_id}/"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)
