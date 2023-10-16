# Copyright 2023 Agnostiq Inc.

"""Unit tests for dispatch helpers"""


import covalent as ct

from covalent_cloud.dispatch_management.helpers import inject_parameter_outputs


def test_parameter_outputs():
    """Test inject_parameter_outputs"""

    @ct.electron
    def task(x):
        return x**2

    @ct.lattice
    def workflow(x):
        return task(x)

    workflow.build_graph(3)

    inject_parameter_outputs(workflow)

    tg = workflow.transport_graph
    param_output = tg.get_node_value(1, "output")
    param_value = tg.get_node_value(1, "output")

    assert param_output.get_deserialized() == param_value.get_deserialized()
