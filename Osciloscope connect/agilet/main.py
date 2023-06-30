import pyvisa as visa
rm = visa.ResourceManager()
print( rm.list_resources() ) #Lista de dispositivos conectados
#Agilet DSO X 2012A
osc='USB0::0x0957::0x1799::MY50210121::INSTR'

myScope = rm.open_resource(osc)
print(myScope.query("*IDN?"))
#AGILENT TECHNOLOGIES,DSO-X 2012A,MY50210121,01.10.2011042700
myScope.write("WGEN:FREQ 50000") #connect the wavegen to channel 1
myScope.write(":TIMebase:SCALe 100.0E-6")
