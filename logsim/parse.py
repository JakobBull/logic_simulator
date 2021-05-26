"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""


class Parser:

    """Parse the definition file and build the logic network.

    The parser deals with error handling. It analyses the syntactic and
    semantic correctness of the symbols it receives from the scanner, and
    then builds the logic network. If there are errors in the definition file,
    the parser detects this and tries to recover from it, giving helpful
    error messages.

    Parameters
    ----------
    names: instance of the names.Names() class.
    devices: instance of the devices.Devices() class.
    network: instance of the network.Network() class.
    monitors: instance of the monitors.Monitors() class.
    scanner: instance of the scanner.Scanner() class.

    Public methods
    --------------
    parse_network(self): Parses the circuit definition file.
    """

    def __init__(self, names, devices, network, monitors, scanner):
        """Initialise constants."""
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.scanner = scanner

        self.type = None
        self.id = None
        self.parse_errors = 0

        self.device_types = [ "NAND","AND", "NOR", "OR", "XOR", "SWITCH", "DTYPE", "CLOCK"]
        self.headings = ["NETWORK","DEVICES", "CONNECTIONS", "SIGNALS", "SETSIGNAL", "SETCLOCK", "MONITOR" ]
        self.punctuation = [";", "{", "}", "-", "="]

        self.headings_found = 0
        self.devices_defined = False
        self.connections_defined = False
        self.setsignal_defined = False
        self.setclock_defined = False
        self.monitor_defined = False



        

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        error_free = True

        while True:

            # Call for the next symbol from scanner
            self.symbol = self.scanner.get_symbol()
            
            if self.symbol in self.headings:
                if self.headings.index(self.symbol) != self.headings_found: #Check if headings are called in the right order
                    raise SyntaxError("Headings called in the wrong order")
                else:
                    self.headings_found += 1




            

        return True
