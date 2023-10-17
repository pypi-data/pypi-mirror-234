import uuid
from typing import Optional, List, Dict, Any

import click
from pycarlo.common.errors import GqlError
from pycarlo.core import Client, Query
from pycarlo.lib.schema import TestCredentialsV2Response

from montecarlodata.common.echo_utils import (
    echo_warning_message,
    echo_error_message,
    styled_warning_icon,
    styled_error_icon,
    styled_success_icon,
)
from montecarlodata.common.user import UserService
from montecarlodata.config import Config
from montecarlodata.errors import complain_and_abort
from montecarlodata.utils import GqlWrapper


class CollectorValidationService:
    def __init__(
        self,
        config: Config,
        mc_client: Client,
        request_wrapper: Optional[GqlWrapper] = None,
        user_service: Optional[UserService] = None,
    ):
        self._mc_client = mc_client
        self._request_wrapper = request_wrapper or GqlWrapper(config)
        self._user_service = user_service or UserService(
            request_wrapper=self._request_wrapper, config=config
        )

    def run_validations(
        self, dc_id: Optional[str] = None, only_periodic: bool = False
    ) -> int:
        """
        Runs all validators for all integrations in the data collector.

        :param dc_id: The UUID of the data collector.
        :param only_periodic: Whether only periodic validations must be run or not.
        """
        dc = self._user_service.get_collector(dc_id)

        # Filter integration list to just integrations for this dc
        all_integrations = [
            integration
            for integration in (
                (self._user_service.warehouses or [])
                + (self._user_service.bi_containers or [])
                + (self._user_service.etl_containers or [])
            )
            if integration.get("dataCollector", {}).get("uuid") == dc.uuid
        ]

        total_failures = 0
        for integration in all_integrations:
            click.echo("")
            connections: List[Dict[str, Any]] = integration.get("connections", [])
            for connection in connections:
                if "type" in connection and "uuid" in connection:
                    connection_failures = self._run_connection_validators(
                        dc_uuid=dc.uuid,
                        name=integration.get("name", ""),
                        connection_type=connection["type"].lower(),
                        connection_uuid=connection["uuid"],
                        only_periodic=only_periodic,
                    )
                    total_failures += connection_failures

        # Run storage access validation. If DC has an agent registered, will validate that the agent's storage location is accessible.
        # If DC has no agent registered, will validate that default storage location is accessible.
        click.echo("")
        total_failures += self._run_storage_access_validation(dc_id=dc.uuid)

        click.echo("")
        if total_failures == 0:
            click.echo("All validations passed")
        else:
            click.echo(f"{total_failures} validations failed")
        return total_failures

    def _run_connection_validators(
        self,
        dc_uuid: uuid.UUID,
        name: str,
        connection_type: str,
        connection_uuid: uuid.UUID,
        only_periodic: bool,
    ) -> int:
        click.echo(
            f"Validating {connection_type} connection: {name} - {connection_uuid}"
        )
        validations = self._get_supported_validations(
            dc_uuid=dc_uuid,
            connection_type=connection_type,
            only_periodic=only_periodic,
        )
        failures = 0
        for validation in validations:
            ok = False
            warning = False
            try:
                result = self._run_single_validation(
                    connection_uuid=connection_uuid,
                    validation_name=validation,
                )

                ok, warning = self._process_validation_result(result)
            except Exception as e:
                echo_error_message(f"\tValidation {validation} failed ({e}).")

            result_icon, failures = self._get_icon(ok, warning, failures)
            click.echo(f"\t{validation}: {result_icon}")

        return failures

    def _get_supported_validations(
        self, dc_uuid: uuid.UUID, connection_type: str, only_periodic: bool
    ) -> List[str]:
        query = Query()
        query.get_supported_validations_v2(
            dc_id=dc_uuid, connection_type=connection_type
        )

        try:
            result = self._mc_client(
                query=query,
            ).get_supported_validations_v2

            return [
                validation.name
                for validation in result.supported_validations
                if not only_periodic or validation.periodic_validation
            ]
        except GqlError as e:
            complain_and_abort(f"Unable to get list of supported validators ({e}).")
            return []

    def _run_single_validation(
        self,
        connection_uuid: uuid.UUID,
        validation_name: str,
    ) -> Optional[TestCredentialsV2Response]:
        query = Query()
        query.test_existing_connection_v2(
            connection_id=connection_uuid, validation_name=validation_name
        )

        return self._mc_client(
            query=query,
            idempotent_request_id=str(uuid.uuid4()),
            timeout_in_seconds=40,  # let Monolith timeout first
        ).test_existing_connection_v2

    def _run_storage_access_validation(
        self,
        dc_id: uuid.UUID,
    ) -> int:
        query = Query()
        query.test_storage_access(dc_id=dc_id)

        click.echo(f"Validating storage access:")

        failures = 0
        ok = False
        warning = False
        try:
            result = self._mc_client(
                query=query,
                idempotent_request_id=str(uuid.uuid4()),
                timeout_in_seconds=40,  # let Monolith timeout first
            ).test_storage_access

            ok, warning = self._process_validation_result(result)
        except Exception as e:
            echo_error_message(f"\tValidation validate_storage_access failed ({e}).")

        result_icon, failures = self._get_icon(ok, warning, failures)
        click.echo(f"\tvalidate_storage_access: {result_icon}")

        return failures

    @staticmethod
    def _process_validation_result(result: TestCredentialsV2Response) -> (bool, bool):
        ok = False
        warning = False

        # if there are only warnings we log them but consider it a successful validation
        ok = result.success or not bool(result.errors)
        if result.warnings:
            for warning in result.warnings:
                echo_warning_message(f"\t{warning.cause}")
        if result.errors:
            for error in result.errors:
                echo_error_message(f"\t{error.cause}")
        elif not result.success:
            warning = True

        return ok, warning

    @staticmethod
    def _get_icon(ok: bool, warning: bool, failures: int) -> (str, int):
        if ok:
            result_icon = styled_warning_icon() if warning else styled_success_icon()
        else:
            result_icon = styled_error_icon()
            failures += 1
        return result_icon, failures
