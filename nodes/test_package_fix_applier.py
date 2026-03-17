def test_package_fix_applier_imports():
    import nodes.package_fix_applier as m
    assert hasattr(m, "handle")
