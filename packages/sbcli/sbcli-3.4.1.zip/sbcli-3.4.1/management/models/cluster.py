# coding=utf-8

from typing import Mapping, List

from management.models.base_model import BaseModel
from management.models.storage_node import StorageNode


class Cluster(BaseModel):

    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_SUSPENDED = "suspended"

    attributes = {
        "uuid": {"type": str, 'default': ""},
        "blk_size": {"type": int, 'default': 0},
        "page_size_in_blocks": {"type": int, 'default': 0},
        "model_ids": {"type": List[str], "default": []},
        "ha_type": {"type": str, 'default': "single"},
        "tls": {"type": bool, 'default': False},
        "auth_hosts_only": {"type": bool, 'default': False},
        "nqn": {"type": str, 'default': ""},
        "iscsi": {"type": str, 'default': ""},
        "dhchap": {"type": str, "default": ""},
        "cli_pass": {"type": str, "default": ""},
        "db_connection": {"type": str, "default": ""},

        "secret": {"type": str, "default": ""},
        "cluster_status": {"type": str, "default": ""},
        "updated_at": {"type": str, "default": ""},
    }

    def __init__(self, data=None):
        super(Cluster, self).__init__()
        self.set_attrs(self.attributes, data)
        self.object_type = "object"

    def get_id(self):
        return self.uuid


class ClusterMap(BaseModel):

    attributes = {
        "partitions_count": {"type": int, 'default': 0},
        "nodes": {"type": Mapping[str, StorageNode], 'default': {}},
    }

    def __init__(self, data=None):
        super(ClusterMap, self).__init__()
        self.set_attrs(self.attributes, data)
        self.object_type = "object"

    def get_id(self):
        return "0"

    def recalculate_partitions(self):
        self.partitions_count = 0
        for node_id in self.nodes:
            self.partitions_count += self.nodes[node_id].partitions_count
