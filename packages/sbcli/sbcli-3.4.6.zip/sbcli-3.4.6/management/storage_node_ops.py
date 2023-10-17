# coding=utf-8
import datetime
import json
import logging
import math
import pprint
import random

import string
import time
import uuid

import docker

from management import constants, scripts, distr_controller
from management import utils
from management.kv_store import DBController
from management import shell_utils
from management.models.compute_node import ComputeNode
from management.models.device_stat import DeviceStat
from management.models.iface import IFace
from management.models.nvme_device import NVMeDevice
from management.models.storage_node import StorageNode
from management import services
from management import spdk_installer
from management.pci_utils import get_nvme_devices, bind_nvme_driver, bind_spdk_driver
from management.rpc_client import RPCClient
from management.snode_client import SNodeClient

logger = logging.getLogger()


class StorageOpsException(Exception):
    def __init__(self, message):
        self.message = message


def _get_ib_devices():
    return _get_data_nics([])


def _get_data_nics(data_nics):
    if not data_nics:
        return
    out, _, _ = shell_utils.run_command("ip -j address show")
    data = json.loads(out)
    logger.debug("ifaces")
    logger.debug(pprint.pformat(data))

    def _get_ip4_address(list_of_addr):
        if list_of_addr:
            for data in list_of_addr:
                if data['family'] == 'inet':
                    return data['local']
        return ""
    devices = {i["ifname"]: i for i in data}
    iface_list = []
    for nic in data_nics:
        if nic not in devices:
            continue
        device = devices[nic]
        iface = IFace({
            'uuid': str(uuid.uuid4()),
            'if_name': device['ifname'],
            'ip4_address': _get_ip4_address(device['addr_info']),
            'port_number': 1,  # TODO: check this value
            'status': device['operstate'],
            'net_type': device['link_type']})
        iface_list.append(iface)

    return iface_list


def _get_if_ip_address(ifname):
    out, _, _ = shell_utils.run_command("ip -j address show %s" % ifname)
    data = json.loads(out)
    logger.debug(pprint.pformat(data))
    if data:
        data = data[0]
        if 'addr_info' in data and data['addr_info']:
            address_info = data['addr_info']
            for adr in address_info:
                if adr['family'] == 'inet':
                    return adr['local']
    logger.error("IP not found for interface %s", ifname)
    exit(1)


def addNvmeDevices(cluster, rpc_client, devs, snode):
    sequential_number = 0
    devices = []
    ret = rpc_client.bdev_nvme_controller_list()
    ctr_map = {i["ctrlrs"][0]['trid']['traddr']: i["name"] for i in ret}

    for index, (pcie, vid) in enumerate(devs):

        if vid in constants.SSD_VENDOR_WHITE_LIST:
            if pcie in ctr_map:
                nvme_bdev = ctr_map[pcie] + "n1"
            else:
                name = "nvme_%s" % pcie.split(":")[2].split(".")[0]
                ret, err = rpc_client.bdev_nvme_controller_attach(name, pcie)
                time.sleep(2)
                nvme_bdev = f"{name}n1"

            ret = rpc_client.get_bdevs(nvme_bdev)
            if ret:
                nvme_dict = ret[0]
                nvme_driver_data = nvme_dict['driver_specific']['nvme'][0]
                model_number = nvme_driver_data['ctrlr_data']['model_number']
                if model_number not in cluster.model_ids:
                    logger.warning("Device model ID is not recognized: %s, "
                                   "skipping device: %s", model_number)
                    continue
                size = nvme_dict['block_size'] * nvme_dict['num_blocks']
                device_partitions_count = int(size / (cluster.blk_size * cluster.page_size_in_blocks))
                devices.append(
                    NVMeDevice({
                        'uuid': str(uuid.uuid4()),
                        'device_name': nvme_dict['name'],
                        'sequential_number': sequential_number,
                        'partitions_count': device_partitions_count,
                        'capacity': size,
                        'size': size,
                        'pcie_address': nvme_driver_data['pci_address'],
                        'model_id': model_number,
                        'serial_number': nvme_driver_data['ctrlr_data']['serial_number'],
                        'nvme_bdev': nvme_bdev,
                        'alloc_bdev': nvme_bdev,
                        'node_id': snode.get_id(),
                        'status': 'online'
                    }))
                sequential_number += device_partitions_count
    return devices


def _get_nvme_list_from_file(cluster):
    devs = get_nvme_devices()
    logger.info("Getting nvme devices")
    logger.debug(devs)
    sequential_number = 0
    devices = []
    for index, (pcie, vid) in enumerate(devs):
        name = "nvme%s" % index
        if vid in constants.SSD_VENDOR_WHITE_LIST:

            model_number = 'Amazon EC2 NVMe Instance Storage'
            if model_number not in cluster.model_ids:
                logger.warning("Device model ID is not recognized: %s, "
                               "skipping device", model_number)
                continue
            size = 7500000000000
            device_partitions_count = int(size / (cluster.blk_size * cluster.page_size_in_blocks))
            devices.append(
                NVMeDevice({
                    'uuid': str(uuid.uuid4()),
                    'device_name': name,
                    'sequential_number': sequential_number,
                    'partitions_count': device_partitions_count,
                    'capacity': size,
                    'size': size,
                    'pcie_address': pcie,
                    'model_id': model_number,
                    'serial_number': "AWS22A4E8CF2CD844ED9",
                    'status': 'Active'
                }))
            sequential_number += device_partitions_count
    return devices


def _get_nvme_list(cluster):
    out, err, _ = shell_utils.run_command("sudo nvme list -v -o json")
    data = json.loads(out)
    logger.debug("nvme list:")
    logger.debug(pprint.pformat(data))

    def _get_pcie_controller(ctrl_list):
        if ctrl_list:
            for item in ctrl_list:
                if 'Transport' in item and item['Transport'] == 'pcie':
                    return item

    def _get_size_from_namespaces(namespaces):
        size = 0
        if namespaces:
            for ns in namespaces:
                size += ns['PhysicalSize']
        return size

    sequential_number = 0
    devices = []
    if data and 'Devices' in data:
        for dev in data['Devices'][0]['Subsystems']:
            controller = _get_pcie_controller(dev['Controllers'])
            if not controller:
                continue

            if controller['ModelNumber'] not in cluster.model_ids:
                logger.info("Device model ID is not recognized: %s, skipping device: %s",
                            controller['ModelNumber'], controller['Controller'])
                continue

            size = _get_size_from_namespaces(controller['Namespaces'])
            device_partitions_count = int(size / (cluster.blk_size * cluster.page_size_in_blocks))
            devices.append(
                NVMeDevice({
                    'device_name': controller['Controller'],
                    'sequential_number': sequential_number,
                    'partitions_count': device_partitions_count,
                    'capacity': size,
                    'size': size,
                    'pcie_address': controller['Address'],
                    'model_id': controller['ModelNumber'],
                    'serial_number': controller['SerialNumber'],
                    # 'status': controller['State']
                }))
            sequential_number += device_partitions_count
    return devices


def generate_rpc_user_and_pass():
    def _generate_string(length):
        return ''.join(random.SystemRandom().choice(
            string.ascii_letters + string.digits) for _ in range(length))

    return _generate_string(8), _generate_string(16)


