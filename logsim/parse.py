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
        self.device_names = []
        self.headings = ["NETWORK","DEVICES", "CONNECTIONS", "SIGNALS", "SETSIGNAL", "SETCLOCK", "MONITOR" ]
        self.punctuation = [";", "{", "}", "-", "="]
        self.numbers = range(20)

        self.headings_found = 0
        self.sections_complete = 0
        self.devices_parsed = False
        self.connections_parsed = False
        self.setsignal_parsed = False
        self.setclock_parsed = False
        self.monitor_parsed = False

        



        

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        

        while True:

            # Call for the next symbol from scanner
            self.symbol = self.scanner.get_symbol()
            
            if self.symbol in self.headings: #Check if symbol is a Heading
                if self.headings.index(self.symbol) != self.headings_found: #Check if headings are called in the right order
                    self.parse_errors += 1
                    raise SyntaxError("Headings called in the wrong order")
                    

                elif self.headings.index(self.symbol) != self.sections_complete:
                    self.parse_errors += 1
                    raise SyntaxError("Previous section not complete") #Check if previous section is complete before new section started
                
                    
                else:
                    self.headings_found += 1
                    # Check that next symbol is {
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol != "{":
                        raise SyntaxError("Always need to follow a heading with {")
                    else:
                        continue # New heading found so call for new symbol at start of new section

            elif self.sections_parsed == 0 and self.headings_found == 2: # Check if the section is DEVICES and parse devices
                #Sequence is name = device ;
                #Get name of device then check there's a = sign then check there's a device
                
                
                if self.symbol == "}": # Check if the Devices section is ending
                    self.devices_parsed = True
                    self.sections_complete = 1

                
                elif self.symbol.isalpha() == False:
                    self.parse_errors += 1
                    raise SyntaxError("Name of device must contain a letter")
                else:
                    self.device_names.append(self.symbol) # add symbol id to a list of device ids
                    self.symbol = self.scanner.get_symbol() #Get next symbol which should be an =
                    if self.symbol != "=":
                        self.parse_errors += 1
                        raise SyntaxError
                    else:
                        self.symbol = self.scanner.get_symbol()
                        if self.symbol not in self.device_types:
                            self.parse_errors += 1
                            raise SyntaxError("Device type not recognised")
                        else:
                            self.symbol = self.scanner.get_symbol()
                            if self.symbol != ";":
                                self.parse_errors += 1
                                raise SyntaxError
                            else:
                                continue #line passes and is in the right syntax
            
            
            elif self.setclock_parsed == 1 and self.headings_found == 3: #Check if section is CONNECTIONS and parse connections
                #Check if symbol is in the list of devices, then check for - then check what it's connected to before checking the ;
                

                if self.symbol == "}": # Check if the Connections section is ending
                    self.connection_parsed = True
                    self.sections_complete = 2
                
                if self.symbol not in self.device_names:
                    self.parse_errors += 1
                    raise SyntaxError("Device not defined")
                
                else:
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol != "-":
                        self.parse_errors += 1
                        raise SyntaxError("No - found to define connection")
                    else:
                        self.symbol = self.scanner.get_symbol()
                        



            
        

                            



                



                


            





            

        return True
