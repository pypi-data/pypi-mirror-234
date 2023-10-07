""" """


class SlotsPortsManager:
    """Process slots and  ports"""
    def __init__(self, slots, slot_port):
        self.slots_dict = slots
        self.slot_port = slot_port
        self.slot_port_erros = f"""
        [ {self.slot_port} ] is not a valid slot/port value
        These are the valid port [1-4]
        """

    def get_target_port(self):
        """"""
        data = self.slots_dict
        if not self.slot_port:
            print(f"No port value provided\n")
            print(f"These are the valid port [1-4]\n\n")
            exit()

        slot1 = {}
        for k, v in data.items():
            if k.endswith('1') and '4' in v:
                slot1[k] = v

        if self.slot_port:
            if len(str(self.slot_port)) == 1:
                # check if provided port is numeric
                if str(self.slot_port).isnumeric():
                    # check if provided port is in within the correct range
                    if int(self.slot_port) in range(1, int(list(slot1.values())[0]) + 1):
                        target_port = f"{list(slot1.keys())[0]}/{self.slot_port}"
                        return target_port
                    else:
                        print(f"\n[ {self.slot_port} ] is not a valid port value")
                        print(f"These are the valid port for this hardware [1-4]\n")
                        exit()
                else:
                    print(f"\n[ {self.slot_port} ] must be a numeric value")
                    print(f"These are the valid port for this hardware [1-4]\n")
                    exit()
            else:
                print(f"\n[ {self.slot_port} ] is not a valid port value")
                print(f"These are the valid port for this hardware [1-4]\n")
                exit()
        else:
            print(self.slot_port_erros)
            exit()

















#