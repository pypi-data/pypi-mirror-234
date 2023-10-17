# coding=utf-8
import logging
import math
import os
import time
import uuid

import docker
import requests

from management import utils, scripts, constants, mgmt_node_ops, storage_node_ops
from management.controllers import events_controller as ec
from management.kv_store import DBController
from management.models.cluster import Cluster
from management.models.device_stat import DeviceStat

logger = logging.getLogger()


def create_cluster(blk_size, page_size_in_blocks, ha_type, tls,
                   auth_hosts_only, cli_pass, model_ids):
    logger.info("Installing dependencies...")
    ret = scripts.install_deps()
    logger.info("Installing dependencies > Done")

    DEV_IP = utils.get_ips().split()[0]
    logger.info(f"Node IP: {DEV_IP}")

    db_connection = f"{utils.generate_string(8)}:{utils.generate_string(32)}@{DEV_IP}:4500"
    ret = scripts.set_db_config(db_connection)

    logger.info("Configuring docker swarm...")
    c = docker.DockerClient(base_url=f"tcp://{DEV_IP}:2375", version="auto")
    try:
        if c.swarm.attrs and "ID" in c.swarm.attrs:
            logger.info("Docker swarm found, leaving swarm now")
            c.swarm.leave(force=True)
            time.sleep(3)

        c.swarm.init()
        logger.info("Configuring docker swarm > Done")
    except Exception as e:
        print(e)

    if not cli_pass:
        cli_pass = utils.generate_string(10)

    logger.info("Deploying swarm stack ...")
    ret = scripts.deploy_stack(cli_pass, DEV_IP)
    # print(f"Return code: {ret}")
    logger.info("Deploying swarm stack > Done")

    logger.info("Configuring DB...")
    time.sleep(5)
    out = scripts.set_db_config_single()
    logger.info("Configuring DB > Done")

    db_controller = DBController()

    # validate cluster duplicate
    logger.info("Adding new cluster object")
    c = Cluster()
    c.uuid = str(uuid.uuid4())
    c.blk_size = blk_size
    c.page_size_in_blocks = page_size_in_blocks
    c.model_ids = model_ids
    c.ha_type = ha_type
    c.tls = tls
    c.auth_hosts_only = auth_hosts_only
    c.nqn = f"{constants.CLUSTER_NQN}:{c.uuid}"
    c.cli_pass = cli_pass
    c.secret = utils.generate_string(20)
    c.db_connection = db_connection
    c.cluster_status = Cluster.STATUS_ACTIVE
    c.updated_at = int(time.time())
    c.write_to_db(db_controller.kv_store)

    mgmt_node_ops.add_mgmt_node(f"{DEV_IP}:2375", c.uuid)

    logger.info("New Cluster has been created")
    logger.info(c.uuid)
    return c.uuid


def deploy_spdk(node_docker, spdk_cpu_mask, spdk_mem):
    nodes = node_docker.containers.list(all=True)
    for node in nodes:
        if node.attrs["Name"] == "/spdk":
            logger.info("spdk container found, skip deploy...")
            return
    container = node_docker.containers.run(
        "hamdykhader/spdk:latest",
        f"/root/scripts/run_distr.sh {spdk_cpu_mask} {spdk_mem}",
        detach=True,
        privileged=True,
        name="spdk",
        network_mode="host",
        volumes=[
            '/var/tmp:/var/tmp',
            '/dev:/dev',
            '/lib/modules/:/lib/modules/',
            '/sys:/sys'],
        restart_policy={"Name": "on-failure", "MaximumRetryCount": 99}
    )
    container2 = node_docker.containers.run(
        "hamdykhader/spdk:latest",
        "python /root/scripts/spdk_http_proxy.py",
        name="spdk_proxy",
        detach=True,
        network_mode="host",
        volumes=[
            '/var/tmp:/var/tmp',
            '/etc/foundationdb:/etc/foundationdb'],
        restart_policy={"Name": "on-failure", "MaximumRetryCount": 99}
    )
    retries = 10
    while retries > 0:
        info = node_docker.containers.get(container.attrs['Id'])
        status = info.attrs['State']["Status"]
        is_running = info.attrs['State']["Running"]
        if not is_running:
            logger.info("Container is not running, waiting...")
            time.sleep(3)
            retries -= 1
        else:
            logger.info(f"Container status: {status}, Is Running: {is_running}")
            break


