# coding=utf-8
import logging
import os

import time
import sys
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(SCRIPT_PATH, "../.."))

from management import services, constants, kv_store
from management.models.storage_node import StorageNode
from management.utils import _get_baseboard_sn


def set_node_online():
    logging.info("Node state is: %s", snode.status)
    if snode.status == StorageNode.STATUS_OFFLINE:
        logging.info("Changing node state to online")
        snode.status = StorageNode.STATUS_ONLINE
        snode.write_to_db(db_store)


def set_node_offline():
    logging.info("Node state is: %s", snode.status)
    if snode.status not in [StorageNode.STATUS_IN_CREATION, StorageNode.STATUS_REPLACED]:
        logging.info("Changing node state to offline")
        snode.status = StorageNode.STATUS_OFFLINE
        snode.write_to_db(db_store)


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
db_controller = kv_store.DBController()

# get node object
baseboard_sn = _get_baseboard_sn()
snode = db_controller.get_storage_node_by_id(baseboard_sn)
if not snode:
    logger.error("This storage node is not part of the cluster")
    exit(1)

logger.info("Starting node monitor")
while True:
    logger.info("Scanning node services")
    if nvmf_srv.is_service_running():
        logger.info("SPDK service is active")
        if rpc_srv.is_service_running():
            logger.info("RPC service is active")
            set_node_online()
        else:
            logger.info("RPC service is inactive")
            set_node_offline()
    else:
        logger.info("SPDK service is inactive")
        set_node_offline()

    time.sleep(constants.NODE_MONITOR_INTERVAL_SEC)
