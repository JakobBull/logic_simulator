"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""

from error import Error


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
        #self.Error = Error

        self.type = None
        self.id = None
        self.parse_errors = 0
        self.device_names = []
        self.connected_inputs = []
        self.gate_var_inputs_IDs = [
            self.scanner.AND_ID,
            self.scanner.NAND_ID,
            self.scanner.OR_ID,
            self.scanner.NOR_ID,
            self.scanner.XOR_ID,

        ]
        self.device_IDs = [
            self.scanner.AND_ID,
            self.scanner.NAND_ID,
            self.scanner.OR_ID,
            self.scanner.NOR_ID,
            self.scanner.XOR_ID,
            self.scanner.DTYPE_ID,
            self.scanner.SWITCH_ID,
            self.scanner.CLOCK_ID
        ]
        self.heading_IDs = [self.scanner.NETWORK_ID, self.scanner.DEVICES_ID,
                            self.scanner.CONNECTIONS_ID,
                            self.scanner.SIGNALS_ID,
                            self.scanner.MONITOR_ID]
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

        # print(self.gate_var_inputs_IDs)
        # print("Netowrk_ID: ", self.scanner.NETWORK_ID)
        while True:
            # Call for the next symbol from scanner
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.KEYWORD:
                # Check if symbol is a Heading
                if self.symbol.id == self.scanner.NETWORK_ID:
                    self.headings_found += 1
                    self.OPENCURLY_search()
                    # report error 0 if network isn't the first heading found
                    if(self.headings_found != 1):
                        Error(0, self.symbol)

                elif self.symbol.id == self.scanner.DEVICES_ID:
                    self.headings_found += 1
                    # report error 0 if network isn't the 2nd heading found
                    if(self.headings_found != 2):
                        Error(0, self.symbol)
                    self.device_list()

                elif self.symbol.id == self.scanner.CONNECTIONS_ID:
                    self.headings_found += 1
                    # report error 0 if network isn't the 3rd heading found
                    if(self.headings_found != 3):
                        Error(0, self.symbol)
                    #self.connection_list()

                elif self.symbol.id == self.scanner.SIGNALS_ID:
                    self.headings_found += 1
                    #self.setsignal_list()
                    # report error 0 if network isn't the 4th heading found
                    if(self.headings_found != 4):
                        Error(0, self.symbol)

                elif self.symbol.id == self.scanner.MONITOR_ID:
                    self.headings_found += 1
                    #self.monitor_list()
                    # report error 0 if network isn't the 2nd heading found
                    if(self.headings_found != 5):
                        Error(0, self.symbol)
            if self.symbol.type ==  self.scanner.EOF:
                if Error.num_errors == 0:
                    return True
                else:
                    print(Error.gui_report_error(self.scanner))
                    return False

    def OPENCURLY_search(self):
        """Search for a { after a heading."""
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type != self.scanner.LEFT_BRACKET:
            self.parse_errors += 1
            Error(1, self.symbol)

    def device_list(self):
        """Parse the device list."""
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type != self.scanner.LEFT_BRACKET:
            Error(1, self.symbol)
        else:
            self.symbol = self.scanner.get_symbol()

        while True:
            self.device_parse()
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.RIGHT_BRACKET:
                self.sections_complete += 1
                break

    def device_parse(self):
        """Parse a single line of a device definition."""
        errors_start = Error.num_errors # errors started with
        # Expected format : name EQUALS device
        #symbol 1: Name
        if self.symbol.type != self.scanner.NAME: # if first symbol of line is a not a name, error 2
            Error(2, self.symbol)
        else:   # if first symbol is a name
            if self.symbol.id in self.device_names: # if a name has already been used as a device, call error 3
                Error(3, self.symbol)
            else:
                self.device_names.append(self.symbol.id)

        self.symbol = self.scanner.get_symbol() # next symbol

        #symbol 2: '='
        if self.symbol.type != self.scanner.EQUALS:
            Error(4, self.symbol)

        self.symbol = self.scanner.get_symbol() # next symbol


        #symbol 3: Device
        gate = False
        clock = False
        if self.symbol.id not in self.device_IDs:
            Error(5, self.symbol)
        elif self.symbol.id in self.gate_var_inputs_IDs: #symbol is a gate, next symbol must be inputs
            gate = True
        elif self.symbol.id == self.scanner.CLOCK_ID: #symbol is a gate, next symbol must be inputs
            clock = True

        self.symbol = self.scanner.get_symbol() # next symbol

        #symbol 4: "inputs" if gate, ';' if not. "halfperiod" if clock, ';' if not.
        if gate:
            if self.symbol.string != "inputs":
                Error(6, self.symbol)
        elif clock:
            if self.symbol.string != "halfperiod":
                Error(8, self.symbol)
        else:
            if self.symbol.type != self.scanner.SEMICOLON:
                Error(10, self.symbol)
            else:
                return Error.num_errors - errors_start

        #symbol 5 should be a number if gate or clock device
        if gate or clock:
            self.symbol = self.scanner.get_symbol() # next symbol
            if gate:
                if self.symbol.type != self.scanner.NUMBER and self.symbol.number < 1:
                    Error(7, self.symbol)
            elif clock:
                if self.symbol.type != self.scanner.NUMBER and self.symbol.number < 1:
                    Error(9, self.symbol)

        #symbol 6 should be a ';' if gate or clock device
        if gate or clock:
            self.symbol = self.scanner.get_symbol() # next symbol
            if self.symbol.type != self.scanner.SEMICOLON:
                Error(10, self.symbol)

    def connection_list(self):
        """Parse the device list."""
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type != self.scanner.LEFT_BRACKET:
            Error(1, self.symbol)
        else:
            self.symbol = self.scanner.get_symbol()

        while True:
            self.connection_parse()
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.RIGHT_BRACKET:
                self.sections_complete += 1
                break

    def connection_parse(self):
        """Parse a single connection."""
        errors_start = Error.num_errors # errors started with
        # Expected format : name DASH name PERIOD Inumber
        #symbol 1: Name
        if self.symbol.id not in self.device_names:
            Error(11, self.symbol)
        self.symbol = self.scanner.get_symbol() # next symbol

        #symbol 2: '-'
        if self.symbol.type != self.scanner.DASH:
            Error(12, self.symbol)

        self.symbol = self.scanner.get_symbol() # next symbol
        #symbol 3: name
        if self.symbol.id not in self.device_names:
            Error(11, self.symbol)

        self.symbol = self.scanner.get_symbol() # next symbol

        #symbol 3: '.'
        if self.symbol.id != self.scanner.PERIOD:
            Error(13, self.symbol)

        self.symbol = self.scanner.get_symbol() # next symbol

        #symbol 4: I + input#
        if self.symbol.string[0] != 'I':
            Error(13, self.symbol)
        else:
            input_num = "" + self.symbol.string[1:]
            if not input_num.isdigit():
                Error(13, self.symbol)

        self.symbol = self.scanner.get_symbol() # next symbol
        if self.symbol.type == self.scanner.EOF:
            return 0

        #symbol 5: ';'
        if self.symbol.type != self.scanner.SEMICOLON:
            Error(18, self.symbol)
        print("hello")

    def signame_in(self):
        """Return the device ID and port ID for a device."""
        in_device = self.devices.get_device(self.symbol.id)
        if in_device.device_kind == self.devices.D_TYPE:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type != self.scanner.PERIOD:
                self.parse_errors += 1
                Error(16, self.symbol)

            else:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.id not in self.devices.dtype_output_ids:
                    self.parse_errors += 1
                    Error(17, self.symbol)

                else:
                    return [in_device.device_id, self.symbol.id]

        else:
            return [in_device.device_id, None]

    def setsignal_list(self):
        """Parse the setsignal section."""
        self.OPENCURLY_search()
        self.symbol = self.scanner.get_symbol()
        #  Go to first symbol of the line
        if self.symbol.type == self.scanner.RIGHT_BRACKET:
            # print(self.symbol.string)
            self.setsignal_parsed = True
            self.sections_complete += 1
            return
        self.setsignal_parse()
        while self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol()
            # Go to first symbol of next line
            if self.symbol.type == self.scanner.RIGHT_BRACKET:
                # Check if } which denotes end of setsignal
                self.setsignal_parsed = True
                self.sections_complete += 1
                break
            self.setsignal_parse()

    def setsignal_parse(self):
        """Parse a single line of the setsignal section."""
        # Expected format : name EQUALS BINARYNUMBER SEMICOLON
        if self.symbol.id not in self.device_names:
            self.parse_errors += 1
            Error(18, self.symbol)
            self.advance_line_error()

        switch_set_ID = self.devices.get_device(self.symbol.id)

        self.symbol = self.scanner.get_symbol()
        if self.symbol.type != self.scanner.EQUALS:
            self.parse_errors += 1
            Error(19, self.symbol)
            self.advance_line_error()
        self.symbol = self.scanner.get_symbol()
        if self.symbol.string != "0" and self.symbol.string != "1":
            self.parse_errors += 1
            Error(20, self.symbol)
            self.advance_line_error()

        elif self.symbol.type != self.scanner.NUMBER:
            self.parse_errors += 1
            Error(20, self.symbol)
            self.advance_line_error()
        elif self.symbol.string == "1":
            self.devices.set_switch(switch_set_ID, 1)

        self.symbol = self.scanner.get_symbol()

        if self.symbol.type != self.scanner.SEMICOLON:
            self.parse_errors += 1
            Error(22, self.symbol)
            self.advance_line_error()

    def monitor_list(self):
        """Parse the monitor section of the code."""
        self.OPENCURLY_search()

        self.symbol = self.scanner.get_symbol()

        if self.symbol.type == self.scanner.RIGHT_BRACKET:
            self.parse_errors += 1
            Error(23, self.symbol)

        else:
            self.monitor_parse()
            while self.symbol.type == self.scanner.SEMICOLON:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.RIGHT_BRACKET:
                    # print(self.symbol.string)
                    self.sections_complete += 1
                    self.monitor_parsed = True
                    break
                else:
                    self.monitor_parse()

    def monitor_parse(self):
        """Parse a line in Monitor."""
        # Expected format : name SEMICOLON
        if self.symbol.id not in self.device_names:
            self.parse_errors += 1
            Error(24, self.symbol)
            self.advance_line_error()

        [device_id, output_id] = self.signame_in()

        error_type = self.monitors.make_monitor(device_id, output_id)

        if error_type == self.monitors.NOT_OUTPUT:
            self.parse_errors += 1
            Error(25, self.symbol)
            self.advance_line_error()

        elif error_type == self.monitors.MONITOR_PRESENT:
            self.parse_errors += 1
            Error(26, self.symbol)
            self.advance_line_error()

        self.symbol = self.scanner.get_symbol()

        if self.symbol.type != self.scanner.SEMICOLON:
            self.parse_errors += 1
            Error(27, self.symbol)
            self.advance_line_error()

    def advance_line_error(self):
        """Advances to the next ; xafter an error to continue parsing.
        while (self.symbol.type != self.scanner.SEMICOLON or
                self.symbol.type != self.scanner.RIGHT_BRACKET):
            self.symbol = self.scanner.get_symbol()
            # if self.symbol.id in self.heading_IDs:
            """
        pass
