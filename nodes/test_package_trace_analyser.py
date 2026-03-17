from nodes.package_trace_analyser import package_trace_analyser


def test_package_trace_analyser_imports():
    assert callable(package_trace_analyser)
