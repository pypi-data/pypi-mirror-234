import concurrent.futures
import os
import time
from dataclasses import dataclass, field
from pprint import pprint
from typing import Dict, List, Optional, TYPE_CHECKING, Union

from dataclasses_json import config, dataclass_json, LetterCase

from predibase.pql.api import ServerResponseError
from predibase.resource import model as mdl
from predibase.resource.connection import get_dataset
from predibase.resource.dataset import Dataset
from predibase.resource.engine import Engine
from predibase.resource.llm.response import GeneratedResponse
from predibase.resource.llm.template import FinetuneTemplateCollection
from predibase.util import load_yaml

if TYPE_CHECKING:
    from predibase.pql.api import Session

_PATH_HERE = os.path.abspath(os.path.dirname(__file__))
_TEMPLATE_DIR = os.path.join(_PATH_HERE, "templates")


class HuggingFaceLLM:
    def __init__(self, session: "Session", model_name: str):
        self.session = session
        self.model_name = model_name

    def get_finetune_templates(self) -> FinetuneTemplateCollection:
        return FinetuneTemplateCollection(self)

    def deploy(
        self,
        deployment_name: str,
        engine_template: Optional[str] = None,
        hf_token: Optional[str] = None,
        auto_suspend_seconds: Optional[int] = None,
    ) -> "LLMDeploymentJob":
        # TODO: if model is an adapter add the base model from the adapter_config.json
        model_params = {
            "name": deployment_name,
            "modelName": self.model_name,
            "engineTemplate": engine_template,
            "scaleDownPeriod": auto_suspend_seconds,
            "source": "huggingface",
        }

        if hf_token is not None:
            model_params["hfToken"] = hf_token

        print("Deploying the model with the following params:")
        pprint(model_params)

        self.session.post_json(
            "/llms",
            json=model_params,
        )
        return LLMDeploymentJob(deployment_name, self.session)

    def finetune(
        self,
        prompt_template: Optional[str] = None,
        target: Optional[str] = None,
        dataset: Optional[Union[str, Dataset]] = None,
        engine: Optional[Union[str, Engine]] = None,
        config: Optional[Union[str, Dict]] = None,
        repo: Optional[str] = None,
    ) -> "mdl.ModelFuture":
        if config is None:
            config = self.get_finetune_templates().default.to_config(prompt_template=prompt_template, target=target)
        else:
            if isinstance(config, str):
                config = load_yaml(config)

            if not isinstance(config, dict):
                raise ValueError(f"Invalid config type: {type(config)}, expected str or dict")

        if repo is None:
            dataset_name = dataset.name if isinstance(dataset, Dataset) else dataset
            if "/" in dataset_name:
                _, dataset_name = dataset_name.split("/")

            model_name = self.model_name
            if "/" in model_name:
                _, model_name = model_name.split("/")

            repo = f"{model_name}-{dataset_name}"

        if "/" in repo:
            repo = repo.replace("/", "-")

        repo: "mdl.ModelRepo" = get_or_create_repo(self.session, repo)
        if dataset is None:
            # Assume the dataset is the same as the repo head
            md = repo.head().to_draft()
            md.config = config
        else:
            if isinstance(dataset, str):
                conn_name = None
                if "/" in dataset:
                    conn_name, dataset = dataset.split("/")
                dataset = get_dataset(self.session, dataset, connection_name=conn_name)
            md = repo.create_draft(config=config, dataset=dataset)

        return md.train_async(engine=engine)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class _LLMDeployment:
    id: int = field(metadata=config(field_name="id"))
    tenant_id: int = field(metadata=config(field_name="tenantID"))
    uuid: str = field(metadata=config(field_name="uuid"))
    name: str = field(metadata=config(field_name="name"))
    description: Optional[str] = field(metadata=config(field_name="description"))
    model_name: str = field(metadata=config(field_name="modelName"))
    num_shards: Optional[int] = field(metadata=config(field_name="numShards"))
    quantize: bool = field(metadata=config(field_name="quantize"))
    deployment_status: str = field(metadata=config(field_name="deploymentStatus"))

    prompt_template: str = field(metadata=config(field_name="promptTemplate"))
    min_replicas: int = field(metadata=config(field_name="minReplicas"))
    max_replicas: int = field(metadata=config(field_name="maxReplicas"))
    created: str = field(metadata=config(field_name="created"))
    updated: str = field(metadata=config(field_name="updated"))
    created_by_user_id: Optional[int] = field(metadata=config(field_name="createdByUserID"))
    scale_down_period: int = field(metadata=config(field_name="scaleDownPeriod"))
    error_text: Optional[str] = field(metadata=config(field_name="errorText"), default=None)
    dynamic_adapter_loading_enabled: bool = field(
        metadata=config(field_name="dynamicAdapterLoadingEnabled"),
        default=False,
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LLMDeploymentReadyResponse:
    name: str
    ready: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LLMDeploymentScaledResponse:
    name: str
    scaled: bool


class LLMDeployment:
    def __init__(
        self,
        session: "Session",
        name: str,
        # adapter: Optional["mdl.Model"] = None,
        # adapter can be a HuggingFaceLLM or mdl.Model
        adapter: Optional[Union["mdl.Model", HuggingFaceLLM]] = None,
        deployment_metadata: Optional[_LLMDeployment] = None,
    ):
        self.session = session
        self.name = name
        self.data = (
            _LLMDeployment.from_dict(self.session.get_json(f"/llms/{self.name}"))
            if deployment_metadata is None
            else deployment_metadata
        )

        if adapter:
            if not self.data.dynamic_adapter_loading_enabled:
                raise RuntimeError(f"Base deployment {self.name} is not configured to accept dynamic adapters")

            # TODO: (magdy) check base model compatibility for hf based adapters here
            # (Delayed now since we need to do a roundtrip to hf) (INFRA-2052)
            # Directly import `Model` here to avoid cyclic import issues.
            from predibase.resource.model import Model

            if isinstance(adapter, Model) and self.data.model_name != adapter.llm_base_model_name:
                raise RuntimeError(
                    f"base deployment {self.name} does not match the adapter's base model. "
                    f"Expected base deployment model to be: {adapter.llm_base_model_name}. "
                    f"Actual: {self.data.model_name}",
                )

        self._adapter = adapter

    @property
    def adapter(self) -> Optional["mdl.Model"]:
        return self._adapter

    def with_adapter(self, model: Union["mdl.Model", HuggingFaceLLM]) -> "LLMDeployment":
        return LLMDeployment(
            session=self.session,
            name=self.name,
            adapter=model,
            deployment_metadata=self.data,
        )

    def generate(
        self,
        templates: Union[str, List[str]],
        options: Optional[Dict[str, Union[str, float]]] = None,
    ) -> List[GeneratedResponse]:
        templates = [templates] if isinstance(templates, str) else templates

        resp_list, future_to_args = [], dict()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for input_text in templates:
                data = {
                    "inputs": input_text,
                    "parameters": options,
                }

                if self._adapter:
                    if isinstance(self._adapter, HuggingFaceLLM):
                        data["parameters"]["adapter_id"] = self._adapter.model_name
                        data["parameters"]["adapter_source"] = "hub"
                    else:
                        data["parameters"][
                            "adapter_id"
                        ] = f"{self._adapter.uuid}/{self._adapter.best_run_id}/artifacts/model/model_weights/"
                        data["parameters"]["adapter_source"] = "s3"

                future = executor.submit(
                    self.session.post_json,
                    f"/llms/{self.name}/generate",
                    data,
                )
                future_to_args[future] = (self.name, input_text)
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                try:
                    deployment_name, input_text = future_to_args[future]
                    res = future.result()
                    res = GeneratedResponse(
                        prompt=input_text,
                        response=res["generated_text"],
                        model_name=deployment_name,
                        generated_tokens=res["details"]["generated_tokens"],
                    )
                    resp_list.append(res)
                except Exception as exc:
                    print("ERROR:", exc)
        return resp_list

    def prompt(
        self,
        templates: Union[str, List[str]],
        options: Optional[Dict[str, float]] = None,
    ) -> List[GeneratedResponse]:
        deployment_status = self.get_status()
        if deployment_status != "active":
            raise Exception(f"Target LLM deployment `{self.name}` is not active yet!")

        deployment_ready = self.is_ready()
        if not deployment_ready:
            print(f"WARNING: Target LLM deployment `{self.name}` is not fully scaled yet. Responses may be delayed...")

        # talk directly to the LLM, bypassing Temporal and the engines.
        return self.generate(templates=templates, options=options)

    def delete(self):
        print(f"Requested deletion of llm deployment: `{self.name}` ...")
        endpoint = f"/llms/{self.name}"
        resp = self.session._delete(endpoint)
        if not resp.ok:
            raise RuntimeError(f"Failed to trigger LLM deletion - got status {resp.status_code} -- {resp.reason}")

        while True:
            try:
                self.session.get_json(endpoint)
            except Exception as e:
                if isinstance(e, ServerResponseError) and "record not found" in e.message:
                    print(f"Successfully deleted llm deployment: `{self.name}`")
                    break
                else:
                    raise RuntimeError(f"Error while deleting deployment `{self.name}`: {e} {type(e)}")
            time.sleep(1.0)

    def is_ready(self) -> bool:
        resp = self.session.get_json(f"/llms/{self.name}/ready")
        return LLMDeploymentReadyResponse.from_dict(resp).ready

    def wait_for_ready(self, timeout_seconds: int = 600, poll_interval_seconds: int = 5) -> bool:
        start = time.time()
        while int(time.time() - start) < timeout_seconds:
            if self.is_ready():
                return True
            time.sleep(poll_interval_seconds)
        return False

    def is_scaled(self) -> bool:
        resp = self.session.get_json(f"/llms/{self.name}/scaled")
        return LLMDeploymentScaledResponse.from_dict(resp).scaled

    def get_status(self) -> str:
        resp = _LLMDeployment.from_dict(self.session.get_json(f"/llms/{self.name}"))
        return resp.deployment_status


class LLMDeploymentJob:
    def __init__(self, deployment_name: str, session: "Session"):
        self._deployment_name = deployment_name
        self._uri = f"pb://jobs/deploy::{deployment_name}"
        self._session = session

    def get(self) -> LLMDeployment:
        resp = self._session.get_llm_deployment_until_with_logging(
            f"/llms/{self._deployment_name}",
            lambda resp: resp["deploymentStatus"] == "active",
            lambda resp: f"Failed to create deployment {self._deployment_name} with status {resp['deploymentStatus']}"
            if resp["deploymentStatus"] in ("failed", "canceled")
            else None,
        )

        return LLMDeployment(self._session, self._deployment_name, deployment_metadata=resp)

    def cancel(self):
        return self._session.post_json(f"/llms/{self._deployment_name}/cancel", {})


def get_or_create_repo(session: "Session", repo_name: str) -> "mdl.ModelRepo":
    return mdl.create_model_repo(session, name=repo_name, exists_ok=True)