def create_partitions_arrays(global_settings, nvme_devs):
    sequential_number = 0
    device_to_partition = {}
    for index, nvme in enumerate(nvme_devs):
        device_number = index + 1
        device_size = nvme.size
        device_partitions_count = int(device_size / (global_settings.NS_LB_SIZE * global_settings.NS_SIZE_IN_LBS))
        for device_partition_index in range(device_partitions_count):
            device_to_partition[sequential_number + device_partition_index] = (
                device_number, (global_settings.NS_SIZE_IN_LBS * device_partition_index))
        sequential_number += device_partitions_count
    status_ns = {i: 'Active' for i in range(sequential_number)}
    return device_to_partition, status_ns


def _run_nvme_smart_log(dev_name):
    out, _, _ = shell_utils.run_command("sudo nvme smart-log /dev/%s -o json" % dev_name)
    data = json.loads(out)
    logger.debug(out)
    return data


def _run_nvme_smart_log_add(dev_name):
    out, _, _ = shell_utils.run_command("sudo nvme intel smart-log-add /dev/%s --json" % dev_name)
    data = json.loads(out)
    logger.debug(out)
    return data


def get_next_cluster_device_order(db_controller):
    max_order = 0
    for node in db_controller.get_storage_nodes():
        for dev in node.nvme_devices:
            max_order = max(max_order, dev.cluster_device_order)
    if max_order > 0:
        return max_order+1
    return 0



def _prepare_cluster_devices(snode):
    db_controller = DBController()

    rpc_client = RPCClient(
        snode.mgmt_ip, snode.rpc_port,
        snode.rpc_username, snode.rpc_password)

    for index, nvme in enumerate(snode.nvme_devices):
        if nvme.status != "online":
            logger.debug(f"Device is not online: {nvme.get_id()}, status: {nvme.status}")
            continue
        alceml_id = nvme.get_id()
        node_id_mini = snode.get_id().split("-")[-1]
        alceml_id_mini = alceml_id.split("-")[-1]
        alceml_name = f"node_{node_id_mini}_dev_{alceml_id_mini}"
        logger.info(f"adding {alceml_name}")
        ret = rpc_client.bdev_alceml_create(alceml_name, nvme.nvme_bdev, alceml_id)
        if not ret:
            logger.error(f"Failed to create alceml bdev: {alceml_name}")

        # add pass through
        pt_name = f"{alceml_name}_PT"
        ret = rpc_client.bdev_PT_NoExcl_create(pt_name, alceml_name)
        if not ret:
            logger.error(f"Failed to create pt noexcl bdev: {pt_name}")

        subsystem_nqn = snode.subsystem + ":dev:" + alceml_id
        logger.info("creating subsystem %s", subsystem_nqn)
        ret = rpc_client.subsystem_create(subsystem_nqn, 'sbcli-cn', alceml_id)
        IP = None
        for iface in snode.data_nics:
            if iface.ip4_address:
                tr_type = iface.get_transport_type()
                ret = rpc_client.transport_create(tr_type)
                logger.info("adding listener for %s on IP %s" % (subsystem_nqn, iface.ip4_address))
                ret = rpc_client.listeners_create(subsystem_nqn, tr_type, iface.ip4_address, "4420")
                IP = iface.ip4_address
                break
        logger.info(f"add {pt_name} to subsystem")
        ret = rpc_client.nvmf_subsystem_add_ns(subsystem_nqn, pt_name)

        nvme.alceml_bdev = alceml_name
        nvme.pt_bdev = pt_name
        nvme.nvmf_nqn = subsystem_nqn
        nvme.nvmf_ip = IP
        nvme.nvmf_port = 4420
        nvme.status = "online"
    snode.write_to_db(db_controller.kv_store)


def _connect_to_remote_devs(this_node):
    db_controller = DBController()

    rpc_client = RPCClient(
        this_node.mgmt_ip, this_node.rpc_port,
        this_node.rpc_username, this_node.rpc_password)

    remote_devices = []
    # connect to remote devs
    snodes = db_controller.get_storage_nodes()
    for node_index, node in enumerate(snodes):
        if node.get_id() == this_node.get_id() or node.status == node.STATUS_OFFLINE:
            continue
        for index, dev in enumerate(node.nvme_devices):
            if dev.status != 'online':
                logger.debug(f"Device is not online: {dev.get_id()}, status: {dev.status}")
                continue
            name = f"remote_{dev.alceml_bdev}"
            logger.info(f"Connecting to {name}")
            ret = rpc_client.bdev_nvme_attach_controller_tcp(name, dev.nvmf_nqn, dev.nvmf_ip, dev.nvmf_port)
            dev.remote_bdev = f"{name}n1"
            remote_devices.append(dev)
    return remote_devices


