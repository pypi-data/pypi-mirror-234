
def add_storage_node(cluster_id, iface_name, data_nics):
    db_controller = DBController()
    kv_store = db_controller.kv_store

    clusters = db_controller.get_clusters(cluster_id)
    if not clusters:
        logging.error("Cluster not found: %s", cluster_id)
        return False
    cluster = clusters[0]

    logging.info("Add Storage node")
    subsystem_nqn = cluster.nqn
    BASE_NQN = subsystem_nqn.split(":")[0]

    baseboard_sn = utils.get_baseboard_sn()
    snode = db_controller.get_storage_node_by_id(baseboard_sn)
    if snode:
        logger.error("Node already exists")
        #exit(1)
    else:
        snode = StorageNode()

    mgmt_ip = _get_if_ip_address(iface_name)

    system_id = utils.get_system_id()
    hostname = utils.get_hostname()
    if data_nics:
        data_nics = _get_data_nics("", data_nics)
    else:
        data_nics = _get_data_nics(iface_name, [])


    # install spdk
    logger.info("Installing SPDK")
    spdk_installer.install_spdk()


    logger.info("Creating ultra21 service")
    ultra21 = services.ultra21
    ultra21.init_service()
    time.sleep(3)
    logger.info(f"ultra21 service is running: {ultra21.is_service_running()}")
    snode.services = ["ultra21"]

    logger.info("Creating rpc_http_proxy service")
    rpc_user, rpc_pass = generate_rpc_user_and_pass()
    rpc_srv = services.rpc_http_proxy
    rpc_srv.args = [mgmt_ip, str(constants.RPC_HTTP_PROXY_PORT), rpc_user,  rpc_pass]
    rpc_srv.service_remove()
    time.sleep(3)
    rpc_srv.init_service()
    time.sleep(1)
    logger.info(f"rpc_http_proxy service is running: {rpc_srv.is_service_running()}")
    snode.services.append("rpc_http_proxy")

    # Creating monitors services
    # logger.info("Creating ultra_node_monitor service")
    # nm_srv = services.ultra_node_monitor
    # nm_srv.init_service()
    # dm_srv = services.ultra_device_monitor
    # dm_srv.init_service()
    # sc_srv = services.ultra_stat_collector
    # sc_srv.init_service()

    # creating storage node object

    snode.status = StorageNode.STATUS_IN_CREATION
    snode.baseboard_sn = baseboard_sn
    snode.uuid = baseboard_sn
    snode.system_uuid = system_id
    snode.hostname = hostname
    snode.host_nqn = f"{BASE_NQN}:{hostname}"
    snode.subsystem = subsystem_nqn
    snode.data_nics = data_nics
    snode.mgmt_ip = mgmt_ip
    snode.rpc_port = constants.RPC_HTTP_PROXY_PORT
    snode.rpc_username = rpc_user
    snode.rpc_password = rpc_pass
    snode.write_to_db(kv_store)

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    nvme_devs = _get_nvme_list_from_file(cluster)
    if not nvme_devs:
        logger.error("No NVMe devices was found!")

    logger.debug(nvme_devs)
    snode.nvme_devices = nvme_devs

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

    # add listeners
    logger.info("adding listeners")
    for iface in data_nics:
        if iface.ip4_address:
            tr_type = iface.get_transport_type()
            ret = rpc_client.transport_create(tr_type)
            logger.debug(ret)
            logger.info("adding listener for %s on IP %s" % (subsystem_nqn, iface.ip4_address))
            ret = rpc_client.listeners_create(subsystem_nqn, tr_type, iface.ip4_address, "4420")
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


    logger.debug("controllers list")
    ret = rpc_client.bdev_nvme_controller_list()
    logger.debug(ret)
    ctr_names = [i["name"] for i in ret]

    # attach bdev controllers
    for index, nvme in enumerate(nvme_devs):
        nvme.node_id = snode.get_id()
        name = "nvme_ultra_%s" % index
        if name in ctr_names:
            logger.info(f"controller exists: {name}")
            continue
        logger.info(f"adding controller: {name}")

        # ret, err = rpc_client.ultra21_alloc_ns_init(nvme.pcie_address)
        # time.sleep(5)
        ret, err = rpc_client.alloc_bdev_controller_attach(name, nvme.pcie_address)
        logger.debug(ret)
        if err:
            logger.error(err)
            continue
        bdev_name = ret['bdev_name']

        nvme.nvme_bdev = bdev_name
        # ret = rpc_client.create_lvstore("alloc_bdev_%s" % index, bdev_name)
        # logger.debug(ret)
        nvme.alloc_bdev = bdev_name

    snode.nvme_devices = nvme_devs

    logging.info("Setting node status to Active")
    snode.status = StorageNode.STATUS_ONLINE
    snode.write_to_db(kv_store)
    logger.info("Done")
    return "Success"


