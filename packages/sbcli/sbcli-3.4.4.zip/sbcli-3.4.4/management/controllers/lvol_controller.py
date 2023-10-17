# coding=utf-8
import datetime
import logging as lg
import json
import string
import random
import sys
import time

from management import utils, constants
from management.controllers import snapshot_controller, pool_controller
from management.kv_store import DBController
from management.models.pool import Pool
from management.models.storage_node import LVol
from management.rpc_client import RPCClient

logger = lg.getLogger()
db_controller = DBController()


def _generate_hex_string(length):
    def _generate_string(length):
        return ''.join(random.SystemRandom().choice(
            string.ascii_letters + string.digits) for _ in range(length))

    return _generate_string(length).encode('utf-8').hex()


def _create_crypto_lvol(rpc_client, name, base_name):
    key_name = f'key_{name}'
    key1 = _generate_hex_string(32)
    key2 = _generate_hex_string(32)
    ret = rpc_client.lvol_crypto_key_create(key_name, key1, key2)
    if not ret:
        logger.warning("failed to create crypto key")
    ret = rpc_client.lvol_crypto_create(name, base_name, key_name)
    if not ret:
        logger.error(f"failed to create crypto LVol {name}")
        return False
    return ret


def _create_compress_lvol(rpc_client, base_bdev_name):
    pm_path = constants.PMEM_DIR
    ret = rpc_client.lvol_compress_create(base_bdev_name, pm_path)
    if not ret:
        logger.error("failed to create compress LVol on the storage node")
        return False
    return ret


def ask_for_device_number(devices_list):
    question = f"Enter the device number [1-{len(devices_list)}]: "
    while True:
        sys.stdout.write(question)
        choice = str(input())
        try:
            ch = int(choice.strip())
            ch -= 1
            return devices_list[ch]
        except Exception as e:
            logger.debug(e)
            sys.stdout.write(f"Please respond with numbers 1 - {len(devices_list)}\n")


def ask_for_lvol_vuid():
    question = f"Enter VUID number: "
    while True:
        sys.stdout.write(question)
        choice = str(input())
        try:
            ch = int(choice.strip())
            return ch
        except Exception as e:
            logger.debug(e)
            sys.stdout.write(f"Please respond with numbers")


def validate_add_lvol_func(name, size, host_id_or_name, pool_id_or_name,
             max_rw_iops, max_rw_mbytes, max_r_mbytes, max_w_mbytes):
    #  Validation
    #  name validation
    if not name or name == "":
        return False, "Name can not be empty"

    #  size validation
    if size < 100 * 1024 * 1024:
        return False, "Size must be larger than 100M"

    #  host validation
    snode = db_controller.get_storage_node_by_id(host_id_or_name)
    if not snode:
        snode = db_controller.get_storage_node_by_hostname(host_id_or_name)
        if not snode:
            return False, f"Can not find storage node: {host_id_or_name}"

    if snode.status != snode.STATUS_ONLINE:
        return False, "Storage node in not Online"

    if not snode.nvme_devices:
        return False, "Storage node has no nvme devices"

    #  pool validation
    pool = None
    for p in db_controller.get_pools():
        if pool_id_or_name == p.id or pool_id_or_name == p.pool_name:
            pool = p
            break
    if not pool:
        return False, f"Pool not found: {pool_id_or_name}"

    if 0 < pool.lvol_max_size < size:
        return False, f"Pool Max LVol size is: {utils.humanbytes(pool.lvol_max_size)}, LVol size: {utils.humanbytes(size)} must be below this limit"

    if pool.pool_max_size > 0:
        total = pool_controller.get_pool_total_capacity(pool.get_id())
        if total + size > pool.pool_max_size:
            return False, f"Invalid LVol size: {utils.humanbytes(size)} " \
                          f"Pool max size has reached {utils.humanbytes(total)} of {utils.humanbytes(pool.pool_max_size)}"

    if pool.has_qos():
        if pool.max_rw_ios_per_sec > 0:
            if max_rw_iops <= 0:
                return False, "LVol must have max_rw_iops value because the Pool has it set"
            total = pool_controller.get_pool_total_rw_iops(pool.get_id())
            if max_rw_iops + total > pool.max_rw_ios_per_sec:
                return False, f"Invalid LVol max_rw_iops: {max_rw_iops} " \
                              f"Pool Max RW IOPS has reached {total} of {pool.max_rw_ios_per_sec}"

        if pool.max_rw_mbytes_per_sec > 0:
            if max_rw_mbytes <= 0:
                return False, "LVol must have max_rw_mbytes value because the Pool has it set"
            total = pool_controller.get_pool_total_rw_mbytes(pool.get_id())
            if max_rw_mbytes + total > pool.max_rw_mbytes_per_sec:
                return False, f"Invalid LVol max_rw_mbytes: {max_rw_mbytes} " \
                              f"Pool Max RW MBytes has reached {total} of {pool.max_rw_mbytes_per_sec}"

        if pool.max_r_mbytes_per_sec > 0:
            if max_r_mbytes <= 0:
                return False, "LVol must have max_r_mbytes value because the Pool has it set"
            total = pool_controller.get_pool_total_r_mbytes(pool.get_id())
            if max_r_mbytes + total > pool.max_r_mbytes_per_sec:
                return False, f"Invalid LVol max_r_mbytes: {max_r_mbytes} " \
                              f"Pool Max R MBytes has reached {total} of {pool.max_r_mbytes_per_sec}"

        if pool.max_w_mbytes_per_sec > 0:
            if max_w_mbytes <= 0:
                return False, "LVol must have max_w_mbytes value because the Pool has it set"
            total = pool_controller.get_pool_total_w_mbytes(pool.get_id())
            if max_w_mbytes + total > pool.max_w_mbytes_per_sec:
                return False, f"Invalid LVol max_w_mbytes: {max_w_mbytes} " \
                              f"Pool Max W MBytes has reached {total} of {pool.max_w_mbytes_per_sec}"

    return True, ""


