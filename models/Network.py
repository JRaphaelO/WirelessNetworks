from models.Package import Package


class Network:
    def __init__(self, router) -> None:
        self.package_id = 0
        self.router = router

    def send_package(self, message: str, destination: int):
        print(message, self.router.node.id, destination)

        if message:
            package = Package(self.package_id, 'DATA', message,
                              self.router.node.id, destination)
            self.package_id += 1

            self.router.set_neighbours()
            
            for router in self.router.neighbours:
                if destination == router.node.id:	
                    break

        pass