def add_node(cluster_id, node_ip, iface_name, data_nics_list, spdk_cpu_mask, spdk_mem):
    db_controller = DBController()
    kv_store = db_controller.kv_store

    clusters = db_controller.get_clusters(cluster_id)
    if not clusters:
        logging.error("Cluster not found: %s", cluster_id)
        return False
    cluster = clusters[0]

    logging.info(f"Add Storage node: {node_ip}")
    snode_api = SNodeClient(node_ip)

    node_info, _ = snode_api.info()
    logging.info(f"Node info: {node_info}")

    logger.info("Deploying SPDK")
    results, err = snode_api.spdk_process_start(spdk_cpu_mask, spdk_mem)
    if not results:
        logger.error(f"Failed to start spdk: {err}")
        return False

    logger.info("Joining docker swarm...")
    cluster_docker = utils.get_docker_client(cluster_id)
    results, err = snode_api.join_swarm(
        cluster_ip=cluster_docker.info()["Swarm"]["NodeAddr"],
        join_token=cluster_docker.swarm.attrs['JoinTokens']['Worker'],
        db_connection=cluster.db_connection)

    if not results:
        logger.error(f"Failed to Join docker swarm: {err}")
        return False

    hostname = node_info['hostname']
    snode = db_controller.get_storage_node_by_hostname(hostname)
    if snode:
        logger.error("Node already exists, try remove it first.")
        return False

    data_nics = []
    names = data_nics_list or [iface_name]
    for nic in names:
        device = node_info['network_interface'][nic]
        data_nics.append(
            IFace({
                'uuid': str(uuid.uuid4()),
                'if_name': device['name'],
                'ip4_address': device['ip'],
                'status': device['status'],
                'net_type': device['net_type']}))

    rpc_user, rpc_pass = generate_rpc_user_and_pass()
    BASE_NQN = cluster.nqn.split(":")[0]
    subsystem_nqn = f"{BASE_NQN}:{hostname}"
    # creating storage node object
    snode = StorageNode()
    snode.uuid = str(uuid.uuid4())
    snode.status = StorageNode.STATUS_IN_CREATION
    snode.baseboard_sn = node_info['system_id']
    snode.system_uuid = node_info['system_id']
    snode.hostname = hostname
    snode.host_nqn = subsystem_nqn
    snode.subsystem = subsystem_nqn
    snode.data_nics = data_nics
    snode.mgmt_ip = node_info['network_interface'][iface_name]['ip']
    snode.rpc_port = constants.RPC_HTTP_PROXY_PORT
    snode.rpc_username = rpc_user
    snode.rpc_password = rpc_pass
    snode.cluster_id = cluster_id
    snode.api_endpoint = node_ip
    snode.write_to_db(kv_store)

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip, snode.rpc_port,
        snode.rpc_username, snode.rpc_password)

    devs = []
    for d in node_info['nvme_devices']:
        devs.append((d[0], d[1]))
    nvme_devs = addNvmeDevices(cluster, rpc_client, devs, snode)
    if not nvme_devs:
        logger.error("No NVMe devices was found!")

    logger.debug(nvme_devs)
    snode.nvme_devices = nvme_devs


    # Set device cluster order
    dev_order = get_next_cluster_device_order(db_controller)
    for index, nvme in enumerate(snode.nvme_devices):
        nvme.cluster_device_order = dev_order
        dev_order += 1
    snode.write_to_db(db_controller.kv_store)

    # prepare devices
    _prepare_cluster_devices(snode)

    logger.info("Connecting to remote devices")
    remote_devices = _connect_to_remote_devs(snode)
    snode.remote_devices = remote_devices

    logging.info("Setting node status to Active")
    snode.status = StorageNode.STATUS_ONLINE
    snode.write_to_db(kv_store)

    # make other nodes connect to the new devices
    logger.info("Make other nodes connect to the new devices")
    snodes = db_controller.get_storage_nodes()
    for node_index, node in enumerate(snodes):
        if node.get_id() == snode.get_id():
            continue
        logger.info(f"Connecting to node: {node.get_id()}")
        rpc_client = RPCClient(node.mgmt_ip, node.rpc_port, node.rpc_username, node.rpc_password)
        count = 0
        for dev in snode.nvme_devices:
            name = f"remote_{dev.alceml_bdev}"
            ret = rpc_client.bdev_nvme_attach_controller_tcp(name, dev.nvmf_nqn, dev.nvmf_ip, dev.nvmf_port)
            if not ret:
                logger.error(f"Failed to connect to device: {name}")
                continue

            dev.remote_bdev = f"{name}n1"
            idx = -1
            for i, d in enumerate(node.remote_devices):
                if d.get_id() == dev.get_id():
                    idx = i
                    break
            if idx >= 0:
                node.remote_devices[idx] = dev
            else:
                node.remote_devices.append(dev)
            count += 1
        node.write_to_db(kv_store)
        logger.info(f"connected to devices count: {count}")

    logging.info("Sending cluster map")
    snodes = db_controller.get_storage_nodes()
    for node in snodes:
        if node.status != node.STATUS_ONLINE:
            continue
        logger.info(f"Sending to: {node.get_id()}")
        rpc_client = RPCClient(node.mgmt_ip, node.rpc_port, node.rpc_username, node.rpc_password)
        if node.get_id() == snode.get_id():
            cluster_map_data = get_distr_cluster_map(snodes, node)
            cluster_map_data['UUID_node_target'] = node.get_id()
            ret = rpc_client.distr_send_cluster_map(cluster_map_data)
        else:
            cluster_map_data = get_distr_cluster_map([snode], node)
            cl_map = {
                "map_cluster": cluster_map_data['map_cluster'],
                "map_prob": cluster_map_data['map_prob']}
            ret = rpc_client.distr_add_nodes(cl_map)
        time.sleep(3)

    logging.info("Sending cluster event updates")
    distr_controller.send_node_status_event(snode.get_id(), "online")

    for dev in snode.nvme_devices:
        distr_controller.send_dev_status_event(dev.cluster_device_order, "online")

    logger.info("Done")
    return "Success"



def add_storage_node(cluster_id, iface_name, data_nics):
    db_controller = DBController()
    kv_store = db_controller.kv_store

    clusters = db_controller.get_clusters(cluster_id)
    if not clusters:
        logging.error("Cluster not found: %s", cluster_id)
        return False
    cluster = clusters[0]

    logging.info("Add Storage node")

    hostname = utils.get_hostname()
    snode = db_controller.get_storage_node_by_hostname(hostname)
    if snode:
        logger.error("Node already exists, try remove it first.")
        exit(1)
    else:
        snode = StorageNode()
        snode.uuid = str(uuid.uuid4())

    mgmt_ip = _get_if_ip_address(iface_name)
    system_id = utils.get_system_id()

    BASE_NQN = cluster.nqn.split(":")[0]
    subsystem_nqn = f"{BASE_NQN}:{hostname}"

    if data_nics:
        data_nics = _get_data_nics(data_nics)
    else:
        data_nics = _get_data_nics([iface_name])

    rpc_user, rpc_pass = generate_rpc_user_and_pass()

    # creating storage node object
    snode.status = StorageNode.STATUS_IN_CREATION
    snode.baseboard_sn = utils.get_baseboard_sn()
    snode.system_uuid = system_id
    snode.hostname = hostname
    snode.host_nqn = subsystem_nqn
    snode.subsystem = subsystem_nqn
    snode.data_nics = data_nics
    snode.mgmt_ip = mgmt_ip
    snode.rpc_port = constants.RPC_HTTP_PROXY_PORT
    snode.rpc_username = rpc_user
    snode.rpc_password = rpc_pass
    snode.cluster_id = cluster_id
    snode.write_to_db(kv_store)

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    logger.info("Getting nvme devices")
    devs = get_nvme_devices()
    logger.debug(devs)
    nvme_devs = addNvmeDevices(cluster, rpc_client, devs, snode)
    if not nvme_devs:
        logger.error("No NVMe devices was found!")

    logger.debug(nvme_devs)
    snode.nvme_devices = nvme_devs

    # Set device cluster order
    dev_order = get_next_cluster_device_order(db_controller)
    for index, nvme in enumerate(snode.nvme_devices):
        nvme.cluster_device_order = dev_order
        dev_order += 1
    snode.write_to_db(db_controller.kv_store)

    # prepare devices
    _prepare_cluster_devices(snode)

    logger.info("Connecting to remote devices")
    remote_devices = _connect_to_remote_devs(snode)
    snode.remote_devices = remote_devices

    logging.info("Setting node status to Active")
    snode.status = StorageNode.STATUS_ONLINE
    snode.write_to_db(kv_store)

    # make other nodes connect to the new devices
    logger.info("Make other nodes connect to the new devices")
    snodes = db_controller.get_storage_nodes()
    for node_index, node in enumerate(snodes):
        if node.get_id() == snode.get_id():
            continue
        logger.info(f"Connecting to node: {node.get_id()}")
        rpc_client = RPCClient(node.mgmt_ip, node.rpc_port, node.rpc_username, node.rpc_password)
        count = 0
        for dev in snode.nvme_devices:
            name = f"remote_{dev.alceml_bdev}"
            ret = rpc_client.bdev_nvme_attach_controller_tcp(name, dev.nvmf_nqn, dev.nvmf_ip, dev.nvmf_port)
            if not ret:
                logger.error(f"Failed to connect to device: {name}")
                continue

            dev.remote_bdev = f"{name}n1"
            idx = -1
            for i, d in enumerate(node.remote_devices):
                if d.get_id() == dev.get_id():
                    idx = i
                    break
            if idx >= 0:
                node.remote_devices[idx] = dev
            else:
                node.remote_devices.append(dev)
            count += 1
        node.write_to_db(kv_store)
        logger.info(f"connected to devices count: {count}")

    logging.info("Sending cluster map")
    snodes = db_controller.get_storage_nodes()
    for node in snodes:
        if node.status != node.STATUS_ONLINE:
            continue
        logger.info(f"Sending to: {node.get_id()}")
        rpc_client = RPCClient(node.mgmt_ip, node.rpc_port, node.rpc_username, node.rpc_password)
        if node.get_id() == snode.get_id():
            cluster_map_data = get_distr_cluster_map(snodes, node)
            cluster_map_data['UUID_node_target'] = node.get_id()
            ret = rpc_client.distr_send_cluster_map(cluster_map_data)
        else:
            cluster_map_data = get_distr_cluster_map([snode], node)
            cl_map = {
                "map_cluster": cluster_map_data['map_cluster'],
                "map_prob": cluster_map_data['map_prob']}
            ret = rpc_client.distr_add_nodes(cl_map)
        time.sleep(3)

    logging.info("Sending cluster event updates")
    distr_controller.send_node_status_event(snode.get_id(), "online")

    for dev in snode.nvme_devices:
        distr_controller.send_dev_status_event(dev.cluster_device_order, "online")

    logger.info("Done")
    return "Success"


