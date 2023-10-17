# coding=utf-8
import logging
import time
import uuid

import docker

from management import utils
from management.controllers import events_controller as ec
from management.kv_store import DBController
from management.models.cluster import Cluster
from management.models.device_stat import DeviceStat

logger = logging.getLogger()
db_controller = DBController()


def add_cluster(blk_size, page_size_in_blocks, model_ids, ha_type, tls,
                auth_hosts_only, dhchap, nqn, iscsi, cli_pass):
    logger.info("Adding new cluster")
    c = Cluster()
    c.uuid = str(uuid.uuid4())
    c.blk_size = blk_size
    c.page_size_in_blocks = page_size_in_blocks
    c.model_ids = model_ids
    c.ha_type = ha_type
    c.tls = tls
    c.auth_hosts_only = auth_hosts_only
    c.nqn = nqn
    c.iscsi = iscsi
    c.dhchap = dhchap
    c.cli_pass = cli_pass
    c.cluster_status = Cluster.STATUS_ACTIVE
    c.updated_at = int(time.time())
    c.write_to_db(db_controller.kv_store)
    logger.info("New Cluster has been created")
    logger.info(c.uuid)


def show_cluster(cl_id):
    cls = db_controller.get_clusters(id=cl_id)
    if not cls:
        logger.error(f"Cluster not found {cl_id}")
        return False

    st = db_controller.get_storage_nodes()
    mt = db_controller.get_mgmt_nodes()

    data = []
    for cl in cls:
        data.append({
            "UUID": cl.id,
            "NQN": cl.nqn,
            "ha_type": cl.ha_type,
            "tls": cl.tls,
            "mgmt nodes": len(mt),
            "storage nodes": len(st),
            "Status": cl.cluster_status,
        })
    return utils.print_table(data)


def suspend_cluster(cl_id):
    cls = db_controller.get_clusters(id=cl_id)
    if not cls:
        logger.error(f"Cluster not found {cl_id}")
        return False
    cl = cls[0]
    old_status = cl.status
    cl.status = Cluster.STATUS_SUSPENDED
    cl.write_to_db(db_controller.kv_store)

    ec.log_event_cluster(
        cluster_id=cl.get_id(),
        domain=ec.DOMAIN_CLUSTER,
        event=ec.EVENT_STATUS_CHANGE,
        db_object=cl,
        caused_by=ec.CAUSED_BY_CLI,
        message=f"Cluster status changed from {old_status} to {Cluster.STATUS_SUSPENDED}")

    return "Done"


def unsuspend_cluster(cl_id):
    cls = db_controller.get_clusters(id=cl_id)
    if not cls:
        logger.error(f"Cluster not found {cl_id}")
        return False
    cl = cls[0]
    old_status = cl.status
    cl.status = Cluster.STATUS_ACTIVE
    cl.write_to_db(db_controller.kv_store)
    ec.log_event_cluster(
        cluster_id=cl.get_id(),
        domain=ec.DOMAIN_CLUSTER,
        event=ec.EVENT_STATUS_CHANGE,
        db_object=cl,
        caused_by=ec.CAUSED_BY_CLI,
        message=f"Cluster status changed from {old_status} to {Cluster.STATUS_ACTIVE}")

    return "Done"


def list():
    cls = db_controller.get_clusters()
    st = db_controller.get_storage_nodes()
    mt = db_controller.get_mgmt_nodes()

    data = []
    for cl in cls:
        data.append({
            "UUID": cl.id,
            "NQN": cl.nqn,
            "ha_type": cl.ha_type,
            "tls": cl.tls,
            "mgmt nodes": len(mt),
            "storage nodes": len(st),
            "Status": cl.cluster_status,
        })
    return utils.print_table(data)


