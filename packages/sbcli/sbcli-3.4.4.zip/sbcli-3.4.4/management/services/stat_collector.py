# coding=utf-8
import logging
import os
import numpy

import time
import sys
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(SCRIPT_PATH, "../.."))

from management import services, constants, kv_store
from management.rpc_client import RPCClient
from management.utils import _get_baseboard_sn


def calculate_mean_and_stdev_for_all_devices(devices_list):
    capacity_list = []
    for device in devices_list:
        capacity_list.append(device.get_capacity_percentage())
    n_array = numpy.array(capacity_list)
    mean_value = int(numpy.mean(n_array))
    st_dev = int(numpy.std(n_array))
    return mean_value, st_dev


def update_device_stats(node, device, stat):
    db_controller.add_device_stats(node, device, stat)
    device.capacity = stat['capacity']
    device_capacity_percentage = device.get_capacity_percentage()
    mean_value, st_dev = calculate_mean_and_stdev_for_all_devices(
        db_controller.get_storage_devices())
    allowed_capacity_from_stdev = (mean_value + (global_settings.DEVICE_OVERLOAD_STDEV_VALUE*st_dev))
    if device_capacity_percentage > allowed_capacity_from_stdev:
        device.status = device.STATUS_OVERLOADED
        device.overload_percentage = (device_capacity_percentage - allowed_capacity_from_stdev) / (
                100-allowed_capacity_from_stdev)
        device.write_to_db(db_store)
        logger.warning("Device %s is overloaded, device capacity percentage is %s, "
                       "allowed capacity is %s (calculated from stdev)",
                       device.device_name, device_capacity_percentage, allowed_capacity_from_stdev)

    elif device_capacity_percentage > global_settings.DEVICE_OVERLOAD_CAPACITY_THRESHOLD:
        device.status = device.STATUS_OVERLOADED
        device.overload_percentage = (device_capacity_percentage - global_settings.DEVICE_OVERLOAD_CAPACITY_THRESHOLD
                                      ) / (100-global_settings.DEVICE_OVERLOAD_CAPACITY_THRESHOLD)
        device.write_to_db(db_store)
        logger.warning("Device %s is overloaded, device capacity percentage is %s, "
                       "capacity threshold is %s",
                       device.device_name, device_capacity_percentage,
                       global_settings.DEVICE_OVERLOAD_CAPACITY_THRESHOLD)
    elif device.status == device.STATUS_OVERLOADED:
        device.status = device.STATUS_AVAILABLE
        device.write_to_db(db_store)
        logger.info("Device %s is not overloaded anymore", device.device_name)


# configure logging
logger_handler = logging.StreamHandler(stream=sys.stdout)
logger_handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
logger = logging.getLogger()
logger.addHandler(logger_handler)
logger.setLevel(logging.DEBUG)

# get DB controller
db_store = kv_store.KVStore()
db_controller = kv_store.DBController()
global_settings = db_controller.get_global_settings()

# get node object
baseboard_sn = _get_baseboard_sn()
snode = db_controller.get_storage_node_by_id(baseboard_sn)
if not snode:
    logger.error("This storage node is not part of the cluster")
    exit(1)

rpc_client = RPCClient(
    snode.mgmt_ip,
    snode.rpc_port,
    snode.rpc_username,
    snode.rpc_password)

logger.info("Starting stats collector")
while True:
    for nvme_device in snode.nvme_devices:
        # getting device stats
        logger.info("Getting device stats, device: %s", nvme_device.device_name)
        response = rpc_client.get_device_stats(snode, nvme_device.device_name)
        if 'result' in response and response['result']:
            stats = response['result']['stats']
            update_device_stats(snode, nvme_device, stats)
        else:
            logger.error("Error getting device stats, device: %s", nvme_device.device_name)
            logger.debug(response)

    time.sleep(constants.STAT_COLLECTOR_INTERVAL_SEC)
