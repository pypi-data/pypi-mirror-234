# Copyright 2023 Agnostiq Inc.


from abc import ABC, abstractmethod, abstractproperty


class BaseQClient(ABC):
    @abstractmethod
    def submit(self, qscripts, executors, qelectron_info, qnode_specs):
        raise NotImplementedError

    @abstractmethod
    def get_results(self, batch_id):
        raise NotImplementedError

    @abstractproperty
    def selector(self):
        raise NotImplementedError

    @abstractproperty
    def database(self):
        raise NotImplementedError

    # The following methods are abstract because the qserver
    # is expecting serialized inputs and will be sending
    # back serialized outputs, thus even if these methods
    # essentially just pass through, they are still to be
    # implemented by the child class and should use the same
    # seriliazing/deserializing methods as are being used by the equivalent qserver.

    @abstractmethod
    def serialize(self, obj):
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, ser_obj):
        raise NotImplementedError