def get_distr_cluster_map(snodes, target_node):
    map_cluster = {}
    map_prob = []
    for snode in snodes:
        if snode.status != snode.STATUS_ONLINE:
            logger.debug(f"Node is not online: {snode.get_id()}, status: {snode.status}")
            continue
        dev_map = {}
        dev_w_map = []
        node_w = 0

        for i, dev in enumerate(snode.nvme_devices):
            if dev.status != "online":
                logger.debug(f"Device is not online: {dev.get_id()}, status: {dev.status}")
                continue
            dev_w = int(dev.size/(1024*1024*1024)) or 1
            node_w += dev_w
            if snode.get_id() == target_node.get_id():
                name = dev.alceml_bdev
            else:
                name = dev.remote_bdev
            dev_map[dev.cluster_device_order] = {
                "UUID": dev.get_id(),
                "bdev_name": name,
                "status": "online"}
            dev_w_map.append({
                "weight": dev_w,
                "id": dev.cluster_device_order})
        map_cluster[snode.get_id()] = {
                "availability_group": 0,
                "status": "online",
                "devices": dev_map}
        map_prob.append({
            "weight": node_w,
            "items": dev_w_map
        })
    cl_map = {
        "name": "",
        "UUID_node_target": "",
        "timestamp": datetime.datetime.now().isoformat("T", "seconds")+'Z',
        "map_cluster": map_cluster,
        "map_prob": map_prob
    }
    return cl_map


def remove_storage_node(node_id, force=False):
    db_controller = DBController()
    snode = db_controller.get_storage_node_by_id(node_id)
    if not snode:
        logger.error(f"Can not find storage node: {node_id}")
        return False

    if snode.lvols:
        logger.error(f"Remove all lVols first")
        if force is False:
            return False

    snaps = db_controller.get_snapshots()
    for sn in snaps:
        if sn.lvol.node_id == node_id and sn.deleted is False:
            logger.error(f"Remove all snapshots first, snap Id: {sn.get_id()}")
            if force is False:
                return False


    # check if offline

    logging.info("Removing storage node")

    # send cluster events
    # disconnect devices from all other nodes
    #


    logger.info("Leaving swarm...")
    node_docker = docker.DockerClient(base_url=f"tcp://{snode.mgmt_ip}:2375", version="auto")
    try:
        cluster_docker = utils.get_docker_client(snode.cluster_id)
        cluster_docker.nodes.get(node_docker.info()["Swarm"]["NodeID"]).remove(force=True)
    except:
        pass

    try:
        node_docker.swarm.leave()
    except:
        pass

    snode_api = SNodeClient(snode.api_endpoint)
    results, err = snode_api.spdk_process_kill()

    snode.remove(db_controller.kv_store)
    logging.info("done")


def restart_storage_node(node_id, run_tests):
    db_controller = DBController()
    kv_store = db_controller.kv_store

    db_controller = DBController()
    logging.info("Restarting storage node")
    snode = db_controller.get_storage_node_by_id(node_id)
    if not snode:
        logger.error(f"Can not find storage node: {node_id}")
        return False

    logging.info("Setting node state to restarting")
    snode.status = StorageNode.STATUS_RESTARTING
    snode.write_to_db(kv_store)

    logging.info(f"Add Storage node: {snode.mgmt_ip}")
    snode_api = SNodeClient(snode.api_endpoint)

    node_info, _ = snode_api.info()
    logging.info(f"Node info: {node_info}")

    logger.info("Deploying SPDK")
    results, err = snode_api.spdk_process_start(None, None)
    if not results:
        logger.error(f"Failed to start spdk: {err}")
        return False

    clusters = db_controller.get_clusters(snode.cluster_id)
    cluster = clusters[0]
    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip, snode.rpc_port,
        snode.rpc_username, snode.rpc_password)

    devs = []
    for d in node_info['nvme_devices']:
        devs.append((d[0], d[1]))
    nvme_devs = addNvmeDevices(cluster, rpc_client, devs, snode)
    if not nvme_devs:
        logger.error("No NVMe devices was found!")

    logger.info(f"Devices found: {len(nvme_devs)}")
    logger.debug(nvme_devs)

    logger.info(f"Devices in db: {len(snode.nvme_devices)}")
    logger.debug(snode.nvme_devices)

    new_devices = []
    active_devices = []
    known_devices_sn = []
    devices_sn = [d.serial_number for d in nvme_devs]
    for db_dev in snode.nvme_devices:
        known_devices_sn.append(db_dev.serial_number)
        if db_dev.serial_number in devices_sn:
            logger.info(f"Device found: {db_dev.get_id()}")
            active_devices.append(db_dev)
            db_dev.status = "online"
        else:
            logger.info(f"Device not found: {db_dev.get_id()}")
            db_dev.status = "removed"

    for dev in nvme_devs:
        if dev.serial_number not in known_devices_sn:
            logger.info(f"New device found: {dev.get_id()}")
            dev.status = 'new'
            new_devices.append(dev)
            snode.nvme_devices.append(dev)

    # prepare devices
    _prepare_cluster_devices(snode)

    logger.info("Connecting to remote devices")
    remote_devices = _connect_to_remote_devs(snode)
    snode.remote_devices = remote_devices

    logging.info("Setting node status to Active")
    snode.status = StorageNode.STATUS_ONLINE
    snode.write_to_db(kv_store)

    # make other nodes connect to the new devices
    logger.info("Make other nodes connect to the new devices")
    snodes = db_controller.get_storage_nodes()
    for node_index, node in enumerate(snodes):
        if node.get_id() == snode.get_id():
            continue
        logger.info(f"Connecting to node: {node.get_id()}")
        rpc_client = RPCClient(node.mgmt_ip, node.rpc_port, node.rpc_username, node.rpc_password)
        count = 0
        for dev in snode.nvme_devices:
            name = f"remote_{dev.alceml_bdev}"
            ret = rpc_client.bdev_nvme_attach_controller_tcp(name, dev.nvmf_nqn, dev.nvmf_ip, dev.nvmf_port)
            if not ret:
                logger.error(f"Failed to connect to device: {name}")
                continue

            dev.remote_bdev = f"{name}n1"
            idx = -1
            for i, d in enumerate(node.remote_devices):
                if d.get_id() == dev.get_id():
                    idx = i
                    break
            if idx >= 0:
                node.remote_devices[idx] = dev
            else:
                node.remote_devices.append(dev)
            count += 1
        node.write_to_db(kv_store)
        logger.info(f"connected to devices count: {count}")

    logging.info("Sending cluster map")
    snodes = db_controller.get_storage_nodes()
    for node in snodes:
        if node.status != node.STATUS_ONLINE:
            continue
        logger.info(f"Sending to: {node.get_id()}")
        rpc_client = RPCClient(node.mgmt_ip, node.rpc_port, node.rpc_username, node.rpc_password)
        if node.get_id() == snode.get_id():
            cluster_map_data = get_distr_cluster_map(snodes, node)
            cluster_map_data['UUID_node_target'] = node.get_id()
            ret = rpc_client.distr_send_cluster_map(cluster_map_data)
        else:
            cluster_map_data = get_distr_cluster_map([snode], node)
            cl_map = {
                "map_cluster": cluster_map_data['map_cluster'],
                "map_prob": cluster_map_data['map_prob']}
            ret = rpc_client.distr_add_nodes(cl_map)
        time.sleep(3)

    logging.info("Sending cluster event updates")
    distr_controller.send_node_status_event(snode.get_id(), "online")

    for dev in snode.nvme_devices:
        distr_controller.send_dev_status_event(dev.cluster_device_order, "online")

    logger.info("Done")
    return "Success"




