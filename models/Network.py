from utils.logs import log
from models.Package import Package
from copy import deepcopy


class Network:

    def __init__(self, host, package_ID_Counter):
        self.package_id = package_ID_Counter
        self.received_package = []
        self.pending_packages = []
        self.host = host

    def get_next_jump(self, hosts):
        for idx, host in enumerate(hosts):
            if host.node.id == self.host.node.id:
                return hosts[idx +1]


    def add_received_package(self, package_id):
        if package_id in self.received_package:
            return False
        
        self.received_package.append(package_id)
        return True

    def send_package(self, message: str, destination: int):

        if message:
            package = Package(self.package_id.get(), 'DATA', message,
                              self.host.node.id, destination)

            log(f'     Network: create DATA package from host[{self.host.node.id}] to destination host[{destination}]')
            self.package_id.add()

            self.host.set_neighbours()

            for host in self.host.neighbours:
                if destination == host.node.id:
                    log(f'     Network: host[{destination}] is my neighbour')
                    self.host.link.sending_request(package)
                    return
            
            if self.host.check_destiny(destination):
                hosts = self.host.routes[destination]
                log(f'     Network: host[{self.host.node.id}] can get into the destination')
                package.path = hosts
                package.next = self.get_next_jump(hosts)
                log(f'     Network: I\'m Sending DATA to next Host[{package.next.node.id}]')

                self.host.link.sending_request(package)  

            else:
                log(f'     Network: host[{self.host.node.id}] has no routes to host[{destination}]')
                self.pending_packages.append(package)

                package_RREQ = Package(self.package_id.get(), 'RREQ', '', self.host.node.id, package.destiny)
                self.package_id.add()

                self.received_package.append(package_RREQ.id)
                log(f'     Network: host[{self.host.node.id}] is creating a RREQ package to the host[{destination}]')
                log(f'     Network: host[{self.host.node.id}] is adding itself to the path')

                package_RREQ.path.append(self.host)
                self.host.link.sending_request(package_RREQ)

    def receive_package(self, package: Package):
        log(f'     Network: receive package |{package.type}| by Link Layer.')
        if package.type == 'DATA':
            self.receive_data_package(package)
        elif package.type == 'RREQ':
            self.receive_rreq_package(package)
        else:
            self.receive_rrep_package(package)

    def receive_data_package(self, package: Package):
        package = deepcopy(package)
        if package.destiny == self.host.node.id:
            if self.add_received_package(package.id):
                log(f'     Network: host[{self.host.node.id}] receive a package from host[{package.origin}]\n' 
                  + f'        Message is: {package.content}.')
        
        elif package.next != None and self.host.node.id == package.next.node.id:
            log(f'     Network: host[{self.host.node.id}] receives a DATA package, but I\'m not the destination')
            if self.add_received_package(package.id):
                package.next = self.get_next_jump(package.path)
                log(f'     Network: I\'m Sending DATA to next Host[{package.next.node.id}]')

                self.host.link.sending_request(package)
    
    def receive_rreq_package(self, package: Package):
        package = deepcopy(package)
        if self.host.node.id == package.destiny:
            if self.add_received_package(package.id):
                package.path.append(self.host)

                package_RREP = Package(self.package_id.get(), 'RREP', '', self.host.node.id, package.origin)
                log(f'     Network: host[{self.host.node.id}] has received a RREQ package, which is the destination')
                log(f'     Network: host[{self.host.node.id}] is sending a RREP package to host[{package.origin}]')

                self.package_id.add()

                package_RREP.path = package.path
                self.host.routes[package.origin] = package.path[::-1]
                package_RREP.next = self.host.routes[package.origin][1]

                self.host.link.sending_request(package_RREP)

        else:
            if self.add_received_package(package.id):
                log(f'     Network: host[{self.host.node.id}] I\'ve received a RREQ package, but I\'m not the destination host')
                log(f'     Network: host[{self.host.node.id}] is sending a RREQ package in broadcast')
                log(f'     Network: host[{self.host.node.id}] is adding itself to a path')

                package.path.append(self.host)
                self.host.link.sending_request(package)

    def receive_rrep_package(self, package: Package):
        package = deepcopy(package)
        if self.host.node.id == package.destiny:
            if self.add_received_package(package.id):
                log(f'     Network: host[{self.host.node.id}] has received a RREP package from the host[{package.origin}]')
                log(f'     Network: I am the origin, and I\'m sending a DATA package to host[{package.origin}]')
                
                data_package = self.pending_packages.pop(0)
                paths = deepcopy(package.path)
                while len(paths) > 2:
                    self.host.routes[paths.pop().node.id] = package.path
                
                next_host = package.path.index(package.next) + 1 
                data_package.next = package.path[next_host]
                data_package.path = package.path
                log(f'     Network: I\'m Sending DATA to next Host[{data_package.next.node.id}]')

                self.host.link.sending_request(data_package)
                

        elif self.host.node.id == package.next.node.id:
            if self.add_received_package(package.id):
                next_host = package.path.index(package.next) - 1
                
                package.next = package.path[next_host]
                log(f'     Network: host[{self.host.node.id}] I\'ve received a package from RREP, but I\'m not the destination')
                log(f'     Network: I\'m Sending RREP to next Host[{package.next.node.id}]')
                self.host.link.sending_request(package)


