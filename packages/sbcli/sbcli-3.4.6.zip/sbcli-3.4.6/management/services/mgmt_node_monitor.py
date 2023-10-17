# coding=utf-8
import logging
import os

import time
import sys
from datetime import datetime

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(SCRIPT_PATH, "../.."))

from management import services, constants, kv_store
from management.models.storage_node import StorageNode
from management.rpc_client import RPCClient

# configure logging
logger_handler = logging.StreamHandler(stream=sys.stdout)
logger_handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
logger = logging.getLogger()
logger.addHandler(logger_handler)
logger.setLevel(logging.DEBUG)

# get service object
nvmf_srv = services.spdk_nvmf_tgt
rpc_srv = services.rpc_http_proxy

# get DB controller
db_store = kv_store.KVStore()
db_controller = kv_store.DBController(kv_store=db_store)


def set_node_online(snode):
    if snode.status == StorageNode.STATUS_OFFLINE:
        snode = db_controller.get_storage_node_by_id(snode.get_id())
        snode.status = StorageNode.STATUS_ONLINE
        snode.updated_at = str(datetime.now())
        snode.write_to_db(db_store)


def set_node_offline(snode):
    if snode.status not in [StorageNode.STATUS_IN_CREATION, StorageNode.STATUS_REPLACED]:
        snode = db_controller.get_storage_node_by_id(snode.get_id())
        snode.status = StorageNode.STATUS_OFFLINE
        snode.updated_at = str(datetime.now())
        snode.write_to_db(db_store)


def ping_host(ip):
    logger.info(f"Pinging ip {ip}")
    response = os.system(f"ping -c 1 {ip}")
    if response == 0:
        logger.info(f"{ip} is UP")
        return True
    else:
        logger.info(f"{ip} is DOWN")
        return False


logger.setLevel(constants.LOG_LEVEL)
logger.info("Starting node monitor")

while True:
    # get storage nodes
    nodes = db_controller.get_storage_nodes()
    for node in nodes:
        logger.info(f"Checking node {node.hostname}")
        if not ping_host(node.mgmt_ip):
            logger.info(f"Node {node.hostname} is offline")
            set_node_offline(node)
            continue
        rpc_client = RPCClient(
            node.mgmt_ip,
            node.rpc_port,
            node.rpc_username,
            node.rpc_password)
        try:
            logger.info(f"Calling rpc get_version...")
            response = rpc_client.get_version()
            if response:
                logger.info(f"Node {node.hostname} is online")
                set_node_online(node)
            else:
                logger.info(f"Node {node.hostname} is offline")
                set_node_offline(node)
        except Exception as e:
            logger.info(f"Error connecting to node: {node.hostname}")
            print(e)
            logger.info(f"Setting node status to offline")
            set_node_offline(node)

    logger.info(f"Sleeping for {constants.NODE_MONITOR_INTERVAL_SEC} seconds")
    time.sleep(constants.NODE_MONITOR_INTERVAL_SEC)
