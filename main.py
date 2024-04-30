from dataclasses import dataclass
from pyvis.network import Network
import networkx as nx

@dataclass
class Router():
    lsa: list

    def get_originator(self) -> str:
        """Pull the originator out of the lsa"""

        new_info = []
        originator = ''

        for i in self.lsa:
            if i:
                new_info.append(i.split())

        try:
            originator = new_info[1][0].split('=')[1]
        except IndexError:
            pass

        return originator

    def get_neighbors(self) -> list:
        """Parse the LSA for neighbors information"""

        # List of neighbor dictionaries
        neighbors = []

        # Read the lsa list in reverse as neighbors are at the bottom
        for i in reversed(self.lsa):
            neighbor_entry = i.split()

            neighbor = {}
            # If list is not empty and type= is found
            if neighbor_entry:
                if 'type=' in neighbor_entry[0]:
                    for x in neighbor_entry:
                        key, value = x.split('=')
                        neighbor[key] = value

                    neighbors.append(neighbor)

        return neighbors

def get_lsa_info() -> list:
    """Parse the lsa for every individual entry and create a list of Router classes"""

    routers = []
    lsa = []

    with open('lsa.txt', 'r') as f:
        for line in f.readlines():
            if len(line.strip()) == 0:
                routers.append(Router(lsa))
                lsa = []

            lsa.append(line.strip('\n'))
 
    return routers

def create_graph(routers: list) -> None:
    """Create a graph using the information from Router class"""

    G = nx.Graph()

    for router in routers:
        originator = router.get_originator()
        neighbors = router.get_neighbors()

        for neighbor in neighbors:
            if neighbor['type'] == 'stub':
                continue

            G.add_edge(originator, neighbor['id'])

    nt = Network('1000px', '1500px')
    nt.from_nx(G)
    nt.show_buttons()

    nt.save_graph('nx.html')

def main() -> None:
    """Main script function"""

    create_graph(get_lsa_info())

if __name__ == '__main__':
    main()
