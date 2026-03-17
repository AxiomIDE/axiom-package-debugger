def test_package_debug_reader_imports():
    import nodes.package_debug_reader as m
    assert hasattr(m, "handle")
