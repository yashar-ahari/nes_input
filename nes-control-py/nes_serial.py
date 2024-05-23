from enum import Enum
import serial
import time

class NesInput:
    A = False
    B = False
    SELECT = False
    START = False
    UP = False
    DOWN = False
    LEFT = False
    RIGHT = False
    
    def zero(self):
        self.A = False
        self.B = False
        self.SELECT = False
        self.START = False
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False
    
    def get_value(self):
        val = self.A
        val = val | self.B << 1
        val = val | self.SELECT << 2
        val = val | self.START << 3
        val = val | self.UP << 4
        val = val | self.DOWN << 5
        val = val | self.LEFT << 6
        val = val | self.RIGHT << 6
        return val;

    def Zero():
        return NesInput()
    
    def A():
        i = NesInput()
        i.A = True
        return i
    
    def B():
        i = NesInput()
        i.B = True
        return i
    
    def Select():
        i = NesInput()
        i.SELECT = True
        return i

    def Start():
        i = NesInput()
        i.START = True
        return i

    def Up():
        i = NesInput()
        i.Up = True
        return i

    def Down():
        i = NesInput()
        i.DOWN = True
        return i

    def Left():
        i = NesInput()
        i.LEFT = True
        return i

    def Right():
        i = NesInput()
        i.RIGHT = True
        return i


class NesBroker:
    HAND_SHAKE_BYTE = 183
    CMD_OK = 'OK'
    CMD_FAIL = 'NO'
    CMD_EXIT_SAFE_MODE = 1
    CMD_UPDATE_CONTROL_STATE = 2
    CMD_ENTER_SAFE_MODE = 3

    class BrokerState(Enum):
        ACTIVE = 0
        SAFE = 1

    state = BrokerState.SAFE;

    def __init__(self, port, bitrate=9600):
        self.port = port
        self.bitrate = bitrate
        self.state = NesBroker.BrokerState.SAFE
        
        
        
    def __enter__(self):
        self.port = serial.Serial(self.port, self.bitrate, 8, timeout=0.5)
        if not self.port.is_open:
            self.port.open()
        while not self.port.is_open:
            continue;
        time.sleep(1)
        self.enter_safe_mode()
        return self
    
    def __exit__(self, *args):
        if self.port.is_open:
            self.port.close()
            
    def __conntect(self):
        self.port.write(NesBroker.__create_data(NesBroker.CMD_EXIT_SAFE_MODE, 0).to_bytes(4, 'little'))
        response = self.__read_serial()
        if response == NesBroker.CMD_OK:
            self.state = NesBroker.BrokerState.ACTIVE
            print("State set to " + str(self.state));
        return response;
        

    
    def __create_data(command : int, data : int) -> int:
        _c = command.to_bytes(1, 'little')[0]
        _d = data.to_bytes(1, 'little')[0]
        parity_byte = NesBroker.HAND_SHAKE_BYTE ^ _c ^ _d
        return int.from_bytes([NesBroker.HAND_SHAKE_BYTE, _c, _d, parity_byte], 'little')
          
    def exit_safe_mode(self):
        return self.__conntect();
    
    def enter_safe_mode(self):
        self.port.write(NesBroker.__create_data(NesBroker.CMD_ENTER_SAFE_MODE, 0).to_bytes(4, 'little'))
        response = self.__read_serial()
        if response == NesBroker.CMD_OK:
            self.state = NesBroker.BrokerState.SAFE
            print("State set to " + str(self.state));
        return response;

    def set_control_state(self, control_state):
        self.port.write(NesBroker.__create_data(NesBroker.CMD_UPDATE_CONTROL_STATE, control_state).to_bytes(4, 'little'))
        response = self.__read_serial()
        return response;

    def set_nes_input(self, nes_input : NesInput):
        return self.set_control_state(nes_input.get_value());

    def __read_serial(self):
        waiting = self.port.in_waiting  # find num of bytes currently waiting in hardware
        buffer = self.port.read(waiting)
        res = buffer.decode('ascii')
        print(res)
        return res
    

    
    

        