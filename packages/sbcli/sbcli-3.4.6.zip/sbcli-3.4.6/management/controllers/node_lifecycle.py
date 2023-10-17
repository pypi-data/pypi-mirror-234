# coding=utf-8
import logging
import time

from management import constants
from management import utils
from management.kv_store import DBController
from management.models.compute_node import ComputeNode
from management.models.nvme_device import NVMeDevice
from management.models.storage_node import StorageNode
from management import services
from management import spdk_installer
from management.pci_utils import bind_spdk_driver, get_nvme_devices, bind_nvme_driver
from management.rpc_client import RPCClient
from management.storage_node_ops import _get_nvme_list, _run_nvme_smart_log, _run_nvme_smart_log_add

logger = logging.getLogger()



def shutdown_storage_node(kv_store):
    db_controller = DBController(kv_store)
    baseboard_sn = utils.get_baseboard_sn()
    snode = db_controller.get_storage_node_by_id(baseboard_sn)
    if not snode:
        logger.error("This storage node is not part of the cluster")
        exit(1)

    logging.info("Node found: %s in state: %s", snode.hostname, snode.status)
    if snode.status != StorageNode.STATUS_ONLINE:
        logging.error("Node is not in online state")
        exit(1)

    logging.info("Shutting down node")
    snode.status = StorageNode.STATUS_IN_SHUTDOWN
    snode.write_to_db(kv_store)

    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    logger.info("Stopping spdk_nvmf_tgt service")
    nvmf_service = services.spdk_nvmf_tgt
    if nvmf_service.is_service_running():
        nvmf_service.service_stop()

    # make shutdown request
    response = rpc_client.shutdown_node(snode.get_id())
    if 'result' in response and response['result']:
        logging.info("Setting node status to Offline")
        snode.status = StorageNode.STATUS_OFFLINE
        snode.write_to_db(kv_store)
        logger.info("Done")
        return True
    else:
        logger.error("Error shutting down node")
        logger.debug(response)
        exit(1)


def suspend_storage_node(kv_store):
    #  in this case all process must be running
    db_controller = DBController(kv_store)
    baseboard_sn = utils.get_baseboard_sn()
    snode = db_controller.get_storage_node_by_id(baseboard_sn)
    if not snode:
        logger.error("This storage node is not part of the cluster")
        exit(1)

    logging.info("Node found: %s in state: %s", snode.hostname, snode.status)
    if snode.status != StorageNode.STATUS_ONLINE:
        logging.error("Node is not in online state")
        exit(1)

    logging.info("Suspending node")

    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    # make suspend request
    response = rpc_client.suspend_node(snode.get_id())
    if 'result' in response and response['result']:
        logging.info("Setting node status to suspended")
        snode.status = StorageNode.STATUS_SUSPENDED
        snode.write_to_db(kv_store)
        logger.info("Done")
        return True
    else:
        logger.error("Error suspending node")
        logger.debug(response)
        exit(1)


def resume_storage_node(kv_store):
    db_controller = DBController(kv_store)
    baseboard_sn = utils.get_baseboard_sn()
    snode = db_controller.get_storage_node_by_id(baseboard_sn)
    if not snode:
        logger.error("This storage node is not part of the cluster")
        exit(1)

    logging.info("Node found: %s in state: %s", snode.hostname, snode.status)
    if snode.status != StorageNode.STATUS_SUSPENDED:
        logging.error("Node is not in suspended state")
        exit(1)

    logging.info("Resuming node")

    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    # make suspend request
    response = rpc_client.resume_node(snode.get_id())
    if 'result' in response and response['result']:
        logging.info("Setting node status to online")
        snode.status = StorageNode.STATUS_ONLINE
        snode.write_to_db(kv_store)
        logger.info("Done")
        return True
    else:
        logger.error("Error suspending node")
        logger.debug(response)
        exit(1)