def list_storage_nodes(kv_store, is_json):
    db_controller = DBController(kv_store)
    nodes = db_controller.get_storage_nodes()
    data = []
    output = ""

    for node in nodes:
        logging.debug(node)
        logging.debug("*" * 20)
        data.append({
            "UUID": node.uuid,
            "Hostname": node.hostname,
            "Management IP": node.mgmt_ip,
            "Subsystem": node.subsystem,
            "NVMe Devs": f"{len(node.nvme_devices)}",
            "LVOLs": f"{len(node.lvols)}",
            "Data NICs": "\n".join([d.if_name for d in node.data_nics]),
            "Status": node.status,
            "Updated At": datetime.datetime.strptime(node.updated_at, "%Y-%m-%d %H:%M:%S.%f").strftime(
                "%H:%M:%S, %d/%m/%Y"),
        })

    if not data:
        return output

    if is_json:
        output = json.dumps(data, indent=2)
    else:
        output = utils.print_table(data)
    return output


def list_storage_devices(kv_store, node_id, sort, is_json):
    db_controller = DBController(kv_store)
    snode = db_controller.get_storage_node_by_id(node_id)
    if not snode:
        logger.error("This storage node is not part of the cluster")
        return False

    data = []
    for device in snode.nvme_devices:
        logging.debug(device)
        logging.debug("*" * 20)
        data.append({
            "UUID": device.uuid,
            "Name": device.device_name,
            "Hostname": snode.hostname,
            "Size": utils.humanbytes(device.size),
            # "Sequential Number": device.sequential_number,
            # "Partitions Count": device.partitions_count,
            # "Model ID": device.model_id,
            "Serial Number": device.serial_number,
            "PCIe": device.pcie_address,
            "Status": device.status,
        })

    if sort and sort in ['node-seq', 'dev-seq', 'serial']:
        if sort == 'serial':
            sort_key = "Serial Number"
        elif sort == 'dev-seq':
            sort_key = "Sequential Number"
        elif sort == 'node-seq':
            # TODO: check this key
            sort_key = "Sequential Number"
        sorted_data = sorted(data, key=lambda d: d[sort_key])
        data = sorted_data

    if is_json:
        return json.dumps(data, indent=2)
    else:
        return utils.print_table(data)


def shutdown_storage_node(node_id, force=False):
    db_controller = DBController()
    snode = db_controller.get_storage_node_by_id(node_id)
    if not snode:
        logger.error("This storage node is not part of the cluster")
        return False

    logging.info("Node found: %s in state: %s", snode.hostname, snode.status)
    if snode.status != StorageNode.STATUS_SUSPENDED:
        logging.error("Node is not in suspended state")
        if force is False:
            return False

    # cls = db_controller.get_clusters(id=snode.cluster_id)
    # snodes = db_controller.get_storage_nodes()
    # online_nodes = 0
    # for node in snodes:
    #     if node.status == node.STATUS_ONLINE:
    #         online_nodes += 1
    # if cls[0].ha_type == "ha" and online_nodes <= 3:
    #     logger.warning(f"Cluster mode is HA but online storage nodes are less than 3")
    #     if force is False:
    #         return False

    logging.info("Shutting down node")
    snode.status = StorageNode.STATUS_IN_SHUTDOWN
    snode.write_to_db(db_controller.kv_store)

    distr_controller.send_node_status_event(snode.get_id(), "in_shutdown")
    for dev in snode.nvme_devices:
        dev.status = 'unavailable'
        distr_controller.send_dev_status_event(dev.cluster_device_order, "unavailable")

    # shutdown node
    # make other nodes disconnect from this node
    logger.info("disconnect all other nodes connections to this node")
    snodes = db_controller.get_storage_nodes()
    node_devs_ids = [d.get_id() for d in snode.nvme_devices]
    for node in snodes:
        if node.status != node.STATUS_ONLINE or node.get_id() == node_id:
            continue
        new_remote_devices = []
        rpc_client = RPCClient(node.mgmt_ip, node.rpc_port, node.rpc_username, node.rpc_password)
        for rem_dev in node.remote_devices:
            if rem_dev.get_id() in node_devs_ids:
                ctrl_name = rem_dev.remote_bdev[:-2]
                rpc_client.bdev_nvme_detach_controller(ctrl_name)
            else:
                new_remote_devices.append(rem_dev)
        node.remote_devices = new_remote_devices
        node.write_to_db(db_controller.kv_store)

    logger.info("Stopping SPDK")
    snode_api = SNodeClient(snode.api_endpoint)
    results, err = snode_api.spdk_process_kill()

    distr_controller.send_node_status_event(snode.get_id(), "offline")

    logging.info("Setting node status to offline")
    snode.status = StorageNode.STATUS_OFFLINE
    snode.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return True


def suspend_storage_node(node_id, force=False):
    db_controller = DBController()
    snode = db_controller.get_storage_node_by_id(node_id)
    if not snode:
        logger.error("This storage node is not part of the cluster")
        return False

    logging.info("Node found: %s in state: %s", snode.hostname, snode.status)
    if snode.status != StorageNode.STATUS_ONLINE:
        logging.error("Node is not in online state")
        return False

    cls = db_controller.get_clusters(id=snode.cluster_id)
    snodes = db_controller.get_storage_nodes()
    online_nodes = 0
    for node in snodes:
        if node.status == node.STATUS_ONLINE:
            online_nodes += 1
    if cls[0].ha_type == "ha" and online_nodes <= 3:
        logger.warning(f"Cluster mode is HA but online storage nodes are less than 3")
        if force is False:
            return False

    logging.info("Suspending node")
    distr_controller.send_node_status_event(snode.get_id(), "suspended")
    for dev in snode.nvme_devices:
        dev.status = 'unavailable'
        distr_controller.send_dev_status_event(dev.cluster_device_order, "unavailable")

    logging.info("Setting node status to suspended")
    snode.status = StorageNode.STATUS_SUSPENDED
    snode.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return True


