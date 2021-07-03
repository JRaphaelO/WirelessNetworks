from utils.logs import log

class Physical:
    def __init__(self, host):
        self.host = host

    def send_package(self, package):
        self.host.set_neighbours()
        neighbours = self.host.neighbours

        for neighbour in neighbours:
            log(f'     Physical: Host[{self.host.node.id}] sending package to Host[{neighbour.node.id}]')
            neighbour.physical.receive_package(package)

    def receive_package(self, package):
        self.host.link.receive_package_to_physical(package)
