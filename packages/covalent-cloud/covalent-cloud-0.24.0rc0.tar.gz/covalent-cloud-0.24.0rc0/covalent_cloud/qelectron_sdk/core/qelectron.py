# Copyright 2023 Agnostiq Inc.


import functools
from typing import Callable, List, Optional, Union

import pennylane as qml

from ..core.qnode_qe import QElectronInfo, QNodeQE
from ..executors.base import CloudQCluster, CloudQExecutor

Selector = Union[str, Callable[[qml.tape.QuantumScript, List[CloudQExecutor]], CloudQExecutor]]


def qelectron(
    qnode: Optional[qml.QNode] = None,
    *,
    executors: Union[CloudQExecutor, CloudQCluster, List[CloudQExecutor]] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    selector: str = "random",
) -> QNodeQE:
    """
    QElectron decorator to be called upon a Pennylane QNode. Adds multi-backend
    execution functionality to the original QNode.

    Args:
        qnode: The Pennylane :code:`QNode` to wrap.

    Keyword Args:
        executors: The quantum executor(s) to use for running the QNode. A single
            executor, list of executors, or a :code:`QCluster` instance are accepted.
            If a list of multiple executors is passed, a quantum cluster is
            initialized from this list automatically and :code:`selector` is used as the
            cluster's selector. Defaults to a :code:`CloudQExecutor`.
        name: An optional name for the QElectron. Defaults to the circuit function's
            name.
        description: An optional description for the QElectron. Defaults to the
            circuit function's docstring.
        selector: One of the strings :code:`"cyclic"` or :code:`"random"`. Used to
            select the executor from the cluster when multiple executors are passed.

    Raises:
        ValueError: If any invalid executors are passed.

    Returns:
        :code:`QNodeQE`: A sub-type of :code:`QNode` that integrates QElectrons.
    """

    if executors is None:
        executors = CloudQExecutor()

    if qnode is None:
        # This only happens when `qelectron()` is not used as a decorator.
        return functools.partial(
            qelectron, executors=executors, name=name, description=description
        )

    # Check if executor is a list of executors.
    if isinstance(executors, list):
        if not all(isinstance(ex, CloudQExecutor) for ex in executors):
            raise ValueError("Invalid executor in executors list.")
        if len(executors) > 1:
            # Convert to cluster if more than one executor in list.
            executors = CloudQCluster(executors=executors, selector=selector)

    # Set default name and description.
    if name is None:
        name = qnode.func.__name__

    if description is None:
        description = qnode.func.__doc__

    qelectron_info = QElectronInfo(
        name=name,
        description=description,
        qnode_device_shots=qnode.device.shots,
        num_device_wires=qnode.device.num_wires,
        pennylane_active_return=qml.active_return(),
    )

    # Validating shots and wires for the batch of circuits
    # Here the `executors` will either be a CloudQExecutor or a CloudQCluster
    executors.set_shots(qelectron_info.qnode_device_shots)
    executors.validate_attrs()

    # Check if a single executor instance was passed.
    if not isinstance(executors, list):
        executors = [executors]

    # Create and return a new `QNodeQE` instance.
    return QNodeQE(qnode, executors, qelectron_info)
