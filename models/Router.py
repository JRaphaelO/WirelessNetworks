import numpy as np
from models.Node import Node
from models.Network import Network


class Router:
    def __init__(self, node: Node) -> None:
        self.node = node
        self.network = Network(self)
        self.routers = []
        self.neighbours = set()

    def set_routers(self, routers):
        self.routers: list[self] = routers

    def send_message(self, message: str, destination: int):
        self.network.send_package(message, destination)

    def set_neighbours(self):
        origin_node_axis = np.array(
            (self.node.position["x"], self.node.position["y"]))
        for router in self.routers:
            destiny_node_axis = np.array(
                (router.node.position["x"], router.node.position["y"]))
            node_distance = np.linalg.norm(
                origin_node_axis - destiny_node_axis)
            if node_distance < self.node.radius:
                self.neighbours.add(router)