def join_cluster(cluster_ip, cluster_id, role, ifname, data_nics,  spdk_cpu_mask, spdk_mem):  # role: ["management", "storage"]

    if role not in ["management", "storage", "storage-alloc"]:
        logger.error(f"Unknown role: {role}")
        return False

    try:
        resp = requests.get(f"http://{cluster_ip}/cluster/{cluster_id}")
        resp_json = resp.json()
        cluster_data = resp_json['results'][0]
        logger.info(f"Cluster found! NQN:{cluster_data['nqn']}")
        logger.debug(cluster_data)
    except Exception as e:
        logger.error("Error getting cluster data!")
        logger.error(e)
        return ""

    logger.info("Installing dependencies...")
    ret = scripts.install_deps()
    logger.info("Installing dependencies > Done")

    DEV_IP = utils.get_ips().split()[0]
    logger.info(f"Node IP: {DEV_IP}")

    db_connection = cluster_data['db_connection']
    ret = scripts.set_db_config(db_connection)

    if role == "storage":
        logger.info("Deploying SPDK")
        node_cpu_count = os.cpu_count()
        if spdk_cpu_mask:
            requested_cpu_count = len(format(int(spdk_cpu_mask, 16), 'b'))
            if requested_cpu_count > node_cpu_count:
                logger.error(f"The requested cpu count: {requested_cpu_count} "
                             f"is larger than the node's cpu count: {node_cpu_count}")
                return False
        else:
            spdk_cpu_mask = hex(int(math.pow(2, node_cpu_count))-1)
        if spdk_mem:
            spdk_mem = int(spdk_mem/(1024*1024))
        else:
            spdk_mem = 4096
        node_docker = docker.DockerClient(base_url=f"tcp://{DEV_IP}:2375", version="auto", timeout=60*5)
        deploy_spdk(node_docker, spdk_cpu_mask, spdk_mem)
        time.sleep(5)

    logger.info("Joining docker swarm...")
    db_controller = DBController()
    nodes = db_controller.get_mgmt_nodes(cluster_id=cluster_id)
    if not nodes:
        logger.error("No mgmt nodes was found in the cluster!")
        exit(1)

    try:
        cluster_docker = utils.get_docker_client(cluster_id)
        docker_ip = cluster_docker.info()["Swarm"]["NodeAddr"]

        if role == 'management':
            join_token = cluster_docker.swarm.attrs['JoinTokens']['Manager']
        else:
            join_token = cluster_docker.swarm.attrs['JoinTokens']['Worker']

        node_docker = docker.DockerClient(base_url=f"tcp://{DEV_IP}:2375", version="auto")
        if node_docker.info()["Swarm"]["LocalNodeState"] == "active":
            logger.info("Node is part of another swarm, leaving swarm")
            try:
                cluster_docker.nodes.get(node_docker.info()["Swarm"]["NodeID"]).remove(force=True)
            except:
                pass
            node_docker.swarm.leave(force=True)
            time.sleep(5)
        node_docker.swarm.join([f"{docker_ip}:2377"], join_token)

        retries = 10
        while retries > 0:
            if node_docker.info()["Swarm"]["LocalNodeState"] == "active":
                break
            logger.info("Waiting for node to be active...")
            retries -= 1
            time.sleep(2)
        logger.info("Joining docker swarm > Done")
        time.sleep(5)

    except Exception as e:
        raise e

    if role == 'management':
        mgmt_node_ops.add_mgmt_node(f"{DEV_IP}:2375", cluster_id)
        cluster_obj = db_controller.get_clusters(cluster_id)[0]
        nodes = db_controller.get_mgmt_nodes(cluster_id=cluster_id)
        if len(nodes) >= 3:
            logger.info("Waiting for FDB container to be active...")
            fdb_cont = None
            retries = 30
            while retries > 0 and fdb_cont is None:
                logger.info("Looking for FDB container...")
                for cont in node_docker.containers.list(all=True):
                    logger.debug(cont.attrs['Name'])
                    if cont.attrs['Name'].startswith("/app_fdb"):
                        fdb_cont = cont
                        break
                if fdb_cont:
                    logger.info("FDB container found")
                    break
                else:
                    retries -= 1
                    time.sleep(5)

            if not fdb_cont:
                logger.warning("FDB container was not found")
            else:
                retries = 10
                while retries > 0:
                    info = node_docker.containers.get(fdb_cont.attrs['Id'])
                    status = info.attrs['State']["Status"]
                    is_running = info.attrs['State']["Running"]
                    if not is_running:
                        logger.info("Container is not running, waiting...")
                        time.sleep(3)
                        retries -= 1
                    else:
                        logger.info(f"Container status: {status}, Is Running: {is_running}")
                    break

            logger.info("Configuring Double DB...")
            time.sleep(3)
            out = scripts.set_db_config_double()
            cluster_obj.ha_type = "ha"
            cluster_obj.write_to_db(db_controller.kv_store)
            logger.info("Configuring DB > Done")

    elif role == "storage":
        # add storage node
        fdb_cont = None
        retries = 30
        while retries > 0 and fdb_cont is None:
            logger.info("Looking for SpdkAppProxy container...")
            for cont in node_docker.containers.list(all=True):
                logger.debug(cont.attrs['Name'])
                if cont.attrs['Name'].startswith("/app_SpdkAppProxy"):
                    fdb_cont = cont
                    break
            if fdb_cont:
                logger.info("SpdkAppProxy container found")
                break
            else:
                retries -= 1
                time.sleep(5)

        if not fdb_cont:
            logger.warning("SpdkAppProxy container was not found")
        else:
            retries = 10
            while retries > 0:
                info = node_docker.containers.get(fdb_cont.attrs['Id'])
                status = info.attrs['State']["Status"]
                is_running = info.attrs['State']["Running"]
                if not is_running:
                    logger.info("Container is not running, waiting...")
                    time.sleep(3)
                    retries -= 1
                else:
                    logger.info(f"Container status: {status}, Is Running: {is_running}")
                break
        storage_node_ops.add_storage_node(cluster_id, ifname, data_nics)

    logger.info("Node joined the cluster")


