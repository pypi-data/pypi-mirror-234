from numbers import Number
from enum import Enum
from math import sqrt
from dataclasses import dataclass

def primeFactors(n: float | int):
    if n == 1:
        return None, None
    elif n == 0:
        return None, None
    negative_powers = False
    if n < 1:
        n = 1//n
        negative_powers = True
    fac = []
    powers = []
    count = 0
    while n % 2 == 0:
        count += 1
        n = n // 2
    fac.append(2) if count > 0 else 0
    powers.append(count) if count > 0 else 0
    # n must be odd at this point
    # so a skip of 2 ( i = i + 2) can be used
    for i in range(3,int(sqrt(n))+1,2):
        # while i divides n , add i to the list
        count = 0
        while n % i== 0:
            count += 1
            n = n // i
        fac.append(i) if count > 0 else 0
        powers.append(count) if count > 0 else 0
    # Condition if n is a prime
    # number greater than 2
    if n > 2:
        fac.append(n)
        powers.append(1) 
    if negative_powers:
        powers = [-e for e in powers]
    return fac, powers 

class Prefix(Enum):
    QUETTA = 1e30
    RONNA  = 1e27
    YOTTA  = 1e24
    ZETTA  = 1e21
    EXA    = 1e18
    PETA   = 1e15
    TERA   = 1e12
    GIGA   = 1e9
    MEGA   = 1e6
    KILO   = 1e3
    HECTO  = 1e2
    DECA   = 1e1
    NONE   = 1
    DECI   = 1e-1
    CENTI  = 1e-2
    MILI   = 1e-3
    MICRO  = 1e-6
    NANO   = 1e-9
    PICO   = 1e-12
    FEMTO  = 1e-15
    ATTO   = 1e-18
    ZEPTO  = 1e-21
    YOCTO  = 1e-24
    RONTO  = 1e-27
    QUECTO = 1e-30
    
    def __mul__(self, other):
        if isinstance(other, Number):
            return other * self.value
        if isinstance(other, Prefix):
            try:
                return Prefix(self.value * other.value)
            except:
                return self.value * other.value
    def __rmul__(self, other):
        if isinstance(other, Number):
            return other * self.value
    def __truediv__(self, other):
        if isinstance(other, Number):
            return self.value / other
        if isinstance(other, Prefix):
            try:
                return Prefix(self.value / other.value)
            except:
                return self.value / other.value
    def __rtruediv__(self, other):
        if isinstance(other, Number):
            return other / self.value
    
    def __float__(self):
        return float(self.value)
    def __int__(self):
        return int(self.value)

    def __str__(self):
        match self:
            case Prefix.QUETTA:
                return "Q"
            case Prefix.RONNA:
                return "R"
            case Prefix.YOTTA:
                return "Y"
            case Prefix.ZETTA: 
                return "Z"
            case Prefix.EXA: 
                return "E"
            case Prefix.PETA:  
                return "P"
            case Prefix.TERA:  
                return "T"
            case Prefix.GIGA:  
                return "G"
            case Prefix.MEGA:  
                return "M"
            case Prefix.KILO:  
                return "k"
            case Prefix.HECTO: 
                return "h"
            case Prefix.DECA:  
                return "da"
            case Prefix.NONE:  
                return ""
            case Prefix.DECI:  
                return "d"
            case Prefix.CENTI: 
                return "c"
            case Prefix.MILI:  
                return "m"
            case Prefix.MICRO: 
                return "µ"
            case Prefix.NANO:  
                return "n"
            case Prefix.PICO:  
                return "p"
            case Prefix.FEMTO: 
                return "f"
            case Prefix.ATTO:  
                return "a"
            case Prefix.ZEPTO: 
                return "z"
            case Prefix.YOCTO: 
                return "y"
            case Prefix.RONTO: 
                return "r"
            case Prefix.QUECTO:
                return "q"

class BasicUnit(Enum):
    METER = 2
    SECOND = 3
    KILOGRAM = 5
    KELVIN = 7
    AMPERE = 11
    MOL = 13
    CANDELA = 17
    HERTZ = 1 / SECOND
    NEWTON = METER * KILOGRAM * (1/SECOND**2)
    def __mul__(self, other):
        if isinstance(other, Number):
            return Quantity(other, Unit(self.value))
        if isinstance(other, Prefix):
            return Quantity(unit=Unit(self.value, other))
        if isinstance(other, BasicUnit):
            return Quantity(unit=Unit(self.value)) * Quantity(unit=Unit(other))
    def __rmul__(self, other):
        if isinstance(other, Number):
            return Quantity(other, Unit(self.value))
        if isinstance(other, Prefix):
            return Quantity(unit=Unit(other, self.value))
    def __truediv__(self, other):
        if isinstance(other, Number):
            return Quantity(1/other, Unit(self.value))
        if isinstance(other, BasicUnit):
            return Quantity(unit=Unit(self.value)) / Quantity(unit=Unit(other))
    def __rtruediv__(self, other):
        if isinstance(other, Number):
            return Quantity(other, Unit(float(1/self)))
        if isinstance(other, BasicUnit):
            return Quantity(unit=Unit(other)) / Quantity(unit=Unit(self.value))

    def __int__(self):
        return int(self.value)
    def __float__(self):
        return float(self.value)

    def __str__(self):
        match self:
            case BasicUnit.METER:
                return "m"
            case BasicUnit.SECOND:
                return "s"
            case BasicUnit.KILOGRAM:
                return "kg"
            case BasicUnit.KELVIN:
                return "K"
            case BasicUnit.AMPERE:
                return "A"
            case BasicUnit.MOL:
                return "mol"
            case BasicUnit.CANDELA:
                return "cd"