def resume_storage_node(node_id):
    db_controller = DBController()
    snode = db_controller.get_storage_node_by_id(node_id)
    if not snode:
        logger.error("This storage node is not part of the cluster")
        exit(1)

    logging.info("Node found: %s in state: %s", snode.hostname, snode.status)
    if snode.status != StorageNode.STATUS_SUSPENDED:
        logging.error("Node is not in suspended state")
        exit(1)

    logging.info("Resuming node")

    logging.info("Sending cluster event updates")
    distr_controller.send_node_status_event(snode.get_id(), "online")

    for dev in snode.nvme_devices:
        dev.status = 'online'
        distr_controller.send_dev_status_event(dev.cluster_device_order, "online")

    logging.info("Setting node status to online")
    snode.status = StorageNode.STATUS_ONLINE
    snode.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return True


def reset_storage_device(kv_store, dev_name):
    db_controller = DBController(kv_store)
    baseboard_sn = utils.get_baseboard_sn()
    snode = db_controller.get_storage_node_by_id(baseboard_sn)
    if not snode:
        logger.error("This storage node is not part of the cluster")
        exit(1)

    nvme_device = None
    for node_nvme_device in snode.nvme_devices:
        if node_nvme_device.device_name == dev_name:
            nvme_device = node_nvme_device
            break

    if nvme_device is None:
        logging.error("Device not found")
        exit(1)

    logging.info("Resetting device")

    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    # make suspend request
    response = rpc_client.reset_device(nvme_device.device_name)
    if 'result' in response and response['result']:
        logging.info("Setting device status to resetting")
        nvme_device.status = NVMeDevice.STATUS_RESETTING
        snode.write_to_db(kv_store)
        logger.info("Done")
        return True
    else:
        logger.error("Error resetting device")
        logger.debug(response)
        exit(1)


def run_test_storage_device(kv_store, dev_name):
    db_controller = DBController(kv_store)
    baseboard_sn = utils.get_baseboard_sn()
    snode = db_controller.get_storage_node_by_id(baseboard_sn)
    if not snode:
        logger.error("This storage node is not part of the cluster")
        exit(1)

    nvme_device = None
    for node_nvme_device in snode.nvme_devices:
        if node_nvme_device.device_name == dev_name:
            nvme_device = node_nvme_device
            break

    if nvme_device is None:
        logging.error("Device not found")
        exit(1)

    global_settings = db_controller.get_global_settings()
    logger.debug("Running smart-log on device: %s", dev_name)
    smart_log_data = _run_nvme_smart_log(dev_name)
    if "critical_warning" in smart_log_data:
        critical_warnings = smart_log_data["critical_warning"]
        if critical_warnings > 0:
            logger.info("Critical warnings found: %s on device: %s, setting drive to failed state" %
                        (critical_warnings, dev_name))
            nvme_device.status = NVMeDevice.STATUS_FAILED
    logger.debug("Running smart-log-add on device: %s", dev_name)
    additional_smart_log = _run_nvme_smart_log_add(dev_name)
    program_fail_count = additional_smart_log['Device stats']['program_fail_count']['normalized']
    erase_fail_count = additional_smart_log['Device stats']['erase_fail_count']['normalized']
    crc_error_count = additional_smart_log['Device stats']['crc_error_count']['normalized']
    if program_fail_count < global_settings.NVME_PROGRAM_FAIL_COUNT:
        nvme_device.status = NVMeDevice.STATUS_FAILED
        logger.info("program_fail_count: %s is below %s on drive: %s, setting drive to failed state",
                    program_fail_count, global_settings.NVME_PROGRAM_FAIL_COUNT, dev_name)
    if erase_fail_count < global_settings.NVME_ERASE_FAIL_COUNT:
        nvme_device.status = NVMeDevice.STATUS_FAILED
        logger.info("erase_fail_count: %s is below %s on drive: %s, setting drive to failed state",
                    erase_fail_count, global_settings.NVME_ERASE_FAIL_COUNT, dev_name)
    if crc_error_count < global_settings.NVME_CRC_ERROR_COUNT:
        nvme_device.status = NVMeDevice.STATUS_FAILED
        logger.info("crc_error_count: %s is below %s on drive: %s, setting drive to failed state",
                    crc_error_count, global_settings.NVME_CRC_ERROR_COUNT, dev_name)

    snode.write_to_db(kv_store)
    logger.info("Done")


def add_storage_device(dev_name, node_id, cluster_id):
    db_controller = DBController()
    kv_store = db_controller.kv_store
    clusters = db_controller.get_clusters(cluster_id)
    if not clusters:
        logging.error("Cluster not found: %s", cluster_id)
        return False
    cluster = clusters[0]

    snode = db_controller.get_storage_node_by_id(node_id)
    if not snode:
        logger.error("Node is not part of the cluster: %s", node_id)
        exit(1)

    for node_nvme_device in snode.nvme_devices:
        if node_nvme_device.device_name == dev_name:
            logging.error("Device already added to the cluster")
            exit(1)

    nvme_devs = _get_nvme_list(cluster)
    for device in nvme_devs:
        if device.device_name == dev_name:
            nvme_device = device
            break
    else:
        logging.error("Device not found: %s", dev_name)
        exit(1)

    # running smart tests
    logger.debug("Running smart-log on device: %s", dev_name)
    smart_log_data = _run_nvme_smart_log(dev_name)
    if "critical_warning" in smart_log_data:
        critical_warnings = smart_log_data["critical_warning"]
        if critical_warnings > 0:
            logger.info("Critical warnings found: %s on device: %s" % (critical_warnings, dev_name))
            exit(1)

    logger.debug("Running smart-log-add on device: %s", dev_name)
    additional_smart_log = _run_nvme_smart_log_add(dev_name)
    program_fail_count = additional_smart_log['Device stats']['program_fail_count']['normalized']
    erase_fail_count = additional_smart_log['Device stats']['erase_fail_count']['normalized']
    crc_error_count = additional_smart_log['Device stats']['crc_error_count']['normalized']
    if program_fail_count < constants.NVME_PROGRAM_FAIL_COUNT:
        logger.info("program_fail_count: %s is below %s on drive: %s",
                    program_fail_count, constants.NVME_PROGRAM_FAIL_COUNT, dev_name)
        exit(1)
    if erase_fail_count < constants.NVME_ERASE_FAIL_COUNT:
        logger.info("erase_fail_count: %s is below %s on drive: %s",
                    erase_fail_count, constants.NVME_ERASE_FAIL_COUNT, dev_name)
        exit(1)
    if crc_error_count < constants.NVME_CRC_ERROR_COUNT:
        logger.info("crc_error_count: %s is below %s on drive: %s",
                    crc_error_count, constants.NVME_CRC_ERROR_COUNT, dev_name)
        exit(1)

    logger.info("binding spdk drivers")
    bind_spdk_driver(nvme_device.pcie_address)
    time.sleep(1)

    logger.info("init device in spdk")
    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    # attach bdev controllers
    logger.info("adding controller")
    ret = rpc_client.bdev_nvme_controller_attach("nvme_ultr21a_%s" % nvme_device.sequential_number,
                                                 nvme_device.pcie_address)
    logger.debug(ret)

    logger.debug("controllers list")
    ret = rpc_client.bdev_nvme_controller_list()
    logger.debug(ret)

    # # create nvme partitions
    # device_to_partition, status_ns = create_partitions_arrays(global_settings, nvme_devs)
    # out_data = {
    #     'device_to_partition': device_to_partition,
    #     'status_ns': status_ns,
    #     'NS_LB_SIZE': global_settings.NS_LB_SIZE,
    #     'NS_SIZE_IN_LBS': global_settings.NS_SIZE_IN_LBS}
    # rpc_client.create_nvme_partitions(out_data)

    # allocate bdevs
    logger.info("Allocating bdevs")
    ret = rpc_client.allocate_bdev(nvme_device.device_name, nvme_device.sequential_number)
    logger.debug(ret)

    # creating namespaces
    logger.info("Creating namespaces")
    ret = rpc_client.nvmf_subsystem_add_ns(snode.subsystem, nvme_device.device_name)
    logger.debug(ret)

    # set device new sequential number, increase node device count
    nvme_device.sequential_number = snode.sequential_number
    snode.sequential_number += nvme_device.partitions_count
    snode.partitions_count += nvme_device.partitions_count
    snode.nvme_devices.append(nvme_device)
    snode.write_to_db(kv_store)

    # create or update cluster map
    logger.info("Updating cluster map")
    cmap = db_controller.get_cluster_map()
    cmap.recalculate_partitions()
    logger.debug(cmap)
    cmap.write_to_db(kv_store)

    logger.info("Done")
    return True


