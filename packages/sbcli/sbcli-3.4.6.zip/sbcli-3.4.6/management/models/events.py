# coding=utf-8
from management.models.base_model import BaseModel


class EventObj(BaseModel):
    """
    uuid:
    cluster_uuid: 1234
    event: STATUS_CHANGE
    domain: Cluster, Management, Storage
    object_name: cluster,
    object_dict:
    caused_by: CLI, API, MONITOR
    message:
    meta_data:
    date:
    """
    attributes = {
        "uuid": {"type": str, 'default': ""},
        "cluster_uuid": {"type": str, 'default': ""},
        "date": {"type": int, 'default': 0},

        "event": {"type": str, 'default': ""},
        "domain": {"type": str, 'default': ""},
        "object_name": {"type": str, 'default': ""},
        "object_dict": {"type": dict, 'default': {}},
        "caused_by": {"type": str, 'default': ""},
        "message": {"type": str, 'default': ""},
        "meta_data": {"type": str, 'default': ""},

    }

    def __init__(self, data=None):
        super(EventObj, self).__init__()
        self.set_attrs(self.attributes, data)
        self.object_type = "object"

    def get_id(self):
        return "%s/%s/%s" % (self.cluster_uuid, self.uuid, self.date)
