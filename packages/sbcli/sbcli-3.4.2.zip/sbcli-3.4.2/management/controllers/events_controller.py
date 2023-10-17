import time
import uuid

from management.models.events import EventObj
from management.kv_store import DBController

EVENT_STATUS_CHANGE = "STATUS_CHANGE"
DOMAIN_CLUSTER = "cluster"
DOMAIN_MANAGEMENT = "management"
DOMAIN_STORAGE = "storage"
CAUSED_BY_CLI = "cli"
CAUSED_BY_API = "api"


def log_event_cluster(cluster_id, domain, event, db_object, caused_by, message):
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

    ds = EventObj()
    ds.uuid = str(uuid.uuid4())
    ds.cluster_uuid = cluster_id
    ds.date = int(time.time())

    ds.event = event
    ds.domain = domain
    ds.object_name = db_object.name
    ds.object_dict = db_object.get_clean_dict()
    ds.caused_by = caused_by
    ds.message = message

    db_controller = DBController()
    ds.write_to_db(db_controller.kv_store)
