import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

#Comunicación 
rm = visa.ResourceManager()
print( rm.list_resources() )
#Dirección
osc='USB0::0x1AB1::0x0516::DS8A234200645::INSTR'
scope = rm.open_resource(osc)
#
print(scope)