def add_lvol(name, size, host_id_or_name, pool_id_or_name, use_comp, use_crypto,
             distr_vuid, distr_ndcs, distr_npcs,
             max_rw_iops, max_rw_mbytes, max_r_mbytes, max_w_mbytes,
             distr_bs=None, distr_chunk_bs=None):
    logger.info("adding LVol")

    snode = db_controller.get_storage_node_by_id(host_id_or_name)
    if not snode:
        snode = db_controller.get_storage_node_by_hostname(host_id_or_name)
        if not snode:
            return False, f"Can not find storage node: {host_id_or_name}"

    pool = None
    for p in db_controller.get_pools():
        if pool_id_or_name == p.id or pool_id_or_name == p.pool_name:
            pool = p
            break
    if not pool:
        return False, f"Pool not found: {pool_id_or_name}"

    max_rw_iops = max_rw_iops or 0
    max_rw_mbytes = max_rw_mbytes or 0
    max_r_mbytes = max_r_mbytes or 0
    max_w_mbytes = max_w_mbytes or 0

    result, error = validate_add_lvol_func(name, size, host_id_or_name, pool_id_or_name,
             max_rw_iops, max_rw_mbytes, max_r_mbytes, max_w_mbytes)

    if error:
        logger.error(error)
        return False, error

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    if not snode.nvme_devices:
        logger.error("Storage node has no nvme devices")
        return False, "Storage node has no nvme devices"

    if snode.status != snode.STATUS_ONLINE:
        logger.error("Storage node in not Online")
        return False, "Storage node in not Online"

    lvol = LVol()
    lvol.lvol_name = name
    lvol.size = size

    bdev_stack = []

    if distr_vuid == 0:
        vuid = 1 + int(random.random() * 10000)
    else:
        vuid = distr_vuid

    num_blocks = int(size/distr_bs)
    alloc_names = []
    for dev in snode.nvme_devices:
        alloc_names.append(dev.alceml_bdev)
    for dev in snode.remote_devices:
        alloc_names.append(dev.remote_bdev)
    names = ",".join(alloc_names)

    # name, vuid, ndcs, npcs, num_blocks, block_size, alloc_names
    ret = rpc_client.bdev_distrib_create(f"distr_{name}", vuid, distr_ndcs, distr_npcs, num_blocks, distr_bs, names, distr_chunk_bs)
    bdev_stack.append({"type": "distr", "name": f"distr_{name}"})
    if not ret:
        logger.error("failed to create Distr bdev")
        return False

    time.sleep(3)
    ret = rpc_client.create_lvstore(f"LVS_{vuid}", f"distr_{name}")
    bdev_stack.append({"type": "lvs", "name": f"LVS_{vuid}"})
    if not ret:
        logger.error("failed to create lvs")
        # return False
    lvol.base_bdev = f"distr_{name}"

    ret = rpc_client.create_lvol(name, size, f"LVS_{vuid}")
    bdev_stack.append({"type": "lvol", "name": f"LVS_{vuid}/{name}"})

    if not ret:
        logger.error("failed to create LVol on the storage node")
        return False, "failed to create LVol on the storage node"
    lvol_id = ret

    lvol_type = 'lvol'
    lvol_bdev = f"LVS_{vuid}/{name}"
    crypto_bdev = ''
    comp_bdev = ''
    top_bdev = lvol_bdev
    if use_crypto is True:
        crypto_bdev = _create_crypto_lvol(rpc_client, name, lvol_bdev)
        bdev_stack.append({"type": "crypto", "name": crypto_bdev})
        if not crypto_bdev:
            return False, "Error creating crypto bdev"
        lvol_type += ',crypto'
        top_bdev = crypto_bdev

    if use_comp is True:
        n = crypto_bdev if crypto_bdev else lvol_bdev
        comp_bdev = _create_compress_lvol(rpc_client, n)
        bdev_stack.append({"type": "comp", "name": comp_bdev})
        if not comp_bdev:
            return False, "Error creating comp bdev"
        lvol_type += ',compress'
        top_bdev = comp_bdev

    subsystem_nqn = snode.subsystem+":lvol:"+lvol_id
    logger.info("creating subsystem %s", subsystem_nqn)
    ret = rpc_client.subsystem_create(subsystem_nqn, 'sbcli-cn', lvol_id)
    logger.debug(ret)

    # add listeners
    logger.info("adding listeners")
    for iface in snode.data_nics:
        if iface.ip4_address:
            tr_type = iface.get_transport_type()
            ret = rpc_client.transport_create(tr_type)
            logger.info("adding listener for %s on IP %s" % (subsystem_nqn, iface.ip4_address))
            ret = rpc_client.listeners_create(subsystem_nqn, tr_type, iface.ip4_address, "4420")

    logger.info(f"add lvol {name} to subsystem")
    ret = rpc_client.nvmf_subsystem_add_ns(subsystem_nqn, top_bdev)

    lvol.bdev_stack = bdev_stack
    lvol.uuid = lvol_id
    lvol.lvol_bdev = lvol_bdev
    lvol.crypto_bdev = crypto_bdev
    lvol.comp_bdev = comp_bdev
    lvol.hostname = snode.hostname
    lvol.node_id = snode.get_id()
    lvol.mode = 'read-write'
    lvol.lvol_type = lvol_type
    lvol.nqn = subsystem_nqn

    lvol.pool_uuid = pool.id
    pool.lvols.append(lvol_id)
    pool.write_to_db(db_controller.kv_store)

    lvol.write_to_db(db_controller.kv_store)

    snode.lvols.append(lvol_id)
    snode.write_to_db(db_controller.kv_store)

    # set QOS
    if max_rw_iops or max_rw_mbytes or max_r_mbytes or max_w_mbytes:
        set_lvol(lvol_id, max_rw_iops, max_rw_mbytes, max_r_mbytes, max_w_mbytes)
    return lvol_id, None