def replace_node(kv_store, old_node_name, iface_name):
    db_controller = DBController(kv_store)
    baseboard_sn = utils.get_baseboard_sn()
    this_node = db_controller.get_storage_node_by_id(baseboard_sn)
    if this_node:
        logger.error("This storage node is part of the cluster")
        exit(1)

    old_node = db_controller.get_storage_node_by_hostname(old_node_name)
    if old_node is None:
        logging.error("Old node was not found in the cluster")
        exit(1)

    logging.info("Old node found: %s in state: %s", old_node.hostname, old_node.status)
    if old_node.status != StorageNode.STATUS_OFFLINE:
        logging.error("Node is not in offline state")
        exit(1)

    logging.info("Setting old node status to removed")
    old_node.status = StorageNode.STATUS_REMOVED
    old_node.write_to_db(kv_store)

    logging.info("Replacing node")

    mgmt_ip = _get_if_ip_address(iface_name)

    # install spdk
    logger.info("Installing SPDK")
    spdk_installer.install_spdk()

    system_id = utils.get_system_id()
    hostname = utils.get_hostname()
    ib_devices = _get_data_nics([iface_name])

    nvme_devs = old_node.nvme_devices
    logger.info("binding spdk drivers")
    for dv in nvme_devs:
        bind_spdk_driver(dv.pcie_address)
        time.sleep(1)

    logger.info("Creating spdk_nvmf_tgt service")
    nvmf_srv = services.spdk_nvmf_tgt
    nvmf_srv.init_service()

    logger.info("Creating rpc_http_proxy service")
    rpc_user, rpc_pass = generate_rpc_user_and_pass()
    rpc_srv = services.rpc_http_proxy
    rpc_srv.args = [mgmt_ip, str(constants.RPC_HTTP_PROXY_PORT), rpc_user, rpc_pass]
    rpc_srv.service_remove()
    time.sleep(3)
    rpc_srv.init_service()

    # Creating monitors services
    logger.info("Creating ultra_node_monitor service")
    nm_srv = services.ultra_node_monitor
    nm_srv.init_service()
    dm_srv = services.ultra_device_monitor
    dm_srv.init_service()
    sc_srv = services.ultra_stat_collector
    sc_srv.init_service()

    # creating storage node object
    snode = StorageNode()
    snode.status = StorageNode.STATUS_IN_CREATION
    snode.baseboard_sn = baseboard_sn
    snode.system_uuid = system_id
    snode.hostname = hostname
    snode.host_nqn = old_node.host_nqn
    snode.subsystem = old_node.subsystem
    snode.nvme_devices = nvme_devs
    snode.ib_devices = ib_devices
    snode.mgmt_ip = mgmt_ip
    snode.rpc_port = constants.RPC_HTTP_PROXY_PORT
    snode.rpc_username = rpc_user
    snode.rpc_password = rpc_pass
    snode.sequential_number = old_node.sequential_number
    snode.partitions_count = old_node.partitions_count
    snode.write_to_db(kv_store)

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    subsystem_nqn = snode.subsystem

    # add subsystems
    logger.info("getting subsystem list")
    subsystem_list = rpc_client.subsystem_list()
    logger.debug(subsystem_list)
    subsystem = [x for x in subsystem_list if x['nqn'] == subsystem_nqn]
    if subsystem:
        logger.info("subsystem exist, skipping creation")
    else:
        logger.info("creating subsystem %s", subsystem_nqn)
        ret = rpc_client.subsystem_create(subsystem_nqn, nvme_devs[0].serial_number, nvme_devs[0].model_id)
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
    for iface in ib_devices:
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
    for index, nvme in enumerate(nvme_devs):
        logger.info("adding controller")
        ret = rpc_client.bdev_nvme_controller_attach("nvme_ultr21a_%s" % nvme.sequential_number, nvme.pcie_address)
        logger.debug(ret)

    logger.info("controllers list")
    ret = rpc_client.bdev_nvme_controller_list()
    logger.debug(ret)

    # create nvme partitions
    global_settings = db_controller.get_global_settings()

    device_to_partition = {}
    status_ns = {}
    for index, nvme in enumerate(nvme_devs):
        device_number = index + 1
        device_size = nvme.size
        sequential_number = nvme.sequential_number
        device_partitions_count = int(device_size / (global_settings.NS_LB_SIZE * global_settings.NS_SIZE_IN_LBS))
        for device_partition_index in range(device_partitions_count):
            device_to_partition[sequential_number + device_partition_index] = (
                device_number, (global_settings.NS_SIZE_IN_LBS * device_partition_index))
        status_ns.update(
            {i: 'Active' for i in range(sequential_number, sequential_number + device_partitions_count)})

    out_data = {
        'device_to_partition': device_to_partition,
        'status_ns': status_ns,
        'NS_LB_SIZE': global_settings.NS_LB_SIZE,
        'NS_SIZE_IN_LBS': global_settings.NS_SIZE_IN_LBS}
    rpc_client.create_nvme_partitions(out_data)

    # allocate bdevs
    logger.info("Allocating bdevs")
    for index, nvme in enumerate(nvme_devs):
        ret = rpc_client.allocate_bdev(nvme.device_name, nvme.sequential_number)
        logger.debug(ret)

    # creating namespaces
    logger.info("Creating namespaces")
    for index, nvme in enumerate(nvme_devs):
        ret = rpc_client.nvmf_subsystem_add_ns(subsystem_nqn, nvme.device_name)
        logger.debug(ret)

    logging.info("Setting node status to Active")
    snode.status = StorageNode.STATUS_ONLINE
    snode.write_to_db(kv_store)
    logger.info("Done")


def get_device_capacity(device_id, history):
    db_controller = DBController()
    device = db_controller.get_storage_devices(device_id)
    if not device:
        logger.error("device not found")

    data = db_controller.get_device_stats(device)
    out = []
    if not history:
        data = data[:1]

    for record in data:
        total_size = record.data_nr * record.pagesz
        free_size = record.freepg_cnt * record.pagesz
        util = int((total_size / free_size) * 100)
        out.append({
            "Date": time.strftime("%H:%M:%S, %d/%m/%Y", time.gmtime(record.date)),
            "drive size": utils.humanbytes(device.size),
            "provisioned": utils.humanbytes(total_size),
            "util": utils.humanbytes(free_size),
            "util_percent": f"{util}%",
        })
    return utils.print_table(out)


