from OLT_ONT_PORTFINDER import ont_4ports, \
    ont_8ports, ont_16ports_plus, ont_16ports


class PortFinder:
    """Collect data from external source and process it
        the slot must be a dict
        the slot must be a string like this '1/3' for slot with more than 4 ports
        and '1' for a 4 ports slot
    """

    def __init__(self, slots, slot_port=None):
        self.slots = slots
        self.slot_port = slot_port

    def get_target_port(self):
        """
            received data should be something like this:
            16_ports = {'1/1/3/10/1/1': '8', '1/1/3/10/1/3': '8'}
            16_ports_plus4 = {'1/1/1/3/10/1': '4', '1/1/3/10/1/1': '8', '1/1/3/10/1/3': '8'}
            8_ports = {'1/1/3/10/1/1': '8'}
            4_ports = {'1/1/1/3/10/1': '4'}
        """

        if self.slots and self.slot_port:
            # check if 16 port ont
            if len(self.slots) == 2 and list(self.slots.values()) == ['8', '8']:
                    port = ont_16ports.SlotsPortsManager(self.slots, self.slot_port)
                    port = port.get_target_port()
                    return port
            # check if 16 ports + 4
            elif len(self.slots) == 3 and list(self.slots.values()) == ['4', '8', '8']:
                    port = ont_16ports_plus.SlotsPortsManager(self.slots, self.slot_port)
                    port = port.get_target_port()
                    return port
            # check if 16 ports + 4
            elif len(self.slots) == 3 and list(self.slots.values()) == ['8', '8', '4']:
                    port = ont_16ports_plus.SlotsPortsManager(self.slots, self.slot_port)
                    port = port.get_target_port()
                    return port
            # check if 8 ports
            elif len(self.slots) == 1 and list(self.slots.values()) == ['8']:
                    port = ont_8ports.SlotsPortsManager(self.slots, self.slot_port)
                    port = port.get_target_port()
                    return port
            # check if 4 ports
            elif len(self.slots) == 1 and list(self.slots.values()) == ['4']:
                    port = ont_4ports.SlotsPortsManager(self.slots, self.slot_port)
                    port = port.get_target_port()
                    return port
            else:
                return f"Operation not supported\n"
        else:
            return f"No data provided\n"