def delete_lvol(uuid, force_delete=False):
    lvol = db_controller.get_lvol_by_id(uuid)
    if not lvol:
        logger.error(f"lvol not found: {uuid}")
        return False

    pool = db_controller.get_pool_by_id(lvol.pool_uuid)
    if pool.status == Pool.STATUS_INACTIVE:
        logger.error(f"Pool is disabled")
        return False

    logger.debug(lvol)
    snode = db_controller.get_storage_node_by_id(lvol.node_id)
    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    # soft delete LVol if it has snapshots
    snaps = db_controller.get_snapshots()
    for snap in snaps:
        if snap.lvol.get_id() == uuid:
            logger.warning(f"Soft delete LVol that has snapshots. Snapshot:{snap.get_id()}")
            lvol.deleted = True
            lvol.write_to_db(db_controller.kv_store)
            ret = rpc_client.subsystem_delete(lvol.nqn)
            logger.debug(ret)
            return True

    for bdev in lvol.bdev_stack[::-1]:
        type = bdev['type']
        name = bdev['name']
        if type == "alceml":
            ret = rpc_client.bdev_alceml_delete(name)
            if not ret:
                logger.error(f"failed to delete alceml: {name}")
            continue
        if type == "distr":
            ret = rpc_client.bdev_distrib_delete(name)
            if not ret:
                logger.error(f"failed to delete distr: {name}")
            continue
        if type == "lvs":
            ret = rpc_client.bdev_lvol_delete_lvstore(name)
            if not ret:
                logger.error(f"failed to delete lvs: {name}")
            continue
        if type == "lvol":
            ret = rpc_client.delete_lvol(name)
            if not ret:
                logger.error(f"failed to delete lvol bdev {name}")
            continue
        if type == "ultra_pt":
            ret = rpc_client.ultra21_bdev_pass_delete(name)
            if not ret:
                logger.error(f"failed to delete ultra pt {name}")
            continue
        if type == "comp":
            ret = rpc_client.lvol_compress_delete(name)
            if not ret:
                logger.error(f"failed to delete comp bdev {name}")
            continue
        if type == "crypto":
            ret = rpc_client.lvol_crypto_delete(name)
            if not ret:
                logger.error(f"failed to delete crypto bdev {name}")
            continue

    ret = rpc_client.subsystem_delete(lvol.nqn)
    logger.debug(ret)

    # remove from storage node
    snode.lvols.remove(uuid)
    snode.write_to_db(db_controller.kv_store)

    # remove from pool
    pool.lvols.remove(uuid)
    pool.write_to_db(db_controller.kv_store)

    lvol.remove(db_controller.kv_store)

    # if lvol is clone and snapshot is deleted, then delete snapshot
    if lvol.cloned_from_snap:
        snap = db_controller.get_snapshot_by_id(lvol.cloned_from_snap)
        if snap.deleted is True:
            lvols_count = 0
            for lvol in db_controller.get_lvols():
                if lvol.cloned_from_snap == snap.get_id():
                    lvols_count += 1
            if lvols_count == 0:
                snapshot_controller.delete(snap.get_id())

    logger.info("Done")
    return True


