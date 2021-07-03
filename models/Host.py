from models.RequestController import RequestController
from models.Link import Link
import numpy as np
from models.Node import Node
from models.Network import Network
from models.Physical import Physical


class Host:
    def __init__(self, node: Node, requestController: RequestController, package_ID_Counter):
        self.node = node
        self.requestController = requestController
        self.network = Network(self, package_ID_Counter)
        self.link = Link(self)
        self.physical = Physical(self)
        self.hosts = []
        self.routes = {} 
        self.neighbours = set()

    def set_hosts(self, hosts):
        self.hosts: list[self] = hosts

    def send_message(self, message: str, destination: int):
        self.network.send_package(message, destination)
        
    def check_destiny(self, destiny: int):
        return destiny in self.routes

    def set_neighbours(self):
        origin_node_axis = np.array(
            (self.node.position["x"], self.node.position["y"]))

        for host in self.hosts:
            destiny_node_axis = np.array(
                (host.node.position["x"], host.node.position["y"]))
            node_distance = np.linalg.norm(
                origin_node_axis - destiny_node_axis)
            
            if node_distance < self.node.radius:
                self.neighbours.add(host)
