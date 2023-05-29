from machine import Pin

is_enable = False

class Battery:
    def __init__(self) -> None:
        pass
    
    def enable_battery_power(self):
        global is_enable
        is_enable = True
        Pin('A13', Pin.OUT).value(1) # 启用电池对主控供电
    
    def disable_battery_power(self):
        global is_enable
        is_enable = False
        Pin('A13', Pin.OUT).value(0)
    
    def is_enable(self):
        global is_enable
        return is_enable

class PowerSupply:
    def __init__(self) -> None:
        pass
    
    def enable_power_supply(self):
        global is_enable
        is_enable = True
        Pin('A14', Pin.OUT).value(1) # 使能 Port A-F 对外3v3供电
    
    def disable_power_supply(self):
        global is_enable
        is_enable = False
        Pin('A14', Pin.OUT).value(0)
    
    def is_enable(self):
        global is_enable
        return is_enable    