def set_lvol(uuid, max_rw_iops, max_rw_mbytes, max_r_mbytes, max_w_mbytes):
    lvol = db_controller.get_lvol_by_id(uuid)
    if not lvol:
        logger.error(f"lvol not found: {uuid}")
        return False
    pool = db_controller.get_pool_by_id(lvol.pool_uuid)
    if pool.status == Pool.STATUS_INACTIVE:
        logger.error(f"Pool is disabled")
        return False

    snode = db_controller.get_storage_node_by_hostname(lvol.hostname)
    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    rw_ios_per_sec = 0
    if max_rw_iops is not None and max_rw_iops >= 0:
        rw_ios_per_sec = max_rw_iops

    rw_mbytes_per_sec = 0
    if max_rw_mbytes is not None and max_rw_mbytes >= 0:
        rw_mbytes_per_sec = max_rw_mbytes

    r_mbytes_per_sec = 0
    if max_r_mbytes is not None and max_r_mbytes >= 0:
        r_mbytes_per_sec = max_r_mbytes

    w_mbytes_per_sec = 0
    if max_w_mbytes is not None and max_w_mbytes >= 0:
        w_mbytes_per_sec = max_w_mbytes

    ret = rpc_client.bdev_set_qos_limit(lvol.lvol_bdev, rw_ios_per_sec, rw_mbytes_per_sec, r_mbytes_per_sec, w_mbytes_per_sec)
    if not ret:
        return "Error"

    lvol.rw_ios_per_sec = rw_ios_per_sec
    lvol.rw_mbytes_per_sec = rw_mbytes_per_sec
    lvol.r_mbytes_per_sec = r_mbytes_per_sec
    lvol.w_mbytes_per_sec = w_mbytes_per_sec
    lvol.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return True


