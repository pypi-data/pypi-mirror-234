from typing import Any, Dict, List, Optional, Union

import pandas as pd

from predibase.resource import model as mdl
from predibase.resource.deployment import Deployment
from predibase.util import spinner


class DeploymentMixin:
    @spinner(name="Create Deployment")
    def create_deployment(
        self,
        name: str,
        model: "mdl.Model",
        engine_name: Optional[str] = None,
        replace: bool = False,
        exists_ok: bool = False,
        comment: Optional[str] = None,
        df: bool = False,
    ) -> Union[pd.DataFrame, List[Deployment]]:
        """Creates a deployment.

        :param str name: Name of deployment.
        :param Model model: Model object to deploy.
        :param str engine_name: Optional serving engine name to deploy to (Default None).
        :param bool replace: Optional flag replace a deployment (default False).
        :param bool exists_ok: Optional flag to only create deployment if not exists (default False).
        :param str comment: Optional comment for the deployment (default None).
        :param bool df: Optional flag to return the result as a dataframe (Default False).
        :return: pandas DataFrame or list of Deployment objects.
        """
        if self.session.is_free_trial():
            raise PermissionError(
                "Deployments are locked during the trial period. Contact us to upgrade or if you would like a demo",
            )
        elif self.session.is_plan_expired():
            raise PermissionError(
                "Deployments are locked for expired plans. Contact us to upgrade or if you would like a demo",
            )
        else:
            conditions = []
            if replace:
                conditions.append("OR REPLACE")
            conditions.append("DEPLOYMENT")
            if exists_ok:
                conditions.append("IF NOT EXISTS")
            conditions.append(f'"{name}"')

            if engine_name is not None:
                conditions.append(f'TO "{engine_name}"')
            conditions.append(f'USING "{model.repo.name}" VERSION {model.version}')
            if comment is not None:
                conditions.append(f"COMMENT '{comment}'")

            query = f"CREATE {' '.join(conditions)}"
            result = self.session.execute(query)
            deployments = self._format_deployment_result(result)
            # TODO: Change this to return a DeploymentCollection, with a to_dataframe method.
            if df:
                return pd.DataFrame(deployments)
            return [Deployment.from_dict({"session": self.session, **x}) for x in deployments]

    @spinner(name="Delete Deployment")
    def delete_deployment(
        self,
        name: str,
        if_exists: bool = False,
        df: bool = False,
    ) -> Union[pd.DataFrame, List[Deployment]]:
        """Deletes a deployment.

        :param str name: required name of deployment.
        :param bool if_exists: Optional flag to only delete deployment if it exists (default False).
        :param bool df: Optional flag to return the result as a dataframe (Default False).
        :return: pandas DataFrame or list of Deployment objects.
        """
        conditions = []
        conditions.append("DROP DEPLOYMENT")
        if if_exists:
            conditions.append("IF EXISTS")
        conditions.append(f'"{name}"')

        query = f"{' '.join(conditions)}"
        result = self.session.execute(query)
        deployments = self._format_deployment_result(result)
        if df:
            return pd.DataFrame(deployments)
        return [Deployment.from_dict({"session": self.session, **x}) for x in deployments]

    def list_deployments(
        self,
        deployment_name_pattern: Optional[str] = None,
        engine_name: Optional[str] = None,
        repo_name: Optional[str] = None,
        model_version: Optional[str] = None,
        df: bool = False,
    ) -> Union[pd.DataFrame, List[Deployment]]:
        """Lists Deployments.

        :param str deployment_name_pattern: Optional filter for deployment name (Default None).
        :param str engine_name: Optional filter by engine name (Default None).
        :param str repo_name: Optional filter by model repository name (Default None).
        :param str model_version: Optional filter by model version (Default None).
        :param bool df: Optional flag to return the result as a dataframe (Default False).
        :return: pandas DataFrame or list of Deployment objects.
        """
        conditions = []
        if engine_name is not None:
            conditions.append(f'IN "{engine_name}"')
        if repo_name is not None:
            conditions.append(f'USING "{repo_name}"')
            if model_version is not None:
                conditions.append(f"VERSION {model_version}")
        if deployment_name_pattern is not None:
            conditions.append(f"LIKE '{deployment_name_pattern}'")

        query = f"SHOW DEPLOYMENTS {' '.join(conditions)}"
        result = self.session.execute(query)
        deployments = self._format_deployment_result(result)
        if df:
            return pd.DataFrame(deployments)
        return [Deployment.from_dict({"session": self.session, **x}) for x in deployments]

    def _format_deployment_result(self, result: pd.DataFrame) -> List[Dict[str, Any]]:
        deployments = [
            {
                "session": self.session,
                "name": row["name"],
                "deploymentUrl": row["url"],
                "deploymentVersion": row["head_version_number"],
                "engineName": row["head_version_engine_name"],
                "modelName": row["head_version_model_name"],
                "modelVersion": row["head_version_model_version"],
                "comment": row["head_version_comment"],
                "errorText": row["head_version_error_text"],
            }
            for row in result.to_dict(orient="records")
        ]
        return deployments

    def get_deployment(self, name: str) -> Deployment:
        """Gets a deployment.

        :param str name: Name of deployment.
        :return: Deployment object.
        """
        deployments = self.list_deployments(deployment_name_pattern=name, df=False)
        if len(deployments) == 0:
            raise ValueError(f"Deployment '{name}' not found.")
        return deployments[0]
