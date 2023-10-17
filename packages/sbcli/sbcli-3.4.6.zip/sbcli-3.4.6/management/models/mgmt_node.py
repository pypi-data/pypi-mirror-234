# coding=utf-8

from management.models.base_model import BaseModel


class MgmtNode(BaseModel):

    attributes = {
        "baseboard_sn": {"type": str, 'default': ""},
        "system_uuid": {"type": str, 'default': ""},
        "hostname": {"type": str, 'default': ""},
        "status": {"type": str, 'default': ""},
        "docker_ip_port": {"type": str, 'default': ""},
        "cluster_id": {"type": str, 'default': ""},
    }

    def __init__(self, data=None):
        super(MgmtNode, self).__init__()
        self.set_attrs(self.attributes, data)
        self.object_type = "object"

    def get_id(self):
        return self.system_uuid
