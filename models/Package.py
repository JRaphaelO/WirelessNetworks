class Package:
    def __init__(self, package_id: int, package_type: str, content: str, origin: int, destination: int) -> None:
        self.id = package_id
        self.type = package_type
        self.content = content
        self.origin = origin
        self.destination = destination