def get_device(device_id):
    db_controller = DBController()
    device = db_controller.get_storage_devices(device_id)
    if not device:
        logger.error("device not found")
    out = [device.get_clean_dict()]
    return utils.print_table(out)


def get_device_iostats(device_id, history):
    db_controller = DBController()
    device = db_controller.get_storage_devices(device_id)
    if not device:
        logger.error("device not found")
        return False

    data = db_controller.get_device_stats(device)
    out = []
    if not history:
        data = data[:1]

    for record in data:
        out.append({
            "Date": time.strftime("%H:%M:%S, %d/%m/%Y", time.gmtime(record.date)),
            "bytes_read": record.stats["bytes_read"],
            "read_ops": record.stats["num_read_ops"],
            "read speed /s": utils.humanbytes(record.read_bytes_per_sec),
            "read_ops /s": record.read_iops,
            "bytes_write": record.stats["bytes_written"],
            "write_ops": record.stats["num_write_ops"],
            "write speed /s": utils.humanbytes(record.write_bytes_per_sec),
            "write_ops /s": record.write_iops,
            "read_lat_ticks": record.read_latency_ticks,
            "write_lat_ticks": record.write_latency_ticks,
            "IO Error": record.stats["io_error"],
        })
    return utils.print_table(out)


def get_node_capacity(node_id, history):
    db_controller = DBController()
    this_node = db_controller.get_storage_node_by_id(node_id)
    if not this_node:
        logger.error("This storage node is not part of the cluster")
        return

    devices = this_node.nvme_devices
    out = []
    t_size = t_prov = t_util = t_perc = 0
    for dev in devices:
        try:
            record = db_controller.get_device_stats(dev)[:1]
            total_size = record.data_nr * record.pagesz
            free_size = record.freepg_cnt * record.pagesz
            util = int((total_size / free_size) * 100)
        except:
            total_size = 0
            free_size = 0
            util = 0
        out.append({
            "Name": dev.device_name,
            "drive size": utils.humanbytes(dev.size),
            "provisioned": utils.humanbytes(total_size),
            "util": utils.humanbytes(free_size),
            "util_percent": f"{util}%",
        })
        t_size += dev.size
        t_prov += total_size
        t_util += free_size
        t_perc += util
    if devices:
        utp = int(t_perc / len(out))
        out.append({
            "Name": "Total",
            "drive size": utils.humanbytes(t_size),
            "provisioned": utils.humanbytes(t_prov),
            "util": utils.humanbytes(t_util),
            "util_percent": f"{utp}%",
        })
    return utils.print_table(out)


def get_node_iostats(node_id, history):
    db_controller = DBController()

    node = db_controller.get_storage_node_by_id(node_id)
    if not node:
        logger.error("node not found")
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
    for dev in node.nvme_devices:
        record = DeviceStat(data={"uuid": dev.get_id(), "node_id": node.get_id()}).get_last(db_controller.kv_store)
        if not record:
            continue
        out.append({
            "Device": dev.device_name,
            "bytes_read (MB/s)": record.read_bytes_per_sec,
            "num_read_ops (IOPS)": record.read_iops,
            "bytes_write (MB/s)": record.write_bytes_per_sec,
            "num_write_ops (IOPS)": record.write_iops,
            "bytes_unmapped (MB/s)": record.unmapped_bytes_per_sec,
            "read_latency_ticks": record.read_latency_ticks,
            "write_latency_ticks": record.write_latency_ticks,
        })
        total_values["read_bytes_per_sec"] += record.read_bytes_per_sec
        total_values["read_iops"] += record.read_iops
        total_values["write_bytes_per_sec"] += record.write_bytes_per_sec
        total_values["write_iops"] += record.write_iops
        total_values["unmapped_bytes_per_sec"] += record.unmapped_bytes_per_sec
        total_values["read_latency_ticks"] += record.read_latency_ticks
        total_values["write_latency_ticks"] += record.write_latency_ticks

    out.append({
        "Device": "Total",
        "bytes_read (MB/s)": total_values['read_bytes_per_sec'],
        "num_read_ops (IOPS)": total_values["read_iops"],
        "bytes_write (MB/s)": total_values["write_bytes_per_sec"],
        "num_write_ops (IOPS)": total_values["write_iops"],
        "bytes_unmapped (MB/s)": total_values["unmapped_bytes_per_sec"],
        "read_latency_ticks": total_values["read_latency_ticks"],
        "write_latency_ticks": total_values["write_latency_ticks"],
    })

    return utils.print_table(out)


def get_node_ports(node_id):
    db_controller = DBController()
    node = db_controller.get_storage_node_by_id(node_id)
    if not node:
        logger.error("node not found")
        return False

    out = []
    for nic in node.data_nics:
        out.append({
            "ID": nic.get_id(),
            "Device name": nic.if_name,
            "Address": nic.ip4_address,
            "Net type": nic.get_transport_type(),
            "Status": nic.status,
        })
    return utils.print_table(out)


def get_node_port_iostats(port_id, history=None):
    db_controller = DBController()
    nodes = db_controller.get_storage_nodes()
    nd = None
    port = None
    for node in nodes:
        for nic in node.data_nics:
            if nic.get_id() == port_id:
                port = nic
                nd = node
                break

    if not port:
        logger.error("Port not found")
        return False

    limit = 20
    if history and history > 1:
        limit = history
    data = db_controller.get_port_stats(nd.get_id(), port.get_id(), limit=limit)
    out = []

    for record in data:
        out.append({
            "Date": time.strftime("%H:%M:%S, %d/%m/%Y", time.gmtime(record.date)),
            "out_speed": utils.humanbytes(record.out_speed),
            "in_speed": utils.humanbytes(record.in_speed),
            "bytes_sent": utils.humanbytes(record.bytes_sent),
            "bytes_received": utils.humanbytes(record.bytes_received),
        })
    return utils.print_table(out)


def deploy():
    logger.info("Installing dependencies")
    ret = scripts.install_deps()

    DEV_IP = utils.get_ips().split()[0]
    logger.info(f"Node IP: {DEV_IP}")

    node_docker = docker.DockerClient(base_url=f"tcp://{DEV_IP}:2375", version="auto", timeout=60 * 5)
    # create the api container
    nodes = node_docker.containers.list(all=True)
    for node in nodes:
        if node.attrs["Name"] == "/SNodeAPI":
            logger.info("SNodeAPI container found, skip deploy...")
            return False
    container = node_docker.containers.run(
        "hamdykhader/simplyblock:latest",
        "python WebApp/snode_app.py",
        detach=True,
        privileged=True,
        name="SNodeAPI",
        network_mode="host",
        volumes=[
            '/etc/foundationdb:/etc/foundationdb',
            '/var/tmp:/var/tmp',
            '/var/run:/var/run',
            '/dev:/dev',
            '/lib/modules/:/lib/modules/',
            '/sys:/sys'],
        restart_policy={"Name": "on-failure", "MaximumRetryCount": 99}
    )
    node_docker.images.pull("hamdykhader/spdk")
    return f"{DEV_IP}:5000"
