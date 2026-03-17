from nodes.package_debug_reader import package_debug_reader


def test_package_debug_reader_imports():
    assert callable(package_debug_reader)