def get_capacity(cluster_id):
    db_controller = DBController()
    nodes = db_controller.get_storage_nodes()
    out = []
    total_size = 0
    for this_node in nodes:
        devices = this_node.nvme_devices
        for dev in devices:
            total_size += dev.size
            out.append({
                "Node ID": this_node.uuid,
                "device name": dev.device_name,
                "provisioned": utils.humanbytes(dev.size),
                "util_percent": 0,
                "util": 0})
    out.append({
        "Node ID": "Total",
        "device name": "Total",
        "provisioned": utils.humanbytes(total_size),
        "util_percent": 0,
        "util": 0,
    })
    return utils.print_table(out)


def _get_node_io_data(node):
    total_values = {
        "node_id": node.get_id(),
        "read_bytes_per_sec": 0,
        "read_iops": 0,
        "write_bytes_per_sec": 0,
        "write_iops": 0,
        "unmapped_bytes_per_sec": 0,
        "read_latency_ticks": 0,
        "write_latency_ticks": 0,
    }
    for dev in node.nvme_devices:
        record = DeviceStat(data={"uuid": dev.get_id(), "node_id": node.get_id()}).get_last(db_controller.kv_store)
        if not record:
            continue
        total_values["read_bytes_per_sec"] += record.read_bytes_per_sec
        total_values["read_iops"] += record.read_iops
        total_values["write_bytes_per_sec"] += record.write_bytes_per_sec
        total_values["write_iops"] += record.write_iops
        total_values["unmapped_bytes_per_sec"] += record.unmapped_bytes_per_sec
        total_values["read_latency_ticks"] += record.read_latency_ticks
        total_values["write_latency_ticks"] += record.write_latency_ticks

    return total_values


def get_iostats(cluster_id):
    db_controller = DBController()
    nodes = db_controller.get_storage_nodes()
    if not nodes:
        logger.error("no nodes found")
        return False

    out = []
    total_values = {
        "read_bytes_per_sec": 0,
        "read_iops": 0,
        "write_bytes_per_sec": 0,
        "write_iops": 0,
        "unmapped_bytes_per_sec": 0,
        "read_latency_ticks": 0,
        "write_latency_ticks": 0,
    }
    for node in nodes:
        record = _get_node_io_data(node)
        if not record:
            continue
        out.append({
            "Node": record['node_id'],
            "bytes_read (MB/s)": record['read_bytes_per_sec'],
            "num_read_ops (IOPS)": record["read_iops"],
            "bytes_write (MB/s)": record["write_bytes_per_sec"],
            "num_write_ops (IOPS)": record["write_iops"],
            "bytes_unmapped (MB/s)": record["unmapped_bytes_per_sec"],
            "read_latency_ticks": record["read_latency_ticks"],
            "write_latency_ticks": record["write_latency_ticks"],
        })
        total_values["read_bytes_per_sec"] += record["read_bytes_per_sec"]
        total_values["read_iops"] += record["read_iops"]
        total_values["write_bytes_per_sec"] += record["write_bytes_per_sec"]
        total_values["write_iops"] += record["write_iops"]
        total_values["unmapped_bytes_per_sec"] += record["unmapped_bytes_per_sec"]
        total_values["read_latency_ticks"] += record["read_latency_ticks"]
        total_values["write_latency_ticks"] += record["write_latency_ticks"]

    out.append({
        "Node": "Total",
        "bytes_read (MB/s)": total_values['read_bytes_per_sec'],
        "num_read_ops (IOPS)": total_values["read_iops"],
        "bytes_write (MB/s)": total_values["write_bytes_per_sec"],
        "num_write_ops (IOPS)": total_values["write_iops"],
        "bytes_unmapped (MB/s)": total_values["unmapped_bytes_per_sec"],
        "read_latency_ticks": total_values["read_latency_ticks"],
        "write_latency_ticks": total_values["write_latency_ticks"],
    })

    return utils.print_table(out)


def get_ssh_pass(cluster_id):
    cls = db_controller.get_clusters(id=cluster_id)
    if not cls:
        logger.error(f"Cluster not found {cluster_id}")
        return False
    cl = cls[0]
    return cl.cli_pass
