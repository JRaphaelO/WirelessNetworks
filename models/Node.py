class Node:
    def __init__(self, node_id: int, x: int, y: int, radius: float):
        self.id = node_id
        self.position = {
                          "x": x,
                          "y": y
                         }
        self.radius = radius
