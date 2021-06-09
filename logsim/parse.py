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

        self.symbol = self.scanner.get_symbol() #set as next symbol from scanner
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
            self.scanner.CLOCK_ID,
            self.scanner.SIGGEN_ID
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
        self.heading_search()

        print(Error.gui_report_error(self.scanner))
        if Error.num_errors == 0:
            return True

    def heading_search(self):
        if self.symbol.id != self.scanner.NETWORK_ID:
            Error(0, self.symbol) # report error 0 if network isn't the first heading found
            return False
        print('Network')
        self.OPENCURLY_search()

        if self.symbol.id != self.scanner.DEVICES_ID:
            Error(0, self.symbol) # report error 0 if network isn't the first heading found
            return False
        print('Devices')
        self.OPENCURLY_search()

        self.device_list()

        if self.symbol.id != self.scanner.CONNECTIONS_ID:
            Error(0, self.symbol) # report error 0 if network isn't the first heading found
            return False
        print('Connections')
        self.OPENCURLY_search()

        self.connection_list()

        if self.symbol.id != self.scanner.SIGNALS_ID:
            Error(0, self.symbol) # report error 0 if network isn't the first heading found
            return False
        self.OPENCURLY_search()
        print('Signals')
        self.setsignal_list()

        if self.symbol.id != self.scanner.MONITOR_ID:
            Error(0, self.symbol) # report error 0 if network isn't the first heading found
            return False
        self.OPENCURLY_search()
        print('Monitor')
        self.monitor_list()



    def OPENCURLY_search(self):
        """Check if next symbol is '{'. If it isn't return error, if it is, go to next symbol"""
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type != self.scanner.LEFT_BRACKET:
            Error(1, self.symbol) # if not '{' - call error and continue parsing while staying at this symbol
        else:
            self.symbol = self.scanner.get_symbol() # if '{' - go to next symbol


    def device_list(self):
        """Parse the device list."""

        while True:
            error = self.device_parse()
            if error == 1:
                break
            if error == 2:
                self.symbol = self.scanner.get_symbol()
                break
            else:
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.RIGHT_BRACKET:
                    self.sections_complete += 1
                    self.symbol = self.scanner.get_symbol()
                    break

    def device_parse(self):
        """Parse a single line of a device definition."""
        errors_start = Error.num_errors # errors started with
        # Expected format : name EQUALS device
        # symbol 1: Name
        if self.symbol.type == self.scanner.SEMICOLON:
            return 0
        if self.symbol.type == self.scanner.EOF:
            return 1
        if self.symbol.type == self.scanner.RIGHT_BRACKET:
            return 2
        if self.symbol.type != self.scanner.NAME: # if first symbol of line is a not a name, error 2
            Error(2, self.symbol)
        else:   # if first symbol is a name
            if self.symbol.id in self.device_names: # if a name has already been used as a device, call error 3
                Error(3, self.symbol)
            else:
                self.new_device_id = self.symbol.id


        self.symbol = self.scanner.get_symbol() # next symbol
        if self.symbol.type == self.scanner.SEMICOLON:
            return 0
        if self.symbol.type == self.scanner.EOF:
            return 1
        if self.symbol.type == self.scanner.RIGHT_BRACKET:
            return 2

        #symbol 2: '='
        if self.symbol.type != self.scanner.EQUALS:
            Error(4, self.symbol)

        self.symbol = self.scanner.get_symbol() # next symbol
        if self.symbol.type == self.scanner.SEMICOLON:
            return 0
        if self.symbol.type == self.scanner.EOF:
            return 1
        if self.symbol.type == self.scanner.RIGHT_BRACKET:
            return 2

        # symbol 3: Device
        gate = False
        clock = False
        siggen = False
        if self.symbol.id not in self.device_IDs:
            Error(5, self.symbol)
        elif self.symbol.id in self.gate_var_inputs_IDs:
            # symbol is a gate, next symbol must be inputs
            gate = True
        elif self.symbol.id == self.scanner.CLOCK_ID:
            # symbol is a clock, next symbol must be halfperiod
            clock = True
        elif self.symbol.id == self.scanner.SIGGEN_ID:
            # symbol is a siggen, next symbol must be halfperiod
            siggen = True
        self.new_device_type = self.symbol.id
        self.symbol = self.scanner.get_symbol() # next symbol


        #symbol 4: "inputs" if gate, ';' if not. "halfperiod" if clock, ';' if not.
        if gate:
            if self.symbol.string != "inputs":
                Error(6, self.symbol)
        elif clock:
            if self.symbol.string != "halfperiod":
                Error(8, self.symbol)
        elif siggen:
            if self.symbol.string != "pulse":
                Error(30, self.symbol)   # need siggen error
        elif (self.symbol.type == self.scanner.SEMICOLON and
                self.new_device_type == self.scanner.SWITCH_ID):
            # Must be a switch so make switch initially 0
            self.devices.make_switch(self.new_device_id, 0)
            self.device_names.append(self.new_device_id)
            return 0

        elif self.symbol.type == self.scanner.SEMICOLON:
            # Must be an xor or dtype so make that device
            self.devices.make_device(
                self.new_device_id, self.new_device_type, None)
            self.device_names.append(self.new_device_id)
            return 0
        elif self.symbol.type == self.scanner.EOF:
            return 1
        elif self.symbol.type == self.scanner.RIGHT_BRACKET:
            return 2
        else:
            if self.symbol.type != self.scanner.SEMICOLON:
                Error(10, self.symbol)
                for i in range(10): # tries to get a semi colon before going to next
                    self.symbol = self.scanner.get_symbol() # next symbol
                    if self.symbol.type == self.scanner.SEMICOLON:
                        return 0
                    if self.symbol.type == self.scanner.EOF:
                        return 1
                    if self.symbol.type == self.scanner.RIGHT_BRACKET:
                        return 2

            else:
                return Error.num_errors - errors_start
        #symbol 5 should be a number if gate or clock device
        if gate or clock or siggen:
            self.symbol = self.scanner.get_symbol() # next symbol
            if self.symbol.type == self.scanner.SEMICOLON:
                return 0
            if self.symbol.type == self.scanner.EOF:
                return 1
            if self.symbol.type == self.scanner.RIGHT_BRACKET:
                return 2

            if gate:
                if self.symbol.type != self.scanner.NUMBER or self.symbol.number < 1:
                    Error(7, self.symbol)
                else:
                    # Build gate object
                    self.devices.make_gate(
                        self.new_device_id, self.new_device_type,
                        self.symbol.number)
                    self.device_names.append(self.new_device_id)
            elif clock:
                if self.symbol.type != self.scanner.NUMBER or self.symbol.number < 1:
                    Error(9, self.symbol)
                else:
                    # Build clock object
                    self.devices.make_clock(
                        self.new_device_id, self.symbol.number)
                    self.device_names.append(self.new_device_id)
            elif siggen:
                if self.symbol.type != self.scanner.NUMBER or not self.is_bin_num(self.symbol.number):
                    Error(31, self.symbol)
                else:
                    # Build siggen object
                    self.devices.make_siggen(
                        self.new_device_id, self.symbol.number)
                    self.device_names.append(self.new_device_id)

        #symbol 6 should be a ';' if gate or clock device
        if gate or clock or siggen:
            self.symbol = self.scanner.get_symbol() # next symbol
            if self.symbol.type == self.scanner.SEMICOLON:
                return 0
            if self.symbol.type == self.scanner.EOF:
                return 1
            if self.symbol.type == self.scanner.RIGHT_BRACKET:
                return 2
            if self.symbol.type != self.scanner.SEMICOLON:
                Error(10, self.symbol)
                for i in range(10): #tries to get a semi colon before going to next
                    self.symbol = self.scanner.get_symbol() # next symbol
                    if self.symbol.type == self.scanner.SEMICOLON:
                        return 0
                    if self.symbol.type == self.scanner.EOF:
                        return 1
                    if self.symbol.type == self.scanner.RIGHT_BRACKET:
                        return 2

    def is_bin_num(self, num):
        for i in str(num):
            if i in ("01") == False:
                return False
        return True

    def connection_list(self):
        """Parse the device list."""

        while True:
            if self.connection_parse() == 1: break
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.RIGHT_BRACKET:
                self.sections_complete += 1
                self.symbol = self.scanner.get_symbol()
                break

    def connection_parse(self):
        """Parse a single connection."""
        errors_start = Error.num_errors # errors started with
        # Expected format : name DASH name PERIOD Inumber
        #symbol 1: Name
        dtype = False
        out_device_id = None
        in_device_id = None
        in_port_id = None
        if self.symbol.id not in self.device_names:
            Error(11, self.symbol)
        else:
            [in_device_id, in_port_id] = self.signame_in()

        self.symbol = self.scanner.get_symbol() # next symbol
        if self.symbol.type == self.scanner.SEMICOLON:
            return 0
        if self.symbol.type == self.scanner.EOF:
            return 1

        #symbol 2: '-'
        if self.symbol.type != self.scanner.DASH:
            Error(12, self.symbol)

        self.symbol = self.scanner.get_symbol() # next symbol
        if self.symbol.type == self.scanner.SEMICOLON:
            return 0
        if self.symbol.type == self.scanner.EOF:
            return 1

        #symbol 3: name
        if self.symbol.id not in self.device_names:
            Error(11, self.symbol)

        else:
            out_device_id = self.symbol.id
            out_device = self.devices.get_device(self.symbol.id)

            if out_device.device_kind == self.devices.D_TYPE:
                dtype = True

        self.symbol = self.scanner.get_symbol() # next symbol
        if self.symbol.type == self.scanner.SEMICOLON:
            return 0
        if self.symbol.type == self.scanner.EOF:
            return 1

        #symbol 3: '.'
        print(self.symbol.string)
        if self.symbol.type != self.scanner.PERIOD:
            Error(13, self.symbol)

        self.symbol = self.scanner.get_symbol() # next symbol
        if self.symbol.type == self.scanner.SEMICOLON:
            return 0
        if self.symbol.type == self.scanner.EOF:
            return 1

        #symbol 4: I + input#
        if dtype:
            if self.symbol.id not in self.devices.dtype_input_ids:
                Error(13, self.symbol)
        else:
            if self.symbol.string[0] != 'I':
                Error(13, self.symbol)
            else:
                input_num = "" + self.symbol.string[1:]
                if not input_num.isdigit():
                    Error(13, self.symbol)

        error_type = self.network.make_connection(
            in_device_id, in_port_id,
            out_device_id, self.symbol.id)

        if error_type != self.network.NO_ERROR:
            Error(13, self.symbol)

        self.symbol = self.scanner.get_symbol() # next symbol
        if self.symbol.type == self.scanner.SEMICOLON:
            return 0
        if self.symbol.type == self.scanner.EOF:
            return 1

        if self.symbol.type == self.scanner.EOF:
            return 0

        #symbol 5: ';'
        if self.symbol.type != self.scanner.SEMICOLON:
            Error(18, self.symbol)
            for i in range(10): #tries to get a semi colon before going to next
                self.symbol = self.scanner.get_symbol() # next symbol
                if self.symbol.type == self.scanner.SEMICOLON:
                    return 0
                if self.symbol.type == self.scanner.EOF:
                    return 1

    def setsignal_list(self):
        """Parse the setsignal section."""
        while True:
            if self.setsignal_parse() == 1: break
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.RIGHT_BRACKET:
                self.sections_complete += 1
                self.symbol = self.scanner.get_symbol()
                break

    def setsignal_parse(self):
        """Parse a single line of the setsignal section."""
        errors_start = Error.num_errors # errors started with
        # Expected format : name EQUALS BINARYNUMBER SEMICOLON
        if self.symbol.id not in self.device_names:
            Error(20, self.symbol)

        # Find the switch device ID
        switch_set_ID = self.devices.get_device(self.symbol.id)

        self.symbol = self.scanner.get_symbol() # next symbol
        if self.symbol.type == self.scanner.SEMICOLON:
            return 0
        if self.symbol.type == self.scanner.EOF:
            return 1

        if self.symbol.type != self.scanner.EQUALS:
            Error(21, self.symbol)

        self.symbol = self.scanner.get_symbol() # next symbol
        if self.symbol.type == self.scanner.SEMICOLON:
            return 0
        if self.symbol.type == self.scanner.EOF:
            return 1

        if self.symbol.type != self.scanner.NUMBER:
            Error(22, self.symbol)
        elif self.symbol.number != 0 and self.symbol.number != 1:
            Error(22, self.symbol)
        elif self.symbol.number == 1:
            self.devices.set_switch(switch_set_ID, 1)

        self.symbol = self.scanner.get_symbol() # next symbol
        if self.symbol.type == self.scanner.SEMICOLON:
            return 0
        if self.symbol.type == self.scanner.EOF:
            return 1

        if self.symbol.type != self.scanner.SEMICOLON:
            Error(24, self.symbol)


    def monitor_list(self):
        """Parse the monitor section of the code."""
        print(self.device_names)
        print(self.symbol.string)
        while True:
            if self.monitor_parse() == 1: break
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.RIGHT_BRACKET:
                self.sections_complete += 1
                self.symbol = self.scanner.get_symbol()
                break

    def monitor_parse(self):
        # Parse a line in Monitor.
        errors_start = Error.num_errors # errors started with
        error_type = 0
        # Expected format : name SEMICOLON
        device_id = None
        output_id = None

        if self.symbol.id not in self.device_names:
            Error(26, self.symbol)
        else:
            print(self.symbol.string)
            [device_id, output_id] = self.signame_in()

            error_type = self.monitors.make_monitor(device_id, output_id)

        if error_type == self.monitors.NOT_OUTPUT:
            Error(27, self.symbol)

        elif error_type == self.monitors.MONITOR_PRESENT:
            Error(28, self.symbol)

        self.symbol = self.scanner.get_symbol() # next symbol
        if self.symbol.type == self.scanner.SEMICOLON:
            return 0
        if self.symbol.type == self.scanner.EOF:
            return 1

        if self.symbol.type != self.scanner.SEMICOLON:
            Error(29, self.symbol)

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
