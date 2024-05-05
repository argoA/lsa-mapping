from dataclasses import dataclass
from pyvis.network import Network
import networkx as nx
import argparse


@dataclass
class Router:
    lsa: list

    def get_originator(self) -> str:
        """Pull the originator out of the lsa"""

        new_info = []
        originator = ""

        for i in self.lsa:
            if i:
                new_info.append(i.split())

        try:
            originator = new_info[1][0].split("=")[1]
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
                if "type=" in neighbor_entry[0]:
                    for x in neighbor_entry:
                        key, value = x.split("=")
                        neighbor[key] = value

                    neighbors.append(neighbor)

        return neighbors


def get_lsa_info(args: tuple) -> list:
    """Parse the lsa for every individual entry and create a list of Router classes"""

    routers = []
    lsa = []

    for line in args.file.readlines():
        if len(line.strip()) == 0:
            routers.append(Router(lsa))
            lsa = []

        lsa.append(line.strip("\n"))

    return routers


def create_graph(routers: list) -> None:
    """Create a graph using the information from Router class"""

    G = nx.Graph()

    for router in routers:
        originator = router.get_originator()
        neighbors = router.get_neighbors()

        for neighbor in neighbors:
            if neighbor["type"] == "stub":
                continue

            G.add_edge(originator, neighbor["id"])

    return G


def draw_graph(G: nx.Graph) -> None:
    """Function to draw the Graph and save it as .html"""

    nt = Network("1080px", "1920px")
    nt.from_nx(G)
    nt.show_buttons()

    nt.save_graph("nx.html")


def main() -> None:
    """Main script function"""

    # create user arguments
    parser = argparse.ArgumentParser(
        description="Create a graph out of an OSPF LSA .txt file."
    )
    parser.add_argument(
        "file",
        type=argparse.FileType("r"),
        help="an LSA .txt file",
    )

    args = parser.parse_args()

    G = create_graph(get_lsa_info(args))

    draw_graph(G)


if __name__ == "__main__":
    main()
