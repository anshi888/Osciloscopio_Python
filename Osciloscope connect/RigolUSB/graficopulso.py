import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import numpy

#Comunicación 
rm = visa.ResourceManager()
print( rm.list_resources() )
#Dirección
osc='USB0::0x1AB1::0x0516::DS8A234200645::INSTR'
myScope = rm.open_resource(osc)
#

#pedir peticion a los datos del osciloscopio
data = myScope.query("WAV:DATA?")
data=data.split(',')
data= list(data)
data=data[10:len(data)-1]
muestra=np.array(data)
#Sampleo muestras
lista_sample=[]
for k in range(len(muestra)-1):
    lista_sample.append(float(muestra[k]))
#Parametros Y graficar limpiar - Voltage
y= [float(x) for x in lista_sample]
#Parametros de tiempo
timeoffset = float(myScope.query(":TIM:OFFS?")[0])
timescale = float(myScope.query(":TIM:SCAL?"))
time = numpy.linspace(timeoffset  * timescale, 0.0000005+50e-09 * timescale, num=len(y))
#Graficar
plt.plot(time,y)
plt.xlabel("Time [seconds]")
plt.ylabel("Volt [V]")
plt.grid()
plt.show()