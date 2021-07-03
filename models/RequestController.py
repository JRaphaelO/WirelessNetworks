from utils.logs import log

class RequestController:
    def __init__(self):
        self.send_queue = []
        self.sender_allowed = None

    def send_permission(self):
        if len(self.send_queue) > 0:
            self.sender_allowed = self.send_queue.pop(0)

            log(f'     Request Controller: Host[{self.sender_allowed.node.id}] is allowed to start sending');
    
            self.sender_allowed.link.send_package_to_physical()
        else:
            log(f'  Request Controller: not hosts in queue to send\n')

    def add_queue(self, host):
        log(
            f'     Request Controller: the Host[{host.node.id}] want to send a package, wait is permission to send.\n')
        self.send_queue.append(host)

    def get_all_requests(self):
        return self.send_queue
