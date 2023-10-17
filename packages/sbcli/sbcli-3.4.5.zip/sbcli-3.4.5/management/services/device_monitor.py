# coding=utf-8
import logging
import os

import time
import sys


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(SCRIPT_PATH, "../.."))

from management import services, constants, kv_store
from management.rpc_client import RPCClient
from management.utils import _get_baseboard_sn


def update_device_status(device, status):
    logging.info("Device state is: %s", device.status)
    if device.status != status:
        logging.info("Changing device state to: %s", status)
        device.status = status


# configure logging
logger_handler = logging.StreamHandler(stream=sys.stdout)
logger_handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
logger = logging.getLogger()
logger.addHandler(logger_handler)
logger.setLevel(logging.DEBUG)

# get DB controller
db_store = kv_store.KVStore()
db_controller = kv_store.DBController()

# get node object
baseboard_sn = _get_baseboard_sn()
snode = db_controller.get_storage_node_by_id(baseboard_sn)
if not snode:
    logger.error("This storage node is not part of the cluster")
    exit(1)

logger.info("Starting device monitor")

rpc_client = RPCClient(
    snode.mgmt_ip,
    snode.rpc_port,
    snode.rpc_username,
    snode.rpc_password)

while True:
    for nvme_device in snode.nvme_devices:
        # getting device status
        response = rpc_client.get_device_status(nvme_device.device_name)
        if 'result' in response and response['result']:
            status = response['result']['status']
            update_device_status(nvme_device, status)
        else:
            logger.error("Error getting device status, device: %s", nvme_device.device_name)
            logger.debug(response)
    snode.write_to_db(db_store)
    time.sleep(constants.DEVICE_MONITOR_INTERVAL_SEC)
