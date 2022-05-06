from builder.core.entity.version import Version


def test_version_parse():
    content = '0.12.1'
    v = Version.parse_str(content)
    assert v.get_full() == 'v.0.12.1'
