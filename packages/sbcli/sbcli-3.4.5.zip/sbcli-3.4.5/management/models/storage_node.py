# coding=utf-8

from datetime import datetime
from typing import List

from management.models.base_model import BaseModel
from management.models.iface import IFace
from management.models.nvme_device import NVMeDevice


class LVol(BaseModel):

    attributes = {
        "lvol_name": {"type": str, 'default': ""},
        "size": {"type": int, 'default': 0},
        "uuid": {"type": str, 'default': ""},
        "base_bdev": {"type": str, 'default': ""},
        "lvol_bdev": {"type": str, 'default': ""},
        "comp_bdev": {"type": str, 'default': ""},
        "crypto_bdev": {"type": str, 'default': ""},
        "nvme_dev": {"type": NVMeDevice, 'default': None},
        "pool_uuid": {"type": str, 'default': ""},
        "hostname": {"type": str, 'default': ""},
        "node_id": {"type": str, 'default': ""},
        "mode": {"type": str, 'default': "read-write"},
        "lvol_type": {"type": str, 'default': "lvol"},  # lvol, compressed, crypto, dedup
        "bdev_stack": {"type": List, 'default': []},
        "crypto_key_name": {"type": str, 'default': ""},
        "rw_ios_per_sec": {"type": int, 'default': 0},
        "rw_mbytes_per_sec": {"type": int, 'default': 0},
        "r_mbytes_per_sec": {"type": int, 'default': 0},
        "w_mbytes_per_sec": {"type": int, 'default': 0},
        "cloned_from_snap": {"type": str, 'default': ""},
        "nqn": {"type": str, 'default': ""},

    }

    def __init__(self, data=None):
        super(LVol, self).__init__()
        self.set_attrs(self.attributes, data)
        self.object_type = "object"

    def get_id(self):
        return self.uuid


class StorageNode(BaseModel):

    STATUS_ONLINE = 'online'
    STATUS_OFFLINE = 'offline'
    STATUS_ERROR = 'error'
    STATUS_REPLACED = 'replaced'
    STATUS_SUSPENDED = 'suspended'
    STATUS_IN_CREATION = 'in_creation'
    STATUS_IN_SHUTDOWN = 'in_shutdown'
    STATUS_RESTARTING = 'restarting'
    STATUS_REMOVED = 'removed'

    attributes = {
        "uuid": {"type": str, 'default': ""},
        "baseboard_sn": {"type": str, 'default': ""},
        "system_uuid": {"type": str, 'default': ""},
        "hostname": {"type": str, 'default': ""},
        "host_nqn": {"type": str, 'default': ""},
        "subsystem": {"type": str, 'default': ""},
        "nvme_devices": {"type": List[NVMeDevice], 'default': []},
        "sequential_number": {"type": int, 'default': 0},
        "partitions_count": {"type": int, 'default': 0},
        "ib_devices": {"type": List[IFace], 'default': []},
        "status": {"type": str, 'default': "in_creation"},
        "updated_at": {"type": str, 'default': str(datetime.now())},
        "create_dt": {"type": str, 'default': str(datetime.now())},
        "remove_dt": {"type": str, 'default': str(datetime.now())},
        "mgmt_ip": {"type": str, 'default': ""},
        "rpc_port": {"type": int, 'default': -1},
        "rpc_username": {"type": str, 'default': ""},
        "rpc_password": {"type": str, 'default': ""},
        "data_nics": {"type": List[IFace], 'default': []},
        "lvols": {"type": List[str], 'default': []},
        "node_lvs": {"type": str, 'default': "lvs"},
        "services": {"type": List[str], 'default': []},
        "cluster_id": {"type": str, 'default': ""},
        "api_endpoint": {"type": str, 'default': ""},
        "remote_devices": {"type": List[NVMeDevice], 'default': []},

    }

    def __init__(self, data=None):
        super(StorageNode, self).__init__()
        self.set_attrs(self.attributes, data)
        self.object_type = "object"

    def get_id(self):
        return self.uuid