def restart_storage_node(kv_store, run_tests):
    db_controller = DBController(kv_store)
    global_settings = db_controller.get_global_settings()
    logging.info("Restarting node")
    baseboard_sn = utils.get_baseboard_sn()
    snode = db_controller.get_storage_node_by_id(baseboard_sn)
    if not snode:
        logger.error("This storage node is not part of the cluster")
        exit(1)

    logging.info("Node found: %s in state: %s", snode.hostname, snode.status)
    if snode.status != StorageNode.STATUS_OFFLINE:
        logging.error("Node is not in offline state")
        exit(1)

    logger.info("Checking spdk_nvmf_tgt service status")
    nvmf_service = services.spdk_nvmf_tgt
    if nvmf_service.is_service_running():
        logging.error("Can not restart node: %s, service spdk_nvmf_tgt is running", snode.hostname)
        exit(1)
    logger.info("Service spdk_nvmf_tgt is inactive")

    logging.info("Setting node state to restarting")
    snode.status = StorageNode.STATUS_RESTARTING
    snode.write_to_db(kv_store)

    devs = get_nvme_devices()
    logger.info("binding nvme drivers")
    for dv in devs:
        bind_nvme_driver(dv[0])
        time.sleep(1)

    logger.info("Getting NVMe drives info")
    nvme_devs = _get_nvme_list(global_settings)
    logging.debug(nvme_devs)

    logger.info("Comparing node drives and local drives")
    for node_nvme_device in snode.nvme_devices:
        logger.info("checking device: %s ,status: %s", node_nvme_device.serial_number, node_nvme_device.status)
        if node_nvme_device in nvme_devs:
            local_nvme_device = nvme_devs[nvme_devs.index(node_nvme_device)]
            if node_nvme_device.status == local_nvme_device.status:
                logger.info("No status update needed")
            else:
                logger.info("Updating status to: %s", local_nvme_device.status)
                node_nvme_device.status = local_nvme_device.status
        else:
            logger.info("device was not found on the node, status will be set to removed")
            node_nvme_device.status = NVMeDevice.STATUS_REMOVED
    logger.debug(snode.nvme_devices)

    # run smart log test
    if run_tests:
        logger.info("Running tests")
        for node_nvme_device in snode.nvme_devices:
            device_name = node_nvme_device.device_name
            logger.debug("Running smart-log on device: %s", device_name)
            smart_log_data = _run_nvme_smart_log(device_name)
            if "critical_warning" in smart_log_data:
                critical_warnings = smart_log_data["critical_warning"]
                if critical_warnings > 0:
                    logger.info("Critical warnings found: %s on device: %s, setting drive to failed state" %
                                (critical_warnings, device_name))
                    node_nvme_device.status = NVMeDevice.STATUS_FAILED
            logger.debug("Running smart-log-add on device: %s", device_name)
            additional_smart_log = _run_nvme_smart_log_add(device_name)
            program_fail_count = additional_smart_log['Device stats']['program_fail_count']['normalized']
            erase_fail_count = additional_smart_log['Device stats']['erase_fail_count']['normalized']
            crc_error_count = additional_smart_log['Device stats']['crc_error_count']['normalized']
            if program_fail_count < global_settings.NVME_PROGRAM_FAIL_COUNT:
                node_nvme_device.status = NVMeDevice.STATUS_FAILED
                logger.info("program_fail_count: %s is below %s on drive: %s, setting drive to failed state",
                            program_fail_count, global_settings.NVME_PROGRAM_FAIL_COUNT, device_name)
            if erase_fail_count < global_settings.NVME_ERASE_FAIL_COUNT:
                node_nvme_device.status = NVMeDevice.STATUS_FAILED
                logger.info("erase_fail_count: %s is below %s on drive: %s, setting drive to failed state",
                            erase_fail_count, global_settings.NVME_ERASE_FAIL_COUNT, device_name)
            if crc_error_count < global_settings.NVME_CRC_ERROR_COUNT:
                node_nvme_device.status = NVMeDevice.STATUS_FAILED
                logger.info("crc_error_count: %s is below %s on drive: %s, setting drive to failed state",
                            crc_error_count, global_settings.NVME_CRC_ERROR_COUNT, device_name)

    snode.write_to_db(kv_store)

    # Reinstall spdk service
    nvmf_service.service_remove()
    nvmf_service.init_service()

    # Reinstall spdk rpc service
    rpc_ip = snode.mgmt_ip
    rpc_user = snode.rpc_username
    rpc_pass = snode.rpc_password
    rpc_srv = services.rpc_http_proxy
    rpc_srv.args = [rpc_ip, str(constants.RPC_HTTP_PROXY_PORT), rpc_user,  rpc_pass]
    rpc_srv.service_remove()
    time.sleep(3)
    rpc_srv.init_service()


    # Creating monitors services
    logger.info("Creating ultra_node_monitor service")
    nm_srv = services.ultra_node_monitor
    nm_srv.service_remove()
    nm_srv.init_service()
    dm_srv = services.ultra_device_monitor
    dm_srv.service_remove()
    dm_srv.init_service()
    sc_srv = services.ultra_stat_collector
    sc_srv.service_remove()
    sc_srv.init_service()

    logger.info("binding spdk drivers")
    for dv in devs:
        bind_spdk_driver(dv[0])
        time.sleep(1)

    subsystem_nqn = snode.subsystem
    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    # add subsystems
    logger.info("getting subsystem list")
    subsystem_list = rpc_client.subsystem_list()
    logger.debug(subsystem_list)
    subsystem = [x for x in subsystem_list if x['nqn'] == subsystem_nqn]
    if subsystem:
        logger.info("subsystem exist, skipping creation")
    else:
        logger.info("creating subsystem %s", subsystem_nqn)
        ret = rpc_client.subsystem_create(
            subsystem_nqn, snode.nvme_devices[0].serial_number, snode.nvme_devices[0].model_id)
        logger.debug(ret)
        ret = rpc_client.subsystem_list()
        logger.debug(ret)

    # add rdma transport
    logger.info("getting transport list")
    ret = rpc_client.transport_list()
    logger.debug(ret)
    rdma_tr = [x for x in ret if x['trtype'] == "RDMA"]
    if rdma_tr:
        logger.info("RDMA transport exist, skipping creation")
    else:
        logger.info("creating RDMA transport")
        ret = rpc_client.transport_create('RDMA')
        logger.debug(ret)

    # add listeners
    logger.info("adding listeners")
    for iface in snode.ib_devices:
        if iface.ip4_address:
            logger.info("adding listener for %s on IP %s" % (subsystem_nqn, iface.ip4_address))
            ret = rpc_client.listeners_create(subsystem_nqn, "RDMA", iface.ip4_address, "4420")
            logger.debug(ret)

    logger.debug("getting listeners")
    ret = rpc_client.listeners_list(subsystem_nqn)
    logger.debug(ret)

    # add compute nodes to allowed hosts
    logger.info("Adding Active Compute nodes to the node's whitelist")
    cnodes = ComputeNode().read_from_db(kv_store)

    for node in cnodes:
        if node.status == node.STATUS_ONLINE:
            logger.info("Active compute node found on host: %s" % node.hostname)
            ret = rpc_client.subsystem_add_host(subsystem_nqn, node.host_nqn)
            logger.debug(ret)

    # attach bdev controllers
    for index, nvme in enumerate(snode.nvme_devices):
        if nvme.status in [NVMeDevice.STATUS_AVAILABLE, NVMeDevice.STATUS_READONLY,
                           NVMeDevice.STATUS_REMOVED, NVMeDevice.STATUS_UNRECOGNIZED]:
            logger.info("adding controller")
            ret = rpc_client.bdev_nvme_controller_attach("nvme_ultr21a_%s" % nvme.sequential_number, nvme.pcie_address)
            logger.debug(ret)

    logger.debug("controllers list")
    ret = rpc_client.bdev_nvme_controller_list()
    logger.debug(ret)

   # TODO: Don't create nvme partitions
   #  device_to_partition, status_ns = create_partitions_arrays(global_settings, snode.nvme_devices)
   #  out_data = {
   #      'device_to_partition': device_to_partition,
   #      'status_ns': status_ns,
   #      'NS_LB_SIZE': global_settings.NS_LB_SIZE,
   #      'NS_SIZE_IN_LBS': global_settings.NS_SIZE_IN_LBS}
   #  rpc_client.create_nvme_partitions(out_data)

    # allocate bdevs
    logger.info("Allocating bdevs")
    for index, nvme in enumerate(snode.nvme_devices):
        if nvme.status in [NVMeDevice.STATUS_AVAILABLE, NVMeDevice.STATUS_READONLY,
                           NVMeDevice.STATUS_REMOVED, NVMeDevice.STATUS_UNRECOGNIZED]:
            ret = rpc_client.allocate_bdev(nvme.device_name, nvme.sequential_number)
            logger.debug(ret)

    # creating namespaces
    logger.info("Creating namespaces")
    for index, nvme in enumerate(snode.nvme_devices):
        if nvme.status in [NVMeDevice.STATUS_AVAILABLE, NVMeDevice.STATUS_READONLY,
                           NVMeDevice.STATUS_REMOVED, NVMeDevice.STATUS_UNRECOGNIZED]:
            ret = rpc_client.nvmf_subsystem_add_ns(subsystem_nqn, nvme.device_name)
            logger.debug(ret)

    logging.info("Setting node status to Active")
    snode.status = StorageNode.STATUS_ONLINE
    snode.write_to_db(kv_store)
    logger.info("Done")

