# coding=utf-8
import datetime
import json
import logging

import docker

from management import utils
from management.kv_store import DBController
from management.models.mgmt_node import MgmtNode

logger = logging.getLogger()


def _get_docker_client(ip_list):
    for ip in ip_list:
        try:
            c = docker.DockerClient(base_url=f"tcp://{ip}", version="auto")
            return c
        except docker.errors.DockerException as e:
            print(e)
    raise e


def add_mgmt_node(ip_port):
    db_controller = DBController()
    baseboard_sn = utils.get_baseboard_sn()
    node = db_controller.get_mgmt_node_by_id(baseboard_sn)
    if node:
        logger.warning("Node already exists in the cluster")

    node = MgmtNode()
    node.baseboard_sn = baseboard_sn
    node.system_uuid = utils.get_system_id()
    node.hostname = utils.get_hostname()
    node.docker_ip_port = ip_port
    node.status = 'active'
    node.write_to_db(db_controller.kv_store)
    logger.info("Done")
    return True


def list_mgmt_nodes(is_json):
    db_controller = DBController()
    nodes = db_controller.get_mgmt_nodes()
    data = []
    output = ""

    for node in nodes:
        logging.debug(node)
        logging.debug("*" * 20)
        data.append({
            "Hostname": node.hostname,
            "Docker IP:PORT": node.docker_ip_port,
            "Status": node.status,
        })

    if not data:
        return output

    if is_json:
        output = json.dumps(data, indent=2)
    else:
        output = utils.print_table(data)
    return output


def remove_mgmt_node(hostname):
    db_controller = DBController()
    logging.info("removing mgmt node")
    snode = db_controller.get_mgmt_node_by_hostname(hostname)
    if not snode:
        logger.error("can not find node")
        exit(1)
    snode.remove(db_controller.kv_store)
    logging.info("done")


def show_cluster():
    db_controller = DBController()
    nodes = db_controller.get_mgmt_nodes()
    if not nodes:
        logger.error("No mgmt nodes was found in the cluster!")
        exit(1)

    docker_ips = [node.docker_ip_port for node in nodes]
    c = _get_docker_client(docker_ips)
    nl = c.nodes.list()
    nodes = []
    for n in nl:
        nodes.append({
            "Hostname": n.attrs['Description']['Hostname'],
            "IP": n.attrs['ManagerStatus']['Addr'].split(":")[0],
            "Status": n.attrs['Status']['State'],
            "UpdatedAt": datetime.datetime.strptime(n.attrs['UpdatedAt'][:26], "%Y-%m-%dT%H:%M:%S.%f").strftime(
                "%H:%M:%S, %d/%m/%Y"),
        })
    return utils.print_table(nodes)


def cluster_status():
    db_controller = DBController()
    nodes = db_controller.get_mgmt_nodes()
    if not nodes:
        logger.error("No mgmt nodes was found in the cluster!")
        exit(1)

    docker_ips = [node.docker_ip_port for node in nodes]
    c = _get_docker_client(docker_ips)
    ns = c.nodes.list()
    total_nodes = len(ns)
    active_nodes = 0
    lead_node = None
    for n in ns:
        if n.attrs['Status']['State'] == 'ready':
            active_nodes += 1
        if 'Leader' in n.attrs['ManagerStatus'] and n.attrs['ManagerStatus']['Leader']:
            lead_node = n.attrs['Description']['Hostname']

    status = {
        "Status": "Online",
        "Active Nodes": active_nodes,
        "Total nodes": total_nodes,
        "Leader": lead_node
    }

    return utils.print_table([status])
