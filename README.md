# LSA Graphing
The following Python script is able to take OSPF LSA data and turn it into an interactive graph.
## Support
Below are the current and planned devices supported.
| Technology | Supported |
| ---------- | --------- |
|  MikroTik  |    ✅     |
|  Juniper   |    ❌     |
## Requirements
### NetworkX
```bash
pip install networkx
```
### Pyvis
```bash
pip install pyvis
```
## Usage
### MikroTik
Log into a MikroTik device on your network and run the following command in terminal:
```rsc
routing ospf lsa print detail file='lsa.txt'
```
Download this file to the same directory as the main.py and run the code with the lsa file as an option (`python3 main.py lsa.txt`). A new nx.html file will be created. Open this file in your browser.
### Juniper
Coming soon...
