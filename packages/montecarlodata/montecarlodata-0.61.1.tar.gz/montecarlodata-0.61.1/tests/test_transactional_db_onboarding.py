from unittest import TestCase
from unittest.mock import Mock, patch

from montecarlodata.common.user import UserService
from montecarlodata.integrations.onboarding.transactional.transactional_db import (
    TransactionalOnboardingService,
)
from montecarlodata.queries.onboarding import (
    TEST_DATABASE_CRED_MUTATION,
)
from montecarlodata.utils import GqlWrapper, AwsClientWrapper
from tests.test_base_onboarding import _SAMPLE_BASE_OPTIONS
from tests.test_common_user import _SAMPLE_CONFIG


class TransactionalOnboardingTest(TestCase):
    def setUp(self) -> None:
        self._user_service_mock = Mock(autospec=UserService)
        self._request_wrapper_mock = Mock(autospec=GqlWrapper)
        self._aws_wrapper_mock = Mock(autospec=AwsClientWrapper)

        self._service = TransactionalOnboardingService(
            _SAMPLE_CONFIG,
            request_wrapper=self._request_wrapper_mock,
            aws_wrapper=self._aws_wrapper_mock,
            user_service=self._user_service_mock,
        )

    @patch.object(TransactionalOnboardingService, "onboard")
    def test_generic_transactional_db_flow(self, onboard_mock):
        expected_options = {
            **{
                "connectionType": "transactional-db",
                "warehouseType": "transactional-db",
            },
            **_SAMPLE_BASE_OPTIONS,
        }

        self._service.onboard_transactional_db(**_SAMPLE_BASE_OPTIONS)
        onboard_mock.assert_called_once_with(
            validation_query=TEST_DATABASE_CRED_MUTATION,
            validation_response="testDatabaseCredentials",
            connection_type="transactional-db",
            **expected_options
        )