def list_lvols(is_json):
    lvols = db_controller.get_lvols()
    data = []
    for lvol in lvols:
        if lvol.deleted is True:
            continue
        logger.debug(lvol)
        data.append({
            "id": lvol.uuid,
            "name": lvol.lvol_name,
            "size": utils.humanbytes(lvol.size),
            "pool": lvol.pool_uuid,
            "hostname": lvol.hostname,
            "types": lvol.lvol_type,
            "status": "on",
        })

    if is_json:
        return json.dumps(data, indent=2)
    else:
        return utils.print_table(data)


def get_lvol(lvol_id, is_json):
    lvol = db_controller.get_lvol_by_id(lvol_id)
    if not lvol:
        logger.error(f"lvol not found: {lvol_id}")
        return False

    data = lvol.get_clean_dict()

    del data['nvme_dev']

    if is_json:
        return json.dumps(data, indent=2)
    else:
        data2 = [{"key": key, "value": data[key]} for key in data]
        return utils.print_table(data2)


def connect_lvol(uuid):
    lvol = db_controller.get_lvol_by_id(uuid)
    if not lvol:
        logger.error(f"lvol not found: {uuid}")
        return False

    snode = db_controller.get_storage_node_by_hostname(lvol.hostname)
    out = ""
    for nic in snode.data_nics:
        ip = nic.ip4_address
        out += f"sudo nvme connect --transport=tcp --traddr={ip} --trsvcid=4420 --nqn={lvol.nqn}\n"
    return out


def resize_lvol(id, new_size):
    lvol = db_controller.get_lvol_by_id(id)
    if not lvol:
        logger.error(f"LVol not found: {id}")
        return False

    pool = db_controller.get_pool_by_id(lvol.pool_uuid)
    if pool.status == Pool.STATUS_INACTIVE:
        logger.error(f"Pool is disabled")
        return False

    if lvol.size >= new_size:
        logger.error(f"New size {new_size} must be higher than the original size {lvol.size}")
        return False

    logger.info(f"Resizing LVol: {lvol.id}, new size: {lvol.size}")

    # if lvol.pool_uuid:
    #     pool = db_controller.get_pool_by_id(lvol.pool_uuid)
    #     if pool:
    #         print(pool)

    snode = db_controller.get_storage_node_by_hostname(lvol.hostname)

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    # ret = rpc_client.get_bdevs(lvol.lvol_name)
    # bdev_data = ret[0]
    # logger.debug(json.dumps(ret, indent=2))
    # print("is claimed:", bdev_data['claimed'])
    size_mb = int(new_size / (1024 * 1024))
    ret = rpc_client.resize_lvol(lvol.lvol_bdev, size_mb)
    if not ret:
        return "Error"

    lvol.size = new_size
    lvol.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return ret


def set_read_only(id):
    lvol = db_controller.get_lvol_by_id(id)
    if not lvol:
        logger.error(f"LVol not found: {id}")
        return False

    pool = db_controller.get_pool_by_id(lvol.pool_uuid)
    if pool.status == Pool.STATUS_INACTIVE:
        logger.error(f"Pool is disabled")
        return False

    logger.info(f"Setting LVol: {lvol.id} read only")

    snode = db_controller.get_storage_node_by_hostname(lvol.hostname)

    # creating RPCClient instance
    rpc_client = RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    ret = rpc_client.lvol_read_only(lvol.lvol_bdev)
    if not ret:
        return "Error"

    lvol.mode = 'read-only'
    lvol.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return True


def create_snapshot(lvol_id, snapshot_name):
    return snapshot_controller.add(lvol_id, snapshot_name)


def clone(snapshot_id, clone_name):
    return snapshot_controller.clone(snapshot_id, clone_name)


def get_capacity(id, history):
    lvol = db_controller.get_lvol_by_id(id)
    if not lvol:
        logger.error(f"lvol not found: {id}")
        return False

    out = [{
        "provisioned": lvol.size,
        "util_percent": 0,
        "util": 0,
    }]

    return utils.print_table(out)


def get_io_stats(lvol_uuid, history):
    lvol = db_controller.get_lvol_by_id(lvol_uuid)
    if not lvol:
        logger.error(f"lvol not found: {lvol_uuid}")
        return False

    if history and history > 1:
        data = db_controller.get_lvol_stats(lvol, limit=history)
    else:
        data = db_controller.get_lvol_stats(lvol, limit=1)
    out = []
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
