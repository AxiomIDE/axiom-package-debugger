from nodes.package_fix_applier import package_fix_applier


def test_package_fix_applier_imports():
    assert callable(package_fix_applier)