@dataclass
class Unit:
    unit: float
    prefix: float = 1
    
    def __mul__(self, other):
        if isinstance(other, Unit):
            self.prefix *= other.prefix
            self.unit *= other.unit
            return self
        if isinstance(other, BasicUnit):
            self.unit *= other.value
            return self
        if isinstance(other, Prefix):
            self.prefix *= other.value
            return self
    def __rmul__(self, other):
        if isinstance(other, BasicUnit):
            self.unit *= other.value
            return self
        if isinstance(other, Prefix):
            self.prefix *= other.value
            return self
    def __truediv__(self, other):
        if isinstance(other, Unit):
            self.prefix /= other.prefix
            self.unit /= other.unit
            return self
        if isinstance(other, BasicUnit):
            self.unit /= other.value
            return self
        if isinstance(other, Prefix):
            self.prefix /= other.value
            return self
    def __rtruediv__(self, other):
        if isinstance(other, Number):
            self.unit = 1 / self.unit
            return self
        if isinstance(other, BasicUnit):
            self.unit = other.value / self.unit
            return self
        if isinstance(other, Prefix):
            self.prefix = other.value / self.prefix
            return self

class Quantity:
    def __init__(self, value = None, unit: Unit = 0) -> None:
        self._value = value
        self._unit: Unit = unit
        
    def __mul__(self, other):
        if isinstance(other, Number):
            self._value *= other
            return self
        if isinstance(other, BasicUnit):
            self._unit *= other
            return self
        if isinstance(other, Prefix):
            self._unit *= other
            return self
        if isinstance(other, Unit):
            self._unit *= other
            return self
        if isinstance(other, Quantity):
            self._value *= other._value
            self._unit *= other._unit
            return self
    def __rmul__(self, other):
        if isinstance(other, Number):
            self._value *= other
            return self
        if isinstance(other, BasicUnit):
            self._unit *= other
            return self
        if isinstance(other, Prefix):
            self._unit *= other
            return self
        if isinstance(other, Unit):
            self._unit *= other
            return self
    def __truediv__(self, other):
        if isinstance(other, Number):
            self._value /= other
            return self
        if isinstance(other, BasicUnit):
            self._unit /= other
            return self
        if isinstance(other, Prefix):
            self._unit /= other
            return self
        if isinstance(other, Quantity):
            self._value /= other._value
            self._unit /= other._unit
            return self
        if isinstance(other, Unit):
            self._unit /= other
            return self
    def __rtruediv__(self, other):
        if isinstance(other, Number):
            self._value = other / self._value
            self._unit = 1 / self._unit
            return self
        if isinstance(other, BasicUnit):
            self._unit = other / self._unit
            return self
        if isinstance(other, Prefix):
            self._unit = other / self._unit
            return self
        if isinstance(other, Unit):
            self._unit = other / self._unit
            return self
    
    def __str__(self) -> str:
        top, bottom = self._unit.unit.as_integer_ratio()
        primes_top, powers_top = primeFactors(top)
        primes_bottom, powers_bottom = primeFactors(bottom)
        powers_bottom = [-e for e in powers_bottom]
        primes = primes_top + primes_bottom
        powers = powers_top + powers_bottom
        if primes == None:
            return str(self._value * self._unit.prefix)
        unit_str = f"{BasicUnit(primes[0])}^{powers[0]}" if powers[0] != 1 else f"{BasicUnit(primes[0])}"
        for i in range(1, len(primes)):
            unit_str += " * "
            unit_str += f"{BasicUnit(primes[i])}^{powers[i]}" if powers[i] != 1 else f"{BasicUnit(primes[i])}"
        return str(self._value * self._unit.prefix) + " " + unit_str if self._value != None else unit_str

a = 5
a *= BasicUnit.METER
a *= BasicUnit.SECOND
b = 1 * BasicUnit.NEWTON
print(a/b) 