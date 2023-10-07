from fiddler.schema.server_info import Version
from fiddler.utils.helpers import match_semver


def test_match_semvar_version():
    assert match_semver(None, '>=22.9.0') is False
    assert match_semver(Version.parse('22.9.0'), '>=22.10.0') is False
    assert match_semver(Version.parse('22.10.0'), '>=22.10.0') is True
    assert match_semver(Version.parse('22.10.0'), '>22.10.0') is False
    assert match_semver(Version.parse('22.11.0'), '>=22.10.0') is True
    assert match_semver(Version.parse('22.11.0'), '>22.10.0') is True
    assert match_semver(Version.parse('22.10.0'), '<=22.10.0') is True
    assert match_semver(Version.parse('22.10.0'), '<22.10.0') is False
    assert match_semver(Version.parse('22.9.0'), '<22.10.0') is True
    assert match_semver(Version.parse('22.11.0-RC1'), '>=22.11.0') is True
