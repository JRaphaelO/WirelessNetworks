import matplotlib.pyplot as plt
import random

def random_color():
    random_color_value = lambda: random.randint(0,255)
    random_color = ('#%02X%02X%02X35' % (random_color_value(),random_color_value(),random_color_value()))
    return random_color

def generate_nodes_graph(nodes, x_min, y_min, x_max, y_max):
    fig, ax = plt.subplots(figsize=(6, 8))
    
    for idx, node in enumerate(nodes):
        circle_range = plt.Circle((node.position["x"], node.position["y"]), node.radius, color=random_color(), fill=True)
        ax.add_patch(circle_range)
        ax.text(x=node.position["x"] - 0.5, y=node.position["y"] + 0.5, s=f'h{idx}', c="#022E57")
        ax.plot(node.position["x"], node.position["y"], f'o', color='#005A8D') 
        
    if y_min < 0: ax.axvline(x=0, ymin=y_min, ymax=y_max, linewidth=1, linestyle="--", color='black') 
    if x_min < 0: ax.axhline(xmin=x_min, xmax=x_max, y=0, linewidth=1, linestyle="--", color='black') 
    
    ax.set_title('Nós utilizados na rede', fontsize=14, fontweight='bold')
    ax.set_xlim((x_min, x_max))
    ax.set_ylim((y_min, y_max))
    plt.savefig(fname="./results/initial_nodes")
    # plt.show()
