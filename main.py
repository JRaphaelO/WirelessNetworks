from utils.readDataFile import readDataFile
from models.Router import Router

number_of_nodes, nodes = readDataFile('./input/nodes.txt')
routers = []

for node in nodes:
    router = Router(node)
    routers.append(router)

for idx in range(len(routers)):
    routers[idx].set_routers(routers[:idx] + routers[idx+1:])

routers[0].send_message("teste", 4)
