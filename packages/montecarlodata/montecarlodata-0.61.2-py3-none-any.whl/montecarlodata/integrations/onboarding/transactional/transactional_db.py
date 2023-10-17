from montecarlodata.config import Config
from montecarlodata.errors import manage_errors
from montecarlodata.integrations.onboarding.base import BaseOnboardingService
from montecarlodata.integrations.onboarding.fields import (
    EXPECTED_GENERIC_DB_GQL_RESPONSE_FIELD,
    TRANSACTIONAL_WAREHOUSE_TYPE,
    TRANSACTIONAL_CONNECTION_TYPE,
)
from montecarlodata.queries.onboarding import (
    TEST_DATABASE_CRED_MUTATION,
)


class TransactionalOnboardingService(BaseOnboardingService):
    def __init__(self, config: Config, **kwargs):
        super().__init__(config, **kwargs)

    @manage_errors
    def onboard_transactional_db(self, **kwargs) -> None:
        """
        Onboard a Transactional DB connection by validating and adding a connection.
        """
        kwargs["connectionType"] = TRANSACTIONAL_CONNECTION_TYPE
        kwargs["warehouseType"] = TRANSACTIONAL_WAREHOUSE_TYPE

        self.onboard(
            validation_query=TEST_DATABASE_CRED_MUTATION,
            validation_response=EXPECTED_GENERIC_DB_GQL_RESPONSE_FIELD,
            connection_type=TRANSACTIONAL_CONNECTION_TYPE,
            **kwargs
        )
