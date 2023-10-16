from typing import Optional, Union

from predibase.connection_mixin import ConnectionMixin
from predibase.dataset_mixin import DatasetMixin
from predibase.deployment_mixin import DeploymentMixin
from predibase.engine_mixin import EngineMixin
from predibase.llm_mixin import LlmMixin
from predibase.model_mixin import ModelMixin
from predibase.permission_mixin import PermissionMixin
from predibase.pql import start_session
from predibase.pql.api import Session
from predibase.query_mixin import QueryMixin


class PredibaseClient(
    QueryMixin,
    ConnectionMixin,
    DatasetMixin,
    EngineMixin,
    ModelMixin,
    DeploymentMixin,
    PermissionMixin,
    LlmMixin,
):
    def __init__(self, session: Optional[Session] = None, gateway: str = None, token: str = None):
        self._session = session or start_session(gateway, token)

    @property
    def session(self) -> Session:
        return self._session

    def set_connection(self, connection: Union[str, int]):
        """This method sets the default connection to use for any method requiring a connection argument.

        :param connection: The desired connection name or id
        """
        self.session.set_connection(connection)
