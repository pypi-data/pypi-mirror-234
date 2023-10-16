import logging
import asyncio
from typing import List
from pymodbus.client import AsyncModbusTcpClient, AsyncModbusUdpClient
from .base import ModbusBaseClientWrapper
from ..object_factory import get_modbus_object_from_range, get_modbus_object
from ..function_argument import WriteFunctionArgument, ReadFunctionArgument
from ..objects import ModbusObject


LOG = logging.getLogger(__name__)


class AsyncModbusBaseClientWrapper(ModbusBaseClientWrapper):

    async def read(
            self,
            modbus_numbers: List[int | str],
            unit: int = 0,
            *args,
            **kwargs
        ) -> dict:
        
        modbus_objects = self._get_modbus_objects(modbus_numbers, unit)

        await self.read_modbus_objects(modbus_objects, *args, **kwargs)

        return self._get_dict_results_from_objects(modbus_objects)


    async def read_modbus_objects(
            self, 
            modbus_objects: List[ModbusObject],  
            max_read_size: int = None, 
            read_mask: int = None,
            ) -> None:
        
        arguments = ReadFunctionArgument.get_arguments(
            modbus_objects,
            max_read_size=max_read_size, 
            read_mask=read_mask
            )

        async with self as client:
            tasks = []
            for arg in arguments: 
                tasks.append(asyncio.create_task(client._read(arg)))
                
            results = asyncio.gather(*tasks)
            await results


    async def write(self, modbus_numbers_with_values: dict) -> dict:
        modbus_objects = [get_modbus_object(n,v) for n,v in modbus_numbers_with_values.items()]

        await self.write_modbus_objects(modbus_objects)

        return self._get_dict_results_from_objects(modbus_objects)


    async def write_modbus_objects(self, modbus_objects: List[ModbusObject]):
        arguments = WriteFunctionArgument.get_arguments(
                                        modbus_objects,
                                        )

        async with self as client:
            tasks = []
            for arg in arguments: 
                tasks.append(asyncio.create_task(self._write(arg)))
                
            results = asyncio.gather(*tasks)
            await results

            
    async def _write(self, write_argument: WriteFunctionArgument):
        
        write_function = self._get_function(write_argument.write_function_code)
        function_string = write_function.__doc__.splitlines()[0]
        self._pre_logging(write_argument, function_string)

        write_response = await write_function(
            write_argument.starting_address,
            write_argument.values_to_write, 
            write_argument.unit
            )

        self._update_objects_with_write_values(
            write_response,
            write_argument,
            function_string,
            )
        

    
    async def _read(self, argument: ReadFunctionArgument) -> None:

        read_function = self._get_function(argument.type.FUNCTION_CODE.read)
        function_string = read_function.__doc__.splitlines()[0]

        self._pre_logging(argument, function_string)
        
        read_result = await read_function(
            argument.starting_address,
            argument.size,
            argument.unit
            )
        
        self._update_objects_with_collected_values(
            argument,
            read_result,
            function_string
        )

class AsyncModbusTcpClientWrapper(AsyncModbusBaseClientWrapper, AsyncModbusTcpClient):
    pass


class AsyncModbusUdpClientWrapper(AsyncModbusBaseClientWrapper, AsyncModbusUdpClient):
    pass

