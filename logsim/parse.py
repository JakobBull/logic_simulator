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
        self.gate_var_inputs_IDs = [5, 6, 7, 8]
        self.new_device_id = None
        self.new_device_type = None
        self.numbers = range(20)

        self.headings_found = 0
        self.sections_complete = 0
        self.devices_parsed = False
        self.connections_parsed = False
        self.setsignal_parsed = False
        self.setclock_parsed = False
        self.monitor_parsed = False
        self.input_list = []
        self.input_number = None
        self.input_I = None

        



        

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        

        while True:

            # Call for the next symbol from scanner
            self.symbol = self.scanner.get_symbol()
            
            if self.symbol.type == self.scanner.KEYWORD: #Check if symbol is a Heading
                #print('Keyword')
                #print(self.symbol.string)
                '''
                if self.headings.index(self.symbol) != self.headings_found: #Check if headings are called in the right order
                    self.parse_errors += 1
                    raise SyntaxError("Headings called in the wrong order")
                    '''
                if self.symbol.id == self.scanner.NETWORK_ID:
                    self.headings_found += 1
                    self.OPENCURLY_search()

                
                elif self.symbol.id == self.scanner.DEVICES_ID:

                    if self.sections_complete == 0 and self.headings_found == 1:
                        self.headings_found += 1
                        #print("devices")
                        self.device_list()
                    else:
                        raise SyntaxError("Headings called in wrong order")
                    

                elif self.symbol.id == self.scanner.CONNECTIONS_ID:
                
                    if self.sections_complete == 1 and self.headings_found == 2:
                        self.headings_found += 1
                        #print("connections")
                        self.connection_list()
                    else:
                        raise SyntaxError("Headings called in wrong order")

                elif self.symbol.id == self.scanner.SIGNALS_ID:
                    if self.sections_complete == 2 and self.headings_found == 3:
                        self.headings_found += 1
                        #print("signals")
                        self.setsignal_list()
                    else:
                        raise SyntaxError("Headings called in wrong order")
                    

                elif self.symbol.id == self.scanner.MONITOR_ID:
                    if self.sections_complete == 3 and self.headings_found == 4:
                        self.headings_found += 1
                        self.monitor_list()

                    else:
                        raise SyntaxError("Headings called in wrong order")

                
            elif self.sections_complete == 4 and self.headings_found == 5:
                #print(self.symbol.string)
                #print("complete")
                return True
            else:
                return False
                


    def OPENCURLY_search(self):
        """Function which searches for a { after a heading"""
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type != self.scanner.LEFT_BRACKET:
            raise SyntaxError("Always need to follow a heading with {")
        #print('{')
              
    def device_list(self):
        """ Function which parses the device list"""

        self.OPENCURLY_search()
        
        self.symbol = self.scanner.get_symbol()
        self.device_parse()
        self.symbol = self.scanner.get_symbol()
        
        while self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.RIGHT_BRACKET:
                #print(self.symbol.string)
                self.devices_parsed = True
                self.sections_complete += 1
                break
            else:
                self.device_parse()
                self.symbol = self.scanner.get_symbol()               
               
    def device_parse(self):
        """Function which parses a single line of a device definition"""
        # Expected format : name EQUALS device

        if self.symbol.type != self.scanner.NAME:
            self.parse_errors += 1
            raise SyntaxError("Device: Name of device must contain a letter") 
        
        

        else:
            if self.symbol.id in self.device_names:
                self.parse_errors += 1
                raise SyntaxError("Device: Name for device already used")

            self.device_names.append(self.symbol.id) # add symbol id to a list of device ids
            self.new_device_id = self.symbol.id
            #print(self.symbol.string)
            self.symbol = self.scanner.get_symbol() #Get next symbol which should be an = sign   
            if self.symbol.type != self.scanner.EQUALS:
                    self.parse_errors += 1
                    raise SyntaxError("Device: Expected symbol is an =")
            else:
                self.symbol = self.scanner.get_symbol()
                #print(self.symbol.string)
                
                if self.symbol.id < 2 or self.symbol.id > 9:
                    self.new_device_id = self.symbol.id
                    self.parse_errors += 1
                    raise SyntaxError("Device: Device type not found")
  
                else:
                    self.new_device_type = self.symbol.id 

                    if self.symbol.id == self.scanner.XOR_ID or self.symbol.id == self.scanner.DTYPE_ID:
                        self.devices.make_device(self.new_device_id, self.new_device_type, None)

                    elif self.symbol.id == self.scanner.SWITCH_ID:
                        self.symbol = self.scanner.get_symbol()
                        self.devices.make_switch(self.new_device_id, 0)

                    elif self.symbol.id in self.gate_var_inputs_IDs:
                        self.symbol = self.scanner.get_symbol()
                        if self.symbol.string != "inputs":
                            self.parse_errors += 1
                            raise SyntaxError("Word inputs required")
                        else:
                            self.symbol = self.scanner.get_symbol()
                            if self.symbol.type != self.scanner.NUMBER:
                                self.parse_errors += 1
                                raise SyntaxError("Invalid number of inputs")
                            if self.symbol.id < 1 or self.symbol.id > 16:
                                self.parse_errors += 1
                                raise SyntaxError("Invalid number of inputs")
                            else:
                                self.devices.make_gate(self.new_device_id, self.new_device_type, self.symbol.id)
                            
                    elif self.symbol.id == self.scanner.CLOCK_ID:
                        self.symbol = self.scanner.get_symbol()
                        if self.symbol.string != "halfperiod":
                            self.parse_errors += 1
                            raise SyntaxError("Word halfperiod required")
                        else:
                            self.symbol = self.scanner.get_symbol()
                            if self.symbol.type != self.scanner.NUMBER:
                                self.parse_errors += 1
                                raise SyntaxError("Invalid halfperiod")
                            else:
                                self.devices.make_clock(self.new_device_id, self.symbol.id)

                                



                    



                
                
                    

    def connection_list(self):
        """Function whhich parses the connection list"""
        
        self.OPENCURLY_search()

        self.symbol = self.scanner.get_symbol() # Go to first symbol of line
        self.connection_parse() 
        self.symbol = self.scanner.get_symbol() # Go to last symbol of line, should be ;
        while self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol() # Go to first symbol of next line
            if self.symbol.type == self.scanner.RIGHT_BRACKET: # Check if } which denotes end of connections
                #print(self.symbol.string)
                self.connections_parsed = True
                self.sections_complete += 1 
                break
            else:
                self.connection_parse() 
                self.symbol = self.scanner.get_symbol()  #Go to last symbol of line, should be ;

                
    def connection_parse(self):
        """Function which parses a single connection"""
        # Expected format : name DASH name PERIOD Inumber
        
        if self.symbol.id not in self.device_names:
            #print("Not defined:", self.symbol.string)
            self.parse_errors += 1
            raise SyntaxError("CONNECTION: Device not defined")

        else: 
            [in_device_id, in_port_id] = self.signame_in()

            self.symbol = self.scanner.get_symbol()
    
            if self.symbol.type != self.scanner.DASH:
                self.parse_errors += 1
                raise SyntaxError("CONNECTION: No - found to define connection")

            else:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type != self.scanner.NAME:
                    self.parse_errors += 1
                    raise SyntaxError("CONNECTION: Device not defined")

                else:
                    out_device = self.symbol.devices.get_device(self.symbol.id)
                    out_device_id = out_device.device_id
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type != self.scanner.PERIOD:
                        raise SyntaxError("CONNECTION: No . found")

                    else: 
                        self.symbol = self.scanner.get_symbol()
                        out_port_id = self.symbol.id
                        self.input_list = list(self.symbol.string)
                        if self.input_list[0] != "I":
                            self.parse_errors += 1 
                            raise SyntaxError("CONNECTION: Input not initialised")
                        self.input_number = "".join(self.input_list[1:])
                        

                        if self.input_number.isdigit() == False:
                            
                            raise SyntaxError("CONNECTION: Input not defined")
                        
                        error_type = self.network.make_connection(
                            in_device_id, in_port_id, out_device_id, self.symbol.id)
                        if error_type != self.network.NO_ERROR:
                            raise SyntaxError("Error creating connection")
                        



    def signame_in(self):
        in_device = self.devices.get_device(self.symbol.id)
        if in_device.device_kind == self.devices.D_TYPE:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type != self.scanner.PERIOD:
                self.parse_errors += 1
                raise SyntaxError("D type output denoted by a .")
            else:
                self.symbol = self.scanner.get_symbol
                if self.symbol.id not in self.devices.dtype_output_ids:
                    self.parse_errors += 1
                    raise SyntaxError("Not a valid D type output")
                
                else:
                    return [in_device.device_id, self.symbol.id]
            
        else:
            return [in_device.device_id, None]



    
    def setsignal_list(self):
        """Function which parses the setsignal section"""

        self.OPENCURLY_search()
        self.symbol = self.scanner.get_symbol() #Go to first symbol of the line
        if self.symbol.type == self.scanner.RIGHT_BRACKET:
            #print(self.symbol.string)
            self.setsignal_parsed = True
            self.sections_complete += 1
            return 
        self.setsignal_parse()
        while self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol() # Go to first symbol of next line
            if self.symbol.type == self.scanner.RIGHT_BRACKET: # Check if } which denotes end of setsignal
                #print(self.symbol.string)
                self.setsignal_parsed = True
                self.sections_complete += 1
                break 
            self.setsignal_parse()
            
        


    def setsignal_parse(self):
        """Function which parses a single line of the setsignal section"""
        #Expected format : name EQUALS BINARYNUMBER "starttime" NUMBER SEMICOLON
        
        

        if self.symbol.id not in self.device_names:
            self.parse_errors += 1
            raise SyntaxError("SIGNALS: Device not defined")
            
        
        self.symbol = self.scanner.get_symbol() 
        
        if self.symbol.type != self.scanner.EQUALS:
                self.parse_errors += 1
                raise SyntaxError("SIGNALS: = sign expected")

        self.symbol = self.scanner.get_symbol()
        if self.symbol.string != "0" and self.symbol.string != "1":
            self.parse_errors += 1
            
            raise SyntaxError("SIGNALS: Signal can only be set to 1 or 0")
        elif self.symbol.type != self.scanner.NUMBER:
            self.parse_errors += 1
            raise SyntaxError("SIGNALS: Signal can only be set to 1 or 0")
        self.symbol = self.scanner.get_symbol()

        if self.symbol.type != self.scanner.SEMICOLON:
            self.parse_errors += 1
            raise SyntaxError("SIGNALS: Expected ; to end line")


    def monitor_list(self):
        """Function that parses the monitor section of the code"""

        self.OPENCURLY_search()

        self.symbol = self.scanner.get_symbol()

        if self.symbol.type == self.scanner.RIGHT_BRACKET:
            self.parse_errors += 1
            raise SyntaxError("MONITOR: No devices monitored")
        
        
        else:
            self.monitor_parse()
            while self.symbol.type == self.scanner.SEMICOLON:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.RIGHT_BRACKET:
                    #print(self.symbol.string)
                    self.sections_complete += 1
                    self.monitor_parsed = True
                    break
                else:
                    self.monitor_parse()


    
    def monitor_parse(self):
        """Function which parses a line in Monitor """
        #Expected format : name SEMICOLON
        if self.symbol.id not in self.device_names:
            self.parse_errors += 1
            raise SyntaxError("MONITOR: Device not defined")
        
        self.symbol = self.scanner.get_symbol()

        if self.symbol.type != self.scanner.SEMICOLON:
            self.parse_errors += 1
            raise SyntaxError("MONITOR: Expected ; to end line")





        


            
                
        
        


        
        
        




                
            
     


                        



            
        

                            



                



                


            





            