def add_cluster(blk_size, page_size_in_blocks, model_ids, ha_type, tls,
                auth_hosts_only, dhchap, nqn, iscsi, cli_pass):
    db_controller = DBController()
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
    db_controller = DBController()
    cls = db_controller.get_clusters(id=cl_id)
    if not cls:
        logger.error(f"Cluster not found {cl_id}")
        return False

    cluster = cls[0]
    st = db_controller.get_storage_nodes()
    data = []
    for node in st:
        for dev in node.cluster_devices:
            node_name = db_controller.get_storage_node_by_id(dev['node_id'])
            data.append({
                "UUID": dev['id'],
                "Storage ID": dev['cluster_device_order'],
                "Size": utils.humanbytes(dev['size']),
                "Hostname": node_name.hostname,
                "Status": dev['status']
            })
    data = sorted(data, key=lambda x: x["Storage ID"])
    return utils.print_table(data)


def suspend_cluster(cl_id):
    db_controller = DBController()
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
    db_controller = DBController()
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
    db_controller = DBController()
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
    db_controller = DBController()
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
    db_controller = DBController()
    cls = db_controller.get_clusters(id=cluster_id)
    if not cls:
        logger.error(f"Cluster not found {cluster_id}")
        return False
    cl = cls[0]
    return cl.cli_pass


def get_secret(cluster_id):
    db_controller = DBController()
    cls = db_controller.get_clusters(id=cluster_id)
    if not cls:
        logger.error(f"Cluster not found {cluster_id}")
        return False
    cl = cls[0]
    return cl.secret


def set_secret(cluster_id, secret):
    db_controller = DBController()
    cls = db_controller.get_clusters(cluster_id)
    if not cls:
        logger.error(f"Cluster not found {cluster_id}")
        return False
    cl = cls[0]

    secret = secret.strip()
    if len(secret) < 20:
        return "Secret must be at least 20 char"

    cl.secret = secret
    cl.write_to_db(db_controller.kv_store)
    return "Done"
