from unittest import TestCase, mock
from urllib.parse import urljoin

from decouple import config
from responses import RequestsMock

from fiddler.api.api import FiddlerClient
from fiddler.constants import CURRENT_API_VERSION


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        _url = config('TEST_FIDDLER_API_SERVER', 'http://127.0.0.1:30001')
        self._url = (
            _url
            if _url.endswith(CURRENT_API_VERSION)
            else urljoin(_url, CURRENT_API_VERSION)
        )
        self._org = config('TEST_FIDDLER_ORGANIZATION_NAME', 'test_organization')
        _token = config('TEST_FIDDLER_API_TOKEN', 'asdbas')
        self.requests_mock = RequestsMock(assert_all_requests_are_fired=True)
        self.requests_mock.start()
        self.server_info_mock = mock.patch.object(FiddlerClient, '_get_server_info')
        self.server_info_mock.start()
        self._check_semver_mock = mock.patch.object(
            FiddlerClient, '_check_server_version'
        )
        self._check_semver_mock.start()
        _check_vc_mock = mock.patch.object(
            FiddlerClient, '_check_version_compatibility'
        )
        _check_vc_mock.start()
        self.client = FiddlerClient(self._url, self._org, _token)

    def tearDown(self) -> None:
        self.client = None
        self.requests_mock.stop()
        self.requests_mock.reset()
        mock.patch.stopall()
