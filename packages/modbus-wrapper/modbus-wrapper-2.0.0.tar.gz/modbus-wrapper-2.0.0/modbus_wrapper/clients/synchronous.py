from .base import ModbusBaseClientWrapper
from pymodbus.client import ModbusSerialClient, ModbusTcpClient, ModbusUdpClient
from .. import modbus_function_code 



class ModbusTcpClientWrapper(ModbusBaseClientWrapper, ModbusTcpClient):
    pass


class ModbusUdpClientWrapper(ModbusBaseClientWrapper, ModbusUdpClient):
    pass


class ModbusSerialClientWrapper(ModbusBaseClientWrapper, ModbusSerialClient):
    pass


class ModbusSerialClientWrapper(ModbusBaseClientWrapper, ModbusSerialClient):
    def __init__(
        self, 
        port,
        baudrate=9600,
        bytesize=8,
        parity="N",
        stopbits=1,
        timeout=1,
        *args, 
        **kwargs
                 ):
    
        ModbusSerialClient.__init__(
                self,
                port=port,
                baudrate=baudrate,
                bytesize=bytesize,
                parity=parity,
                stopbits=stopbits,
                timeout=timeout,
                *args, 
                **kwargs
                )        
      
        self.function_map = {
            modbus_function_code.READ_COILS: self.read_coils,
            modbus_function_code.READ_HOLDING_REGISTERS: self.read_holding_registers,
            modbus_function_code.READ_DISCRETE_INPUTS: self.read_discrete_inputs,
            modbus_function_code.READ_INPUT_REGISTERS: self.read_input_registers,
            modbus_function_code.WRITE_SINGLE_COIL: self.write_coil,
            modbus_function_code.WRITE_SINGLE_HOLDING_REGISTER: self.write_register,
            modbus_function_code.WRITE_MULTIPLE_COILS: self.write_coils,
            modbus_function_code.WRITE_MULTIPLE_HOLDING_REGISTERS: self.write_registers
         }
