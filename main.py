from models.Message import Message
from utils.generateNodesGraph import generate_nodes_graph
from models.RequestController import RequestController
from utils.readDataFile import readDataFile
from models.Host import Host
from models.Package_ID_Counter import Package_ID_Counter
from datetime import datetime
import logging
import csv
from utils.logs import log

logging.basicConfig(filename='results/logs.log', level=logging.INFO)
master = RequestController()

def ReadMessage(messages_file: str):
    messages = []
    with open(f'input/{messages_file}', 'r', encoding='latin-1') as messages_file:
        messages_reader = csv.reader(messages_file, delimiter=',')
        next(messages_reader)

        for line in messages_reader:
            print(line)
            message = Message(line[0], int(line[1]), int(line[2]))
            messages.append(message)
    
    return messages

def main(): 
    number_of_nodes, nodes, x_min, y_min, x_max, y_max = readDataFile('./input/nodes.txt')
    hosts = []

    # Cria os roteadores
    package_ID_Counter = Package_ID_Counter()

    for node in nodes:
        host = Host(node, master, package_ID_Counter)
        hosts.append(host)

    generate_nodes_graph(nodes, x_min, y_min, x_max, y_max)

    messages = ReadMessage(messages_file='message.csv')


    # Adiciona a lista de todos os roteadores no roteador
    for idx in range(len(hosts)):
        hosts[idx].set_hosts(hosts[:idx] + hosts[idx+1:])

    time = datetime.now()
    time = time.strftime('%d/%m/%Y %H:%M')

    log(f'Intial Time: {time}')


    count = 1

    for message in messages:
    # Envia a mensagem
        hosts[message.origin].send_message(message.message, message.destiny)

        while master.get_all_requests() != []:

            time = datetime.now()
            time = time.strftime('%d/%m/%Y %H:%M')
            log(f'\n  {count}. Time Request: {time}')

            master.send_permission()
            count += 1

        time = datetime.now()
        time = time.strftime('%d/%m/%Y %H:%M')
    
    log(f'\n\nEnd Time: {time}\n\n')

main()
