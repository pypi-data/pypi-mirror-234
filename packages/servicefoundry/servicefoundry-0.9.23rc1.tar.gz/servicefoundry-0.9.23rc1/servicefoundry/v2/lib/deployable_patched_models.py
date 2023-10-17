from typing import Union

from pydantic import Field, conint, constr

from servicefoundry.auto_gen import models
from servicefoundry.lib.model.entity import Deployment
from servicefoundry.v2.lib.deploy import deploy_component
from servicefoundry.v2.lib.patched_models import Autoscaling


class Service(models.Service):
    type: constr(regex=r"service") = "service"
    resources: models.Resources = Field(default_factory=models.Resources)
    # This is being patched because cue export marks this as a "number"
    replicas: Union[conint(ge=0, le=100), models.ServiceAutoscaling] = Field(
        1,
        description="+label=Replicas\n+usage=Replicas of service you want to run\n+icon=fa-clone\n+sort=3",
    )

    class Config:
        extra = "forbid"

    def deploy(self, workspace_fqn: str, wait: bool = True) -> Deployment:
        return deploy_component(component=self, workspace_fqn=workspace_fqn, wait=wait)


class Job(models.Job):
    type: constr(regex=r"job") = "job"
    resources: models.Resources = Field(default_factory=models.Resources)

    class Config:
        extra = "forbid"

    def deploy(self, workspace_fqn: str, wait: bool = True) -> Deployment:
        return deploy_component(component=self, workspace_fqn=workspace_fqn, wait=wait)


class ModelDeployment(models.ModelDeployment):
    type: constr(regex=r"model-deployment") = "model-deployment"
    resources: models.Resources = Field(default_factory=models.Resources)

    class Config:
        extra = "forbid"

    def deploy(self, workspace_fqn: str, wait: bool = True) -> Deployment:
        return deploy_component(component=self, workspace_fqn=workspace_fqn, wait=wait)


class Notebook(models.Notebook):
    type: constr(regex=r"^notebook$") = Field("notebook", description="+value=notebook")
    resources: models.Resources = Field(default_factory=models.Resources)

    class Config:
        extra = "forbid"

    def deploy(self, workspace_fqn: str, wait: bool = True) -> Deployment:
        return deploy_component(component=self, workspace_fqn=workspace_fqn, wait=wait)


class Helm(models.Helm):
    type: constr(regex=r"^helm$") = "helm"

    class Config:
        extra = "forbid"

    def deploy(self, workspace_fqn: str, wait: bool = True) -> Deployment:
        return deploy_component(component=self, workspace_fqn=workspace_fqn, wait=wait)


class Volume(models.Volume):
    type: constr(regex=r"^volume$") = "volume"

    class Config:
        extra = "forbid"

    def deploy(self, workspace_fqn: str, wait: bool = True) -> Deployment:
        return deploy_component(component=self, workspace_fqn=workspace_fqn, wait=wait)


class AsyncService(models.AsyncService):
    type: constr(regex=r"^async-service$") = "async-service"
    replicas: Union[conint(ge=0, le=100), models.AsyncServiceAutoscaling] = 1
    resources: models.Resources = Field(default_factory=models.Resources)

    class Config:
        extra = "forbid"

    def deploy(self, workspace_fqn: str, wait: bool = True) -> Deployment:
        return deploy_component(component=self, workspace_fqn=workspace_fqn, wait=wait)


class Application(models.Application):
    class Config:
        extra = "forbid"

    def deploy(self, workspace_fqn: str, wait: bool = True) -> Deployment:
        return deploy_component(
            component=self.__root__, workspace_fqn=workspace_fqn, wait=wait
        )
