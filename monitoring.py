from pyspectator.computer import Computer
from pyspectator.convert import UnitByte


class Property():

    def __init__(self):
        self.computer = Computer()

    def _format_bytes(self, byte_value):
        try:
            if (byte_value is None) or (byte_value == 0):
                byte_value = '0'
            elif isinstance(byte_value, (int, float)):
                val, unit = UnitByte.auto_convert(byte_value)
                byte_value = '{:.2f}'.format(val) + \
                             UnitByte.get_name_reduction(unit)
        finally:
            return byte_value

    def _transform_timetable(self, timetable, count=100):
        values = list(timetable.newest_values(count))
        keys = range(len(values))
        collection = list(zip(keys, values))
        return collection

    @property
    def disk_info(self):
        return self.computer.nonvolatile_memory

    @property
    def cpu_info(self):
        return self.computer.processor

    @property
    def mem_info(self):
        return self.computer.virtual_memory

    @property
    def nif(self):
        return self.computer.network_interface

    @property
    def current_user(self):
        return None

    def start(self):
        self.computer.start_monitoring()

    def stop(self):
        self.computer.stop_monitoring()


class Monitoring(Property):
    @property
    def general_info(self):
        total_disk_mem = 0
        for dev in self.disk_info:
            if isinstance(dev.total, (int, float)):
                total_disk_mem += dev.total
        # General information
        info = {
            'os': self.computer.os,
            'architecture': self.computer.architecture,
            'hostname': self.computer.hostname,
            'cpu_name': self.cpu_info.name,
            'boot_time': self.computer.boot_time,
            'raw_uptime': int(self.computer.raw_uptime.total_seconds()),
            'uptime': self.computer.uptime,
            'total_mem': self._format_bytes(self.mem_info.total),
            'total_disk_mem': self._format_bytes(total_disk_mem)
        }
        return info

    @property
    def cpu(self):
        info = {
            'name': self.cpu_info.name,
            'count': self.cpu_info.count,
            'load': self.cpu_info.load if self.cpu_info.load else 0
        }
        return info

    @property
    def disk(self):
        info = list()
        for dev in self.disk_info:
            if dev.used_percent is None:
                used_percent = 0
            else:
                used_percent = dev.used_percent
            info.append({
                'device': dev.device,
                'mountpoint': dev.mountpoint,
                'fstype': dev.fstype,
                'used': self._format_bytes(dev.used),
                'total': self._format_bytes(dev.total),
                'used_percent': used_percent
            })
        return info

    @property
    def network(self):
        info = {
            'hostname': self.computer.hostname,
            'mac_address': self.nif.hardware_address,
            'ip_address': self.nif.ip_address,
            'mask': self.nif.subnet_mask,
            'gateway': self.nif.default_route,
            'bytes_sent': self._format_bytes(self.nif.bytes_sent),
            'bytes_recv': self._format_bytes(self.nif.bytes_recv)
        }
        return info
