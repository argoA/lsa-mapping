from pprint import pprint
from dataclasses import dataclass

@dataclass
class Router():
    lsa: list

    def get_originator(self) -> str:
        """Pull the originator out of the lsa"""

        new_info = []

        for i in self.lsa:
            if i:
                new_info.append(i.split())

        return new_info[1][0].split('=')[1]

    def get_neighbors(self) -> list:
        """Parse the LSA for every neighbor and cost"""

        # List of dictionaries
        neighbors = []

        # Read the lsa list in reverse
        for i in reversed(self.lsa):
            neighbor = {}
            neighbor_entry = i.split()

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

def main() -> None:
    """Main script function"""
    routers = get_lsa_info()

    router = routers[600]
    originator = router.get_originator()
    neighbors = router.get_neighbors()

    pprint(originator)
    pprint(neighbors)

if __name__ == '__main__':
    main()
