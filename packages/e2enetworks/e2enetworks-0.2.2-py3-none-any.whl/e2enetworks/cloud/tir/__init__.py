from e2enetworks.cloud.tir import version as tir_version

__version__ = tir_version.__version__
from e2enetworks.cloud.tir import client
from e2enetworks.cloud.tir.pipelines import PipelineClient
from e2enetworks.cloud.tir.images import Images
from e2enetworks.cloud.tir.skus import Skus
from e2enetworks.cloud.tir.apitoken import APITokens
from e2enetworks.cloud.tir.notebook import Notebooks
from e2enetworks.cloud.tir.datasets import Datasets
from e2enetworks.cloud.tir.models import Models
from e2enetworks.cloud.tir.endpoints import EndPoints
from e2enetworks.cloud.tir.projects import Projects
from e2enetworks.cloud.tir.teams import Teams


init = client.Default.init

__all__ = (
    "init",
    "PipelineClient"
)

def help():
    print("\t\tAIPlatform Help")
    print("\t\t=================")
    print("\t\tAvailable classes:")
    print("\t\t- init: Provides functionalities for initialization.")
    print("\t\t- Images: Provides functionalities to interact with images.")
    print("\t\t- Skus: Provides functionalities to interact with skus.")
    print("\t\t- Notebooks: Provides functionalities to interact with notebooks.")
    print("\t\t- Datasets: Provides functionalities to interact with datasets.")
    print("\t\t- EndPoints: Provides functionalities to interact with endpoints.")
    print("\t\t- Models: Provides functionalities to interact with models.")
    print("\t\t- Projects: Provides functionalities to interact with projects.")
    print("\t\t- Teams: Provides functionalities to interact with teams.")
    print("\t\t- APITokens: Provides functionalities to interact with API tokens.")
    print("\t\t- beautify: beautify and print the specific response")

    # Call help() method on each class
    client.Default.help()
    Images.help()
    Skus.help()
    Notebooks.help()
    Datasets.help()
    EndPoints.help()
    Models.help()
    Projects.help()
    Teams.help()
    APITokens.help()
