import json
import time
from typing import Optional, Dict

from montecarlodata.iac.schemas import (
    ConfigTemplateUpdateAsyncResponse,
    ConfigTemplateDeleteResponse,
    ConfigTemplateUpdateState,
)
from montecarlodata.queries.iac import (
    CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE_ASYNC,
    DELETE_MONTE_CARLO_CONFIG_TEMPLATE,
    GET_MONTE_CARLO_CONFIG_TEMPLATE_UPDATE_STATE,
)
from montecarlodata.utils import GqlWrapper


class MonteCarloConfigTemplateClient:
    ASYNC_TIMEOUT_SECONDS = 60 * 15 * 2  # 30m (2x the lambda timeout of 15 minutes)

    def __init__(self, gql_wrapper: GqlWrapper):
        self._gql_wrapper = gql_wrapper

    def apply_config_template(
        self,
        namespace: str,
        config_template_as_dict: Dict,
        resource: Optional[str] = None,
        dry_run: bool = False,
        misconfigured_as_warning: bool = False,
    ) -> ConfigTemplateUpdateState:
        response = self.apply_config_template_async(
            namespace=namespace,
            config_template_as_dict=config_template_as_dict,
            resource=resource,
            dry_run=dry_run,
            misconfigured_as_warning=misconfigured_as_warning,
        )

        if response.errors:
            return ConfigTemplateUpdateState(
                state="FAILED",
                resource_modifications=[],
                errors_as_json=response.errors_as_json,
                changes_applied=False,
            )

        update_uuid = response.update_uuid

        start = time.time()
        while time.time() - start < self.ASYNC_TIMEOUT_SECONDS:
            state = self.get_config_template_update_state(update_uuid)

            if state.state != "PENDING":
                return state

            time.sleep(5)

    def apply_config_template_async(
        self,
        namespace: str,
        config_template_as_dict: Dict,
        resource: Optional[str] = None,
        dry_run: bool = False,
        misconfigured_as_warning: bool = False,
    ) -> ConfigTemplateUpdateAsyncResponse:
        response = self._gql_wrapper.make_request_v2(
            query=CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE_ASYNC,
            operation="createOrUpdateMonteCarloConfigTemplateAsync",
            variables=dict(
                namespace=namespace,
                configTemplateJson=json.dumps(config_template_as_dict),
                dryRun=dry_run,
                misconfiguredAsWarning=misconfigured_as_warning,
                resource=resource,
            ),
        )

        return ConfigTemplateUpdateAsyncResponse.from_dict(response.data["response"])

    def get_config_template_update_state(
        self, update_uuid: str
    ) -> ConfigTemplateUpdateState:
        response = self._gql_wrapper.make_request_v2(
            query=GET_MONTE_CARLO_CONFIG_TEMPLATE_UPDATE_STATE,
            operation="getMonteCarloConfigTemplateUpdateState",
            variables=dict(updateUuid=update_uuid),
        )

        return ConfigTemplateUpdateState.from_dict(response.data)

    def delete_config_template(
        self, namespace: str, dry_run: bool = False
    ) -> ConfigTemplateDeleteResponse:
        response = self._gql_wrapper.make_request_v2(
            query=DELETE_MONTE_CARLO_CONFIG_TEMPLATE,
            operation="deleteMonteCarloConfigTemplate",
            variables=dict(
                namespace=namespace,
                dryRun=dry_run,
            ),
        )

        return ConfigTemplateDeleteResponse.from_dict(response.data["response"])
