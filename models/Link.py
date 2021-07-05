from utils.logs import log

class Link:
    def __init__(self, host):
        self.host = host
        self.pending_package = []
        self.package = 0

    def sending_request(self, package):
        self.pending_package.append(package)
        log(f'     Link: sending package to request controller from host[{self.host.node.id}]')
        self.host.requestController.add_queue(self.host)

    def send_package_to_physical(self):
        self.package = self.pending_package.pop(0)
        self.host.physical.send_package(self.package)

    def receive_package_to_physical(self, package):
        log(f'     Link: receive package |{package.type}| from Physical Layer and send to Network Layer')
        self.host.network.receive_package(package)
