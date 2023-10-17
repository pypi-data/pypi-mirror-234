import pytest
from pytest_mock import MockerFixture

from fiddler.exceptions import NotSupported
from fiddler.schema.server_info import Version
from fiddler.utils.decorators import check_version


def test_with_supported_version(mocker: MockerFixture) -> None:
    @check_version(version_expr='>=23.2.0')
    def func(self):
        pass

    self_ = mocker.MagicMock()
    self_.server_info.server_version = Version.parse('23.2.0')

    func(self_)


def test_with_unsupported_version(mocker: MockerFixture) -> None:
    @check_version(version_expr='>=23.2.0')
    def func(self):
        pass

    self_ = mocker.MagicMock()
    self_.server_info.server_version = Version.parse('23.1.0')

    with pytest.raises(NotSupported) as cx:
        func(self_)

    assert (
        str(cx.value)
        == 'func method is supported with server version >=23.2.0, but the current server version is 23.1.0'
    )