def remove_storage_node(kv_store, hostname):
    db_controller = DBController(kv_store)
    logging.info("removing storage node")
    snode = db_controller.get_storage_node_by_hostname(hostname)
    if not snode:
        logger.error("can not find storage node")
        exit(1)
    snode.remove(kv_store)
    logging.info("done")


def restart_storage_node(cluster_id, run_tests):
    db_controller = DBController()
    kv_store = db_controller.kv_store

    clusters = db_controller.get_clusters(cluster_id)
    if not clusters:
        logging.error("Cluster not found: %s", cluster_id)
        return False
    cluster = clusters[0]

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
    nvme_devs = _get_nvme_list(cluster)
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
            if program_fail_count < constants.NVME_PROGRAM_FAIL_COUNT:
                node_nvme_device.status = NVMeDevice.STATUS_FAILED
                logger.info("program_fail_count: %s is below %s on drive: %s, setting drive to failed state",
                            program_fail_count, constants.NVME_PROGRAM_FAIL_COUNT, device_name)
            if erase_fail_count < constants.NVME_ERASE_FAIL_COUNT:
                node_nvme_device.status = NVMeDevice.STATUS_FAILED
                logger.info("erase_fail_count: %s is below %s on drive: %s, setting drive to failed state",
                            erase_fail_count, constants.NVME_ERASE_FAIL_COUNT, device_name)
            if crc_error_count < constants.NVME_CRC_ERROR_COUNT:
                node_nvme_device.status = NVMeDevice.STATUS_FAILED
                logger.info("crc_error_count: %s is below %s on drive: %s, setting drive to failed state",
                            crc_error_count, constants.NVME_CRC_ERROR_COUNT, device_name)

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


def list_storage_nodes(kv_store, is_json):
    db_controller = DBController(kv_store)
    nodes = db_controller.get_storage_nodes()
    data = []
    output = ""

    for node in nodes:
        logging.debug(node)
        logging.debug("*" * 20)
        data.append({
            "UUID": node.get_id(),
            "Hostname": node.hostname,
            "Management IP": node.mgmt_ip,
            "Subsystem": node.subsystem,
            "NVMe Devs": f"{len(node.nvme_devices)}",
            "LVOLs": f"{len(node.lvols)}",
            "Data NICs": "\n".join([d.if_name for d in node.data_nics]),
            "Status": node.status,
            "Updated At": datetime.datetime.strptime(node.updated_at, "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M:%S, %d/%m/%Y"),
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
            "Size": device.size,
            "Sequential Number": device.sequential_number,
            "Partitions Count": device.partitions_count,
            "Model ID": device.model_id,
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
    ret = rpc_client.bdev_nvme_controller_attach("nvme_ultr21a_%s" % nvme_device.sequential_number, nvme_device.pcie_address)
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
    ib_devices = _get_data_nics(iface_name)

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
    rpc_srv.args = [mgmt_ip, str(constants.RPC_HTTP_PROXY_PORT), rpc_user,  rpc_pass]
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
