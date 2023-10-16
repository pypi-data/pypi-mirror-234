# Copyright 2023 Agnostiq Inc.


from .base_client import BaseQClient


class CloudQClient(BaseQClient):
    def submit(self, qscripts, executors, qelectron_info, qnode_specs):
        raise NotImplementedError

    def get_results(self, batch_id):
        raise NotImplementedError

    @property
    def selector(self):
        raise NotImplementedError

    @property
    def database(self):
        raise NotImplementedError

    def serialize(self, obj):
        raise NotImplementedError

    def deserialize(self, ser_obj):
        raise NotImplementedError
